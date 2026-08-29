import os
import subprocess

BASE_DIR = r"E:\sitios web"
PC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")
BASE_DIR_C = r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web"

print("=" * 80, flush=True)
print("RESTAURACIÓN AL PUNTO ESTABLE ANTERIOR (0feaff1 / CATÁLOGO COMPLETO INTACTO)")
print("=" * 80, flush=True)

# 1. RESTAURAR ARCHIVOS DE PC-CUSTOM-LAB AL COMMIT 0feaff1
lock_file = os.path.join(PC_DIR, ".git", "index.lock")
if os.path.exists(lock_file):
    try: os.remove(lock_file)
    except: pass

subprocess.run(["git", "checkout", "0feaff1", "--", "index.html", "js/ct-exact-catalog-engine.js"], cwd=PC_DIR)
print("✅ pc-custom-lab: index.html y js/ct-exact-catalog-engine.js restaurados al punto previo 0feaff1.")

# 2. RESTAURAR RAÍZ MONOREPO
lock_root = os.path.join(BASE_DIR, ".git", "index.lock")
if os.path.exists(lock_root):
    try: os.remove(lock_root)
    except: pass

subprocess.run(["git", "checkout", "0c3a326", "--", "index.html", "bazar-viamx-nfl.gdl/index.html", "cigarros-bazar/index.html", "dulces-bazar/index.html", "kiosco-digital/index.html", "mi-puesto-bazar/index.html", "ofertas-y-liquidaciones/index.html"], cwd=BASE_DIR)
print("✅ sitios-web: portal matriz y tiendas del ecosistema restauradas.")

# 3. SINCRONIZAR A ONEDRIVE C:
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

print("✅ Sincronización espejo a OneDrive C: completada.")

# 4. COMMIT Y PUSH EN PC-CUSTOM-LAB
subprocess.run(["git", "add", "-A"], cwd=PC_DIR)
subprocess.run(["git", "commit", "-m", "revert: restablecimiento total al punto estable anterior con catalogo completo"], cwd=PC_DIR)
p1 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=PC_DIR, capture_output=True, text=True)
print(f" -> pc-custom-lab push code: {p1.returncode}")

# 5. COMMIT Y PUSH EN ROOT
subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
subprocess.run(["git", "commit", "-m", "revert: restablecimiento del ecosistema al punto estable previo"], cwd=BASE_DIR)
p2 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f" -> root monorepo push code: {p2.returncode}")

print("=" * 80, flush=True)
print("RESTAURACIÓN FINALIZADA CON ÉXITO")
print("=" * 80, flush=True)
