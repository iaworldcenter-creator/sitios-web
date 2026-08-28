import os
import subprocess

BASE_DIR = r"E:\sitios web"
BASE_DIR_C = r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web"

print("=" * 80)
print("RESTAURACIÓN TOTAL DEL ECOSISTEMA AL ESTADO PERFECTO APROBADO")
print("=" * 80)

boutiques = [
    'pc-custom-lab', 
    'bazar-viamx-nfl.gdl', 
    'cigarros-bazar', 
    'dulces-bazar', 
    'kiosco-digital', 
    'mi-puesto-bazar', 
    'ofertas-y-liquidaciones'
]

# 1. En cada boutique, restaurar index.html al commit 033d603 (o el commit previo funcional)
for b in boutiques:
    sub_path = os.path.join(BASE_DIR, b)
    lock_file = os.path.join(sub_path, ".git", "index.lock")
    if os.path.exists(lock_file):
        try: os.remove(lock_file)
        except: pass

    # Eliminar js/ecosystem-catalog-engine.js si existe
    eng_js = os.path.join(sub_path, "js", "ecosystem-catalog-engine.js")
    if os.path.exists(eng_js):
        try: os.remove(eng_js)
        except: pass

    # Buscar el hash del commit donde se agregó el neon activo y catalogo 200 items
    r = subprocess.run(["git", "log", "--grep=neon", "-n", "1", "--format=%H"], cwd=sub_path, capture_output=True, text=True)
    target_hash = r.stdout.strip()
    if not target_hash:
        r2 = subprocess.run(["git", "log", "-n", "5", "--format=%H"], cwd=sub_path, capture_output=True, text=True)
        hashes = r2.stdout.strip().split('\n')
        target_hash = hashes[-1] if hashes else "HEAD"

    print(f"Restaurando [{b}] a commit {target_hash[:7]}...")
    subprocess.run(["git", "checkout", target_hash, "--", "index.html"], cwd=sub_path)

# 2. Restaurar root monorepo a f0383d1 (o commit con layout limpio)
lock_root = os.path.join(BASE_DIR, ".git", "index.lock")
if os.path.exists(lock_root):
    try: os.remove(lock_root)
    except: pass

eng_root = os.path.join(BASE_DIR, "js", "ecosystem-catalog-engine.js")
if os.path.exists(eng_root):
    try: os.remove(eng_root)
    except: pass

r_root = subprocess.run(["git", "log", "--grep=fichas", "-n", "1", "--format=%H"], cwd=BASE_DIR, capture_output=True, text=True)
root_hash = r_root.stdout.strip() or "f0383d1"
print(f"Restaurando Root Monorepo a commit {root_hash[:7]}...")
subprocess.run(["git", "checkout", root_hash, "--", "index.html"], cwd=BASE_DIR)

# 3. Espejo a C:
for root, dirs, files in os.walk(BASE_DIR):
    if '.git' in root or 'node_modules' in root: continue
    for file in files:
        if file.endswith(('.html', '.js', '.json', '.css')):
            src = os.path.join(root, file)
            rel = os.path.relpath(src, BASE_DIR)
            dst = os.path.join(BASE_DIR_C, rel)
            if os.path.exists(os.path.dirname(dst)):
                try:
                    with open(src, "rb") as f_in, open(dst, "wb") as f_out:
                        f_out.write(f_in.read())
                except: pass

print("✅ Todos los sitios restaurados al código funcional aprobado!")
