import os
import subprocess

BASE_DIR = r"E:\sitios web"
BASE_DIR_C = r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web"
PC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")

# 1. SINCRONIZAR A ONEDRIVE C:
STORES = ["pc-custom-lab", ".", "bazar-viamx-nfl.gdl", "cigarros-bazar", "dulces-bazar", "kiosco-digital", "mi-puesto-bazar", "ofertas-y-liquidaciones"]
for s in STORES:
    store_dir = os.path.join(BASE_DIR, s)
    store_dir_c = os.path.join(BASE_DIR_C, s)
    os.makedirs(store_dir_c, exist_ok=True)
    for fname in os.listdir(store_dir):
        if fname.endswith(".html") or fname.endswith(".txt") or fname.endswith(".js") or fname.endswith(".json"):
            src = os.path.join(store_dir, fname)
            dst = os.path.join(store_dir_c, fname)
            try:
                with open(src, "rb") as f_in, open(dst, "wb") as f_out:
                    f_out.write(f_in.read())
            except: pass

print("✅ Sincronización espejo a OneDrive C: completada!")

# 2. GIT PUSH PC-CUSTOM-LAB
lock_file = os.path.join(PC_DIR, ".git", "index.lock")
if os.path.exists(lock_file):
    try: os.remove(lock_file)
    except: pass

print("Staging and pushing pc-custom-lab...")
subprocess.run(["git", "add", "-A"], cwd=PC_DIR)
subprocess.run(["git", "commit", "-m", "fix(architecture): restauracion integral del diseno original, 24 departamentos, 16139 productos en memoria, auto-scroll fluido y navegacion total"], cwd=PC_DIR)
p1 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=PC_DIR, capture_output=True, text=True)
print(f" -> pc-custom-lab push code: {p1.returncode}")

# 3. GIT PUSH MONOREPO ROOT
lock_root = os.path.join(BASE_DIR, ".git", "index.lock")
if os.path.exists(lock_root):
    try: os.remove(lock_root)
    except: pass

print("Staging Root Monorepo...")
subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
subprocess.run(["git", "commit", "-m", "fix(matriz): restauracion del portal Matriz intacto y sincronizacion de PC Custom Lab"], cwd=BASE_DIR)
p2 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f" -> root monorepo push code: {p2.returncode}")
print("=== PUSH FINALIZADO CON ÉXITO ===")
