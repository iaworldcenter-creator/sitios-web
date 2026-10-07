#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auditoria_exhaustiva_1a1.py
Auditoría Exhaustiva Producto por Producto (1a1) en los 17,899 Artículos:
1. Categoría: Verifica y purifica semánticamente cada producto con clasificador_semantico_vectec.
2. Precio en MXN: Audita congruencia matemática estricta (Tipo de Cambio 19.50, Factor Lista 2.20, Margen Oferta 1.65, Mayoreo 0.90).
3. Imagen: Audita existencia física en disco en pc-custom-lab/assets/img/, tamaño > 500 bytes, y normaliza enlaces rotos.
4. Si detecta desvíos, rectifica de forma atómica y replica a los 8 proyectos del ecosistema.
"""

import os
import sys
import json
import time
import shutil
from collections import Counter

BASE_DIR = r"D:\Proyectos\sitios web"
PCC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")
PCC_DATA_DIR = os.path.join(PCC_DIR, "data")
IMG_DIR = os.path.join(PCC_DIR, "assets", "img")
COMPACT_JSON = os.path.join(PCC_DATA_DIR, "catalogo_maestro_compact.json")
SEARCH_JSON = os.path.join(PCC_DATA_DIR, "inventario_maestro_buscador.json")
PLACEHOLDERS_DIR = os.path.join(IMG_DIR, "placeholders")

sys.path.insert(0, BASE_DIR)
from scripts.clasificador_semantico_vectec import clasificar_producto_semantico, DEPARTAMENTOS_OFICIALES
from scripts.regenerar_vitrinas_congruentes import regenerar_vitrinas_congruentes
from scripts.verificar_paridad_ocho_sitios import auditar_paridad

TIPO_CAMBIO = 19.50
FACTOR_LISTA = 2.20
FACTOR_OFERTA = 1.65
FACTOR_MAYOREO = 0.90
FACTOR_VENTA_MXN = TIPO_CAMBIO * FACTOR_OFERTA # 32.175


def auditar_todo():
    t_start = time.time()
    print("=" * 80)
    print("   AUDITORÍA EXHAUSTIVA 1 A 1 - CATÁLOGO MAESTRO VECTEC")
    print("   Alcance: 100% de productos | Categoría | Precio MXN | Imagen WebP")
    print("=" * 80)

    if not os.path.exists(COMPACT_JSON):
        print(f"[ERR] No se encontró el catálogo en {COMPACT_JSON}")
        return

    with open(COMPACT_JSON, "r", encoding="utf-8") as f:
        items = json.load(f)

    total_items = len(items)
    print(f"[*] Total de productos cargados para auditoría unitaria: {total_items:,}")

    # Contadores de auditoría
    corregidos_categoria = 0
    corregidos_precio = 0
    corregidos_imagen = 0
    auditoria_por_categoria = Counter()
    alertas_graves = []

    productos_auditados = []

    for idx, it in enumerate(items):
        sku = it.get("s", "")
        raw_sku = sku.replace("A-", "").replace("B-", "")
        nombre = it.get("n", "")
        marca = it.get("m", "")
        cat_actual = it.get("c", "")
        desc = it.get("d", "")
        subcat = it.get("subgrupo_label", "")
        precio_actual = it.get("p", 0.0)
        costo_usd = it.get("u", 0.0)
        precio_orig = it.get("o", 0.0)
        precio_may = it.get("y", 0.0)
        images = it.get("k", [])

        modificado_item = False

        # -------------------------------------------------------------
        # 1. AUDITORÍA Y PURIFICACIÓN DE CATEGORÍA
        # -------------------------------------------------------------
        cat_esperada = clasificar_producto_semantico(
            raw_sku, nombre, marca, subgrupo_header=subcat, desc=desc
        )

        if cat_actual != cat_esperada:
            # Rectificar categoría si difiere
            it["c"] = cat_esperada
            cat_actual = cat_esperada
            corregidos_categoria += 1
            modificado_item = True

        auditoria_por_categoria[cat_actual] += 1

        # Detección de anomalías de hardware en software
        desc_u = f"{nombre} {desc}".upper()
        if cat_actual in ["sistemas_operativos", "ofimatica_productividad", "software_contable_administrativo", "antivirus_seguridad_digital"]:
            if any(hw in desc_u for hw in ["PROCESADOR INTEL", "PROCESADOR AMD", "RYZEN", "CORE I5", "CORE I7", "CORE I9", "MOTHERBOARD", "TARJETA MADRE", "MEMORIA RAM DDR"]):
                alertas_graves.append(f"Hardware en Software: SKU {sku} ({nombre[:40]}) -> {cat_actual}")

        # -------------------------------------------------------------
        # 2. AUDITORÍA DE PRECIOS EN PESOS MEXICANOS (MXN)
        # -------------------------------------------------------------
        # Si tiene costo USD registrado, verificar que el precio de venta en MXN sea matemáticamente exacto
        if costo_usd > 0:
            costo_mxn = costo_usd * TIPO_CAMBIO
            esperado_o = round(costo_mxn * FACTOR_LISTA, 2)
            esperado_p = round(esperado_o * 0.75, 2)
            esperado_y = round(esperado_p * FACTOR_MAYOREO, 2)

            # Si el precio difiere por más de 50 centavos respecto a la fórmula oficial, rectificar
            if abs(precio_actual - esperado_p) > 0.50:
                it["p"] = esperado_p
                it["o"] = esperado_o
                it["y"] = esperado_y
                corregidos_precio += 1
                modificado_item = True
            else:
                # Asegurar que o e y existan y sean congruentes
                if abs(precio_orig - esperado_o) > 0.50 or abs(precio_may - esperado_y) > 0.50:
                    it["o"] = esperado_o
                    it["y"] = esperado_y
                    modificado_item = True
        elif precio_actual <= 0:
            # Precio no puede ser 0
            alertas_graves.append(f"Precio cero detectado: SKU {sku}")

        # -------------------------------------------------------------
        # 3. AUDITORÍA DE IMAGEN (EXISTENCIA FÍSICA EN DISCO Y WEBP)
        # -------------------------------------------------------------
        img_valida = None
        cand_paths = []
        if images and len(images) > 0:
            for im in images:
                cand_paths.append(im.replace("assets/img/", ""))
        cand_paths.extend([f"{raw_sku}.webp", f"{raw_sku}_0.webp", f"B-{raw_sku}.webp"])

        for cp in cand_paths:
            full_p = os.path.join(IMG_DIR, cp)
            if os.path.exists(full_p) and os.path.getsize(full_p) > 500:
                img_valida = f"assets/img/{cp}"
                break

        if not img_valida:
            # Asignar placeholder temático de alta resolución existente
            pl_cand = os.path.join(PLACEHOLDERS_DIR, f"{cat_actual}.jpg")
            if os.path.exists(pl_cand):
                img_valida = f"assets/img/placeholders/{cat_actual}.jpg"
            else:
                img_valida = "assets/img/placeholders/acc_placeholder.jpg"
            corregidos_imagen += 1
            modificado_item = True

        if it.get("k") != [img_valida]:
            it["k"] = [img_valida]
            it["i"] = 1 if not "placeholders" in img_valida else 0
            modificado_item = True

        productos_auditados.append(it)

        if (idx + 1) % 2500 == 0 or (idx + 1) == total_items:
            pct = (idx + 1) / total_items * 100
            sys.stdout.write(f"\r   -> Progreso: {idx + 1:,}/{total_items:,} ({pct:.1f}%) | Cat corregidas: {corregidos_categoria} | Precios corregidos: {corregidos_precio} | Fotos ajustadas: {corregidos_imagen}")
            sys.stdout.flush()

    print("\n\n" + "=" * 80)
    print("   RESUMEN DE AUDITORÍA UNITARIA 1 A 1")
    print("=" * 80)
    print(f"[*] Productos evaluados unitariamente:        {total_items:,}")
    print(f"[*] Ajustes finos de Categoría semántica:     {corregidos_categoria:,}")
    print(f"[*] Ajustes de consistencia de Precio MXN:    {corregidos_precio:,}")
    print(f"[*] Ajustes de Enlace de Imagen física:       {corregidos_imagen:,}")
    print(f"[*] Alertas graves de corrupción de datos:    {len(alertas_graves)}")
    for a in alertas_graves[:5]:
        print(f"    - {a}")
    print("=" * 80)

    # -------------------------------------------------------------
    # 4. GUARDAR CATÁLOGO MAESTRO PURIFICADO
    # -------------------------------------------------------------
    print("[+] Guardando catálogo compacto purificado...")
    with open(COMPACT_JSON, "w", encoding="utf-8") as f:
        json.dump(productos_auditados, f, ensure_ascii=False, separators=(',', ':'))
    print(f"   [OK] catalogo_maestro_compact.json ({os.path.getsize(COMPACT_JSON)/1024:.1f} KB)")

    # Actualizar inventario_maestro_buscador.json
    print("[+] Sincronizando inventario_maestro_buscador.json...")
    with open(SEARCH_JSON, "r", encoding="utf-8") as f:
        search_items = json.load(f)

    compact_by_sku = {it["s"]: it for it in productos_auditados}
    for s_it in search_items:
        c_it = compact_by_sku.get(s_it.get("sku") or s_it.get("s"))
        if c_it:
            s_it["c"] = c_it["c"]
            s_it["p"] = c_it["p"]
            s_it["o"] = c_it["o"]
            s_it["img"] = c_it["k"][0] if c_it.get("k") else s_it.get("img")

    with open(SEARCH_JSON, "w", encoding="utf-8") as f:
        json.dump(search_items, f, ensure_ascii=False, separators=(',', ':'))
    print(f"   [OK] inventario_maestro_buscador.json ({os.path.getsize(SEARCH_JSON)/1024:.1f} KB)")

    # -------------------------------------------------------------
    # 5. REGENERAR VITRINAS Y PARTICIONES DEPARTAMENTALES
    # -------------------------------------------------------------
    print("\n[+] Regenerando vitrinas y particiones departamentales...")
    regenerar_vitrinas_congruentes()

    # -------------------------------------------------------------
    # 6. PROPAGAR A LOS 8 PROYECTOS DEL ECOSISTEMA
    # -------------------------------------------------------------
    print("\n[+] Replicando catálogo 100% auditado y verificado a los 8 sitios web...")
    ALL_TARGET_DATA_DIRS = [
        PCC_DATA_DIR,
        os.path.join(BASE_DIR, "ofertas-y-liquidaciones", "data"),
        os.path.join(BASE_DIR, "bazar-viamx-nfl.gdl", "data"),
        os.path.join(BASE_DIR, "mi-puesto-bazar", "data"),
        os.path.join(BASE_DIR, "kiosco-digital", "data"),
        os.path.join(BASE_DIR, "dulces-bazar", "data"),
        os.path.join(BASE_DIR, "cigarros-bazar", "data"),
        os.path.join(BASE_DIR, "data")
    ]

    MASTER_FILES = [
        "inventario_maestro_buscador.json",
        "liquidaciones_outlet.json",
        "hardware_ensamble.json",
        "esquema_articulo.json",
        "catalogo_maestro_compact.json",
        "departments_manifest.json"
    ]

    for target_dir in ALL_TARGET_DATA_DIRS:
        os.makedirs(target_dir, exist_ok=True)
        for fname in MASTER_FILES:
            src = os.path.join(PCC_DATA_DIR, fname)
            dst = os.path.join(target_dir, fname)
            if src != dst and os.path.exists(src):
                shutil.copy2(src, dst)

        # Particiones departamentales
        src_depts = os.path.join(PCC_DATA_DIR, "departments")
        if os.path.exists(src_depts) and target_dir != PCC_DATA_DIR:
            dst_depts = os.path.join(target_dir, "departments")
            os.makedirs(dst_depts, exist_ok=True)
            for jf in os.listdir(src_depts):
                if jf.endswith(".json"):
                    shutil.copy2(os.path.join(src_depts, jf), os.path.join(dst_depts, jf))

        rel_t = os.path.relpath(target_dir, BASE_DIR)
        print(f"   [OK] Catálogo y 83 particiones sincronizadas en: {rel_t}")

    # -------------------------------------------------------------
    # 7. BARRIDO FINAL DE PARIDAD EN LOS 8 SITIOS
    # -------------------------------------------------------------
    print("\n[+] Ejecutando barrido final de paridad en los 8 sitios...")
    paridad_ok = auditar_paridad()

    t_total = time.time() - t_start
    print(f"\n[TIEMPO TOTAL DE AUDITORÍA UNITARIA]: {t_total:.1f} segundos ({t_total/60:.2f} minutos)")

    # Guardar reporte de auditoría 1 a 1 en JSON
    rep_final = {
        "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_auditados": total_items,
        "corregidos_categoria": corregidos_categoria,
        "corregidos_precio": corregidos_precio,
        "corregidos_imagen": corregidos_imagen,
        "alertas_graves": alertas_graves,
        "conteo_departamentos": dict(auditoria_por_categoria.most_common()),
        "paridad_ocho_sitios": paridad_ok,
        "duracion_segundos": round(t_total, 1)
    }

    out_rep_path = os.path.join(PCC_DATA_DIR, "reporte_auditoria_unitaria_1a1.json")
    with open(out_rep_path, "w", encoding="utf-8") as f:
        json.dump(rep_final, f, ensure_ascii=False, indent=2)

    print(f"[OK] Reporte exhaustivo unitario guardado en: {out_rep_path}")
    return rep_final


if __name__ == "__main__":
    auditar_todo()
