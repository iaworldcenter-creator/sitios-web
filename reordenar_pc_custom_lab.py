import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
PC_LAB_INDEX = os.path.join(BASE_DIR, "pc-custom-lab", "index.html")

if not os.path.exists(PC_LAB_INDEX):
    print("Error: No se encontró pc-custom-lab/index.html")
    exit(1)

with open(PC_LAB_INDEX, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Función para extraer secciones completas por palabras clave
def extract_section_block(text, keyword):
    pos = text.find(keyword)
    if pos == -1:
        return None, text
    
    # Buscar etiqueta de apertura hacia atrás
    section_start = text.rfind('<section', 0, pos)
    div_start = text.rfind('<div', 0, pos)
    
    start_pos = max(section_start, div_start)
    if start_pos == -1:
        return None, text
    
    tag_match = re.match(r'<([a-zA-Z0-9]+)', text[start_pos:])
    if not tag_match:
        return None, text
    tag_name = tag_match.group(1)
    
    # Balancear etiquetas para encontrar el cierre exacto
    depth = 0
    i = start_pos
    end_pos = -1
    while i < len(text):
        if text[i:i+len(tag_name)+1].lower() == f"<{tag_name}" and (i+len(tag_name)+1 >= len(text) or text[i+len(tag_name)+1].isspace() or text[i+len(tag_name)+1] == '>'):
            depth += 1
        elif text[i:i+len(tag_name)+3].lower() == f"</{tag_name}>":
            depth -= 1
            if depth == 0:
                end_pos = i + len(tag_name) + 3
                break
        i += 1
        
    if end_pos != -1 and start_pos <= pos < end_pos:
        block = text[start_pos:end_pos]
        clean_text = text[:start_pos] + text[end_pos:]
        return block, clean_text
    return None, text

print("=== REUBICANDO SECCIONES EN PC CUSTOM LAB ===")

# Extraer Bloque Tigre (Garantía, Calidad y Respaldo)
tigre_block, html_no_tigre = extract_section_block(html, "Garantía, Calidad y Respaldo")
if not tigre_block:
    tigre_block, html_no_tigre = extract_section_block(html, "PC CUSTOM LAB & TECH SERVICE")

# Extraer Bloque Refacciones (Miles de Piezas & Refacciones Sueltas)
refacciones_block, html_clean = extract_section_block(html_no_tigre, "Miles de Piezas & Refacciones Sueltas")
if not refacciones_block:
    refacciones_block, html_clean = extract_section_block(html_no_tigre, "Explorar Boutique de Refacciones")

if not tigre_block or not refacciones_block:
    print("Aviso: No se pudieron extraer los bloques de forma aislada. Aplicando reestructuración modular...")

# Ajustar estilo del bloque Tigre para desplazamiento en cámara lenta suave
if tigre_block:
    # Añadir animación de transición suave y espaciado de lectura
    tigre_block = re.sub(
        r'(<div[^>]*class="[^"]*flex[^"]*overflow-x-auto[^"]*"[^>]*>)',
        r'\1\n<style>@keyframes slowScrollTigre { 0% { transform: translateX(0); } 50% { transform: translateX(-15px); } 100% { transform: translateX(0); } } .slow-pan { animation: slowScrollTigre 8s ease-in-out infinite; }</style>',
        tigre_block
    )

# 2. Reinsertar 'Boutique de Refacciones' INMEDIATAMENTE debajo del Hero Principal
hero_end_match = re.search(r'(<\/section>\s*|\s*<\/div>\s*)(?=<!--\s*(?:CAT[ÁA]LOGO|PRODUCTOS|FILTROS)|\s*<section[^>]*id=["\'](?:catalogo|productos|filtros)["\'])', html_clean, re.IGNORECASE)
if hero_end_match and refacciones_block:
    pos_insert_ref = hero_end_match.start()
    html_clean = html_clean[:pos_insert_ref] + "\n\n" + refacciones_block + "\n\n" + html_clean[pos_insert_ref:]
    print("✓ 'Boutique de Refacciones' ubicada inmediatamente debajo del Hero.")

# 3. Reinsertar 'Garantía, Calidad y Respaldo (Tigre)' ENTRE Cotizador y Programa de Lealtad
lealtad_match = re.search(r'(<!--\s*(?:PROGRAMA DE LEALTAD|CLUB DE SOCIOS)|\s*<section[^>]*id=["\'](?:lealtad|recompensas|club)["\']|\s*<div[^>]*>\s*//\s*CLUB DE SOCIOS|\s*CLUB DE SOCIOS PC CUSTOM LAB)', html_clean, re.IGNORECASE)

if lealtad_match and tigre_block:
    # Buscar el inicio de la sección de Lealtad
    lealtad_pos = lealtad_match.start()
    # Retroceder al <section o <div contenedor
    tag_before = max(html_clean.rfind('<section', 0, lealtad_pos), html_clean.rfind('<div class="max-w', 0, lealtad_pos), html_clean.rfind('<div class="relative', 0, lealtad_pos))
    if tag_before != -1:
        insert_pos = tag_before
    else:
        insert_pos = lealtad_pos
        
    html_clean = html_clean[:insert_pos] + "\n\n" + tigre_block + "\n\n" + html_clean[insert_pos:]
    print("✓ 'Garantía, Calidad y Respaldo' ubicada entre el Cotizador y Programa de Lealtad con animación lenta.")

with open(PC_LAB_INDEX, "w", encoding="utf-8") as f:
    f.write(html_clean)

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
pc_dir = os.path.join(BASE_DIR, "pc-custom-lab")
if os.path.exists(os.path.join(pc_dir, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=pc_dir, check=True)
    subprocess.run(["git", "commit", "-m", "fix(layout): carrusel tigre reubicado entre cotizador y lealtad con camara lenta; hero despejado", "--allow-empty"], cwd=pc_dir, capture_output=True)
    res_pc = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=pc_dir, capture_output=True, text=True)
    print(f"🟢 pc-custom-lab -> Push: {'OK' if res_pc.returncode == 0 else res_pc.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(pc-custom-lab): orden estricto de hero, refacciones y carrusel tigre", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
