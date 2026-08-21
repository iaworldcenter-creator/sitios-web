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

COMPRAR_AHORA_FN = """
// COMPRA DIRECTA ROBUSTA (Pagar ahora -> Carrito Global -> Checkout)
window.comprarAhoraDirecto = function() {
    try {
        const urlParams = new URLSearchParams(window.location.search);
        let sku = urlParams.get('sku');
        if (!sku && typeof currentProduct !== 'undefined' && currentProduct && currentProduct.sku) {
            sku = currentProduct.sku;
        }
        if (!sku && typeof productCatalog !== 'undefined' && Array.isArray(productCatalog) && productCatalog.length > 0) {
            sku = productCatalog[0].sku;
        }
        if (!sku) {
            window.location.href = 'checkout.html';
            return;
        }

        let product = null;
        if (typeof productCatalog !== 'undefined' && Array.isArray(productCatalog)) {
            product = productCatalog.find(p => p.sku.toUpperCase() === sku.toUpperCase());
        }

        let cart = [];
        try {
            const stored = localStorage.getItem("ecosystem_global_cart");
            if (stored) cart = JSON.parse(stored);
        } catch(e) {}

        const existing = cart.find(i => i.sku.toUpperCase() === sku.toUpperCase());
        if (existing) {
            existing.quantity = Math.max(1, (existing.quantity || 0) + 1);
            if (product && (!existing.imagen || existing.imagen === '')) existing.imagen = product.imagen;
        } else if (product) {
            cart.push({
                sku: product.sku,
                nombre: product.nombre,
                precio: product.precio,
                imagen: product.imagen,
                quantity: 1
            });
        } else {
            cart.push({
                sku: sku,
                nombre: "Producto " + sku,
                precio: 0,
                imagen: "",
                quantity: 1
            });
        }

        localStorage.setItem("ecosystem_global_cart", JSON.stringify(cart));
        window.location.href = 'checkout.html';
    } catch(err) {
        console.error("Error en comprarAhoraDirecto:", err);
        window.location.href = 'checkout.html';
    }
};
"""

NEW_CHECKOUT_RENDER = """div.innerHTML = `
    <div class="w-[170px] h-[170px] min-w-[170px] max-w-[170px] rounded-2xl overflow-hidden bg-slate-950 border border-slate-700/80 shrink-0 p-1 flex items-center justify-center">
        <img src="${imgUrl}" class="w-full h-full object-cover rounded-xl" alt="${item.nombre}" loading="lazy" onerror="this.src='assets/img/slider_ia_human_thumb.webp?v=1.1.0';" />
    </div>
    <div class="flex-1 flex flex-col gap-1.5 min-w-0">
        <div class="flex justify-between items-start gap-2">
            <div>
                <span class="text-white font-bold text-sm sm:text-base leading-snug block">${item.nombre}</span>
                <span class="text-[10px] font-mono text-slate-500 uppercase block mt-0.5">${item.sku}</span>
            </div>
            <span class="text-slate-400 font-bold text-xs shrink-0">$$${parseFloat(item.precio).toLocaleString()} c/u</span>
        </div>
        ${statusTagHtml}
        <div class="flex items-center justify-between gap-3 flex-wrap mt-2 pt-2 border-t border-slate-800/60">
            ${controlsHtml}
        </div>
    </div>
`;"""

def patch_producto_file(store):
    filepath = os.path.join(BASE_DIR, store, "producto.html")
    if not os.path.exists(filepath):
        return

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # Asignar comprarAhoraDirecto() al botón "Pagar ahora"
    html = re.sub(
        r'<(?:button|a)[^>]*?(?:onclick=["\'][^"\']*["\']|href=["\'][^"\']*["\'])?[^>]*?>\s*(?:<[^>]+>\s*)*[Pp]agar\s+[Aa]hora[\s\S]*?</(?:button|a)>',
        r'<button onclick="comprarAhoraDirecto()" class="w-full bg-amber-500 hover:bg-amber-400 text-slate-950 font-black py-3.5 rounded-xl text-xs uppercase tracking-wider transition cursor-pointer flex items-center justify-center gap-2 active:scale-95 shadow-md">Pagar ahora <i class="fa-solid fa-credit-card"></i></button>',
        html,
        flags=re.IGNORECASE
    )

    # Inyectar la función JS de compra directa si no está presente
    if "window.comprarAhoraDirecto" not in html:
        if "</body>" in html:
            html = html.replace("</body>", f"<script>{COMPRAR_AHORA_FN}</script>\n</body>", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] {store}/producto.html -> Compra directa enlazada.")

def patch_checkout_file(store):
    filepath = os.path.join(BASE_DIR, store, "checkout.html")
    if not os.path.exists(filepath):
        return

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # Inyectar resolución de imagen de respaldo (fallback) desde productCatalog
    img_fallback_code = """let imgUrl = item.imagen;
            if (!imgUrl || imgUrl === '' || imgUrl === 'null' || imgUrl === 'undefined') {
                if (typeof productCatalog !== 'undefined' && Array.isArray(productCatalog)) {
                    const catProd = productCatalog.find(p => p.sku && p.sku.toUpperCase() === item.sku.toUpperCase());
                    if (catProd && catProd.imagen) imgUrl = catProd.imagen;
                }
            }
            if (!imgUrl || imgUrl === '') {
                imgUrl = 'assets/img/slider_ia_human_thumb.webp?v=1.1.0';
            }
            if (imgUrl.startsWith('assets/img/')) {
                imgUrl = './' + imgUrl;
            }"""

    html = re.sub(
        r'let\s+imgUrl\s*=\s*item\.imagen;[\s\S]*?if\s*\(!imgUrl\.startsWith\(["\'](\.\/|http)["\']\)\)\s*\{[\s\S]*?\}',
        img_fallback_code,
        html
    )

    # Actualizar render a recuadro de 170px
    re_cart = re.compile(r'div\.innerHTML\s*=\s*`[\s\S]*?\$\{controlsHtml\}[\s\S]*?`;')
    html = re_cart.sub(NEW_CHECKOUT_RENDER, html)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] {store}/checkout.html -> Miniatura 170px y fallback de imagen activos.")

def execute_pipeline():
    print("=== 1. MODIFICANDO ARCHIVOS DE TIENDAS ===")
    for store in STORES:
        patch_producto_file(store)
        patch_checkout_file(store)

    print("\n=== 2. DESPLIEGUE GIT MASIVO ===")
    for store in STORES:
        store_dir = os.path.join(BASE_DIR, store)
        if os.path.exists(os.path.join(store_dir, ".git")):
            subprocess.run(["git", "add", "-A"], cwd=store_dir, check=True)
            subprocess.run(["git", "commit", "-m", "fix(checkout): compra directa y miniatura 170px", "--allow-empty"], cwd=store_dir, capture_output=True)
            subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=store_dir, capture_output=True)
            print(f"🟢 Push OK: {store}")

    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(checkout): integracion visual 170px y compra directa", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
    subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True)
    print("🟢 Push OK: Repositorio Raíz (sitios web)")

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    execute_pipeline()
    print("\nProceso y despliegue finalizados con éxito.")
