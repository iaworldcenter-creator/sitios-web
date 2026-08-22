import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
PC_INDEX_PATH = os.path.join(BASE_DIR, "pc-custom-lab", "index.html")

CART_LOGIC_CORREGIDA = """
// ========================================================================
// SISTEMA DE CARRITO GLOBAL UNIFICADO Y SINCRONIZACIÓN EN TIEMPO REAL
// ========================================================================
function getCart() {
    try {
        const stored = localStorage.getItem("ecosystem_global_cart");
        const parsed = stored ? JSON.parse(stored) : [];
        return Array.isArray(parsed) ? parsed.filter(i => i && (parseInt(i.quantity) || 0) > 0) : [];
    } catch(e) {
        return [];
    }
}

function saveCart(cart) {
    const cleanCart = Array.isArray(cart) ? cart.filter(i => i && (parseInt(i.quantity) || 0) > 0) : [];
    localStorage.setItem("ecosystem_global_cart", JSON.stringify(cleanCart));
    updateCartBadge();
    syncGlobalCartState();
    window.dispatchEvent(new Event('storage'));
}

function updateCartBadge() {
    const cart = getCart();
    const totalQty = cart.reduce((sum, item) => sum + (parseInt(item.quantity) || 0), 0);
    
    const badge = document.getElementById("cart-badge-count");
    if (badge) badge.innerText = totalQty;
    
    const badgeMobile = document.getElementById("cart-badge-count-mobile");
    if (badgeMobile) badgeMobile.innerText = totalQty;
}

function syncGlobalCartState() {
    try {
        const cart = getCart();
        const totalCount = cart.reduce((sum, i) => sum + (parseInt(i.quantity) || 0), 0);

        document.querySelectorAll('#cart-badge-count, #cart-count, .cart-counter, [data-cart-count]').forEach(el => {
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

window.addToCart = function(sku) {
    const prod = (typeof productCatalog !== 'undefined') ? productCatalog.find(p => p.sku === sku) : null;
    let cart = getCart();
    const existing = cart.find(item => item.sku === sku);
    
    if (existing) {
        existing.quantity = (parseInt(existing.quantity) || 1) + 1;
    } else if (prod) {
        cart.push({...prod, quantity: 1});
    } else {
        cart.push({ sku: sku, nombre: 'Producto ' + sku, precio: 100, imagen: '', quantity: 1 });
    }
    
    saveCart(cart);
    openCartDrawer();
};

window.removeFromCart = function(sku) {
    let cart = getCart();
    cart = cart.filter(item => item.sku !== sku);
    saveCart(cart);
    renderDrawerCart();
};

window.changeQuantity = function(sku, amount) {
    let cart = getCart();
    const item = cart.find(i => i.sku === sku);
    if (item) {
        item.quantity = (parseInt(item.quantity) || 1) + amount;
        if (item.quantity <= 0) {
            cart = cart.filter(i => i.sku !== sku);
        }
    }
    saveCart(cart);
    renderDrawerCart();
};

window.renderDrawerCart = function() {
    const container = document.getElementById("drawer-cart-items");
    const subtotalDisplay = document.getElementById("drawer-subtotal");
    const totalQtyDisplay = document.getElementById("drawer-total-qty");
    const totalCostDisplay = document.getElementById("drawer-total-cost");
    if (!container) return;
    
    const cart = getCart();
    container.innerHTML = "";
    
    if (cart.length === 0) {
        container.innerHTML = `<div class="text-center py-12 text-slate-500"><i class="fa-solid fa-cart-flatbed text-4xl mb-3 block opacity-40"></i><p class="text-xs font-semibold">Tu carrito está vacío.</p></div>`;
        if (subtotalDisplay) subtotalDisplay.innerText = "$0.00 MXN";
        if (totalQtyDisplay) totalQtyDisplay.innerText = "0";
        if (totalCostDisplay) totalCostDisplay.innerText = "$0.00 MXN";
        return;
    }
    
    let subtotal = 0;
    let totalItems = 0;

    cart.forEach(item => {
        const price = parseFloat(item.precio) || 0;
        const qty = parseInt(item.quantity) || 1;
        subtotal += price * qty;
        totalItems += qty;
        
        const div = document.createElement("div");
        div.className = "flex items-center gap-3.5 bg-slate-950 border border-slate-800/80 rounded-2xl p-3 shadow-md";
        div.innerHTML = `
            <div class="w-12 h-16 rounded-lg overflow-hidden bg-slate-900 border border-slate-800 shrink-0">
                <img loading="lazy" src="${item.imagen || ''}" alt="${item.nombre}" class="w-full h-full object-contain p-1 bg-slate-950" onerror="this.src='assets/img/slider_ia_human_thumb.webp'">
            </div>
            <div class="flex-1 flex flex-col justify-between min-h-[50px]">
                <div class="flex justify-between items-start gap-1">
                    <h4 class="text-[11px] font-black text-white leading-tight line-clamp-2">${item.nombre}</h4>
                    <button onclick="removeFromCart('${item.sku}')" class="text-slate-500 hover:text-red-400 text-xs cursor-pointer p-1" title="Eliminar"><i class="fa-solid fa-trash-can"></i></button>
                </div>
                <div class="flex justify-between items-center mt-1">
                    <span class="text-xs font-black text-amber-400">$${price.toFixed(2)}</span>
                    <div class="flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-lg px-2 py-0.5">
                        <button onclick="changeQuantity('${item.sku}', -1)" class="text-[10px] text-slate-400 hover:text-white cursor-pointer px-1">-</button>
                        <span class="text-[11px] font-mono font-bold w-4 text-center text-slate-300">${qty}</span>
                        <button onclick="changeQuantity('${item.sku}', 1)" class="text-[10px] text-slate-400 hover:text-white cursor-pointer px-1">+</button>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(div);
    });
    
    if (subtotalDisplay) subtotalDisplay.innerText = `$${subtotal.toFixed(2)} MXN`;
    if (totalQtyDisplay) totalQtyDisplay.innerText = totalItems.toString();
    if (totalCostDisplay) totalCostDisplay.innerText = `$${subtotal.toFixed(2)} MXN`;
};

window.openCartDrawer = function() {
    const drawer = document.getElementById("cartDrawer");
    if (drawer) {
        drawer.style.setProperty("display", "block", "important");
        drawer.classList.remove("hidden");
        renderDrawerCart();
    }
};

window.closeCartDrawer = function() {
    const drawer = document.getElementById("cartDrawer");
    if (drawer) {
        drawer.style.setProperty("display", "none", "important");
        drawer.classList.add("hidden");
    }
};

window.toggleCartDrawer = function() {
    const drawer = document.getElementById("cartDrawer");
    if (drawer) {
        if (drawer.style.display === "block" && !drawer.classList.contains("hidden")) {
            closeCartDrawer();
        } else {
            openCartDrawer();
        }
    }
};
"""

def fix_cart():
    print("=" * 75)
    print("SANEANDO ESTADO DEL CARRITO Y BOTÓN DE BASURA EN PC CUSTOM LAB")
    print("=" * 75)

    if not os.path.exists(PC_INDEX_PATH):
        print(f"[Error] No se encontró {PC_INDEX_PATH}")
        return

    with open(PC_INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Reemplazar la lógica anterior del carrito por la versión robusta
    pattern_cart = r'function getCart\(\)[\s\S]*?window\.renderDrawerCart\s*=\s*function\(\)[\s\S]*?^\s*\};'
    if re.search(pattern_cart, content, flags=re.MULTILINE):
        content = re.sub(pattern_cart, CART_LOGIC_CORREGIDA, content, flags=re.MULTILINE)
    else:
        content = content.replace("</script>", f"{CART_LOGIC_CORREGIDA}\n</script>")

    # 2. Asegurar que syncGlobalCartState() se ejecute en DOMContentLoaded y storage
    init_call = """
    document.addEventListener('DOMContentLoaded', () => {
        updateCartBadge();
        syncGlobalCartState();
    });
    window.addEventListener('storage', () => {
        updateCartBadge();
        syncGlobalCartState();
        if (typeof renderDrawerCart === 'function') renderDrawerCart();
    });
    """
    if "updateCartBadge();\n        syncGlobalCartState();" not in content:
        content = content.replace("</body>", f"<script>{init_call}</script>\n</body>")

    with open(PC_INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("✓ Lógica de carrito unificada y purga de artículos fantasma corregida.")

def deploy():
    print("\n" + "=" * 75)
    print("SUBIENDO CORRECCIÓN A GITHUB PAGES (-C GC.AUTO=0)")
    print("=" * 75)
    pc_dir = os.path.join(BASE_DIR, "pc-custom-lab")
    subprocess.run(["git", "add", "-A"], cwd=pc_dir, check=True)
    subprocess.run(["git", "commit", "-m", "fix(cart): sincronizacion estricta de badge en header y purga real al eliminar", "--allow-empty"], cwd=pc_dir, capture_output=True)
    res_pc = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=pc_dir, capture_output=True, text=True)
    print(f"🟢 pc-custom-lab -> Push: {'OK' if res_pc.returncode == 0 else res_pc.stderr.strip()}")

    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "fix(ecosystem): sincronizacion exacta de estado de carrito y vaciado", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
    res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
    print(f"🟢 Monorepositorio Raíz -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    fix_cart()
    deploy()
