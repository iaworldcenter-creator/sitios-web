import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
PC_INDEX_PATH = os.path.join(BASE_DIR, "pc-custom-lab", "index.html")

def fix_boutique_routing():
    print("=" * 75)
    print("REPARANDO ENRUTAMIENTO Y CONEXIÓN CON LA BOUTIQUE EN PC CUSTOM LAB")
    print("=" * 75)

    if not os.path.exists(PC_INDEX_PATH):
        print(f"[Error] No se encontró: {PC_INDEX_PATH}")
        return

    with open(PC_INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Eliminar scripts duplicados e inconsistentes al final del body
    # Limpiar bloques redundantes de HARDWARE_CATALOG repetidos
    pattern_dups = r'<script>\s*// Sincronización automática de contador[\s\S]*?<\/script>\s*</body>'
    clean_closing_script = """<script>
// Sincronización automática de contador y drawer de carrito
function syncGlobalCartState() {
    try {
        let cart = [];
        const raw = localStorage.getItem('ecosystem_global_cart');
        if (raw) cart = JSON.parse(raw);
        const activeItems = cart.filter(i => i && i.quantity > 0);
        const totalCount = activeItems.reduce((sum, i) => sum + (parseInt(i.quantity) || 0), 0);

        document.querySelectorAll('#cart-count, .cart-counter, [data-cart-count]').forEach(el => {
            el.innerText = totalCount;
            el.style.display = totalCount > 0 ? 'inline-flex' : 'none';
        });

        document.querySelectorAll('header a, header button').forEach(el => {
            if (el.innerText && el.innerText.includes('MI CARRITO')) {
                el.innerHTML = '<i class="fa-solid fa-cart-shopping"></i> MI CARRITO (' + totalCount + ')';
            }
        });
    } catch(e) {}
}
document.addEventListener('DOMContentLoaded', syncGlobalCartState);
window.addEventListener('storage', syncGlobalCartState);
</script>
</body>"""

    if re.search(pattern_dups, content):
        content = re.sub(pattern_dups, clean_closing_script, content)

    # 2. Inyección robusta del enrutador de la boutique en el script principal
    js_boutique_router = """
// ========================================================================
// ENRUTADOR BIDIRECCIONAL A LA BOUTIQUE (10 PÁGINAS CATALAGO)
// ========================================================================
const BOUTIQUE_PAGE_MAP = {
    'gpu': 1,
    'tarjeta-video': 1,
    'motherboards': 2,
    'tarjeta-madre': 2,
    'ram': 3,
    'memoria-ram': 3,
    'procesadores': 4,
    'cpu': 4,
    'almacenamiento': 5,
    'ssd': 5,
    'hdd': 5,
    'gabinetes': 6,
    'gabinete': 6,
    'fuentes': 7,
    'fuente': 7,
    'enfriamiento': 8,
    'cooling': 8,
    'monitores': 9,
    'monitor': 9,
    'perifericos': 10,
    'teclado': 10,
    'mouse': 10
};

window.goToBoutiqueCategory = function(cat) {
    const targetPage = BOUTIQUE_PAGE_MAP[cat] || 1;
    const btns = document.querySelectorAll('.pagination-btn');
    const targetBtn = btns[targetPage - 1];
    
    if (typeof changePage === 'function') {
        changePage(targetPage, targetBtn);
    }
    
    const prodSection = document.getElementById('productos');
    if (prodSection) {
        prodSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
};
"""

    if "BOUTIQUE_PAGE_MAP" not in content:
        content = content.replace("function changePage(page, btnElement) {", f"{js_boutique_router}\nfunction changePage(page, btnElement) {{")
    else:
        content = re.sub(r'const BOUTIQUE_PAGE_MAP =[\s\S]*?window\.goToBoutiqueCategory = function[\s\S]*?};', js_boutique_router, content)

    # 3. Asegurar que los botones de la pirámide invoquen la función global
    piramide_clean_buttons = """<div class="flex flex-col gap-1.5" id="pyramid-list">
                        <button type="button" onclick="window.goToBoutiqueCategory('ram')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group cursor-pointer">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-memory text-[11px] text-cyan-400"></i> 1. Memoria RAM</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-ram">$0 MXN</span>
                        </button>
                        <button type="button" onclick="window.goToBoutiqueCategory('perifericos')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group cursor-pointer">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-computer-mouse text-[11px] text-blue-400"></i> 2. Mouse &amp; Mousepad</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-mouse">$0 MXN</span>
                        </button>
                        <button type="button" onclick="window.goToBoutiqueCategory('fuentes')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group cursor-pointer">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-plug text-[11px] text-emerald-400"></i> 3. Fuente de Poder</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-psu">$0 MXN</span>
                        </button>
                        <button type="button" onclick="window.goToBoutiqueCategory('monitores')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group cursor-pointer">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-tv text-[11px] text-purple-400"></i> 4. Monitor</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-monitor">$0 MXN</span>
                        </button>
                        <button type="button" onclick="window.goToBoutiqueCategory('perifericos')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group cursor-pointer">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-keyboard text-[11px] text-emerald-400"></i> 5. Teclado Gamer / Oficina</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-teclado">$0 MXN</span>
                        </button>
                        <button type="button" onclick="window.goToBoutiqueCategory('gabinetes')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group cursor-pointer">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-box text-[11px] text-blue-400"></i> 6. Gabinete (Chasis)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-gabinete">$0 MXN</span>
                        </button>
                        <button type="button" onclick="window.goToBoutiqueCategory('procesadores')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group cursor-pointer">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-microchip text-[11px] text-pink-400"></i> 7. Procesador (Intel / AMD)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-cpu">$0 MXN</span>
                        </button>
                        <button type="button" onclick="window.goToBoutiqueCategory('almacenamiento')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group cursor-pointer">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-hard-drive text-[11px] text-amber-400"></i> 8. Almacenamiento (SSD / HDD)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-ssd">$0 MXN</span>
                        </button>
                        <button type="button" onclick="window.goToBoutiqueCategory('gpu')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group cursor-pointer">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-vr-cardboard text-[11px] text-indigo-400"></i> 9. Tarjeta de Video (GPU)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-gpu">$0 MXN</span>
                        </button>
                        <button type="button" onclick="window.goToBoutiqueCategory('motherboards')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group cursor-pointer">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-chess-board text-[11px] text-purple-400"></i> 10. Tarjeta Madre (Motherboard)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-mobo">$0 MXN</span>
                        </button>
                        <button type="button" onclick="window.goToBoutiqueCategory('enfriamiento')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group cursor-pointer">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-fan text-[11px] text-teal-400"></i> 11. Sistema de Enfriamiento</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-cooling">$0 MXN</span>
                        </button>
                        <div class="w-full flex justify-between items-center bg-slate-900/60 border border-slate-800/80 rounded-lg px-3 py-1.5 text-left">
                            <span class="text-xs font-semibold text-slate-300 flex items-center gap-2"><i class="fa-brands fa-windows text-[11px] text-pink-400"></i> 12. Sistema Operativo &amp; Software</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-software">$0 MXN</span>
                        </div>
                    </div>"""

    content = re.sub(r'<div class="flex flex-col gap-1\.5" id="pyramid-list">[\s\S]*?<\/div>\s*<\/div>\s*<!-- SEMÁFORO', f"{piramide_clean_buttons}\n                </div>\n                <!-- SEMÁFORO", content)

    with open(PC_INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("✓ Enrutamiento de la boutique integrado y scripts duplicados saneados.")

def deploy():
    print("\n" + "=" * 75)
    print("SUBIENDO CAMBIOS A GITHUB PAGES (-C GC.AUTO=0)")
    print("=" * 75)
    pc_dir = os.path.join(BASE_DIR, "pc-custom-lab")
    subprocess.run(["git", "add", "-A"], cwd=pc_dir, check=True)
    subprocess.run(["git", "commit", "-m", "fix(cotizador): navegacion funcional a las 10 paginas de la boutique", "--allow-empty"], cwd=pc_dir, capture_output=True)
    res_pc = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=pc_dir, capture_output=True, text=True)
    print(f"🟢 pc-custom-lab -> Push: {'OK' if res_pc.returncode == 0 else res_pc.stderr.strip()}")

    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "fix(pc-custom-lab): enlaces interactivos boutique y limpieza de scripts", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
    res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
    print(f"🟢 Monorepositorio Raíz -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    fix_boutique_routing()
    deploy()
