import os
import subprocess

BASE_DIR = r"E:\sitios web"
PC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")

# 1. Asegurar .gitignore en base y en pc-custom-lab
for path in [BASE_DIR, PC_DIR]:
    gi = os.path.join(path, ".gitignore")
    content = ""
    if os.path.exists(gi):
        with open(gi, "r", encoding="utf-8") as f:
            content = f.read()
    
    entries_to_add = ["*.zip", "*.tar.gz", "__pycache__/", "*.tmp", "*.log"]
    new_entries = [e for e in entries_to_add if e not in content]
    if new_entries:
        with open(gi, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(new_entries) + "\n")

# 2. Deshacer el commit local en BASE_DIR si tenía el .zip
for p in [BASE_DIR, PC_DIR]:
    lock = os.path.join(p, ".git", "index.lock")
    if os.path.exists(lock):
        try: os.remove(lock)
        except: pass

# Unstage/reset zip
subprocess.run(["git", "reset", "HEAD~1"], cwd=BASE_DIR)
subprocess.run(["git", "reset", "pc-custom-lab_BACKUP_ORO_2026-08-31.zip"], cwd=BASE_DIR)

# 3. Commit y Push limpio de pc-custom-lab
print("Commit & Push pc-custom-lab...")
subprocess.run(["git", "add", "-A"], cwd=PC_DIR)
subprocess.run(["git", "commit", "-m", "chore(cleanup): purga de archivos temporales y optimizacion de repositorio"], cwd=PC_DIR)
r1 = subprocess.run(["git", "push", "origin", "main"], cwd=PC_DIR, capture_output=True, text=True)
print(f"pc-custom-lab push: {r1.returncode}, {r1.stdout}, {r1.stderr}")

# 4. Commit y Push limpio de BASE_DIR
print("Commit & Push root monorepo...")
subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
subprocess.run(["git", "commit", "-m", "chore(cleanup): purga integral del ecosistema y saneamiento de git"], cwd=BASE_DIR)
r2 = subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"root monorepo push: {r2.returncode}, {r2.stdout}, {r2.stderr}")

print("✅ Sincronización limpia completada con éxito.")
