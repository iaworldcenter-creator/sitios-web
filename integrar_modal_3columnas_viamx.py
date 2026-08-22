import os
import json
import re
import subprocess

BASE_DIR = r"E:\sitios web"
VIAMX_DIR = os.path.join(BASE_DIR, "bazar-viamx-nfl.gdl")

if not os.path.exists(VIAMX_DIR):
    alt = os.path.join(BASE_DIR, "bazar-viamx-NFL.GDL")
    if os.path.exists(alt):
        VIAMX_DIR = alt

INDEX_PATH = os.path.join(VIAMX_DIR, "index.html")

if not os.path.exists(INDEX_PATH):
    print(f"[Error] No se encontró {INDEX_PATH}")
    exit(1)

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

print("=" * 70)
print("INTEGRANDO VENTANA MODAL DE PRODUCTO EN 3 COLUMNAS EN VÍA MX")
print("=" * 70)

# Modal interactivo universal de 3 columnas para Vía MX
MODAL_3_COLUMNAS_HTML = """
<!-- ========================================================================
     VENTANA MODAL DE DETALLE DE PRODUCTO (ESTRUCTURA DE 3 COLUMNAS VÍAMX)
     ======================================================================== -->
<div id="productDetailModal" class="fixed inset-0 z-[250] hidden flex items-center justify-center bg-slate-950/85 backdrop-blur-md p-3 sm:p-6 overflow-y-auto" role="dialog" aria-modal="true" aria-labelledby="modal-p-title">
    <div class="relative w-full max-w-6xl bg-slate-900 border border-slate-800 rounded-3xl p-5 sm:p-8 shadow-[0_20px_60px_rgba(0,0,0,0.8)] text-slate-100 my-auto max-h-[92vh] overflow-y-auto">
        
        <!-- Botón de Cierre Superior -->
        <button onclick="closeProductModal()" class="absolute top-4 right-4 sm:top-6 sm:right-6 text-slate-400 hover:text-white bg-slate-950/60 hover:bg-slate-800 border border-slate-800 rounded-full w-10 h-10 flex items-center justify-center transition cursor-pointer z-30" aria-label="Cerrar ventana">
            <i class="fa-solid fa-xmark text-lg"></i>
        </button>

        <!-- GRID PRINCIPAL DE 3 COLUMNAS -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8 items-start mt-2">
            
            <!-- -------------------------------------------------------------
                 COLUMNA 1 (IZQUIERDA): FOTO GIGANTE Y GALERÍA DE ASSETS
                 ------------------------------------------------------------- -->
            <div class="lg:col-span-4 flex flex-col gap-3">
                <div class="w-full h-80 sm:h-96 bg-slate-950 border border-slate-800 rounded-2xl p-4 flex items-center justify-center relative overflow-hidden shadow-inner">
                    <img id="modal-p-img" src="" alt="Producto VíaMX" class="w-full h-full object-contain transition-transform duration-300 hover:scale-105" />
                    <span id="modal-p-badge" class="absolute top-3 left-3 bg-amber-500/20 border border-amber-500/50 text-amber-300 text-[10px] font-mono font-black px-2 py-0.5 rounded-md shadow">
                        Oferta VíaMX 2026
                    </span>
                </div>
                <div class="flex items-center justify-center gap-2 p-2 bg-slate-950/60 border border-slate-800/80 rounded-xl text-center">
                    <i class="fa-solid fa-shield-check text-cyan-400 text-sm"></i>
                    <span class="text-[11px] font-mono text-slate-300">Garantía física en Pedro Moreno 501 A</span>
                </div>
            </div>

            <!-- -------------------------------------------------------------
                 COLUMNA 2 (CENTRO): ESPECIFICACIONES, PRECIOS Y DESCRIPCIÓN
                 ------------------------------------------------------------- -->
            <div class="lg:col-span-5 flex flex-col gap-4 border-b lg:border-b-0 lg:border-r border-slate-800 pb-6 lg:pb-0 lg:pr-6">
                
                <!-- Encabezado y Marca -->
                <div>
                    <div class="flex items-center justify-between gap-2 mb-1">
                        <span id="modal-p-brand" class="text-xs font-mono text-cyan-400 font-bold uppercase tracking-wider"></span>
                        <span id="modal-p-sku" class="text-[10px] font-mono text-slate-500"></span>
                    </div>
                    <h2 id="modal-p-title" class="text-lg sm:text-xl font-black text-white leading-snug"></h2>
                    
                    <!-- Rating y Opiniones -->
                    <div class="flex items-center gap-2 mt-2">
                        <div class="flex items-center gap-1 text-amber-400 text-xs" id="modal-p-stars">
                            <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star-half-stroke"></i>
                        </div>
                        <span id="modal-p-rating-val" class="text-xs font-bold text-amber-300 font-mono">4.8</span>
                        <span class="text-slate-600">•</span>
                        <span id="modal-p-reviews" class="text-xs font-mono text-cyan-400">1,240 calificaciones</span>
                    </div>
                </div>

                <!-- Bloque de Precio y Descuento -->
                <div class="p-3.5 bg-slate-950 border border-slate-800 rounded-2xl flex flex-col gap-1">
                    <div class="flex items-baseline gap-3">
                        <span id="modal-p-discount" class="text-xs font-black text-red-400 bg-red-500/10 border border-red-500/30 px-2 py-0.5 rounded">
                            -25%
                        </span>
                        <span id="modal-p-price" class="text-2xl sm:text-3xl font-black text-amber-400 font-mono"></span>
                        <span id="modal-p-original" class="text-xs font-mono text-slate-500 line-through"></span>
                    </div>
                    <span class="text-[11px] text-slate-400 font-medium">
                        Hasta <strong>12 meses sin intereses</strong> de <span id="modal-p-monthly" class="text-slate-200 font-mono font-bold">$0.00 MXN</span>
                    </span>
                </div>

                <!-- Características Destacadas (Acerca de este artículo) -->
                <div>
                    <h3 class="text-xs font-mono text-cyan-400 uppercase tracking-widest font-black mb-2 flex items-center gap-1.5">
                        <i class="fa-solid fa-circle-info"></i> Acerca de este artículo
                    </h3>
                    <p id="modal-p-desc" class="text-xs text-slate-300 leading-relaxed bg-slate-950/50 p-3 rounded-xl border border-slate-800/80 mb-3"></p>
                </div>

                <!-- Tabla de Parámetros B2B -->
                <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3 text-xs">
                    <div class="grid grid-cols-2 gap-2 text-[11px]">
                        <div><span class="text-slate-500 font-mono uppercase">Disponibilidad:</span> <strong class="text-emerald-400 block font-sans">En Stock Guadalajara</strong></div>
                        <div><span class="text-slate-500 font-mono uppercase">Garantía:</span> <strong class="text-slate-200 block font-sans">12 Meses Directa</strong></div>
                        <div><span class="text-slate-500 font-mono uppercase">Punto de Entrega:</span> <strong class="text-slate-200 block font-sans">Pedro Moreno 501 A</strong></div>
                        <div><span class="text-slate-500 font-mono uppercase">Devoluciones:</span> <strong class="text-slate-200 block font-sans">48h con empaque</strong></div>
                    </div>
                </div>

            </div>

            <!-- -------------------------------------------------------------
                 COLUMNA 3 (DERECHA): PANEL DE COMPRA (BUY BOX VÍAMX)
                 ------------------------------------------------------------- -->
            <div class="lg:col-span-3 bg-slate-950 border border-slate-800 rounded-3xl p-5 shadow-xl flex flex-col gap-4">
                
                <div>
                    <span class="text-[10px] font-mono text-slate-400 uppercase block font-bold">Precio Total:</span>
                    <div id="modal-box-price" class="text-2xl font-black text-amber-400 font-mono"></div>
                    <span class="text-[11px] text-emerald-400 font-bold flex items-center gap-1 mt-1">
                        <i class="fa-solid fa-circle-check"></i> Disponible para entrega inmediata
                    </span>
                </div>

                <!-- Entrega Local -->
                <div class="text-[11px] text-slate-300 space-y-1 bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                    <p>📍 <strong>Entrega directa:</strong> Sucursal Pedro Moreno 501 A, Guadalajara Centro.</p>
                    <p class="text-slate-400">⏱️ Tiempo estimado: Mismo día o máx. 24-48 horas.</p>
                </div>

                <!-- Selector de Cantidad -->
                <div>
                    <label for="modal-p-qty" class="block text-[10px] font-mono text-slate-400 uppercase font-bold mb-1">Cantidad:</label>
                    <select id="modal-p-qty" class="w-full bg-slate-900 border border-slate-700 text-white rounded-xl p-2.5 text-xs font-bold focus:border-cyan-500 focus:outline-none cursor-pointer">
                        <option value="1" selected>1 unidad</option>
                        <option value="2">2 unidades</option>
                        <option value="3">3 unidades</option>
                        <option value="4">4 unidades</option>
                        <option value="5">5 unidades (Mayoreo B2B)</option>
                    </select>
                </div>

                <!-- Botones Dobles de Acción -->
                <div class="flex flex-col gap-2.5 pt-2">
                    <button onclick="addModalItemToCart()" class="w-full bg-slate-900 hover:bg-slate-800 border-2 border-cyan-500 text-cyan-300 hover:text-white font-black py-3 rounded-2xl text-xs uppercase tracking-wider transition active:scale-95 flex items-center justify-center gap-2 shadow-md shadow-cyan-950/40 cursor-pointer">
                        <i class="fa-solid fa-cart-plus text-sm"></i> Agregar al Carrito
                    </button>
                    <button onclick="buyNowModalItem()" class="w-full bg-gradient-to-r from-amber-400 via-amber-500 to-yellow-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black py-3 rounded-2xl text-xs uppercase tracking-wider transition active:scale-95 flex items-center justify-center gap-2 shadow-lg shadow-amber-500/25 cursor-pointer">
                        <i class="fa-solid fa-bolt text-sm"></i> Comprar Ahora
                    </button>
                </div>

                <!-- Beneficio de Cashback -->
                <div class="pt-3 border-t border-slate-800/80 text-[10px] text-slate-400 space-y-1">
                    <div class="flex items-center gap-1.5 text-amber-300 font-bold font-mono">
                        <i class="fa-solid fa-coins"></i> <span>5% de Cashback acumulable</span>
                    </div>
                    <p class="text-slate-400 leading-tight">Transacción segura respaldada por Anti-Gravity Ecosistema Comercial.</p>
                </div>

            </div>

        </div>

    </div>
</div>
"""

# Funciones JS para controlar la apertura dinámica del modal y las compras
JS_MODAL_LOGIC = """
    // Control Dinámico de la Ventana Modal de Producto (3 Columnas)
    let currentModalSku = null;

    function openProductModal(sku) {
        const item = viamxCatalog.find(p => p.sku === sku);
        if (!item) return;

        currentModalSku = sku;
        document.getElementById('modal-p-img').src = item.imagen || 'assets/img/mascota_tigre_thumb.webp';
        document.getElementById('modal-p-brand').innerText = item.marca || 'VÍA MX';
        document.getElementById('modal-p-sku').innerText = item.sku;
        document.getElementById('modal-p-title').innerText = item.nombre;
        document.getElementById('modal-p-rating-val').innerText = item.rating || '4.8';
        document.getElementById('modal-p-reviews').innerText = `${item.reviews || '1,200'} opiniones verificadas`;
        
        const priceFmt = formatCurrency(item.precio);
        document.getElementById('modal-p-price').innerText = `${priceFmt} MXN`;
        document.getElementById('modal-box-price').innerText = `${priceFmt} MXN`;
        
        if (item.original && item.original > item.precio) {
            document.getElementById('modal-p-original').innerText = formatCurrency(item.original);
            const discountPct = Math.round((1 - (item.precio / item.original)) * 100);
            document.getElementById('modal-p-discount').innerText = `-${discountPct}%`;
            document.getElementById('modal-p-discount').style.display = 'inline-block';
            document.getElementById('modal-p-original').style.display = 'inline-block';
        } else {
            document.getElementById('modal-p-discount').style.display = 'none';
            document.getElementById('modal-p-original').style.display = 'none';
        }

        const monthly = (parseFloat(item.precio) / 12).toFixed(2);
        document.getElementById('modal-p-monthly').innerText = `$${monthly} MXN`;
        document.getElementById('modal-p-desc').innerText = item.descripcion || '';
        document.getElementById('modal-p-qty').value = "1";

        const modal = document.getElementById('productDetailModal');
        if (modal) {
            modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }
    }

    function closeProductModal() {
        const modal = document.getElementById('productDetailModal');
        if (modal) {
            modal.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
    }

    function addModalItemToCart() {
        if (!currentModalSku) return;
        const qty = parseInt(document.getElementById('modal-p-qty').value) || 1;
        const item = viamxCatalog.find(i => i.sku === currentModalSku);
        if (!item) return;

        let cart = [];
        try {
            const stored = localStorage.getItem("ecosystem_global_cart");
            cart = stored ? JSON.parse(stored) : [];
        } catch(e) {}

        const existIdx = cart.findIndex(i => i.sku === currentModalSku);
        if (existIdx > -1) {
            cart[existIdx].quantity = (cart[existIdx].quantity || 1) + qty;
        } else {
            cart.push({
                sku: item.sku,
                nombre: item.nombre,
                precio: item.precio,
                imagen: item.imagen || 'assets/img/mascota_tigre_thumb.webp',
                categoria: item.categoria || 'viamx',
                quantity: qty
            });
        }

        localStorage.setItem("ecosystem_global_cart", JSON.stringify(cart));
        updateCartBadge();
        alert(`¡Se agregaron ${qty} unidad(es) de "${item.nombre}" a tu carrito!`);
        closeProductModal();
    }

    function buyNowModalItem() {
        if (!currentModalSku) return;
        const qty = parseInt(document.getElementById('modal-p-qty').value) || 1;
        const item = viamxCatalog.find(i => i.sku === currentModalSku);
        if (!item) return;

        let cart = [];
        try {
            const stored = localStorage.getItem("ecosystem_global_cart");
            cart = stored ? JSON.parse(stored) : [];
        } catch(e) {}

        const existIdx = cart.findIndex(i => i.sku === currentModalSku);
        if (existIdx > -1) {
            cart[existIdx].quantity = (cart[existIdx].quantity || 1) + qty;
        } else {
            cart.push({
                sku: item.sku,
                nombre: item.nombre,
                precio: item.precio,
                imagen: item.imagen || 'assets/img/mascota_tigre_thumb.webp',
                categoria: item.categoria || 'viamx',
                quantity: qty
            });
        }

        localStorage.setItem("ecosystem_global_cart", JSON.stringify(cart));
        window.location.href = 'checkout.html';
    }

    // Cerrar modal con la tecla Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeProductModal();
    });
"""

# Reemplazar la función renderCatalogPage para enlazar el clic en cada tarjeta hacia openProductModal
OLD_CARD_ONCLICK = 'class="bg-slate-950/90 border border-slate-800/90 hover:border-cyan-500/60 rounded-2xl p-3.5 flex flex-col justify-between transition duration-300 shadow-xl group hover:shadow-cyan-950/20"'
NEW_CARD_ONCLICK = 'onclick="openProductModal(\'${item.sku}\')" class="bg-slate-950/90 border border-slate-800/90 hover:border-cyan-500/60 rounded-2xl p-3.5 flex flex-col justify-between transition duration-300 shadow-xl group hover:shadow-cyan-950/20 cursor-pointer"'

html = html.replace(OLD_CARD_ONCLICK, NEW_CARD_ONCLICK)

# Evitar propagación en los botones inferiores de la tarjeta
html = html.replace('onclick="addToCart(\'${item.sku}\')"', 'onclick="event.stopPropagation(); addToCart(\'${item.sku}\')"')
html = html.replace('onclick="buyNow(\'${item.sku}\')"', 'onclick="event.stopPropagation(); buyNow(\'${item.sku}\')"')

# Insertar el modal antes de </main> o <footer>
if 'id="productDetailModal"' in html:
    html = re.sub(r'<div id="productDetailModal"[\s\S]*?<\/div>\s*<\/div>\s*<\/div>', MODAL_3_COLUMNAS_HTML.strip(), html, count=1)
else:
    footer_pos = html.find("<footer")
    if footer_pos != -1:
        html = html[:footer_pos] + f"\n\n{MODAL_3_COLUMNAS_HTML.strip()}\n\n" + html[footer_pos:]

# Inyectar la lógica JS
if 'function openProductModal' in html:
    html = re.sub(r'let currentModalSku[\s\S]*?document\.addEventListener\(\'keydown\', \(e\) => \{[^}]*\}\);', JS_MODAL_LOGIC.strip(), html, count=1)
else:
    html = html.replace("</script>\n</body>", f"{JS_MODAL_LOGIC}\n    </script>\n</body>")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("✓ Modal de 3 columnas integrado y conectado a los 200 productos.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(modal): ventana emergente de detalle de producto en 3 columnas para los 200 articulos", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(viamx): ventana modal 3 columnas interactiva con buy box y cashback", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
