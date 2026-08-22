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
print("REDISEÑANDO CABECERA, IDENTIDAD Y BUSCADOR DE VÍA MX")
print("=" * 70)

NIVEL_2_HEADER = """
    <!-- Nivel 2: Fila Principal de Identidad, Búsqueda y Mi Cuenta -->
    <div class="w-full max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4 py-4 px-6 md:px-10">
        
        <!-- Lado Izquierdo: Mi Carrito y Mi Cuenta (Ampliados y Destacados) -->
        <div class="shrink-0 flex items-center gap-3.5 order-2 md:order-1">
            <button onclick="toggleCartDrawer()" class="flex items-center gap-3 bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-sky-400 px-4 py-2.5 rounded-2xl transition cursor-pointer group shadow-lg shadow-sky-950/20">
                <div class="relative">
                    <i class="fa-solid fa-cart-shopping text-xl text-sky-400 group-hover:scale-110 transition"></i>
                    <span class="absolute -top-2.5 -right-2.5 bg-amber-500 text-slate-950 text-[10px] font-black rounded-full px-1.5 py-0.2 min-w-[18px] text-center shadow" id="cart-badge-count">0</span>
                </div>
                <div class="flex flex-col text-left">
                    <span class="text-[10px] font-mono text-slate-400 uppercase leading-none font-bold">Mi Carrito</span>
                    <span class="text-xs font-black text-white mt-0.5" id="header-cart-total">$0.00 MXN</span>
                </div>
            </button>
            <button onclick="openDeliveryModal()" class="flex items-center gap-3 bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-amber-400 px-4 py-2.5 rounded-2xl transition cursor-pointer group shadow-lg shadow-amber-950/20">
                <i class="fa-solid fa-circle-user text-2xl text-amber-400 group-hover:scale-110 transition"></i>
                <div class="flex flex-col text-left">
                    <span class="text-[10px] font-mono text-slate-400 uppercase leading-none font-bold">Hola, Socio</span>
                    <span class="text-xs font-black text-white group-hover:text-amber-400 transition mt-0.5">Mi Cuenta</span>
                </div>
            </button>
        </div>

        <!-- Centro: Buscador Compacto con Marco Resaltado Neón Sky -->
        <div class="flex-1 max-w-md mx-auto w-full px-2 order-3 md:order-2">
            <form class="flex items-center bg-slate-950/90 rounded-full border-2 border-sky-400 shadow-[0_0_18px_rgba(56,189,248,0.55)] hover:shadow-[0_0_26px_rgba(56,189,248,0.8)] w-full px-3 py-1.5 gap-2 transition duration-300" onsubmit="handleSearchSubmit(event);" role="search">
                <label class="sr-only" for="siteSearch">¿Qué deseas buscar hoy?</label>
                <input aria-label="Buscar productos en el catálogo" autocomplete="off" class="flex-1 bg-transparent border-0 outline-none text-white font-bold text-xs px-3 placeholder-slate-400" id="siteSearch" name="q" placeholder="¿Qué producto o curaduría buscas hoy?..." type="text"/>
                <button aria-label="Buscar" class="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black px-5 py-1.5 rounded-full text-xs uppercase tracking-wider transition active:scale-95 shrink-0 flex items-center gap-1.5 shadow-md shadow-amber-500/20 cursor-pointer" type="submit">
                    <i class="fa-solid fa-magnifying-glass text-xs"></i> BUSCAR
                </button>
            </form>
        </div>

        <!-- Lado Derecho: Logo de la Mascota y VÍA MX en Letras Grandes Azules -->
        <div class="shrink-0 flex items-center gap-3.5 group cursor-pointer order-1 md:order-3" onclick="window.location.href='index.html'">
            <div class="relative">
                <img alt="Logo Oficial Vía MX" class="w-13 h-13 rounded-full object-cover border-2 border-sky-400 shadow-[0_0_16px_rgba(56,189,248,0.5)] group-hover:scale-105 transition" src="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" onerror="this.src='assets/img/mascota_tigre.webp';" />
            </div>
            <div class="flex flex-col text-left">
                <span class="text-3xl sm:text-4xl font-black tracking-wider uppercase text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-blue-400 to-cyan-300 drop-shadow-[0_2px_14px_rgba(56,189,248,0.45)] leading-tight">
                    Vía MX
                </span>
                <span class="text-[10px] font-mono font-bold tracking-widest text-sky-300 uppercase leading-none">Curaduría Selecta</span>
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

    # 1. Purgar textos residuales y comentarios rotos
    html = re.sub(r'Centro:?\s*Buscador Enorme\s*<--->[\s\S]*?-->', '', html, flags=re.IGNORECASE)
    html = re.sub(r'Centro:\s*Buscador[\s\S]*?V[íi]aMX\)?\s*-->', '', html, flags=re.IGNORECASE)
    html = re.sub(r'Centro:\"?Buscador Enorme[\s\S]*?-->', '', html, flags=re.IGNORECASE)

    # 2. Reemplazar la Fila Principal de la cabecera (Nivel 2)
    # Localizar desde el final de la barra superior (Nivel 1) hasta el cierre de </header>
    if "<!-- Nivel 2:" in html:
        html = re.sub(
            r'<!-- Nivel 2:[\s\S]*?<\/header>',
            f'{NIVEL_2_HEADER.strip()}\n</header>',
            html,
            flags=re.IGNORECASE
        )
    else:
        # Reemplazo dentro del contenedor de cabecera estándar
        html = re.sub(
            r'(<div class="w-full max-w-7xl mx-auto flex flex-col[\s\S]*?<\/header>)',
            f'{NIVEL_2_HEADER.strip()}\n</header>',
            html,
            flags=re.IGNORECASE
        )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  ✓ {os.path.basename(VIAMX_DIR)}/{filename} reestructurado exitosamente.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "style(header): buscador compacto neon, rotulo grande Via MX y seccion Mi Cuenta ampliada", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "style(viamx): purga de textos residuales y actualizacion de cabecera", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
