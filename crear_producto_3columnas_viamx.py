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
PRODUCTO_PATH = os.path.join(VIAMX_DIR, "producto.html")
CATALOG_PATH = os.path.join(VIAMX_DIR, "catalog.json")

print("=" * 70)
print("CREANDO PÁGINA DEDICADA PRODUCTO.HTML (3 COLUMNAS + MARQUEE CONTINUO)")
print("=" * 70)

# Cargar catálogo de 200 productos
with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    productos_200 = json.load(f)

JSON_EMBEDDED = json.dumps(productos_200, ensure_ascii=False)

# 1. GENERAR PRODUCTO.HTML COMPLETO
PRODUCTO_HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="BwSy5nNuFFrHJUtxe189nJtPxM4h5QY-SxK1V8wqYDE" />
    <title id="page-title">VíaMX | Detalle de Producto</title>
    <meta name="description" content="Detalle de producto y curaduría exclusiva en VíaMX Boutique Internacional. Pedro Moreno 501 A, Guadalajara Centro.">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="assets/css/tailwind-built.css?v=1.1.0" />
    <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></noscript>
    
    <style>
    @font-face {{ font-family: 'FontAwesome'; font-display: swap; }}
    @font-face {{ font-family: 'Font Awesome 6 Free'; font-display: swap; }}
    @font-face {{ font-family: 'Font Awesome 6 Brands'; font-display: swap; }}
    body {{ font-display: swap; }}
    
    /* Animación continua del Marquee Amarillo */
    @keyframes marquee-viamx-loop {{
        0% {{ transform: translate3d(0, 0, 0); }}
        100% {{ transform: translate3d(-50%, 0, 0); }}
    }}
    .animate-marquee-viamx {{
        display: flex;
        width: max-content;
        animation: marquee-viamx-loop 28s linear infinite;
        will-change: transform;
    }}
    .animate-marquee-viamx:hover {{
        animation-play-state: paused;
    }}
    </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased overflow-x-hidden min-h-screen flex flex-col justify-between">

    <!-- CABECERA OFICIAL VIAMX -->
    <header class="w-full bg-slate-950 border-b border-slate-900 flex flex-col relative z-[100] text-slate-100 shadow-2xl">
        
        <!-- Nivel 1: Barra Superior Deslizable Universal -->
        <div class="w-full bg-slate-950 border-b border-slate-900 py-3 px-4 flex items-center justify-start md:justify-center overflow-x-auto whitespace-nowrap gap-4 text-xs font-bold text-slate-300" style="scrollbar-width: none; -ms-overflow-style: none;">
            <style>::-webkit-scrollbar {{ display: none; }}</style>
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

        <!-- Nivel 2: Fila Principal -->
        <div class="w-full max-w-[98%] 2xl:max-w-7xl mx-auto flex flex-nowrap items-center justify-between gap-3 sm:gap-6 py-3 px-2 sm:px-6">
            
            <!-- Extremo Izquierdo: Carrito y Cuenta -->
            <div class="shrink-0 flex items-center gap-4 sm:gap-6">
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

            <!-- Centro: Buscador Amplio -->
            <div class="flex-1 max-w-3xl mx-2 sm:mx-6">
                <form class="flex items-center bg-[#f4efe8] rounded-full border-2 border-cyan-400 shadow-[0_0_18px_rgba(6,182,212,0.45)] hover:shadow-[0_0_26px_rgba(6,182,212,0.7)] w-full px-4 py-1.5 gap-2 transition duration-300" onsubmit="handleSearchSubmit(event);" role="search">
                    <label class="sr-only" for="siteSearch">¿Qué deseas buscar hoy?</label>
                    <input aria-label="Buscar productos en el catálogo" autocomplete="off" class="flex-1 bg-transparent border-0 outline-none text-slate-950 font-black text-xs sm:text-sm px-3 placeholder-slate-500 selection:bg-cyan-500 selection:text-white" id="siteSearch" name="q" placeholder="¿Qué producto, pieza o antojo buscas hoy? Escribe aquí..." type="text"/>
                    <button aria-label="Buscar" class="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black px-6 py-2 rounded-full text-xs uppercase tracking-wider transition active:scale-95 shrink-0 flex items-center gap-1.5 shadow-md shadow-amber-500/20 cursor-pointer" type="submit">
                        <i class="fa-solid fa-magnifying-glass text-xs"></i> BUSCAR
                    </button>
                </form>
            </div>

            <!-- Extremo Derecho: Logo Vía MX -->
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

    <!-- CINTILLO MARQUEE AMARILLO CONTINUO (CONFIANZA & CONVERSIÓN B2B) -->
    <div class="w-full bg-amber-400 text-slate-950 py-2.5 overflow-hidden border-y border-amber-500 font-black text-xs shadow-md select-none">
        <div class="animate-marquee-viamx flex whitespace-nowrap gap-10 uppercase font-mono tracking-wider items-center">
            <span>🔥 5% DE CASHBACK ACUMULABLE CON REGISTRO ACTIVO</span>
            <span>•</span>
            <span>📦 PRECIO DE MAYOREO: 15% DE DESCUENTO DIRECTO A PARTIR DE 10 PIEZAS</span>
            <span>•</span>
            <span>🛡️ CONDICIÓN: SIN REGISTRO NO HAY CASHBACK ACUMULABLE</span>
            <span>•</span>
            <span>🏬 BOUTIQUES ESPECIALIZADAS. UN SOLO CARRITO GLOBAL UNIFICADO</span>
            <span>•</span>
            <span>💳 PAGOS CON TARJETA BANCARIA, TRANSFERENCIA SPEI Y EFECTIVO CONTRA ENTREGA</span>
            <span>•</span>
            <span>🚚 ENVÍO GRATIS A PARTIR DE $1,500 MXN EN GUADALAJARA CENTRO</span>
            <span>•</span>
            <!-- Duplicado idéntico para ciclo continuo infinito sin saltos -->
            <span>🔥 5% DE CASHBACK ACUMULABLE CON REGISTRO ACTIVO</span>
            <span>•</span>
            <span>📦 PRECIO DE MAYOREO: 15% DE DESCUENTO DIRECTO A PARTIR DE 10 PIEZAS</span>
            <span>•</span>
            <span>🛡️ CONDICIÓN: SIN REGISTRO NO HAY CASHBACK ACUMULABLE</span>
            <span>•</span>
            <span>🏬 BOUTIQUES ESPECIALIZADAS. UN SOLO CARRITO GLOBAL UNIFICADO</span>
            <span>•</span>
            <span>💳 PAGOS CON TARJETA BANCARIA, TRANSFERENCIA SPEI Y EFECTIVO CONTRA ENTREGA</span>
            <span>•</span>
            <span>🚚 ENVÍO GRATIS A PARTIR DE $1,500 MXN EN GUADALAJARA CENTRO</span>
            <span>•</span>
        </div>
    </div>

    <!-- ========================================================================
         CUERPO PRINCIPAL: VISTA DE PRODUCTO EN 3 COLUMNAS (ESTRUCTURA UNIVERSAL)
         ======================================================================== -->
    <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        
        <!-- Migas de Pan (Breadcrumbs) -->
        <nav class="flex items-center gap-2 text-xs font-mono text-slate-400 mb-6" aria-label="Breadcrumb">
            <a href="index.html" class="hover:text-cyan-400 transition">Inicio</a>
            <span>/</span>
            <a href="index.html#catalogo" class="hover:text-cyan-400 transition" id="breadcrumb-category">Curaduría</a>
            <span>/</span>
            <span class="text-slate-200 truncate max-w-xs sm:max-w-md font-bold" id="breadcrumb-product">Cargando producto...</span>
        </nav>

        <!-- GRID MAESTRO DE 3 COLUMNAS -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-10 items-start">
            
            <!-- -------------------------------------------------------------
                 COLUMNA 1 (IZQUIERDA): FOTO GIGANTE Y GALERÍA COMPLETA
                 ------------------------------------------------------------- -->
            <div class="lg:col-span-4 flex flex-col gap-4">
                <div class="w-full h-[420px] sm:h-[480px] bg-slate-900 border border-slate-800 rounded-3xl p-4 flex items-center justify-center relative overflow-hidden shadow-2xl">
                    <img id="detail-p-img" src="" alt="Producto VíaMX" class="w-full h-full object-contain transition-transform duration-300 hover:scale-105" />
                    <span class="absolute top-4 left-4 bg-amber-500/20 border border-amber-500/50 text-amber-300 text-[10px] font-mono font-black px-2.5 py-1 rounded-lg shadow-md">
                        Edición Curaduría 2026
                    </span>
                </div>

                <!-- Miniaturas de Galería -->
                <div class="grid grid-cols-3 gap-2.5">
                    <div class="h-20 bg-slate-900 border-2 border-cyan-400 rounded-xl p-1 flex items-center justify-center cursor-pointer shadow-md">
                        <img id="thumb-1" src="" alt="Vista 1" class="w-full h-full object-contain" />
                    </div>
                    <div class="h-20 bg-slate-900 border border-slate-800 rounded-xl p-1 flex items-center justify-center cursor-pointer hover:border-cyan-400 transition shadow-md">
                        <img id="thumb-2" src="assets/img/mascota_tigre_thumb.webp" alt="Vista 2" class="w-full h-full object-contain opacity-70 hover:opacity-100" />
                    </div>
                    <div class="h-20 bg-slate-900 border border-slate-800 rounded-xl p-1 flex items-center justify-center cursor-pointer hover:border-cyan-400 transition shadow-md">
                        <img id="thumb-3" src="assets/img/mascota_tigre_thumb.webp" alt="Vista 3" class="w-full h-full object-contain opacity-70 hover:opacity-100" />
                    </div>
                </div>

                <!-- Respaldo Local -->
                <div class="p-3.5 bg-slate-900/60 border border-slate-800 rounded-2xl flex items-center gap-3">
                    <i class="fa-solid fa-shield-halved text-cyan-400 text-xl shrink-0"></i>
                    <div class="text-[11px] leading-tight">
                        <strong class="text-white block font-bold">Garantía Local Inmediata</strong>
                        <span class="text-slate-400">Inspección y entrega física en Pedro Moreno 501 A.</span>
                    </div>
                </div>
            </div>

            <!-- -------------------------------------------------------------
                 COLUMNA 2 (CENTRO): DETALLES, ESPECIFICACIONES Y DESCRIPCIÓN
                 ------------------------------------------------------------- -->
            <div class="lg:col-span-5 flex flex-col gap-5 border-b lg:border-b-0 lg:border-r border-slate-800 pb-8 lg:pb-0 lg:pr-8">
                
                <div>
                    <div class="flex items-center justify-between gap-2 mb-1.5">
                        <span id="detail-p-brand" class="text-xs font-mono text-cyan-400 font-bold uppercase tracking-wider"></span>
                        <span id="detail-p-sku" class="text-xs font-mono text-slate-500"></span>
                    </div>
                    <h1 id="detail-p-title" class="text-2xl sm:text-3xl font-black text-white leading-tight"></h1>
                    <a href="index.html#catalogo" class="text-xs text-cyan-400 hover:underline font-bold mt-1 inline-block">Visita el catálogo oficial de la marca</a>
                    
                    <!-- Rating y Calificaciones -->
                    <div class="flex items-center gap-2 mt-3">
                        <div class="flex items-center gap-1 text-amber-400 text-sm">
                            <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star-half-stroke"></i>
                        </div>
                        <span id="detail-p-rating" class="text-xs font-bold text-amber-300 font-mono">4.8</span>
                        <span class="text-slate-600">•</span>
                        <span id="detail-p-reviews" class="text-xs font-mono text-slate-400">1,240 valoraciones en la zona</span>
                    </div>
                </div>

                <!-- Recuadro: ¿Por qué elegir este artículo? -->
                <div class="bg-slate-900/90 border border-cyan-500/40 rounded-2xl p-4 shadow-lg flex flex-col gap-2">
                    <h3 class="text-xs font-mono text-cyan-300 font-bold uppercase tracking-wider flex items-center gap-1.5">
                        <i class="fa-solid fa-circle-question text-cyan-400"></i> ¿Por qué elegir este artículo?
                    </h3>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        Este producto oficial del Ecosistema es el favorito por su durabilidad superior, componentes certificados y garantía local directa inmediata de fábrica.
                    </p>
                    <div class="flex items-center justify-between pt-2 border-t border-slate-800 text-xs">
                        <span class="text-slate-400">Precio Unitario Promocional:</span>
                        <strong class="text-amber-400 font-mono text-sm font-black" id="detail-p-promo-price">$0.00 MXN</strong>
                    </div>
                </div>

                <!-- Ficha Técnica -->
                <div>
                    <h3 class="text-xs font-mono text-white uppercase tracking-widest font-black mb-3">Ficha Técnica</h3>
                    <div class="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden text-xs">
                        <div class="grid grid-cols-2 p-3 border-b border-slate-800/80 bg-slate-950/40">
                            <span class="text-slate-400 font-mono uppercase">Marca:</span>
                            <strong class="text-white" id="spec-brand">Vía MX</strong>
                        </div>
                        <div class="grid grid-cols-2 p-3 border-b border-slate-800/80">
                            <span class="text-slate-400 font-mono uppercase">Código SKU:</span>
                            <strong class="text-cyan-400 font-mono" id="spec-sku">VMX-001</strong>
                        </div>
                        <div class="grid grid-cols-2 p-3 border-b border-slate-800/80 bg-slate-950/40">
                            <span class="text-slate-400 font-mono uppercase">Categoría:</span>
                            <strong class="text-white capitalize" id="spec-cat">Electrónica</strong>
                        </div>
                        <div class="grid grid-cols-2 p-3">
                            <span class="text-slate-400 font-mono uppercase">Disponibilidad:</span>
                            <strong class="text-emerald-400">En Stock Guadalajara Centro</strong>
                        </div>
                    </div>
                </div>

                <!-- Descripción Detallada del Producto -->
                <div>
                    <h3 class="text-xs font-mono text-white uppercase tracking-widest font-black mb-2">Descripción del Producto</h3>
                    <div class="text-xs text-slate-300 leading-relaxed space-y-2 bg-slate-900/40 p-4 rounded-2xl border border-slate-800">
                        <p id="detail-p-desc"></p>
                        <ul class="list-disc pl-4 space-y-1 text-slate-400 text-[11px] pt-2 border-t border-slate-800/80">
                            <li>Soporte local y garantía oficial directa en la zona Centro.</li>
                            <li>Empaque seguro con sellado hermético contra golpes e importación certificada.</li>
                            <li>Acepta consolidación con cualquiera de las otras 6 tiendas del Ecosistema.</li>
                        </ul>
                    </div>
                </div>

            </div>

            <!-- -------------------------------------------------------------
                 COLUMNA 3 (DERECHA): PANEL DE COMPRA (BUY BOX VÍAMX)
                 ------------------------------------------------------------- -->
            <div class="lg:col-span-3 bg-slate-900/90 border border-slate-800 rounded-3xl p-6 shadow-2xl flex flex-col gap-4 sticky top-24">
                
                <div>
                    <span class="text-[10px] font-mono text-slate-400 uppercase block font-bold">Precio Unitario</span>
                    <div class="text-3xl font-black text-cyan-400 font-mono" id="buybox-price">$0.00 MXN</div>
                    <div class="flex items-baseline gap-2 mt-1">
                        <span class="text-slate-500 line-through text-xs font-mono" id="buybox-original"></span>
                        <span class="text-red-400 text-xs font-bold font-mono" id="buybox-discount"></span>
                    </div>
                </div>

                <!-- Entrega Local -->
                <div class="text-xs text-slate-300 space-y-1 bg-slate-950 p-3.5 rounded-2xl border border-slate-800">
                    <p class="font-bold text-white flex items-center gap-1.5">
                        <i class="fa-solid fa-truck-fast text-emerald-400"></i> Entrega Local: <span class="text-emerald-400 font-mono">GRATIS</span>
                    </p>
                    <p class="text-[11px] text-slate-400 leading-tight">
                        Aplica en pedidos de $1,500 MXN o retiro directo en Pedro Moreno 501 A.
                    </p>
                </div>

                <!-- Módulo de Mayoreo B2B -->
                <div class="bg-cyan-950/30 border border-cyan-500/40 rounded-2xl p-3.5 text-xs text-slate-300">
                    <strong class="text-cyan-300 block font-mono uppercase text-[10px] tracking-wider mb-1">
                        <i class="fa-solid fa-boxes-stacked"></i> Módulo de Mayoreo B2B
                    </strong>
                    <p class="text-[11px] text-slate-300 leading-tight">
                        Precio especial para mayoristas: Obtén <strong>15% de descuento</strong> a partir de la pieza 10.
                    </p>
                </div>

                <!-- Desbloqueo de Cashback -->
                <div class="bg-amber-950/20 border border-amber-500/30 rounded-2xl p-3.5 flex flex-col gap-2">
                    <div class="text-[11px] font-bold text-amber-300 flex items-center gap-1.5">
                        <i class="fa-solid fa-coins"></i> <span>Desbloquear 5% de Cashback</span>
                    </div>
                    <p class="text-[10px] text-slate-400 leading-tight">
                        Obtén saldo de regalo en esta compra registrándote gratis en nuestro portal de socios.
                    </p>
                    <button onclick="openDeliveryModal()" class="bg-slate-900 hover:bg-slate-800 text-amber-400 border border-amber-500/40 py-1.5 px-3 rounded-xl text-[11px] font-bold transition cursor-pointer">
                        Registrar Cuenta Gratis
                    </button>
                    <span class="text-[9px] text-slate-500 leading-none">Nota: Sin registro de correo y teléfono no se genera cashback.</span>
                </div>

                <!-- Selector de Cantidad -->
                <div>
                    <label for="buybox-qty" class="block text-[10px] font-mono text-slate-400 uppercase font-bold mb-1">Cantidad:</label>
                    <select id="buybox-qty" class="w-full bg-slate-950 border border-slate-700 text-white rounded-xl p-2.5 text-xs font-bold focus:border-cyan-500 focus:outline-none cursor-pointer">
                        <option value="1" selected>1 unidad</option>
                        <option value="2">2 unidades</option>
                        <option value="3">3 unidades</option>
                        <option value="4">4 unidades</option>
                        <option value="5">5 unidades</option>
                        <option value="10">10 unidades (Aplica 15% Mayoreo)</option>
                    </select>
                </div>

                <!-- Botones de Acción -->
                <div class="flex flex-col gap-2.5 pt-2">
                    <button onclick="ejecutarCompraDirecta()" class="w-full bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black py-3 rounded-2xl text-xs uppercase tracking-wider transition active:scale-95 shadow-lg shadow-amber-500/25 flex items-center justify-center gap-2 cursor-pointer">
                        <i class="fa-solid fa-credit-card"></i> PAGAR AHORA
                    </button>
                    <button onclick="agregarAlCarritoDesdeBuybox()" class="w-full bg-slate-950 hover:bg-slate-800 border border-cyan-500 text-cyan-300 hover:text-white font-black py-3 rounded-2xl text-xs uppercase tracking-wider transition active:scale-95 flex items-center justify-center gap-2 cursor-pointer shadow-md shadow-cyan-950/30">
                        <i class="fa-solid fa-cart-shopping"></i> Agregar al carrito
                    </button>
                    <a href="index.html#catalogo" class="w-full bg-slate-950/60 hover:bg-slate-800 text-slate-400 hover:text-white py-2 rounded-xl text-center text-xs font-bold transition flex items-center justify-center gap-1.5 cursor-pointer">
                        <i class="fa-solid fa-arrow-left text-[10px]"></i> Seguir comprando
                    </a>
                </div>

            </div>

        </div>

    </main>

    <!-- FOOTER UNIVERSAL HOMOLOGADO (3 COLUMNAS) -->
    <footer class="bg-slate-950 border-t border-slate-900 pt-16 pb-8 text-slate-400 text-xs">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 pb-12 border-b border-slate-800/80">
                <div class="flex flex-col gap-3">
                    <h3 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-location-dot text-amber-400"></i> Contacto Local
                    </h3>
                    <p class="flex items-start gap-2 text-slate-300">
                        <i class="fa-solid fa-map-pin text-slate-400 mt-0.5 shrink-0"></i>
                        <span>Pedro Moreno 501 A, Guadalajara Centro, Jalisco (CP 44100)</span>
                    </p>
                    <p class="flex items-center gap-2">
                        <i class="fa-solid fa-phone text-cyan-400 shrink-0"></i>
                        <span>Teléfono Fijo: <a href="tel:3336136348" class="text-slate-200 hover:text-cyan-400 font-mono">(33) 3613 6348</a></span>
                    </p>
                    <p class="flex items-center gap-2">
                        <i class="fa-brands fa-whatsapp text-emerald-400 shrink-0 text-sm"></i>
                        <span>WhatsApp: <a href="https://wa.me/523337271440" target="_blank" rel="noopener" class="text-slate-200 hover:text-emerald-400 font-mono">+52 33 3727 1440</a></span>
                    </p>
                </div>
                <div class="flex flex-col gap-3">
                    <h3 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-shield-halved text-cyan-400"></i> Políticas de Compra
                    </h3>
                    <p class="text-slate-400 text-[11px] leading-relaxed">
                        <strong class="text-slate-200 block text-xs">Devoluciones Directas:</strong>
                        Permitidas físicamente en tienda dentro de las primeras 48 horas con empaque íntegro.
                    </p>
                </div>
                <div class="flex flex-col gap-3">
                    <h3 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-coins text-emerald-400"></i> Ahorro y Cashback
                    </h3>
                    <p class="text-slate-300 font-bold flex items-center gap-2">
                        <i class="fa-solid fa-piggy-bank text-amber-400 text-base shrink-0"></i>
                        <span>5% de Cashback en cada compra de forma directa.</span>
                    </p>
                    <p class="text-[11px] text-slate-400 leading-relaxed bg-slate-900/60 p-3 rounded-xl border border-slate-800/80">
                        El cashback es acumulable únicamente con registro activo en nuestro portal central.
                    </p>
                </div>
            </div>
            <div class="pt-8 text-center text-slate-400 text-[11px] flex flex-col sm:flex-row items-center justify-between gap-4">
                <div class="flex items-center gap-2">
                    <img src="assets/img/mascota_tigre_thumb.webp" alt="Vía MX" width="20" height="20" class="rounded-full">
                    <span class="text-white font-bold">Vía MX Curaduría Internacional</span>
                </div>
                <p>© 2026 Vía MX — Ecosistema Anti-Gravity & Alfa. Pedro Moreno 501 A, Guadalajara Centro.</p>
            </div>
        </div>
    </footer>

    <!-- LÓGICA DE DETALLE Y COMPRA -->
    <script>
    const viamxCatalog = {JSON_EMBEDDED};
    let currentItem = null;

    function formatCurrency(amount) {{
        const num = parseFloat(amount) || 0;
        return '$' + num.toLocaleString('es-MX', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
    }}

    function initProductPage() {{
        const urlParams = new URLSearchParams(window.location.search);
        let sku = urlParams.get('sku');
        if (!sku && viamxCatalog.length > 0) {{
            sku = viamxCatalog[0].sku;
        }}

        currentItem = viamxCatalog.find(p => p.sku === sku) || viamxCatalog[0];
        if (!currentItem) return;

        // Títulos y metadatos
        document.title = `${{currentItem.nombre}} | VíaMX Curaduría`;
        document.getElementById('page-title').innerText = `${{currentItem.nombre}} | VíaMX`;
        document.getElementById('breadcrumb-category').innerText = currentItem.categoria.toUpperCase();
        document.getElementById('breadcrumb-product').innerText = currentItem.nombre;

        // Columna 1 (Foto y Miniaturas)
        const mainImg = currentItem.imagen || 'assets/img/mascota_tigre_thumb.webp';
        document.getElementById('detail-p-img').src = mainImg;
        document.getElementById('thumb-1').src = mainImg;

        // Columna 2 (Detalles)
        document.getElementById('detail-p-brand').innerText = currentItem.marca || 'VÍA MX';
        document.getElementById('detail-p-sku').innerText = `SKU: ${{currentItem.sku}}`;
        document.getElementById('detail-p-title').innerText = currentItem.nombre;
        document.getElementById('detail-p-rating').innerText = currentItem.rating || '4.8';
        document.getElementById('detail-p-reviews').innerText = `${{currentItem.reviews || '1,200'}} valoraciones en la zona`;
        document.getElementById('detail-p-promo-price').innerText = `${{formatCurrency(currentItem.precio)}} MXN`;
        document.getElementById('spec-brand').innerText = currentItem.marca || 'Vía MX';
        document.getElementById('spec-sku').innerText = currentItem.sku;
        document.getElementById('spec-cat').innerText = currentItem.categoria;
        document.getElementById('detail-p-desc').innerText = currentItem.descripcion || '';

        // Columna 3 (Buy Box)
        document.getElementById('buybox-price').innerText = `${{formatCurrency(currentItem.precio)}} MXN`;
        if (currentItem.original && currentItem.original > currentItem.precio) {{
            document.getElementById('buybox-original').innerText = formatCurrency(currentItem.original);
            const discountPct = Math.round((1 - (currentItem.precio / currentItem.original)) * 100);
            document.getElementById('buybox-discount').innerText = `-${{discountPct}}%`;
        }}

        updateCartBadge();
        syncHeaderAccountStatus();
    }}

    function agregarAlCarritoDesdeBuybox() {{
        if (!currentItem) return;
        const qty = parseInt(document.getElementById('buybox-qty').value) || 1;

        let cart = [];
        try {{
            const stored = localStorage.getItem("ecosystem_global_cart");
            cart = stored ? JSON.parse(stored) : [];
        }} catch(e) {{}}

        const existIdx = cart.findIndex(i => i.sku === currentItem.sku);
        if (existIdx > -1) {{
            cart[existIdx].quantity = (cart[existIdx].quantity || 1) + qty;
        }} else {{
            cart.push({{
                sku: currentItem.sku,
                nombre: currentItem.nombre,
                precio: currentItem.precio,
                imagen: currentItem.imagen || 'assets/img/mascota_tigre_thumb.webp',
                categoria: currentItem.categoria || 'viamx',
                quantity: qty
            }});
        }}

        localStorage.setItem("ecosystem_global_cart", JSON.stringify(cart));
        updateCartBadge();
        alert(`¡Se agregaron ${{qty}} unidad(es) de "${{currentItem.nombre}}" al carrito!`);
    }}

    function ejecutarCompraDirecta() {{
        agregarAlCarritoDesdeBuybox();
        window.location.href = 'checkout.html';
    }}

    function updateCartBadge() {{
        try {{
            const stored = localStorage.getItem("ecosystem_global_cart");
            const cart = stored ? JSON.parse(stored) : [];
            const count = Array.isArray(cart) ? cart.reduce((acc, i) => acc + (i.quantity || 1), 0) : 0;
            const total = Array.isArray(cart) ? cart.reduce((acc, i) => acc + ((parseFloat(i.precio) || 0) * (i.quantity || 1)), 0) : 0;
            
            const badge = document.getElementById("cart-badge-count");
            const totalEl = document.getElementById("header-cart-total");
            if (badge) badge.textContent = count;
            if (totalEl) totalEl.textContent = formatCurrency(total) + ' MXN';
        }} catch(e) {{}}
    }}

    function syncHeaderAccountStatus() {{
        try {{
            const stored = sessionStorage.getItem('ecosystem_delivery_address') || localStorage.getItem('ecosystem_delivery_address');
            const titleEl = document.getElementById('header-acc-title');
            const subEl = document.getElementById('header-acc-sub');
            if (stored && titleEl && subEl) {{
                const addr = JSON.parse(stored);
                if (addr && addr.name) {{
                    titleEl.innerText = "Mi Dirección";
                    subEl.innerText = "Hola, " + addr.name.split(' ')[0];
                    return;
                }}
            }}
            if (titleEl && subEl) {{
                titleEl.innerText = "Mi Cuenta";
                subEl.innerText = "Regístrate, socio";
            }}
        }} catch(e) {{}}
    }}

    function handleSearchSubmit(e) {{
        if (e) e.preventDefault();
        const input = document.getElementById("siteSearch");
        if (input && input.value.trim()) {{
            window.location.href = `index.html?q=${{encodeURIComponent(input.value.trim())}}#catalogo`;
        }}
    }}

    document.addEventListener("DOMContentLoaded", initProductPage);
    </script>
</body>
</html>
"""

with open(PRODUCTO_PATH, "w", encoding="utf-8") as f:
    f.write(PRODUCTO_HTML_CONTENT)

print(f"✓ {PRODUCTO_PATH} creado exitosamente con la estructura de 3 columnas y marquee continuo.")

# 2. ACTUALIZAR INDEX.HTML PARA QUE LAS TARJETAS ABRAN PRODUCTO.HTML
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    index_content = f.read()

# Purgar el modal previo de index.html
index_content = re.sub(r'<!--\s*=+\s*VENTANA MODAL[\s\S]*?<\/div>\s*<\/div>\s*<\/div>', '', index_content, flags=re.IGNORECASE)
index_content = re.sub(r'let currentModalSku[\s\S]*?document\.addEventListener\(\'keydown\', \(e\) => \{[^}]*\}\);', '', index_content, flags=re.IGNORECASE)

# Actualizar el onclick de las tarjetas para redirigir a producto.html?sku=...
index_content = re.sub(
    r'onclick="openProductModal\(\\\'[^\\\']+\\\'\)"',
    'onclick="window.location.href=\\\'producto.html?sku=\\\' + item.sku"',
    index_content
)
index_content = re.sub(
    r'onclick="openProductModal\(\'\$\{item\.sku\}\'\)"',
    'onclick="window.location.href=\'producto.html?sku=\' + item.sku"',
    index_content
)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(index_content)

print(f"✓ {INDEX_PATH} actualizado: Las tarjetas ahora navegan a producto.html?sku=...")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(producto): pagina dedicada producto.html en 3 columnas con marquee continuo y buy box", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(viamx): pagina de producto en 3 columnas y navegacion fluida desplegada", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
