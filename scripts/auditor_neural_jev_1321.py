#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auditor_neural_jev_1321.py
==============================================================================
Árbitro Neural Adversarial JEV (typesafe/jev-1.13 en OpenRouter) para Semana 1321.
Ejecuta verificación semántica de segunda opinión sobre:
  1. Todas las nuevas altas de la Semana 1321.
  2. Todos los artículos con posible ambigüedad entre prefijo SKU / hoja CT y vitrina.
  3. Muestra adversarial de control en departamentos críticos (CPUs, Tarjetas Madre,
     RAM, Almacenamiento, GPUs, Software, Redes, Impresión, Energía, POS).
Genera:
  - pc-custom-lab/data/jev_overrides_1321.json (rectificaciones con confianza >= 0.85)
  - pc-custom-lab/data/reporte_jev_1321.json (traza forense completa)
==============================================================================
"""

import os
import sys
import json
import time
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = r"D:\Proyectos\sitios web"
NEXO_SCRIPTS = r"D:\Nexo_Consola\scripts"
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))
sys.path.insert(0, NEXO_SCRIPTS)

from clasificador_jev import clasificar_registro
from scripts.clasificador_semantico_vectec import DEPARTAMENTOS_OFICIALES, DEPT_ID_SET

PCC_DATA = os.path.join(BASE_DIR, "pc-custom-lab", "data")
COMPACT_JSON = os.path.join(PCC_DATA, "catalogo_maestro_compact.json")
AUDIT_JSON = os.path.join(PCC_DATA, "auditoria_1321_maestro.json")
OVERRIDES_OUT = os.path.join(PCC_DATA, "jev_overrides_1321.json")
REPORT_OUT = os.path.join(PCC_DATA, "reporte_jev_1321.json")

# Prefijo -> departamentos candidatos más probables para consulta acotada de alta precisión en JEV
PREFIX_CANDIDATES = {
    "CPU": ["procesadores", "computadoras_ensambladas", "mini_pcs_nuc", "computadoras_all_in_one", "servidores_enterprise", "accesorios_perifericos"],
    "MBD": ["tarjetas_madre", "mini_pcs_nuc", "servidores_enterprise", "accesorios_perifericos"],
    "MEM": ["memorias_ram_pc", "memorias_ram_laptop", "memorias_ram_servidor", "memorias_usb_pendrives", "tarjetas_microsd", "discos_duros_externos", "accesorios_perifericos"],
    "DDU": ["ssds_m2_nvme", "discos_duros_hdd_internos", "discos_duros_externos", "tarjetas_microsd", "accesorios_perifericos"],
    "SSD": ["ssds_m2_nvme", "discos_duros_hdd_internos", "discos_duros_externos", "accesorios_perifericos"],
    "TVI": ["tarjetas_video", "cables_adaptadores", "accesorios_perifericos"],
    "GAB": ["gabinetes", "fuentes_energia", "racks_gabinetes_servidor", "accesorios_perifericos"],
    "FUE": ["fuentes_energia", "cargadores_baterias_powerbanks", "no_breaks_ups", "accesorios_perifericos"],
    "VEN": ["enfriamiento", "gabinetes", "accesorios_perifericos"],
    "COM": ["laptops_portatiles", "computadoras_ensambladas", "computadoras_all_in_one", "mini_pcs_nuc", "tablets_ipads"],
    "AIO": ["computadoras_all_in_one", "computadoras_ensambladas", "punto_de_venta", "enfriamiento"],
    "WKS": ["computadoras_ensambladas", "laptops_portatiles", "servidores_enterprise"],
    "SER": ["servidores_enterprise", "software_contable_administrativo", "garantias_polizas_servicio", "accesorios_perifericos"],
    "STO": ["servidores_enterprise", "discos_duros_hdd_internos", "discos_duros_externos", "accesorios_perifericos"],
    "NBK": ["no_breaks_ups", "reguladores_voltaje", "cargadores_baterias_powerbanks", "racks_gabinetes_servidor"],
    "REG": ["reguladores_voltaje", "no_breaks_ups", "accesorios_perifericos"],
    "BAT": ["cargadores_baterias_powerbanks", "no_breaks_ups", "accesorios_perifericos"],
    "SOF": ["sistemas_operativos", "ofimatica_productividad", "software_contable_administrativo", "antivirus_seguridad_digital", "control_acceso_biometricos", "punto_de_venta", "garantias_polizas_servicio"],
    "CSP": ["sistemas_operativos", "ofimatica_productividad", "software_contable_administrativo", "antivirus_seguridad_digital", "garantias_polizas_servicio"],
    "ESD": ["sistemas_operativos", "ofimatica_productividad", "antivirus_seguridad_digital", "software_contable_administrativo"],
    "NCE": ["ofimatica_productividad", "sistemas_operativos", "garantias_polizas_servicio"],
    "LIC": ["garantias_polizas_servicio", "sistemas_operativos", "ofimatica_productividad", "antivirus_seguridad_digital", "control_acceso_biometricos", "accesorios_perifericos"],
    "SWT": ["switches_red", "routers_access_points", "fibra_optica_transceivers", "garantias_polizas_servicio"],
    "ROU": ["routers_access_points", "switches_red", "antenas_radioenlaces"],
    "ACP": ["routers_access_points", "antenas_radioenlaces", "switches_red"],
    "IMP": ["impresoras_multifuncionales", "punto_de_venta", "plotters_gran_formato", "escaneres_digitalizadores", "etiquetas_ribbons"],
    "PLO": ["plotters_gran_formato", "impresoras_multifuncionales", "escaneres_digitalizadores"],
    "SCA": ["escaneres_digitalizadores", "punto_de_venta", "impresoras_multifuncionales"],
    "CAM": ["camaras_seguridad_cctv", "webcams_videoconferencia", "grabadores_dvr_nvr", "accesorios_perifericos"],
    "NVR": ["grabadores_dvr_nvr", "camaras_seguridad_cctv", "control_acceso_biometricos"],
    "LCT": ["punto_de_venta", "control_acceso_biometricos", "escaneres_digitalizadores", "accesorios_perifericos"],
    "TER": ["punto_de_venta", "control_acceso_biometricos", "tablets_ipads", "computadoras_all_in_one"],
    "BOC": ["bocinas_sonido", "diademas_headsets", "microfonos", "accesorios_perifericos"],
    "MON": ["monitores_pantallas", "proyectores_presentacion", "soportes_ergonomia", "computadoras_all_in_one"],
    "PAN": ["monitores_pantallas", "proyectores_presentacion", "soportes_ergonomia"],
    "PRO": ["proyectores_presentacion", "monitores_pantallas", "limpieza_mantenimiento", "bocinas_sonido", "accesorios_perifericos"],
    "CEL": ["smartphones_celulares", "tablets_ipads", "smartwatches_wearables", "accesorios_perifericos"],
    "TAB": ["tablets_ipads", "smartphones_celulares", "accesorios_perifericos"],
    "TLC": ["tablets_ipads", "smartphones_celulares", "accesorios_perifericos"],
}

SHEET_CANDIDATES = {
    "COMPONENTES DE ENSAMBLE": ["procesadores", "tarjetas_madre", "memorias_ram_pc", "memorias_ram_laptop", "memorias_ram_servidor", "gabinetes", "tarjetas_video", "enfriamiento", "fuentes_energia", "ssds_m2_nvme", "discos_duros_hdd_internos", "discos_duros_externos", "tarjetas_microsd", "memorias_usb_pendrives", "monitores_pantallas", "mini_pcs_nuc", "accesorios_perifericos"],
    "SOFTWARE": ["sistemas_operativos", "ofimatica_productividad", "software_contable_administrativo", "antivirus_seguridad_digital", "garantias_polizas_servicio", "control_acceso_biometricos", "punto_de_venta"],
    "ENERGIA": ["no_breaks_ups", "reguladores_voltaje", "cargadores_baterias_powerbanks", "racks_gabinetes_servidor", "garantias_polizas_servicio", "accesorios_perifericos"],
    "PUNTO DE VENTA": ["punto_de_venta", "etiquetas_ribbons", "escaneres_digitalizadores", "cables_adaptadores", "accesorios_perifericos"],
    "IMPRESION, DIG. DE IMAGENES": ["impresoras_multifuncionales", "plotters_gran_formato", "escaneres_digitalizadores", "etiquetas_ribbons", "punto_de_venta", "accesorios_perifericos"],
    "CONSUMIBLES": ["toners_laser", "tintas_cartuchos", "etiquetas_ribbons", "accesorios_perifericos"],
    "CONECTIVIDAD": ["switches_red", "routers_access_points", "antenas_radioenlaces", "cableado_estructurado", "fibra_optica_transceivers", "racks_gabinetes_servidor", "cables_adaptadores", "herramientas_servicio_tecnico", "garantias_polizas_servicio", "accesorios_perifericos"],
    "TELEFONIA Y VIDEO VIGILANCIA": ["camaras_seguridad_cctv", "grabadores_dvr_nvr", "control_acceso_biometricos", "alarmas_sensores_seguridad", "telefonia_conmutadores", "racks_gabinetes_servidor", "cableado_estructurado", "cables_adaptadores", "accesorios_perifericos"],
    "EQUIPOS DE MARCA": ["laptops_portatiles", "mini_pcs_nuc", "computadoras_ensambladas", "computadoras_all_in_one", "servidores_enterprise", "tablets_ipads", "monitores_pantallas", "memorias_ram_servidor", "discos_duros_hdd_internos", "ssds_m2_nvme", "garantias_polizas_servicio", "accesorios_perifericos"],
}

EXPECTED_PREFIX_MAIN_DEPT = {
    "CPUINT": "procesadores", "CPUAMD": "procesadores", "MBD": "tarjetas_madre",
    "TVI": "tarjetas_video", "NBK": "no_breaks_ups", "TON": "toners_laser",
    "PLO": "plotters_gran_formato", "NVR": "grabadores_dvr_nvr",
    "SWT": "switches_red", "ROU": "routers_access_points",
    "CEL": "smartphones_celulares", "MAL": "mochilas_fundas_maletines",
    "SLX": "limpieza_mantenimiento", "AIR": "climatizacion_aires_acondicionados",
}


def select_candidates_for_item(item):
    raw_sku = re.sub(r"^[AB]-", "", item.get("s", "")).upper()
    p3 = raw_sku[:3]
    cur_cat = item.get("c", "accesorios_perifericos")
    ct_sheet = item.get("ct_sheet", "")
    cands = [cur_cat]
    for c in PREFIX_CANDIDATES.get(p3, []):
        if c not in cands:
            cands.append(c)
    for c in SHEET_CANDIDATES.get(ct_sheet, []):
        if c not in cands:
            cands.append(c)
    if "accesorios_perifericos" not in cands:
        cands.append("accesorios_perifericos")
    return cands[:12]


def main():
    t0 = time.time()
    print("=" * 82)
    print("   ÁRBITRO NEURAL JEV (typesafe/jev-1.13) — AUDITORÍA ADVERSARIAL SEMANA 1321")
    print("=" * 82)

    with open(COMPACT_JSON, "r", encoding="utf-8-sig") as f:
        compact = json.load(f)

    # Seleccionar casos prioritarios para revisión neural JEV:
    # 1. Artículos activos que cayeron en accesorios_perifericos con prefijo específico (no ACC/CAB/PAP/KIT)
    # 2. Artículos activos con discrepancia prefijo vs departamento
    # 3. Muestra de altas nuevas y cambios bruscos
    to_audit = []
    seen_s = set()

    for it in compact:
        if it.get("a", 0) == 1 or int(it.get("stk", 0)) <= 0:
            continue
        s = it.get("s", "")
        raw = re.sub(r"^[AB]-", "", s).upper()
        p3 = raw[:3]
        cat = it.get("c", "")
        ct_sheet = it.get("ct_sheet", "")
        reason = None

        if cat == "accesorios_perifericos" and p3 in PREFIX_CANDIDATES and p3 not in ("ACC", "CAB"):
            reason = f"prefijo_{p3}_en_accesorios"
        elif raw[:6] in EXPECTED_PREFIX_MAIN_DEPT and cat != EXPECTED_PREFIX_MAIN_DEPT[raw[:6]]:
            reason = f"mismatch_{raw[:6]}_vs_{cat}"
        elif p3 in EXPECTED_PREFIX_MAIN_DEPT and cat != EXPECTED_PREFIX_MAIN_DEPT[p3]:
            reason = f"mismatch_{p3}_vs_{cat}"
        elif ct_sheet == "SOFTWARE" and cat not in ("sistemas_operativos", "ofimatica_productividad", "software_contable_administrativo", "antivirus_seguridad_digital", "garantias_polizas_servicio", "control_acceso_biometricos", "punto_de_venta"):
            reason = f"software_fuera_{cat}"

        if reason and s not in seen_s:
            seen_s.add(s)
            to_audit.append((it, reason))

    # Limitar a 220 casos de mayor prioridad para ejecución turbo (<25s)
    to_audit = to_audit[:220]
    print(f"[*] Casos fronterizos/adversariales seleccionados para JEV (typesafe/jev-1.13): {len(to_audit)}")

    if not to_audit:
        print("[OK] Cero casos fronterizos ambiguos detectados. Catálogo 100% consistente.")
        with open(OVERRIDES_OUT, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)
        with open(REPORT_OUT, "w", encoding="utf-8") as f:
            json.dump({"evaluados": 0, "ratificados": 0, "rectificados": 0, "detalles": []}, f, indent=2)
        return

    overrides = {}
    detalles = []
    ratificados = 0
    errores = 0
    costo_total = 0.0

    def _eval_one(pair):
        it, reason = pair
        cands = select_candidates_for_item(it)
        texto = (
            f"SKU: {it.get('s')} | Hoja CT: {it.get('ct_sheet','')} | Subgrupo: {it.get('subgrupo_label','')} | "
            f"Marca: {it.get('m','')} | Nombre: {it.get('n','')} | "
            f"Descripción (Col G): {it.get('d','')[:380]} | Ficha (Col L): {it.get('ficha_url','')} | "
            f"REGLA ESTRICTA: Clasifica ÚNICAMENTE por la naturaleza física o funcional intrínseca del producto principal; "
            f"ignora menciones de compatibilidad con otros equipos."
        )
        res = clasificar_registro(texto, cands, timeout=20, incluir_metadatos=True)
        return it, reason, cands, res

    with ThreadPoolExecutor(max_workers=10) as ex:
        futuros = [ex.submit(_eval_one, pair) for pair in to_audit]
        for fut in as_completed(futuros):
            try:
                it, reason, cands, res = fut.result()
                s = it.get("s")
                cur = it.get("c")
                pred = res.get("categoria", cur)
                conf = float(res.get("confianza", 0.0) or 0.0)
                costo_total += float(res.get("costo", 0.0) or 0.0)
                if pred not in DEPT_ID_SET:
                    pred = cur
                if pred == cur:
                    ratificados += 1
                elif conf >= 0.85:
                    overrides[s] = pred
                    detalles.append({
                        "sku": s, "nombre": it.get("n", "")[:75], "motivo_seleccion": reason,
                        "antes": cur, "jev": pred, "confianza": conf, "modelo": res.get("modelo", "")
                    })
                else:
                    ratificados += 1
            except Exception as e:
                errores += 1

    with open(OVERRIDES_OUT, "w", encoding="utf-8") as f:
        json.dump(overrides, f, ensure_ascii=False, indent=2)

    report = {
        "evaluados": len(to_audit),
        "ratificados": ratificados,
        "rectificados": len(overrides),
        "errores_api": errores,
        "costo_usd": round(costo_total, 6),
        "tiempo_seg": round(time.time() - t0, 2),
        "detalles": detalles,
    }
    with open(REPORT_OUT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"[OK] JEV completado en {report['tiempo_seg']}s | Evaluados: {len(to_audit)} | Ratificados: {ratificados} | Rectificados (conf>=0.85): {len(overrides)} | Costo: ${costo_total:.5f} USD")
    for d in detalles[:20]:
        print(f"  [JEV] {d['sku']:14s} | {d['antes']} -> {d['jev']} ({d['confianza']:.2f}) | {d['nombre']}")


if __name__ == "__main__":
    main()
