import os, re, subprocess

BASE_DIR = r"E:\sitios web"
STORES = [
    "pc-custom-lab", "cigarros-bazar", "dulces-bazar",
    "kiosco-digital", "mi-puesto-bazar", "ofertas-y-liquidaciones",
    "bazar-viamx-nfl.gdl"
]

BUY_NOW_JS = '''
// Función de compra directa desde producto individual
window.comprarAhoraDirecto = function() {
    const urlParams = new URLSearchParams(window.location.search);
    const sku = urlParams.get('sku');
    
    if (sku) {
        let cart = [];
        try {
            const stored = localStorage.getItem("ecosystem_global_cart");
            if (stored) cart = JSON.parse(stored);
        } catch(e) {}
        
        const existing = cart.find(item => item.sku === sku);
        if (existing) {
            if (!existing.quantity || existing.quantity < 1) existing.quantity = 1;
        } else {
            let prodObj = null;
            if (typeof productCatalog !== 'undefined') {
                prodObj = productCatalog.find(p => p.sku === sku);
            }
            if (prodObj) {
                cart.push({ ...prodObj, quantity: 1 });
            } else {
                const titleEl = document.querySelector('h1') || document.querySelector('h2');
                const priceEl = document.querySelector('[data-precio]') || document.querySelector('.text-amber-400');
                const name = titleEl ? titleEl.innerText.trim() : 'Producto ' + sku;
                let price = 100;
                if (priceEl) {
                    const cleanP = priceEl.innerText.replace(/[^0-9.]/g, '');
                    if (cleanP) price = parseFloat(cleanP);
                }
                cart.push({ sku: sku, nombre: name, precio: price, quantity: 1, imagen: '' });
            }
        }
        localStorage.setItem("ecosystem_global_cart", JSON.stringify(cart));
    }
    window.location.href = "checkout.html";
};
'''

for store in STORES:
    store_dir = os.path.join(BASE_DIR, store)
    prod_path = os.path.join(store_dir, "producto.html")
    
    if os.path.exists(prod_path):
        with open(prod_path, "r", encoding="utf-8") as f:
            html = f.read()
            
        # 1. Inyectar función comprarAhoraDirecto si no existe
        if "window.comprarAhoraDirecto" not in html:
            html = html.replace("</script>", f"{BUY_NOW_JS}\n</script>", 1)
            
        # 2. Reemplazar enlaces o botones de 'Pagar ahora'
        html = re.sub(
            r'<a[^>]*href=["\'](?:checkout\.html|\#)["\'][^>]*>(.*?[Pp]agar\s+[Aa]hora.*?)</a>',
            r'<button onclick="comprarAhoraDirecto()" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-black py-3 rounded-xl text-xs uppercase tracking-wider transition active:scale-95 cursor-pointer w-full flex items-center justify-center gap-2">\1</button>',
            html,
            flags=re.IGNORECASE
        )
        
        html = re.sub(
            r'<button[^>]*onclick=["\'][^"\']*(?:checkout|window\.location)[^"\']*["\'][^>]*>(.*?[Pp]agar\s+[Aa]hora.*?)</button>',
            r'<button onclick="comprarAhoraDirecto()" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-black py-3 rounded-xl text-xs uppercase tracking-wider transition active:scale-95 cursor-pointer w-full flex items-center justify-center gap-2">\1</button>',
            html,
            flags=re.IGNORECASE
        )
        
        with open(prod_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[OK] {store}/producto.html -> Pagar ahora conectado a compra directa.")

print("Todas las boutiques actualizadas con flujo de compra directa.")
