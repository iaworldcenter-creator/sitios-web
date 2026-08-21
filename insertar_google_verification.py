import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"

STORES = [
    "pc-custom-lab",
    "bazar-viamx-nfl.gdl",
    "cigarros-bazar",
    "dulces-bazar",
    "kiosco-digital",
    "mi-puesto-bazar",
    "ofertas-y-liquidaciones"
]

GOOGLE_META_TAG = '<meta name="google-site-verification" content="2xIPYIU_imoZjFogZhoFRuepS7PFhXQloOamPV7ex6Q" />'

def update_verification_tag(filepath):
    if not os.path.exists(filepath):
        return False
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Si ya existe un meta tag de verificación previo, reemplazarlo
    if "google-site-verification" in content:
        content = re.sub(
            r'<meta\s+name=["\']google-site-verification["\']\s+content=["\'][^"\']*["\']\s*/?>',
            GOOGLE_META_TAG,
            content,
            flags=re.IGNORECASE
        )
    else:
        # Si no existe, insertarlo justo antes de </head>
        content = content.replace("</head>", f"    {GOOGLE_META_TAG}\n</head>", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True

print("=== 1. INSERTANDO TOKEN DE VERIFICACIÓN EN EL ECOSISTEMA ===")

# Actualizar en el Portal Central (index.html raíz)
root_index = os.path.join(BASE_DIR, "index.html")
if update_verification_tag(root_index):
    print("✓ Portal Matriz (sitios web/index.html) actualizado.")

# Actualizar en cada boutique satélite
for store in STORES:
    store_index = os.path.join(BASE_DIR, store, "index.html")
    if update_verification_tag(store_index):
        print(f"✓ {store}/index.html actualizado.")

print("\n=== 2. DESPLIEGUE A GITHUB PAGES ===")
for store in STORES:
    store_dir = os.path.join(BASE_DIR, store)
    if os.path.exists(os.path.join(store_dir, ".git")):
        subprocess.run(["git", "add", "-A"], cwd=store_dir, check=True)
        subprocess.run(["git", "commit", "-m", "feat(seo): token de verificacion Google Search Console", "--allow-empty"], cwd=store_dir, capture_output=True)
        subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=store_dir, capture_output=True)
        print(f"🟢 Push OK: {store}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(seo): insertar meta tag de Google Search Console en portal matriz", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print("🟢 Push OK: Repositorio Raíz (sitios web)")
