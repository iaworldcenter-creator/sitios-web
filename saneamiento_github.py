import os
import subprocess

BASE_DIR = r"E:\sitios web"
PC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")

print("=" * 80)
print("SANEAMIENTO Y LIMPIEZA EN REPOSITORIOS GITHUB")
print("=" * 80)

# 1. Limpiar pc-custom-lab
lock_pc = os.path.join(PC_DIR, ".git", "index.lock")
if os.path.exists(lock_pc):
    try: os.remove(lock_pc)
    except: pass

print("Staging and cleaning pc-custom-lab...")
subprocess.run(["git", "add", "-A"], cwd=PC_DIR)
status_pc = subprocess.run(["git", "status", "--porcelain"], cwd=PC_DIR, capture_output=True, text=True).stdout
if status_pc:
    subprocess.run(["git", "commit", "-m", "chore(cleanup): purga de archivos temporales, imagenes descartadas y optimizacion de repositorio"], cwd=PC_DIR)
    p1 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=PC_DIR, capture_output=True, text=True)
    print(f" -> pc-custom-lab push code: {p1.returncode}")
else:
    print(" -> pc-custom-lab ya está limpio.")

# 2. Limpiar monorepo raíz sitios-web
lock_root = os.path.join(BASE_DIR, ".git", "index.lock")
if os.path.exists(lock_root):
    try: os.remove(lock_root)
    except: pass

print("Staging and cleaning root monorepo...")
subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
status_root = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR, capture_output=True, text=True).stdout
if status_root:
    subprocess.run(["git", "commit", "-m", "chore(cleanup): purga y optimizacion integral del ecosistema"], cwd=BASE_DIR)
    p2 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
    print(f" -> root monorepo push code: {p2.returncode}")
else:
    print(" -> root monorepo ya está limpio.")

print("=== SANEAMIENTO GITHUB COMPLETADO ===")
