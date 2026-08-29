import os
import json
import re

BASE_DIR = r"E:\sitios web\pc-custom-lab"
DATA_FILE = os.path.join(BASE_DIR, "data", "catalogo_maestro_ct.json")

print("=" * 80, flush=True)
print("ELIMINACIÓN DEFINITIVA DE SOLICITUDES BLOQUEANTES, REEMPLAZO DE TAILWIND CDN POR CSS COMPILADO")
print("Y DESACOPLAMIENTO TOTAL DEL HILO PRINCIPAL PARA CELULARES")
print("=" * 80, flush=True)

# 1. Cargar catálogo y generar payload inicial de solo 40 productos clave (~15 KB)
with open(DATA_FILE, "r", encoding="utf-8") as f:
    full_catalog = json.load(f)

initial_items = full_catalog[:40]

with open(os.path.join(BASE_DIR, "js", "ct-catalog-data.js"), "w", encoding="utf-8") as f:
    f.write(f"window.CT_CATALOG_DATA_INITIAL = {json.dumps(initial_items, ensure_ascii=False)};\n")
    f.write("window.CT_CATALOG_DATA = window.CT_CATALOG_DATA_INITIAL;\n")
    f.write("window.PC_COMBOS_DATA = [];\n")

print(f"✅ Payload inicial ultraligero: {len(initial_items)} productos ({os.path.getsize(os.path.join(BASE_DIR, 'js', 'ct-catalog-data.js')) // 1024} KB).", flush=True)

# 2. Agregar estilos específicos de PC Custom Lab a tailwind-built.css
custom_styles = """
/* === PC CUSTOM LAB ESTILOS CRÍTICOS INLINE === */
.no-scrollbar::-webkit-scrollbar { display: none !important; }
.no-scrollbar { -ms-overflow-style: none !important; scrollbar-width: none !important; }
.neon-glow-pc {
    border: 1px solid rgba(6,182,212,0.9) !important;
    box-shadow: 0 0 16px rgba(6,182,212,0.6), inset 0 0 10px rgba(6,182,212,0.3) !important;
}
@font-face {
    font-family: 'Font Awesome 6 Free';
    font-display: swap;
}
@font-face {
    font-family: 'Font Awesome 6 Brands';
    font-display: swap;
}
"""

css_path = os.path.join(BASE_DIR, "assets", "css", "tailwind-built.css")
with open(css_path, "r", encoding="utf-8") as f:
    existing_css = f.read()

if '.neon-glow-pc' not in existing_css:
    with open(css_path, "a", encoding="utf-8") as f:
        f.write(custom_styles)

# 3. Reescribir el <head> de index.html con CERO scripts bloqueantes
with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
    html = f.read()

NEW_HEAD = """<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PC Custom Lab | Hardware Mayorista & Ensamble de Cómputo</title>
    <meta name="description" content="Catálogo oficial de hardware mayorista PC Custom Lab, procesadores Intel/AMD, placas ASUS, tarjetas gráficas RTX y configuraciones armadas.">
    
    <!-- Preconexión DNS y CDN -->
    <link rel="preconnect" href="https://static.ctonline.mx" crossorigin>
    <link rel="dns-prefetch" href="https://static.ctonline.mx">

    <!-- CSS Precompilado Local (Cero bloqueos de renderizado de cdn.tailwindcss.com) -->
    <link rel="stylesheet" href="assets/css/tailwind-built.css">
    <link rel="stylesheet" href="assets/css/fontawesome-all.min.css" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="assets/css/fontawesome-all.min.css"></noscript>

    <style>
        .no-scrollbar::-webkit-scrollbar { display: none !important; }
        .no-scrollbar { -ms-overflow-style: none !important; scrollbar-width: none !important; }
        .neon-glow-pc {
            border: 1px solid rgba(6,182,212,0.9) !important;
            box-shadow: 0 0 16px rgba(6,182,212,0.6), inset 0 0 10px rgba(6,182,212,0.3) !important;
        }
    </style>
</head>"""

html = re.sub(r'<head>[\s\S]*?</head>', NEW_HEAD, html)

CACHE_VER = "20260828_1940"
html = re.sub(r'src="js/ct-catalog-data\.js.*?"', f'src="js/ct-catalog-data.js?v={CACHE_VER}"', html)
html = re.sub(r'src="js/ct-exact-catalog-engine\.js.*?"', f'src="js/ct-exact-catalog-engine.js?v={CACHE_VER}"', html)

with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

# 4. Espejo a OneDrive C:
BASE_DIR_C = r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web\pc-custom-lab"
for root, dirs, files in os.walk(BASE_DIR):
    if '.git' in root or 'node_modules' in root: continue
    for file in files:
        src = os.path.join(root, file)
        rel = os.path.relpath(src, r"E:\sitios web")
        dst = os.path.join(r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web", rel)
        if os.path.exists(os.path.dirname(dst)):
            try:
                with open(src, "rb") as f_in, open(dst, "wb") as f_out:
                    f_out.write(f_in.read())
            except: pass

print("✅ Optimización y purga de recursos bloqueantes completada con éxito!", flush=True)
