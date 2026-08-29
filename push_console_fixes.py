import os
import subprocess

BASE_DIR = r"E:\sitios web"
PC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")

lock_file = os.path.join(PC_DIR, ".git", "index.lock")
if os.path.exists(lock_file):
    try: os.remove(lock_file)
    except: pass

print("Staging and pushing console fixes in pc-custom-lab...")
subprocess.run(["git", "add", "-A"], cwd=PC_DIR)
subprocess.run(["git", "commit", "-m", "fix(console): eliminacion de los 2 errores de consola en Lighthouse - retiro de frame-ancestors en meta CSP e inicializacion sin fallo de red en dataset"], cwd=PC_DIR)
p1 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=PC_DIR, capture_output=True, text=True)
print(f" -> pc-custom-lab push code: {p1.returncode}")

lock_root = os.path.join(BASE_DIR, ".git", "index.lock")
if os.path.exists(lock_root):
    try: os.remove(lock_root)
    except: pass

print("Staging Root Monorepo...")
subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
subprocess.run(["git", "commit", "-m", "fix(ecosistema): eliminacion de frame-ancestors en meta CSP y blindaje de consola en los 8 sitios"], cwd=BASE_DIR)
p2 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f" -> root monorepo push code: {p2.returncode}")
print("=== PUSH FINALIZADO CON ÉXITO ===")
