import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
STORES = [
    "pc-custom-lab",
    "cigarros-bazar",
    "dulces-bazar",
    "kiosco-digital",
    "mi-puesto-bazar",
    "ofertas-y-liquidaciones",
    "bazar-viamx-nfl.gdl"
]

RESOLVE_IMG_JS = """
function getGlobalProductImage(sku, localImg) {
    if (localImg && (localImg.startsWith('http://') || localImg.startsWith('https://'))) {
        return localImg;
    }
    const cleanSku = (sku || '').toUpperCase();
    let storeDomain = 'pc-custom-lab';
    if (cleanSku.startsWith('GPU-') || cleanSku.startsWith('PC-')) storeDomain = 'pc-custom-lab';
    else if (cleanSku.startsWith('CN-') || cleanSku.startsWith('CB-')) storeDomain = 'cigarros-bazar';
    else if (cleanSku.startsWith('DB-') || cleanSku.startsWith('DUL-')) storeDomain = 'dulces-bazar';
    else if (cleanSku.startsWith('KD-') || cleanSku.startsWith('KIO-')) storeDomain = 'kiosco-digital';
    else if (cleanSku.startsWith('PB-') || cleanSku.startsWith('PUE-')) storeDomain = 'mi-puesto-bazar';
    else if (cleanSku.startsWith('OLG-') || cleanSku.startsWith('LIQ-')) storeDomain = 'ofertas-y-liquidaciones';
    else if (cleanSku.startsWith('NFL-') || cleanSku.startsWith('VIA-')) storeDomain = 'bazar-viamx-nfl.gdl';

    let path = localImg || 'assets/img/slider_ia_human_thumb.webp';
    path = path.replace(/^(\.\/|\/)/, '');
    return 'https://iaworldcenter-creator.github.io/' + storeDomain + '/' + path;
}
"""

CHECKOUT_ROW_TEMPLATE = """
            let globalImg = getGlobalProductImage(item.sku, item.imagen);
            let rowClass = "flex flex-col sm:flex-row items-center sm:items-stretch gap-4 p-4 bg-slate-900 border border-slate-800 rounded-2xl mb-3 shadow-md transition-all duration-300";
            let controlsHtml = "";

            if (isInactive) {
                rowClass += " opacity-50 grayscale";
                controlsHtml = `
                    <div class="flex items-center justify-between w-full mt-2 pt-2 border-t border-slate-800">
                        <span class="bg-red-500/10 border border-red-500/30 text-red-400 font-bold px-2 py-0.5 rounded text-[10px] uppercase tracking-wider">Desactivado</span>
                        <button onclick="changeQty('${item.sku}', 1)" class="px-3 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs transition cursor-pointer flex items-center gap-1.5 active:scale-95 shadow-md">
                            Reactivar +
                        </button>
                    </div>
                `;
            } else {
                let minusBtn = `<button onclick="changeQty('${item.sku}', -1)" class="w-8 h-8 rounded-lg bg-slate-800 text-slate-300 hover:text-white transition flex items-center justify-center font-bold text-xs cursor-pointer">-</button>`;
                if (item.quantity === 1) {
                    minusBtn = `<button onclick="deleteItem('${item.sku}')" class="w-8 h-8 rounded-lg bg-red-950/80 text-red-400 hover:bg-red-900 hover:text-red-200 transition flex items-center justify-center text-xs cursor-pointer" title="Eliminar"><i class="fa-solid fa-trash-can"></i></button>`;
                }
                controlsHtml = `
                    <div class="flex items-center justify-between w-full mt-2 pt-2 border-t border-slate-800">
                        <div class="flex items-center gap-1.5 bg-slate-950 border border-slate-800 rounded-xl p-1">
                            ${minusBtn}
                            <span class="text-white font-black text-xs w-7 text-center font-mono">${item.quantity}</span>
                            <button onclick="changeQty('${item.sku}', 1)" class="w-8 h-8 rounded-lg bg-slate-800 text-slate-300 hover:text-white transition flex items-center justify-center font-bold text-xs cursor-pointer">+</button>
                        </div>
                        <div class="flex flex-col items-end">
                            <span class="text-[10px] text-slate-400 font-semibold">$${parseFloat(item.precio).toLocaleString()} c/u</span>
                            <span class="text-cyan-400 font-black text-sm">$${sub.toFixed(2)} MXN</span>
                        </div>
                        <button onclick="deleteItem('${item.sku}')" class="text-slate-500 hover:text-red-400 text-sm cursor-pointer shrink-0 transition p-1.5 ml-1" title="Eliminar"><i class="fa-solid fa-trash-can"></i></button>
                    </div>
                `;
            }

            const div = document.createElement("div");
            div.className = rowClass;
            div.innerHTML = `
                <div class="w-[170px] h-[170px] min-w-[170px] max-w-[170px] min-h-[170px] max-h-[170px] rounded-xl overflow-hidden bg-slate-950 border border-slate-700/80 shrink-0 p-2 flex items-center justify-center">
                    <img src="${globalImg}" class="w-full h-full object-contain rounded-lg" alt="${item.nombre}" loading="lazy" onerror="this.onerror=null;this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp';" />
                </div>
                <div class="flex-1 flex flex-col justify-between min-w-0 w-full py-1">
                    <div>
                        <h3 class="text-white font-bold text-sm sm:text-base leading-snug">${item.nombre}</h3>
                        <span class="text-[10px] font-mono text-slate-400 uppercase font-bold tracking-wider block mt-1">${item.sku}</span>
                    </div>
                    ${controlsHtml}
                </div>
            `;
"""

SYNC_NAVBAR_CART_JS = """
<script>
// Sincronización automática de contador y drawer de carrito
function syncGlobalCartState() {
    try {
        let cart = [];
        const raw = localStorage.getItem('ecosystem_global_cart');
        if (raw) cart = JSON.parse(raw);
        const activeItems = cart.filter(i => i && i.quantity > 0);
        const totalCount = activeItems.reduce((sum, i) => sum + (parseInt(i.quantity) || 0), 0);

        // Actualizar badges en la barra de navegación
        document.querySelectorAll('#cart-count, .cart-counter, [data-cart-count]').forEach(el => {
            el.innerText = totalCount;
            el.style.display = totalCount > 0 ? 'inline-flex' : 'none';
        });

        // Actualizar header 'MI CARRITO (X)'
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
"""

for store in STORES:
    store_dir = os.path.join(BASE_DIR, store)

    # 1. Parchear index.html con sincronizador de badge/drawer
    idx_path = os.path.join(store_dir, "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8") as f:
            idx_c = f.read()
        if "syncGlobalCartState" not in idx_c:
            idx_c = idx_c.replace("</body>", f"{SYNC_NAVBAR_CART_JS}\n</body>", 1)
            with open(idx_path, "w", encoding="utf-8") as f:
                f.write(idx_c)

    # 2. Parchear checkout.html con resolución inter-tiendas y 170px
    co_path = os.path.join(store_dir, "checkout.html")
    if os.path.exists(co_path):
        with open(co_path, "r", encoding="utf-8") as f:
            co_c = f.read()

        if "getGlobalProductImage" not in co_c:
            co_c = co_c.replace("</script>", f"{RESOLVE_IMG_JS}\n</script>", 1)

        co_c = re.sub(
            r'let\s+rowClass\s*=\s*[\'"][^\'"]*[\'"];[\s\S]*?container\.appendChild\(div\);',
            CHECKOUT_ROW_TEMPLATE.strip() + '\n            container.appendChild(div);',
            co_c
        )
        with open(co_path, "w", encoding="utf-8") as f:
            f.write(co_c)

print("Todas las boutiques actualizadas con resolución inter-tiendas.")
