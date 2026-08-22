import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
VIAMX_DIR = os.path.join(BASE_DIR, "bazar-viamx-nfl.gdl")

if not os.path.exists(VIAMX_DIR):
    alt = os.path.join(BASE_DIR, "bazar-viamx-NFL.GDL")
    if os.path.exists(alt):
        VIAMX_DIR = alt

INDEX_PATH = os.path.join(VIAMX_DIR, "index.html")

if not os.path.exists(INDEX_PATH):
    print(f"[Error] No se encontró {INDEX_PATH}")
    exit(1)

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

print("=" * 70)
print("AMPLIANDO ALTURA VERTICAL DEL CARRUSEL EN VÍA MX")
print("=" * 70)

# Actualizar altura en reglas CSS internas si existen
html = re.sub(
    r'\.hero-slider-container\s*\{[^}]*\}',
    '.hero-slider-container { min-height: 720px; } @media (min-width: 640px) { .hero-slider-container { min-height: 800px; } }',
    html
)

# Actualizar clases de altura en el contenedor del carrusel
html = re.sub(
    r'(<div[^>]*class=["\'][^"\']*relative\s+w-full\s+)[^"\']*(overflow-hidden[^"\']*["\'])',
    r'\1h-[720px] sm:h-[800px] min-h-[720px] sm:min-h-[800px] \2',
    html
)

# Reemplazo directo en caso de estilos inline o clases previas
html = re.sub(
    r'h-\[\d+px\]\s+sm:h-\[\d+px\]\s+min-h-\[\d+px\]\s+sm:min-h-\[\d+px\]',
    'h-[720px] sm:h-[800px] min-h-[720px] sm:min-h-[800px]',
    html
)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("✓ Altura expandida a 720px / 800px aplicada exitosamente.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "style(hero): ampliar altura vertical del carrusel a 720px/800px", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "style(viamx): carrusel con mayor amplitud vertical", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
