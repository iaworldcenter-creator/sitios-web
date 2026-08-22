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
print("CORRIGIENDO PROPORCIONES DE CABECERA EN VÍA MX")
print("=" * 70)

NIVEL_2_HEADER = """
    <!-- Nivel 2: Fila Principal de Identidad, Búsqueda y Mi Cuenta -->
    <div class="w-full max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4 py-3 px-4 sm:px-6 lg:px-8">
        
        <!-- Lado Izquierdo: Mi Carrito y Mi Cuenta -->
        <div class="shrink-0 flex items-center gap-3">
            <button onclick="toggleCartDrawer()" class="flex items-center gap-2.5 bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-sky-400 px-3.5 py-2 rounded-xl transition cursor-pointer group shadow-md shadow-sky-950/20">
                <div class="relative">
                    <i class="fa-solid fa-cart-shopping text-lg text-sky-400 group-hover:scale-105 transition"></i>
                    <span class="absolute -top-2 -right-2 bg-amber-500 text-slate-950 text-[10px] font-black rounded-full px-1.5 py-0.2 min-w-[16px] text-center shadow" id="cart-badge-count">0</span>
                </div>
                <div class="flex flex-col text-left">
                    <span class="text-[9px] font-mono text-slate-400 uppercase leading-none font-bold">Mi Carrito</span>
                    <span class="text-xs font-black text-white mt-0.5" id="header-cart-total">$0.00 MXN</span>
                </div>
            </button>
            <button onclick="openDeliveryModal()" class="flex items-center gap-2.5 bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-amber-400 px-3.5 py-2 rounded-xl transition cursor-pointer group shadow-md shadow-amber-950/20">
                <i class="fa-solid fa-circle-user text-xl text-amber-400 group-hover:scale-105 transition"></i>
                <div class="flex flex-col text-left">
                    <span class="text-[9px] font-mono text-slate-400 uppercase leading-none font-bold">Hola, Socio</span>
                    <span class="text-xs font-black text-white group-hover:text-amber-400 transition mt-0.5">Mi Cuenta</span>
                </div>
            </button>
        </div>

        <!-- Centro: Buscador Compacto Proporcional con Marco Neón -->
        <div class="flex-1 max-w-md w-full px-2">
            <form class="flex items-center bg-slate-950/90 rounded-full border-2 border-sky-400 shadow-[0_0_15px_rgba(56,189,248,0.4)] hover:shadow-[0_0_22px_rgba(56,189,248,0.65)] w-full px-3 py-1 gap-2 transition duration-300" onsubmit="handleSearchSubmit(event);" role="search">
                <label class="sr-only" for="siteSearch">¿Qué deseas buscar hoy?</label>
                <input aria-label="Buscar productos en el catálogo" autocomplete="off" class="flex-1 bg-transparent border-0 outline-none text-white font-bold text-xs px-3 placeholder-slate-400" id="siteSearch" name="q" placeholder="¿Qué producto o curaduría buscas hoy?..." type="text"/>
                <button aria-label="Buscar" class="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black px-4 py-1.5 rounded-full text-xs uppercase tracking-wider transition active:scale-95 shrink-0 flex items-center gap-1 shadow-md shadow-amber-500/20 cursor-pointer" type="submit">
                    <i class="fa-solid fa-magnifying-glass text-[11px]"></i> BUSCAR
                </button>
            </form>
        </div>

        <!-- Lado Derecho: Logo del Tigre (48px fijos) y VÍA MX en Azul -->
        <div class="shrink-0 flex items-center gap-3 group cursor-pointer" onclick="window.location.href='index.html'">
            <div class="relative w-12 h-12 flex items-center justify-center shrink-0">
                <img alt="Logo Oficial Vía MX" class="w-12 h-12 rounded-full object-cover border-2 border-sky-400 shadow-[0_0_12px_rgba(56,189,248,0.4)] group-hover:scale-105 transition shrink-0" style="width: 48px; height: 48px; max-width: 48px; max-height: 48px;" src="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" onerror="this.src='assets/img/mascota_tigre.webp';" />
            </div>
            <div class="flex flex-col text-left">
                <span class="text-2xl font-black tracking-wider uppercase text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-blue-400 to-cyan-300 drop-shadow-[0_2px_10px_rgba(56,189,248,0.35)] leading-tight">
                    Vía MX
                </span>
                <span class="text-[9px] font-mono font-bold tracking-widest text-sky-300 uppercase leading-none">Curaduría Selecta</span>
            </div>
        </div>

    </div>
"""

files_to_update = ["index.html", "producto.html", "checkout.html"]

for filename in files_to_update:
    filepath = os.path.join(VIAMX_DIR, filename)
    if not os.path.exists(filepath):
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # Reemplazar el nivel 2 de la cabecera preservando la barra deslizable superior
    if "<!-- Nivel 2:" in html:
        html = re.sub(
            r'<!-- Nivel 2:[\s\S]*?<\/header>',
            f'{NIVEL_2_HEADER.strip()}\n</header>',
            html,
            flags=re.IGNORECASE
        )
    else:
        html = re.sub(
            r'(<div class="w-full max-w-7xl mx-auto flex flex-col[\s\S]*?<\/header>)',
            f'{NIVEL_2_HEADER.strip()}\n</header>',
            html,
            flags=re.IGNORECASE
        )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  ✓ {os.path.basename(VIAMX_DIR)}/{filename} proporciones corregidas.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "fix(header): corregir dimensiones exactas de logotipo (48px) y alinear buscador con Via MX", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(viamx): proporciones definitivas de cabecera", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
