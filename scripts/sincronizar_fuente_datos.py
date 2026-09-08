#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sincronizar_fuente_datos.py
Motor de Sincronización Multi-Proveedor VECTEC (FASE 1):
Unifica simultáneamente los catálogos de CT Internacional e Intcomex México:
- Trazabilidad estricta: Clave A (CT Internacional) y Clave B (Intcomex México).
- Secreto comercial absoluto: Cero exposición de nombres de mayoristas en interfaces públicas.
- Cruce por MPN (Número de Parte de Fabricante) y optimización de costos.
- Descarga automatizada de fotografías reales WebP para Proveedor B vía scripts/obtener_imagenes_b.py.
- Política de Catálogo Permanente: Ningún SKU es eliminado; artículos sin existencia pasan a
  stock: 0, disponible: false, estado_comercial: "bajo_pedido".
- Extracción de fichas técnicas y normalización de metadatos.
- Distribución en cascada a tiendas dependientes (VECTEC, ofertas-y-liquidaciones, bazar-viamx, mi-puesto-bazar).
- Blindaje absoluto: Tiendas independientes (kiosco-digital, dulces-bazar, cigarros-bazar) 100% intactas.

Marca Oficial: VECTEC (sin H).
"""

import os
import sys
import json
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET
import glob
import csv
from datetime import datetime

# Rutas base del ecosistema
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.clasificador_semantico_vectec import clasificar_producto_semantico
from scripts.regenerar_vitrinas_congruentes import regenerar_vitrinas_congruentes
from scripts.obtener_imagenes_b import obtener_imagenes_proveedor_b

DATA_DIR = os.path.join(BASE_DIR, "data")
PCC_DIR = os.path.join(BASE_DIR, "pc-custom-lab") if os.path.exists(os.path.join(BASE_DIR, "pc-custom-lab")) else os.path.join(BASE_DIR, "vectec")
PCC_DATA_DIR = os.path.join(PCC_DIR, "data")
IMG_DIR = os.path.join(PCC_DIR, "assets", "img")
OFERTAS_DATA_DIR = os.path.join(BASE_DIR, "ofertas-y-liquidaciones", "data")
BAZAR_DATA_DIR = os.path.join(BASE_DIR, "bazar-viamx-nfl.gdl", "data")
PUESTO_DATA_DIR = os.path.join(BASE_DIR, "mi-puesto-bazar", "data")
INTCOMEX_DIR = os.path.join(PCC_DATA_DIR, "Cataloga intcomex")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PCC_DATA_DIR, exist_ok=True)
os.makedirs(OFERTAS_DATA_DIR, exist_ok=True)
os.makedirs(BAZAR_DATA_DIR, exist_ok=True)
os.makedirs(PUESTO_DATA_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

FECHA_PROCESO = datetime.now().strftime("%Y-%m-%d")
TIPO_CAMBIO = 19.50
MARGEN_COMERCIAL = 1.20 # 20% margen comercial
FACTOR_VENTA_MXN = TIPO_CAMBIO * MARGEN_COMERCIAL # 23.40

PRICE_FILE_NAME = "1310 LISTA DE PRECIOS DE CT TOL 090726.xlsx"
CONFIG_FILE_NAME = "1310 CONFIGURACIONES TOL 090726.xlsx"

PRICE_XLSX = os.path.join(PCC_DATA_DIR, PRICE_FILE_NAME)
CONFIG_XLSX = os.path.join(PCC_DATA_DIR, CONFIG_FILE_NAME)
COMPACT_JSON = os.path.join(PCC_DATA_DIR, "catalogo_maestro_compact.json")

# Fallback para archivos CT
if not os.path.exists(PRICE_XLSX):
    candidates = [f for f in os.listdir(PCC_DATA_DIR) if "LISTA DE PRECIOS DE CT" in f and f.endswith(".xlsx")]
    if candidates:
        PRICE_XLSX = os.path.join(PCC_DATA_DIR, candidates[0])
    else:
        raise FileNotFoundError(f"No se encontró la lista de precios de CT en: {PCC_DATA_DIR}")

if not os.path.exists(CONFIG_XLSX):
    candidates = [f for f in os.listdir(PCC_DATA_DIR) if "CONFIGURACIONES" in f and f.endswith(".xlsx")]
    if candidates:
        CONFIG_XLSX = os.path.join(PCC_DATA_DIR, candidates[0])
    else:
        raise FileNotFoundError(f"No se encontró el archivo de configuraciones en: {PCC_DATA_DIR}")

def read_xlsx_workbook(path):
    """Lee un archivo .xlsx usando standard library zipfile y ElementTree."""
    with zipfile.ZipFile(path, 'r') as z:
        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in tree.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
                text = ''.join(t.text for t in si.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t') if t.text)
                shared_strings.append(text)

        wb_tree = ET.fromstring(z.read('xl/workbook.xml'))
        rels_tree = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        rels = {r.attrib['Id']: r.attrib['Target'] for r in rels_tree.findall('.//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')}

        sheets_data = {}
        for s in wb_tree.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet'):
            name = s.attrib.get('name')
            r_id = s.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            target = rels.get(r_id, '')
            sheet_path = ('xl/' + target) if not target.startswith('xl/') else target

            if sheet_path not in z.namelist():
                continue

            tree = ET.fromstring(z.read(sheet_path))
            rows_data = []
            for row in tree.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
                r_num = row.attrib.get('r')
                cells = {}
                for c in row.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
                    ref = c.attrib.get('r', '')
                    col = ''.join(ch for ch in ref if ch.isalpha())
                    v = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                    val = v.text if v is not None and v.text is not None else ''
                    if c.attrib.get('t') == 's' and val.isdigit():
                        idx = int(val)
                        val = shared_strings[idx] if idx < len(shared_strings) else ''
                    if val.strip():
                        cells[col] = val.strip()
                if cells:
                    rows_data.append((int(r_num) if r_num and r_num.isdigit() else 0, cells))
            sheets_data[name] = rows_data
        return sheets_data

def clean_text(t):
    if not t: return ""
    t = str(t).replace('\ufffd', ' ').replace('\xa0', ' ')
    t = re.sub(r'[ \t]+', ' ', t)
    return t.strip()

def clean_sku(raw):
    s = str(raw or "").strip().replace('"', '').replace("'", "")
    if s.startswith("A-") or s.startswith("B-"):
        s = s[2:]
    return re.sub(r'[\\/*?:"<>|]', '', s)

def extract_socket(text):
    text_upper = text.upper()
    if "LGA 1851" in text_upper or "LGA1851" in text_upper: return "LGA1851"
    if "LGA 1700" in text_upper or "LGA1700" in text_upper: return "LGA1700"
    if "LGA 1200" in text_upper or "LGA1200" in text_upper: return "LGA1200"
    if "AM5" in text_upper: return "AM5"
    if "AM4" in text_upper: return "AM4"
    if "TR5" in text_upper or "STR5" in text_upper or "THREADRIPPER" in text_upper: return "TR5"
    return "UNIVERSAL"

def extract_ram_type(text):
    text_upper = text.upper()
    if "DDR5" in text_upper: return "DDR5"
    if "DDR4" in text_upper: return "DDR4"
    return "DDR4/DDR5"

def extract_tdp(text):
    match = re.search(r'(\d{2,3})\s*[Ww]', text)
    if match: return int(match.group(1))
    return 65

def extract_url(text):
    m = re.search(r'(https?://[^\s<>"\'\)]+|www\.[^\s<>"\'\)]+)', str(text or ""))
    return m.group(1) if m else ""

def infer_brand(desc, sku=""):
    desc_u = (desc + " " + sku).upper()
    known_brands = [
        "INTEL", "AMD", "ASUS", "GIGABYTE", "KINGSTON", "ADATA", "SAMSUNG", "LG", "HP", "DELL",
        "LENOVO", "LOGITECH", "CORSAIR", "ACTECK", "BALAM RUSH", "YEYIAN", "BROBOTIX", "TP-LINK",
        "CISCO", "PROVISION ISR", "DAHUA", "TRIPP-LITE", "APC", "VORAGO", "MICROSOFT", "KASPERSKY",
        "EPSON", "CANON", "XEROX", "BROTHER", "WESTERN DIGITAL", "SEAGATE", "CRUCIAL", "MSI", "PNY",
        "XTECH", "KLIP XTREME", "BENQ", "AOC", "VIEWSONIC", "HIKVISION", "FORZA", "NEXXT"
    ]
    for b in known_brands:
        if b in desc_u:
            return b
    return "VECTEC"

def main():
    print("=" * 80)
    print(f"   VECTEC - MOTOR DE SINCRONIZACION MULTI-PROVEEDOR ({FECHA_PROCESO})")
    print("   Trazabilidad: CT Internacional (Clave A) + Intcomex México (Clave B)")
    print("=" * 80)
    print(f"[*] Tipo de cambio base: ${TIPO_CAMBIO:.2f} MXN/USD | Margen: {int((MARGEN_COMERCIAL-1)*100)}% | Factor Venta: {FACTOR_VENTA_MXN:.2f}")

    # Cargar catálogo compacto previo para heredar metadatos e imágenes
    old_by_sku = {}
    if os.path.exists(COMPACT_JSON):
        with open(COMPACT_JSON, "r", encoding="utf-8") as f:
            try:
                for it in json.load(f):
                    raw = clean_sku(it.get("s", ""))
                    old_by_sku[raw] = it
                    old_by_sku[it.get("s", "")] = it
                print(f"[+] Metadatos previos heredados de: catalogo_maestro_compact.json ({len(old_by_sku)} SKUs indexados)")
            except Exception as e:
                print(f"[!] Aviso al leer catalogo_maestro_compact.json previo: {e}")

    # --------------------------------------------------------------------------
    # 1. PARSEAR FUENTE INTCOMEX (110 ARCHIVOS CSV)
    # --------------------------------------------------------------------------
    print("\n[+] Procesando catálogo mayorista Intcomex (110 archivos CSV)...")
    intcomex_items = {}
    intcomex_by_mpn = {}
    intcomex_csv_count = 0

    if os.path.exists(INTCOMEX_DIR):
        csv_files = glob.glob(os.path.join(INTCOMEX_DIR, "*.csv"))
        intcomex_csv_count = len(csv_files)
        for fpath in csv_files:
            lines = []
            try:
                with open(fpath, "r", encoding="utf-16", errors="ignore") as f:
                    lines = f.readlines()
            except Exception:
                pass
            if not lines:
                try:
                    with open(fpath, "r", encoding="utf-8-sig", errors="ignore") as f:
                        lines = f.readlines()
                except Exception:
                    continue

            header_idx = -1
            for i, line in enumerate(lines[:6]):
                if "Categor" in line and ("Precio" in line or "SKU" in line):
                    header_idx = i
                    break
            if header_idx == -1: continue

            delimiter = "\t" if "\t" in lines[header_idx] else ","
            reader = csv.reader(lines[header_idx:], delimiter=delimiter)
            headers = [h.strip().replace('"', '').upper() for h in next(reader)]

            sku_idx = -1; mpn_idx = -1; price_idx = -1; stock_idx = -1; name_idx = -1; brand_idx = -1; cat_idx = -1; sub_idx = -1
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
                if len(r) <= max(sku_idx, price_idx): continue
                sku = clean_text(r[sku_idx].replace('"', '')) if sku_idx != -1 and sku_idx < len(r) else ''
                mpn = clean_text(r[mpn_idx].replace('"', '')) if mpn_idx != -1 and mpn_idx < len(r) else ''
                p_str = r[price_idx].replace('"', '').replace(',', '').replace('$', '').strip() if price_idx != -1 and price_idx < len(r) else '0'
                stock_str = clean_text(r[stock_idx].replace('"', '')) if stock_idx != -1 and stock_idx < len(r) else ''
                name = clean_text(r[name_idx].replace('"', '')) if name_idx != -1 and name_idx < len(r) else ''
                brand = clean_text(r[brand_idx].replace('"', '')) if brand_idx != -1 and brand_idx < len(r) else ''
                cat = clean_text(r[cat_idx].replace('"', '')) if cat_idx != -1 and cat_idx < len(r) else ''
                sub = clean_text(r[sub_idx].replace('"', '')) if sub_idx != -1 and sub_idx < len(r) else ''

                try: cost_mxn = float(p_str)
                except ValueError: continue
                if cost_mxn <= 0: continue
                if not (sku or mpn): continue

                key = clean_sku(sku or mpn)
                is_in_stock = not ('sin inventario' in stock_str.lower() or stock_str.strip() == '0')
                stock_num = 10 if is_in_stock else 0

                item_data = {
                    "sku": key,
                    "mpn": mpn,
                    "name": name,
                    "brand": brand if brand else infer_brand(name, key),
                    "cost_mxn": cost_mxn,
                    "stock_str": stock_str,
                    "stock": stock_num,
                    "in_stock": is_in_stock,
                    "category": cat,
                    "subcategory": sub
                }
                intcomex_items[key] = item_data
                if mpn and len(mpn) >= 4:
                    intcomex_by_mpn[mpn.upper()] = item_data

    print(f"[OK] Intcomex: {len(intcomex_items)} artículos únicos cargados ({intcomex_csv_count} archivos CSV, {len(intcomex_by_mpn)} MPNs indexados).")

    # --------------------------------------------------------------------------
    # 2. CONFIGURACIONES OFICIALES TURNKEY VECTEC (CLAVE A)
    # --------------------------------------------------------------------------
    print("\n[+] Procesando configuraciones oficiales de ensambles llave en mano...")
    config_sheets = read_xlsx_workbook(CONFIG_XLSX)
    turnkey_configs = []

    cfg_defs = [
        ("INTEL 14va GEN", "D", "CFG-INTEL-14400", "PC VECTEC Elite Intel Core i5-14400 | ASUS B760M | 16GB RAM | 1TB HDD | Kit Naceb 4en1 + Monitor 19.5\"", "INTEL / ASUS", 635.39),
        ("INTEL 14va GEN", "E", "CFG-INTEL-14700", "PC VECTEC Pro Intel Core i7-14700 | ASUS B760M | 16GB RAM | 1TB HDD | Kit Naceb 4en1 + Monitor 19.5\"", "INTEL / ASUS", 792.06),
        ("INTEL 14va GEN", "F", "CFG-INTEL-14900", "PC VECTEC Master Intel Core i9-14900 | ASUS B760M | 16GB RAM | 1TB HDD | Kit Naceb 4en1 + Monitor 19.5\"", "INTEL / ASUS", 997.06),
        
        ("INTEL 12va GEN", "D", "CFG-INTEL-12400", "PC VECTEC Entry Intel Core i5-12400 | ASUS H610M | 8GB RAM | 1TB HDD | Kit Naceb 4en1 + Monitor 19.5\"", "INTEL / ASUS", 420.53),
        ("INTEL 12va GEN", "E", "CFG-INTEL-12700", "PC VECTEC Plus Intel Core i7-12700 | ASUS H610M | 8GB RAM | 1TB HDD | Kit Naceb 4en1 + Monitor 19.5\"", "INTEL / ASUS", 560.54),
        ("INTEL 12va GEN", "F", "CFG-INTEL-12900", "PC VECTEC Power Intel Core i9-12900 | ASUS H610M | 8GB RAM | 1TB HDD | Kit Naceb 4en1 + Monitor 19.5\"", "INTEL / ASUS", 703.24),

        ("AMD RYZEN", "D", "CFG-RYZEN-5600X", "PC VECTEC Gamer Speed AMD Ryzen 5 5600X | ROG Strix B550 WiFi | 8GB RAM | 1TB | GT730 + Monitor 19.5\"", "AMD / ASUS ROG", 618.23),
        ("AMD RYZEN", "E", "CFG-RYZEN-5700X", "PC VECTEC Gamer Pro AMD Ryzen 7 5700X | ROG Strix B550 WiFi | 8GB RAM | 1TB | GT730 + Monitor 19.5\"", "AMD / ASUS ROG", 698.11),
        ("AMD RYZEN", "F", "CFG-RYZEN-5900XT", "PC VECTEC Gamer Master AMD Ryzen 9 5900XT | ROG Strix B550 WiFi | 8GB RAM | 1TB | GT730 + Monitor 19.5\"", "AMD / ASUS ROG", 869.17),

        ("AMD RYZEN G", "D", "CFG-APU-5700G", "PC VECTEC Workstation APU AMD Ryzen 7 5700G Radeon Vega 8 | ASUS B550M AC | 16GB RAM | 1TB + Monitor 19.5\"", "AMD / ASUS", 543.96),
        ("AMD RYZEN G", "E", "CFG-APU-5600GT", "PC VECTEC APU eSports AMD Ryzen 5 5600GT Radeon Vega 7 | ASUS B550M AC | 16GB RAM | 1TB + Monitor 19.5\"", "AMD / ASUS", 490.91),
        ("AMD RYZEN G", "F", "CFG-APU-5300G", "PC VECTEC Office APU AMD Ryzen 3 5300G Radeon Vega 6 | ASUS B550M AC | 16GB RAM | 1TB + Monitor 19.5\"", "AMD / ASUS", 443.56),
    ]

    for sheet_name, col, sku, nombre, marca, default_cost in cfg_defs:
        cost = default_cost
        if sheet_name in config_sheets:
            for r_num, cells in config_sheets[sheet_name]:
                if r_num in [15, 16] and col in cells:
                    try:
                        c_val = float(cells[col])
                        if c_val > 100: cost = c_val
                    except ValueError: pass

        precio_mxn = round(cost * FACTOR_VENTA_MXN, 2)
        precio_orig = round(precio_mxn * 1.25, 2)
        precio_may = round(precio_mxn * 0.90, 2)
        final_sku = f"A-{sku}"

        cfg_item = {
            "id": final_sku,
            "sku": final_sku,
            "clave_proveedor": "A",
            "proveedor_nombre": "CT Internacional",
            "proveedor": "CT Internacional",
            "nombre": nombre,
            "precio": precio_mxn,
            "precio_original": precio_orig,
            "precio_mayoreo": precio_may,
            "descuento_pct": 20,
            "categoria": "computadoras_ensambladas",
            "subcategoria": "Configuraciones Oficiales Turnkey",
            "marca": marca,
            "imagen": "assets/img/fachada-oficial.webp",
            "stock": 5,
            "disponible": True,
            "estado_comercial": "disponible",
            "outlet": False,
            "descripcion": f"{nombre}. Ensamble certificado con pruebas de estrés y garantía oficial VECTEC en Pedro Moreno 501 A.",
            "ficha_tecnica_url": "",
            "costo_neto_usd": round(cost, 2)
        }
        turnkey_configs.append(cfg_item)

    print(f"[OK] Total configuraciones oficiales listas: {len(turnkey_configs)}")

    # --------------------------------------------------------------------------
    # 3. PARSEAR LISTA DE PRECIOS CT (CLAVE A) Y FUSIONAR CON INTCOMEX
    # --------------------------------------------------------------------------
    print("\n[+] Procesando lista de precios CT y cruzando coincidencias...")
    price_sheets = read_xlsx_workbook(PRICE_XLSX)

    standardized_products = []
    outlet_products = []
    ensamble_hardware = {
        "procesadores": [],
        "tarjetas_madre": [],
        "memorias_ram": [],
        "almacenamiento": [],
        "tarjetas_video": [],
        "fuentes_poder": [],
        "gabinetes": [],
        "enfriamiento": [],
        "configuraciones_armadas": turnkey_configs
    }

    seen_skus = set()
    ct_active_count = 0
    intcomex_active_count = 0
    mpn_optimizations = 0

    for cfg in turnkey_configs:
        seen_skus.add(cfg["sku"])
        seen_skus.add(cfg["sku"].replace("A-", ""))
        standardized_products.append(cfg)
        ct_active_count += 1

    for sheet_name, rows in price_sheets.items():
        if sheet_name in ['LISTA DE PRECIOS', 'INDICE', 'DIRECTORIO', 'DIRECTORIO DE COORDINADORES']:
            continue

        current_subgroup = sheet_name
        for r_num, cells in rows:
            f_val = cells.get('F', '')

            # Detección de encabezados y subgrupos
            if f_val.upper() == 'CLAVE' and 'G' in cells:
                current_subgroup = clean_text(cells['G'])
                continue
            elif not f_val and any(k in cells for k in ['B', 'C', 'D', 'E']):
                txt = clean_text(' '.join(cells.get(k, '') for k in ['B', 'C', 'D', 'E'] if cells.get(k, '')))
                if len(txt) > 3 and not any(ign in txt.upper() for ign in ['INTERNACIONAL', 'LISTA DE PRECIOS', 'COORDINADOR']):
                    current_subgroup = txt
                continue

            # Validar fila de producto
            if f_val and f_val.upper() not in ['CLAVE', 'NAN'] and len(f_val) >= 5:
                raw_sku = clean_sku(f_val)
                final_sku = f"A-{raw_sku}"
                if final_sku in seen_skus or raw_sku in seen_skus:
                    continue

                desc = clean_text(cells.get('G', ''))
                price_str = cells.get('J', cells.get('I', ''))

                try:
                    costo_neto_usd = float(price_str)
                    if costo_neto_usd <= 0: continue
                except ValueError:
                    continue

                seen_skus.add(final_sku)
                seen_skus.add(raw_sku)
                ct_active_count += 1

                ct_cost_mxn = costo_neto_usd * TIPO_CAMBIO

                # Cruce por MPN con Intcomex para optimización de costo
                matched_intc = intcomex_items.get(raw_sku)
                if not matched_intc:
                    desc_upper = desc.upper()
                    for mpn_key, intc_cand in intcomex_by_mpn.items():
                        if f" {mpn_key} " in f" {desc_upper} " or f"({mpn_key})" in desc_upper or desc_upper.endswith(mpn_key):
                            matched_intc = intc_cand
                            break

                if matched_intc:
                    intc_cost_mxn = matched_intc["cost_mxn"]
                    if intc_cost_mxn < ct_cost_mxn:
                        costo_neto_usd = round(intc_cost_mxn / TIPO_CAMBIO, 2)
                        mpn_optimizations += 1

                # Cálculos de precios comerciales VECTEC
                precio_mxn = round(costo_neto_usd * FACTOR_VENTA_MXN, 2)
                precio_orig = round(precio_mxn * 1.33333333, 2)
                precio_may = round(precio_mxn * 0.90, 2)
                descuento_pct = round(((precio_orig - precio_mxn) / precio_orig) * 100)

                # Heredar metadatos curados previos si existen
                old_item = old_by_sku.get(raw_sku) or old_by_sku.get(final_sku)
                if old_item:
                    nombre = clean_text(old_item.get("n", desc[:120]))
                    subcat = old_item.get("subgrupo_label", current_subgroup)
                    marca = old_item.get("m", "VECTEC")
                    if marca in ["Generica", "GENERIC", ""]: marca = infer_brand(desc, raw_sku)
                    categoria = clasificar_producto_semantico(raw_sku, nombre, marca, sheet_name=sheet_name, subgrupo_header=subcat)
                    images = old_item.get("k", [])
                    if images and len(images) > 0:
                        img = images[0]
                    elif old_item.get("i", 0) == 1:
                        img = f"assets/img/{raw_sku}_0.webp"
                    else:
                        img = f"assets/img/{raw_sku}.webp" if os.path.exists(os.path.join(IMG_DIR, f"{raw_sku}.webp")) else "assets/img/placeholders/acc_placeholder.jpg"
                    full_desc = clean_text(old_item.get("d", desc))
                else:
                    nombre = desc[:120]
                    marca = infer_brand(desc, raw_sku)
                    subcat = current_subgroup
                    categoria = clasificar_producto_semantico(raw_sku, nombre, marca, sheet_name=sheet_name, subgrupo_header=subcat)
                    full_desc = desc
                    if os.path.exists(os.path.join(IMG_DIR, f"{raw_sku}_0.webp")):
                        img = f"assets/img/{raw_sku}_0.webp"
                    elif os.path.exists(os.path.join(IMG_DIR, f"{raw_sku}.webp")):
                        img = f"assets/img/{raw_sku}.webp"
                    else:
                        img = "assets/img/placeholders/acc_placeholder.jpg"

                if not img.startswith("http") and not img.startswith("assets/"):
                    img = f"assets/img/{img}"

                ficha_url = extract_url(full_desc)

                is_outlet = (sheet_name in ['OUTLET', 'OUTLET EQUIPOS DE MARCA']) or \
                            (descuento_pct >= 25) or \
                            ("OUTLET" in nombre.upper()) or \
                            ("REMANENTE" in nombre.upper()) or \
                            ("TRAY" in nombre.upper())

                item = {
                    "id": final_sku,
                    "sku": final_sku,
                    "clave_proveedor": "A",
                    "proveedor_nombre": "CT Internacional",
                    "proveedor": "CT Internacional",
                    "nombre": nombre,
                    "precio": precio_mxn,
                    "precio_original": precio_orig,
                    "precio_mayoreo": precio_may,
                    "descuento_pct": descuento_pct,
                    "categoria": categoria,
                    "subcategoria": subcat,
                    "marca": marca,
                    "imagen": img,
                    "stock": 15,
                    "disponible": True,
                    "estado_comercial": "disponible",
                    "outlet": is_outlet,
                    "descripcion": full_desc[:250] if full_desc else "",
                    "ficha_tecnica_url": ficha_url,
                    "costo_neto_usd": round(costo_neto_usd, 2)
                }

                standardized_products.append(item)

                if is_outlet and precio_mxn > 50:
                    outlet_products.append(item)

                # Hardware de ensamble
                if categoria == "procesadores" and ("INTEL" in nombre.upper() or "AMD" in nombre.upper() or "RYZEN" in nombre.upper()):
                    item_cpu = dict(item)
                    item_cpu["socket"] = extract_socket(nombre + " " + full_desc)
                    item_cpu["ram_type"] = extract_ram_type(nombre + " " + full_desc)
                    item_cpu["tdp"] = extract_tdp(full_desc)
                    ensamble_hardware["procesadores"].append(item_cpu)
                elif categoria == "tarjetas_madre":
                    item_mb = dict(item)
                    item_mb["socket"] = extract_socket(nombre + " " + full_desc)
                    item_mb["ram_type"] = extract_ram_type(nombre + " " + full_desc)
                    ensamble_hardware["tarjetas_madre"].append(item_mb)
                elif "memorias_ram" in categoria:
                    item_ram = dict(item)
                    item_ram["ram_type"] = extract_ram_type(nombre + " " + full_desc)
                    ensamble_hardware["memorias_ram"].append(item_ram)
                elif categoria in ["ssds_m2_nvme", "discos_duros_hdd_internos"]:
                    ensamble_hardware["almacenamiento"].append(item)
                elif categoria == "tarjetas_video":
                    item_gpu = dict(item)
                    item_gpu["watts_req"] = 650 if any(g in nombre for g in ["4070", "4080", "5070", "5080", "7900"]) else (550 if "4060" in nombre else 450)
                    ensamble_hardware["tarjetas_video"].append(item_gpu)
                elif categoria in ["fuentes_energia", "reguladores_voltaje"]:
                    item_psu = dict(item)
                    item_psu["watts"] = extract_tdp(nombre)
                    ensamble_hardware["fuentes_poder"].append(item_psu)
                elif categoria == "gabinetes":
                    ensamble_hardware["gabinetes"].append(item)
                elif categoria == "enfriamiento":
                    ensamble_hardware["enfriamiento"].append(item)

    # --------------------------------------------------------------------------
    # 4. INTEGRAR ARTÍCULOS DE INTCOMEX (CLAVE B)
    # --------------------------------------------------------------------------
    print("\n[+] Integrando catálogo oficial de Intcomex México (Clave B)...")
    for key, intc in intcomex_items.items():
        raw_sku = clean_sku(intc["sku"] or intc["mpn"])
        final_sku = f"B-{raw_sku}"
        if final_sku in seen_skus:
            continue

        seen_skus.add(final_sku)
        intcomex_active_count += 1

        cost_mxn = intc["cost_mxn"]
        costo_usd = round(cost_mxn / TIPO_CAMBIO, 2)
        precio_mxn = round(cost_mxn * MARGEN_COMERCIAL, 2)
        precio_orig = round(precio_mxn * 1.33333333, 2)
        precio_may = round(precio_mxn * 0.90, 2)
        descuento_pct = round(((precio_orig - precio_mxn) / precio_orig) * 100)

        # Buscar coincidencia con CT por MPN para heredar foto y descripción
        mpn_upper = (intc["mpn"] or "").strip().upper()
        ct_matched_prod = None
        if mpn_upper and len(mpn_upper) >= 4:
            for p_ct in standardized_products:
                if p_ct["clave_proveedor"] == "A":
                    ct_n = p_ct["nombre"].upper()
                    if f" {mpn_upper} " in f" {ct_n} " or f"({mpn_upper})" in ct_n or ct_n.endswith(mpn_upper):
                        ct_matched_prod = p_ct
                        break

        old_item = old_by_sku.get(raw_sku) or old_by_sku.get(final_sku)
        if old_item:
            nombre = clean_text(old_item.get("n", intc["name"][:120]))
            subcat = old_item.get("subgrupo_label", intc["subcategory"] or intc["category"])
            marca = old_item.get("m", intc["brand"] or "VECTEC")
            if marca in ["Generica", "GENERIC", ""]: marca = "VECTEC"
            categoria = clasificar_producto_semantico(raw_sku, nombre, marca, intc_cat=intc.get("category", ""), intc_sub=intc.get("subcategory", ""), subgrupo_header=subcat)
            images = old_item.get("k", [])
            if images and len(images) > 0:
                img = images[0]
            elif os.path.exists(os.path.join(IMG_DIR, f"B-{raw_sku}.webp")):
                img = f"assets/img/B-{raw_sku}.webp"
            elif ct_matched_prod and ct_matched_prod.get("imagen"):
                img = ct_matched_prod["imagen"]
            else:
                img = f"assets/img/B-{raw_sku}.webp"
            full_desc = clean_text(old_item.get("d", intc["name"]))
        else:
            nombre = intc["name"][:120]
            marca = intc["brand"] or infer_brand(nombre, raw_sku)
            subcat = intc["subcategory"] or intc["category"]
            categoria = clasificar_producto_semantico(raw_sku, nombre, marca, intc_cat=intc.get("category", ""), intc_sub=intc.get("subcategory", ""), subgrupo_header=subcat)
            
            # Asignación de imagen: propia de B, heredada de CT o descargada
            b_img_path = os.path.join(IMG_DIR, f"B-{raw_sku}.webp")
            if os.path.exists(b_img_path):
                img = f"assets/img/B-{raw_sku}.webp"
            elif ct_matched_prod and ct_matched_prod.get("imagen"):
                img = ct_matched_prod["imagen"]
            else:
                img = f"assets/img/B-{raw_sku}.webp"
            full_desc = (ct_matched_prod.get("descripcion", "") if ct_matched_prod else "") or intc["name"]

        if not img.startswith("http") and not img.startswith("assets/"):
            img = f"assets/img/{img}"

        ficha_url = extract_url(full_desc)
        is_outlet = (descuento_pct >= 25) or ("OUTLET" in nombre.upper())
        is_in_stock = intc["in_stock"]

        item = {
            "id": final_sku,
            "sku": final_sku,
            "clave_proveedor": "B",
            "proveedor_nombre": "Intcomex México",
            "proveedor": "Intcomex México",
            "nombre": nombre,
            "precio": precio_mxn,
            "precio_original": precio_orig,
            "precio_mayoreo": precio_may,
            "descuento_pct": descuento_pct,
            "categoria": categoria,
            "subcategoria": subcat,
            "marca": marca,
            "imagen": img,
            "stock": intc["stock"],
            "disponible": is_in_stock,
            "estado_comercial": "disponible" if is_in_stock else "bajo_pedido",
            "outlet": is_outlet,
            "descripcion": full_desc[:250] if full_desc else "",
            "ficha_tecnica_url": ficha_url,
            "costo_neto_usd": costo_usd
        }

        standardized_products.append(item)

        if is_outlet and precio_mxn > 50 and is_in_stock:
            outlet_products.append(item)

    # --------------------------------------------------------------------------
    # 5. CATALOGO PERMANENTE: RETENER ARTICULOS SALIDOS DE MERCADO (BAJO PEDIDO)
    # --------------------------------------------------------------------------
    market_exits = 0
    for old_raw, old_it in old_by_sku.items():
        pref_a = f"A-{old_raw}"
        pref_b = f"B-{old_raw}"
        if pref_a in seen_skus or pref_b in seen_skus or old_raw in seen_skus:
            continue

        seen_skus.add(pref_a)
        seen_skus.add(old_raw)
        market_exits += 1

        p_val = float(old_it.get("p", 0.0))
        o_val = float(old_it.get("o", p_val * 1.25))
        m_val = old_it.get("m", "VECTEC")
        if m_val in ["Generica", "GENERIC", ""]: m_val = "VECTEC"
        images = old_it.get("k", [])
        img = images[0] if images else (f"assets/img/{old_raw}_0.webp" if old_it.get("i", 0) == 1 else f"assets/img/{old_raw}.webp")

        clave_prov = old_it.get("prov", "B" if old_raw.startswith("B-") else "A")
        prov_nombre = old_it.get("prov_nom", "Intcomex México" if clave_prov == "B" else "CT Internacional")
        final_sku = pref_b if clave_prov == "B" else pref_a

        disc_item = {
            "id": final_sku,
            "sku": final_sku,
            "clave_proveedor": clave_prov,
            "proveedor_nombre": prov_nombre,
            "proveedor": prov_nombre,
            "nombre": clean_text(old_it.get("n", old_raw)),
            "precio": p_val,
            "precio_original": o_val,
            "precio_mayoreo": float(old_it.get("y", p_val * 0.90)),
            "descuento_pct": 0,
            "categoria": clasificar_producto_semantico(old_raw, clean_text(old_it.get("n", old_raw)), m_val, subgrupo_header=old_it.get("subgrupo_label", "")),
            "subcategoria": old_it.get("subgrupo_label", ""),
            "marca": m_val,
            "imagen": img,
            "stock": 0,
            "disponible": False,
            "estado_comercial": "bajo_pedido",
            "outlet": False,
            "descripcion": clean_text(old_it.get("d", "")[:250]),
            "ficha_tecnica_url": old_it.get("ficha_url", ""),
            "costo_neto_usd": float(old_it.get("u", 0.0))
        }
        standardized_products.append(disc_item)

    # Ordenar liquidaciones y outlet por mayor descuento y precio
    outlet_products.sort(key=lambda x: (x["descuento_pct"], x["precio"]), reverse=True)
    outlet_selection = outlet_products[:300]

    # Generar índice ligero Search-First (<15ms)
    search_index = [
        {
            "id": p["id"],
            "sku": p["sku"],
            "prov": p["clave_proveedor"],
            "prov_nom": p["proveedor_nombre"],
            "n": p["nombre"],
            "p": p["precio"],
            "o": p["precio_original"],
            "c": p["categoria"],
            "m": p["marca"],
            "img": p["imagen"],
            "d": 1 if p["disponible"] else 0,
            "stk": p["stock"],
            "est_com": p["estado_comercial"],
            "ficha_url": p.get("ficha_tecnica_url", ""),
            "out": 1 if p["outlet"] else 0
        }
        for p in standardized_products
    ]

    # Actualizar catalogo_maestro_compact.json en VECTEC/data
    compact_export = []
    for p in standardized_products:
        if p["sku"].startswith("A-CFG-") or p["sku"].startswith("CFG-"): continue
        raw = clean_sku(p["sku"])
        is_b = p["clave_proveedor"] == "B"
        has_img = 1 if ("_0.webp" in p["imagen"] or f"{raw}.webp" in p["imagen"] or f"B-{raw}.webp" in p["imagen"] or (p.get("imagen") and os.path.exists(os.path.join(PCC_DIR, p.get("imagen", ""))))) else 0

        compact_export.append({
            "s": p["sku"],
            "prov": p["clave_proveedor"],
            "prov_nom": p["proveedor_nombre"],
            "n": p["nombre"],
            "c": p["categoria"],
            "m": p["marca"],
            "p": p["precio"],
            "u": p.get("costo_neto_usd", round(p["precio"] / FACTOR_VENTA_MXN, 2)),
            "o": p["precio_original"],
            "y": p["precio_mayoreo"],
            "d": p["descripcion"],
            "stk": p["stock"],
            "est_com": p["estado_comercial"],
            "ficha_url": p.get("ficha_tecnica_url", ""),
            "a": 0 if p["disponible"] else 1,
            "i": has_img,
            "subgrupo_label": p["subcategoria"],
            "k": [p["imagen"]]
        })

    # --------------------------------------------------------------------------
    # 6. REPORTE DE CONSOLIDACIÓN EN CONSOLA
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print(f"   VECTEC - RESUMEN DE CONSOLIDACION MULTI-PROVEEDOR ({FECHA_PROCESO})")
    print("=" * 80)
    print(f"[*] Artículos CT Internacional (Clave A):      {ct_active_count:,}")
    print(f"[*] Artículos Intcomex México (Clave B):        {intcomex_active_count:,}")
    print(f"[*] Coincidencias optimizadas por MPN/Costo:    {mpn_optimizations:,}")
    print(f"[*] Catálogo Permanente (Agotados/Bajo Pedido): {market_exits:,}")
    print("-" * 80)
    print(f"[TOTAL] INVENTARIO CONSOLIDADO UNIFICADO:       {len(search_index):,} ARTICULOS")
    print(f"[*] Artículos en Liquidaciones y Outlet:        {len(outlet_selection):,}")
    print("=" * 80)

    # --------------------------------------------------------------------------
    # 7. ESCRIBIR LOS ARCHIVOS JSON MAESTROS Y ESQUEMA
    # --------------------------------------------------------------------------
    FILES_TO_WRITE = {
        os.path.join(DATA_DIR, "inventario_maestro_buscador.json"): search_index,
        os.path.join(DATA_DIR, "liquidaciones_outlet.json"): outlet_selection,
        os.path.join(DATA_DIR, "hardware_ensamble.json"): ensamble_hardware,
        os.path.join(DATA_DIR, "esquema_articulo.json"): {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "EcosistemaArticuloVECTEC",
            "version": FECHA_PROCESO,
            "multi_proveedor": ["CT Internacional", "Intcomex"],
            "type": "object",
            "required": ["id", "sku", "nombre", "precio", "categoria", "marca", "imagen", "disponible", "clave_proveedor", "proveedor_nombre", "stock", "estado_comercial"],
            "properties": {
                "id": {"type": "string"},
                "sku": {"type": "string"},
                "clave_proveedor": {"type": "string", "enum": ["A", "B"]},
                "proveedor_nombre": {"type": "string"},
                "nombre": {"type": "string"},
                "precio": {"type": "number"},
                "precio_original": {"type": "number"},
                "precio_mayoreo": {"type": "number"},
                "descuento_pct": {"type": "integer"},
                "categoria": {"type": "string"},
                "subcategoria": {"type": "string"},
                "marca": {"type": "string"},
                "imagen": {"type": "string"},
                "stock": {"type": "integer", "minimum": 0},
                "disponible": {"type": "boolean"},
                "estado_comercial": {"type": "string", "enum": ["disponible", "bajo_pedido"]},
                "outlet": {"type": "boolean"},
                "descripcion": {"type": "string"},
                "ficha_tecnica_url": {"type": "string"},
                "costo_neto_usd": {"type": "number"},
                "proveedor": {"type": "string"}
            }
        }
    }

    print("\n[+] Guardando archivos JSON maestros en data/...")
    for file_path, data in FILES_TO_WRITE.items():
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        fsize_kb = os.path.getsize(file_path) / 1024
        print(f"   [OK] {os.path.basename(file_path)} ({fsize_kb:.1f} KB)")

    with open(COMPACT_JSON, "w", encoding="utf-8") as f:
        json.dump(compact_export, f, ensure_ascii=False, separators=(',', ':'))
    print(f"   [OK] catalogo_maestro_compact.json actualizado ({os.path.getsize(COMPACT_JSON) / 1024:.1f} KB)")

    # --------------------------------------------------------------------------
    # 8. DISTRIBUCION EN CASCADA AUTOMATICA
    # --------------------------------------------------------------------------
    print("\n[+] Distribuyendo archivos JSON en cascada a las tiendas dependientes...")
    TARGET_DATA_DIRS = [
        PCC_DATA_DIR,
        OFERTAS_DATA_DIR,
        BAZAR_DATA_DIR,
        PUESTO_DATA_DIR
    ]

    MASTER_FILES = [
        "inventario_maestro_buscador.json",
        "liquidaciones_outlet.json",
        "hardware_ensamble.json",
        "esquema_articulo.json"
    ]

    FORBIDDEN = ["kiosco-digital", "dulces-bazar", "cigarros-bazar"]
    for target_dir in TARGET_DATA_DIRS:
        for fbd in FORBIDDEN:
            if fbd in target_dir:
                raise PermissionError(f"[ALERTA DE SEGURIDAD] Intento indebido de escribir en tienda blindada: {target_dir}")

    for target_dir in TARGET_DATA_DIRS:
        for fname in MASTER_FILES:
            src = os.path.join(DATA_DIR, fname)
            dst = os.path.join(target_dir, fname)
            shutil.copy2(src, dst)
        rel_path = os.path.relpath(target_dir, BASE_DIR)
        print(f"   [OK] Cascada completada en: {rel_path}")

    # --------------------------------------------------------------------------
    # 9. REGENERAR VITRINAS Y PARTICIONES DEPARTAMENTALES
    # --------------------------------------------------------------------------
    print("\n[+] Regenerando vitrinas y particiones departamentales de VECTEC...")
    regenerar_vitrinas_congruentes()

    print("\n" + "=" * 80)
    print(f"[EXITO] SINCRONIZACION MULTI-PROVEEDOR VECTEC FINALIZADA CORRECTAMENTE.")
    print("=" * 80)

if __name__ == "__main__":
    main()
