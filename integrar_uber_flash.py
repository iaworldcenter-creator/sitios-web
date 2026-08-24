import os
import subprocess

BASE_DIR = r"E:\sitios web"

print("=" * 80)
print("INTEGRANDO MOTOR UBER FLASH + CÓDIGO PIN + PAGO SPEI EN APP Y CHECKOUT WEB")
print("=" * 80)

# --------------------------------------------------------------------------
# 1. APP MÓVIL PWA ACTUALIZADA (app.html)
# --------------------------------------------------------------------------
APP_HTML_CONTENT = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>BAZAR NFL App | Despacho B2B Uber Flash & Refacciones</title>
    
    <link rel="manifest" href="./manifest.json" />
    <meta name="theme-color" content="#0f172a" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    <link rel="apple-touch-icon" href="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" />

    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />

    <style>
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
        .cart-pop { animation: popBadge 0.25s ease-in-out; }
        @keyframes popBadge { 0% { transform: scale(1); } 50% { transform: scale(1.35); } 100% { transform: scale(1); } }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen flex flex-col justify-between selection:bg-cyan-500 selection:text-slate-950 pb-20 select-none">

    <!-- CABECERA FIJA -->
    <header class="bg-slate-900/95 backdrop-blur border-b border-slate-800 sticky top-0 z-50 px-4 py-3 shadow-xl">
        <div class="max-w-md mx-auto flex items-center justify-between gap-3">
            <div class="flex items-center gap-2.5">
                <img 
                    src="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" 
                    alt="Logo Tigre App" 
                    class="w-10 h-10 rounded-full object-cover border-2 border-amber-400 shadow-md"
                />
                <div>
                    <div class="flex items-center gap-1.5">
                        <span class="font-black text-lg text-white tracking-wider leading-none">BAZAR NFL</span>
                        <span class="bg-emerald-500/20 text-emerald-400 font-mono font-bold text-[9px] px-1.5 py-0.2 rounded border border-emerald-500/40">UBER DIRECT</span>
                    </div>
                    <span class="text-[10px] font-mono text-slate-400 block leading-tight">Pedro Moreno 501 A • GDL</span>
                </div>
            </div>

            <button onclick="toggleCartModal()" class="relative bg-slate-800 border border-slate-700 p-2.5 rounded-2xl text-cyan-400 active:scale-90 transition shadow">
                <i class="fa-solid fa-cart-shopping text-base"></i>
                <span id="app-cart-badge" class="absolute -top-1.5 -right-1.5 bg-amber-500 text-slate-950 font-mono font-black text-[10px] rounded-full w-5 h-5 flex items-center justify-center shadow">0</span>
            </button>
        </div>
    </header>

    <!-- CONTENIDO PRINCIPAL -->
    <main class="max-w-md mx-auto w-full px-4 py-4 space-y-4 flex-1">
        
        <!-- PROTOCOLO DE SEGURIDAD UBER FLASH -->
        <div class="bg-gradient-to-r from-slate-900 via-slate-900 to-emerald-950/40 border border-emerald-500/30 p-3.5 rounded-3xl space-y-2 shadow-lg">
            <div class="flex items-center justify-between">
                <span class="text-[9px] font-mono font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1">
                    <i class="fa-solid fa-shield-halved"></i> Entrega Segura con PIN
                </span>
                <span class="text-[10px] font-mono text-slate-400">Despacho en 3 min</span>
            </div>
            <p class="text-xs text-slate-300 leading-snug">
                Tus piezas se entregan vía <strong>Uber Moto</strong> con empaque sellado y <strong>Código PIN obligatorio</strong> al recibir.
            </p>
        </div>

        <!-- COTIZADOR DINÁMICO UBER FLASH -->
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-3xl shadow-xl space-y-3">
            <div class="flex items-center justify-between">
                <span class="text-xs font-mono font-bold text-white flex items-center gap-1.5">
                    <i class="fa-brands fa-uber text-white"></i> Cotizador Uber Flash
                </span>
                <span id="shipping-rate-badge" class="text-xs font-mono font-black text-amber-400 bg-amber-950/40 px-2 py-0.5 rounded-lg border border-amber-500/30">$35.00 MXN</span>
            </div>

            <select id="shippingZoneSelect" onchange="updateShippingZone()" class="w-full bg-slate-950 border border-slate-800 rounded-2xl px-3.5 py-2.5 text-xs font-bold text-slate-200 outline-none focus:border-cyan-400">
                <option value="35">Zona 1 (0-2.5 km): Centro / Calzada / Chapultepec ($35 MXN)</option>
                <option value="52">Zona 2 (2.5-5 km): Zapopan / Minerva / Tlaquepaque ($52 MXN)</option>
                <option value="75">Zona 3 (5+ km): Periférico / Tonalá / Tlajomulco ($75 MXN)</option>
            </select>

            <div class="flex items-center justify-between text-[10px] font-mono text-slate-400 pt-1">
                <span><i class="fa-solid fa-box text-cyan-400 mr-1"></i> Gratis desde $1,500 MXN</span>
                <span><i class="fa-solid fa-clock text-amber-400 mr-1"></i> Envíos de 9am a 7pm</span>
            </div>
        </div>

        <!-- SÚPER-BUSCADOR -->
        <div class="relative">
            <div class="flex items-center bg-white rounded-2xl px-3.5 py-2 gap-2 shadow-lg border-2 border-cyan-400">
                <i class="fa-solid fa-magnifying-glass text-slate-400 text-sm"></i>
                <input 
                    type="text" 
                    id="mobileSearchInput" 
                    placeholder="Buscar pieza, SKU o falla (ej. RAM, ASUS, cable, pantalla)..." 
                    class="flex-1 bg-transparent border-0 outline-none text-slate-950 font-bold text-xs placeholder-slate-400"
                    oninput="onMobileSearch(event)"
                />
            </div>
        </div>

        <!-- LISTADO DE REFACCIONES -->
        <div class="space-y-2">
            <div class="flex justify-between items-center px-1">
                <span class="text-xs font-mono font-bold text-slate-400 uppercase">Catálogo de Entrega Inmediata</span>
                <span class="text-[10px] font-mono text-emerald-400 font-bold"><i class="fa-solid fa-circle-check"></i> Stock Local</span>
            </div>
            <div id="mobile-product-list" class="space-y-2.5"></div>
        </div>

    </main>

    <!-- BARRA INFERIOR DE NAVEGACIÓN -->
    <nav class="fixed bottom-0 left-0 right-0 bg-slate-900/98 backdrop-blur border-t border-slate-800 px-6 py-2.5 z-40">
        <div class="max-w-md mx-auto flex items-center justify-between text-xs font-bold">
            <a href="https://iaworldcenter-creator.github.io/sitios-web/" class="flex flex-col items-center gap-1 text-slate-400 hover:text-amber-400 transition">
                <i class="fa-solid fa-house text-base"></i>
                <span class="text-[9px] font-mono">Portal Matriz</span>
            </a>
            <button onclick="location.reload()" class="flex flex-col items-center gap-1 text-cyan-400">
                <i class="fa-solid fa-motorcycle text-base"></i>
                <span class="text-[9px] font-mono">Uber Flash</span>
            </button>
            <a href="https://wa.me/523337271440" target="_blank" class="flex flex-col items-center gap-1 text-emerald-400">
                <i class="fa-brands fa-whatsapp text-base"></i>
                <span class="text-[9px] font-mono">Atención</span>
            </a>
            <button onclick="toggleCartModal()" class="flex flex-col items-center gap-1 text-amber-400">
                <i class="fa-solid fa-bag-shopping text-base"></i>
                <span class="text-[9px] font-mono">Mi Orden</span>
            </button>
        </div>
    </nav>

    <!-- MODAL DE CHECKOUT: SPEI + PIN DE SEGURIDAD -->
    <div id="appCartModal" class="fixed inset-0 z-50 hidden">
        <div class="absolute inset-0 bg-slate-950/80 backdrop-blur-sm" onclick="toggleCartModal()"></div>
        <div class="absolute bottom-0 left-0 right-0 max-w-md mx-auto bg-slate-900 border-t-2 border-emerald-400 rounded-t-3xl p-5 shadow-2xl flex flex-col justify-between max-h-[90vh] z-10">
            <div>
                <div class="flex justify-between items-center border-b border-slate-800 pb-3 mb-3">
                    <h3 class="font-black text-white text-sm flex items-center gap-2">
                        <i class="fa-solid fa-receipt text-cyan-400"></i> Despacho con Pago Previo SPEI
                    </h3>
                    <button onclick="toggleCartModal()" class="text-slate-400 hover:text-white p-1">
                        <i class="fa-solid fa-xmark text-lg"></i>
                    </button>
                </div>

                <!-- LISTA DE PRODUCTOS -->
                <div id="modal-cart-items" class="flex flex-col gap-2 overflow-y-auto max-h-[25vh] pr-1 no-scrollbar"></div>

                <!-- MÓDULO DE CÓDIGO PIN GENERADO -->
                <div class="mt-3 p-3 bg-slate-950 rounded-2xl border border-emerald-500/40 flex items-center justify-between">
                    <div>
                        <span class="text-[9px] font-mono text-emerald-400 uppercase font-bold block">Tu Código PIN de Entrega Uber:</span>
                        <span id="delivery-pin-display" class="text-xl font-mono font-black text-white tracking-widest">----</span>
                    </div>
                    <span class="text-[9px] text-slate-400 max-w-[150px] text-right">Díctalo al chofer para recibir el paquete.</span>
                </div>

                <!-- DATOS DE TRANSFERENCIA SPEI -->
                <div class="mt-3 p-3 bg-slate-950 rounded-2xl border border-slate-800 space-y-1.5 text-xs font-mono">
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400 text-[10px]">Banco Receptor:</span>
                        <strong class="text-white text-[11px]">BBVA México / STP</strong>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400 text-[10px]">CLABE Interbancaria:</span>
                        <div class="flex items-center gap-1.5">
                            <span class="text-cyan-300 font-bold text-[11px]" id="clabe-txt">0123 2001 5824 9382 10</span>
                            <button onclick="copyCLABE()" class="text-[9px] bg-slate-800 hover:bg-slate-700 px-1.5 py-0.5 rounded text-slate-300 cursor-pointer" title="Copiar CLABE">
                                <i class="fa-solid fa-copy"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- TOTALES Y ENVÍO A WHATSAPP -->
            <div class="border-t border-slate-800 pt-3 space-y-2 mt-3">
                <div class="flex justify-between text-xs font-mono">
                    <span class="text-slate-400">Subtotal Piezas:</span>
                    <span id="modal-subtotal-txt" class="text-white font-bold">$0.00 MXN</span>
                </div>
                <div class="flex justify-between text-xs font-mono">
                    <span class="text-slate-400">Flete Uber Flash:</span>
                    <span id="modal-shipping-txt" class="text-amber-400 font-bold">$35.00 MXN</span>
                </div>
                <div class="flex justify-between text-sm font-mono pt-1 border-t border-slate-800">
                    <strong class="text-white">Total a Transferir:</strong>
                    <strong id="modal-total-txt" class="text-emerald-400 font-black text-base">$0.00 MXN</strong>
                </div>

                <button onclick="sendOrderViaWhatsApp()" class="w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-black py-3 rounded-2xl text-xs uppercase tracking-wider transition active:scale-95 shadow-lg flex items-center justify-center gap-2 cursor-pointer">
                    <i class="fa-brands fa-whatsapp text-sm text-slate-950"></i> Mandar Comprobante SPEI & Despachar
                </button>
            </div>
        </div>
    </div>

    <script>
    const appProducts = [
        { sku: "PC-001", nombre: "Gabinete Micro-ATX con Fuente 500W", precio: 1250.00, original: 1550.00, desc: "Fuente certificada, USB 3.0 para taller.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/gabinete_negro.webp", tokens: ["gabinete", "fuente", "pc"] },
        { sku: "PC-002", nombre: "Tarjeta Madre ASUS Prime B760M-A WiFi DDR5", precio: 3400.00, original: 3950.00, desc: "Soporte Intel 12va/13va/14va Gen, dual M.2.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/motherboard_asus.webp", tokens: ["tarjeta madre", "asus", "placa"] },
        { sku: "PC-004", nombre: "RAM Kingston FURY Beast 16GB DDR5 5600MHz", precio: 1250.00, original: 1500.00, desc: "Disipador de aluminio de bajo perfil.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/ram_caja.webp", tokens: ["ram", "kingston", "fury", "ddr5"] },
        { sku: "PC-005", nombre: "SSD Kingston NV2 1TB NVMe PCIe 4.0", precio: 1350.00, original: 1650.00, desc: "3,500 MB/s lectura ultra rápida.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/disco_solido_m2.webp", tokens: ["ssd", "kingston", "nvme", "disco"] },
        { sku: "PUE-001", nombre: "Lentes Inteligentes Bluetooth con Audio", precio: 680.00, original: 950.00, desc: "Llamadas y música con protección UV.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_gamer_thumb.webp", tokens: ["lentes", "bluetooth", "audio"] },
        { sku: "PUE-003", nombre: "Cable USB-C a USB-C 65W Reforzado 2M", precio: 120.00, original: 180.00, desc: "Carga rápida para celulares y laptops.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/fuente_modular.webp", tokens: ["cable", "cargador", "usb c"] },
        { sku: "DUL-001", nombre: "Paleta Payaso Ricolino (Caja 15 piezas)", precio: 245.00, original: 290.00, desc: "Malvavisco con chocolate tradicional.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp", tokens: ["paleta", "dulces"] }
    ];

    let currentShippingCost = 35;
    let generatedPIN = "";

    function generatePIN() {
        generatedPIN = Math.floor(1000 + Math.random() * 9000).toString();
        const el = document.getElementById("delivery-pin-display");
        if (el) el.innerText = generatedPIN;
    }

    function renderMobileList(items = appProducts) {
        const container = document.getElementById("mobile-product-list");
        if (!container) return;

        container.innerHTML = items.map(p => {
            const discountPct = p.original ? Math.round((1 - (p.precio / p.original)) * 100) : 0;
            return `
                <div class="bg-slate-900 border border-slate-800 rounded-2xl p-3 flex items-center justify-between gap-3 shadow-md">
                    <img src="${p.img}" alt="${p.nombre}" class="w-14 h-14 object-contain rounded-xl bg-slate-950 p-1 shrink-0" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';" />
                    <div class="min-w-0 flex-1">
                        <span class="text-[9px] font-mono text-cyan-400 font-bold block">${p.sku}</span>
                        <h4 class="text-xs font-bold text-white line-clamp-1">${p.nombre}</h4>
                        <div class="flex items-baseline gap-2 mt-0.5">
                            <span class="text-amber-400 font-mono font-black text-xs">$${p.precio.toFixed(2)}</span>
                            ${p.original ? `<span class="text-[10px] font-mono text-red-400 line-through">$${p.original.toFixed(2)}</span>` : ''}
                        </div>
                    </div>
                    <button onclick="addToCartApp('${p.sku}')" class="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black p-2.5 rounded-xl text-xs active:scale-90 transition shadow shrink-0">
                        <i class="fa-solid fa-plus"></i>
                    </button>
                </div>
            `;
        }).join('');
    }

    function onMobileSearch(e) {
        const q = e.target.value.toLowerCase().trim();
        const filtered = appProducts.filter(p => {
            const searchStr = `${p.sku} ${p.nombre} ${(p.tokens || []).join(' ')}`.toLowerCase();
            return searchStr.includes(q);
        });
        renderMobileList(q ? filtered : appProducts);
    }

    function updateShippingZone() {
        const select = document.getElementById("shippingZoneSelect");
        currentShippingCost = parseFloat(select.value) || 35;
        document.getElementById("shipping-rate-badge").innerText = `$${currentShippingCost.toFixed(2)} MXN`;
        syncAppCart();
    }

    function addToCartApp(sku) {
        const item = appProducts.find(p => p.sku === sku);
        if (!item) return;

        let cart = [];
        try {
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cart = JSON.parse(raw);
        } catch(e) {}

        const exist = cart.find(i => i.sku === sku);
        if (exist) {
            exist.quantity = (parseInt(exist.quantity) || 1) + 1;
        } else {
            cart.push({ ...item, quantity: 1 });
        }

        localStorage.setItem('ecosystem_global_cart', JSON.stringify(cart));
        syncAppCart();

        const badge = document.getElementById("app-cart-badge");
        badge.classList.remove("cart-pop");
        void badge.offsetWidth;
        badge.classList.add("cart-pop");
    }

    function syncAppCart() {
        let cart = [];
        try {
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cart = JSON.parse(raw);
        } catch(e) {}

        const count = cart.reduce((sum, i) => sum + (parseInt(i.quantity) || 0), 0);
        const subtotal = cart.reduce((sum, i) => sum + ((parseFloat(i.precio) || 0) * (parseInt(i.quantity) || 0)), 0);
        const isFreeShipping = subtotal >= 1500 || count >= 10;
        const shippingFinal = isFreeShipping ? 0 : (subtotal > 0 ? currentShippingCost : 0);
        const total = subtotal + shippingFinal;

        document.getElementById("app-cart-badge").innerText = count;
        document.getElementById("modal-subtotal-txt").innerText = `$${subtotal.toFixed(2)} MXN`;
        document.getElementById("modal-shipping-txt").innerText = isFreeShipping ? "GRATIS ($0.00)" : `$${shippingFinal.toFixed(2)} MXN`;
        document.getElementById("modal-total-txt").innerText = `$${total.toFixed(2)} MXN`;

        const container = document.getElementById("modal-cart-items");
        if (!container) return;

        if (cart.length === 0) {
            container.innerHTML = '<div class="text-center py-6 text-slate-500 text-xs">Sin artículos en la orden.</div>';
            return;
        }

        container.innerHTML = cart.map(i => `
            <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex justify-between items-center text-xs">
                <div>
                    <strong class="text-white block truncate max-w-[190px]">${i.nombre}</strong>
                    <span class="text-slate-400 text-[10px]">Cant: ${i.quantity} x $${parseFloat(i.precio).toFixed(2)}</span>
                </div>
                <span class="text-amber-400 font-mono font-bold">$${(parseFloat(i.precio) * parseInt(i.quantity)).toFixed(2)}</span>
            </div>
        `).join('');
    }

    function toggleCartModal() {
        generatePIN();
        document.getElementById("appCartModal").classList.toggle("hidden");
        syncAppCart();
    }

    function copyCLABE() {
        const clabe = document.getElementById("clabe-txt").innerText.replace(/\s+/g, '');
        navigator.clipboard.writeText(clabe);
        alert('✓ CLABE copiada al portapapeles para tu transferencia SPEI.');
    }

    function sendOrderViaWhatsApp() {
        let cart = [];
        try {
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cart = JSON.parse(raw);
        } catch(e) {}

        if (cart.length === 0) {
            alert('Agrega al menos un artículo a tu orden.');
            return;
        }

        const subtotal = cart.reduce((sum, i) => sum + ((parseFloat(i.precio) || 0) * (parseInt(i.quantity) || 0)), 0);
        const shipping = subtotal >= 1500 ? 0 : currentShippingCost;
        const total = subtotal + shipping;

        let msg = `🛵 *ORDEN DESPACHO UBER FLASH - BAZAR NFL*%0A`;
        msg += `📍 *Origen:* Pedro Moreno 501 A, GDL Centro%0A`;
        msg += `🔐 *PIN de Seguridad Entrega:* ${generatedPIN}%0A%0A`;
        msg += `📦 *PRODUCTOS:*%0A`;
        cart.forEach(i => {
            msg += `• *${i.quantity}x* ${i.nombre} ($${(parseFloat(i.precio)*parseInt(i.quantity)).toFixed(2)})%0A`;
        });
        msg += `%0A💵 *Subtotal:* $${subtotal.toFixed(2)} MXN`;
        msg += `%0A🛵 *Flete Uber Flash:* ${shipping === 0 ? 'GRATIS' : '$' + shipping.toFixed(2) + ' MXN'}`;
        msg += `%0A💰 *TOTAL SPEI:* $${total.toFixed(2)} MXN%0A%0A`;
        msg += `_Adjunto captura de transferencia SPEI para liberar moto._`;

        window.open(`https://wa.me/523337271440?text=${msg}`, '_blank');
    }

    document.addEventListener("DOMContentLoaded", () => {
        renderMobileList();
        syncAppCart();
    });
    </script>
</body>
</html>
"""

# Guardar app.html
app_path = os.path.join(BASE_DIR, "app.html")
with open(app_path, "w", encoding="utf-8") as f:
    f.write(APP_HTML_CONTENT)
print(f"✓ App móvil B2B actualizada con Uber Flash + PIN en: {app_path}")

# Guardar también en sitios-web para sincronía
sitios_app_path = os.path.join(BASE_DIR, "sitios-web", "app.html")
if os.path.exists(os.path.dirname(sitios_app_path)):
    with open(sitios_app_path, "w", encoding="utf-8") as f:
        f.write(APP_HTML_CONTENT)
    print(f"✓ App móvil sincronizada en submódulo: {sitios_app_path}")

# --------------------------------------------------------------------------
# 2. ACTUALIZAR CHECKOUT UNIVERSAL WEB (checkout.html)
# --------------------------------------------------------------------------
CHECKOUT_HTML_CONTENT = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Checkout Seguro | Despacho Uber Flash & Envío Nacional Pedro Moreno 501 A</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen flex flex-col justify-between selection:bg-cyan-500 selection:text-slate-950">

    <header class="bg-slate-900 border-b border-slate-800 px-4 py-3 sticky top-0 z-50">
        <div class="max-w-4xl mx-auto flex items-center justify-between">
            <a href="https://iaworldcenter-creator.github.io/sitios-web/" class="flex items-center gap-3">
                <img src="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" class="w-10 h-10 rounded-full border-2 border-amber-400" />
                <span class="font-black text-lg text-white uppercase">BAZAR NFL.GDL</span>
            </a>
            <span class="text-xs font-mono text-emerald-400 flex items-center gap-1">
                <i class="fa-solid fa-lock"></i> Checkout Blindado SPEI
            </span>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-8 flex-1 w-full grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
        
        <!-- FORMULARIO DE ENVÍO Y ZONA UBER -->
        <div class="md:col-span-7 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
            <h2 class="text-base font-black text-white flex items-center gap-2 border-b border-slate-800 pb-3">
                <i class="fa-solid fa-location-dot text-amber-400"></i> 1. Datos de Entrega en Guadalajara
            </h2>

            <div class="space-y-3 text-xs">
                <div>
                    <label class="block text-slate-400 font-bold mb-1">Nombre Completo o Razón Social del Taller:</label>
                    <input type="text" id="custName" placeholder="Ej. Taller Electrónico Silva / Juan Pérez" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white outline-none focus:border-cyan-400" />
                </div>
                <div>
                    <label class="block text-slate-400 font-bold mb-1">Dirección Exacta con Entre Calles:</label>
                    <input type="text" id="custAddress" placeholder="Calle, Número, Colonia y Referencias" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white outline-none focus:border-cyan-400" />
                </div>
                <div>
                    <label class="block text-slate-400 font-bold mb-1">Zona de Reparto Uber Flash:</label>
                    <select id="checkoutZoneSelect" onchange="calculateTotals()" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white outline-none focus:border-cyan-400 font-bold">
                        <option value="35">Zona 1 (0-2.5 km): Centro / Calzada / Chapultepec ($35 MXN)</option>
                        <option value="52">Zona 2 (2.5-5 km): Zapopan / Minerva / Tlaquepaque ($52 MXN)</option>
                        <option value="75">Zona 3 (5+ km): Periférico / Tonalá / Tlajomulco ($75 MXN)</option>
                    </select>
                </div>
            </div>

            <!-- PIN DE SEGURIDAD GENERADO -->
            <div class="p-4 bg-slate-950 border border-emerald-500/40 rounded-2xl flex items-center justify-between">
                <div>
                    <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase block">Código PIN de Entrega Uber:</span>
                    <span id="checkout-pin" class="text-2xl font-mono font-black text-white tracking-widest">----</span>
                </div>
                <i class="fa-solid fa-shield-check text-2xl text-emerald-400"></i>
            </div>
        </div>

        <!-- RESUMEN DE COMPRA Y DATOS SPEI -->
        <div class="md:col-span-5 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
            <h2 class="text-base font-black text-white flex items-center gap-2 border-b border-slate-800 pb-3">
                <i class="fa-solid fa-receipt text-cyan-400"></i> 2. Resumen y Pago SPEI
            </h2>

            <div id="checkout-items" class="space-y-2 max-h-40 overflow-y-auto no-scrollbar text-xs"></div>

            <div class="space-y-1.5 text-xs font-mono pt-3 border-t border-slate-800">
                <div class="flex justify-between text-slate-400">
                    <span>Subtotal:</span>
                    <span id="chk-subtotal" class="text-white font-bold">$0.00 MXN</span>
                </div>
                <div class="flex justify-between text-slate-400">
                    <span>Flete Uber Flash:</span>
                    <span id="chk-shipping" class="text-amber-400 font-bold">$35.00 MXN</span>
                </div>
                <div class="flex justify-between text-sm font-bold text-white pt-2 border-t border-slate-800">
                    <span>Total a Transferir:</span>
                    <span id="chk-total" class="text-emerald-400 font-black text-base">$0.00 MXN</span>
                </div>
            </div>

            <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-[11px] font-mono space-y-1">
                <span class="text-slate-400 block text-[10px]">CLABE para Transferencia:</span>
                <strong class="text-cyan-300 block text-xs">0123 2001 5824 9382 10</strong>
                <span class="text-slate-500 text-[10px] block">BBVA México • Pedro Moreno 501 A</span>
            </div>

            <button onclick="finishCheckout()" class="w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-black py-3 rounded-xl text-xs uppercase tracking-wider transition active:scale-95 shadow-lg flex items-center justify-center gap-2 cursor-pointer">
                <i class="fa-brands fa-whatsapp text-sm text-slate-950"></i> Confirmar con Comprobante
            </button>
        </div>

    </main>

    <script>
    let generatedPin = Math.floor(1000 + Math.random() * 9000).toString();
    document.getElementById("checkout-pin").innerText = generatedPin;

    function getCart() {
        try {
            const raw = localStorage.getItem('ecosystem_global_cart');
            return raw ? JSON.parse(raw) : [];
        } catch(e) { return []; }
    }

    function calculateTotals() {
        const cart = getCart();
        const subtotal = cart.reduce((sum, i) => sum + ((parseFloat(i.precio) || 0) * (parseInt(i.quantity) || 0)), 0);
        const count = cart.reduce((sum, i) => sum + (parseInt(i.quantity) || 0), 0);
        const zoneCost = parseFloat(document.getElementById("checkoutZoneSelect").value) || 35;
        const isFree = subtotal >= 1500 || count >= 10;
        const shipping = isFree ? 0 : (subtotal > 0 ? zoneCost : 0);
        const total = subtotal + shipping;

        document.getElementById("chk-subtotal").innerText = `$${subtotal.toFixed(2)} MXN`;
        document.getElementById("chk-shipping").innerText = isFree ? "GRATIS ($0.00)" : `$${shipping.toFixed(2)} MXN`;
        document.getElementById("chk-total").innerText = `$${total.toFixed(2)} MXN`;

        const container = document.getElementById("checkout-items");
        if (cart.length === 0) {
            container.innerHTML = '<span class="text-slate-500 text-center block py-4">Tu canasta está vacía.</span>';
            return;
        }
        container.innerHTML = cart.map(i => `
            <div class="flex justify-between items-center bg-slate-950 p-2 rounded-lg">
                <span class="truncate max-w-[180px]">${i.nombre} (x${i.quantity})</span>
                <span class="font-mono text-amber-400 font-bold">$${(parseFloat(i.precio)*parseInt(i.quantity)).toFixed(2)}</span>
            </div>
        `).join('');
    }

    function finishCheckout() {
        const name = document.getElementById("custName").value.trim();
        const address = document.getElementById("custAddress").value.trim();
        const cart = getCart();

        if (cart.length === 0) { alert('Tu canasta está vacía.'); return; }
        if (!name || !address) { alert('Por favor ingresa tu nombre y dirección completa para el repartidor de Uber.'); return; }

        const subtotal = cart.reduce((sum, i) => sum + ((parseFloat(i.precio) || 0) * (parseInt(i.quantity) || 0)), 0);
        const zoneCost = parseFloat(document.getElementById("checkoutZoneSelect").value) || 35;
        const shipping = subtotal >= 1500 ? 0 : zoneCost;
        const total = subtotal + shipping;

        let msg = `🛵 *NUEVA ORDEN WEB BAZAR NFL - DESPACHO UBER FLASH*%0A`;
        msg += `👤 *Cliente / Taller:* ${name}%0A`;
        msg += `📍 *Dirección Entrega:* ${address}%0A`;
        msg += `🔐 *PIN Uber:* ${generatedPin}%0A%0A`;
        msg += `📦 *ARTÍCULOS:*%0A`;
        cart.forEach(i => {
            msg += `• *${i.quantity}x* ${i.nombre} ($${(parseFloat(i.precio)*parseInt(i.quantity)).toFixed(2)})%0A`;
        });
        msg += `%0A💰 *TOTAL SPEI:* $${total.toFixed(2)} MXN%0A%0A`;
        msg += `_Adjunto comprobante de pago bancario para enviar la moto._`;

        window.open(`https://wa.me/523337271440?text=${msg}`, '_blank');
    }

    document.addEventListener("DOMContentLoaded", calculateTotals);
    </script>
</body>
</html>
"""

# Guardar checkout en PC Custom Lab y en la raíz
checkout_paths = [
    os.path.join(BASE_DIR, "pc-custom-lab", "checkout.html"),
    os.path.join(BASE_DIR, "checkout.html")
]

for cp in checkout_paths:
    if os.path.exists(os.path.dirname(cp)):
        with open(cp, "w", encoding="utf-8") as f:
            f.write(CHECKOUT_HTML_CONTENT)
        print(f"✓ Checkout web blindado actualizado en: {cp}")

# Push integral a GitHub Pages
print("\n=== DESPLEGANDO A GITHUB PAGES ===")
subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(uber): integracion completa de cotizador Uber Flash, PIN antirrobo y checkout SPEI", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
