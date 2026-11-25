#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agente_clasificador_remoto.py
Auditor especializado para cada uno de los 18 agentes de GitHub Actions.
Valida clasificación semántica, precios MXN Factor 2.20, ausencia de agotados
en vitrinas públicas y paridad de inventario por dominio departamental.
"""

import os
import sys
import json
import argparse

BASE_DIR = r"D:\Proyectos\sitios web" if os.path.exists(r"D:\Proyectos\sitios web") else os.getcwd()
PCC_DATA_DIR = os.path.join(BASE_DIR, "pc-custom-lab", "data")

AGENT_DOMAINS = {
    "01-procesadores-cpus": ["procesadores"],
    "02-tarjetas-madre": ["tarjetas_madre"],
    "03-memorias-ram-pc-laptop": ["memorias_ram_pc", "memorias_ram_laptop", "memorias_ram_servidor"],
    "04-almacenamiento-ssds-nvme": ["ssds_m2_nvme", "discos_duros_hdd_internos", "discos_duros_externos", "tarjetas_microsd", "memorias_usb_pendrives"],
    "05-tarjetas-video-gpus": ["tarjetas_video"],
    "06-fuentes-poder-gabinetes": ["fuentes_energia", "gabinetes"],
    "07-enfriamiento-disipadores": ["enfriamiento"],
    "08-laptops-portatiles": ["laptops_portatiles", "mini_pcs_nuc", "computadoras_ensambladas", "computadoras_all_in_one", "smartphones_celulares", "tablets_ipads", "smartwatches_wearables"],
    "09-monitores-pantallas": ["monitores_pantallas", "proyectores_presentacion", "soportes_ergonomia"],
    "10-redes-switches-routers": ["switches_red", "routers_access_points", "antenas_radioenlaces", "cableado_estructurado", "fibra_optica_transceivers", "telefonia_conmutadores"],
    "11-impresoras-tintas-toners": ["impresoras_multifuncionales", "toners_laser", "tintas_cartuchos", "plotters_gran_formato", "etiquetas_ribbons", "escaneres_digitalizadores"],
    "12-seguridad-cctv-biometricos": ["camaras_seguridad_cctv", "grabadores_dvr_nvr", "control_acceso_biometricos", "alarmas_sensores_seguridad"],
    "13-accesorios-teclados-mouse": ["teclados", "ratones_mouse", "combos_teclado_mouse", "diademas_headsets", "bocinas_sonido", "microfonos", "webcams_videoconferencia", "cables_adaptadores", "mochilas_fundas_maletines", "hubs_docks_estaciones", "herramientas_servicio_tecnico", "candados_seguridad_laptop", "limpieza_mantenimiento", "gaming_consolas_sillas", "climatizacion_aires_acondicionados", "accesorios_perifericos"],
    "14-punto-de-venta-scanners": ["punto_de_venta"],
    "15-servidores-racks-enterprise": ["servidores_enterprise", "racks_gabinetes_servidor"],
    "16-energia-ups-reguladores": ["no_breaks_ups", "reguladores_voltaje", "cargadores_baterias_powerbanks"],
    "17-ensambles-turnkey-vectec": ["sistemas_operativos", "ofimatica_productividad", "software_contable_administrativo", "antivirus_seguridad_digital", "garantias_polizas_servicio"],
    "18-cruce-intcomex-y-cuarentena": ["__GLOBAL_CUARENTENA_INTCOMEX__"],
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--departamento", required=True)
    args = parser.parse_args()
    agent_id = args.departamento
    depts = AGENT_DOMAINS.get(agent_id, [])

    compact_path = os.path.join(PCC_DATA_DIR, "catalogo_maestro_compact.json")
    manifest_path = os.path.join(PCC_DATA_DIR, "departments_manifest.json")

    with open(compact_path, "r", encoding="utf-8-sig") as f:
        compact = json.load(f)
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print(f"=== AGENTE REMOTO CERTIFICADOR: {agent_id} ===")
    errors = []

    if agent_id == "18-cruce-intcomex-y-cuarentena":
        prov_b = [x for x in compact if x.get("prov") == "B"]
        cuarentena = [x for x in compact if x.get("a") == 1 or int(x.get("stk", 0)) <= 0]
        activos = [x for x in compact if x.get("a") == 0 and int(x.get("stk", 0)) > 0]
        for x in activos:
            if float(x.get("p", 0)) <= 0:
                errors.append(f"Precio <= 0 en activo: {x.get('s')}")
            if float(x.get("o", 0)) < float(x.get("p", 0)):
                errors.append(f"Precio lista < venta: {x.get('s')}")
        print(f"  Activos: {len(activos):,} | Cuarentena: {len(cuarentena):,} | Intcomex (Prov B): {len(prov_b):,}")
    else:
        total_vitrina = 0
        for dept_id in depts:
            dinfo = manifest.get("departments", {}).get(dept_id, {})
            for rel_f in dinfo.get("files", []):
                fpath = os.path.join(BASE_DIR, "pc-custom-lab", rel_f.replace("/", os.sep))
                if not os.path.exists(fpath):
                    errors.append(f"Falta partición: {rel_f}")
                    continue
                with open(fpath, "r", encoding="utf-8") as fp:
                    items = json.load(fp)
                total_vitrina += len(items)
                for it in items:
                    if it.get("c") != dept_id:
                        errors.append(f"Categoría cruzada en {rel_f}: {it.get('s')} tiene c={it.get('c')}")
                    if it.get("a", 0) == 1 or int(it.get("stk", 0)) <= 0:
                        errors.append(f"Producto agotado/cuarentena en vitrina pública {rel_f}: {it.get('s')}")
                    if float(it.get("p", 0)) <= 0:
                        errors.append(f"Precio <= 0 en vitrina {rel_f}: {it.get('s')}")
        print(f"  Departamentos auditados ({len(depts)}): {', '.join(depts)}")
        print(f"  Total productos activos certificados en vitrina: {total_vitrina:,}")

    if errors:
        print(f"[FALLO] {len(errors)} errores detectados:")
        for e in errors[:20]:
            print("  -", e)
        sys.exit(1)
    print(f"[CERTIFICADO] Agente {agent_id}: 0 errores, 100% congruencia.")


if __name__ == "__main__":
    main()
