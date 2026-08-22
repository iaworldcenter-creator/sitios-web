import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
PC_LAB_INDEX = os.path.join(BASE_DIR, "pc-custom-lab", "index.html")

def get_tag_bounds(html, keyword, tags=["section", "div"]):
    kw_pos = html.find(keyword)
    if kw_pos == -1:
        return None
    
    for tag_name in tags:
        open_tag_regex = re.compile(rf'<{tag_name}[\s>]', re.IGNORECASE)
        matches = [m for m in open_tag_regex.finditer(html[:kw_pos])]
        if not matches:
            continue
            
        for m in reversed(matches):
            start_idx = m.start()
            depth = 0
            i = start_idx
            found = False
            while i < len(html):
                if html[i:i+len(tag_name)+1].lower() == f"<{tag_name}" and (i+len(tag_name)+1 >= len(html) or html[i+len(tag_name)+1].isspace() or html[i+len(tag_name)+1] == '>'):
                    depth += 1
                elif html[i:i+len(tag_name)+3].lower() == f"</{tag_name}>":
                    depth -= 1
                    if depth == 0:
                        end_idx = i + len(tag_name) + 3
                        if start_idx <= kw_pos < end_idx:
                            return (start_idx, end_idx, html[start_idx:end_idx])
                        break
                i += 1
    return None

if not os.path.exists(PC_LAB_INDEX):
    print("Error: No se encontró pc-custom-lab/index.html")
    exit(1)

with open(PC_LAB_INDEX, "r", encoding="utf-8") as f:
    html = f.read()

# Identificar bloques de Refacciones y Mascota Tigre
block_refacciones = get_tag_bounds(html, "Miles de Piezas & Refacciones")
if not block_refacciones:
    block_refacciones = get_tag_bounds(html, "Explorar Boutique de Refacciones")

block_tigre = get_tag_bounds(html, "Garantía, Calidad y Respaldo")
if not block_tigre:
    block_tigre = get_tag_bounds(html, "Conoce a nuestra mascota")

if not block_refacciones or not block_tigre:
    print("Error: No se pudo localizar uno de los dos bloques de contenido.")
    print(f"Refacciones: {'Encontrado' if block_refacciones else 'No encontrado'}")
    print(f"Tigre: {'Encontrado' if block_tigre else 'No encontrado'}")
    exit(1)

start_ref, end_ref, content_ref = block_refacciones
start_tigre, end_tigre, content_tigre = block_tigre

# Comprobar si Refacciones está arriba del Tigre para invertirlos
if start_ref < start_tigre:
    print("Invirtiendo posiciones: Colocando Carrusel del Tigre arriba y Boutique de Refacciones abajo...")
    new_html = html[:start_ref] + content_tigre + html[end_ref:start_tigre] + content_ref + html[end_tigre:]
    
    with open(PC_LAB_INDEX, "w", encoding="utf-8") as f:
        f.write(new_html)
    print("✓ Posiciones restauradas con éxito en pc-custom-lab/index.html.")
else:
    print("El carrusel del Tigre ya se encuentra arriba de la sección de refacciones.")

# 2. Despliegue Git
print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
pc_dir = os.path.join(BASE_DIR, "pc-custom-lab")
if os.path.exists(os.path.join(pc_dir, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=pc_dir, check=True)
    subprocess.run(["git", "commit", "-m", "fix(layout): restaurar posicion original de carrusel tigre y boutique refacciones", "--allow-empty"], cwd=pc_dir, capture_output=True)
    res_pc = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=pc_dir, capture_output=True, text=True)
    print(f"🟢 pc-custom-lab -> Push: {'OK' if res_pc.returncode == 0 else res_pc.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(pc-custom-lab): revertir orden de hero carrusel tigre y refacciones", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
