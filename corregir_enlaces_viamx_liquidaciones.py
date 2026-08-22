import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"

# Mapeo canónico exacto según los repositorios reales de GitHub Pages
CANONICAL_URLS = {
    "pc-custom-lab": "https://iaworldcenter-creator.github.io/pc-custom-lab/",
    "bazar-viamx-nfl.gdl": "https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/",
    "cigarros-bazar": "https://iaworldcenter-creator.github.io/cigarros-bazar/",
    "dulces-bazar": "https://iaworldcenter-creator.github.io/dulces-bazar/",
    "kiosco-digital": "https://iaworldcenter-creator.github.io/kiosco-digital/",
    "mi-puesto-bazar": "https://iaworldcenter-creator.github.io/mi-puesto-bazar/",
    "ofertas-y-liquidaciones": "https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/"
}

print("=" * 70)
print("1. CORRIGIENDO ENLACES EN EL PORTAL MATRIZ (index.html)")
print("=" * 70)

root_index = os.path.join(BASE_DIR, "index.html")
if os.path.exists(root_index):
    with open(root_index, "r", encoding="utf-8") as f:
        html = f.read()

    # Corregir enlace a Liquidaciones (con guión final)
    html = re.sub(
        r'https:\/\/iaworldcenter-creator\.github\.io\/ofertas-y-liquidaciones\/(?!-)',
        'https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/',
        html
    )
    html = re.sub(
        r'href=["\'](?:ofertas-y-liquidaciones\/?|ofertas-y-liquidaciones-\/?)["\']',
        'href="https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/"',
        html
    )

    # Corregir enlace a Viamx NFL (con mayúsculas canónicas)
    html = re.sub(
        r'https:\/\/iaworldcenter-creator\.github\.io\/bazar-viamx-nfl\.gdl\/',
        'https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/',
        html,
        flags=re.IGNORECASE
    )
    html = re.sub(
        r'href=["\'](?:bazar-viamx-nfl\.gdl\/?|bazar-viamx-NFL\.GDL\/?)["\']',
        'href="https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/"',
        html
    )

    with open(root_index, "w", encoding="utf-8") as f:
        f.write(html)
    print("✓ Enlaces corregidos en Portal Matriz (sitios web/index.html).")

print("\n" + "=" * 70)
print("2. CORRIGIENDO TOPBARS Y FOOTERS EN LAS 7 BOUTIQUES")
print("=" * 70)

for store, url in CANONICAL_URLS.items():
    # Buscar el directorio local (manejando variaciones con o sin guión)
    store_dir = os.path.join(BASE_DIR, store)
    if not os.path.exists(store_dir) and store == "ofertas-y-liquidaciones":
        alt_dir = os.path.join(BASE_DIR, "ofertas-y-liquidaciones-")
        if os.path.exists(alt_dir):
            store_dir = alt_dir

    if not os.path.exists(store_dir):
        continue

    for filename in ["index.html", "producto.html", "checkout.html"]:
        filepath = os.path.join(store_dir, filename)
        if not os.path.exists(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Reemplazar rutas hacia liquidaciones
        content = re.sub(
            r'https:\/\/iaworldcenter-creator\.github\.io\/ofertas-y-liquidaciones\/(?!-)',
            'https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/',
            content
        )

        # Reemplazar rutas hacia viamx
        content = re.sub(
            r'https:\/\/iaworldcenter-creator\.github\.io\/bazar-viamx-nfl\.gdl\/',
            'https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/',
            content,
            flags=re.IGNORECASE
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"  ✓ {os.path.basename(store_dir)}/{filename} actualizado.")

print("\n" + "=" * 70)
print("3. SINCRONIZACIÓN Y DESPLIEGUE A GITHUB")
print("=" * 70)

# Desplegar boutiques
for d in os.listdir(BASE_DIR):
    full_path = os.path.join(BASE_DIR, d)
    if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, ".git")):
        subprocess.run(["git", "add", "-A"], cwd=full_path, check=True)
        subprocess.run(["git", "commit", "-m", "fix(links): correccion de URLs exactas para Viamx y Liquidaciones", "--allow-empty"], cwd=full_path, capture_output=True)
        res = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=full_path, capture_output=True, text=True)
        print(f"  🟢 {d.ljust(28)} -> Push: {'OK' if res.returncode == 0 else res.stderr.strip()}")

# Desplegar repositorio central
subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(portal): rutas canonicas exactas para Viamx y Liquidaciones", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central        -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")

print("\n" + "=" * 70)
print("VERIFICACIÓN DE URLs OPERATIVAS:")
print("=" * 70)
print("  * Viamx NFL:     https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/")
print("  * Liquidaciones: https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/")
