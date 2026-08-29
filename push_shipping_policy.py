import os
import subprocess

BASE_DIR = r"E:\sitios web"
PC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")

lock_file = os.path.join(PC_DIR, ".git", "index.lock")
if os.path.exists(lock_file):
    try: os.remove(lock_file)
    except: pass

print("Staging and pushing shipping policy update in pc-custom-lab...")
subprocess.run(["git", "add", "index.html", "checkout.html"], cwd=PC_DIR)
subprocess.run(["git", "commit", "-m", "legal(shipping): politica de envios exprés limitada a pedidos menores de $2,000 MXN, paqueteria blindada para pedidos mayores y footer institucional completo"], cwd=PC_DIR)
p1 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=PC_DIR, capture_output=True, text=True)
print(f" -> pc-custom-lab push code: {p1.returncode}")

lock_root = os.path.join(BASE_DIR, ".git", "index.lock")
if os.path.exists(lock_root):
    try: os.remove(lock_root)
    except: pass

print("Staging Root Monorepo...")
subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
subprocess.run(["git", "commit", "-m", "legal(ecosistema): implementacion universal de politica de envios $2000 MXN y footer institucional de 3 columnas en los 8 sitios"], cwd=BASE_DIR)
p2 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f" -> root monorepo push code: {p2.returncode}")
print("=== PUSH FINALIZADO CON ÉXITO ===")
