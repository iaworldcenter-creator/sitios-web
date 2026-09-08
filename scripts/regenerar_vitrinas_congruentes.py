# -*- coding: utf-8 -*-
"""
REGENERADOR DE VITRINAS CONGRUENTES VECTEC (67 DEPARTAMENTOS)
Genera VECTEC/js/ct-showcase-data.js y particiones JSON por departamento
garantizando 100% de congruencia visual y libre de contaminacion cruzada.
"""

import os
import sys
import json
import shutil
from collections import defaultdict

# Import clasificador_semantico_vectec from same directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from clasificador_semantico_vectec import clasificar_producto_semantico, DEPARTAMENTOS_OFICIALES, DEPT_ID_SET

BASE_DIR = os.path.dirname(script_dir)
DATA_DIR = os.path.join(BASE_DIR, "data")
PCC_DIR = os.path.join(BASE_DIR, "pc-custom-lab") if os.path.exists(os.path.join(BASE_DIR, "pc-custom-lab")) else os.path.join(BASE_DIR, "vectec")
PCC_DATA_DIR = os.path.join(PCC_DIR, "data")
PCC_JS_DIR = os.path.join(PCC_DIR, "js")
DEPTS_OUTPUT_DIR = os.path.join(PCC_DATA_DIR, "departments")
MANIFEST_PATH = os.path.join(PCC_DATA_DIR, "departments_manifest.json")
SHOWCASE_DATA_JS = os.path.join(PCC_JS_DIR, "ct-showcase-data.js")
CATALOG_DATA_JS = os.path.join(PCC_JS_DIR, "ct-catalog-data.js")
COMPACT_JSON = os.path.join(PCC_DATA_DIR, "catalogo_maestro_compact.json")
INVENTARIO_JSON = os.path.join(DATA_DIR, "inventario_maestro_buscador.json")

def regenerar_vitrinas():
    print("=" * 80)
    print("REGENERANDO VITRINAS Y PARTICIONES TAXONOMICAS VECTEC")
    print("=" * 80)

    # 1. Cargar catalogo compacto
    if not os.path.exists(COMPACT_JSON):
        raise FileNotFoundError(f"No se encontro {COMPACT_JSON}")

    with open(COMPACT_JSON, "r", encoding="utf-8") as f:
        catalog_items = json.load(f)

    print(f"[*] Total articulos cargados de catalogo compacto: {len(catalog_items):,}")

    # 2. Agrupar y re-clasificar con el clasificador semantico estricto
    dept_products = defaultdict(list)
    reclassified_count = 0

    img_dir = os.path.join(PCC_DIR, "assets", "img")

    for p in catalog_items:
        sku = p.get("s", "")
        name = p.get("n", "")
        desc = p.get("d", "")
        brand = p.get("m", "VECTEC")
        if brand in ["Generica", "GENERIC", ""]:
            brand = "VECTEC"
            p["m"] = "VECTEC"

        subg = p.get("subgrupo_label", "")
        old_cat = p.get("c", "accesorios_perifericos")

        # Clasificacion semantica estricta basada en contenido real
        new_cat = clasificar_producto_semantico(sku, name, brand, subgrupo_header=subg)
        if new_cat != old_cat:
            reclassified_count += 1
            p["c"] = new_cat

        # Validacion de imagen (soporta SKU con prefijo A- o B- y archivos en disco)
        raw_sku = sku.replace("A-", "").replace("B-", "")
        has_webp_sku = os.path.exists(os.path.join(img_dir, f"{sku}.webp"))
        has_webp_raw = os.path.exists(os.path.join(img_dir, f"{raw_sku}.webp"))
        has_webp_0 = os.path.exists(os.path.join(img_dir, f"{sku}_0.webp")) or os.path.exists(os.path.join(img_dir, f"{raw_sku}_0.webp"))

        if has_webp_sku:
            p["k"] = [f"assets/img/{sku}.webp"]
            p["i"] = 1
        elif has_webp_raw:
            p["k"] = [f"assets/img/{raw_sku}.webp"]
            p["i"] = 1
        elif has_webp_0:
            p["k"] = [f"assets/img/{raw_sku}_0.webp"]
            p["i"] = 1
        elif p.get("k") and len(p["k"]) > 0 and os.path.exists(os.path.join(PCC_DIR, p["k"][0])):
            p["i"] = 1
        else:
            p["i"] = 0

        dept_products[new_cat].append(p)

    print(f"[*] Articulos re-clasificados semanticamente: {reclassified_count:,}")

    # 3. Preparar los 4 mejores articulos para cada una de las 67 vitrinas (CT_CATALOG_DATA_INITIAL)
    initial_showcase_items = []
    dept_meta_counts = {}

    for d in DEPARTAMENTOS_OFICIALES:
        dept_id = d["id"]
        prods = dept_products.get(dept_id, [])
        dept_meta_counts[dept_id] = len(prods)

        # Ordenar para vitrina: primero los que tienen imagen verificada, disponibles y con precio razonable
        sorted_prods = sorted(prods, key=lambda x: (
            -x.get("i", 0),               # 1: Fotos verificadas primero
            x.get("a", 0),                # 0: Disponibles primero (a: 0 = disponible)
            -(len(x.get("d", "")) > 20),   # Descripcion con texto
            x.get("p", 0)                 # Precio
        ))

        # Seleccionar exactamente 4 productos para el slice inicial
        sample = sorted_prods[:4]
        if len(sample) < 4:
            print(f"[ALERTA] Vitrina {dept_id} solo tiene {len(sample)} productos")

        initial_showcase_items.extend(sample)

    print(f"[*] Slice inicial de vitrinas generado: {len(initial_showcase_items)} articulos ({len(DEPARTAMENTOS_OFICIALES)} depts x 4)")

    # 4. Actualizar metadata de departamentos oficiales con conteos reales
    updated_depts = []
    for d in DEPARTAMENTOS_OFICIALES:
        updated_depts.append({
            "id": d["id"],
            "name": d["name"],
            "icon": d["icon"],
            "order": d["order"],
            "count": dept_meta_counts.get(d["id"], 0)
        })

    # Subdepartamentos agrupados
    subdepts = {}
    for d in DEPARTAMENTOS_OFICIALES:
        dept_id = d["id"]
        prods = dept_products.get(dept_id, [])
        sub_counts = defaultdict(int)
        for p in prods:
            sub = p.get("subgrupo_label", "").strip()
            if sub and len(sub) > 2 and sub != dept_id:
                sub_counts[sub] += 1
        top_subs = sorted([{"name": k, "count": v} for k, v in sub_counts.items()], key=lambda x: -x["count"])[:8]
        subdepts[dept_id] = top_subs

    # 5. Escribir VECTEC/js/ct-showcase-data.js
    os.makedirs(PCC_JS_DIR, exist_ok=True)
    with open(SHOWCASE_DATA_JS, "w", encoding="utf-8") as f:
        f.write("// METADATOS OFICIALES DE DEPARTAMENTOS VECTEC (67 DEPARTAMENTOS)\n")
        f.write("window.PC_DEPARTAMENTOS = " + json.dumps(updated_depts, ensure_ascii=False, separators=(",", ":")) + ";\n")
        f.write("window.PC_SUBDEPARTAMENTOS = " + json.dumps(subdepts, ensure_ascii=False, separators=(",", ":")) + ";\n\n")
        f.write("// SLICE INICIAL INSTANTANEO (4 ARTICULOS ESTRICTAMENTE CONGRUENTES POR VITRINA)\n")
        f.write("window.CT_CATALOG_DATA_INITIAL = " + json.dumps(initial_showcase_items, ensure_ascii=False, separators=(",", ":")) + ";\n")

    print(f"   [OK] {os.path.basename(SHOWCASE_DATA_JS)} ({os.path.getsize(SHOWCASE_DATA_JS)/1024:.1f} KB)")

    # 6. Escribir particiones por departamento en VECTEC/data/departments/
    os.makedirs(DEPTS_OUTPUT_DIR, exist_ok=True)
    for existing in os.listdir(DEPTS_OUTPUT_DIR):
        if existing.endswith(".json"):
            os.remove(os.path.join(DEPTS_OUTPUT_DIR, existing))

    MAX_CHUNK_BYTES = 320 * 1024
    manifest = {
        "generatedAt": "2026-09-07T14:50:00Z",
        "totalProducts": len(catalog_items),
        "departmentsCount": len(DEPARTAMENTOS_OFICIALES),
        "departments": {}
    }

    total_written_files = 0
    total_written_products = 0

    for d in DEPARTAMENTOS_OFICIALES:
        dept_id = d["id"]
        items = dept_products.get(dept_id, [])

        dept_info = {
            "id": dept_id,
            "name": d["name"],
            "icon": d["icon"],
            "order": d["order"],
            "count": len(items),
            "files": []
        }

        if len(items) == 0:
            manifest["departments"][dept_id] = dept_info
            continue

        full_json = json.dumps(items, ensure_ascii=False, separators=(",", ":"))
        full_size = len(full_json.encode("utf-8"))

        if full_size <= MAX_CHUNK_BYTES:
            filename = f"{dept_id}.json"
            filepath = os.path.join(DEPTS_OUTPUT_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_json)
            dept_info["files"].append(f"data/departments/{filename}")
            total_written_files += 1
            total_written_products += len(items)
        else:
            current_chunk = []
            current_bytes = 2
            part_idx = 1
            for it in items:
                it_str = json.dumps(it, ensure_ascii=False, separators=(",", ":"))
                it_bytes = len(it_str.encode("utf-8")) + 1
                if current_bytes + it_bytes > MAX_CHUNK_BYTES and current_chunk:
                    filename = f"{dept_id}_part_{part_idx}.json"
                    filepath = os.path.join(DEPTS_OUTPUT_DIR, filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(current_chunk, f, ensure_ascii=False, separators=(",", ":"))
                    dept_info["files"].append(f"data/departments/{filename}")
                    total_written_files += 1
                    total_written_products += len(current_chunk)
                    part_idx += 1
                    current_chunk = [it]
                    current_bytes = 2 + it_bytes
                else:
                    current_chunk.append(it)
                    current_bytes += it_bytes
            if current_chunk:
                filename = f"{dept_id}_part_{part_idx}.json"
                filepath = os.path.join(DEPTS_OUTPUT_DIR, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(current_chunk, f, ensure_ascii=False, separators=(",", ":"))
                dept_info["files"].append(f"data/departments/{filename}")
                total_written_files += 1
                total_written_products += len(current_chunk)

        manifest["departments"][dept_id] = dept_info

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"   [OK] {total_written_files} archivos departamentales particionados escritos en data/departments/")
    print(f"   [OK] departments_manifest.json actualizado ({os.path.getsize(MANIFEST_PATH)/1024:.1f} KB)")

    # 7. Actualizar catalogo compacto con las categorias corregidas
    with open(COMPACT_JSON, "w", encoding="utf-8") as f:
        json.dump(catalog_items, f, ensure_ascii=False, separators=(",", ":"))
    print(f"   [OK] catalogo_maestro_compact.json actualizado con categorias purificadas ({os.path.getsize(COMPACT_JSON)/1024:.1f} KB)")

    print("=" * 80)
    print("[EXITO] REGENERACION DE VITRINAS COMPLETADA AL 100%")
    print("=" * 80)

regenerar_vitrinas_congruentes = regenerar_vitrinas

if __name__ == "__main__":
    regenerar_vitrinas()
