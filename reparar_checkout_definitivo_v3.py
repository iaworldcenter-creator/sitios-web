import os, re, subprocess

BASE_DIR = r"E:\sitios web"
STORES = [
    "pc-custom-lab", "cigarros-bazar", "dulces-bazar",
    "kiosco-digital", "mi-puesto-bazar", "ofertas-y-liquidaciones",
    "bazar-viamx-nfl.gdl"
]

NEW_CART_ITEM_RENDER = '''
            let rowClass = "flex flex-row items-center gap-4 p-4 bg-slate-900/80 rounded-2xl border border-slate-800 mb-3 transition-all duration-300";
            let controlsHtml = "";
            let statusTagHtml = "";

            if (isInactive) {
                rowClass += " opacity-40 grayscale";
                statusTagHtml = <span class="bg-red-500/10 border border-red-500/30 text-red-500 font-bold px-2 py-0.5 rounded text-[9px] uppercase tracking-wider block mt-0.5 w-max">Desactivado</span>;
                controlsHtml = 
                    <button onclick="changeQty('', 1)" class="px-3 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-[11px] transition cursor-pointer flex items-center gap-1.5 active:scale-95 shadow-md">
                        Reactivar <i class="fa-solid fa-plus text-[10px]"></i>
                    </button>
                ;
            } else {
                let minusBtn = <button onclick="changeQty('', -1)" class="w-8 h-8 rounded-lg bg-slate-800 text-slate-300 hover:text-white transition flex items-center justify-center font-bold text-xs cursor-pointer">-</button>;
                if (item.quantity === 1) {
                    minusBtn = <button onclick="deleteItem('')" class="w-8 h-8 rounded-lg bg-red-950/80 text-red-400 hover:bg-red-900 hover:text-red-200 transition flex items-center justify-center text-xs cursor-pointer" title="Eliminar"><i class="fa-solid fa-trash-can"></i></button>;
                }
                controlsHtml = 
                    <div class="flex items-center gap-1.5 bg-slate-950 border border-slate-800 rounded-xl p-1">
                        
                        <span class="text-white font-black text-xs w-7 text-center font-mono"></span>
                        <button onclick="changeQty('', 1)" class="w-8 h-8 rounded-lg bg-slate-800 text-slate-300 hover:text-white transition flex items-center justify-center font-bold text-xs cursor-pointer">+</button>
                    </div>
                    <div class="flex flex-col items-end min-w-[75px]">
                        <span class="text-[10px] text-slate-400 font-semibold">E:\sitios web{parseFloat(item.precio).toLocaleString()} c/u</span>
                        <span class="text-cyan-400 font-black text-sm">E:\sitios web{sub.toFixed(2)} MXN</span>
                    </div>
                    <button onclick="deleteItem('')" class="text-slate-500 hover:text-red-400 text-sm cursor-pointer shrink-0 transition p-1.5 ml-1" title="Eliminar"><i class="fa-solid fa-trash-can"></i></button>
                ;
            }

            const div = document.createElement("div");
            div.className = rowClass;
            div.innerHTML = 
                <div class="w-[170px] h-[170px] min-w-[170px] max-w-[170px] rounded-2xl overflow-hidden bg-slate-950 border border-slate-700/80 shrink-0 p-1 flex items-center justify-center">
                    <img src="" class="w-full h-full object-cover rounded-xl" alt="" loading="lazy" onerror="this.src='assets/img/slider_ia_human.webp';" />
                </div>
                <div class="flex-1 flex flex-col gap-2 min-w-0">
                    <span class="text-white font-bold text-sm leading-snug"></span>
                    <span class="text-[10px] font-mono text-slate-400 uppercase font-bold tracking-wider"></span>
                    
                    <div class="flex items-center gap-3 flex-wrap mt-1">
                        
                    </div>
                </div>
            ;
'''

URL_SKU_HANDLER = '''
        // Captura automática de producto desde parámetro URL (?sku=...)
        try {
            const urlParams = new URLSearchParams(window.location.search);
            const skuParam = urlParams.get('sku');
            if (skuParam) {
                let cart = getCart();
                let existingItem = cart.find(i => i.sku.toUpperCase() === skuParam.toUpperCase());
                if (existingItem) {
                    if (existingItem.quantity === 0) {
                        existingItem.quantity = 1;
                        saveCart(cart);
                    }
                } else if (typeof productCatalog !== 'undefined' && Array.isArray(productCatalog)) {
                    const product = productCatalog.find(p => p.sku.toUpperCase() === skuParam.toUpperCase());
                    if (product) {
                        cart.push({
                            sku: product.sku,
                            nombre: product.nombre,
                            precio: product.precio,
                            imagen: product.imagen,
                            quantity: 1
                        });
                        saveCart(cart);
                    }
                }
            }
        } catch(e) { console.warn("Error capturando SKU de URL:", e); }
'''

for store in STORES:
    store_dir = os.path.join(BASE_DIR, store)
    
    # 1. Limpiar auto-resets residuales de index.html y checkout.html
    for page in ["index.html", "producto.html", "checkout.html"]:
        p_path = os.path.join(store_dir, page)
        if os.path.exists(p_path):
            with open(p_path, "r", encoding="utf-8") as f:
                c = f.read()
            c = re.sub(r'<script>[\s\S]*?ecosystem_reset_v2026_clean[\s\S]*?</script>', '', c)
            with open(p_path, "w", encoding="utf-8") as f:
                f.write(c)

    # 2. Inyectar renderizado y captura de URL en checkout.html
    co_path = os.path.join(store_dir, "checkout.html")
    if os.path.exists(co_path):
        with open(co_path, "r", encoding="utf-8") as f:
            co_html = f.read()
            
        # Reemplazar la sección de render de producto
        co_html = re.sub(
            r'let\s+rowClass\s*=\s*[\'"][^\'"]*[\'"];[\s\S]*?container\.appendChild\(div\);',
            NEW_CART_ITEM_RENDER.strip() + '\n            container.appendChild(div);',
            co_html
        )
        
        # Inyectar captura de SKU antes de renderCheckout()
        if "urlParams.get('sku')" not in co_html:
            co_html = co_html.replace("renderCheckout();", URL_SKU_HANDLER + "\n        renderCheckout();", 1)
            
        with open(co_path, "w", encoding="utf-8") as f:
            f.write(co_html)

print("Todas las boutiques han sido actualizadas localmente.")
