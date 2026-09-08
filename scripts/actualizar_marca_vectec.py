#!/usr/bin/env python3
"""
actualizar_marca_vectec.py
Actualiza todos los títulos, textos de interfaz, encabezados, metadatos
y referencias visuales de 'VECTEC' y 'Vectec' para reflejar
exclusivamente la marca oficial VECTEC.
"""

import os
import glob
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TARGET_PATTERNS = [
    os.path.join(BASE_DIR, "pc-custom-lab", "*.html"),
    os.path.join(BASE_DIR, "index.html"),
    os.path.join(BASE_DIR, "app.html"),
    os.path.join(BASE_DIR, "ofertas-y-liquidaciones", "*.html"),
    os.path.join(BASE_DIR, "bazar-viamx-nfl.gdl", "*.html"),
    os.path.join(BASE_DIR, "mi-puesto-bazar", "*.html")
]

files_to_process = []
for pattern in TARGET_PATTERNS:
    files_to_process.extend(glob.glob(pattern))

print(f"[+] Archivos encontrados para actualización de marca: {len(files_to_process)}")

REPLACEMENTS = [
    ("VECTEC", "VECTEC"),
    ("VECTEC", "VECTEC"),
    ("Vectec | Vector Tecnológico", "VECTEC | Vector Tecnológico"),
    ("Vectec · Vector Tecnológico", "VECTEC · Vector Tecnológico"),
    ("Vectec", "VECTEC"),
    ("VECTEC", "VECTEC"),
    ("vectec.oficial", "vectec.oficial"),
    ("pc_custom_lab", "vectec_gdl"),
    ("VECTEC", "VECTEC")
]

# Excepciones que no deben tocar rutas locales de archivos como VECTEC/ o vectec/ en URLs si rompen recursos
def replace_brand_safe(content):
    modified = content
    # Reemplazar títulos y metas
    modified = re.sub(r'<title>(.*?)(VECTEC|Vectec|VECTEC)(.*?)</title>', r'<title>\1VECTEC\3</title>', modified, flags=re.IGNORECASE)
    
    # Reemplazos textuales
    for old, new in REPLACEMENTS:
        # No reemplazar si es parte de una ruta de carpeta local tipo href="VECTEC/" o href="../VECTEC/"
        modified = re.sub(rf'(?<!/)(?<!\\)\b{re.escape(old)}\b(?!\.html)(?!\.css)(?!\.js)(?!\.webp)(?!\.png)', new, modified)
    
    return modified

updated_count = 0
for file_path in files_to_process:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        original = f.read()

    modified = replace_brand_safe(original)
    if modified != original:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(modified)
        updated_count += 1
        print(f"[OK] Actualizada marca a VECTEC en: {os.path.relpath(file_path, BASE_DIR)}")

print(f"\n[OK] Se actualizaron {updated_count} archivos con la marca oficial VECTEC.")
