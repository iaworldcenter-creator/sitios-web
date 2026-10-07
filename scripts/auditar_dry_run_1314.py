#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditoría Dry-Run Catálogos CT Internacional Semana 1314 (Vigencia 5 al 10 Octubre 2026)
Verifica integridad de precios, esquemas, categorización semántica y estado de imágenes.
"""

import os
import sys
import json
import re
from collections import Counter, defaultdict

BASE_DIR = r"D:\Proyectos\sitios web"
PCC_DATA_DIR = os.path.join(BASE_DIR, "pc-custom-lab", "data")
IMG_DIR = os.path.join(BASE_DIR, "pc-custom-lab", "assets", "img")
sys.path.insert(0, BASE_DIR)

from scripts.sincronizar_fuente_datos import (
    read_xlsx_workbook, clean_text, clean_sku, extract_url, infer_brand,
    TIPO_CAMBIO, FACTOR_LISTA, MARGEN_OFERTA, FACTOR_VENTA_MXN
)
from scripts.clasificador_semantico_vectec import clasificar_producto_semantico, DEPARTAMENTOS_OFICIALES

PRICE_XLSX = os.path.join(PCC_DATA_DIR, "1314 LISTA DE PRECIOS DE CT TOL 100526.xlsx")
CONFIG_XLSX = os.path.join(PCC_DATA_DIR, "1314 CONFIGURACIONES TOL 100526.xlsx")
COMPACT_JSON = os.path.join(PCC_DATA_DIR, "catalogo_maestro_compact.json")


def run_dry_run():
    print("=" * 80)
    print("   AUDITORÍA DRY-RUN: CT INTERNACIONAL SEMANA 1314 (05-10 OCT 2026)")
    print("=" * 80)

    # 1. Cargar catálogo previo
    old_by_sku = {}
    if os.path.exists(COMPACT_JSON):
        with open(COMPACT_JSON, "r", encoding="utf-8") as f:
            for it in json.load(f):
                raw = clean_sku(it.get("s", ""))
                old_by_sku[raw] = it
                old_by_sku[it.get("s", "")] = it
    print(f"[*] Catálogo maestro previo: {len(old_by_sku)} SKUs indexados.")

    # 2. Parsear configuraciones llave en mano
    print("[*] Parseando 1314 CONFIGURACIONES...")
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
        turnkey_configs.append((sku, nombre, cost))
    print(f"[+] Configuraciones turnkey procesadas: {len(turnkey_configs)}")

    # 3. Parsear lista de precios CT 1314
    print("[*] Parseando 1314 LISTA DE PRECIOS DE CT (esto toma unos segundos)...")
    price_sheets = read_xlsx_workbook(PRICE_XLSX)

    productos_procesados = []
    seen_skus = set()
    conteo_categorias = Counter()
    productos_nuevos = []
    cambios_precio = {"subio": 0, "bajo": 0, "igual": 0}
    productos_con_windows = []
    auditoria_software = []
    auditoria_cpus = []
    skus_nuevos_sin_foto = []

    for sheet_name, rows in price_sheets.items():
        if sheet_name in ['LISTA DE PRECIOS', 'INDICE', 'DIRECTORIO', 'DIRECTORIO DE COORDINADORES']:
            continue

        current_subgroup = sheet_name
        for r_num, cells in rows:
            f_val = cells.get('F', '')
            if f_val.upper() == 'CLAVE' and 'G' in cells:
                current_subgroup = clean_text(cells['G'])
                continue
            elif not f_val and any(k in cells for k in ['B', 'C', 'D', 'E']):
                txt = clean_text(' '.join(cells.get(k, '') for k in ['B', 'C', 'D', 'E'] if cells.get(k, '')))
                if len(txt) > 3 and not any(ign in txt.upper() for ign in ['INTERNACIONAL', 'LISTA DE PRECIOS', 'COORDINADOR']):
                    current_subgroup = txt
                continue

            if f_val and f_val.upper() not in ['CLAVE', 'NAN'] and len(f_val) >= 5:
                raw_sku = clean_sku(f_val)
                final_sku = f"A-{raw_sku}"
                if final_sku in seen_skus or raw_sku in seen_skus:
                    continue

                desc = clean_text(cells.get('G', ''))
                price_str = cells.get('J', cells.get('I', ''))

                try:
                    price_val = float(price_str)
                    if price_val <= 0: continue
                except ValueError:
                    continue

                seen_skus.add(final_sku)
                seen_skus.add(raw_sku)

                # Moneda
                col_h = cells.get('H', '').strip().lower()
                if col_h == 'm':
                    ct_cost_mxn = price_val
                    costo_neto_usd = round(price_val / TIPO_CAMBIO, 2)
                else:
                    costo_neto_usd = price_val
                    ct_cost_mxn = price_val * TIPO_CAMBIO

                # Precios oficiales VECTEC
                costo_base_mxn = ct_cost_mxn
                precio_orig = round(costo_base_mxn * FACTOR_LISTA, 2)
                precio_mxn = round(precio_orig * 0.75, 2)
                precio_may = round(precio_mxn * 0.90, 2)

                # Clasificación semántica
                old_item = old_by_sku.get(raw_sku) or old_by_sku.get(final_sku)
                subcat = current_subgroup if current_subgroup and current_subgroup != sheet_name else (old_item.get("subgrupo_label", current_subgroup) if old_item else current_subgroup)
                marca = (old_item.get("m") if old_item and old_item.get("m") not in ["Generica", "GENERIC", ""] else infer_brand(desc, raw_sku))
                full_desc = desc or (old_item.get("d") if old_item else "")
                nombre = desc[:120] if desc else (old_item.get("n", raw_sku) if old_item else raw_sku)

                categoria = clasificar_producto_semantico(
                    raw_sku, nombre, marca, sheet_name=sheet_name,
                    subgrupo_header=subcat, desc=full_desc
                )

                conteo_categorias[categoria] += 1

                # Auditoría específica solicitada por el usuario:
                # "¿Un procesador con Windows se fue a software?"
                desc_u = full_desc.upper()
                if "WINDOWS" in desc_u:
                    productos_con_windows.append({
                        "sku": raw_sku,
                        "nombre": nombre[:60],
                        "cat": categoria,
                        "sheet": sheet_name
                    })

                if categoria in ["sistemas_operativos", "ofimatica_productividad", "software_contable_administrativo", "antivirus_seguridad_digital"]:
                    # Revisar si se coló hardware
                    if any(hw in desc_u for hw in ["PROCESADOR", "RYZEN", "INTEL CORE", "TARJETA MADRE", "MOTHERBOARD", "RAM ", "DDR4", "DDR5", "SSD", "GABINETE", "FUENTE DE PODER", "TARJETA DE VIDEO", "RTX", "GTX", "RX "]):
                        auditoria_software.append({
                            "sku": raw_sku,
                            "nombre": nombre[:60],
                            "categoria_asignada": categoria,
                            "alerta": "HARDWARE EN SOFTWARE"
                        })

                if categoria == "procesadores":
                    auditoria_cpus.append(raw_sku)

                # Comparar precios y novedad
                if old_item:
                    old_p = old_item.get("p", 0)
                    if precio_mxn > old_p:
                        cambios_precio["subio"] += 1
                    elif precio_mxn < old_p:
                        cambios_precio["bajo"] += 1
                    else:
                        cambios_precio["igual"] += 1
                else:
                    productos_nuevos.append({
                        "sku": raw_sku,
                        "nombre": nombre,
                        "categoria": categoria,
                        "precio": precio_mxn,
                        "marca": marca,
                        "sheet": sheet_name,
                        "desc": full_desc
                    })
                    # Verificar si tiene imagen
                    cand1 = os.path.join(IMG_DIR, f"{raw_sku}.webp")
                    cand2 = os.path.join(IMG_DIR, f"{raw_sku}_0.webp")
                    if not (os.path.exists(cand1) or os.path.exists(cand2)):
                        skus_nuevos_sin_foto.append({
                            "sku": raw_sku,
                            "nombre": nombre,
                            "categoria": categoria,
                            "url_ficha": extract_url(full_desc)
                        })

                productos_procesados.append({
                    "sku": final_sku,
                    "cat": categoria,
                    "precio": precio_mxn
                })

    # Guardar reporte de auditoría en JSON para verificación
    reporte = {
        "fecha": "2026-10-03",
        "archivo_precios": "1314 LISTA DE PRECIOS DE CT TOL 100526.xlsx",
        "archivo_configs": "1314 CONFIGURACIONES TOL 100526.xlsx",
        "total_procesados_ct": len(productos_procesados),
        "total_turnkey_configs": len(turnkey_configs),
        "total_skus_nuevos": len(productos_nuevos),
        "cambios_precio": cambios_precio,
        "conteo_por_categoria": dict(conteo_categorias.most_common()),
        "auditoria_software_alertas": auditoria_software,
        "total_cpus_identificados": len(auditoria_cpus),
        "productos_con_windows_total": len(productos_con_windows),
        "skus_nuevos_sin_foto_total": len(skus_nuevos_sin_foto),
        "muestras_nuevos_sin_foto": skus_nuevos_sin_foto[:10],
        "muestras_productos_nuevos": productos_nuevos[:10]
    }

    out_reporte = os.path.join(PCC_DATA_DIR, "auditoria_dry_run_1314.json")
    with open(out_reporte, "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 80)
    print("   RESULTADOS DEL DRY-RUN")
    print("=" * 80)
    print(f"Total productos activos en CT 1314: {len(productos_procesados):,}")
    print(f"Productos nuevos (ingreso en lista 1314): {len(productos_nuevos):,}")
    print(f"Precios actualizados: {cambios_precio['subio']} subieron, {cambios_precio['bajo']} bajaron, {cambios_precio['igual']} sin cambio")
    print(f"Alertas de Hardware colado en Software: {len(auditoria_software)}")
    print(f"Total procesadores (CPUs) auditados: {len(auditoria_cpus)}")
    print(f"Productos con mención 'Windows': {len(productos_con_windows)}")
    print(f"Nuevos productos sin imagen física en disco: {len(skus_nuevos_sin_foto)}")
    print(f"\nReporte JSON completo guardado en: {out_reporte}")
    return reporte


if __name__ == "__main__":
    run_dry_run()
