import os
import subprocess

BASE_DIR = r"E:\sitios web"
VIAMX_DIR = os.path.join(BASE_DIR, "bazar-viamx-nfl.gdl")

if not os.path.exists(VIAMX_DIR):
    alt = os.path.join(BASE_DIR, "bazar-viamx-NFL.GDL")
    if os.path.exists(alt):
        VIAMX_DIR = alt

INDEX_PATH = os.path.join(VIAMX_DIR, "index.html")

print("=" * 70)
print("RECONSTRUYENDO VÍA MX: BUSCADOR AMPLIO + CARRUSEL EXPANDIDO (720PX)")
print("=" * 70)

FULL_HTML_VIAMX = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="BwSy5nNuFFrHJUtxe189nJtPxM4h5QY-SxK1V8wqYDE" />
    <title>VíaMX | Curaduría y Boutique Internacional</title>
    <meta name="description" content="Boutique oficial VíaMX en Guadalajara Centro. Curaduría de artículos selectos e importaciones dentro del ecosistema Anti-Gravity. Pedro Moreno 501 A.">
    
    <!-- Preload del Logo LCP -->
    <link rel="preload" as="image" href="assets/img/mascota_tigre_thumb.webp" fetchpriority="high">
    
    <!-- Tipografías & Estilos -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="assets/css/tailwind-built.css?v=1.1.0" />
    <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></noscript>
    
    <style>
    @font-face { font-family: 'FontAwesome'; font-display: swap; }
    @font-face { font-family: 'Font Awesome 6 Free'; font-display: swap; }
    @font-face { font-family: 'Font Awesome 6 Brands'; font-display: swap; }
    body { font-display: swap; }
    </style>
    
    <script>
    window.addEventListener('error', function(e) { e.preventDefault(); return true; }, true);
    window.addEventListener('unhandledrejection', function(e) { e.preventDefault(); });
    </script>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased overflow-x-hidden min-h-screen flex flex-col justify-between">

    <!-- ========================================================================
         CABECERA OFICIAL VIAMX (2 NIVELES: BUSCADOR AL DOBLE DE ANCHO)
         ======================================================================== -->
    <header class="w-full bg-slate-950 border-b border-slate-900 flex flex-col relative z-[100] text-slate-100 shadow-2xl">
        
        <!-- Nivel 1: Barra Superior Deslizable Universal -->
        <div class="w-full bg-slate-950 border-b border-slate-900 py-3 px-4 flex items-center justify-start md:justify-center overflow-x-auto whitespace-nowrap gap-4 text-xs font-bold text-slate-300" style="scrollbar-width: none; -ms-overflow-style: none;">
            <style>::-webkit-scrollbar { display: none; }</style>
            <a href="https://gemini.google.com" target="_blank" class="hover:text-amber-400 transition flex items-center gap-1">
                <i class="fa-solid fa-wand-magic-sparkles text-cyan-400"></i> Iniciar sesión con Google Gemini
            </a>
            <span class="text-slate-800">|</span>
            <button onclick="openDeliveryModal()" class="hover:text-amber-400 transition cursor-pointer">Registra tu domicilio de entrega</button>
            <span class="text-slate-800">|</span>
            <a href="checkout.html" class="hover:text-amber-400 transition cursor-pointer">Elige tu forma de pago</a>
            <span class="text-slate-800">|</span>
            <a href="#pedidos" onclick="window.location.href='checkout.html';" class="hover:text-amber-400 transition cursor-pointer text-cyan-400 flex items-center gap-1">
                <i class="fa-solid fa-clock-rotate-left"></i> Mis Pedidos
            </a>
            <span class="text-slate-800">|</span>
            <a href="https://iaworldcenter-creator.github.io/cigarros-bazar/" class="hover:text-amber-400 transition">Cigarros Bazar</a>
            <span class="text-slate-800">|</span>
            <a href="https://iaworldcenter-creator.github.io/dulces-bazar/" class="hover:text-amber-400 transition">Dulces Bazar</a>
            <span class="text-slate-800">|</span>
            <a href="https://iaworldcenter-creator.github.io/kiosco-digital/" class="hover:text-amber-400 transition">Kiosco Digital</a>
            <span class="text-slate-800">|</span>
            <a href="https://iaworldcenter-creator.github.io/mi-puesto-bazar/" class="hover:text-amber-400 transition">Puesto Bazar</a>
            <span class="text-slate-800">|</span>
            <a href="https://iaworldcenter-creator.github.io/pc-custom-lab/" class="hover:text-amber-400 transition">PC Custom Lab</a>
            <span class="text-slate-800">|</span>
            <a href="https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones/" class="hover:text-amber-400 transition">Liquidaciones y Ofertas</a>
            <span class="text-slate-800">|</span>
            <a href="https://iaworldcenter-creator.github.io/sitios-web/" class="hover:text-amber-400 transition flex items-center gap-1">
                <i class="fa-solid fa-store text-amber-400"></i> Portal Central
            </a>
            <span class="text-slate-800">|</span>
            <a href="https://antigravity.google/download" target="_blank" class="hover:text-amber-400 transition">Descargar Anti-Gravity</a>
        </div>

        <!-- Nivel 2: Fila Principal (Izquierda: Carrito/Cuenta, Centro: Buscador Expandido, Derecha: Vía MX) -->
        <div class="w-full max-w-[98%] 2xl:max-w-7xl mx-auto flex flex-nowrap items-center justify-between gap-3 sm:gap-6 py-3 px-2 sm:px-6">
            
            <!-- 1. EXTREMO IZQUIERDO: Mi Carrito y Mi Cuenta -->
            <div class="shrink-0 flex items-center gap-4 sm:gap-6">
                <!-- Mi Carrito -->
                <button onclick="toggleCartDrawer()" class="flex items-center gap-2.5 bg-transparent hover:opacity-80 transition cursor-pointer text-left group">
                    <div class="relative flex items-center justify-center">
                        <i class="fa-solid fa-cart-shopping text-2xl sm:text-3xl text-cyan-400 group-hover:scale-105 transition"></i>
                        <span class="absolute -top-2 -right-2 bg-amber-500 text-slate-950 text-[10px] font-black rounded-full px-1.5 py-0.2 min-w-[17px] text-center shadow" id="cart-badge-count">0</span>
                    </div>
                    <div class="flex flex-col">
                        <span class="text-xs sm:text-sm font-black text-white uppercase tracking-wider leading-tight">Mi Carrito</span>
                        <span class="text-xs sm:text-sm font-black text-white mt-0.5" id="header-cart-total">$0.00 MXN</span>
                    </div>
                </button>

                <!-- Mi Cuenta -->
                <button onclick="openDeliveryModal()" class="flex items-center gap-2.5 bg-transparent hover:opacity-80 transition cursor-pointer text-left group">
                    <div class="relative flex items-center justify-center">
                        <i class="fa-solid fa-circle-user text-2xl sm:text-3xl text-amber-400 group-hover:scale-105 transition"></i>
                    </div>
                    <div class="flex flex-col">
                        <span class="text-xs sm:text-sm font-black text-white uppercase tracking-wider leading-tight" id="header-acc-title">Mi Cuenta</span>
                        <span class="text-[11px] font-bold text-slate-200 mt-0.5" id="header-acc-sub">Regístrate, socio</span>
                    </div>
                </button>
            </div>

            <!-- 2. CENTRO: Buscador Amplio (Doble de Ancho / max-w-3xl) con Fondo Color Hueso -->
            <div class="flex-1 max-w-3xl mx-2 sm:mx-6">
                <form class="flex items-center bg-[#f4efe8] rounded-full border-2 border-cyan-400 shadow-[0_0_18px_rgba(6,182,212,0.45)] hover:shadow-[0_0_26px_rgba(6,182,212,0.7)] w-full px-4 py-1.5 gap-2 transition duration-300" onsubmit="handleSearchSubmit(event);" role="search">
                    <label class="sr-only" for="siteSearch">¿Qué deseas buscar hoy?</label>
                    <input aria-label="Buscar productos en el catálogo" autocomplete="off" class="flex-1 bg-transparent border-0 outline-none text-slate-950 font-black text-xs sm:text-sm px-3 placeholder-slate-500 selection:bg-cyan-500 selection:text-white" id="siteSearch" name="q" placeholder="Escribe aquí lo que buscas... ¡Encuentra tu pieza o curaduría ideal hoy!" type="text"/>
                    <button aria-label="Buscar" class="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black px-6 py-2 rounded-full text-xs uppercase tracking-wider transition active:scale-95 shrink-0 flex items-center gap-1.5 shadow-md shadow-amber-500/20 cursor-pointer" type="submit">
                        <i class="fa-solid fa-magnifying-glass text-xs"></i> BUSCAR
                    </button>
                </form>
            </div>

            <!-- 3. EXTREMO DERECHO: Logo Mascota y Rótulo Vía MX -->
            <div class="shrink-0 flex items-center gap-3 group cursor-pointer" onclick="window.location.href='index.html'">
                <div class="relative w-12 h-12 flex items-center justify-center shrink-0">
                    <img alt="Logo Oficial Vía MX" class="w-12 h-12 rounded-full object-cover border-2 border-cyan-400 shadow-[0_0_14px_rgba(6,182,212,0.5)] group-hover:scale-105 transition shrink-0" style="width: 48px; height: 48px; min-width: 48px; min-height: 48px;" src="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" onerror="this.src='assets/img/mascota_tigre.webp';" />
                </div>
                <span class="text-2xl sm:text-3xl font-black tracking-wider uppercase text-cyan-400 drop-shadow-[0_2px_12px_rgba(6,182,212,0.5)] leading-none select-none">
                    Vía MX
                </span>
            </div>

        </div>
    </header>

    <!-- ========================================================================
         HERO SLIDER SECTION (5 FOTOS FAMILIA TIGRE - 720PX ALTURA - COBERTURA TOTAL)
         ======================================================================== -->
    <div id="hero-slider-container" style="position: relative; width: 100%; height: 720px; min-height: 720px; overflow: hidden; background-color: #020617; border-bottom: 1px solid #1e293b; user-select: none;">
        <div id="hero-slider" style="position: relative; width: 100%; height: 100%;">
            <!-- Slide 1 -->
            <div class="hero-slide active" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 1; z-index: 10; transition: opacity 1000ms ease-in-out; background-image: url('assets/img/carucel (1).jpeg'); background-size: cover; background-position: center;"></div>
            <!-- Slide 2 -->
            <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 1000ms ease-in-out; background-image: url('assets/img/carucel (2).jpeg'); background-size: cover; background-position: center;"></div>
            <!-- Slide 3 -->
            <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 1000ms ease-in-out; background-image: url('assets/img/carucel (3).jpeg'); background-size: cover; background-position: center;"></div>
            <!-- Slide 4 -->
            <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 1000ms ease-in-out; background-image: url('assets/img/carucel (4).jpeg'); background-size: cover; background-position: center;"></div>
            <!-- Slide 5 -->
            <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 1000ms ease-in-out; background-image: url('assets/img/carucel (5).jpeg'); background-size: cover; background-position: center;"></div>
        </div>

        <!-- Controles Izquierda / Derecha -->
        <button type="button" aria-label="Anterior" onclick="prevSlide()" style="position: absolute; left: 24px; top: 50%; transform: translateY(-50%); z-index: 20; width: 48px; height: 48px; min-width: 48px; min-height: 48px; border-radius: 9999px; background-color: rgba(2, 6, 23, 0.75); color: #ffffff; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 10px 25px rgba(0,0,0,0.5); backdrop-filter: blur(8px); transition: all 0.3s;">
            <i class="fa-solid fa-chevron-left" style="font-size: 18px;"></i>
        </button>
        <button type="button" aria-label="Siguiente" onclick="nextSlide()" style="position: absolute; right: 24px; top: 50%; transform: translateY(-50%); z-index: 20; width: 48px; height: 48px; min-width: 48px; min-height: 48px; border-radius: 9999px; background-color: rgba(2, 6, 23, 0.75); color: #ffffff; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 10px 25px rgba(0,0,0,0.5); backdrop-filter: blur(8px); transition: all 0.3s;">
            <i class="fa-solid fa-chevron-right" style="font-size: 18px;"></i>
        </button>

        <!-- Indicadores Inferiores -->
        <div class="hero-slider-dots" style="position: absolute; bottom: 28px; left: 0; right: 0; z-index: 20; display: flex; justify-content: center; align-items: center; gap: 10px;">
            <button type="button" aria-label="Foto 1" class="hero-dot" onclick="goToSlide(0)" style="min-width: 44px; min-height: 44px; padding: 12px; display: flex; align-items: center; justify-content: center; cursor: pointer; background: transparent; border: none;"><span style="width: 32px; height: 10px; border-radius: 9999px; background-color: #22d3ee; display: block; box-shadow: 0 0 10px rgba(34,211,238,0.6); transition: all 0.3s;"></span></button>
            <button type="button" aria-label="Foto 2" class="hero-dot" onclick="goToSlide(1)" style="min-width: 44px; min-height: 44px; padding: 12px; display: flex; align-items: center; justify-content: center; cursor: pointer; background: transparent; border: none;"><span style="width: 12px; height: 10px; border-radius: 9999px; background-color: #64748b; display: block; transition: all 0.3s;"></span></button>
            <button type="button" aria-label="Foto 3" class="hero-dot" onclick="goToSlide(2)" style="min-width: 44px; min-height: 44px; padding: 12px; display: flex; align-items: center; justify-content: center; cursor: pointer; background: transparent; border: none;"><span style="width: 12px; height: 10px; border-radius: 9999px; background-color: #64748b; display: block; transition: all 0.3s;"></span></button>
            <button type="button" aria-label="Foto 4" class="hero-dot" onclick="goToSlide(3)" style="min-width: 44px; min-height: 44px; padding: 12px; display: flex; align-items: center; justify-content: center; cursor: pointer; background: transparent; border: none;"><span style="width: 12px; height: 10px; border-radius: 9999px; background-color: #64748b; display: block; transition: all 0.3s;"></span></button>
            <button type="button" aria-label="Foto 5" class="hero-dot" onclick="goToSlide(4)" style="min-width: 44px; min-height: 44px; padding: 12px; display: flex; align-items: center; justify-content: center; cursor: pointer; background: transparent; border: none;"><span style="width: 12px; height: 10px; border-radius: 9999px; background-color: #64748b; display: block; transition: all 0.3s;"></span></button>
        </div>
    </div>

    <!-- ========================================================================
         CONTENIDO PRINCIPAL: CATÁLOGO OFICIAL
         ======================================================================== -->
    <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <section id="catalogo" class="w-full">
            <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8 pb-4 border-b border-slate-800">
                <div>
                    <span class="text-xs font-mono text-cyan-400 uppercase tracking-widest block mb-1">// Catálogo Oficial</span>
                    <h3 class="text-2xl sm:text-3xl font-black text-white flex items-center gap-2">
                        <i class="fa-solid fa-box-open text-amber-400"></i> Artículos en Curaduría
                    </h3>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-xs text-slate-400 font-mono" id="catalog-count-text">Cargando artículos...</span>
                </div>
            </div>

            <!-- Cuadrícula de Productos -->
            <div id="catalog-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                <!-- Se poblará dinámicamente -->
            </div>
        </section>
    </main>

    <!-- ========================================================================
         FOOTER UNIVERSAL
         ======================================================================== -->
    <footer class="py-8 border-t border-slate-800 bg-slate-950 text-center text-xs text-slate-400 font-mono">
        <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-2">
                <img src="assets/img/mascota_tigre_thumb.webp" alt="VíaMX" width="24" height="24" class="rounded-full">
                <span class="text-white font-bold">VíaMX Curaduría Internacional</span>
            </div>
            <p>© 2026 VíaMX — Ecosistema Anti-Gravity & Alfa. Pedro Moreno 501 A, Guadalajara Centro.</p>
            <div class="flex items-center gap-4 text-slate-300">
                <a href="checkout.html" class="hover:text-cyan-400">Checkout</a>
                <span>•</span>
                <a href="https://iaworldcenter-creator.github.io/sitios-web/" class="hover:text-cyan-400">Portal Central</a>
            </div>
        </div>
    </footer>

    <!-- ========================================================================
         SCRIPTS: CARRUSEL ROBUSTO (5S / 1S TRANSICIÓN) Y CUENTA DINÁMICA
         ======================================================================== -->
    <script id="viamx-slider-clean-script">
    window.currentSlide = 0;
    window.sliderInterval = null;

    window.showSlide = function(index) {
        const slides = document.querySelectorAll('.hero-slide');
        const dots = document.querySelectorAll('.hero-dot span');
        if (slides.length === 0) return;
        
        // Desvanecer slide anterior
        const current = slides[window.currentSlide];
        if (current) {
            current.style.opacity = '0';
            current.style.zIndex = '0';
        }
        const currentDot = dots[window.currentSlide];
        if (currentDot) {
            currentDot.style.width = '12px';
            currentDot.style.backgroundColor = '#64748b';
            currentDot.style.boxShadow = 'none';
        }
        
        window.currentSlide = (index + slides.length) % slides.length;
        
        // Mostrar nuevo slide
        const next = slides[window.currentSlide];
        if (next) {
            next.style.opacity = '1';
            next.style.zIndex = '10';
        }
        const nextDot = dots[window.currentSlide];
        if (nextDot) {
            nextDot.style.width = '32px';
            nextDot.style.backgroundColor = '#22d3ee';
            nextDot.style.boxShadow = '0 0 10px rgba(34,211,238,0.6)';
        }
        window.resetSliderInterval();
    };

    window.resetSliderInterval = function() {
        if (window.sliderInterval) clearInterval(window.sliderInterval);
        if (window.innerWidth < 640) return;
        window.sliderInterval = setInterval(() => {
            window.nextSlide();
        }, 5000);
    };

    window.nextSlide = function() {
        window.showSlide(window.currentSlide + 1);
    };

    window.prevSlide = function() {
        window.showSlide(window.currentSlide - 1);
    };

    window.goToSlide = function(index) {
        window.showSlide(index);
    };

    document.addEventListener('DOMContentLoaded', () => {
        window.showSlide(0);
        window.resetSliderInterval();
    });
    </script>

    <script id="account-status-sync">
    function syncHeaderAccountStatus() {
        try {
            const stored = sessionStorage.getItem('ecosystem_delivery_address') || localStorage.getItem('ecosystem_delivery_address');
            const titleEl = document.getElementById('header-acc-title');
            const subEl = document.getElementById('header-acc-sub');
            if (stored && titleEl && subEl) {
                const addr = JSON.parse(stored);
                if (addr && addr.name) {
                    titleEl.innerText = "Mi Dirección";
                    subEl.innerText = "Hola, " + addr.name.split(' ')[0];
                    return;
                }
            }
            if (titleEl && subEl) {
                titleEl.innerText = "Mi Cuenta";
                subEl.innerText = "Regístrate, socio";
            }
        } catch(e) {}
    }
    document.addEventListener('DOMContentLoaded', syncHeaderAccountStatus);
    window.addEventListener('storage', syncHeaderAccountStatus);
    </script>

    <script>
    let localCatalog = [];

    function formatCurrency(amount) {
        const num = parseFloat(amount) || 0;
        return '$' + num.toLocaleString('es-MX', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }

    function updateCartBadge() {
        try {
            const stored = localStorage.getItem("ecosystem_global_cart");
            const cart = stored ? JSON.parse(stored) : [];
            const count = Array.isArray(cart) ? cart.reduce((acc, i) => acc + (i.quantity || 1), 0) : 0;
            const total = Array.isArray(cart) ? cart.reduce((acc, i) => acc + ((parseFloat(i.precio) || 0) * (i.quantity || 1)), 0) : 0;
            
            const badge = document.getElementById("cart-badge-count");
            const totalEl = document.getElementById("header-cart-total");
            if (badge) badge.textContent = count;
            if (totalEl) totalEl.textContent = formatCurrency(total) + ' MXN';
        } catch(e) {}
    }

    async function loadCatalog() {
        const grid = document.getElementById("catalog-grid");
        const countText = document.getElementById("catalog-count-text");
        try {
            const res = await fetch("catalog.json");
            localCatalog = await res.json();
            renderCatalog(localCatalog);
        } catch(e) {
            if (grid) grid.innerHTML = '<p class="col-span-full text-center text-slate-400 text-xs py-8">Catálogo en proceso de renovación.</p>';
        }
    }

    function renderCatalog(items) {
        const grid = document.getElementById("catalog-grid");
        const countText = document.getElementById("catalog-count-text");
        if (!grid) return;
        
        if (countText) countText.textContent = `Mostrando ${items.length} artículo(s) disponibles`;

        if (!items || items.length === 0) {
            grid.innerHTML = '<p class="col-span-full text-center text-slate-400 text-xs py-8">No se encontraron artículos con ese criterio.</p>';
            return;
        }

        grid.innerHTML = items.map(item => `
            <div class="bg-slate-900/90 border border-slate-800 hover:border-cyan-500/50 rounded-2xl p-5 flex flex-col justify-between transition duration-300 shadow-lg group">
                <div>
                    <div class="w-full h-44 overflow-hidden rounded-xl bg-slate-950 border border-slate-800/80 flex items-center justify-center mb-4 p-2 relative">
                        <img 
                            src="${item.imagen || 'assets/img/mascota_tigre_thumb.webp'}" 
                            alt="${item.nombre}" 
                            loading="lazy" 
                            decoding="async" 
                            width="300" 
                            height="300" 
                            class="w-full h-full object-contain group-hover:scale-105 transition duration-300" 
                            onerror="this.onerror=null;this.src='assets/img/mascota_tigre_thumb.webp';"
                        />
                    </div>
                    <span class="text-[10px] font-mono text-cyan-400 font-bold uppercase tracking-wider block mb-1">${item.sku || 'VMX'}</span>
                    <h4 class="text-white font-bold text-sm mb-1.5 line-clamp-2">${item.nombre}</h4>
                    <p class="text-slate-300 text-xs mb-4 line-clamp-2 leading-relaxed">${item.descripcion || ''}</p>
                </div>
                <div class="flex justify-between items-center pt-3 border-t border-slate-800">
                    <span class="text-amber-400 font-black text-sm font-mono">${formatCurrency(item.precio)}</span>
                    <button onclick="addToCart('${item.sku}')" class="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black px-3.5 py-1.5 rounded-xl text-xs flex items-center gap-1.5 transition active:scale-95 shadow-md shadow-cyan-500/20">
                        <i class="fa-solid fa-cart-plus"></i> Agregar
                    </button>
                </div>
            </div>
        `).join('');
    }

    function addToCart(sku) {
        try {
            const item = localCatalog.find(i => i.sku === sku);
            if (!item) return;
            
            const stored = localStorage.getItem("ecosystem_global_cart");
            let cart = stored ? JSON.parse(stored) : [];
            if (!Array.isArray(cart)) cart = [];
            
            const existIdx = cart.findIndex(i => i.sku === sku);
            if (existIdx > -1) {
                cart[existIdx].quantity = (cart[existIdx].quantity || 1) + 1;
            } else {
                cart.push({
                    sku: item.sku,
                    nombre: item.nombre,
                    precio: item.precio,
                    imagen: item.imagen || 'assets/img/mascota_tigre_thumb.webp',
                    categoria: item.categoria || 'viamx',
                    quantity: 1
                });
            }
            
            localStorage.setItem("ecosystem_global_cart", JSON.stringify(cart));
            updateCartBadge();
            alert(`"${item.nombre}" agregado al carrito.`);
        } catch(e) {}
    }

    function handleSearchSubmit(e) {
        if (e) e.preventDefault();
        const input = document.getElementById("siteSearch");
        if (!input) return;
        
        const q = input.value.toLowerCase().trim();
        let filtered = localCatalog;
        if (q) {
            filtered = filtered.filter(i => 
                (i.nombre || '').toLowerCase().includes(q) || 
                (i.descripcion || '').toLowerCase().includes(q) ||
                (i.sku || '').toLowerCase().includes(q)
            );
        }
        renderCatalog(filtered);
    }

    document.addEventListener("DOMContentLoaded", () => {
        updateCartBadge();
        loadCatalog();
    });
    </script>
</body>
</html>"""

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(FULL_HTML_VIAMX)

print("✓ index.html reconstruido: carrusel 720px y buscador al doble de ancho.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "fix(layout): carrusel 720px full width y buscador amplio al doble", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(viamx): carrusel 720px y buscador amplio sincronizado", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
