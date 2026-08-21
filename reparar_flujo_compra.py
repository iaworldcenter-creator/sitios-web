import os, re, subprocess

BASE_DIR = r"E:\sitios web"
STORES = [
    "pc-custom-lab", "cigarros-bazar", "dulces-bazar",
    "kiosco-digital", "mi-puesto-bazar", "ofertas-y-liquidaciones",
    "bazar-viamx-nfl.gdl"
]

CHECKOUT_SKU_LOADER = '''
        // Lector y auto-insertador de SKU desde URL (?sku=...)
        try {
            const urlParams = new URLSearchParams(window.location.search);
            const skuParam = urlParams.get('sku');
            if (skuParam) {
                let cart = getCart();
                let item = cart.find(i => i.sku && i.sku.toUpperCase() === skuParam.toUpperCase());
                if (!item) {
                    let prod = (typeof productCatalog !== 'undefined') ? productCatalog.find(p => p.sku && p.sku.toUpperCase() === skuParam.toUpperCase()) : null;
                    if (prod) {
                        cart.push({ ...prod, quantity: 1 });
                    } else {
                        cart.push({ sku: skuParam, nombre: 'Producto ' + skuParam, precio: 100, imagen: '', quantity: 1 });
                    }
                    localStorage.setItem("ecosystem_global_cart", JSON.stringify(cart));
                } else if (item.quantity === 0) {
                    item.quantity = 1;
                    localStorage.setItem("ecosystem_global_cart", JSON.stringify(cart));
                }
            }
        } catch(e) { console.warn("Error cargando SKU URL:", e); }
'''

BUY_NOW_HANDLER = '''
<script>
window.comprarAhora = function() {
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const sku = urlParams.get('sku');
        if (sku && typeof addToCart === 'function') {
            addToCart(sku);
        }
        window.location.href = 'checkout.html' + (sku ? '?sku=' + encodeURIComponent(sku) : '');
    } catch(e) {
        window.location.href = 'checkout.html';
    }
};
</script>
'''

for store in STORES:
    store_dir = os.path.join(BASE_DIR, store)
    
    # 1. Conectar botón Pagar Ahora en producto.html
    prod_path = os.path.join(store_dir, "producto.html")
    if os.path.exists(prod_path):
        with open(prod_path, "r", encoding="utf-8") as f:
            p_html = f.read()
            
        if "window.comprarAhora" not in p_html:
            p_html = p_html.replace("</body>", f"{BUY_NOW_HANDLER}\n</body>", 1)
            
        # Reemplazar botones de pagar ahora
        p_html = re.sub(
            r'<(?:a|button)[^>]*?(?:checkout\.html|comprarAhoraDirecto)[^>]*?>\s*(?:<[^>]+>\s*)*[Pp]agar\s+[Aa]hora[\s\S]*?</(?:a|button)>',
            r'<button onclick="comprarAhora()" class="w-full bg-amber-500 hover:bg-amber-400 text-slate-950 font-black py-3.5 rounded-xl text-xs uppercase tracking-wider transition cursor-pointer flex items-center justify-center gap-2 active:scale-95 shadow-md">Pagar ahora <i class="fa-solid fa-credit-card"></i></button>',
            p_html
        )
        with open(prod_path, "w", encoding="utf-8") as f:
            f.write(p_html)

    # 2. Inyectar captura de SKU en checkout.html
    co_path = os.path.join(store_dir, "checkout.html")
    if os.path.exists(co_path):
        with open(co_path, "r", encoding="utf-8") as f:
            co_html = f.read()
            
        # Inyectar justo antes de renderCheckout() en DOMContentLoaded
        if "skuParam" not in co_html:
            co_html = co_html.replace("renderCheckout();", f"{CHECKOUT_SKU_LOADER}\n        renderCheckout();", 1)
            
        with open(co_path, "w", encoding="utf-8") as f:
            f.write(co_html)

print("Todas las boutiques actualizadas con flujo de compra enlazado.")
