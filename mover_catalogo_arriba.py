import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
PC_INDEX_PATH = os.path.join(BASE_DIR, "pc-custom-lab", "index.html")

if not os.path.exists(PC_INDEX_PATH):
    print(f"Error: No se encontró {PC_INDEX_PATH}")
    exit(1)

with open(PC_INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Eliminar cualquier script JS que altere el orden dinámico en el navegador
content = re.sub(r'\(function\s*ordenarFlujoComercial[\s\S]*?\}\)\(\);', '', content)
content = re.sub(r'function\s+ordenarFlujoComercial[\s\S]*?\}', '', content)

# 2. Función extractora robusta de secciones por palabras clave
def extract_block(text, keyword, stop_keywords):
    pos = text.find(keyword)
    if pos == -1:
        return "", text
    
    # Buscar etiqueta de apertura hacia atrás (<section o <div)
    sec_start = text.rfind('<section', 0, pos)
    div_start = text.rfind('<div class="py-', 0, pos)
    if div_start == -1:
        div_start = text.rfind('<div class="max-w', 0, pos)
    
    start_pos = max(sec_start, div_start)
    if start_pos == -1:
        start_pos = pos

    # Buscar el inicio de la siguiente sección
    end_pos = len(text)
    for sk in stop_keywords:
        p_stop = text.find(sk, pos + len(keyword))
        if p_stop != -1 and p_stop < end_pos:
            # Retroceder al <section o <div de esa siguiente sección
            s_tag = text.rfind('<section', 0, p_stop)
            d_tag = text.rfind('<div class="py-', 0, p_stop)
            if d_tag == -1:
                d_tag = text.rfind('<div class="max-w', 0, p_stop)
            tag_limit = max(s_tag, d_tag)
            if tag_limit != -1 and tag_limit > pos:
                end_pos = tag_limit
            else:
                end_pos = p_stop

    block = text[start_pos:end_pos].strip()
    return block

print("=== REUBICANDO EL CATÁLOGO DIRECTAMENTE DEBAJO DEL HERO ===")

# A. Extraer Cabecera + Hero Slider
hero_end_match = re.search(r'(<\/section>\s*)(?=<!--\s*(?:CAT[ÁA]LOGO|PRODUCTOS|TIENDA|CONFIGURADOR|NIVELES|GARANT[ÍI]A)|\s*<section|\s*<main|\s*//\s*TIENDA)', content, re.IGNORECASE)
if hero_end_match:
    idx_hero = hero_end_match.end()
    header_hero = content[:idx_hero].strip()
    rest_of_page = content[idx_hero:]
else:
    # Alternativa por etiqueta de slider
    pos_hero = content.find("No Solo Vendemos, Damos Solución Total")
    if pos_hero != -1:
        sec_end = content.find("</section>", pos_hero)
        header_hero = content[:sec_end+10].strip()
        rest_of_page = content[sec_end+10:]
    else:
        header_hero = content[:1500].strip()
        rest_of_page = content[1500:]

# B. Extraer Bloque Catálogo (Filtros + Grid 20 productos + Paginación)
catalogo_block = extract_block(
    content,
    "Navegación y Filtros",
    ["Nuestros Niveles de Ensamble", "LABORATORIO DE ENSAMBLAJE", "Configura tu Equipo Paso a Paso", "CONFIGURADOR MATRIZ", "Garantía, Calidad y Respaldo", "CLUB DE SOCIOS", "<footer"]
)
if not catalogo_block:
    catalogo_block = extract_block(
        content,
        "Catálogo de Componentes Esenciales",
        ["Nuestros Niveles de Ensamble", "LABORATORIO DE ENSAMBLAJE", "Configura tu Equipo Paso a Paso", "CONFIGURADOR MATRIZ", "Garantía, Calidad y Respaldo", "CLUB DE SOCIOS", "<footer"]
    )

# C. Extraer Bloque Niveles de Ensamble
niveles_block = extract_block(
    content,
    "Nuestros Niveles de Ensamble",
    ["Configura tu Equipo Paso a Paso", "CONFIGURADOR MATRIZ", "Garantía, Calidad y Respaldo", "CLUB DE SOCIOS", "<footer"]
)

# D. Extraer Bloque Configurador / Cotizador
cotizador_block = extract_block(
    content,
    "Configura tu Equipo Paso a Paso",
    ["Garantía, Calidad y Respaldo", "CLUB DE SOCIOS", "<footer"]
)

# E. Extraer Bloque Carrusel Tigres
tigre_block = extract_block(
    content,
    "Garantía, Calidad y Respaldo",
    ["CLUB DE SOCIOS", "Programa de Lealtad", "<footer"]
)

# F. Extraer Bloque Programa de Lealtad
lealtad_block = extract_block(
    content,
    "CLUB DE SOCIOS",
    ["<footer", "<!-- FOOTER"]
)
if not lealtad_block:
    lealtad_block = extract_block(
        content,
        "Programa de Lealtad & Recompensas",
        ["<footer", "<!-- FOOTER"]
    )

# G. Extraer Footer Universal y Scripts
footer_pos = content.rfind("<footer")
scripts_pos = content.find("<script", footer_pos) if footer_pos != -1 else content.rfind("<script")

footer_block = content[footer_pos:scripts_pos].strip() if footer_pos != -1 else ""
scripts_block = content[scripts_pos:].strip() if scripts_pos != -1 else "</body></html>"

# 3. Validar y ensamblar en el orden físico estricto
secciones = [
    ("Header & Hero", header_hero),
    ("Catálogo de Productos", catalogo_block),
    ("Niveles de Ensamble", niveles_block),
    ("Configurador de PC", cotizador_block),
    ("Carrusel de los Tigres", tigre_block),
    ("Programa de Lealtad", lealtad_block),
    ("Footer Universal", footer_block)
]

print("\nVerificando orden de ensamblaje:")
for name, block in secciones:
    print(f"  ✓ {name.ljust(26)} -> {'Detectado (' + str(len(block)) + ' chars)' if block else 'No encontrado'}")

# Ensamblaje físico del documento
FINAL_HTML = f"""{header_hero}

<!-- SECCIÓN 2: CATÁLOGO DE COMPONENTES ESENCIALES (DIRECTO DEBAJO DEL HERO) -->
{catalogo_block}

<!-- SECCIÓN 3: NIVELES DE ENSAMBLE -->
{niveles_block}

<!-- SECCIÓN 4: CONFIGURADOR MATRIZ -->
{cotizador_block}

<!-- SECCIÓN 5: CARRUSEL CONTINUO DEL TIGRE -->
{tigre_block}

<!-- SECCIÓN 6: PROGRAMA DE LEALTAD -->
{lealtad_block}

<!-- SECCIÓN 7: FOOTER UNIVERSAL -->
{footer_block}

{scripts_block}
"""

with open(PC_INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(FINAL_HTML)

print("\n✓ pc-custom-lab/index.html reensamblado con el Catálogo en la parte superior.")

# 4. Despliegue a GitHub Pages
print("\n=== DESPLEGANDO A GITHUB PAGES ===")
pc_dir = os.path.join(BASE_DIR, "pc-custom-lab")
subprocess.run(["git", "add", "-A"], cwd=pc_dir, check=True)
subprocess.run(["git", "commit", "-m", "fix(layout): catalogo de componentes posicionado inmediatamente debajo del hero", "--allow-empty"], cwd=pc_dir, capture_output=True)
res_pc = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=pc_dir, capture_output=True, text=True)
print(f"🟢 pc-custom-lab -> Push: {'OK' if res_pc.returncode == 0 else res_pc.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(pc-custom-lab): catalogo y filtros ubicados arriba despues de bienvenida", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
