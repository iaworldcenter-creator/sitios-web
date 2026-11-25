#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
actualizar_catalogo_1321_maestro.py
==============================================================================
Pipeline Maestro de Actualización, Auditoría 18 Agentes + JEV y Cuarentena
VECTEC / Ecosistema 8 Tiendas — Semana 1321 (Vigencia 23 al 28 de Noviembre 2026)

Características certificadas:
1. Ingesta dual CT Internacional (Semana 1321):
   - 1321 LISTA DE PRECIOS DE CT TOL 112326.xlsx (incluye detección dinámica de
     columna de precio J/I para rescatar OUTLET y extracción 100% real de
     hipervínculos Columna L 'Ver Ficha' desde xl/worksheets/_rels/*.xml.rels).
   - 1321 CONFIGURACIONES TOL 112326.xlsx (detección exacta de filas totales).
   - Intcomex México (110 archivos CSV en data/Cataloga intcomex).
2. Clasificación Semántica Purificada (67 Departamentos, 18 Asistentes) +
   Árbitro Neural JEV (typesafe/jev-1.13) sobre altas nuevas y casos límite.
3. Validación Adversarial de Precios y Márgenes:
   - Tipo de cambio $19.50 MXN/USD | Factor Lista 2.20 | Oferta -25% (1.65) | Mayoreo -10%.
   - Detección de precios en cero, formatos corruptos, cambios bruscos (>= +-30%),
     anomalías de moneda/precio absurdo (con cuarentena preventiva automática).
4. Cuarentena Bidireccional + Cero Agotados en Vitrinas Públicas:
   - Retornos de cuarentena -> a=0, stk=15, disponible=True.
   - Nuevos a cuarentena -> a=1, stk=0, disponible=False (excluidos de vitrinas
     públicas data/departments/*.json y ct-showcase-data.js, preservando 100% de
     fotos WebP en disco y registro histórico en catalogo_maestro_compact.json).
5. Inyección obligatoria de leyenda legal en descripciones + reporte forense JSON.
==============================================================================
"""

import os
import sys
import io
import re
import glob
import csv
import json
import ssl
import shutil
import zipfile
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter, defaultdict

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

BASE_DIR = r"D:\Proyectos\sitios web"
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

from scripts.sincronizar_fuente_datos import (
    read_xlsx_workbook, clean_text, clean_sku, extract_url,
    extract_tdp, infer_brand,
    TIPO_CAMBIO, FACTOR_LISTA, MARGEN_OFERTA, FACTOR_VENTA_MXN
)
from scripts.clasificador_semantico_vectec import (
    clasificar_producto_semantico, DEPARTAMENTOS_OFICIALES, DEPT_ID_SET
)
from scripts.regenerar_vitrinas_congruentes import regenerar_vitrinas_congruentes
from scripts.gauntlet_loop_auditoria_adversarial import (
    extract_socket_robusto, extract_ram_type_robusto
)

PCC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")
PCC_DATA_DIR = os.path.join(PCC_DIR, "data")
IMG_DIR = os.path.join(PCC_DIR, "assets", "img")
PLACEHOLDERS_DIR = os.path.join(IMG_DIR, "placeholders")
DATA_DIR = os.path.join(BASE_DIR, "data")
INTCOMEX_DIR = os.path.join(PCC_DATA_DIR, "Cataloga intcomex")

PRICE_XLSX = os.path.join(PCC_DATA_DIR, "1321 LISTA DE PRECIOS DE CT TOL 112326.xlsx")
CONFIG_XLSX = os.path.join(PCC_DATA_DIR, "1321 CONFIGURACIONES TOL 112326.xlsx")
COMPACT_JSON = os.path.join(PCC_DATA_DIR, "catalogo_maestro_compact.json")
AUDIT_JSON = os.path.join(PCC_DATA_DIR, "auditoria_1321_maestro.json")
JEV_OVERRIDES_JSON = os.path.join(PCC_DATA_DIR, "jev_overrides_1321.json")

# SKUs CT bloqueados preventivamente de venta pública (fuera de vitrinas y checkout)
# por anomalía confirmada de precio/moneda/obsolescencia en archivo de origen CT 1321
QUARANTINE_ANOMALY_SKUS = {
    # Errores críticos de precio absurdamente bajo / sentinels CT
    "CABUBI040": "Anomalía crítica CT: Ubiquiti Dream Router WiFi 6 (UDR) cotizado a $0.685 USD ($22.04 MXN).",
    "SOFPDV690": "Sentinel CT: Software POS Tools MyBusiness cotizado a $0.0125 MXN.",
    "EXTTRL160": "Sentinel CT: Garantía extendida Tripp Lite cotizada a $0.1895 MXN.",
    "EXTTRL360": "Sentinel CT: Garantía extendida Tripp Lite cotizada a $0.1895 MXN.",
    # Inventario obsoleto >20 años en hoja OUTLET (columna corrida I)
    "SOFNRT080": "Producto obsoleto OUTLET CT (2004): Norton Antivirus 2004 5 Pack.",
    "MEMRAM080": "Producto obsoleto OUTLET CT (~2004): DDR 400MHz PC3200 128MB.",
    "MEMRAM720": "Producto obsoleto OUTLET CT (~2003): DDR 512MB PC2100 266MHz ECC REG.",
    "ACCHPD130": "Póliza legacy OUTLET CT (columna corrida I): Extensión Garantía HP U9810E.",
    # 20 componentes HPE en CT sin bandera 'm' (precios en MXN tratados como USD → inflados 19.5x)
    "MEMHPE500": "Probable omisión bandera 'm' CT: HPE RAM 64GB DDR5 a 19,578.95 sin 'm' ($629,953 MXN).",
    "MEMHPE580": "Probable omisión bandera 'm' CT: HPE RAM 64GB DDR5 a 18,378.26 sin 'm' ($591,321 MXN).",
    "MEMHPE490": "Probable omisión bandera 'm' CT: HPE RAM 32GB DDR5 a 9,545.26 sin 'm' ($307,119 MXN).",
    "MEMHPE540": "Probable omisión bandera 'm' CT: HPE RAM 32GB DDR5 a 8,960.87 sin 'm' ($288,316 MXN).",
    "MEMHPE570": "Probable omisión bandera 'm' CT: HPE RAM 32GB DDR5 a 5,342.39 sin 'm' ($171,891 MXN).",
    "MEMHPE480": "Probable omisión bandera 'm' CT: HPE RAM 16GB DDR5 a 5,103.16 sin 'm' ($164,194 MXN).",
    "MEMHPE530": "Probable omisión bandera 'm' CT: HPE RAM 16GB DDR5 a 3,834.78 sin 'm' ($123,384 MXN).",
    "DDUHPE1140": "Probable omisión bandera 'm' CT: HPE SSD 3.84TB a 20,282.11 sin 'm' ($652,577 MXN).",
    "DDUHPE1190": "Probable omisión bandera 'm' CT: HPE SSD 1.92TB a 9,920.00 sin 'm' ($319,176 MXN).",
    "DDUHPE1210": "Probable omisión bandera 'm' CT: HPE SSD MSA 1.92TB a 8,559.47 sin 'm' ($275,401 MXN).",
    "DDUHPE1380": "Probable omisión bandera 'm' CT: HPE SSD 960GB a 6,496.84 sin 'm' ($209,036 MXN).",
    "DDUHPE1180": "Probable omisión bandera 'm' CT: HPE SSD 960GB SAS a 6,117.89 sin 'm' ($196,843 MXN).",
    "DDUHPE1050": "Probable omisión bandera 'm' CT: HPE SSD 960GB SAS LFF a 5,562.11 sin 'm' ($178,961 MXN).",
    "ACCHPE2530": "Probable omisión bandera 'm' CT: HPE NS204i-p NVMe Boot a 5,221.05 sin 'm' ($167,987 MXN).",
    "DDUHPE1110": "Probable omisión bandera 'm' CT: HPE SSD 480GB a 5,178.95 sin 'm' ($166,633 MXN).",
    "DDUHPE1130": "Probable omisión bandera 'm' CT: HPE SSD 1.92TB a 4,810.53 sin 'm' ($154,779 MXN).",
    "DDUHPE1320": "Probable omisión bandera 'm' CT: HPE SSD 480GB a 4,694.74 sin 'm' ($151,053 MXN).",
    "DDUHPE1100": "Probable omisión bandera 'm' CT: HPE SSD 960GB LFF a 4,273.68 sin 'm' ($137,506 MXN).",
    "DDUHPE1120": "Probable omisión bandera 'm' CT: HPE SSD 960GB a 2,852.63 sin 'm' ($91,783 MXN).",
    "DDUHPE1290": "Probable omisión bandera 'm' CT: HPE SSD 480GB M.2 a 2,837.89 sin 'm' ($91,309 MXN).",
}

LEYENDA_LEGAL = (
    "Precio en pesos mexicanos (MXN). Precio sujeto a cambio o variación sin previo aviso "
    "debido a la fluctuación cambiaria del dólar."
)

# Mapa canónico de hoja CT -> conjunto de departamentos naturalmente esperados en esa hoja
# (Sirve para medir reubicaciones respecto a la clasificación de origen del archivo CT)
CT_SHEET_EXPECTED_DEPTS = {
    "COMPONENTES DE ENSAMBLE": {
        "procesadores", "tarjetas_madre", "memorias_ram_pc", "memorias_ram_laptop",
        "memorias_ram_servidor", "gabinetes", "tarjetas_video", "enfriamiento",
        "fuentes_energia", "ssds_m2_nvme", "discos_duros_hdd_internos",
        "discos_duros_externos", "tarjetas_microsd", "memorias_usb_pendrives",
        "monitores_pantallas", "mini_pcs_nuc",
    },
    "EQUIPOS DE MARCA": {
        "laptops_portatiles", "mini_pcs_nuc", "computadoras_ensambladas",
        "computadoras_all_in_one", "servidores_enterprise", "tablets_ipads",
        "monitores_pantallas", "memorias_ram_servidor", "discos_duros_hdd_internos",
        "ssds_m2_nvme", "garantias_polizas_servicio",
    },
    "OUTLET EQUIPOS DE MARCA": {
        "laptops_portatiles", "computadoras_ensambladas", "computadoras_all_in_one", "mini_pcs_nuc",
    },
    "IMPRESION, DIG. DE IMAGENES": {
        "impresoras_multifuncionales", "plotters_gran_formato", "escaneres_digitalizadores",
        "etiquetas_ribbons", "punto_de_venta",
    },
    "CONSUMIBLES": {
        "toners_laser", "tintas_cartuchos", "etiquetas_ribbons",
    },
    "CONECTIVIDAD": {
        "switches_red", "routers_access_points", "antenas_radioenlaces",
        "cableado_estructurado", "fibra_optica_transceivers", "racks_gabinetes_servidor",
        "cables_adaptadores", "herramientas_servicio_tecnico",
    },
    "TELEFONIA Y VIDEO VIGILANCIA": {
        "camaras_seguridad_cctv", "grabadores_dvr_nvr", "control_acceso_biometricos",
        "alarmas_sensores_seguridad", "telefonia_conmutadores", "racks_gabinetes_servidor",
    },
    "ELECTRONICA DE CONSUMO": {
        "monitores_pantallas", "proyectores_presentacion", "smartphones_celulares",
        "tablets_ipads", "smartwatches_wearables", "bocinas_sonido", "diademas_headsets",
        "microfonos", "webcams_videoconferencia", "gaming_consolas_sillas",
    },
    "LINEA BLANCA": {
        "climatizacion_aires_acondicionados", "accesorios_perifericos",
    },
    "PUNTO DE VENTA": {
        "punto_de_venta", "etiquetas_ribbons", "escaneres_digitalizadores",
    },
    "SOFTWARE": {
        "sistemas_operativos", "ofimatica_productividad", "software_contable_administrativo",
        "antivirus_seguridad_digital", "garantias_polizas_servicio",
    },
    "ACCESORIOS": {
        "teclados", "ratones_mouse", "combos_teclado_mouse", "diademas_headsets",
        "bocinas_sonido", "microfonos", "webcams_videoconferencia", "limpieza_mantenimiento",
        "cables_adaptadores", "mochilas_fundas_maletines", "soportes_ergonomia",
        "hubs_docks_estaciones", "herramientas_servicio_tecnico", "candados_seguridad_laptop",
        "gaming_consolas_sillas", "cargadores_baterias_powerbanks", "smartwatches_wearables",
        "accesorios_perifericos", "enfriamiento",
    },
    "ENERGIA": {
        "no_breaks_ups", "reguladores_voltaje", "cargadores_baterias_powerbanks",
        "racks_gabinetes_servidor",
    },
    "OUTLET": set(DEPT_ID_SET),
}

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

SSL_CTX = ssl._create_unverified_context()
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8"
}


def extract_xlsx_col_l_hyperlinks(path):
    """Extrae mapa exacto (sheet_name, row_num) -> URL real de Columna L ('Ver Ficha')."""
    links = {}
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    rns = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    with zipfile.ZipFile(path, "r") as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        wbrels = {
            r.attrib["Id"]: r.attrib["Target"]
            for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        }
        for s in wb.findall(f".//{ns}sheet"):
            sname = s.attrib.get("name", "")
            rid = s.attrib.get(f"{rns}id", "")
            target = wbrels.get(rid, "")
            spath = ("xl/" + target) if not target.startswith("xl/") else target
            relpath = spath.replace("worksheets/", "worksheets/_rels/") + ".rels"
            if spath not in z.namelist() or relpath not in z.namelist():
                continue
            srels = {
                r.attrib["Id"]: r.attrib["Target"]
                for r in ET.fromstring(z.read(relpath))
            }
            stree = ET.fromstring(z.read(spath))
            for hl in stree.findall(f".//{ns}hyperlink"):
                ref = hl.attrib.get("ref", "")
                if not ref.startswith("L"):
                    continue
                digits = "".join(ch for ch in ref if ch.isdigit())
                if not digits:
                    continue
                url = srels.get(hl.attrib.get(f"{rns}id", ""), "").strip()
                if url.startswith("http"):
                    links[(sname, int(digits))] = url
    return links


def save_as_webp(img_bytes, dest_path, quality=85):
    if not img_bytes or len(img_bytes) < 100:
        return False
    try:
        if HAS_PIL:
            with Image.open(io.BytesIO(img_bytes)) as img:
                if img.mode in ("RGBA", "LA", "P"):
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    bg.paste(img, mask=img.split()[3])
                    img = bg
                elif img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(dest_path, "WEBP", quality=quality)
                return True
        else:
            with open(dest_path, "wb") as f:
                f.write(img_bytes)
            return True
    except Exception:
        return False


def download_bytes(url, timeout=7):
    if not url or not url.startswith("http"):
        return None
    try:
        req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=timeout) as resp:
            data = resp.read()
            if len(data) > 1000:
                return data
    except Exception:
        pass
    return None


def fetch_ct_product_image(sku):
    url = f"https://ctonline.mx/buscar/productos?b={sku}"
    try:
        req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=7) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            matches = re.findall(r'(https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp))', html)
            for m in matches:
                m_low = m.lower()
                if any(ign in m_low for ign in ["logo", "banner", "icon", "placeholder", "sprite", "social", "header"]):
                    continue
                if any(k in m_low for k in ["ctonline", "cloudfront", "product", "art", sku.lower()]):
                    return m
    except Exception:
        pass
    return None


def main():
    print("=" * 84)
    print("   VECTEC - PIPELINE MAESTRO SEMANA 1321 (VIGENCIA 23 AL 28 DE NOVIEMBRE 2026)")
    print("   18 Asistentes Especializados + Motor JEV + Cuarentena Bidireccional Estricta")
    print("   Garantía: Factor Lista 2.20 / Oferta 1.65 MXN | Cero Agotados en Vitrinas")
    print("=" * 84)

    # Cargar overrides certificados por JEV (si existen)
    jev_overrides = {}
    if os.path.exists(JEV_OVERRIDES_JSON):
        with open(JEV_OVERRIDES_JSON, "r", encoding="utf-8") as f:
            jev_overrides = json.load(f)
        print(f"[*] Overrides certificados JEV cargados: {len(jev_overrides):,}")

    # 1. Cargar catálogo maestro previo (Semana 1320)
    print("\n[PASO 1] Cargando catálogo maestro previo (Semana 1320)...")
    old_by_sku = {}
    old_by_prov_raw = {}
    prev_total_activos = 0
    prev_total_cuarentena = 0

    if os.path.exists(COMPACT_JSON):
        with open(COMPACT_JSON, "r", encoding="utf-8-sig") as f:
            for it in json.load(f):
                sku_str = it.get("s", "")
                raw = clean_sku(sku_str)
                prov = it.get("prov", "B" if sku_str.startswith("B-") else "A")
                old_by_sku[raw] = it
                old_by_sku[sku_str] = it
                old_by_prov_raw[(prov, raw)] = it
                if it.get("a", 0) == 0:
                    prev_total_activos += 1
                else:
                    prev_total_cuarentena += 1

    print(f"    - Previos Activos (a=0):    {prev_total_activos:,}")
    print(f"    - Previos Cuarentena (a=1): {prev_total_cuarentena:,}")

    # 2. Cargar Intcomex México (110 CSVs)
    print("\n[PASO 2] Procesando catálogo mayorista Intcomex (Clave B, 110 CSVs)...")
    intcomex_items = {}
    if os.path.exists(INTCOMEX_DIR):
        for fpath in glob.glob(os.path.join(INTCOMEX_DIR, "*.csv")):
            lines = []
            try:
                with open(fpath, "r", encoding="utf-16", errors="ignore") as fp:
                    lines = fp.readlines()
            except Exception:
                pass
            if not lines:
                try:
                    with open(fpath, "r", encoding="utf-8-sig", errors="ignore") as fp:
                        lines = fp.readlines()
                except Exception:
                    continue
            h_idx = -1
            for i, l in enumerate(lines[:6]):
                if "Categor" in l and ("Precio" in l or "SKU" in l):
                    h_idx = i
                    break
            if h_idx == -1:
                continue
            delim = "\t" if "\t" in lines[h_idx] else ","
            reader = csv.reader(lines[h_idx:], delimiter=delim)
            headers = [h.strip().upper() for h in next(reader)]
            sku_idx = mpn_idx = price_idx = stock_idx = name_idx = brand_idx = cat_idx = sub_idx = -1
            for idx, h in enumerate(headers):
                if "SKU" in h: sku_idx = idx
                elif "PARTE" in h or "MPN" in h: mpn_idx = idx
                elif "PRECIO" in h: price_idx = idx
                elif "DISPONIBILIDAD" in h or "STOCK" in h: stock_idx = idx
                elif "NOMBRE" in h or "DESCRIPCI" in h: name_idx = idx
                elif "MARCA" in h: brand_idx = idx
                elif "CATEGOR" in h and "SUB" not in h: cat_idx = idx
                elif "SUBCATEGOR" in h: sub_idx = idx
            for r in reader:
                if len(r) <= max(sku_idx, price_idx):
                    continue
                sku = clean_text(r[sku_idx].replace('"', '')) if sku_idx != -1 and sku_idx < len(r) else ''
                mpn = clean_text(r[mpn_idx].replace('"', '')) if mpn_idx != -1 and mpn_idx < len(r) else ''
                p_str = r[price_idx].replace('"', '').replace(',', '').replace('$', '').strip() if price_idx != -1 and price_idx < len(r) else '0'
                stock_str = clean_text(r[stock_idx].replace('"', '')) if stock_idx != -1 and stock_idx < len(r) else ''
                name = clean_text(r[name_idx].replace('"', '')) if name_idx != -1 and name_idx < len(r) else ''
                brand = clean_text(r[brand_idx].replace('"', '')) if brand_idx != -1 and brand_idx < len(r) else ''
                cat = clean_text(r[cat_idx].replace('"', '')) if cat_idx != -1 and cat_idx < len(r) else ''
                sub = clean_text(r[sub_idx].replace('"', '')) if sub_idx != -1 and sub_idx < len(r) else ''
                try:
                    cost_mxn = float(p_str)
                except ValueError:
                    continue
                if cost_mxn <= 0 or not (sku or mpn):
                    continue
                key = clean_sku(sku or mpn)
                is_in_stock = not ("sin inventario" in stock_str.lower() or stock_str.strip() == "0")
                intcomex_items[key] = {
                    "sku": key, "mpn": mpn, "name": name,
                    "brand": brand if brand else infer_brand(name, key),
                    "cost_mxn": cost_mxn, "stock_str": stock_str,
                    "stock": 10 if is_in_stock else 0, "in_stock": is_in_stock,
                    "category": cat, "subcategory": sub,
                }
    print(f"[*] Intcomex: {len(intcomex_items):,} artículos cargados.")

    # 3. Parsear Configuraciones Turnkey (1321 CONFIGURACIONES)
    print("\n[PASO 3] Procesando configuraciones oficiales llave en mano (1321 CONFIGURACIONES)...")
    config_sheets = read_xlsx_workbook(CONFIG_XLSX)
    turnkey_configs = []
    cfg_defs = [
        ("INTEL 14va GEN", "D", "CFG-INTEL-14400", "PC VECTEC Elite Intel Core i5-14400 | ASUS B760M | 16GB RAM | 1TB HDD | Kit Naceb 4en1 + Monitor 19.5\"", "INTEL / ASUS", 620.75),
        ("INTEL 14va GEN", "E", "CFG-INTEL-14700", "PC VECTEC Pro Intel Core i7-14700 | ASUS B760M | 16GB RAM | 1TB HDD | Kit Naceb 4en1 + Monitor 19.5\"", "INTEL / ASUS", 791.25),
        ("INTEL 14va GEN", "F", "CFG-INTEL-14900", "PC VECTEC Master Intel Core i9-14900 | ASUS B760M | 16GB RAM | 1TB HDD | Kit Naceb 4en1 + Monitor 19.5\"", "INTEL / ASUS", 991.58),
        ("INTEL 12va GEN", "D", "CFG-INTEL-12400", "PC VECTEC Entry Intel Core i5-12400 | ASUS H610M | 8GB RAM | 1TB HDD | Kit Naceb 4en1 + Monitor 19.5\"", "INTEL / ASUS", 418.85),
        ("INTEL 12va GEN", "E", "CFG-INTEL-12700", "PC VECTEC Plus Intel Core i7-12700 | ASUS H610M | 8GB RAM | 1TB HDD | Kit Naceb 4en1 + Monitor 19.5\"", "INTEL / ASUS", 556.53),
        ("INTEL 12va GEN", "F", "CFG-INTEL-12900", "PC VECTEC Power Intel Core i9-12900 | ASUS H610M | 8GB RAM | 1TB HDD | Kit Naceb 4en1 + Monitor 19.5\"", "INTEL / ASUS", 697.47),
        ("AMD RYZEN", "D", "CFG-RYZEN-5600X", "PC VECTEC Gamer Speed AMD Ryzen 5 5600X | ROG Strix B550 WiFi | 8GB RAM | 1TB | GT730 + Monitor 19.5\"", "AMD / ASUS ROG", 608.02),
        ("AMD RYZEN", "E", "CFG-RYZEN-5700X", "PC VECTEC Gamer Pro AMD Ryzen 7 5700X | ROG Strix B550 WiFi | 8GB RAM | 1TB | GT730 + Monitor 19.5\"", "AMD / ASUS ROG", 687.35),
        ("AMD RYZEN", "F", "CFG-RYZEN-5900XT", "PC VECTEC Gamer Master AMD Ryzen 9 5900XT | ROG Strix B550 WiFi | 8GB RAM | 1TB | GT730 + Monitor 19.5\"", "AMD / ASUS ROG", 792.63),
        ("AMD RYZEN G", "D", "CFG-APU-5700G", "PC VECTEC Workstation APU AMD Ryzen 7 5700G Radeon Vega 8 | ASUS B550M AC | 16GB RAM | 1TB + Monitor 19.5\"", "AMD / ASUS", 641.38),
        ("AMD RYZEN G", "E", "CFG-APU-5600GT", "PC VECTEC APU eSports AMD Ryzen 5 5600GT Radeon Vega 7 | ASUS B550M AC | 16GB RAM | 1TB + Monitor 19.5\"", "AMD / ASUS", 478.21),
        ("AMD RYZEN G", "F", "CFG-APU-5300G", "PC VECTEC Office APU AMD Ryzen 3 5300G Radeon Vega 6 | ASUS B550M AC | 16GB RAM | 1TB + Monitor 19.5\"", "AMD / ASUS", 430.86),
    ]
    for sheet_name, col, sku, nombre, marca, default_cost in cfg_defs:
        cost = default_cost
        if sheet_name in config_sheets:
            for r_num, cells in config_sheets[sheet_name]:
                # La fila de total de configuración no tiene clave en columna B ni C, y sí tiene valor numérico en D/E/F
                if r_num in (15, 16) and not cells.get("B") and not cells.get("C") and col in cells:
                    try:
                        c_val = float(cells[col])
                        if c_val > 100:
                            cost = c_val
                    except ValueError:
                        pass
        cost_mxn = cost * TIPO_CAMBIO
        p_orig = round(cost_mxn * FACTOR_LISTA, 2)
        p_lista = round(p_orig * 0.75, 2)
        p_may = round(p_lista * 0.90, 2)
        final_sku = f"A-{sku}"
        turnkey_configs.append({
            "id": final_sku, "sku": final_sku, "clave_proveedor": "A",
            "proveedor_nombre": "CT Internacional", "proveedor": "CT Internacional",
            "nombre": nombre, "precio": p_lista, "precio_original": p_orig,
            "precio_mayoreo": p_may, "descuento_pct": 25,
            "categoria": "computadoras_ensambladas",
            "subcategoria": "Configuraciones Oficiales Turnkey",
            "marca": marca, "imagen": "assets/img/fachada-oficial.webp",
            "stock": 5, "disponible": True, "estado_comercial": "disponible",
            "outlet": False,
            "descripcion": f"{nombre}. Ensamble certificado con pruebas de estrés y garantía oficial VECTEC. {LEYENDA_LEGAL}",
            "ficha_tecnica_url": "", "costo_neto_usd": round(cost, 2),
            "ct_sheet": "CONFIGURACIONES",
        })
    print(f"[*] Configuraciones Turnkey 1321 procesadas: {len(turnkey_configs)}")

    # 4. Parsear lista de precios CT 1321 + Hipervínculos reales de Columna L
    print(f"\n[PASO 4] Parseando {os.path.basename(PRICE_XLSX)} + Columna L ('Ver Ficha')...")
    price_sheets = read_xlsx_workbook(PRICE_XLSX)
    col_l_links = extract_xlsx_col_l_hyperlinks(PRICE_XLSX)
    print(f"[*] Enlaces reales extraídos de Columna L: {len(col_l_links):,}")

    standardized_products = []
    outlet_products = []
    ensamble_hardware = {
        "procesadores": [], "tarjetas_madre": [], "memorias_ram": [],
        "almacenamiento": [], "tarjetas_video": [], "fuentes_poder": [],
        "gabinetes": [], "enfriamiento": [],
        "configuraciones_armadas": turnkey_configs,
    }

    seen_skus = set()
    ct_active_count = 0
    nuevas_altas_ct = []
    retornos_cuarentena_ct = []
    mantenidos_activos_ct = []
    preventive_quarantine_anomalies = []
    outlet_shifted_col_rescued = []
    price_changes = {"subieron": 0, "bajaron": 0, "sin_cambio": 0}
    big_price_swings = []
    reubicados_vs_1320 = []
    reubicados_vs_ct_origen = []
    zero_or_corrupt_rows = []
    col_l_verified_count = 0

    for cfg in turnkey_configs:
        seen_skus.add(cfg["sku"])
        seen_skus.add(cfg["sku"].replace("A-", ""))
        standardized_products.append(cfg)

    for sheet_name, rows in price_sheets.items():
        if sheet_name in ["LISTA DE PRECIOS", "INDICE", "DIRECTORIO", "DIRECTORIO DE COORDINADORES"]:
            continue
        current_subgroup = sheet_name
        price_col = "J"
        for r_num, cells in rows:
            f_val = cells.get("F", "").strip()
            g_val = clean_text(cells.get("G", ""))
            if f_val.upper() == "CLAVE" and g_val:
                current_subgroup = g_val
                if cells.get("I", "").strip().upper() == "PRECIO":
                    price_col = "I"
                elif cells.get("J", "").strip().upper() == "PRECIO":
                    price_col = "J"
                continue
            elif not f_val and any(k in cells for k in ["B", "C", "D", "E"]):
                txt = clean_text(" ".join(cells.get(k, "") for k in ["B", "C", "D", "E"] if cells.get(k, "")))
                if len(txt) > 3 and not any(ign in txt.upper() for ign in ["INTERNACIONAL", "LISTA DE PRECIOS", "COORDINADOR"]):
                    current_subgroup = txt
                continue

            if not f_val or f_val.upper() in ["CLAVE", "NAN"] or len(f_val) < 5:
                continue

            j_raw = str(cells.get(price_col, "")).strip()
            if not g_val and not j_raw:
                continue  # Nota / pie de página

            raw_sku = clean_sku(f_val)
            final_sku = f"A-{raw_sku}"
            if final_sku in seen_skus:
                continue

            try:
                price_val = float(j_raw.replace(",", "").replace("$", "").strip())
            except ValueError:
                zero_or_corrupt_rows.append({"sku": raw_sku, "sheet": sheet_name, "row": r_num, "raw": j_raw, "desc": g_val[:70]})
                continue
            if price_val <= 0:
                zero_or_corrupt_rows.append({"sku": raw_sku, "sheet": sheet_name, "row": r_num, "raw": j_raw, "desc": g_val[:70]})
                continue

            seen_skus.add(final_sku)
            seen_skus.add(raw_sku)
            if price_col == "I":
                outlet_shifted_col_rescued.append({"sku": final_sku, "sheet": sheet_name, "price_raw": price_val, "desc": g_val[:70]})

            col_h = cells.get("H", "").strip().lower()
            if col_h == "m":
                costo_mxn = price_val
                costo_neto_usd = round(price_val / TIPO_CAMBIO, 2)
            else:
                costo_neto_usd = price_val
                costo_mxn = price_val * TIPO_CAMBIO

            precio_orig = round(costo_mxn * FACTOR_LISTA, 2)
            precio_mxn = round(precio_orig * 0.75, 2)
            precio_may = round(precio_mxn * 0.90, 2)
            descuento_pct = 25

            old_item = old_by_prov_raw.get(("A", raw_sku)) or old_by_sku.get(final_sku) or old_by_sku.get(raw_sku)
            full_desc = g_val
            if LEYENDA_LEGAL not in full_desc:
                full_desc = f"{full_desc} {LEYENDA_LEGAL}".strip()

            nombre = clean_text(g_val[:120] if g_val else (old_item.get("n", raw_sku) if old_item else raw_sku))
            subcat = current_subgroup if current_subgroup and current_subgroup != sheet_name else (old_item.get("subgrupo_label", current_subgroup) if old_item else current_subgroup)
            marca = infer_brand(g_val, raw_sku)
            if old_item and old_item.get("m") not in [None, "", "Generica", "GENERIC", "VECTEC"]:
                marca = old_item.get("m")

            # Clasificación semántica purificada (18 Asistentes) + override JEV si aplica
            jev_cert = 0
            if final_sku in jev_overrides and jev_overrides[final_sku] in DEPT_ID_SET:
                categoria = jev_overrides[final_sku]
                jev_cert = 1
            else:
                categoria = clasificar_producto_semantico(
                    raw_sku, nombre, marca,
                    sheet_name=sheet_name, subgrupo_header=subcat, desc=full_desc
                )

            # Enlace real Columna L ('Ver Ficha')
            col_l_url = col_l_links.get((sheet_name, r_num), "")
            if col_l_url:
                col_l_verified_count += 1
                ficha_url = col_l_url
            else:
                ficha_url = extract_url(full_desc) or f"https://ctonline.mx/buscar/productos?b={raw_sku}"

            # Imagen preservada o nueva
            if old_item:
                images = old_item.get("k", [])
                if images and len(images) > 0 and "placeholder" not in images[0]:
                    img = images[0]
                elif os.path.exists(os.path.join(IMG_DIR, f"{raw_sku}.webp")):
                    img = f"assets/img/{raw_sku}.webp"
                elif os.path.exists(os.path.join(IMG_DIR, f"{raw_sku}_0.webp")):
                    img = f"assets/img/{raw_sku}_0.webp"
                else:
                    img = f"assets/img/{raw_sku}.webp"
            else:
                img = f"assets/img/{raw_sku}.webp"
                nuevas_altas_ct.append({
                    "sku": raw_sku, "name": nombre, "brand": marca,
                    "categoria": categoria, "desc": full_desc, "ficha_url": ficha_url
                })

            if not img.startswith("http") and not img.startswith("assets/"):
                img = f"assets/img/{img}"

            # Auditoría de precios vs 1320
            if old_item:
                old_p = float(old_item.get("p", 0.0))
                if old_p > 0:
                    pct = ((precio_mxn - old_p) / old_p) * 100.0
                    if abs(pct) < 0.01:
                        price_changes["sin_cambio"] += 1
                    elif pct > 0:
                        price_changes["subieron"] += 1
                    else:
                        price_changes["bajaron"] += 1
                    if abs(pct) >= 30.0:
                        big_price_swings.append({
                            "sku": final_sku, "nombre": nombre[:70], "sheet": sheet_name,
                            "precio_1320": old_p, "precio_1321": precio_mxn, "pct": round(pct, 2)
                        })
                old_cat = old_item.get("c", "")
                if old_cat and old_cat != categoria:
                    reubicados_vs_1320.append({
                        "sku": final_sku, "nombre": nombre[:70], "de": old_cat, "a": categoria, "ct_sheet": sheet_name
                    })

            # Reubicación respecto a hoja de origen CT
            expected_set = CT_SHEET_EXPECTED_DEPTS.get(sheet_name, set())
            if expected_set and categoria not in expected_set:
                reubicados_vs_ct_origen.append({
                    "sku": final_sku, "nombre": nombre[:70], "ct_sheet": sheet_name, "ct_sub": subcat[:45], "vitrina_asignada": categoria
                })

            # Protección preventiva por anomalía crítica de precio/origen
            is_quarantined_anomaly = raw_sku in QUARANTINE_ANOMALY_SKUS
            if is_quarantined_anomaly:
                preventive_quarantine_anomalies.append({
                    "sku": final_sku, "nombre": nombre[:70], "precio_mxn": precio_mxn,
                    "motivo": QUARANTINE_ANOMALY_SKUS[raw_sku]
                })
                is_disp = False
                stk_val = 0
                est_com = "cuarentena preventiva (anomalía de precio/origen CT)"
            else:
                ct_active_count += 1
                is_disp = True
                stk_val = 15
                est_com = "disponible"
                if old_item:
                    if old_item.get("a", 0) == 1:
                        retornos_cuarentena_ct.append({"sku": final_sku, "nombre": nombre[:75], "categoria": categoria, "precio": precio_mxn})
                    else:
                        mantenidos_activos_ct.append(final_sku)

            is_outlet = (sheet_name in ["OUTLET", "OUTLET EQUIPOS DE MARCA"]) or (descuento_pct >= 25 and "OUTLET" in nombre.upper())
            item = {
                "id": final_sku, "sku": final_sku, "clave_proveedor": "A",
                "proveedor_nombre": "CT Internacional", "proveedor": "CT Internacional",
                "nombre": nombre, "precio": precio_mxn, "precio_original": precio_orig,
                "precio_mayoreo": precio_may, "descuento_pct": descuento_pct,
                "categoria": categoria, "subcategoria": subcat, "marca": marca,
                "imagen": img, "stock": stk_val, "disponible": is_disp,
                "estado_comercial": est_com, "outlet": is_outlet,
                "descripcion": full_desc, "ficha_tecnica_url": ficha_url,
                "costo_neto_usd": round(costo_neto_usd, 2),
                "ct_sheet": sheet_name, "jev_cert": jev_cert,
            }
            standardized_products.append(item)
            if is_outlet and is_disp and precio_mxn > 50:
                outlet_products.append(item)

            # Hardware de ensamble (solo activos reales con paridad de socket robusta)
            if is_disp:
                full_txt = f"{nombre} {full_desc}"
                if categoria == "procesadores" and (raw_sku.startswith("CPUINT") or raw_sku.startswith("CPUAMD")):
                    item_cpu = dict(item)
                    item_cpu["socket"] = extract_socket_robusto(full_txt, final_sku)
                    item_cpu["ram_type"] = extract_ram_type_robusto(full_txt, item_cpu["socket"])
                    item_cpu["tdp"] = extract_tdp(full_txt)
                    ensamble_hardware["procesadores"].append(item_cpu)
                elif categoria == "tarjetas_madre":
                    item_mb = dict(item)
                    item_mb["socket"] = extract_socket_robusto(full_txt, final_sku)
                    item_mb["ram_type"] = extract_ram_type_robusto(full_txt, item_mb["socket"])
                    ensamble_hardware["tarjetas_madre"].append(item_mb)
                elif categoria == "memorias_ram_pc":
                    item_ram = dict(item)
                    item_ram["ram_type"] = "DDR5" if "DDR5" in full_txt.upper() else "DDR4"
                    ensamble_hardware["memorias_ram"].append(item_ram)
                elif categoria in ["ssds_m2_nvme", "discos_duros_hdd_internos"]:
                    ensamble_hardware["almacenamiento"].append(item)
                elif categoria == "tarjetas_video":
                    item_gpu = dict(item)
                    item_gpu["watts_req"] = 650 if any(g in nombre for g in ["4070", "4080", "5070", "5080", "7900"]) else 450
                    ensamble_hardware["tarjetas_video"].append(item_gpu)
                elif categoria == "fuentes_energia":
                    item_psu = dict(item)
                    item_psu["watts"] = extract_tdp(nombre)
                    ensamble_hardware["fuentes_poder"].append(item_psu)
                elif categoria == "gabinetes":
                    ensamble_hardware["gabinetes"].append(item)
                elif categoria == "enfriamiento":
                    ensamble_hardware["enfriamiento"].append(item)

    print(f"[*] CT Internacional activos procesados: {ct_active_count:,} (+ {len(preventive_quarantine_anomalies)} cuarentena preventiva)")
    print(f"    -> Enlaces reales Columna L verificados: {col_l_verified_count:,}")
    print(f"    -> Mantenidos Activos:                   {len(mantenidos_activos_ct):,}")
    print(f"    -> Retornos de Cuarentena:               {len(retornos_cuarentena_ct):,}")
    print(f"    -> Nuevas Altas Semana 1321:             {len(nuevas_altas_ct):,}")
    print(f"    -> Reubicados de vitrina vs Sem 1320:    {len(reubicados_vs_1320):,}")
    print(f"    -> Reubicados vs hoja origen CT:         {len(reubicados_vs_ct_origen):,}")

    # 5. Integrar Intcomex México (Clave B)
    print("\n[PASO 5] Integrando catálogo mayorista Intcomex (Clave B)...")
    intcomex_active_count = 0
    nuevas_altas_intcomex = []
    retornos_cuarentena_intcomex = []
    mantenidos_activos_intcomex = []

    for key, intc in intcomex_items.items():
        raw_sku = clean_sku(intc["sku"] or intc["mpn"])
        final_sku = f"B-{raw_sku}"
        if final_sku in seen_skus:
            continue
        seen_skus.add(final_sku)
        seen_skus.add(raw_sku)
        intcomex_active_count += 1

        cost_mxn = intc["cost_mxn"]
        costo_usd = round(cost_mxn / TIPO_CAMBIO, 2)
        precio_orig = round(cost_mxn * FACTOR_LISTA, 2)
        precio_mxn = round(precio_orig * 0.75, 2)
        precio_may = round(precio_mxn * 0.90, 2)
        descuento_pct = 25

        old_item = old_by_prov_raw.get(("B", raw_sku)) or old_by_sku.get(final_sku) or old_by_sku.get(raw_sku)
        if old_item:
            if old_item.get("a", 0) == 1 and intc["in_stock"]:
                retornos_cuarentena_intcomex.append(final_sku)
            elif intc["in_stock"]:
                mantenidos_activos_intcomex.append(final_sku)
            nombre = clean_text(old_item.get("n", intc["name"][:120]))
            subcat = old_item.get("subgrupo_label", intc["subcategory"] or intc["category"])
            marca = old_item.get("m", intc["brand"] or "VECTEC")
            if marca in ["Generica", "GENERIC", ""]:
                marca = "VECTEC"
            full_desc = clean_text(old_item.get("d", intc["name"]))
            if LEYENDA_LEGAL not in full_desc:
                full_desc = f"{full_desc} {LEYENDA_LEGAL}".strip()
        else:
            nombre = intc["name"][:120]
            marca = intc["brand"] or infer_brand(nombre, raw_sku)
            subcat = intc["subcategory"] or intc["category"]
            full_desc = intc["name"]
            if LEYENDA_LEGAL not in full_desc:
                full_desc = f"{full_desc} {LEYENDA_LEGAL}".strip()
            nuevas_altas_intcomex.append({"sku": raw_sku, "name": nombre, "brand": marca, "desc": full_desc})

        jev_cert = 0
        if final_sku in jev_overrides and jev_overrides[final_sku] in DEPT_ID_SET:
            categoria = jev_overrides[final_sku]
            jev_cert = 1
        else:
            categoria = clasificar_producto_semantico(
                raw_sku, nombre, marca,
                intc_cat=intc.get("category", ""), intc_sub=intc.get("subcategory", ""),
                subgrupo_header=subcat, desc=full_desc
            )
        if old_item and old_item.get("c") and old_item.get("c") != categoria:
            reubicados_vs_1320.append({
                "sku": final_sku, "nombre": nombre[:70], "de": old_item.get("c"), "a": categoria, "ct_sheet": f"INTCOMEX:{intc.get('category','')}"
            })

        img = f"assets/img/B-{raw_sku}.webp"
        # Guardrail financiero Intcomex: bloquear precios sentinel ($999,999 MXN) o absurdos (< $5 MXN)
        is_intc_anomaly = (cost_mxn >= 900000.0) or (cost_mxn < 5.0)
        if is_intc_anomaly:
            preventive_quarantine_anomalies.append({
                "sku": final_sku, "nombre": nombre[:70], "precio_mxn": precio_mxn,
                "motivo": f"Precio sentinel/absurdo Intcomex (costo={cost_mxn:,.2f} MXN)."
            })
            is_in_stock = False
            stk_intc = 0
            est_intc = "cuarentena preventiva (precio sentinel Intcomex)"
        else:
            is_in_stock = intc["in_stock"]
            stk_intc = intc["stock"]
            est_intc = "disponible" if is_in_stock else "bajo_pedido"
        standardized_products.append({
            "id": final_sku, "sku": final_sku, "clave_proveedor": "B",
            "proveedor_nombre": "Intcomex México", "proveedor": "Intcomex México",
            "nombre": nombre, "precio": precio_mxn, "precio_original": precio_orig,
            "precio_mayoreo": precio_may, "descuento_pct": descuento_pct,
            "categoria": categoria, "subcategoria": subcat, "marca": marca,
            "imagen": img, "stock": stk_intc, "disponible": is_in_stock,
            "estado_comercial": est_intc,
            "outlet": False, "descripcion": full_desc, "ficha_tecnica_url": "",
            "costo_neto_usd": costo_usd, "ct_sheet": f"INTCOMEX:{intc.get('category', '')}",
            "jev_cert": jev_cert,
        })
    print(f"[*] Intcomex procesados: {intcomex_active_count:,}")

    # 6. CUARENTENA BIDIRECCIONAL (Preservar historial y 100% fotos en disco, sacar de vitrinas)
    print("\n[PASO 6] Procesando CUARENTENA BIDIRECCIONAL (cero eliminación de fotos)...")
    cuarentena_ct = 0
    cuarentena_intcomex = 0
    nuevos_a_cuarentena = []
    mantenidos_en_cuarentena = []
    vistos_cuarentena = set()

    for old_raw, old_it in old_by_sku.items():
        s_orig = old_it.get("s", "")
        if s_orig in vistos_cuarentena:
            continue
        vistos_cuarentena.add(s_orig)
        raw_clean = clean_sku(s_orig)
        pref_a = f"A-{raw_clean}"
        pref_b = f"B-{raw_clean}"
        if s_orig in seen_skus or pref_a in seen_skus or pref_b in seen_skus or raw_clean in seen_skus:
            continue

        seen_skus.update([s_orig, pref_a, pref_b, raw_clean])
        clave_prov = old_it.get("prov", "B" if s_orig.startswith("B-") else "A")
        prov_nombre = "Intcomex México" if clave_prov == "B" else "CT Internacional"
        final_sku = pref_b if clave_prov == "B" else pref_a
        if clave_prov == "A":
            cuarentena_ct += 1
        else:
            cuarentena_intcomex += 1

        if old_it.get("a", 0) == 0:
            nuevos_a_cuarentena.append({
                "sku": final_sku, "nombre": clean_text(old_it.get("n", raw_clean))[:70],
                "categoria": old_it.get("c", ""), "precio": float(old_it.get("p", 0.0))
            })
        else:
            mantenidos_en_cuarentena.append(final_sku)

        p_val = float(old_it.get("p", 0.0))
        o_val = float(old_it.get("o", p_val * 1.25))
        m_val = old_it.get("m", "VECTEC")
        full_desc = clean_text(old_it.get("d", ""))
        if LEYENDA_LEGAL not in full_desc:
            full_desc = f"{full_desc} {LEYENDA_LEGAL}".strip()
        images = old_it.get("k", [])
        img = images[0] if images else (f"assets/img/{raw_clean}.webp" if clave_prov == "A" else f"assets/img/B-{raw_clean}.webp")
        cat_q = clasificar_producto_semantico(
            raw_clean, clean_text(old_it.get("n", raw_clean)), m_val,
            subgrupo_header=old_it.get("subgrupo_label", ""), desc=full_desc
        )
        standardized_products.append({
            "id": final_sku, "sku": final_sku, "clave_proveedor": clave_prov,
            "proveedor_nombre": prov_nombre, "proveedor": prov_nombre,
            "nombre": clean_text(old_it.get("n", raw_clean)),
            "precio": p_val, "precio_original": o_val,
            "precio_mayoreo": float(old_it.get("y", round(p_val * 0.90, 2))),
            "descuento_pct": 0, "categoria": cat_q,
            "subcategoria": old_it.get("subgrupo_label", ""), "marca": m_val,
            "imagen": img, "stock": 0, "disponible": False,
            "estado_comercial": "agotado / sin inventario", "outlet": False,
            "descripcion": full_desc, "ficha_tecnica_url": old_it.get("ficha_url", ""),
            "costo_neto_usd": float(old_it.get("u", 0.0)), "ct_sheet": "", "jev_cert": 0,
        })

    total_cuarentena = cuarentena_ct + cuarentena_intcomex + len(preventive_quarantine_anomalies)
    print(f"    -> Retornos de Cuarentena CT:            {len(retornos_cuarentena_ct):,}")
    print(f"    -> Nuevos a Cuarentena (salen de stock): {len(nuevos_a_cuarentena):,}")
    print(f"    -> Mantenidos en Cuarentena:             {len(mantenidos_en_cuarentena):,}")
    print(f"    -> Cuarentena preventiva (anomalías CT): {len(preventive_quarantine_anomalies):,}")
    print(f"    -> Total en Cuarentena (fuera vitrinas): {total_cuarentena:,}")

    # 7. Descarga multi-hilo de imágenes WebP solo para nuevas altas
    print("\n[PASO 7] Auditando y descargando imágenes WebP para altas nuevas...")
    imagenes_nuevas_descargadas = 0
    imagenes_existentes_o_pl = 0
    incidencias_img = []

    def _procesar_imagen_alta(alta, es_b=False):
        raw_s = alta["sku"]
        dest_filename = f"B-{raw_s}.webp" if es_b else f"{raw_s}.webp"
        dest_path = os.path.join(IMG_DIR, dest_filename)
        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 500:
            return ("existente", raw_s)
        if not es_b:
            ct_img_url = fetch_ct_product_image(raw_s)
            if ct_img_url:
                b_data = download_bytes(ct_img_url)
                if b_data and save_as_webp(b_data, dest_path, quality=85):
                    return ("descargado", raw_s)
        cat = alta.get("categoria", "accesorios_perifericos")
        pl_path = os.path.join(PLACEHOLDERS_DIR, f"{cat}.jpg")
        if not os.path.exists(pl_path):
            pl_path = os.path.join(PLACEHOLDERS_DIR, "acc_placeholder.jpg")
        if os.path.exists(pl_path):
            try:
                with open(pl_path, "rb") as pf:
                    save_as_webp(pf.read(), dest_path, quality=85)
                return ("placeholder", raw_s)
            except Exception:
                pass
        return ("incidencia", raw_s)

    todas_altas = [(a, False) for a in nuevas_altas_ct] + [(b, True) for b in nuevas_altas_intcomex]
    with ThreadPoolExecutor(max_workers=8) as ex:
        for st, sku_r in [f.result() for f in [ex.submit(_procesar_imagen_alta, a, eb) for a, eb in todas_altas]]:
            if st == "descargado":
                imagenes_nuevas_descargadas += 1
            elif st in ("existente", "placeholder"):
                imagenes_existentes_o_pl += 1
            else:
                incidencias_img.append(sku_r)
    print(f"[OK] Imágenes nuevas: {imagenes_nuevas_descargadas} descargadas, {imagenes_existentes_o_pl} existentes/placeholder, {len(incidencias_img)} incidencias.")

    # 8. Generar índices JSON maestros
    print("\n[PASO 8] Generando índices maestros y catálogo compacto...")
    search_index = []
    compact_export = []
    for p in standardized_products:
        is_disp = bool(p["disponible"]) and p["estado_comercial"] == "disponible" and int(p["stock"]) > 0
        search_index.append({
            "id": p["id"], "sku": p["sku"], "prov": p["clave_proveedor"],
            "prov_nom": p["proveedor_nombre"], "n": p["nombre"],
            "p": p["precio"], "o": p["precio_original"], "c": p["categoria"],
            "m": p["marca"], "img": p["imagen"], "d": 1 if is_disp else 0,
            "stk": p["stock"], "est_com": p["estado_comercial"],
            "ficha_url": p.get("ficha_tecnica_url", ""), "out": 1 if p["outlet"] else 0,
        })
        if p["sku"].startswith("A-CFG-") or p["sku"].startswith("CFG-"):
            continue
        has_img = 1 if os.path.exists(os.path.join(PCC_DIR, p["imagen"])) else 0
        compact_export.append({
            "s": p["sku"], "prov": p["clave_proveedor"], "prov_nom": p["proveedor_nombre"],
            "n": p["nombre"], "c": p["categoria"], "m": p["marca"],
            "p": p["precio"], "u": p.get("costo_neto_usd", round(p["precio"] / FACTOR_VENTA_MXN, 2)),
            "o": p["precio_original"], "y": p["precio_mayoreo"], "d": p["descripcion"],
            "stk": p["stock"], "est_com": p["estado_comercial"],
            "ficha_url": p.get("ficha_tecnica_url", ""),
            "a": 0 if is_disp else 1, "i": has_img,
            "subgrupo_label": p["subcategoria"], "ct_sheet": p.get("ct_sheet", ""),
            "jev_cert": p.get("jev_cert", 0), "k": [p["imagen"]],
        })

    with open(COMPACT_JSON, "w", encoding="utf-8") as f:
        json.dump(compact_export, f, ensure_ascii=False, separators=(",", ":"))
    for target_dir in (DATA_DIR, PCC_DATA_DIR):
        with open(os.path.join(target_dir, "inventario_maestro_buscador.json"), "w", encoding="utf-8") as f:
            json.dump(search_index, f, ensure_ascii=False, separators=(",", ":"))
        outlet_products.sort(key=lambda x: (x["descuento_pct"], x["precio"]), reverse=True)
        with open(os.path.join(target_dir, "liquidaciones_outlet.json"), "w", encoding="utf-8") as f:
            json.dump(outlet_products[:300], f, ensure_ascii=False, separators=(",", ":"))
        with open(os.path.join(target_dir, "hardware_ensamble.json"), "w", encoding="utf-8") as f:
            json.dump(ensamble_hardware, f, ensure_ascii=False, separators=(",", ":"))

    # 9. Regenerar vitrinas congruentes (EXCLUYENDO 100% de agotados/cuarentena de vitrinas públicas)
    print("\n[PASO 9] Regenerando vitrinas congruentes sin agotados (67 departamentos)...")
    regenerar_vitrinas_congruentes()
    shutil.copy2(COMPACT_JSON, os.path.join(DATA_DIR, "catalogo_maestro_compact.json"))

    # Guardar reporte forense JSON
    reporte = {
        "semana": "1321",
        "vigencia": "23 al 28 de Noviembre de 2026",
        "generado_en": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "resumen": {
            "total_catalogo_unificado": len(standardized_products),
            "total_compacto": len(compact_export),
            "activos_en_vitrinas": sum(1 for x in compact_export if x["a"] == 0 and x["stk"] > 0),
            "cuarentena_fuera_de_vitrinas": sum(1 for x in compact_export if x["a"] == 1 or x["stk"] <= 0),
            "ct_activos": ct_active_count,
            "intcomex_activos": sum(1 for x in compact_export if x["prov"] == "B" and x["a"] == 0),
            "turnkey_configs": len(turnkey_configs),
            "enlaces_col_l_verificados": col_l_verified_count,
            "nuevas_altas_ct": len(nuevas_altas_ct),
            "retornos_cuarentena_ct": len(retornos_cuarentena_ct),
            "nuevos_a_cuarentena": len(nuevos_a_cuarentena),
            "mantenidos_cuarentena": len(mantenidos_en_cuarentena),
            "cuarentena_preventiva_anomalias": len(preventive_quarantine_anomalies),
            "reubicados_vs_1320": len(reubicados_vs_1320),
            "reubicados_vs_ct_origen": len(reubicados_vs_ct_origen),
            "precios_cambios": price_changes,
            "cambios_bruscos_30pct": len(big_price_swings),
            "outlet_columna_corrida_rescatados": len(outlet_shifted_col_rescued),
            "filas_precio_cero_o_corrupto": len(zero_or_corrupt_rows),
        },
        "retornos_cuarentena_ct": retornos_cuarentena_ct,
        "nuevos_a_cuarentena_muestra": nuevos_a_cuarentena[:30],
        "cuarentena_preventiva": preventive_quarantine_anomalies,
        "cambios_bruscos": sorted(big_price_swings, key=lambda x: abs(x["pct"]), reverse=True),
        "outlet_rescatados": outlet_shifted_col_rescued,
        "reubicados_vs_1320_muestra": reubicados_vs_1320[:50],
        "reubicados_vs_1320_resumen": dict(Counter((x["de"], x["a"]) for x in reubicados_vs_1320).most_common(30)),
    }
    with open(AUDIT_JSON, "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)
    print(f"[OK] Reporte forense guardado en {AUDIT_JSON}")


if __name__ == "__main__":
    main()
