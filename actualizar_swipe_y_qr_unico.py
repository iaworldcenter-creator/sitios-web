import os
import subprocess
import json
import urllib.parse

BASE_DIR = r"E:\sitios web"
APP_URL = "https://iaworldcenter-creator.github.io/sitios-web/app.html"

print("=" * 80)
print("APLICANDO CORRECCIÓN: QR ÚNICO + SWIPE HORIZONTAL MÓVIL EN LOS 8 PORTALES")
print("=" * 80)

# Barra de navegación cruzada deslizable en móviles
NAV_BAR_MOBILE_SWIPE = f"""
<nav class="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1 w-full lg:w-auto text-[11px] font-bold text-slate-300 shrink-0">
    <a href="https://iaworldcenter-creator.github.io/sitios-web/" class="px-2.5 py-1 rounded-lg bg-amber-500/15 border border-amber-500/40 text-amber-400 hover:bg-amber-500 hover:text-slate-950 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-house text-[10px]"></i> Matriz</a>
    <a href="https://iaworldcenter-creator.github.io/pc-custom-lab/" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 hover:text-cyan-400 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-microchip text-[10px] text-cyan-400"></i> PC Custom</a>
    <a href="https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 hover:text-cyan-300 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-gem text-[10px] text-cyan-300"></i> Vía MX</a>
    <a href="https://iaworldcenter-creator.github.io/cigarros-bazar/" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 hover:text-amber-400 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-smoking text-[10px] text-amber-400"></i> Cigarros</a>
    <a href="https://iaworldcenter-creator.github.io/dulces-bazar/" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 hover:text-pink-400 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-candy-cane text-[10px] text-pink-400"></i> Dulces</a>
    <a href="https://iaworldcenter-creator.github.io/kiosco-digital/" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 hover:text-indigo-400 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-newspaper text-[10px] text-indigo-400"></i> Kiosco</a>
    <a href="https://iaworldcenter-creator.github.io/mi-puesto-bazar/" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 hover:text-emerald-400 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-store text-[10px] text-emerald-400"></i> Mi Puesto</a>
    <a href="https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 hover:text-red-400 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-tags text-[10px] text-red-400"></i> Liquidaciones</a>
</nav>
"""

# Módulo único y garantizado del Código QR
QR_SINGLE_BLOCK = f"""
                <div class="mt-4 p-4 bg-slate-950 border-2 border-cyan-400 rounded-3xl shadow-[0_0_25px_rgba(6,182,212,0.25)] text-center space-y-3">
                    <div class="flex items-center justify-center gap-2">
                        <i class="fa-solid fa-qrcode text-cyan-400 text-lg"></i>
                        <span class="text-xs font-mono font-black text-white uppercase tracking-wider">App Móvil para Talleres</span>
                    </div>

                    <div class="w-44 h-44 mx-auto bg-white p-2.5 rounded-2xl shadow-xl flex items-center justify-center">
                        <img 
                            src="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(APP_URL)}&margin=1" 
                            alt="Código QR App BAZAR NFL" 
                            class="w-full h-full object-contain rounded-lg"
                            onerror="this.onerror=null; this.src='https://quickchart.io/qr?text={urllib.parse.quote(APP_URL)}&size=300';"
                        />
                    </div>

                    <p class="text-[11px] text-slate-300 leading-snug font-medium">
                        Apunta con la cámara de tu celular a este código para abrir e instalar la App en tu teléfono.
                    </p>

                    <div class="flex flex-col gap-2 pt-1">
                        <a href="{APP_URL}" target="_blank" class="flex items-center justify-center gap-3 bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-emerald-400 py-2.5 px-3 rounded-xl text-left transition shadow group">
                            <i class="fa-brands fa-google-play text-xl text-emerald-400 group-hover:scale-110 transition"></i>
                            <div>
                                <span class="text-[8px] font-mono text-slate-400 block uppercase leading-none">Disponible vía Web / PWA</span>
                                <strong class="text-xs text-white block leading-none font-bold">Instalar en Android</strong>
                            </div>
                        </a>
                        <a href="{APP_URL}" target="_blank" class="flex items-center justify-center gap-3 bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-cyan-400 py-2.5 px-3 rounded-xl text-left transition shadow group">
                            <i class="fa-brands fa-apple text-2xl text-white group-hover:scale-110 transition"></i>
                            <div>
                                <span class="text-[8px] font-mono text-slate-400 block uppercase leading-none">Compatible con iPhone</span>
                                <strong class="text-xs text-white block leading-none font-bold">Instalar en iOS / Apple</strong>
                            </div>
                        </a>
                    </div>
                </div>
"""

# Reescritura limpia y robusta del Portal Matriz
PORTAL_MATRIZ_CLEAN_HTML = f"""<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>BAZAR NFL.GDL | Ecosistema Comercial Pedro Moreno 501 A</title>
    <meta name="description" content="Hub central BAZAR NFL.GDL: 7 boutiques especializadas en Pedro Moreno 501 A, Guadalajara Centro. Hardware, Pantallas, Tabacos, Dulces, Kiosco y Novedades con Carrito Global y Envío Exprés." />
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />

    <style>
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
        .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
        .cart-pop {{ animation: popBadge 0.25s ease-in-out; }}
        @keyframes popBadge {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.35); }} 100% {{ transform: scale(1); }} }}
    </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen flex flex-col justify-between overflow-x-hidden selection:bg-cyan-500 selection:text-slate-950">

    <header class="bg-slate-900/95 backdrop-blur border-b border-slate-800 sticky top-0 z-50 shadow-2xl">
        <div class="max-w-[99%] 2xl:max-w-[1850px] mx-auto px-4 py-2 flex flex-wrap items-center justify-between gap-2 text-xs border-b border-slate-800/80">
            <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded bg-amber-500/10 border border-amber-500/30 text-amber-400 font-mono font-bold text-[10px] uppercase">
                    Envío Exprés El Mismo Día
                </span>
                <span class="text-slate-300 hidden sm:inline text-[11px] font-semibold">Guadalajara Centro • Carrito Unificado</span>
            </div>

            {NAV_BAR_MOBILE_SWIPE}

            <div class="flex items-center gap-3 font-bold text-[11px]">
                <a href="https://gemini.google.com" target="_blank" class="text-slate-300 hover:text-cyan-400 transition flex items-center gap-1">
                    <i class="fa-solid fa-wand-magic-sparkles text-cyan-400"></i> Gemini AI
                </a>
                <span class="text-slate-700">|</span>
                <a href="https://antigravity.google/download" target="_blank" class="text-slate-300 hover:text-amber-400 transition flex items-center gap-1">
                    <i class="fa-solid fa-download text-amber-400"></i> Anti-Gravity
                </a>
            </div>
        </div>

        <div class="max-w-[99%] 2xl:max-w-[1850px] mx-auto px-4 py-3 flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-3.5 cursor-pointer shrink-0" onclick="document.getElementById('pie-de-pagina').scrollIntoView({{ behavior: 'smooth' }});">
                <div class="relative w-12 h-12 flex items-center justify-center">
                    <img src="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" alt="Logo Tigre BAZAR NFL.GDL" class="w-12 h-12 rounded-full object-cover border-2 border-amber-400 shadow-[0_0_15px_rgba(251,191,36,0.5)]" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';" />
                </div>
                <div class="flex flex-col">
                    <span class="font-black text-2xl text-white tracking-wider uppercase leading-none">BAZAR NFL.GDL</span>
                    <span class="text-[11px] font-mono text-cyan-400 uppercase tracking-tight mt-1 flex items-center gap-1 hover:underline">
                        <i class="fa-solid fa-location-dot text-amber-400"></i> Pedro Moreno 501 A, Guadalajara Centro
                    </span>
                </div>
            </div>

            <div class="flex-1 max-w-3xl w-full relative">
                <div class="flex items-center bg-white rounded-full border-2 border-cyan-400 shadow-[0_0_22px_rgba(6,182,212,0.4)] px-4 py-1.5 gap-2">
                    <i class="fa-solid fa-magnifying-glass text-slate-400 text-sm"></i>
                    <input type="text" id="masterSearchInput" autocomplete="off" spellcheck="false" placeholder="Busca, encuentra y compra rápido (ej. RAM Kingston, Marlboro, Paletas, Cohiba, Lentes)..." class="flex-1 bg-transparent border-0 outline-none text-slate-950 font-bold text-sm placeholder-slate-400" oninput="onMasterSearch(event)" />
                    <button onclick="clearMasterSearch()" id="clear-search-btn" class="hidden text-slate-400 hover:text-slate-600 text-xs px-2 font-bold cursor-pointer"><i class="fa-solid fa-xmark"></i></button>
                    <button onclick="executeMasterSearch()" class="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black px-6 py-2 rounded-full text-xs uppercase tracking-wider transition active:scale-95 shrink-0 shadow cursor-pointer">BUSCAR</button>
                </div>
                <div id="master-autocomplete-box" class="hidden absolute top-full left-0 right-0 mt-2 bg-slate-900 border-2 border-cyan-500/60 rounded-2xl shadow-2xl z-50 p-2.5 flex flex-col gap-2 max-h-96 overflow-y-auto no-scrollbar"></div>
            </div>

            <button onclick="toggleCartDrawer()" class="flex items-center gap-3 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white px-4 py-2.5 rounded-xl transition cursor-pointer active:scale-95 shadow shrink-0 group">
                <div class="relative">
                    <i class="fa-solid fa-cart-shopping text-cyan-400 text-base group-hover:scale-110 transition"></i>
                    <span id="portal-cart-badge" class="absolute -top-2.5 -right-2.5 bg-amber-500 text-slate-950 font-mono font-black text-[10px] rounded-full w-5 h-5 flex items-center justify-center shadow">0</span>
                </div>
                <div class="flex flex-col text-left">
                    <span class="text-[10px] font-mono text-slate-400 uppercase leading-none">Canasta Global</span>
                    <span id="portal-cart-total" class="text-xs font-mono font-bold text-amber-400">$0.00 MXN</span>
                </div>
            </button>
        </div>
    </header>

    <main class="w-full max-w-[99%] 2xl:max-w-[1850px] mx-auto px-2 sm:px-4 py-8 flex-1">
        <div class="flex flex-col lg:flex-row gap-8 items-start justify-center">
            
            <!-- SIDEBAR PROPORCIONAL -->
            <aside class="w-full lg:w-[340px] xl:w-[370px] shrink-0 bg-slate-900/90 rounded-3xl p-5 shadow-2xl relative" id="portal-sidebar-root">
                <div class="flex items-center justify-between border-b border-slate-800 pb-3.5 mb-3.5">
                    <h3 class="font-mono text-sm font-black text-white uppercase tracking-wider flex items-center gap-2 truncate">
                        <i class="fa-solid fa-layer-group text-amber-400"></i> Nuestras 7 Boutiques
                    </h3>
                </div>
                <div class="mb-3.5">
                    <span class="text-[10px] font-mono text-cyan-400 font-bold bg-cyan-950/40 border border-cyan-500/30 px-3 py-1 rounded-xl block text-center uppercase tracking-widest">
                        Compras Rápidas
                    </span>
                </div>

                <nav class="flex flex-col gap-2" id="sidebar-boutiques-list"></nav>

                <!-- UN SOLO CÓDIGO QR -->
                {QR_SINGLE_BLOCK}

                <!-- TARJETAS DE GEMINI Y ANTI-GRAVITY -->
                <div class="mt-5 pt-5 border-t border-slate-800 flex flex-col gap-3">
                    <div class="bg-gradient-to-b from-slate-950 to-slate-900 border border-cyan-500/40 rounded-2xl p-4 flex flex-col gap-2 shadow-lg">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-wand-magic-sparkles text-cyan-400 text-sm"></i>
                            <span class="text-[10px] font-mono font-bold uppercase text-cyan-300">Creado por Google Gemini</span>
                        </div>
                        <p class="text-[11px] text-slate-300 leading-snug">Concebido y programado con la Inteligencia Artificial de Google Gemini.</p>
                        <a href="https://gemini.google.com" target="_blank" class="w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black py-2 rounded-xl text-xs text-center uppercase tracking-wider transition active:scale-95 shadow">Suscribirse a Gemini</a>
                    </div>
                    <div class="bg-gradient-to-b from-slate-950 to-slate-900 border border-amber-500/40 rounded-2xl p-4 flex flex-col gap-2 shadow-lg">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-robot text-amber-400 text-sm"></i>
                            <span class="text-[10px] font-mono font-bold uppercase text-amber-300">Desarrollado por Anti-Gravity</span>
                        </div>
                        <p class="text-[11px] text-slate-300 leading-snug">Desarrollado, compilado y desplegado por Anti-Gravity Copilot.</p>
                        <a href="https://antigravity.google/download" target="_blank" class="w-full bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black py-2 rounded-xl text-xs text-center uppercase tracking-wider transition active:scale-95 shadow">Bajar Anti-Gravity Gratis</a>
                    </div>
                </div>

                <div id="sidebar-flyout-panel" class="hidden lg:absolute left-full top-0 ml-3.5 w-[460px] bg-slate-900/98 border-2 border-cyan-400 rounded-3xl p-5 shadow-[0_12px_45px_rgba(6,182,212,0.4)] z-50 backdrop-blur-xl">
                    <div class="flex justify-between items-center border-b border-slate-800 pb-3 mb-3">
                        <div>
                            <span id="flyout-boutique-tag" class="text-[9px] font-mono font-bold uppercase tracking-wider px-2.5 py-0.5 rounded bg-cyan-500/20 text-cyan-300">BOUTIQUE</span>
                            <h4 id="flyout-boutique-title" class="text-xs font-black text-white mt-1">Compras Inmediatas</h4>
                        </div>
                        <span class="text-[10px] font-mono text-emerald-400 font-bold"><i class="fa-solid fa-bolt"></i> Compra Directa</span>
                    </div>
                    <div id="flyout-boutique-products" class="flex flex-col gap-3 max-h-[400px] overflow-y-auto pr-1 no-scrollbar"></div>
                    <div class="mt-4 pt-3 border-t border-slate-800 text-center">
                        <a id="flyout-enter-link" href="#" class="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 text-slate-950 font-black py-2.5 rounded-xl text-xs uppercase tracking-wider transition flex items-center justify-center gap-2 shadow">
                            <span>Entrar a Boutique Completa</span> <i class="fa-solid fa-arrow-right text-[10px]"></i>
                        </a>
                    </div>
                </div>
            </aside>

            <!-- ESCAPARATE DE 7 SECCIONES CON SWIPE HORIZONTAL EN MÓVILES -->
            <section class="flex-1 w-full flex flex-col gap-8 min-w-0" id="showcase-container"></section>
        </div>
    </main>

    <section class="max-w-[99%] 2xl:max-w-[1850px] mx-auto px-4 py-8 w-full border-t border-slate-800/80">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="p-4 bg-slate-900/60 rounded-2xl flex items-center gap-3.5 shadow-md">
                <div class="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 text-lg shrink-0"><i class="fa-solid fa-truck-fast"></i></div>
                <div><strong class="text-white text-xs block font-bold">Envío Gratis Local</strong><span class="text-slate-400 text-[11px]">En compras desde $1,500 MXN</span></div>
            </div>
            <div class="p-4 bg-slate-900/60 rounded-2xl flex items-center gap-3.5 shadow-md">
                <div class="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 text-lg shrink-0"><i class="fa-solid fa-percent"></i></div>
                <div><strong class="text-white text-xs block font-bold">15% Mayoreo B2B</strong><span class="text-slate-400 text-[11px]">Automático en 10 o más piezas</span></div>
            </div>
            <div class="p-4 bg-slate-900/60 rounded-2xl flex items-center gap-3.5 shadow-md">
                <div class="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 text-lg shrink-0"><i class="fa-solid fa-coins"></i></div>
                <div><strong class="text-white text-xs block font-bold">5% Cashback</strong><span class="text-slate-400 text-[11px]">Acumulable con registro activo</span></div>
            </div>
        </div>
    </section>

    <footer class="bg-slate-950 border-t border-slate-900 pt-16 pb-8 text-slate-400 text-xs" id="pie-de-pagina">
        <div class="max-w-[99%] 2xl:max-w-[1850px] mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 pb-12 border-b border-slate-800/80">
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2"><i class="fa-solid fa-location-dot text-amber-400"></i> Contacto Local</h4>
                    <p class="flex items-start gap-2 text-slate-300"><i class="fa-solid fa-map-pin text-slate-500 mt-0.5 shrink-0"></i><span>Pedro Moreno 501 A, Guadalajara Centro, Jalisco (CP 44100)</span></p>
                    <p class="flex items-center gap-2"><i class="fa-solid fa-phone text-cyan-400 shrink-0"></i><span>Teléfono Fijo: <a href="tel:3336136348" class="text-slate-200 hover:text-cyan-400 font-mono">(33) 3613 6348</a></span></p>
                    <p class="flex items-center gap-2"><i class="fa-brands fa-whatsapp text-emerald-400 shrink-0 text-sm"></i><span>WhatsApp: <a href="https://wa.me/523337271440" target="_blank" class="text-slate-200 hover:text-emerald-400 font-mono">+52 33 3727 1440</a></span></p>
                </div>
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2"><i class="fa-solid fa-shield-halved text-cyan-400"></i> Políticas de Compra</h4>
                    <p class="text-[11px] text-slate-400">Devoluciones en tienda dentro de las 48 horas con empaque íntegro. Soporte técnico y garantía local.</p>
                </div>
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2"><i class="fa-solid fa-coins text-emerald-400"></i> Ahorro y Cashback</h4>
                    <p class="text-slate-300 font-bold">5% de Cashback acumulable en compras consolidadas.</p>
                </div>
            </div>
            <div class="pt-8 text-center text-slate-500 text-[11px]">
                <p>&copy; 2026 BAZAR NFL.GDL & Ecosistema Comercial Pedro Moreno 501 A. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>

    <!-- SCRIPT DEL MOTOR DEL PORTAL -->
    <script>
    const boutiquesConfig = [
        {{ id: "pc-custom", name: "PC Custom Lab", tag: "TECNOLOGÍA", icon: "fa-microchip", color: "text-cyan-400", desc: "Hardware esencial, GPUs NVIDIA RTX y procesadores.", url: "https://iaworldcenter-creator.github.io/pc-custom-lab/" }},
        {{ id: "viamx", name: "Vía MX Boutique", tag: "DEPARTAMENTAL", icon: "fa-gem", color: "text-cyan-300", desc: "Pantallas 4K, refrigeradores, laptops slim y electrónica.", url: "https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/" }},
        {{ id: "cigarros", name: "Cigarros Bazar", tag: "TABACOS", icon: "fa-smoking", color: "text-amber-400", desc: "Cigarros premium, puros habanos y encendedores selectos.", url: "https://iaworldcenter-creator.github.io/cigarros-bazar/" }},
        {{ id: "dulces", name: "Dulces Bazar", tag: "DULCERÍA", icon: "fa-candy-cane", color: "text-pink-400", desc: "Paletas payaso, mazapanes y confitería mexicana.", url: "https://iaworldcenter-creator.github.io/dulces-bazar/" }},
        {{ id: "kiosco", name: "Kiosco Digital", tag: "LECTURA", icon: "fa-newspaper", color: "text-indigo-400", desc: "Suscripciones digitales anuales a revistas y prensa.", url: "https://iaworldcenter-creator.github.io/kiosco-digital/" }},
        {{ id: "puesto", name: "Mi Puesto Bazar", tag: "NOVEDADES", icon: "fa-store", color: "text-emerald-400", desc: "Lentes con audio, consolas retro y cables de carga.", url: "https://iaworldcenter-creator.github.io/mi-puesto-bazar/" }},
        {{ id: "ofertas", name: "Ofertas & Liquidaciones", tag: "OUTLET B2B", icon: "fa-tags", color: "text-red-400", desc: "Excedentes de inventario y remates con hasta 50% de dto.", url: "https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/" }}
    ];

    const masterItems = [
        {{ sku: "PC-001", boutiqueId: "pc-custom", nombre: "Gabinete Micro-ATX con Fuente 500W Incluida", marca: "Acteck", precio: 1250.00, original: 1550.00, desc: "Chasis esbelto con fuente certificada y USB 3.0.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/gabinete_negro.webp", tokens: ["gabinete", "fuente", "pc"] }},
        {{ sku: "PC-002", boutiqueId: "pc-custom", nombre: "Tarjeta Madre ASUS Prime B760M-A WiFi DDR5", marca: "ASUS", precio: 3400.00, original: 3950.00, desc: "Soporte Intel 12va/13va/14va Gen y dual M.2.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/motherboard_asus.webp", tokens: ["tarjeta madre", "asus", "placa"] }},
        {{ sku: "PC-003", boutiqueId: "pc-custom", nombre: "Procesador Intel Core i5-14400F 10C/16T Disipador", marca: "Intel", precio: 4350.00, original: 4990.00, desc: "10 núcleos híbridos de alto desempeño.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/cpu_intel_ultra.webp", tokens: ["procesador", "cpu", "intel"] }},
        {{ sku: "PC-004", boutiqueId: "pc-custom", nombre: "Memoria RAM Kingston FURY Beast 16GB DDR5", marca: "Kingston", precio: 1250.00, original: 1500.00, desc: "Disipador térmico de aluminio negro de bajo perfil.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/ram_caja.webp", tokens: ["ram", "kingston", "fury"] }},
        {{ sku: "PC-005", boutiqueId: "pc-custom", nombre: "Disco Sólido SSD Kingston NV2 1TB NVMe PCIe 4.0", marca: "Kingston", precio: 1350.00, original: 1650.00, desc: "3,500 MB/s lectura para encendido al instante.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/disco_solido_m2.webp", tokens: ["ssd", "kingston", "nvme"] }},
        
        {{ sku: "VMX-001", boutiqueId: "viamx", nombre: "Pantalla Smart TV 55 Pulgadas 4K UHD HDR10+", marca: "Samsung", precio: 7999.00, original: 11499.00, desc: "Panel LED 4K con asistente de voz y HDMI 2.1.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_curvo_negro.webp", tokens: ["pantalla", "smart tv", "samsung"] }},
        {{ sku: "VMX-002", boutiqueId: "viamx", nombre: "Refrigerador Inverter No Frost 14 Pies Cúbicos", marca: "LG", precio: 11899.00, original: 15999.00, desc: "Doble puerta con compresor Inverter bajo consumo.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_warehouse_thumb.webp", tokens: ["refrigerador", "lg", "linea blanca"] }},
        {{ sku: "VMX-003", boutiqueId: "viamx", nombre: "Freidora de Aire Digital 6.5L con 12 Programas", marca: "Tefal", precio: 1499.00, original: 2199.00, desc: "Canastilla antiadherente con calor envolvente 360.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp", tokens: ["freidora", "aire", "airfryer"] }},
        {{ sku: "VMX-004", boutiqueId: "viamx", nombre: "Laptop Ultra Slim 15.6 Pulgadas Core i7 16GB RAM", marca: "Lenovo", precio: 14500.00, original: 18900.00, desc: "Chasis de aluminio ligero y lector de huella.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_mantenimiento_thumb.webp", tokens: ["laptop", "lenovo", "core i7"] }},
        {{ sku: "VMX-005", boutiqueId: "viamx", nombre: "Smartphone 5G Desbloqueado 256GB / 8GB RAM", marca: "Motorola", precio: 4899.00, original: 6499.00, desc: "Pantalla AMOLED 120Hz con batería de 5000mAh.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/perifericos_combo_1.webp", tokens: ["celular", "telefono", "smartphone"] }},

        {{ sku: "CIG-001", boutiqueId: "cigarros", nombre: "Cigarros Marlboro Gold Original (Cajetilla 20)", marca: "Marlboro", precio: 82.00, original: 95.00, desc: "Sabor suave y filtro blanco balanceado.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["cigarros", "marlboro", "gold"] }},
        {{ sku: "CIG-003", boutiqueId: "cigarros", nombre: "Puro Habanos Cohiba Siglo VI Tubo Individual", marca: "Cohiba", precio: 850.00, original: 1100.00, desc: "Puro cubano hecho a mano con notas amaderadas.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["puro", "cohiba", "siglo vi"] }},
        {{ sku: "CIG-005", boutiqueId: "cigarros", nombre: "Encendedor Vintage Recargable a Gas Clipper", marca: "Clipper Pro", precio: 195.00, original: 260.00, desc: "Cuerpo metálico cepillado con piedra intercambiable.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["encendedor", "clipper", "gas"] }},

        {{ sku: "DUL-001", boutiqueId: "dulces", nombre: "Paleta Payaso Ricolino (Caja 15 piezas)", marca: "Ricolino", precio: 245.00, original: 290.00, desc: "Malvavisco con chocolate y gomitas.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp", tokens: ["paleta", "payaso", "ricolino"] }},
        {{ sku: "DUL-002", boutiqueId: "dulces", nombre: "Mazapán De La Rosa Gigante (Caja 20 piezas)", marca: "De La Rosa", precio: 160.00, original: 195.00, desc: "Dulce tradicional de cacahuate tostado.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp", tokens: ["mazapan", "de la rosa"] }},
        {{ sku: "DUL-003", boutiqueId: "dulces", nombre: "Rocaleta Sonrics con Centro de Goma (Bolsa 30)", marca: "Sonrics", precio: 185.00, original: 230.00, desc: "Caramelo con 4 capas de chile ácido y chicle.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp", tokens: ["rocaleta", "sonrics", "chile"] }}
    ];

    function renderSidebarBoutiques() {{
        const container = document.getElementById("sidebar-boutiques-list");
        if (!container) return;
        container.innerHTML = boutiquesConfig.map(b => `
            <button onclick="window.location.href='${{b.url}}'" class="w-full text-left p-3.5 rounded-2xl bg-slate-950/70 hover:bg-slate-800/90 shadow-md flex justify-between items-center transition group cursor-pointer">
                <div class="flex items-center gap-3.5 min-w-0">
                    <div class="w-8 h-8 rounded-xl bg-slate-900 flex items-center justify-center ${{b.color}} shrink-0 shadow"><i class="fa-solid ${{b.icon}} text-sm"></i></div>
                    <div class="min-w-0">
                        <strong class="text-white text-xs block group-hover:text-cyan-300 truncate font-bold">${{b.name}}</strong>
                        <span class="text-[10px] text-slate-400 block truncate font-medium">${{b.desc}}</span>
                    </div>
                </div>
                <i class="fa-solid fa-chevron-right text-[10px] text-slate-600 group-hover:${{b.color}} transition group-hover:translate-x-0.5 shrink-0 ml-2"></i>
            </button>
        `).join('');
    }}

    function renderShowcase() {{
        const container = document.getElementById("showcase-container");
        if (!container) return;

        container.innerHTML = boutiquesConfig.map(b => {{
            const products = masterItems.filter(p => p.boutiqueId === b.id);
            if (products.length === 0) return '';

            return `
                <div class="bg-slate-900/50 rounded-3xl p-5 shadow-2xl space-y-4">
                    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-slate-800/80 pb-3">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-xl bg-slate-950 flex items-center justify-center ${{b.color}} shadow"><i class="fa-solid ${{b.icon}} text-lg"></i></div>
                            <div>
                                <div class="flex items-center gap-2"><h3 class="text-base font-black text-white">${{b.name}}</h3><span class="text-[9px] font-mono font-bold uppercase px-2 py-0.5 rounded bg-slate-950 text-slate-300">${{b.tag}}</span></div>
                                <p class="text-xs text-slate-400 font-medium">${{b.desc}}</p>
                            </div>
                        </div>
                        <a href="${{b.url}}" class="text-xs font-mono font-bold text-cyan-400 hover:text-cyan-300 transition flex items-center gap-1.5 shrink-0 bg-slate-950 px-3.5 py-1.5 rounded-xl shadow">
                            <span>Ver todo en boutique</span> <i class="fa-solid fa-arrow-right text-[10px]"></i>
                        </a>
                    </div>

                    <!-- FILA CON SWIPE TÁCTIL EN MÓVILES (HORIZONTAL) -->
                    <div class="flex lg:grid lg:grid-cols-5 overflow-x-auto lg:overflow-visible gap-4 pb-2 lg:pb-0 no-scrollbar snap-x snap-mandatory">
                        ${{products.map(p => {{
                            const discountPct = p.original ? Math.round((1 - (p.precio / p.original)) * 100) : 0;
                            return `
                                <div class="w-[240px] sm:w-[260px] lg:w-auto shrink-0 lg:shrink snap-start bg-slate-950/90 hover:bg-slate-950 rounded-2xl p-3.5 flex flex-col justify-between transition group shadow-xl hover:shadow-[0_8px_30px_rgba(6,182,212,0.2)]">
                                    <div>
                                        <div class="w-full h-40 sm:h-44 overflow-hidden rounded-xl bg-slate-900 flex items-center justify-center p-2 relative mb-2.5 shadow-inner">
                                            <img src="${{p.img}}" alt="${{p.nombre}}" class="w-full h-full object-contain group-hover:scale-105 transition duration-300" onerror="this.onerror=null; this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';" />
                                            ${{discountPct > 0 ? `<span class="absolute top-2 left-2 bg-red-600 text-white text-[9px] font-mono font-black px-2 py-0.5 rounded-md shadow-md uppercase tracking-wider">-${{discountPct}}% Ahorro</span>` : `<span class="absolute top-2 left-2 bg-amber-500/20 text-amber-300 text-[9px] font-mono font-black px-2 py-0.5 rounded-md shadow-md uppercase">Directo</span>`}}
                                        </div>
                                        <div class="flex justify-between items-center text-[9px] font-mono mb-1">
                                            <span class="text-cyan-400 font-bold uppercase truncate">${{p.marca}}</span>
                                            <span class="text-slate-500 font-bold">${{p.sku}}</span>
                                        </div>
                                        <h4 class="text-white font-bold text-xs mb-1.5 line-clamp-2 leading-snug group-hover:text-cyan-300 transition" title="${{p.nombre}}">${{p.nombre}}</h4>
                                        <p class="text-slate-400 text-[11px] leading-relaxed line-clamp-2 mb-3 font-normal">${{p.desc}}</p>
                                    </div>

                                    <div>
                                        <div class="pt-2.5 border-t border-slate-900 mb-2.5 flex flex-col gap-1">
                                            ${{p.original ? `<div class="flex items-center justify-between gap-1 text-[11px] font-mono"><span class="text-slate-400 font-bold uppercase text-[10px]">Antes:</span><span class="text-red-400 font-bold line-through bg-red-950/50 border border-red-500/40 px-1.5 py-0.2 rounded">$${{p.original.toLocaleString('es-MX', {{ minimumFractionDigits: 2 }})}}</span></div>` : ''}}
                                            <div class="flex items-baseline justify-between">
                                                <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase">Oferta:</span>
                                                <span class="text-base sm:text-lg font-black font-mono text-amber-400">$${{p.precio.toLocaleString('es-MX', {{ minimumFractionDigits: 2 }})}} <span class="text-[10px] text-amber-300/80 font-normal">MXN</span></span>
                                            </div>
                                        </div>

                                        <div class="grid grid-cols-1 gap-2">
                                            <button onclick="addToCartDirect('${{p.sku}}', 1)" class="w-full bg-slate-900 hover:bg-slate-800 text-cyan-300 font-bold py-2 px-2 rounded-xl text-[11px] flex items-center justify-center gap-1.5 transition active:scale-95 cursor-pointer shadow border border-cyan-500/30">
                                                <i class="fa-solid fa-cart-plus text-xs"></i> <span>Agregar al Carrito</span>
                                            </button>
                                            <button onclick="buyNowDirect('${{p.sku}}')" class="w-full bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black py-2 px-2 rounded-xl text-[11px] flex items-center justify-center gap-1.5 transition active:scale-95 shadow cursor-pointer">
                                                <i class="fa-solid fa-bag-shopping text-xs"></i> <span>Comprar Ahora</span>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            `;
                        }}).join('')}}
                    </div>
                </div>
            `;
        }}).join('');
    }}

    function searchMultiToken(query) {{
        if (!query || !query.trim()) return [];
        const q = query.toLowerCase().trim();
        const tokens = q.split(/\s+/).filter(t => t.length > 0);
        return masterItems.filter(item => {{
            const fullSearch = `${{item.sku}} ${{item.nombre}} ${{item.marca}} ${{item.desc}} ${{ (item.tokens || []).join(' ') }}`.toLowerCase();
            return tokens.every(token => fullSearch.includes(token));
        }});
    }}

    function onMasterSearch(e) {{
        const val = e.target.value;
        const clearBtn = document.getElementById("clear-search-btn");
        if (clearBtn) clearBtn.classList.toggle("hidden", val.length === 0);
        renderMasterAutocomplete(val);
    }}

    function renderMasterAutocomplete(val) {{
        const box = document.getElementById("master-autocomplete-box");
        if (!val || val.trim().length < 1) {{
            box.classList.add("hidden");
            return;
        }}
        const matches = searchMultiToken(val).slice(0, 6);
        if (matches.length === 0) {{
            box.innerHTML = `<div class="p-3 text-center text-slate-400 text-xs">No hay coincidencias para "${{val}}"</div>`;
            box.classList.remove("hidden");
            return;
        }}
        box.innerHTML = matches.map(item => `
            <div class="bg-slate-950 rounded-xl p-2.5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 transition shadow border border-slate-800/80">
                <div class="flex items-center gap-2.5 min-w-0 flex-1">
                    <img src="${{item.img}}" alt="${{item.nombre}}" class="w-10 h-10 object-contain rounded-lg bg-slate-900 p-0.5 shrink-0" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';"/>
                    <div class="min-w-0">
                        <span class="text-[9px] font-mono text-cyan-400 font-bold block">${{item.sku}} &bull; ${{item.marca}}</span>
                        <h5 class="text-xs font-bold text-white truncate">${{item.nombre}}</h5>
                        <span class="text-amber-400 font-mono font-bold text-xs">$${{item.precio.toFixed(2)}} MXN</span>
                    </div>
                </div>
                <div class="flex items-center gap-2 w-full sm:w-auto justify-end shrink-0">
                    <button onclick="addToCartDirect('${{item.sku}}', 1)" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 font-bold px-3 py-1.5 rounded-lg text-[10px] flex items-center gap-1 transition active:scale-95 shadow border border-cyan-500/30"><i class="fa-solid fa-cart-plus"></i> Agregar</button>
                    <button onclick="buyNowDirect('${{item.sku}}')" class="bg-gradient-to-r from-amber-400 to-amber-500 text-slate-950 font-black px-3.5 py-1.5 rounded-lg text-[10px] flex items-center gap-1 transition active:scale-95 shadow"><i class="fa-solid fa-bag-shopping"></i> Comprar Ahora</button>
                </div>
            </div>
        `).join('');
        box.classList.remove("hidden");
    }}

    function clearMasterSearch() {{
        const input = document.getElementById("masterSearchInput");
        input.value = '';
        document.getElementById("clear-search-btn").classList.add("hidden");
        document.getElementById("master-autocomplete-box").classList.add("hidden");
    }}

    function executeMasterSearch() {{
        const input = document.getElementById("masterSearchInput");
        renderMasterAutocomplete(input.value);
    }}

    function addToCartDirect(sku, qty = 1) {{
        const item = masterItems.find(p => p.sku === sku);
        if (!item) return;
        let cartStorage = [];
        try {{
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cartStorage = JSON.parse(raw);
        }} catch(e) {{}}
        const exist = cartStorage.find(i => i.sku === sku);
        if (exist) {{
            exist.quantity = (parseInt(exist.quantity) || 1) + qty;
        }} else {{
            cartStorage.push({{ ...item, quantity: qty }});
        }}
        localStorage.setItem('ecosystem_global_cart', JSON.stringify(cartStorage));
        syncCartState();
        const badge = document.getElementById("portal-cart-badge");
        if (badge) {{
            badge.classList.remove("cart-pop");
            void badge.offsetWidth;
            badge.classList.add("cart-pop");
        }}
    }}

    function buyNowDirect(sku) {{
        addToCartDirect(sku, 1);
        window.location.href = "https://iaworldcenter-creator.github.io/pc-custom-lab/checkout.html";
    }}

    function syncCartState() {{
        let cartStorage = [];
        try {{
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cartStorage = JSON.parse(raw);
        }} catch(e) {{}}
        const totalCount = cartStorage.reduce((sum, i) => sum + (parseInt(i.quantity) || 0), 0);
        const totalMoney = cartStorage.reduce((sum, i) => sum + ((parseFloat(i.precio) || 0) * (parseInt(i.quantity) || 0)), 0);
        const badge = document.getElementById("portal-cart-badge");
        const totalTxt = document.getElementById("portal-cart-total");
        if (badge) badge.innerText = totalCount;
        if (totalTxt) totalTxt.innerText = `$${{totalMoney.toLocaleString('es-MX', {{ minimumFractionDigits: 2 }})}} MXN`;
    }}

    function toggleCartDrawer() {{
        window.location.href = "https://iaworldcenter-creator.github.io/pc-custom-lab/checkout.html";
    }}

    document.addEventListener("DOMContentLoaded", () => {{
        renderSidebarBoutiques();
        renderShowcase();
        syncCartState();
    }});
    window.addEventListener("storage", syncCartState);
    </script>
</body>
</html>
"""

# Guardar Portal Matriz en la raíz y en sitios-web
for p in [os.path.join(BASE_DIR, "index.html"), os.path.join(BASE_DIR, "sitios-web", "index.html")]:
    if os.path.exists(os.path.dirname(p)):
        with open(p, "w", encoding="utf-8") as f:
            f.write(PORTAL_MATRIZ_CLEAN_HTML)
        print(f"✓ Portal Matriz actualizado con QR único y Swipe: {p}")

# Desplegar todo a GitHub Pages
print("\n=== SINCRONIZANDO Y DESPLEGANDO A GITHUB PAGES ===")
sitios_repo = os.path.join(BASE_DIR, "sitios-web")
if os.path.exists(os.path.join(sitios_repo, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=sitios_repo, check=True)
    subprocess.run(["git", "commit", "-m", "fix(mobile): swipe horizontal en productos y navegacion, QR unico garantizado", "--allow-empty"], cwd=sitios_repo, capture_output=True)
    res_sub = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sitios_repo, capture_output=True, text=True)
    print(f"🟢 Submódulo sitios-web -> Push: {'OK' if res_sub.returncode == 0 else res_sub.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(ecosistema): QR unico y swipe tactil horizontal en movil desplegados", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
