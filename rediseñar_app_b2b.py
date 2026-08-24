import os
import subprocess

BASE_DIR = r"E:\sitios web"

print("=" * 80)
print("REESTRUCTURANDO APP MÓVIL: COTIZADOR POR DOMICILIO + 7 BOUTIQUES + ZERO-SEARCH RECOVERY")
print("=" * 80)

APP_REDESIGN_HTML = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>BAZAR NFL App | Portal B2B Técnicos & Talleres GDL</title>
    
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
        .fade-in { animation: fadeIn 0.15s ease-in-out forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen flex flex-col justify-between selection:bg-cyan-500 selection:text-slate-950 pb-20 select-none">

    <!-- CABECERA MÓVIL FIJA -->
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
                        <span class="bg-cyan-500/20 text-cyan-300 font-mono font-bold text-[9px] px-1.5 py-0.2 rounded border border-cyan-500/40">APP B2B</span>
                    </div>
                    <span class="text-[10px] font-mono text-slate-400 block leading-tight">Pedro Moreno 501 A • GDL</span>
                </div>
            </div>

            <!-- Botón de Canasta -->
            <button onclick="toggleCartModal()" class="relative bg-slate-800 border border-slate-700 p-2.5 rounded-2xl text-cyan-400 active:scale-90 transition shadow">
                <i class="fa-solid fa-cart-shopping text-base"></i>
                <span id="app-cart-badge" class="absolute -top-1.5 -right-1.5 bg-amber-500 text-slate-950 font-mono font-black text-[10px] rounded-full w-5 h-5 flex items-center justify-center shadow">0</span>
            </button>
        </div>
    </header>

    <!-- CUERPO PRINCIPAL -->
    <main class="max-w-md mx-auto w-full px-4 py-4 space-y-4 flex-1">
        
        <!-- 1. COTIZADOR POR DOMICILIO REAL (CÁLCULO AUTOMÁTICO DE FLETE) -->
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-3xl shadow-xl space-y-3">
            <div class="flex items-center justify-between">
                <span class="text-xs font-mono font-bold text-white flex items-center gap-1.5">
                    <i class="fa-solid fa-motorcycle text-amber-400"></i> Cotizar Envío a tu Domicilio
                </span>
                <span id="shipping-rate-badge" class="text-xs font-mono font-black text-emerald-400 bg-emerald-950/40 px-2.5 py-0.5 rounded-lg border border-emerald-500/30">$35.00 MXN</span>
            </div>

            <!-- Campo de Texto para Dirección / Colonia -->
            <div class="space-y-1.5">
                <label class="text-[11px] text-slate-300 font-bold block">Pon tu domicilio para calcular el flete exacto:</label>
                <div class="flex items-center bg-slate-950 border border-slate-800 focus-within:border-cyan-400 rounded-2xl px-3 py-2 gap-2 shadow-inner">
                    <i class="fa-solid fa-location-dot text-slate-500 text-xs"></i>
                    <input 
                        type="text" 
                        id="userAddressInput" 
                        placeholder="Ej. Calle, Colonia o Zona (Chapultepec, Centro, Zapopan)..." 
                        class="flex-1 bg-transparent border-0 outline-none text-xs text-white font-medium placeholder-slate-500"
                        oninput="onAddressInput(event)"
                    />
                </div>
            </div>

            <div class="flex items-center justify-between text-[10px] font-mono text-slate-400 pt-0.5">
                <span id="distance-calc-info"><i class="fa-solid fa-route text-cyan-400 mr-1"></i> Despacho desde Pedro Moreno 501 A</span>
                <span class="text-amber-400 font-bold">Gratis desde $1,500</span>
            </div>
        </div>

        <!-- 2. SÚPER-BUSCADOR SEARCH-FIRST MULTI-TOKEN CON ZERO-RESULTS RECOVERY -->
        <div class="relative">
            <div class="flex items-center bg-white rounded-2xl px-3.5 py-2 gap-2 shadow-lg border-2 border-cyan-400">
                <i class="fa-solid fa-magnifying-glass text-slate-400 text-sm"></i>
                <input 
                    type="text" 
                    id="mobileSearchInput" 
                    autocomplete="off"
                    spellcheck="false"
                    placeholder="Busca por pieza, SKU, falla o marca (ej. RAM, 4070, paleta)..." 
                    class="flex-1 bg-transparent border-0 outline-none text-slate-950 font-bold text-xs placeholder-slate-400"
                    oninput="onMobileSearch(event)"
                />
                <button onclick="clearMobileSearch()" id="clear-search-btn" class="hidden text-slate-400 hover:text-slate-600 text-xs px-1 font-bold">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>

            <!-- Desplegable Reactivo de Búsqueda -->
            <div id="mobile-autocomplete-box" class="hidden absolute top-full left-0 right-0 mt-2 bg-slate-900 border-2 border-cyan-500/60 rounded-2xl shadow-2xl z-40 p-2.5 flex flex-col gap-2 max-h-80 overflow-y-auto no-scrollbar"></div>
        </div>

        <!-- 3. LAS 7 BOUTIQUES OFICIALES (DESPLIEGUE DE LOS 3 MÁS VENDIDOS AL TOCAR) -->
        <div class="space-y-2.5">
            <div class="flex justify-between items-center px-1">
                <span class="text-xs font-mono font-bold text-white uppercase flex items-center gap-1.5">
                    <i class="fa-solid fa-layer-group text-amber-400"></i> Nuestras 7 Boutiques
                </span>
                <span class="text-[9px] font-mono text-cyan-400 font-bold">Toca para ver los 3 más vendidos</span>
            </div>

            <div class="grid grid-cols-1 gap-2" id="boutiques-accordion-list">
                <!-- 7 Boutiques inyectadas dinámicamente -->
            </div>
        </div>

        <!-- 4. CATÁLOGO GENERAL DE REFACCIONES Y PRODUCTOS -->
        <div class="space-y-2 pt-2">
            <div class="flex justify-between items-center px-1">
                <span class="text-xs font-mono font-bold text-slate-400 uppercase" id="catalog-section-title">Artículos de Entrega Inmediata</span>
                <span class="text-[10px] font-mono text-emerald-400 font-bold"><i class="fa-solid fa-bolt"></i> Stock Local</span>
            </div>
            <div id="mobile-product-list" class="space-y-2.5"></div>
        </div>

        <!-- BADGES GOOGLE PLAY Y APPLE APP STORE -->
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-3xl shadow-xl space-y-3">
            <div class="flex items-center justify-between">
                <span class="text-xs font-mono font-bold text-white flex items-center gap-1.5">
                    <i class="fa-solid fa-mobile-screen text-cyan-400"></i> Descargar Aplicación Oficial
                </span>
                <span class="text-[9px] font-mono font-bold text-emerald-400 bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-500/30">PWA 2026</span>
            </div>

            <div class="grid grid-cols-2 gap-2.5">
                <button onclick="installPWA()" class="flex items-center justify-center gap-2 bg-slate-950 border border-slate-800 hover:border-emerald-400 py-2.5 px-2.5 rounded-2xl transition active:scale-95 shadow cursor-pointer">
                    <i class="fa-brands fa-google-play text-base text-emerald-400"></i>
                    <div class="text-left">
                        <span class="text-[8px] font-mono text-slate-400 block leading-none">Android</span>
                        <strong class="text-[11px] text-white block leading-none font-bold">Google Play</strong>
                    </div>
                </button>
                <button onclick="showiOSInstallGuide()" class="flex items-center justify-center gap-2 bg-slate-950 border border-slate-800 hover:border-cyan-400 py-2.5 px-2.5 rounded-2xl transition active:scale-95 shadow cursor-pointer">
                    <i class="fa-brands fa-apple text-lg text-white"></i>
                    <div class="text-left">
                        <span class="text-[8px] font-mono text-slate-400 block leading-none">iPhone / iOS</span>
                        <strong class="text-[11px] text-white block leading-none font-bold">App Store</strong>
                    </div>
                </button>
            </div>
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
                <i class="fa-solid fa-bolt text-base"></i>
                <span class="text-[9px] font-mono">B2B App</span>
            </button>
            <a href="https://wa.me/523337271440" target="_blank" class="flex flex-col items-center gap-1 text-emerald-400">
                <i class="fa-brands fa-whatsapp text-base"></i>
                <span class="text-[9px] font-mono">Atención</span>
            </a>
            <button onclick="toggleCartModal()" class="flex flex-col items-center gap-1 text-amber-400">
                <i class="fa-solid fa-bag-shopping text-base"></i>
                <span class="text-[9px] font-mono">Mi Pedido</span>
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

                <div id="modal-cart-items" class="flex flex-col gap-2 overflow-y-auto max-h-[25vh] pr-1 no-scrollbar"></div>

                <!-- PIN DE SEGURIDAD GENERADO -->
                <div class="mt-3 p-3 bg-slate-950 rounded-2xl border border-emerald-500/40 flex items-center justify-between">
                    <div>
                        <span class="text-[9px] font-mono text-emerald-400 uppercase font-bold block">Código PIN de Entrega Uber:</span>
                        <span id="delivery-pin-display" class="text-xl font-mono font-black text-white tracking-widest">----</span>
                    </div>
                    <span class="text-[9px] text-slate-400 max-w-[150px] text-right">Díctalo al chofer para recibir el paquete.</span>
                </div>

                <!-- DATOS SPEI -->
                <div class="mt-3 p-3 bg-slate-950 rounded-2xl border border-slate-800 space-y-1 text-xs font-mono">
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400 text-[10px]">Banco Receptor:</span>
                        <strong class="text-white text-[11px]">BBVA México / STP</strong>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-400 text-[10px]">CLABE Interbancaria:</span>
                        <div class="flex items-center gap-1.5">
                            <span class="text-cyan-300 font-bold text-[11px]" id="clabe-txt">0123 2001 5824 9382 10</span>
                            <button onclick="copyCLABE()" class="text-[9px] bg-slate-800 hover:bg-slate-700 px-1.5 py-0.5 rounded text-slate-300 cursor-pointer">
                                <i class="fa-solid fa-copy"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="border-t border-slate-800 pt-3 space-y-2 mt-3">
                <div class="flex justify-between text-xs font-mono">
                    <span class="text-slate-400">Subtotal Piezas:</span>
                    <span id="modal-subtotal-txt" class="text-white font-bold">$0.00 MXN</span>
                </div>
                <div class="flex justify-between text-xs font-mono">
                    <span class="text-slate-400">Flete Cotizado:</span>
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

    <!-- MOTOR JS DE LA APP -->
    <script>
    // 1. Directorio de las 7 Boutiques Oficiales
    const boutiquesConfig = [
        {
            id: "pc-custom",
            name: "PC Custom Lab",
            tag: "HARDWARE & PC",
            icon: "fa-microchip",
            color: "text-cyan-400",
            url: "https://iaworldcenter-creator.github.io/pc-custom-lab/"
        },
        {
            id: "viamx",
            name: "Vía MX Boutique",
            tag: "DEPARTAMENTAL",
            icon: "fa-gem",
            color: "text-cyan-300",
            url: "https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/"
        },
        {
            id: "cigarros",
            name: "Cigarros Bazar",
            tag: "TABACOS & PUROS",
            icon: "fa-smoking",
            color: "text-amber-400",
            url: "https://iaworldcenter-creator.github.io/cigarros-bazar/"
        },
        {
            id: "dulces",
            name: "Dulces Bazar",
            tag: "DULCERÍA & BOTANAS",
            icon: "fa-candy-cane",
            color: "text-pink-400",
            url: "https://iaworldcenter-creator.github.io/dulces-bazar/"
        },
        {
            id: "kiosco",
            name: "Kiosco Digital",
            tag: "REVISTAS & PRENSA",
            icon: "fa-newspaper",
            color: "text-indigo-400",
            url: "https://iaworldcenter-creator.github.io/kiosco-digital/"
        },
        {
            id: "puesto",
            name: "Mi Puesto Bazar",
            tag: "NOVEDADES & GADGETS",
            icon: "fa-store",
            color: "text-emerald-400",
            url: "https://iaworldcenter-creator.github.io/mi-puesto-bazar/"
        },
        {
            id: "ofertas",
            name: "Ofertas & Liquidaciones",
            tag: "OUTLET DIRECTO B2B",
            icon: "fa-tags",
            color: "text-red-400",
            url: "https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/"
        }
    ];

    // Catálogo Maestro de Artículos
    const appProducts = [
        // PC Custom
        { sku: "PC-001", boutiqueId: "pc-custom", nombre: "Gabinete Micro-ATX con Fuente 500W Incluida", marca: "Acteck", precio: 1250.00, original: 1550.00, desc: "Fuente certificada, puertos USB 3.0 para taller.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/gabinete_negro.webp", tokens: ["gabinete", "fuente", "pc", "chasis"], sales: 95 },
        { sku: "PC-002", boutiqueId: "pc-custom", nombre: "Tarjeta Madre ASUS Prime B760M-A WiFi DDR5", marca: "ASUS", precio: 3400.00, original: 3950.00, desc: "Soporte Intel 12va/13va/14va Gen, dual M.2.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/motherboard_asus.webp", tokens: ["tarjeta madre", "asus", "placa"], sales: 82 },
        { sku: "PC-004", boutiqueId: "pc-custom", nombre: "RAM Kingston FURY Beast 16GB DDR5 5600MHz", marca: "Kingston", precio: 1250.00, original: 1500.00, desc: "Disipador de aluminio de bajo perfil.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/ram_caja.webp", tokens: ["ram", "kingston", "fury", "ddr5", "memoria"], sales: 140 },
        { sku: "PC-005", boutiqueId: "pc-custom", nombre: "SSD Kingston NV2 1TB NVMe PCIe 4.0", marca: "Kingston", precio: 1350.00, original: 1650.00, desc: "3,500 MB/s lectura ultra rápida.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/disco_solido_m2.webp", tokens: ["ssd", "kingston", "nvme", "disco"], sales: 110 },
        { sku: "PC-006", boutiqueId: "pc-custom", nombre: "Tarjeta Gráfica NVIDIA RTX 4070 Ti Super 16GB", marca: "NVIDIA", precio: 17800.00, original: 21500.00, desc: "DLSS 3, Ray Tracing para render y gaming 4K.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/gpu_nvidia.webp", tokens: ["gpu", "nvidia", "rtx", "4070", "grafica"], sales: 45 },

        // Vía MX
        { sku: "VMX-001", boutiqueId: "viamx", nombre: "Pantalla Smart TV 55 Pulgadas 4K UHD HDR10+ WiFi", marca: "Samsung", precio: 7999.00, original: 11499.00, desc: "Panel LED 4K con asistente de voz y HDMI 2.1.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_curvo_negro.webp", tokens: ["pantalla", "smart tv", "samsung", "4k"], sales: 70 },
        { sku: "VMX-003", boutiqueId: "viamx", nombre: "Freidora de Aire Digital 6.5 Litros 12 Programas", marca: "Tefal", precio: 1499.00, original: 2199.00, desc: "Canastilla antiadherente libre de BPA envolvente.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp", tokens: ["freidora", "aire", "airfryer", "tefal"], sales: 88 },
        { sku: "VMX-005", boutiqueId: "viamx", nombre: "Smartphone 5G Desbloqueado 256GB / 8GB RAM 108MP", marca: "Motorola", precio: 4899.00, original: 6499.00, desc: "Pantalla AMOLED 120Hz con batería 5000mAh.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/perifericos_combo_1.webp", tokens: ["celular", "telefono", "smartphone", "motorola"], sales: 65 },

        // Cigarros
        { sku: "CIG-001", boutiqueId: "cigarros", nombre: "Cigarros Marlboro Gold Original (Cajetilla 20)", marca: "Marlboro", precio: 82.00, original: 95.00, desc: "Sabor suave y filtro blanco de importación.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["cigarros", "marlboro", "gold", "tabaco"], sales: 210 },
        { sku: "CIG-003", boutiqueId: "cigarros", nombre: "Puro Habanos Cohiba Siglo VI Tubo Individual", marca: "Cohiba", precio: 850.00, original: 1100.00, desc: "Puro cubano hecho a mano con notas amaderadas.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["puro", "cohiba", "siglo vi", "habano"], sales: 55 },
        { sku: "CIG-005", boutiqueId: "cigarros", nombre: "Encendedor Vintage Recargable a Gas", marca: "Clipper Pro", precio: 195.00, original: 260.00, desc: "Cuerpo metálico cepillado con piedra cambiable.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["encendedor", "clipper", "fuego", "gas"], sales: 78 },

        // Dulces
        { sku: "DUL-001", boutiqueId: "dulces", nombre: "Paleta Payaso Ricolino (Caja 15 piezas)", marca: "Ricolino", precio: 245.00, original: 290.00, desc: "Malvavisco con chocolate y gomitas tradicionales.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp", tokens: ["paleta", "payaso", "ricolino", "dulces"], sales: 180 },
        { sku: "DUL-002", boutiqueId: "dulces", nombre: "Mazapán De La Rosa Gigante (Caja 20 piezas)", marca: "De La Rosa", precio: 160.00, original: 195.00, desc: "Dulce tradicional de cacahuate tostado.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp", tokens: ["mazapan", "de la rosa", "cacahuate"], sales: 250 },
        { sku: "DUL-003", boutiqueId: "dulces", nombre: "Rocaleta Sonrics con Centro de Goma (Bolsa 30)", marca: "Sonrics", precio: 185.00, original: 230.00, desc: "Caramelo con 4 capas de chile ácido y chicle.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp", tokens: ["rocaleta", "sonrics", "chile", "paleta"], sales: 130 },

        // Kiosco
        { sku: "KIO-001", boutiqueId: "kiosco", nombre: "Suscripción Digital Anual Revista National Geographic", marca: "RBA", precio: 599.00, original: 850.00, desc: "12 ediciones digitales HD + archivo histórico.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_plano_blanco.webp", tokens: ["revista", "national geographic", "natgeo", "digital"], sales: 90 },
        { sku: "KIO-002", boutiqueId: "kiosco", nombre: "Suscripción Revista Muy Interesante Digital (1 Año)", marca: "Zinet", precio: 450.00, original: 620.00, desc: "Acceso total a reportajes de ciencia y tecnología.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_plano_blanco.webp", tokens: ["revista", "muy interesante", "ciencia"], sales: 75 },

        // Mi Puesto
        { sku: "PUE-001", boutiqueId: "puesto", nombre: "Lentes Inteligentes Bluetooth con Audio y Micrófono", marca: "SmartVision", precio: 680.00, original: 950.00, desc: "Llamadas y música con protección UV.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_gamer_thumb.webp", tokens: ["lentes", "bluetooth", "audio", "musica"], sales: 115 },
        { sku: "PUE-002", boutiqueId: "puesto", nombre: "Consola Retro Portátil con 500 Juegos Clásicos", marca: "Sup Game", precio: 290.00, original: 390.00, desc: "Batería recargable y salida para TV.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_gemini_thumb.webp", tokens: ["consola", "retro", "videojuegos", "juegos"], sales: 135 },
        { sku: "PUE-003", boutiqueId: "puesto", nombre: "Cable USB-C a USB-C 65W Reforzado 2M", marca: "Baseus", precio: 120.00, original: 180.00, desc: "Carga rápida para celulares y laptops.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/fuente_modular.webp", tokens: ["cable", "cargador", "usb c", "carga rapida"], sales: 190 },

        // Ofertas
        { sku: "OFE-001", boutiqueId: "ofertas", nombre: "Lote de Remate Electrónica y Accesorios Grado A", marca: "Sony / Varios", precio: 2490.00, original: 3800.00, desc: "Paquete surtido de oportunidad comercial con garantía.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/software_estante_madera.webp", tokens: ["lote", "remate", "liquidacion", "oferta"], sales: 40 },
        { sku: "OFE-003", boutiqueId: "ofertas", nombre: "Kit de Herramientas Mecánicas 168 Piezas Maletín", marca: "Stanley", precio: 899.00, original: 1299.00, desc: "Matraca y dados milimétricos al costo.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/software_estante_muro.webp", tokens: ["herramientas", "stanley", "maletin"], sales: 60 }
    ];

    let currentShippingCost = 35;
    let generatedPIN = "";
    let activeBoutiqueId = null;

    // ------------------------------------------------------------------------
    // 1. COTIZADOR POR DOMICILIO AUTOMÁTICO
    // ------------------------------------------------------------------------
    function onAddressInput(e) {
        const text = e.target.value.toLowerCase().trim();
        const badge = document.getElementById("shipping-rate-badge");
        const info = document.getElementById("distance-calc-info");

        if (!text) {
            currentShippingCost = 35;
            badge.innerText = "$35.00 MXN";
            info.innerHTML = '<i class="fa-solid fa-route text-cyan-400 mr-1"></i> Despacho desde Pedro Moreno 501 A';
            syncAppCart();
            return;
        }

        // Estimación automática según colonia/zona de GDL
        if (text.includes("zapopan") || text.includes("minerva") || text.includes("providencia") || text.includes("tlaquepaque") || text.includes("colinas") || text.includes("estancia")) {
            currentShippingCost = 52;
            badge.innerText = "$52.00 MXN";
            info.innerHTML = '📍 <strong class="text-amber-400">Zona Poniente/Sur (~4 km)</strong> • Uber Flash';
        } else if (text.includes("tonala") || text.includes("tonalá") || text.includes("tlajomulco") || text.includes("periferico") || text.includes("periférico") || text.includes("bugambilias")) {
            currentShippingCost = 75;
            badge.innerText = "$75.00 MXN";
            info.innerHTML = '📍 <strong class="text-amber-400">Zona Periférica (~8+ km)</strong> • Uber Flash';
        } else {
            // Centro, Calzada, Chapultepec, Moderna, Americana, San Juan de Dios
            currentShippingCost = 35;
            badge.innerText = "$35.00 MXN";
            info.innerHTML = '📍 <strong class="text-emerald-400">Zona Centro / Cercana (~1.8 km)</strong> • Uber Flash Exprés';
        }

        syncAppCart();
    }

    // ------------------------------------------------------------------------
    // 2. RENDERIZAR LAS 7 BOUTIQUES Y DESPLEGAR LOS 3 MÁS VENDIDOS
    // ------------------------------------------------------------------------
    function renderBoutiquesAccordions() {
        const container = document.getElementById("boutiques-accordion-list");
        if (!container) return;

        container.innerHTML = boutiquesConfig.map(b => {
            const top3 = appProducts.filter(p => p.boutiqueId === b.id).sort((a,b) => b.sales - a.sales).slice(0, 3);
            const isOpen = activeBoutiqueId === b.id;

            return `
                <div class="bg-slate-900 border ${isOpen ? 'border-cyan-400' : 'border-slate-800'} rounded-2xl overflow-hidden shadow-md transition">
                    
                    <!-- Botón Principal de la Boutique -->
                    <button onclick="toggleBoutique('${b.id}')" class="w-full text-left p-3 flex items-center justify-between gap-3 bg-slate-950/60 hover:bg-slate-800/80 transition cursor-pointer">
                        <div class="flex items-center gap-2.5 min-w-0">
                            <div class="w-8 h-8 rounded-xl bg-slate-900 flex items-center justify-center ${b.color} shrink-0 shadow">
                                <i class="fa-solid ${b.icon} text-sm"></i>
                            </div>
                            <div class="min-w-0">
                                <strong class="text-xs font-bold text-white block group-hover:text-cyan-300 truncate">${b.name}</strong>
                                <span class="text-[9px] font-mono text-slate-400 block truncate">${b.tag}</span>
                            </div>
                        </div>
                        <div class="flex items-center gap-2 shrink-0">
                            <span class="text-[9px] font-mono font-bold text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded-lg border border-cyan-500/30">Top 3</span>
                            <i class="fa-solid fa-chevron-${isOpen ? 'up' : 'down'} text-slate-500 text-xs transition"></i>
                        </div>
                    </button>

                    <!-- Lista Desplegable de los 3 Más Vendidos -->
                    ${isOpen ? `
                        <div class="p-3 bg-slate-950 border-t border-slate-800/80 space-y-2.5 fade-in">
                            ${top3.map(p => `
                                <div class="bg-slate-900 rounded-xl p-2.5 flex items-center justify-between gap-2.5 border border-slate-800 shadow-sm">
                                    <img src="${p.img}" alt="${p.nombre}" class="w-10 h-10 object-contain rounded bg-slate-950 p-0.5 shrink-0" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';" />
                                    <div class="min-w-0 flex-1">
                                        <span class="text-[8px] font-mono text-cyan-400 font-bold block">${p.sku}</span>
                                        <h5 class="text-xs font-bold text-white line-clamp-1">${p.nombre}</h5>
                                        <div class="flex items-center gap-1.5">
                                            <span class="text-amber-400 font-mono font-black text-xs">$${p.precio.toFixed(2)}</span>
                                            ${p.original ? `<span class="text-[9px] font-mono text-red-400 line-through">$${p.original.toFixed(2)}</span>` : ''}
                                        </div>
                                    </div>
                                    <div class="flex items-center gap-1 shrink-0">
                                        <button onclick="addToCartApp('${p.sku}')" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 p-2 rounded-lg text-xs active:scale-90 transition shadow border border-cyan-500/30" title="Agregar">
                                            <i class="fa-solid fa-cart-plus"></i>
                                        </button>
                                        <button onclick="buyNowApp('${p.sku}')" class="bg-gradient-to-r from-amber-400 to-amber-500 text-slate-950 font-black px-2.5 py-1.5 rounded-lg text-[10px] active:scale-90 transition shadow">
                                            Comprar
                                        </button>
                                    </div>
                                </div>
                            `).join('')}

                            <div class="pt-1 text-center">
                                <a href="${b.url}" class="text-[11px] font-mono font-bold text-cyan-400 hover:underline inline-flex items-center gap-1">
                                    <span>Ir a la tienda web completa de ${b.name}</span> <i class="fa-solid fa-arrow-right text-[9px]"></i>
                                </a>
                            </div>
                        </div>
                    ` : ''}

                </div>
            `;
        }).join('');
    }

    function toggleBoutique(boutiqueId) {
        activeBoutiqueId = activeBoutiqueId === boutiqueId ? null : boutiqueId;
        renderBoutiquesAccordions();
    }

    // ------------------------------------------------------------------------
    // 3. BÚSQUEDA MULTI-TOKEN CON ZERO-RESULTS RECOVERY
    // ------------------------------------------------------------------------
    function searchMultiToken(query) {
        if (!query || !query.trim()) return [];
        const q = query.toLowerCase().trim();
        const tokens = q.split(/\s+/).filter(t => t.length > 0);

        return appProducts.filter(item => {
            const fullSearch = `${item.sku} ${item.nombre} ${item.marca} ${item.desc} ${(item.tokens || []).join(' ')}`.toLowerCase();
            return tokens.every(token => fullSearch.includes(token));
        });
    }

    function onMobileSearch(e) {
        const val = e.target.value;
        const clearBtn = document.getElementById("clear-search-btn");
        if (clearBtn) clearBtn.classList.toggle("hidden", val.length === 0);

        renderMobileAutocomplete(val);
    }

    function renderMobileAutocomplete(val) {
        const box = document.getElementById("mobile-autocomplete-box");
        if (!val || val.trim().length < 1) {
            box.classList.add("hidden");
            return;
        }

        const matches = searchMultiToken(val);

        // ZERO-RESULTS RECOVERY: Si no hay resultados, sugerir los más vendidos
        if (matches.length === 0) {
            const bestSellers = [...appProducts].sort((a,b) => b.sales - a.sales).slice(0, 3);
            box.innerHTML = `
                <div class="p-2 space-y-2">
                    <div class="text-center pb-2 border-b border-slate-800">
                        <span class="text-xs font-bold text-white block">No encontramos coincidencias para "${val}"</span>
                        <span class="text-[10px] text-amber-400 font-mono">Te recomendamos los más pedidos en Pedro Moreno 501 A:</span>
                    </div>
                    ${bestSellers.map(item => `
                        <div class="bg-slate-950 rounded-xl p-2 flex items-center justify-between gap-2 shadow">
                            <div class="min-w-0 flex-1">
                                <span class="text-[8px] font-mono text-cyan-400 font-bold block">${item.sku}</span>
                                <h5 class="text-xs font-bold text-white truncate">${item.nombre}</h5>
                                <span class="text-amber-400 font-mono font-bold text-xs">$${item.precio.toFixed(2)} MXN</span>
                            </div>
                            <button onclick="addToCartApp('${item.sku}')" class="bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-black px-2.5 py-1 rounded-lg text-[10px] uppercase">
                                +1 Clic
                            </button>
                        </div>
                    `).join('')}
                </div>
            `;
            box.classList.remove("hidden");
            return;
        }

        // Resultados coincidentes
        box.innerHTML = matches.slice(0, 5).map(item => `
            <div class="bg-slate-950 rounded-xl p-2.5 flex items-center justify-between gap-2.5 border border-slate-800 shadow">
                <div class="min-w-0 flex-1">
                    <span class="text-[9px] font-mono text-cyan-400 font-bold block">${item.sku} &bull; ${item.marca}</span>
                    <h5 class="text-xs font-bold text-white truncate">${item.nombre}</h5>
                    <div class="flex items-center gap-1.5 mt-0.5">
                        <span class="text-amber-400 font-mono font-bold text-xs">$${item.precio.toFixed(2)}</span>
                        ${item.original ? `<span class="text-[9px] font-mono text-red-400 line-through">$${item.original.toFixed(2)}</span>` : ''}
                    </div>
                </div>
                <div class="flex items-center gap-1 shrink-0">
                    <button onclick="addToCartApp('${item.sku}')" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 p-2 rounded-lg text-xs active:scale-90 shadow border border-cyan-500/30">
                        <i class="fa-solid fa-cart-plus"></i>
                    </button>
                    <button onclick="buyNowApp('${item.sku}')" class="bg-gradient-to-r from-amber-400 to-amber-500 text-slate-950 font-black px-2.5 py-1.5 rounded-lg text-[10px] active:scale-90 shadow">
                        Comprar
                    </button>
                </div>
            </div>
        `).join('');

        box.classList.remove("hidden");
    }

    function clearMobileSearch() {
        const input = document.getElementById("mobileSearchInput");
        input.value = '';
        document.getElementById("clear-search-btn").classList.add("hidden");
        document.getElementById("mobile-autocomplete-box").classList.add("hidden");
    }

    // ------------------------------------------------------------------------
    // 4. RENDERIZADO DEL CATÁLOGO DE REFACCIONES
    // ------------------------------------------------------------------------
    function renderMobileList(items = appProducts) {
        const container = document.getElementById("mobile-product-list");
        if (!container) return;

        container.innerHTML = items.map(p => {
            const discountPct = p.original ? Math.round((1 - (p.precio / p.original)) * 100) : 0;
            return `
                <div class="bg-slate-900 border border-slate-800 rounded-2xl p-3.5 flex items-center justify-between gap-3 shadow-md hover:border-cyan-500/40 transition">
                    <img src="${p.img}" alt="${p.nombre}" class="w-14 h-14 object-contain rounded-xl bg-slate-950 p-1 shrink-0" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';" />
                    
                    <div class="min-w-0 flex-1">
                        <div class="flex items-center gap-1.5 mb-0.5">
                            <span class="text-[9px] font-mono text-cyan-400 font-bold">${p.sku}</span>
                            ${discountPct > 0 ? `<span class="bg-red-600 text-white text-[8px] font-mono font-bold px-1.5 py-0.2 rounded">-${discountPct}%</span>` : ''}
                        </div>
                        <h4 class="text-xs font-bold text-white line-clamp-1">${p.nombre}</h4>
                        <div class="flex items-baseline gap-2 mt-0.5">
                            <span class="text-amber-400 font-mono font-black text-sm">$${p.precio.toFixed(2)}</span>
                            ${p.original ? `<span class="text-[10px] font-mono text-red-400 line-through">$${p.original.toFixed(2)}</span>` : ''}
                        </div>
                    </div>

                    <div class="flex flex-col gap-1.5 shrink-0">
                        <button onclick="addToCartApp('${p.sku}')" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 font-bold px-3 py-1.5 rounded-xl text-[10px] flex items-center justify-center gap-1 shadow border border-cyan-500/30 active:scale-95 transition">
                            <i class="fa-solid fa-cart-plus text-[10px]"></i> <span>Carrito</span>
                        </button>
                        <button onclick="buyNowApp('${p.sku}')" class="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black px-3 py-1.5 rounded-xl text-[10px] flex items-center justify-center gap-1 shadow active:scale-95 transition">
                            <i class="fa-solid fa-bag-shopping text-[10px]"></i> <span>Comprar</span>
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    // ------------------------------------------------------------------------
    // 5. GESTIÓN DEL CARRITO GLOBAL CON CÓDIGO PIN Y PAGO SPEI
    // ------------------------------------------------------------------------
    function generatePIN() {
        generatedPIN = Math.floor(1000 + Math.random() * 9000).toString();
        const el = document.getElementById("delivery-pin-display");
        if (el) el.innerText = generatedPIN;
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

    function buyNowApp(sku) {
        addToCartApp(sku);
        toggleCartModal();
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

        const address = document.getElementById("userAddressInput").value.trim() || "Dirección a acordar por chat";
        const subtotal = cart.reduce((sum, i) => sum + ((parseFloat(i.precio) || 0) * (parseInt(i.quantity) || 0)), 0);
        const shipping = subtotal >= 1500 ? 0 : currentShippingCost;
        const total = subtotal + shipping;

        let msg = `🛵 *ORDEN DESPACHO UBER FLASH - BAZAR NFL*%0A`;
        msg += `📍 *Origen:* Pedro Moreno 501 A, GDL Centro%0A`;
        msg += `🏠 *Destino:* ${address}%0A`;
        msg += `🔐 *PIN Uber:* ${generatedPIN}%0A%0A`;
        msg += `📦 *PRODUCTOS:*%0A`;
        cart.forEach(i => {
            msg += `• *${i.quantity}x* ${i.nombre} ($${(parseFloat(i.precio)*parseInt(i.quantity)).toFixed(2)})%0A`;
        });
        msg += `%0A💵 *Subtotal:* $${subtotal.toFixed(2)} MXN`;
        msg += `%0A🛵 *Flete Uber:* ${shipping === 0 ? 'GRATIS' : '$' + shipping.toFixed(2) + ' MXN'}`;
        msg += `%0A💰 *TOTAL SPEI:* $${total.toFixed(2)} MXN%0A%0A`;
        msg += `_Adjunto comprobante de pago bancario para enviar la moto._`;

        window.open(`https://wa.me/523337271440?text=${msg}`, '_blank');
    }

    function showiOSInstallGuide() {
        alert('📲 Para instalar en iPhone / iPad:\\n\\n1. Toca el botón de Compartir (icono de caja con flecha arriba).\\n2. Desliza hacia abajo y selecciona \"Agregar a la pantalla de inicio\".\\n3. ¡Listo! Tendrás el icono del Tigre en tu teléfono.');
    }

    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
    });

    function installPWA() {
        if (deferredPrompt) {
            deferredPrompt.prompt();
            deferredPrompt.userChoice.then(() => { deferredPrompt = null; });
        } else {
            alert('Abre el menú de tu navegador y selecciona \"Instalar aplicación\" o \"Agregar a la pantalla principal\".');
        }
    }

    document.addEventListener("DOMContentLoaded", () => {
        renderBoutiquesAccordions();
        renderMobileList();
        syncAppCart();
    });
    </script>
</body>
</html>
"""

# Guardar en la raíz y en sitios-web
paths = [
    os.path.join(BASE_DIR, "app.html"),
    os.path.join(BASE_DIR, "sitios-web", "app.html")
]

for p in paths:
    if os.path.exists(os.path.dirname(p)):
        with open(p, "w", encoding="utf-8") as f:
            f.write(APP_REDESIGN_HTML)
        print(f"✓ App reestructurada guardada en: {p}")

# Desplegar a GitHub Pages
print("\n=== DESPLEGANDO APP REDISEÑADA A GITHUB PAGES ===")
sitios_repo = os.path.join(BASE_DIR, "sitios-web")
if os.path.exists(os.path.join(sitios_repo, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=sitios_repo, check=True)
    subprocess.run(["git", "commit", "-m", "feat(app): cotizador por domicilio real, 7 boutiques desplegables y zero-search recovery", "--allow-empty"], cwd=sitios_repo, capture_output=True)
    res_sub = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sitios_repo, capture_output=True, text=True)
    print(f"🟢 Submódulo sitios-web -> Push: {'OK' if res_sub.returncode == 0 else res_sub.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(ecosistema): App PWA con cotizador por domicilio, top 3 boutiques y zero-search recovery desplegada", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
