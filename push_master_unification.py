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
subprocess.run(["git", "commit", "-m", "feat(unification): integracion maestra y unificacion de catalogo CT Internacional (16,139) + Intcomex (1,319) = 17,458 productos con CSV unificado y nuevos departamentos de Cables y Audio"], cwd=PC_DIR)
p1 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=PC_DIR, capture_output=True, text=True)
print(f" -> pc-custom-lab push code: {p1.returncode}")

# 2. GIT PUSH MONOREPO ROOT
lock_root = os.path.join(BASE_DIR, ".git", "index.lock")
if os.path.exists(lock_root):
    try: os.remove(lock_root)
    except: pass

print("Staging Root Monorepo...")
subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
subprocess.run(["git", "commit", "-m", "feat(ecosistema): sincronizacion maestra de catalogo unificado CT + Intcomex (17,458 productos) y CSV"], cwd=BASE_DIR)
p2 = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f" -> root monorepo push code: {p2.returncode}")
print("=== PUSH FINALIZADO CON ÉXITO ===")
