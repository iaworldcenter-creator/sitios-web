import os
import shutil
import subprocess

BASE_DIR = r"E:\sitios web"
PC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")
SRC_IMG_DIR = os.path.join(PC_DIR, "assets", "temp_ml_images")
ROOT_IMG_DIR = os.path.join(BASE_DIR, "assets", "temp_ml_images")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

os.makedirs(ROOT_IMG_DIR, exist_ok=True)
for fname in os.listdir(SRC_IMG_DIR):
    shutil.copy2(os.path.join(SRC_IMG_DIR, fname), os.path.join(ROOT_IMG_DIR, fname))

# Sincronizar a los 3 respaldos seguros
for b in ["respaldo_seguro_oro", "respaldo_seguro_espejo", "respaldo_desarrollo_activo"]:
    b_assets = os.path.join(BACKUP_DIR, b, "pc-custom-lab", "assets", "temp_ml_images")
    os.makedirs(b_assets, exist_ok=True)
    for fname in os.listdir(SRC_IMG_DIR):
        shutil.copy2(os.path.join(SRC_IMG_DIR, fname), os.path.join(b_assets, fname))
    
    b_data = os.path.join(BACKUP_DIR, b, "pc-custom-lab", "data")
    os.makedirs(b_data, exist_ok=True)
    shutil.copy2(os.path.join(PC_DIR, "data", "Publicar_GITHUB_ASSETS.xlsx"), os.path.join(b_data, "Publicar_GITHUB_ASSETS.xlsx"))

# 1. GIT PUSH PC-CUSTOM-LAB
lock_file = os.path.join(PC_DIR, ".git", "index.lock")
if os.path.exists(lock_file):
    try: os.remove(lock_file)
    except: pass

print("Staging and pushing pc-custom-lab...")
subprocess.run(["git", "add", "-A"], cwd=PC_DIR)
subprocess.run(["git", "commit", "-m", "feat(assets-temp): alojamiento temporal de 15 imagenes en alta resolucion 1000x1000px para validacion Mercado Libre"], cwd=PC_DIR)
p1 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=PC_DIR, capture_output=True, text=True)
print(f" -> pc-custom-lab push code: {p1.returncode}")

# 2. GIT PUSH ROOT MONOREPO
lock_root = os.path.join(BASE_DIR, ".git", "index.lock")
if os.path.exists(lock_root):
    try: os.remove(lock_root)
    except: pass

print("Staging Root Monorepo...")
subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
subprocess.run(["git", "commit", "-m", "feat(assets-temp): publicacion de imagenes HD temporales para Mercado Libre"], cwd=BASE_DIR)
p2 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f" -> root monorepo push code: {p2.returncode}")
print("=== PUSH COMPLETADO ===")
