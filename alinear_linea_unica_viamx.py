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
print("HOMOLOGANDO CABECERA DE VÍA MX EN 2 NIVELES ESTRICTOS")
print("=" * 70)

NIVEL_2_HEADER = """
    <!-- Nivel 2: Fila Principal en UNA SOLA LÍNEA (Izquierda: Carrito/Cuenta, Centro: Buscador Full, Derecha: Vía MX) -->
    <div class="w-full max-w-[98%] 2xl:max-w-7xl mx-auto flex flex-nowrap items-center justify-between gap-3 sm:gap-6 py-3 px-2 sm:px-6">
        
        <!-- 1. EXTREMO IZQUIERDO: Mi Carrito y Mi Cuenta -->
        <div class="shrink-0 flex items-center gap-4 sm:gap-6">
            <!-- Mi Carrito -->
            <button onclick="toggleCartDrawer()" class="flex items-center gap-2.5 bg-transparent hover:opacity-80 transition cursor-pointer text-left group">
                <div class="relative flex items-center justify-center">
                    <i class="fa-solid fa-cart-shopping text-2xl sm:text-3xl text-cyan-400 group-hover:scale-105 transition"></i>
                    <span class="absolute -top-2 -right-2 bg-amber-500 text-slate-950 text-[10px] font-black rounded-full px-1.5 py-0.2 min-w-[17px] text-center shadow" id="cart-badge-count">0</span>
                </div>
                <div class="flex flex-col">
                    <span class="text-xs sm:text-sm font-black text-white uppercase tracking-wider leading-tight">Mi Carrito</span>
                    <span class="text-xs sm:text-sm font-black text-white mt-0.5" id="header-cart-total">$0.00 MXN</span>
                </div>
            </button>

            <!-- Mi Cuenta (Dinámico) -->
            <button onclick="openDeliveryModal()" class="flex items-center gap-2.5 bg-transparent hover:opacity-80 transition cursor-pointer text-left group">
                <div class="relative flex items-center justify-center">
                    <i class="fa-solid fa-circle-user text-2xl sm:text-3xl text-amber-400 group-hover:scale-105 transition"></i>
                </div>
                <div class="flex flex-col">
                    <span class="text-xs sm:text-sm font-black text-white uppercase tracking-wider leading-tight" id="header-acc-title">Mi Cuenta</span>
                    <span class="text-[11px] font-bold text-slate-200 mt-0.5" id="header-acc-sub">Regístrate, socio</span>
                </div>
            </button>
        </div>

        <!-- 2. CENTRO: Buscador Expandido al Máximo Disponible -->
        <div class="flex-1 min-w-[180px] mx-1 sm:mx-3">
            <form class="flex items-center bg-slate-950/90 rounded-full border-2 border-cyan-400 shadow-[0_0_18px_rgba(6,182,212,0.45)] hover:shadow-[0_0_26px_rgba(6,182,212,0.75)] w-full px-3.5 py-1.5 gap-2 transition duration-300" onsubmit="handleSearchSubmit(event);" role="search">
                <label class="sr-only" for="siteSearch">¿Qué deseas buscar hoy?</label>
                <input aria-label="Buscar productos en el catálogo" autocomplete="off" class="flex-1 bg-transparent border-0 outline-none text-white font-bold text-xs px-3 placeholder-slate-400" id="siteSearch" name="q" placeholder="¿Qué producto, artículo o curaduría buscas hoy? Escribe aquí..." type="text"/>
                <button aria-label="Buscar" class="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black px-4 sm:px-6 py-2 rounded-full text-xs uppercase tracking-wider transition active:scale-95 shrink-0 flex items-center gap-1.5 shadow-md shadow-amber-500/20 cursor-pointer" type="submit">
                    <i class="fa-solid fa-magnifying-glass text-xs"></i> BUSCAR
                </button>
            </form>
        </div>

        <!-- 3. EXTREMO DERECHO: Logo Mascota y Rótulo Vía MX -->
        <div class="shrink-0 flex items-center gap-3 group cursor-pointer" onclick="window.location.href='index.html'">
            <div class="relative w-12 h-12 flex items-center justify-center shrink-0">
                <img alt="Logo Oficial Vía MX" class="w-12 h-12 rounded-full object-cover border-2 border-cyan-400 shadow-[0_0_14px_rgba(6,182,212,0.5)] group-hover:scale-105 transition shrink-0" style="width: 48px; height: 48px; min-width: 48px; min-height: 48px;" src="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" onerror="this.src='assets/img/mascota_tigre.webp';" />
            </div>
            <span class="text-2xl sm:text-3xl font-black tracking-wider uppercase text-cyan-400 drop-shadow-[0_2px_12px_rgba(6,182,212,0.5)] leading-none select-none">
                Vía MX
            </span>
        </div>

    </div>
"""

JS_ACCOUNT_SYNC = """
<script id="account-status-sync">
function syncHeaderAccountStatus() {
    try {
        const stored = sessionStorage.getItem('ecosystem_delivery_address') || localStorage.getItem('ecosystem_delivery_address');
        const titleEl = document.getElementById('header-acc-title');
        const subEl = document.getElementById('header-acc-sub');
        if (stored && titleEl && subEl) {
            const addr = JSON.parse(stored);
            if (addr && addr.name) {
                titleEl.innerText = "Mi Dirección";
                subEl.innerText = "Hola, " + addr.name.split(' ')[0];
                return;
            }
        }
        if (titleEl && subEl) {
            titleEl.innerText = "Mi Cuenta";
            subEl.innerText = "Regístrate, socio";
        }
    } catch(e) {}
}
document.addEventListener('DOMContentLoaded', syncHeaderAccountStatus);
window.addEventListener('storage', syncHeaderAccountStatus);
</script>
"""

files_to_update = ["index.html", "producto.html", "checkout.html"]

for filename in files_to_update:
    filepath = os.path.join(VIAMX_DIR, filename)
    if not os.path.exists(filepath):
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # Reemplazar el nivel 2 asegurando una sola línea horizontal
    if "<!-- Nivel 2:" in html:
        html = re.sub(
            r'<!-- Nivel 2:[\s\S]*?<\/header>',
            f'{NIVEL_2_HEADER.strip()}\n</header>',
            html,
            flags=re.IGNORECASE
        )
    else:
        html = re.sub(
            r'(<div class="w-full max-w-7xl mx-auto flex[\s\S]*?<\/header>)',
            f'{NIVEL_2_HEADER.strip()}\n</header>',
            html,
            flags=re.IGNORECASE
        )

    # Inyectar script de sincronización de cuenta si no existe
    if 'id="account-status-sync"' not in html:
        html = html.replace("</body>", f"{JS_ACCOUNT_SYNC}\n</body>")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  ✓ {os.path.basename(VIAMX_DIR)}/{filename} alineado en una sola línea horizontal.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "style(header): estructura estricta en 2 niveles, linea unica continua con buscador full y cuenta dinamica", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "style(viamx): linea unica de cabecera en 2 niveles", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
