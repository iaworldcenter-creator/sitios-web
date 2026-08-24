import os
import subprocess
import json
import urllib.parse

BASE_DIR = r"E:\sitios web"
APP_URL = "https://iaworldcenter-creator.github.io/sitios-web/app.html"

print("=" * 80)
print("APLICANDO VALIDACIÓN DE DOMICILIO UBER Y CARRUSEL 2-COLS CON FLECHAS EN TODO EL ECOSISTEMA")
print("=" * 80)

# --------------------------------------------------------------------------
# 1. REESTRUCTURAR APP MÓVIL (app.html) CON VALIDADOR Y 2 PRODUCTOS + FLECHAS
# --------------------------------------------------------------------------
APP_HTML_CODE = f"""<!DOCTYPE html>
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
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
        .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
        .cart-pop {{ animation: popBadge 0.25s ease-in-out; }}
        @keyframes popBadge {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.35); }} 100% {{ transform: scale(1); }} }}
        .fade-in {{ animation: fadeIn 0.15s ease-in-out forwards; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen flex flex-col justify-between selection:bg-cyan-500 selection:text-slate-950 pb-20 select-none">

    <!-- CABECERA FIJA -->
    <header class="bg-slate-900/95 backdrop-blur border-b border-slate-800 sticky top-0 z-50 px-4 py-3 shadow-xl">
        <div class="max-w-md mx-auto flex items-center justify-between gap-3">
            <div class="flex items-center gap-2.5">
                <img src="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" alt="Logo Tigre App" class="w-10 h-10 rounded-full object-cover border-2 border-amber-400 shadow-md" />
                <div>
                    <div class="flex items-center gap-1.5">
                        <span class="font-black text-lg text-white tracking-wider leading-none">BAZAR NFL</span>
                        <span class="bg-cyan-500/20 text-cyan-300 font-mono font-bold text-[9px] px-1.5 py-0.2 rounded border border-cyan-500/40">APP B2B</span>
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

    <main class="max-w-md mx-auto w-full px-4 py-4 space-y-4 flex-1">
        
        <!-- 1. COTIZADOR POR DOMICILIO CON VALIDACIÓN ESTRICTA -->
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-3xl shadow-xl space-y-3">
            <div class="flex items-center justify-between">
                <span class="text-xs font-mono font-bold text-white flex items-center gap-1.5">
                    <i class="fa-brands fa-uber text-white"></i> Cotizador de Flete Uber
                </span>
                <span id="shipping-rate-badge" class="text-xs font-mono font-bold text-slate-400 bg-slate-950 px-2.5 py-0.5 rounded-lg border border-slate-800">Pendiente Cotizar</span>
            </div>

            <!-- Formulario de Datos Obligatorios -->
            <div class="space-y-2 text-xs">
                <div>
                    <label class="text-[10px] font-mono text-slate-400 block mb-0.5">Calle / Avenida:</label>
                    <input type="text" id="inputCalle" placeholder="Ej. Av. Hidalgo, Pedro Moreno, Colón..." class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2 text-white outline-none focus:border-cyan-400" />
                </div>
                <div class="grid grid-cols-2 gap-2">
                    <div>
                        <label class="text-[10px] font-mono text-slate-400 block mb-0.5">Núm. Exterior / Interior:</label>
                        <input type="text" id="inputNum" placeholder="Ej. #501 int A" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2 text-white outline-none focus:border-cyan-400" />
                    </div>
                    <div>
                        <label class="text-[10px] font-mono text-slate-400 block mb-0.5">Colonia / Barrio:</label>
                        <input type="text" id="inputColonia" placeholder="Ej. Americana, Centro..." class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2 text-white outline-none focus:border-cyan-400" />
                    </div>
                </div>
                <div>
                    <label class="text-[10px] font-mono text-slate-400 block mb-0.5">Municipio / Zona Conurbada:</label>
                    <select id="selectMunicipio" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2 text-white outline-none focus:border-cyan-400 font-medium">
                        <option value="">-- Selecciona tu Municipio --</option>
                        <option value="guadalajara">Guadalajara (Centro / Alrededores)</option>
                        <option value="zapopan">Zapopan (Minerva / Providencia / Poniente)</option>
                        <option value="tlaquepaque">Tlaquepaque (Centro / Alamo)</option>
                        <option value="tonala">Tonalá (Oriente / Periférico)</option>
                        <option value="tlajomulco">Tlajomulco de Zúñiga (Zona Sur / Payuca)</option>
                        <option value="elsalto">El Salto / Aeropuerto</option>
                    </select>
                </div>

                <!-- Caja de Alertas de Validación -->
                <div id="address-error-box" class="hidden p-2 rounded-xl bg-amber-950/60 border border-amber-500/50 text-amber-300 text-[11px] font-mono leading-tight"></div>

                <button onclick="quoteShipping()" class="w-full bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black py-2.5 rounded-xl text-xs uppercase tracking-wider transition active:scale-95 shadow cursor-pointer flex items-center justify-center gap-1.5">
                    <i class="fa-solid fa-calculator text-xs"></i> <span>Cotizar Flete de Envío</span>
                </button>
            </div>

            <div class="flex items-center justify-between text-[10px] font-mono text-slate-400 pt-1 border-t border-slate-800">
                <span id="distance-calc-info">Origen: Pedro Moreno 501 A</span>
                <span class="text-emerald-400 font-bold">Gratis desde $1,500 MXN</span>
            </div>
        </div>

        <!-- 2. SÚPER-BUSCADOR -->
        <div class="relative">
            <div class="flex items-center bg-white rounded-2xl px-3.5 py-2 gap-2 shadow-lg border-2 border-cyan-400">
                <i class="fa-solid fa-magnifying-glass text-slate-400 text-sm"></i>
                <input type="text" id="mobileSearchInput" autocomplete="off" placeholder="Busca pieza, SKU o falla (ej. RAM, 4070, paleta)..." class="flex-1 bg-transparent border-0 outline-none text-slate-950 font-bold text-xs placeholder-slate-400" oninput="onMobileSearch(event)" />
                <button onclick="clearMobileSearch()" id="clear-search-btn" class="hidden text-slate-400 hover:text-slate-600 text-xs px-1 font-bold"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div id="mobile-autocomplete-box" class="hidden absolute top-full left-0 right-0 mt-2 bg-slate-900 border-2 border-cyan-500/60 rounded-2xl shadow-2xl z-40 p-2.5 flex flex-col gap-2 max-h-80 overflow-y-auto no-scrollbar"></div>
        </div>

        <!-- 3. NUESTRAS 7 BOUTIQUES (DESPLEGABLE TOP 3) -->
        <div class="space-y-2.5">
            <div class="flex justify-between items-center px-1">
                <span class="text-xs font-mono font-bold text-white uppercase flex items-center gap-1.5">
                    <i class="fa-solid fa-layer-group text-amber-400"></i> Nuestras 7 Boutiques
                </span>
                <span class="text-[9px] font-mono text-cyan-400 font-bold">Toca para ver top 3</span>
            </div>
            <div class="grid grid-cols-1 gap-2" id="boutiques-accordion-list"></div>
        </div>

        <!-- 4. CATÁLOGO CON SWIPE DE 2 PRODUCTOS + FLECHAS FLOTANTES (< y >) -->
        <div class="space-y-2 pt-2">
            <div class="flex justify-between items-center px-1">
                <span class="text-xs font-mono font-bold text-slate-400 uppercase">Catálogo de Entrega Inmediata</span>
                <span class="text-[10px] font-mono text-cyan-400 font-bold">Desliza a los lados &rarr;</span>
            </div>

            <div class="relative group">
                <button onclick="scrollCarousel('mobile-product-carousel', -1)" class="absolute -left-2 top-1/2 -translate-y-1/2 z-20 w-7 h-7 rounded-full bg-slate-900/95 border border-cyan-400 text-cyan-300 flex items-center justify-center shadow-lg active:scale-90">
                    <i class="fa-solid fa-chevron-left text-[10px]"></i>
                </button>
                
                <div id="mobile-product-carousel" class="flex flex-row overflow-x-auto flex-nowrap gap-2.5 pb-2 no-scrollbar snap-x snap-mandatory scroll-smooth px-1">
                    <!-- 2 productos exactos en pantalla inyectados dinámicamente -->
                </div>

                <button onclick="scrollCarousel('mobile-product-carousel', 1)" class="absolute -right-2 top-1/2 -translate-y-1/2 z-20 w-7 h-7 rounded-full bg-slate-900/95 border border-cyan-400 text-cyan-300 flex items-center justify-center shadow-lg active:scale-90">
                    <i class="fa-solid fa-chevron-right text-[10px]"></i>
                </button>
            </div>
        </div>

    </main>

    <!-- BARRA INFERIOR -->
    <nav class="fixed bottom-0 left-0 right-0 bg-slate-900/98 backdrop-blur border-t border-slate-800 px-6 py-2.5 z-40">
        <div class="max-w-md mx-auto flex items-center justify-between text-xs font-bold">
            <a href="https://iaworldcenter-creator.github.io/sitios-web/" class="flex flex-col items-center gap-1 text-slate-400 hover:text-amber-400 transition">
                <i class="fa-solid fa-house text-base"></i><span class="text-[9px] font-mono">Matriz</span>
            </a>
            <button onclick="location.reload()" class="flex flex-col items-center gap-1 text-cyan-400">
                <i class="fa-solid fa-motorcycle text-base"></i><span class="text-[9px] font-mono">Uber Flash</span>
            </button>
            <a href="https://wa.me/523337271440" target="_blank" class="flex flex-col items-center gap-1 text-emerald-400">
                <i class="fa-brands fa-whatsapp text-base"></i><span class="text-[9px] font-mono">Atención</span>
            </a>
            <button onclick="toggleCartModal()" class="flex flex-col items-center gap-1 text-amber-400">
                <i class="fa-solid fa-bag-shopping text-base"></i><span class="text-[9px] font-mono">Mi Pedido</span>
            </button>
        </div>
    </nav>

    <!-- MODAL DE CHECKOUT -->
    <div id="appCartModal" class="fixed inset-0 z-50 hidden">
        <div class="absolute inset-0 bg-slate-950/80 backdrop-blur-sm" onclick="toggleCartModal()"></div>
        <div class="absolute bottom-0 left-0 right-0 max-w-md mx-auto bg-slate-900 border-t-2 border-emerald-400 rounded-t-3xl p-5 shadow-2xl flex flex-col justify-between max-h-[90vh] z-10">
            <div>
                <div class="flex justify-between items-center border-b border-slate-800 pb-3 mb-3">
                    <h3 class="font-black text-white text-sm flex items-center gap-2">
                        <i class="fa-solid fa-receipt text-cyan-400"></i> Despacho con Pago Previo SPEI
                    </h3>
                    <button onclick="toggleCartModal()" class="text-slate-400 hover:text-white p-1"><i class="fa-solid fa-xmark text-lg"></i></button>
                </div>
                <div id="modal-cart-items" class="flex flex-col gap-2 overflow-y-auto max-h-[25vh] pr-1 no-scrollbar"></div>
                <div class="mt-3 p-3 bg-slate-950 rounded-2xl border border-emerald-500/40 flex items-center justify-between">
                    <div>
                        <span class="text-[9px] font-mono text-emerald-400 uppercase font-bold block">PIN de Entrega Uber:</span>
                        <span id="delivery-pin-display" class="text-xl font-mono font-black text-white tracking-widest">----</span>
                    </div>
                    <span class="text-[9px] text-slate-400 max-w-[150px] text-right">Díctalo al chofer para recibir el paquete.</span>
                </div>
                <div class="mt-3 p-3 bg-slate-950 rounded-2xl border border-slate-800 space-y-1 text-xs font-mono">
                    <div class="flex justify-between items-center"><span class="text-slate-400 text-[10px]">Banco:</span><strong class="text-white text-[11px]">BBVA México / STP</strong></div>
                    <div class="flex justify-between items-center"><span class="text-slate-400 text-[10px]">CLABE:</span><span class="text-cyan-300 font-bold text-[11px]">0123 2001 5824 9382 10</span></div>
                </div>
            </div>
            <div class="border-t border-slate-800 pt-3 space-y-2 mt-3">
                <div class="flex justify-between text-xs font-mono"><span class="text-slate-400">Subtotal:</span><span id="modal-subtotal-txt" class="text-white font-bold">$0.00 MXN</span></div>
                <div class="flex justify-between text-xs font-mono"><span class="text-slate-400">Flete Cotizado:</span><span id="modal-shipping-txt" class="text-amber-400 font-bold">Por Cotizar</span></div>
                <div class="flex justify-between text-sm font-mono pt-1 border-t border-slate-800"><strong class="text-white">Total SPEI:</strong><strong id="modal-total-txt" class="text-emerald-400 font-black text-base">$0.00 MXN</strong></div>
                <button onclick="sendOrderViaWhatsApp()" class="w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 text-slate-950 font-black py-3 rounded-2xl text-xs uppercase tracking-wider transition active:scale-95 shadow-lg flex items-center justify-center gap-2 cursor-pointer">
                    <i class="fa-brands fa-whatsapp text-sm text-slate-950"></i> Mandar Comprobante SPEI & Despachar
                </button>
            </div>
        </div>
    </div>

    <script>
    const boutiquesConfig = [
        {{ id: "pc-custom", name: "PC Custom Lab", tag: "HARDWARE & PC", icon: "fa-microchip", color: "text-cyan-400", url: "https://iaworldcenter-creator.github.io/pc-custom-lab/" }},
        {{ id: "viamx", name: "Vía MX Boutique", tag: "DEPARTAMENTAL", icon: "fa-gem", color: "text-cyan-300", url: "https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/" }},
        {{ id: "cigarros", name: "Cigarros Bazar", tag: "TABACOS & PUROS", icon: "fa-smoking", color: "text-amber-400", url: "https://iaworldcenter-creator.github.io/cigarros-bazar/" }},
        {{ id: "dulces", name: "Dulces Bazar", tag: "DULCERÍA & BOTANAS", icon: "fa-candy-cane", color: "text-pink-400", url: "https://iaworldcenter-creator.github.io/dulces-bazar/" }},
        {{ id: "kiosco", name: "Kiosco Digital", tag: "REVISTAS & PRENSA", icon: "fa-newspaper", color: "text-indigo-400", url: "https://iaworldcenter-creator.github.io/kiosco-digital/" }},
        {{ id: "puesto", name: "Mi Puesto Bazar", tag: "NOVEDADES & GADGETS", icon: "fa-store", color: "text-emerald-400", url: "https://iaworldcenter-creator.github.io/mi-puesto-bazar/" }},
        {{ id: "ofertas", name: "Ofertas & Liquidaciones", tag: "OUTLET DIRECTO B2B", icon: "fa-tags", color: "text-red-400", url: "https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/" }}
    ];

    const appProducts = [
        {{ sku: "PC-001", boutiqueId: "pc-custom", nombre: "Gabinete Micro-ATX con Fuente 500W", marca: "Acteck", precio: 1250.00, original: 1550.00, desc: "Fuente certificada, USB 3.0 para taller.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/gabinete_negro.webp", tokens: ["gabinete", "fuente", "pc"], sales: 95 }},
        {{ sku: "PC-002", boutiqueId: "pc-custom", nombre: "Tarjeta Madre ASUS Prime B760M-A WiFi DDR5", marca: "ASUS", precio: 3400.00, original: 3950.00, desc: "Soporte Intel 12va/13va/14va Gen, dual M.2.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/motherboard_asus.webp", tokens: ["tarjeta madre", "asus", "placa"], sales: 82 }},
        {{ sku: "PC-004", boutiqueId: "pc-custom", nombre: "RAM Kingston FURY Beast 16GB DDR5 5600MHz", marca: "Kingston", precio: 1250.00, original: 1500.00, desc: "Disipador de aluminio de bajo perfil.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/ram_caja.webp", tokens: ["ram", "kingston", "fury", "ddr5"], sales: 140 }},
        {{ sku: "PC-005", boutiqueId: "pc-custom", nombre: "SSD Kingston NV2 1TB NVMe PCIe 4.0", marca: "Kingston", precio: 1350.00, original: 1650.00, desc: "3,500 MB/s lectura ultra rápida.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/disco_solido_m2.webp", tokens: ["ssd", "kingston", "nvme", "disco"], sales: 110 }},
        {{ sku: "VMX-001", boutiqueId: "viamx", nombre: "Pantalla Smart TV 55 Pulgadas 4K UHD", marca: "Samsung", precio: 7999.00, original: 11499.00, desc: "Panel LED 4K con asistente de voz.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_curvo_negro.webp", tokens: ["pantalla", "smart tv", "samsung"], sales: 70 }},
        {{ sku: "CIG-001", boutiqueId: "cigarros", nombre: "Cigarros Marlboro Gold Original (20)", marca: "Marlboro", precio: 82.00, original: 95.00, desc: "Sabor suave de importación.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["cigarros", "marlboro"], sales: 210 }},
        {{ sku: "DUL-001", boutiqueId: "dulces", nombre: "Paleta Payaso Ricolino (Caja 15 piezas)", marca: "Ricolino", precio: 245.00, original: 290.00, desc: "Malvavisco con chocolate y gomitas.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp", tokens: ["paleta", "dulces"], sales: 180 }},
        {{ sku: "PUE-001", boutiqueId: "puesto", nombre: "Lentes Inteligentes Bluetooth con Audio", marca: "SmartVision", precio: 680.00, original: 950.00, desc: "Llamadas y música con protección UV.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_gamer_thumb.webp", tokens: ["lentes", "bluetooth"], sales: 115 }}
    ];

    let currentShippingCost = null;
    let generatedPIN = "";
    let activeBoutiqueId = null;

    // VALIDACIÓN ESTRICTA DEL DOMICILIO Y CÁLCULO DE FLETE UBER FLASH
    function quoteShipping() {{
        const calle = document.getElementById("inputCalle").value.trim();
        const num = document.getElementById("inputNum").value.trim();
        const colonia = document.getElementById("inputColonia").value.trim();
        const municipio = document.getElementById("selectMunicipio").value;
        const errorBox = document.getElementById("address-error-box");
        const badge = document.getElementById("shipping-rate-badge");

        if (!calle) {{
            showError("⚠️ Falta escribir la calle o avenida.");
            return;
        }}
        if (!num) {{
            showError("⚠️ Falta el número exterior / interior de la casa o taller.");
            return;
        }}
        if (!colonia) {{
            showError("⚠️ Falta la colonia o barrio.");
            return;
        }}
        if (!municipio) {{
            showError("⚠️ Falta seleccionar el municipio.");
            return;
        }}

        errorBox.classList.add("hidden");
        let rate = 35;
        let dist = "2.1 km";

        if (municipio === "zapopan") {{ rate = 52; dist = "4.8 km (Zapopan/Poniente)"; }}
        else if (municipio === "tlaquepaque") {{ rate = 48; dist = "4.5 km (Tlaquepaque)"; }}
        else if (municipio === "tonala") {{ rate = 70; dist = "9.2 km (Tonalá)"; }}
        else if (municipio === "tlajomulco") {{ rate = 125; dist = "18.5 km (Tlajomulco Sur/Payuca)"; }}
        else if (municipio === "elsalto") {{ rate = 135; dist = "21.0 km (El Salto)"; }}
        else {{ rate = 35; dist = "1.8 km (Guadalajara Centro)"; }}

        currentShippingCost = rate;
        badge.innerText = `$${{rate.toFixed(2)}} MXN`;
        badge.className = "text-xs font-mono font-black text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded-lg border border-emerald-500/40";
        document.getElementById("distance-calc-info").innerHTML = `🛵 <strong class="text-emerald-400">Uber Flash:</strong> ${{calle}} #${{num}}, Col. ${{colonia}} (~${{dist}})`;
        syncAppCart();
    }}

    function showError(msg) {{
        const box = document.getElementById("address-error-box");
        box.innerText = msg;
        box.classList.remove("hidden");
    }}

    function scrollCarousel(id, direction) {{
        const el = document.getElementById(id);
        if (el) {{
            const amount = el.clientWidth * 0.85;
            el.scrollBy({{ left: direction * amount, behavior: 'smooth' }});
        }}
    }}

    // RENDERIZAR CARRUSEL DE EXACTAMENTE 2 PRODUCTOS EN PANTALLA
    function renderMobileList(items = appProducts) {{
        const container = document.getElementById("mobile-product-carousel");
        if (!container) return;

        container.innerHTML = items.map(p => {{
            const discountPct = p.original ? Math.round((1 - (p.precio / p.original)) * 100) : 0;
            return `
                <div class="w-[calc(50%-5px)] min-w-[155px] max-w-[185px] shrink-0 snap-start bg-slate-900 border border-slate-800 rounded-2xl p-2.5 flex flex-col justify-between shadow-md">
                    <div>
                        <div class="w-full h-32 overflow-hidden rounded-xl bg-slate-950 flex items-center justify-center p-1.5 relative mb-2 shadow-inner">
                            <img src="${{p.img}}" alt="${{p.nombre}}" class="w-full h-full object-contain" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';" />
                            ${{discountPct > 0 ? `<span class="absolute top-1 left-1 bg-red-600 text-white text-[8px] font-mono font-bold px-1.5 py-0.2 rounded">-${{discountPct}}%</span>` : ''}}
                        </div>
                        <span class="text-[8px] font-mono text-cyan-400 font-bold block truncate">${{p.marca}} &bull; ${{p.sku}}</span>
                        <h4 class="text-xs font-bold text-white line-clamp-2 leading-snug mt-0.5" title="${{p.nombre}}">${{p.nombre}}</h4>
                    </div>

                    <div class="pt-1.5 border-t border-slate-800/80 mt-1.5 space-y-1.5">
                        <div class="flex flex-col">
                            ${{p.original ? `<span class="text-[9px] font-mono text-red-400 line-through">$${{p.original.toFixed(2)}}</span>` : ''}}
                            <span class="text-amber-400 font-mono font-black text-xs">$${{p.precio.toFixed(2)}}</span>
                        </div>
                        <div class="grid grid-cols-2 gap-1">
                            <button onclick="addToCartApp('${{p.sku}}')" class="bg-slate-800 text-cyan-300 p-1.5 rounded-lg text-[10px] flex items-center justify-center shadow border border-cyan-500/30 active:scale-90" title="Agregar">
                                <i class="fa-solid fa-cart-plus"></i>
                            </button>
                            <button onclick="buyNowApp('${{p.sku}}')" class="bg-gradient-to-r from-amber-400 to-amber-500 text-slate-950 font-black p-1.5 rounded-lg text-[10px] flex items-center justify-center shadow active:scale-90">
                                Comprar
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }}).join('');
    }}

    function renderBoutiquesAccordions() {{
        const container = document.getElementById("boutiques-accordion-list");
        if (!container) return;

        container.innerHTML = boutiquesConfig.map(b => {{
            const top3 = appProducts.filter(p => p.boutiqueId === b.id).slice(0, 3);
            const isOpen = activeBoutiqueId === b.id;

            return `
                <div class="bg-slate-900 border ${{isOpen ? 'border-cyan-400' : 'border-slate-800'}} rounded-2xl overflow-hidden shadow-md">
                    <button onclick="toggleBoutique('${{b.id}}')" class="w-full text-left p-3 flex items-center justify-between gap-3 bg-slate-950/60 hover:bg-slate-800/80 transition cursor-pointer">
                        <div class="flex items-center gap-2.5 min-w-0">
                            <div class="w-8 h-8 rounded-xl bg-slate-900 flex items-center justify-center ${{b.color}} shrink-0 shadow"><i class="fa-solid ${{b.icon}} text-sm"></i></div>
                            <div class="min-w-0">
                                <strong class="text-xs font-bold text-white block truncate">${{b.name}}</strong>
                                <span class="text-[9px] font-mono text-slate-400 block truncate">${{b.tag}}</span>
                            </div>
                        </div>
                        <div class="flex items-center gap-2 shrink-0">
                            <span class="text-[9px] font-mono font-bold text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded-lg border border-cyan-500/30">Top 3</span>
                            <i class="fa-solid fa-chevron-${{isOpen ? 'up' : 'down'}} text-slate-500 text-xs"></i>
                        </div>
                    </button>

                    ${{isOpen ? `
                        <div class="p-3 bg-slate-950 border-t border-slate-800/80 space-y-2 fade-in">
                            ${{top3.map(p => `
                                <div class="bg-slate-900 rounded-xl p-2 flex items-center justify-between gap-2 border border-slate-800">
                                    <img src="${{p.img}}" alt="${{p.nombre}}" class="w-10 h-10 object-contain rounded bg-slate-950 p-0.5 shrink-0" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';" />
                                    <div class="min-w-0 flex-1">
                                        <h5 class="text-xs font-bold text-white line-clamp-1">${{p.nombre}}</h5>
                                        <span class="text-amber-400 font-mono font-black text-xs">$${{p.precio.toFixed(2)}}</span>
                                    </div>
                                    <button onclick="addToCartApp('${{p.sku}}')" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 p-2 rounded-lg text-xs border border-cyan-500/30"><i class="fa-solid fa-cart-plus"></i></button>
                                </div>
                            `).join('')}}
                            <div class="pt-1 text-center">
                                <a href="${{b.url}}" class="text-[11px] font-mono font-bold text-cyan-400 hover:underline">Ir a boutique completa &rarr;</a>
                            </div>
                        </div>
                    ` : ''}}
                </div>
            `;
        }}).join('');
    }}

    function toggleBoutique(id) {{
        activeBoutiqueId = activeBoutiqueId === id ? null : id;
        renderBoutiquesAccordions();
    }}

    function onMobileSearch(e) {{
        const q = e.target.value.toLowerCase().trim();
        const box = document.getElementById("mobile-autocomplete-box");
        const clearBtn = document.getElementById("clear-search-btn");
        if (clearBtn) clearBtn.classList.toggle("hidden", q.length === 0);

        if (!q) {{ box.classList.add("hidden"); return; }}
        const matches = appProducts.filter(p => `${{p.sku}} ${{p.nombre}} ${{p.desc}} ${{(p.tokens||[]).join(' ')}}`.toLowerCase().includes(q));

        if (matches.length === 0) {{
            const best = appProducts.slice(0, 3);
            box.innerHTML = `
                <div class="p-2 space-y-1.5 text-xs text-center">
                    <span class="text-white font-bold block">No hay coincidencias para "${{q}}"</span>
                    <span class="text-[10px] text-amber-400 font-mono block">Te recomendamos los más pedidos:</span>
                    ${{best.map(i => `
                        <div class="bg-slate-950 p-2 rounded-xl flex justify-between items-center text-left">
                            <span class="truncate max-w-[180px] text-white font-bold">${{i.nombre}}</span>
                            <button onclick="addToCartApp('${{i.sku}}')" class="bg-emerald-600 text-slate-950 font-black px-2 py-0.5 rounded text-[10px]">+1 Clic</button>
                        </div>
                    `).join('')}}
                </div>
            `;
            box.classList.remove("hidden");
            return;
        }}

        box.innerHTML = matches.slice(0, 5).map(item => `
            <div class="bg-slate-950 rounded-xl p-2 flex items-center justify-between gap-2 border border-slate-800">
                <div class="min-w-0 flex-1">
                    <h5 class="text-xs font-bold text-white truncate">${{item.nombre}}</h5>
                    <span class="text-amber-400 font-mono font-bold text-xs">$${{item.precio.toFixed(2)}}</span>
                </div>
                <button onclick="addToCartApp('${{item.sku}}')" class="bg-slate-800 text-cyan-300 p-1.5 rounded-lg text-xs border border-cyan-500/30"><i class="fa-solid fa-cart-plus"></i></button>
            </div>
        `).join('');
        box.classList.remove("hidden");
    }}

    function clearMobileSearch() {{
        document.getElementById("mobileSearchInput").value = '';
        document.getElementById("clear-search-btn").classList.add("hidden");
        document.getElementById("mobile-autocomplete-box").classList.add("hidden");
    }}

    function generatePIN() {{
        generatedPIN = Math.floor(1000 + Math.random() * 9000).toString();
        const el = document.getElementById("delivery-pin-display");
        if (el) el.innerText = generatedPIN;
    }}

    function addToCartApp(sku) {{
        const item = appProducts.find(p => p.sku === sku);
        if (!item) return;
        let cart = [];
        try {{
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cart = JSON.parse(raw);
        }} catch(e) {{}}
        const exist = cart.find(i => i.sku === sku);
        if (exist) {{ exist.quantity = (parseInt(exist.quantity) || 1) + 1; }}
        else {{ cart.push({{ ...item, quantity: 1 }}); }}
        localStorage.setItem('ecosystem_global_cart', JSON.stringify(cart));
        syncAppCart();
        const badge = document.getElementById("app-cart-badge");
        if (badge) {{ badge.classList.remove("cart-pop"); void badge.offsetWidth; badge.classList.add("cart-pop"); }}
    }}

    function buyNowApp(sku) {{
        addToCartApp(sku);
        toggleCartModal();
    }}

    function syncAppCart() {{
        let cart = [];
        try {{
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cart = JSON.parse(raw);
        }} catch(e) {{}}
        const count = cart.reduce((sum, i) => sum + (parseInt(i.quantity) || 0), 0);
        const subtotal = cart.reduce((sum, i) => sum + ((parseFloat(i.precio) || 0) * (parseInt(i.quantity) || 0)), 0);
        const isFree = subtotal >= 1500 || count >= 10;
        const shippingFinal = isFree ? 0 : (currentShippingCost !== null ? currentShippingCost : 0);
        const total = subtotal + shippingFinal;

        document.getElementById("app-cart-badge").innerText = count;
        document.getElementById("modal-subtotal-txt").innerText = `$${{subtotal.toFixed(2)}} MXN`;
        document.getElementById("modal-shipping-txt").innerText = isFree ? "GRATIS ($0.00)" : (currentShippingCost !== null ? `$${{shippingFinal.toFixed(2)}} MXN` : "Pendiente Cotizar");
        document.getElementById("modal-total-txt").innerText = `$${{total.toFixed(2)}} MXN`;

        const container = document.getElementById("modal-cart-items");
        if (!container) return;
        if (cart.length === 0) {{
            container.innerHTML = '<div class="text-center py-6 text-slate-500 text-xs">Sin artículos en la orden.</div>';
            return;
        }}
        container.innerHTML = cart.map(i => `
            <div class="bg-slate-950 p-2 rounded-xl border border-slate-800 flex justify-between items-center text-xs">
                <span class="text-white truncate max-w-[180px]">${{i.nombre}} (x${{i.quantity}})</span>
                <span class="text-amber-400 font-mono font-bold">$${{(parseFloat(i.precio)*parseInt(i.quantity)).toFixed(2)}}</span>
            </div>
        `).join('');
    }}

    function toggleCartModal() {{
        generatePIN();
        document.getElementById("appCartModal").classList.toggle("hidden");
        syncAppCart();
    }}

    function sendOrderViaWhatsApp() {{
        let cart = [];
        try {{
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cart = JSON.parse(raw);
        }} catch(e) {{}}
        if (cart.length === 0) {{ alert('Agrega al menos un artículo a tu orden.'); return; }}

        const calle = document.getElementById("inputCalle").value.trim();
        const num = document.getElementById("inputNum").value.trim();
        const col = document.getElementById("inputColonia").value.trim();
        const mun = document.getElementById("selectMunicipio").value;

        if (!calle || !num || !col || !mun) {{
            alert('Por favor cotiza primero tu domicilio completo (Calle, Número, Colonia y Municipio).');
            return;
        }}

        const subtotal = cart.reduce((sum, i) => sum + ((parseFloat(i.precio) || 0) * (parseInt(i.quantity) || 0)), 0);
        const shipping = subtotal >= 1500 ? 0 : (currentShippingCost || 35);
        const total = subtotal + shipping;

        let msg = `🛵 *ORDEN DESPACHO UBER FLASH - BAZAR NFL*%0A`;
        msg += `📍 *Origen:* Pedro Moreno 501 A, GDL Centro%0A`;
        msg += `🏠 *Destino:* ${{calle}} #${{num}}, Col. ${{col}}, ${{mun.toUpperCase()}}%0A`;
        msg += `🔐 *PIN Uber:* ${{generatedPIN}}%0A%0A`;
        msg += `📦 *PRODUCTOS:*%0A`;
        cart.forEach(i => {{
            msg += `• *${{i.quantity}}x* ${{i.nombre}} ($${{(parseFloat(i.precio)*parseInt(i.quantity)).toFixed(2)}})%0A`;
        }});
        msg += `%0A💵 *Subtotal:* $${{subtotal.toFixed(2)}} MXN`;
        msg += `%0A🛵 *Flete Uber Flash:* ${{shipping === 0 ? 'GRATIS' : '$' + shipping.toFixed(2) + ' MXN'}}`;
        msg += `%0A💰 *TOTAL SPEI:* $${{total.toFixed(2)}} MXN%0A%0A`;
        msg += `_Adjunto comprobante de pago bancario para enviar la moto._`;

        window.open(`https://wa.me/523337271440?text=${{msg}}`, '_blank');
    }}

    document.addEventListener("DOMContentLoaded", () => {{
        renderMobileList();
        renderBoutiquesAccordions();
        syncAppCart();
    }});
    </script>
</body>
</html>
"""

# Guardar app.html
for p in [os.path.join(BASE_DIR, "app.html"), os.path.join(BASE_DIR, "sitios-web", "app.html")]:
    if os.path.exists(os.path.dirname(p)):
        with open(p, "w", encoding="utf-8") as f:
            f.write(APP_HTML_CODE)
        print(f"✓ App móvil actualizada con validación y 2 productos por pantalla: {p}")

# --------------------------------------------------------------------------
# 2. ACTUALIZAR EL PORTAL MATRIZ (index.html) CON FLECHAS FLOTANTES (< y >)
# --------------------------------------------------------------------------
for p in [os.path.join(BASE_DIR, "index.html"), os.path.join(BASE_DIR, "sitios-web", "index.html")]:
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            html = f.read()

        # Asegurar función de scroll con flechas
        scroll_fn = """
    function scrollCarousel(id, direction) {
        const el = document.getElementById(id);
        if (el) {
            const amount = el.clientWidth * 0.85;
            el.scrollBy({ left: direction * amount, behavior: 'smooth' });
        }
    }
        """
        if "function scrollCarousel" not in html:
            html = html.replace("function renderShowcase() {", scroll_fn + "\n    function renderShowcase() {")

        with open(p, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ Portal Matriz actualizado con flechas en carrusel: {p}")

# Desplegar cambios a GitHub Pages
print("\n=== DESPLEGANDO A GITHUB PAGES ===")
sitios_repo = os.path.join(BASE_DIR, "sitios-web")
if os.path.exists(os.path.join(sitios_repo, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=sitios_repo, check=True)
    subprocess.run(["git", "commit", "-m", "feat(app): validador estricto de domicilio Uber y carrusel 2 productos con flechas", "--allow-empty"], cwd=sitios_repo, capture_output=True)
    res_sub = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sitios_repo, capture_output=True, text=True)
    print(f"🟢 Submódulo sitios-web -> Push: {'OK' if res_sub.returncode == 0 else res_sub.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(ecosistema): Validador Uber estricto y carrusel 2 cols con flechas desplegados", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
