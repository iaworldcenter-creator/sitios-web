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

ACCORDION_AND_CLEAN_CHECKOUT_JS = """
<script>
// ==========================================
// MOTOR DE CHECKOUT INTELIGENTE Y CARRITO LIMPIO
// ==========================================

function getGlobalCart() {
    try {
        const raw = localStorage.getItem('ecosystem_global_cart');
        if (!raw) return [];
        let parsed = JSON.parse(raw);
        // Filtrado estricto: Solo productos válidos con cantidad >= 1
        return Array.isArray(parsed) ? parsed.filter(item => item && parseInt(item.quantity) > 0) : [];
    } catch(e) {
        return [];
    }
}

function saveGlobalCart(cart) {
    const cleanCart = cart.filter(item => item && parseInt(item.quantity) > 0);
    localStorage.setItem('ecosystem_global_cart', JSON.stringify(cleanCart));
    window.dispatchEvent(new Event('storage'));
}

function resolveProductImage(sku, localImg) {
    if (localImg && (localImg.startsWith('http://') || localImg.startsWith('https://'))) return localImg;
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

// 1. ELIMINACIÓN Y MODIFICACIÓN ESTRICTA
window.deleteItem = function(sku) {
    let cart = getGlobalCart();
    cart = cart.filter(i => i.sku.toUpperCase() !== sku.toUpperCase());
    saveGlobalCart(cart);
    renderSmartCheckout();
};

window.changeQty = function(sku, delta) {
    let cart = getGlobalCart();
    let item = cart.find(i => i.sku.toUpperCase() === sku.toUpperCase());
    if (item) {
        item.quantity = (parseInt(item.quantity) || 1) + delta;
        if (item.quantity <= 0) {
            cart = cart.filter(i => i.sku.toUpperCase() !== sku.toUpperCase());
        }
    }
    saveGlobalCart(cart);
    renderSmartCheckout();
};

// 2. ACORDEÓN PASO 1: DOMICILIO DE ENTREGA
window.guardarDomicilio = function(e) {
    if (e) e.preventDefault();
    const nombre = document.getElementById('input-nombre')?.value || document.querySelector('input[placeholder*="Juan"]')?.value || 'Cliente General';
    const tel = document.getElementById('input-tel')?.value || document.querySelector('input[placeholder*="33"]')?.value || '';
    const calle = document.getElementById('input-calle')?.value || document.querySelector('input[placeholder*="Moreno"]')?.value || 'Av. Pedro Moreno';
    const col = document.getElementById('input-colonia')?.value || 'Centro';
    const cd = document.getElementById('input-ciudad')?.value || 'Guadalajara';

    const shippingData = { nombre, tel, calle, col, cd, guardado: true };
    localStorage.setItem('ecosystem_shipping_data', JSON.stringify(shippingData));
    toggleDomicilioView(true);
};

window.toggleDomicilioView = function(colapsar) {
    const formBox = document.querySelector('[data-step="1-form"]') || document.getElementById('step-1-form');
    const summaryBox = document.querySelector('[data-step="1-summary"]') || document.getElementById('step-1-summary');
    if (formBox && summaryBox) {
        if (colapsar) {
            formBox.classList.add('hidden');
            summaryBox.classList.remove('hidden');
            const data = JSON.parse(localStorage.getItem('ecosystem_shipping_data') || '{}');
            summaryBox.innerHTML = `
                <div class="flex items-center justify-between p-3.5 bg-slate-900/90 border border-slate-800 rounded-xl text-xs">
                    <div class="flex items-center gap-2.5 min-w-0">
                        <i class="fa-solid fa-location-dot text-amber-400 text-sm"></i>
                        <div class="truncate text-slate-200">
                            <strong>${data.nombre || 'Datos guardados'}</strong> &bull; ${data.calle || ''}, ${data.col || ''} (${data.tel || ''})
                        </div>
                    </div>
                    <button onclick="toggleDomicilioView(false)" class="text-cyan-400 hover:text-cyan-300 font-bold ml-2 underline cursor-pointer shrink-0">Editar</button>
                </div>
            `;
        } else {
            formBox.classList.remove('hidden');
            summaryBox.classList.add('hidden');
        }
    }
};

// 3. ACORDEÓN PASO 2: FORMA DE PAGO
window.seleccionarPago = function(metodo) {
    localStorage.setItem('ecosystem_payment_method', metodo);
    togglePagoView(true);
};

window.togglePagoView = function(colapsar) {
    const formBox = document.querySelector('[data-step="2-form"]') || document.getElementById('step-2-form');
    const summaryBox = document.querySelector('[data-step="2-summary"]') || document.getElementById('step-2-summary');
    if (formBox && summaryBox) {
        if (colapsar) {
            formBox.classList.add('hidden');
            summaryBox.classList.remove('hidden');
            const metodo = localStorage.getItem('ecosystem_payment_method') || 'Tarjeta de Crédito / Débito';
            summaryBox.innerHTML = `
                <div class="flex items-center justify-between p-3.5 bg-slate-900/90 border border-slate-800 rounded-xl text-xs">
                    <div class="flex items-center gap-2.5">
                        <i class="fa-solid fa-credit-card text-emerald-400 text-sm"></i>
                        <span class="text-slate-200">Método: <strong>${metodo}</strong></span>
                    </div>
                    <button onclick="togglePagoView(false)" class="text-cyan-400 hover:text-cyan-300 font-bold ml-2 underline cursor-pointer shrink-0">Editar</button>
                </div>
            `;
        } else {
            formBox.classList.remove('hidden');
            summaryBox.classList.add('hidden');
        }
    }
};

// 4. RENDERIZADO DEL CHECKOUT Y TOTALES
window.renderSmartCheckout = function() {
    const cart = getGlobalCart();
    const container = document.getElementById('cart-items-container') || document.querySelector('[data-cart-container]');
    const countBadge = document.querySelector('[data-item-count]') || document.getElementById('cart-count-badge');
    
    const totalItems = cart.reduce((sum, i) => sum + (parseInt(i.quantity) || 0), 0);
    if (countBadge) countBadge.innerText = `${totalItems} producto${totalItems === 1 ? '' : 's'}`;

    if (!container) return;
    container.innerHTML = '';

    if (cart.length === 0) {
        container.innerHTML = `
            <div class="text-center py-12 px-4 bg-slate-900/40 border border-slate-800/80 rounded-2xl">
                <i class="fa-solid fa-cart-shopping text-4xl text-slate-600 mb-3 block"></i>
                <p class="text-slate-400 font-semibold text-sm">Tu carrito está vacío.</p>
                <a href="index.html" class="inline-block mt-4 px-6 py-2.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-black rounded-xl text-xs uppercase tracking-wider transition">Explorar catálogo</a>
            </div>
        `;
        actualizarTotales(0, 0);
        return;
    }

    let subtotal = 0;
    cart.forEach(item => {
        const itemSub = (parseFloat(item.precio) || 0) * (parseInt(item.quantity) || 1);
        subtotal += itemSub;
        const imgUrl = resolveProductImage(item.sku, item.imagen);

        const minusBtn = item.quantity === 1 
            ? `<button onclick="deleteItem('${item.sku}')" class="w-8 h-8 rounded-lg bg-red-950/80 text-red-400 hover:bg-red-900 transition flex items-center justify-center text-xs cursor-pointer" title="Eliminar"><i class="fa-solid fa-trash-can"></i></button>`
            : `<button onclick="changeQty('${item.sku}', -1)" class="w-8 h-8 rounded-lg bg-slate-800 text-slate-300 hover:text-white transition flex items-center justify-center font-bold text-xs cursor-pointer">-</button>`;

        const div = document.createElement('div');
        div.className = "flex flex-col sm:flex-row items-center sm:items-stretch gap-4 p-4 bg-slate-900 border border-slate-800 rounded-2xl mb-3 shadow-md transition-all";
        div.innerHTML = `
            <div class="w-[170px] h-[170px] min-w-[170px] max-w-[170px] min-h-[170px] max-h-[170px] rounded-xl overflow-hidden bg-slate-950 border border-slate-700/80 shrink-0 p-2 flex items-center justify-center">
                <img src="${imgUrl}" class="w-full h-full object-contain rounded-lg" alt="${item.nombre}" loading="lazy" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp';" />
            </div>
            <div class="flex-1 flex flex-col justify-between min-w-0 w-full py-1">
                <div>
                    <h3 class="text-white font-bold text-sm sm:text-base leading-snug">${item.nombre}</h3>
                    <span class="text-[10px] font-mono text-slate-400 uppercase font-bold tracking-wider block mt-1">${item.sku}</span>
                </div>
                <div class="flex items-center justify-between w-full mt-3 pt-3 border-t border-slate-800">
                    <div class="flex items-center gap-1.5 bg-slate-950 border border-slate-800 rounded-xl p-1">
                        ${minusBtn}
                        <span class="text-white font-black text-xs w-7 text-center font-mono">${item.quantity}</span>
                        <button onclick="changeQty('${item.sku}', 1)" class="w-8 h-8 rounded-lg bg-slate-800 text-slate-300 hover:text-white transition flex items-center justify-center font-bold text-xs cursor-pointer">+</button>
                    </div>
                    <div class="flex flex-col items-end">
                        <span class="text-[10px] text-slate-400 font-semibold">$${parseFloat(item.precio).toLocaleString()} c/u</span>
                        <span class="text-cyan-400 font-black text-sm">$${itemSub.toFixed(2)} MXN</span>
                    </div>
                    <button onclick="deleteItem('${item.sku}')" class="text-slate-500 hover:text-red-400 text-sm cursor-pointer shrink-0 transition p-1.5 ml-1" title="Eliminar"><i class="fa-solid fa-trash-can"></i></button>
                </div>
            </div>
        `;
        container.appendChild(div);
    });

    actualizarTotales(subtotal, totalItems);
};

function actualizarTotales(subtotal, totalItems) {
    const envio = subtotal >= 1500 || subtotal === 0 ? 0 : 49;
    const mayoreoDesc = totalItems >= 10 ? subtotal * 0.15 : 0;
    const subConDescuento = subtotal - mayoreoDesc;
    const total = subConDescuento > 0 ? subConDescuento + envio : 0;
    const cashback = subConDescuento * 0.05;

    document.querySelectorAll('[data-subtotal]').forEach(el => el.innerText = `$${subtotal.toFixed(2)} MXN`);
    document.querySelectorAll('[data-envio]').forEach(el => el.innerText = envio === 0 ? 'GRATIS' : `$${envio.toFixed(2)} MXN`);
    document.querySelectorAll('[data-total]').forEach(el => el.innerText = `$${total.toFixed(2)} MXN`);
    document.querySelectorAll('[data-cashback]').forEach(el => el.innerText = `$${cashback.toFixed(2)} MXN`);
}

document.addEventListener('DOMContentLoaded', () => {
    // Si viene SKU por URL, agregarlo antes de pintar
    const urlParams = new URLSearchParams(window.location.search);
    const skuParam = urlParams.get('sku');
    if (skuParam) {
        let cart = getGlobalCart();
        let existing = cart.find(i => i.sku.toUpperCase() === skuParam.toUpperCase());
        if (!existing) {
            let prod = (typeof productCatalog !== 'undefined') ? productCatalog.find(p => p.sku.toUpperCase() === skuParam.toUpperCase()) : null;
            if (prod) {
                cart.push({ ...prod, quantity: 1 });
            } else {
                cart.push({ sku: skuParam, nombre: 'Producto ' + skuParam, precio: 100, imagen: '', quantity: 1 });
            }
            saveGlobalCart(cart);
        }
    }

    renderSmartCheckout();

    // Comprobar si ya había datos guardados para iniciar colapsado
    const savedShipping = localStorage.getItem('ecosystem_shipping_data');
    if (savedShipping) toggleDomicilioView(true);
    const savedPayment = localStorage.getItem('ecosystem_payment_method');
    if (savedPayment) togglePagoView(true);
});
</script>
"""

def patch_checkout(store):
    filepath = os.path.join(BASE_DIR, store, "checkout.html")
    if not os.path.exists(filepath):
        return

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # Estructurar contenedores de acordeón en Paso 1 y Paso 2 si no existen
    if 'id="step-1-summary"' not in html and 'data-step="1-summary"' not in html:
        html = re.sub(
            r'(<div[^>]*class="[^"]*p-6[^"]*bg-slate-900[^"]*"[^>]*>\s*<h2[^>]*>.*?Domicilio.*?</h2>)([\s\S]*?)(</div>\s*<div[^>]*class="[^"]*p-6)',
            r'\1\n<div id="step-1-summary" class="hidden mt-3"></div>\n<div id="step-1-form">\2</div>\n</div>\n\3',
            html,
            count=1,
            flags=re.IGNORECASE
        )

    # Inyectar motor JS
    if "renderSmartCheckout" not in html:
        html = html.replace("</body>", f"{ACCORDION_AND_CLEAN_CHECKOUT_JS}\n</body>", 1)
    else:
        html = re.sub(r'<script>[\s\S]*?renderSmartCheckout[\s\S]*?</script>', ACCORDION_AND_CLEAN_CHECKOUT_JS, html)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Checkout optimizado en: {store}")

def execute_pipeline():
    print("=== 1. APLICANDO CHECKOUT ACORDEÓN Y LIMPIEZA DE CARRITO ===")
    for store in STORES:
        patch_checkout(store)

    print("\n=== 2. DESPLIEGUE GIT MASIVO ===")
    for store in STORES:
        store_dir = os.path.join(BASE_DIR, store)
        if os.path.exists(os.path.join(store_dir, ".git")):
            subprocess.run(["git", "add", "-A"], cwd=store_dir, check=True)
            subprocess.run(["git", "commit", "-m", "fix(checkout): acordeon interactivo y purga total de eliminados", "--allow-empty"], cwd=store_dir, capture_output=True)
            subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=store_dir, capture_output=True)
            print(f"🟢 Push OK: {store}")

    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(checkout): flujo ultra compacto con acordeon y productos activos", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
    subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True)
    print("🟢 Push OK: Repositorio Raíz (sitios web)")

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    execute_pipeline()
