import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
VIAMX_DIR = os.path.join(BASE_DIR, "bazar-viamx-nfl.gdl")

if not os.path.exists(VIAMX_DIR):
    alt = os.path.join(BASE_DIR, "bazar-viamx-NFL.GDL")
    if os.path.exists(alt):
        VIAMX_DIR = alt

print("=" * 70)
print("AJUSTANDO BARRA DE BÚSQUEDA E INTEGRANDO LOGOTIPO VÍA MX")
print("=" * 70)

files_to_update = ["index.html", "producto.html", "checkout.html"]

for filename in files_to_update:
    filepath = os.path.join(VIAMX_DIR, filename)
    if not os.path.exists(filepath):
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Ajustar el contenedor de la barra de búsqueda para acortar su ancho
    html = re.sub(
        r'(<div[^>]*class=["\'][^"\']*max-w-[\w\d]+[^"\']*mx-auto[^"\']*["\'][^>]*>\s*<form[^>]*>)',
        r'<div class="flex-1 max-w-lg mx-auto w-full px-2">\n    <form class="flex items-center bg-slate-950/70 rounded-full border border-sky-500/60 shadow-[0_0_12px_rgba(14,165,233,0.35)] w-full px-2 py-1 gap-2" onsubmit="handleSearchSubmit(event);" role="search">',
        html,
        flags=re.IGNORECASE
    )

    # 2. Localizar y reestructurar el bloque derecho del logo con el texto 'Vía MX' en azul corporativo
    # Buscamos el contenedor de la imagen del tigre al lado derecho del header
    logo_regex = re.compile(
        r'(<div[^>]*class=["\'][^"\']*shrink-0[^"\']*flex[^"\']*items-center[^"\']*["\'][^>]*>[\s\S]*?<img[^>]*mascota_tigre[^>]*>[\s\S]*?<\/div>)',
        re.IGNORECASE
    )

    nuevo_bloque_logo = """<div class="shrink-0 flex items-center gap-3 group cursor-pointer" onclick="window.location.href='index.html'">
            <div class="relative">
                <img alt="Logo Oficial VíaMX" class="w-11 h-11 rounded-full object-cover border-2 border-sky-400 shadow-md shadow-sky-500/20 group-hover:scale-105 transition" src="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" onerror="this.src='assets/img/mascota_tigre.webp';" />
            </div>
            <div class="flex flex-col text-left">
                <span class="text-xl sm:text-2xl font-black tracking-wider uppercase text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-blue-400 to-indigo-300 drop-shadow-[0_2px_10px_rgba(56,189,248,0.3)] leading-none">
                    Vía MX
                </span>
                <span class="text-[9px] font-mono font-bold tracking-widest text-slate-400 uppercase mt-0.5">Curaduría Selecta</span>
            </div>
        </div>"""

    if logo_regex.search(html):
        html = logo_regex.sub(nuevo_bloque_logo, html, count=1)
    else:
        # Reemplazo por patrón alternativo si la imagen no tiene la clase exacta
        alt_pattern = re.compile(r'(<img[^>]*mascota_tigre[^>]*\/?>(?:\s*<\/div>)?)', re.IGNORECASE)
        html = alt_pattern.sub(nuevo_bloque_logo, html, count=1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  ✓ {os.path.basename(VIAMX_DIR)}/{filename} actualizado.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "style(header): buscador esbelto y logotipo distintivo Via MX en azul", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "style(viamx): ajuste de ancho en barra de busqueda y rotulo azul Via MX", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
