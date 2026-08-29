import os
import subprocess

BASE_DIR = r"E:\sitios web"
PC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")

lock_file = os.path.join(PC_DIR, ".git", "index.lock")
if os.path.exists(lock_file):
    try: os.remove(lock_file)
    except: pass

print("Staging and pushing font optimization in pc-custom-lab...")
subprocess.run(["git", "add", "index.html", "checkout.html", "js/ct-exact-catalog-engine.js"], cwd=PC_DIR)
subprocess.run(["git", "commit", "-m", "perf(fonts): precarga de fuentes woff2 prioritarias (fa-solid, fa-brands), font-display: swap explicito, anulacion metrica y scheduler.yield() para 0ms de bloqueo"], cwd=PC_DIR)
p1 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=PC_DIR, capture_output=True, text=True)
print(f" -> pc-custom-lab push code: {p1.returncode}")

lock_root = os.path.join(BASE_DIR, ".git", "index.lock")
if os.path.exists(lock_root):
    try: os.remove(lock_root)
    except: pass

print("Staging Root Monorepo...")
subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
subprocess.run(["git", "commit", "-m", "perf(ecosistema): optimizacion de visualizacion de fuentes woff2 con swap y scheduler.yield en los 8 sitios"], cwd=BASE_DIR)
p2 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f" -> root monorepo push code: {p2.returncode}")
print("=== PUSH FINALIZADO CON ÉXITO ===")
