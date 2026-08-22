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
print("REDISEÑANDO CABECERA SIMÉTRICA Y PROPORCIONAL DE VÍA MX")
print("=" * 70)

NIVEL_2_HEADER = """
    <!-- Nivel 2: Fila Principal de Identidad, Búsqueda y Mi Cuenta -->
    <div class="w-full max-w-7xl mx-auto flex flex-col lg:flex-row justify-between items-center gap-4 py-3.5 px-4 sm:px-6 lg:px-8">
        
        <!-- Lado Izquierdo: Mi Carrito y Mi Cuenta (Separados, Íconos Grandes y Tipografía Homologada en Blanco) -->
        <div class="shrink-0 flex items-center gap-6 sm:gap-8 order-2 lg:order-1">
            <!-- Mi Carrito -->
            <button onclick="toggleCartDrawer()" class="flex items-center gap-3 bg-transparent hover:opacity-80 transition cursor-pointer group text-left">
                <div class="relative flex items-center justify-center">
                    <i class="fa-solid fa-cart-shopping text-3xl sm:text-4xl text-cyan-400 group-hover:scale-105 transition"></i>
                    <span class="absolute -top-2 -right-2 bg-amber-500 text-slate-950 text-[10px] font-black rounded-full px-1.5 py-0.2 min-w-[18px] text-center shadow" id="cart-badge-count">0</span>
                </div>
                <div class="flex flex-col">
                    <span class="text-xs sm:text-sm font-black text-white uppercase tracking-wider leading-tight">Mi Carrito</span>
                    <span class="text-xs sm:text-sm font-black text-white mt-0.5" id="header-cart-total">$0.00 MXN</span>
                </div>
            </button>

            <!-- Mi Cuenta -->
            <button onclick="openDeliveryModal()" class="flex items-center gap-3 bg-transparent hover:opacity-80 transition cursor-pointer group text-left">
                <div class="relative flex items-center justify-center">
                    <i class="fa-solid fa-circle-user text-3xl sm:text-4xl text-amber-400 group-hover:scale-105 transition"></i>
                </div>
                <div class="flex flex-col">
                    <span class="text-xs sm:text-sm font-black text-white uppercase tracking-wider leading-tight">Mi Cuenta</span>
                    <span class="text-xs sm:text-sm font-black text-white mt-0.5">Hola, Socio</span>
                </div>
            </button>
        </div>

        <!-- Centro: Buscador Amplio con Marco Neón Cian -->
        <div class="flex-1 max-w-2xl w-full px-2 sm:px-4 order-3 lg:order-2">
            <form class="flex items-center bg-slate-950/90 rounded-full border-2 border-cyan-400 shadow-[0_0_18px_rgba(6,182,212,0.45)] hover:shadow-[0_0_26px_rgba(6,182,212,0.75)] w-full px-3.5 py-1.5 gap-2 transition duration-300" onsubmit="handleSearchSubmit(event);" role="search">
                <label class="sr-only" for="siteSearch">¿Qué deseas buscar hoy?</label>
                <input aria-label="Buscar productos en el catálogo" autocomplete="off" class="flex-1 bg-transparent border-0 outline-none text-white font-bold text-xs px-3 placeholder-slate-400" id="siteSearch" name="q" placeholder="¿Qué producto, artículo o curaduría buscas hoy? Escribe aquí..." type="text"/>
                <button aria-label="Buscar" class="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black px-6 py-2 rounded-full text-xs uppercase tracking-wider transition active:scale-95 shrink-0 flex items-center gap-1.5 shadow-md shadow-amber-500/20 cursor-pointer" type="submit">
                    <i class="fa-solid fa-magnifying-glass text-xs"></i> BUSCAR
                </button>
            </form>
        </div>

        <!-- Lado Derecho: Logo de la Mascota y VÍA MX en Azul Cian (Sin subtítulo) -->
        <div class="shrink-0 flex items-center gap-3.5 group cursor-pointer order-1 lg:order-3" onclick="window.location.href='index.html'">
            <div class="relative w-12 h-12 flex items-center justify-center shrink-0">
                <img alt="Logo Oficial Vía MX" class="w-12 h-12 rounded-full object-cover border-2 border-cyan-400 shadow-[0_0_14px_rgba(6,182,212,0.5)] group-hover:scale-105 transition shrink-0" style="width: 48px; height: 48px; max-width: 48px; max-height: 48px;" src="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" onerror="this.src='assets/img/mascota_tigre.webp';" />
            </div>
            <span class="text-2xl sm:text-3xl font-black tracking-wider uppercase text-cyan-400 drop-shadow-[0_2px_12px_rgba(6,182,212,0.5)] leading-none select-none">
                Vía MX
            </span>
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

    # Purgar cualquier comentario residual roto
    html = re.sub(r'Centro:?\s*Buscador Enorme[\s\S]*?-->', '', html, flags=re.IGNORECASE)

    # Reemplazar la fila del nivel 2 manteniendo la barra superior (Nivel 1)
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

    print(f"  ✓ {os.path.basename(VIAMX_DIR)}/{filename} cabecera simétrica actualizada.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "style(header): buscador amplio, elementos simetricos en blanco y rotulo cyan Via MX", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "style(viamx): cabecera simetrica y buscador amplio", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
