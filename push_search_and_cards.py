import os
import subprocess

BASE_DIR = r"E:\sitios web"
PC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")

# 1. GIT PUSH PC-CUSTOM-LAB
lock_file = os.path.join(PC_DIR, ".git", "index.lock")
if os.path.exists(lock_file):
    try: os.remove(lock_file)
    except: pass

print("Staging and pushing pc-custom-lab...")
subprocess.run(["git", "add", "-A"], cwd=PC_DIR)
subprocess.run(["git", "commit", "-m", "fix(search-ui): motor semantico ponderado para reguladores y combos teclado-raton, 3 botones por tarjeta y politicas de envio $2000 MXN"], cwd=PC_DIR)
p1 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=PC_DIR, capture_output=True, text=True)
print(f" -> pc-custom-lab push code: {p1.returncode}")

# 2. GIT PUSH MONOREPO ROOT
lock_root = os.path.join(BASE_DIR, ".git", "index.lock")
if os.path.exists(lock_root):
    try: os.remove(lock_root)
    except: pass

print("Staging Root Monorepo...")
subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
subprocess.run(["git", "commit", "-m", "fix(ecosistema): sincronizacion de motor semantico, tarjetas con 3 botones y triple respaldo"], cwd=BASE_DIR)
p2 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f" -> root monorepo push code: {p2.returncode}")
print("=== PUSH FINALIZADO CON ÉXITO ===")
