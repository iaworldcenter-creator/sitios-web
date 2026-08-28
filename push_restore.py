import os
import subprocess

BASE_DIR = r"E:\sitios web"
boutiques = ['pc-custom-lab', 'bazar-viamx-nfl.gdl', 'cigarros-bazar', 'dulces-bazar', 'kiosco-digital', 'mi-puesto-bazar', 'ofertas-y-liquidaciones']

for b in boutiques:
    sub_path = os.path.join(BASE_DIR, b)
    lock_file = os.path.join(sub_path, ".git", "index.lock")
    if os.path.exists(lock_file):
        try: os.remove(lock_file)
        except: pass

    print(f"Staging and pushing [{b}]...")
    subprocess.run(["git", "add", "-A"], cwd=sub_path)
    subprocess.run(["git", "commit", "-m", "fix: restauracion a diseno original aprobado con grilla simetrica 5x4 y 200 items"], cwd=sub_path)
    p = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sub_path, capture_output=True, text=True)
    print(f"  -> {b} push code: {p.returncode}")

print("\nStaging and pushing Root Monorepo...")
lock_root = os.path.join(BASE_DIR, ".git", "index.lock")
if os.path.exists(lock_root):
    try: os.remove(lock_root)
    except: pass

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
subprocess.run(["git", "commit", "-m", "fix(ecosistema): restauracion general a diseno original aprobado"], cwd=BASE_DIR)
p_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"  -> Root push code: {p_root.returncode}")
print("=== PUSH FINALIZADO CON ÉXITO ===")
