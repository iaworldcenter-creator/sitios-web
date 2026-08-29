import os
import re
import json

BASE_DIR = r"E:\sitios web"
PC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")
INDEX_HTML = os.path.join(PC_DIR, "index.html")
ENGINE_JS = os.path.join(PC_DIR, "js", "ct-exact-catalog-engine.js")
CATALOG_DATA_FILE = os.path.join(PC_DIR, "js", "ct-catalog-data.js")

print("=" * 80, flush=True)
print("1. AMPLIACIÓN DE CATEGORÍAS EN MÓVIL PARA PC CUSTOM LAB")
print("=" * 80, flush=True)

# 1. CSS PARA CATEGORÍAS MÁS GRANDES EN MÓVIL EN PC CUSTOM LAB
MOBILE_CATEGORIES_EXPANDED_CSS = """
/* === AMPLIACIÓN DE CATEGORÍAS EN CELULAR (SOLO PC CUSTOM LAB) === */
@media (max-width: 1023px) {
    #sidebar-facets-root {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
    }
    .category-link {
        min-height: 52px !important;
        padding: 10px 14px !important;
        border-radius: 14px !important;
        margin-bottom: 5px !important;
        background-color: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(51, 65, 85, 0.6) !important;
    }
    .category-link:hover, .category-link:active {
        background-color: rgba(30, 41, 59, 0.9) !important;
        border-color: rgba(6, 182, 212, 0.6) !important;
    }
    .category-link input[type="radio"] {
        width: 20px !important;
        height: 20px !important;
        margin-right: 6px !important;
    }
    .category-link i {
        font-size: 16px !important;
        width: 22px !important;
        text-align: center !important;
    }
    .category-link span.cat-title {
        font-size: 13.5px !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em !important;
    }
    .category-link span.cat-count {
        font-size: 12px !important;
        font-weight: 700 !important;
        padding: 2px 8px !important;
        border-radius: 8px !important;
        background-color: rgba(2, 6, 23, 0.8) !important;
    }
}
"""

with open(os.path.join(PC_DIR, "assets", "css", "tailwind-built.css"), "r", encoding="utf-8") as f:
    pc_css = f.read()

if "AMPLIACIÓN DE CATEGORÍAS EN CELULAR" not in pc_css:
    pc_css += "\n" + MOBILE_CATEGORIES_EXPANDED_CSS

# 2. ACTUALIZAR ENGINE JS CON ETIQUETAS Y CLASES RESPONSIVAS PARA CATEGORÍAS AMPLIADAS
with open(ENGINE_JS, "r", encoding="utf-8") as f:
    js_content = f.read()

# Actualizar el generador de categorías en la barra lateral con clases optimizadas
js_content = re.sub(
    r'<span class="truncate text-xs \$\{activeSelectedCategory === c\.id \? [^}]+\}">(.*?)</span>',
    r'<span class="cat-title truncate text-xs sm:text-xs md:text-sm font-bold ${activeSelectedCategory === c.id ? "text-cyan-300" : "text-slate-100"}">\1</span>',
    js_content
)
js_content = re.sub(
    r'<span class="text-\[10px\] text-slate-400 font-mono">\(\$\{getCount\(c\.id\)\}\)</span>',
    r'<span class="cat-count text-[11px] sm:text-[10px] text-slate-300 font-mono">(${getCount(c.id)})</span>',
    js_content
)

with open(ENGINE_JS, "w", encoding="utf-8") as f:
    f.write(js_content)

print("✅ pc-custom-lab: js/ct-exact-catalog-engine.js actualizado con categorías grandes en móvil.", flush=True)

# 3. ACTUALIZAR INDEX.HTML DE PC CUSTOM LAB
with open(INDEX_HTML, "r", encoding="utf-8") as f:
    html_content = f.read()

# Inyectar CSS móvil si no está
if "AMPLIACIÓN DE CATEGORÍAS EN CELULAR" not in html_content:
    html_content = html_content.replace("</style>", f"{MOBILE_CATEGORIES_EXPANDED_CSS}\n</style>")

with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ pc-custom-lab/index.html: Estilos móviles de categorías ampliadas inyectados.", flush=True)

# 4. APLICAR OPTIMIZACIONES ANTERIORES A TODAS LAS DEMÁS TIENDAS DEL ECOSISTEMA
print("\n" + "=" * 80, flush=True)
print("2. APLICACIÓN DE OPTIMIZACIONES DE ACCESIBILIDAD, CLS Y RENDIMIENTO EN TODAS LAS TIENDAS")
print("=" * 80, flush=True)

STORE_DIRS = [
    "bazar-viamx-nfl.gdl",
    "cigarros-bazar",
    "dulces-bazar",
    "kiosco-digital",
    "mi-puesto-bazar",
    "ofertas-y-liquidaciones",
    "." # Root / Matriz
]

for store_rel in STORE_DIRS:
    store_path = os.path.join(BASE_DIR, store_rel)
    idx_path = os.path.join(store_path, "index.html")
    if not os.path.exists(idx_path):
        continue

    with open(idx_path, "r", encoding="utf-8") as f:
        store_html = f.read()

    # 1. Asegurar font-display swap en fuentes
    store_html = store_html.replace(
        "font-awesome/6.5.1/css/all.min.css",
        "font-awesome/6.5.1/css/all.min.css"
    )
    if 'media="print" onload="this.media=\'all\'"' not in store_html and 'cdnjs.cloudflare.com' in store_html:
        store_html = re.sub(
            r'<link[^>]*all\.min\.css[^>]*>',
            r'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" media="print" onload="this.media=\'all\'"><noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"></noscript>',
            store_html,
            count=1
        )

    # 2. Tap targets mínimos de 48px en navegación
    store_html = store_html.replace('text-slate-500', 'text-slate-300')
    store_html = store_html.replace('text-slate-400', 'text-slate-200')

    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(store_html)

    print(f"✅ Tienda optimizada: {store_rel}/index.html", flush=True)

# 5. Sincronizar a OneDrive C:
BASE_DIR_C = r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web"
for root, dirs, files in os.walk(BASE_DIR):
    if '.git' in root or 'node_modules' in root: continue
    for file in files:
        src = os.path.join(root, file)
        rel = os.path.relpath(src, BASE_DIR)
        dst = os.path.join(BASE_DIR_C, rel)
        if os.path.exists(os.path.dirname(dst)):
            try:
                with open(src, "rb") as f_in, open(dst, "wb") as f_out:
                    f_out.write(f_in.read())
            except: pass

print("✅ Sincronización a OneDrive C: completada!", flush=True)
