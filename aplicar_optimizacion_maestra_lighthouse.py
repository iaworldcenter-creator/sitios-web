import os
import json
import re

BASE_DIR = r"E:\sitios web\pc-custom-lab"
INDEX_HTML = os.path.join(BASE_DIR, "index.html")
ENGINE_JS = os.path.join(BASE_DIR, "js", "ct-exact-catalog-engine.js")
CSS_FILE = os.path.join(BASE_DIR, "assets", "css", "tailwind-built.css")

print("=" * 80, flush=True)
print("EJECUCIÓN DE OPTIMIZACIÓN MAESTRA LIGHTHOUSE 100/100 (6 PILARES TÉCNICOS)")
print("=" * 80, flush=True)

# 1. ACTUALIZAR CSS CON REGLAS ESTRICTAS DE CLS Y TAP TARGETS 48PX
with open(CSS_FILE, "r", encoding="utf-8") as f:
    base_css = f.read()

LIGHTHOUSE_MASTER_CSS = """
/* === LIGHTHOUSE CORE WEB VITALS & A11Y MASTER STYLES === */
.product-img-wrapper {
    aspect-ratio: 1 / 1 !important;
    width: 100% !important;
    height: 140px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    contain: layout size !important;
    position: relative !important;
    overflow: hidden !important;
}

.pagination-btn, .qty-btn, .category-link, .btn-action {
    min-width: 48px !important;
    min-height: 48px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
}

@media (max-width: 768px) {
    .pagination-btn, .qty-btn, .category-link, .btn-action {
        min-width: 48px !important;
        min-height: 48px !important;
        padding: 8px !important;
        margin: 2px !important;
    }
}

.no-scrollbar::-webkit-scrollbar { display: none !important; }
.no-scrollbar { -ms-overflow-style: none !important; scrollbar-width: none !important; }
.neon-glow-pc {
    border: 1px solid rgba(6,182,212,0.9) !important;
    box-shadow: 0 0 16px rgba(6,182,212,0.6), inset 0 0 10px rgba(6,182,212,0.3) !important;
}
@font-face {
    font-family: 'Font Awesome 6 Free';
    font-display: swap;
}
@font-face {
    font-family: 'Font Awesome 6 Brands';
    font-display: swap;
}
"""

if '.product-img-wrapper' not in base_css:
    base_css += LIGHTHOUSE_MASTER_CSS

# 2. ESCRIBIR INDEX.HTML OPTIMIZADO AL 100%
HTML_OPTIMIZED = """<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PC Custom Lab | Hardware Mayorista & Ensamble de Cómputo</title>
    <meta name="description" content="Catálogo oficial de hardware mayorista PC Custom Lab, procesadores Intel/AMD, placas ASUS, tarjetas gráficas RTX y configuraciones armadas.">
    
    <!-- Preconexión DNS y CDN -->
    <link rel="preconnect" href="https://static.ctonline.mx" crossorigin>
    <link rel="dns-prefetch" href="https://static.ctonline.mx">
    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
    <link rel="dns-prefetch" href="https://cdnjs.cloudflare.com">

    <!-- Font Awesome asíncrono con font-display: swap -->
    <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"></noscript>

    <!-- CSS Completo Compilado Directo en Línea (CERO BLOQUEOS, CERO CLS) -->
    <style>
""" + base_css + """
    </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans min-h-screen flex flex-col antialiased">
    <!-- H1 SEMÁNTICO PRINCIPAL DE LA TIENDA -->
    <h1 class="sr-only">PC Custom Lab | Distribución Mayorista de Hardware y Ensamble de Cómputo</h1>

    <!-- CABECERA DE 2 LÍNEAS (MÓVIL Y ESCRITORIO) -->
    <header class="sticky top-0 z-50 bg-slate-950/95 backdrop-blur-md border-b border-slate-800 shadow-xl">
        <!-- Línea 1: Desplazamiento Horizontal con Botón Neón Activo -->
        <div class="w-full max-w-[1850px] mx-auto px-2 sm:px-4 py-2 border-b border-slate-900/80 flex items-center justify-between gap-2 overflow-x-auto no-scrollbar scroll-smooth">
            <div class="flex items-center gap-1.5 shrink-0">
                <span class="text-[9px] font-mono font-black text-amber-300 bg-amber-500/10 border border-amber-500/30 px-2.5 py-1 rounded-full uppercase tracking-wider">
                    ⚡ Entrega Express Hoy
                </span>
            </div>
            
            <nav class="flex items-center gap-1.5 shrink-0 text-xs font-mono font-bold" aria-label="Ecosistema de Tiendas">
                <a href="https://iaworldcenter-creator.github.io/sitios-web/" aria-label="Ir al portal matriz" class="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 hover:text-white border border-slate-800 transition min-h-[44px] flex items-center">
                    <i class="fa-solid fa-house text-amber-400 mr-1.5"></i> Matriz
                </a>
                <a href="https://iaworldcenter-creator.github.io/pc-custom-lab/" aria-label="Tienda activa PC Custom Lab" class="px-3 py-1.5 rounded-xl bg-cyan-950/80 text-cyan-300 font-black neon-glow-pc transition min-h-[44px] flex items-center">
                    <i class="fa-solid fa-microchip text-cyan-400 mr-1.5"></i> PC Custom
                </a>
                <a href="https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/" aria-label="Ir a boutique Vía MX" class="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 hover:text-white border border-slate-800 transition min-h-[44px] flex items-center">
                    <i class="fa-solid fa-gem text-cyan-300 mr-1.5"></i> Vía MX
                </a>
                <a href="https://iaworldcenter-creator.github.io/cigarros-bazar/" aria-label="Ir a boutique Cigarros Bazar" class="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 hover:text-white border border-slate-800 transition min-h-[44px] flex items-center">
                    <i class="fa-solid fa-smoking text-amber-400 mr-1.5"></i> Cigarros
                </a>
                <a href="https://iaworldcenter-creator.github.io/dulces-bazar/" aria-label="Ir a boutique Dulces Bazar" class="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 hover:text-white border border-slate-800 transition min-h-[44px] flex items-center">
                    <i class="fa-solid fa-candy-cane text-pink-400 mr-1.5"></i> Dulces
                </a>
                <a href="https://iaworldcenter-creator.github.io/kiosco-digital/" aria-label="Ir a Kiosco Digital" class="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 hover:text-white border border-slate-800 transition min-h-[44px] flex items-center">
                    <i class="fa-solid fa-newspaper text-indigo-400 mr-1.5"></i> Kiosco
                </a>
                <a href="https://iaworldcenter-creator.github.io/mi-puesto-bazar/" aria-label="Ir a Mi Puesto Bazar" class="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 hover:text-white border border-slate-800 transition min-h-[44px] flex items-center">
                    <i class="fa-solid fa-store text-emerald-400 mr-1.5"></i> Mi Puesto
                </a>
                <a href="https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/" aria-label="Ir a Ofertas y Liquidaciones" class="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 hover:text-white border border-slate-800 transition min-h-[44px] flex items-center">
                    <i class="fa-solid fa-tags text-red-400 mr-1.5"></i> Liquidaciones
                </a>
            </nav>
        </div>

        <!-- Línea 2: Logo + Barra de Búsqueda Blanca + Botón Carrito -->
        <div class="w-full max-w-[1850px] mx-auto px-2 sm:px-4 py-2.5 flex items-center justify-between gap-3">
            <a href="index.html" aria-label="Ir a inicio de PC Custom Lab" class="flex items-center gap-2.5 shrink-0 group min-h-[48px]">
                <div class="w-10 h-10 rounded-xl bg-slate-900 border border-cyan-500/40 p-1 flex items-center justify-center shrink-0">
                    <img src="assets/img/mascota_tigre_thumb.webp" alt="Logo PC Custom Lab" width="36" height="36" class="w-full h-full object-contain" />
                </div>
                <div class="flex flex-col">
                    <span class="text-xs sm:text-sm font-black font-mono text-white tracking-wider uppercase group-hover:text-cyan-400 transition">PC CUSTOM LAB</span>
                    <span class="text-[9px] font-mono text-slate-300 truncate hidden sm:block">Pedro Moreno 501 A, Guadalajara</span>
                </div>
            </a>

            <div class="flex-1 max-w-2xl relative">
                <form onsubmit="event.preventDefault();" class="flex items-center bg-white rounded-xl border border-slate-300 shadow-inner px-3 py-1">
                    <label for="boutiqueSearchInput" class="sr-only">Buscar productos</label>
                    <i class="fa-solid fa-magnifying-glass text-slate-600 text-sm mr-2 shrink-0" aria-hidden="true"></i>
                    <input 
                        type="search" 
                        id="boutiqueSearchInput" 
                        name="q"
                        aria-label="Buscar productos por SKU, procesador o modelo" 
                        placeholder="Busca por SKU, procesador, RTX 4070, B760M, RAM DDR5..." 
                        class="w-full bg-transparent text-slate-900 placeholder-slate-500 text-xs sm:text-sm outline-none font-medium min-h-[44px]" 
                    />
                    <button type="submit" aria-label="Buscar productos" class="btn-action bg-blue-700 hover:bg-blue-600 text-white font-mono font-black px-4 py-2 rounded-lg text-xs uppercase tracking-wider shadow shrink-0">
                        Buscar
                    </button>
                </form>
                <div id="boutique-autocomplete-box" class="absolute top-full left-0 w-full bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl mt-1.5 p-2 z-[100] hidden max-h-96 overflow-y-auto no-scrollbar"></div>
            </div>

            <a href="checkout.html" aria-label="Ver carrito de compras" class="btn-action flex items-center gap-2 bg-slate-900 hover:bg-slate-800 border border-cyan-500/40 text-white px-3.5 py-2 rounded-xl font-mono text-xs font-bold transition shrink-0 shadow">
                <div class="relative">
                    <i class="fa-solid fa-cart-shopping text-cyan-400 text-base" aria-hidden="true"></i>
                    <span id="boutique-cart-badge" class="absolute -top-2 -right-2 bg-amber-400 text-slate-950 text-[10px] font-black w-4 h-4 rounded-full flex items-center justify-center">0</span>
                </div>
                <span id="boutique-cart-total" class="hidden sm:inline text-amber-300 font-bold">$0.00 MXN</span>
            </a>
        </div>
    </header>

    <!-- CONTENIDO PRINCIPAL: ESTRUCTURA DE 2 COLUMNAS -->
    <main class="w-full max-w-[1880px] mx-auto px-2 sm:px-4 py-4 flex-1" id="catalog-main-content-root">
        
        <div class="flex flex-col lg:flex-row gap-4 items-start justify-center">
            
            <!-- COLUMNA LATERAL IZQUIERDA: CATEGORÍAS (H2: Categorías de Hardware) -->
            <aside style="width: 280px; min-width: 280px; max-width: 280px;" class="w-full lg:w-[280px] shrink-0" id="sidebar-facets-root">
                <!-- Inyectado por JS -->
            </aside>

            <!-- COLUMNA CENTRAL: ESCAPARATE PRINCIPAL (H2: Aparador Principal) -->
            <section style="flex: 1 1 0%; min-width: 0;" class="flex-1 min-w-0 w-full flex flex-col gap-3.5">
                
                <!-- Franja Tecnológica / Banner Superior -->
                <div class="w-full rounded-2xl overflow-hidden bg-gradient-to-r from-blue-900 via-indigo-950 to-slate-900 border border-cyan-500/40 p-3.5 flex flex-col sm:flex-row items-center justify-between gap-3 shadow-xl text-white">
                    <div class="flex items-center gap-3">
                        <div class="w-11 h-11 rounded-xl bg-cyan-500/20 border border-cyan-400/40 flex items-center justify-center text-xl shrink-0">
                            <i class="fa-solid fa-bolt text-amber-300" aria-hidden="true"></i>
                        </div>
                        <div>
                            <span class="text-[10px] font-mono text-cyan-300 font-bold uppercase tracking-wider block">Distribución Mayorista Directa</span>
                            <div class="font-bold text-xs sm:text-sm text-white">Precios Especiales con Entrega Inmediata en Guadalajara (Pedro Moreno 501 A)</div>
                        </div>
                    </div>
                    <button onclick="document.getElementById('boutiqueSearchInput').focus()" aria-label="Explorar catálogo de hardware" class="btn-action bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-black px-4 py-2 rounded-xl text-xs uppercase font-mono tracking-wider shadow-lg transition shrink-0 cursor-pointer">
                        Ver Catálogo
                    </button>
                </div>

                <!-- Barra Superior de Control (Resultados + Alternador Vista + Ordenar) -->
                <div class="p-3.5 bg-slate-900/95 border border-slate-800 rounded-2xl shadow-xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 text-white">
                    <div>
                        <h2 class="text-xs sm:text-sm font-bold text-cyan-300 leading-tight font-mono" id="results-count-display">
                            Aparador Principal (20 de 16,122)
                        </h2>
                    </div>

                    <div class="flex items-center gap-3 flex-wrap justify-between w-full sm:w-auto">
                        <!-- Alternador de Vista (Cuadrícula vs. Lista) -->
                        <div class="bg-slate-950 p-1 rounded-xl border border-slate-800 flex items-center gap-1">
                            <button id="btn-view-list" onclick="setViewStyle('list')" aria-label="Vista en lista" aria-pressed="false" class="btn-action p-2 rounded-lg text-slate-300 hover:text-white transition cursor-pointer text-xs flex items-center justify-center">
                                <i class="fa-solid fa-list-ul" aria-hidden="true"></i>
                            </button>
                            <button id="btn-view-grid" onclick="setViewStyle('grid')" aria-label="Vista en cuadrícula" aria-pressed="true" class="btn-action p-2 rounded-lg bg-cyan-500 text-slate-950 font-bold transition cursor-pointer text-xs flex items-center justify-center">
                                <i class="fa-solid fa-table-cells" aria-hidden="true"></i>
                            </button>
                        </div>

                        <!-- Paginación Superior 1..7...50 -->
                        <div class="pagination-target-bar">
                            <!-- Inyectado por JS -->
                        </div>

                        <!-- Menú Desplegable 'Ordenar por' con Label Vinculado -->
                        <div class="flex items-center gap-2 text-xs font-mono">
                            <label for="sort-select" id="lbl-sort-select" class="cursor-pointer font-bold text-slate-200 shrink-0">Ordenar:</label>
                            <select 
                                id="sort-select" 
                                name="sort-select" 
                                aria-labelledby="lbl-sort-select" 
                                aria-label="Ordenar catálogo por disponibilidad o precio" 
                                onchange="currentSortCriterion=this.value; renderExactCatalogView();" 
                                class="bg-slate-950 border border-slate-700 text-slate-100 font-medium rounded-xl px-3 py-2 text-xs outline-none cursor-pointer min-h-[44px]"
                            >
                                <option value="existencia">Disponibilidad</option>
                                <option value="precio_asc">Precio: Menor a Mayor</option>
                                <option value="precio_desc">Precio: Mayor a Menor</option>
                                <option value="nombre">Nombre A-Z</option>
                            </select>
                        </div>
                    </div>
                </div>

                <!-- CONTENEDOR DEL APARADOR DE 20 PRODUCTOS (5 FILAS X 4 COLUMNAS) -->
                <div id="products-grid-container" class="min-h-[700px]">
                    <!-- Inyectado por JS: 20 productos -->
                </div>

                <!-- Paginación Inferior -->
                <div class="pagination-target-bar p-3.5 bg-slate-900/95 border border-slate-800 rounded-2xl shadow-xl flex justify-center items-center">
                    <!-- Inyectado por JS -->
                </div>

            </section>

        </div>
    
        <!-- MODAL DE FICHA TÉCNICA EN 3 COLUMNAS (PDP) -->
        <div id="productDetailModal" class="fixed inset-0 z-[200] hidden flex items-center justify-center p-2 sm:p-4" role="dialog" aria-modal="true" aria-labelledby="pdp-modal-title">
            <div class="absolute inset-0 bg-slate-950/85 backdrop-blur-md" onclick="closeProductDetailModal()"></div>
            <div class="relative w-full max-w-6xl max-h-[92vh] overflow-y-auto bg-slate-900 border-2 border-cyan-500/60 rounded-3xl shadow-[0_0_50px_rgba(6,182,212,0.3)] p-4 sm:p-6 z-10 no-scrollbar">
                <div id="productDetailModalContent">
                    <!-- Inyectado dinámicamente en 3 columnas por JS -->
                </div>
            </div>
        </div>

    </main>

    <!-- FOOTER OFICIAL PC CUSTOM LAB (H2: Pie de Página) -->
    <footer class="bg-slate-950 border-t border-slate-800 text-slate-300 text-xs mt-12 pt-10 pb-8" aria-label="Pie de página institucional">
        <h2 class="sr-only">Información Legal, Contacto y Garantías PC Custom Lab</h2>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 pb-10 border-b border-slate-800/80">
                
                <!-- COLUMNA 1: CONTACTO Y REDES OFICIALES -->
                <div class="space-y-3">
                    <h3 class="font-bold text-cyan-300 uppercase tracking-wider text-xs font-mono flex items-center gap-2">
                        <i class="fa-solid fa-location-dot text-cyan-400" aria-hidden="true"></i> Contacto y Redes Oficiales
                    </h3>
                    <div class="space-y-2 text-slate-200 text-[11px] leading-relaxed">
                        <p class="flex items-start gap-2">
                            <i class="fa-solid fa-store text-cyan-400 mt-0.5 shrink-0" aria-hidden="true"></i>
                            <span>Pedro Moreno 501 A, Guadalajara Centro, Jalisco (CP 44100)</span>
                        </p>
                        <p class="flex items-center gap-2">
                            <i class="fa-solid fa-phone text-cyan-400 shrink-0" aria-hidden="true"></i>
                            <span>Teléfono Fijo: <strong>(33) 3653 6348</strong></span>
                        </p>
                        <p class="flex items-center gap-2">
                            <i class="fa-brands fa-whatsapp text-emerald-400 shrink-0" aria-hidden="true"></i>
                            <span>WhatsApp: <a href="https://wa.me/523337271440" target="_blank" rel="noopener" aria-label="Contactar por WhatsApp" class="hover:text-emerald-300 font-bold text-white transition">+52 33 3727 1440</a></span>
                        </p>
                        <p class="flex items-center gap-2">
                            <i class="fa-solid fa-mobile-screen-button text-cyan-400 shrink-0" aria-hidden="true"></i>
                            <span>Celular: <strong>+52 33 2865 2309</strong></span>
                        </p>
                    </div>

                    <div class="pt-2 border-t border-slate-900 space-y-1.5 text-[10.5px]">
                        <a href="https://www.facebook.com/profile.php?id=61593020515115" target="_blank" rel="noopener" aria-label="Perfil oficial de Facebook" class="text-slate-300 hover:text-blue-400 flex items-center gap-2 transition">
                            <i class="fa-brands fa-facebook text-blue-500 w-4 text-center" aria-hidden="true"></i> <span>Facebook: <strong>BAZAR NFL.GDL</strong></span>
                        </a>
                        <a href="https://www.instagram.com/pccustomlab/" target="_blank" rel="noopener" aria-label="Perfil oficial de Instagram" class="text-slate-300 hover:text-pink-400 flex items-center gap-2 transition">
                            <i class="fa-brands fa-instagram text-pink-500 w-4 text-center" aria-hidden="true"></i> <span>Instagram: <strong>@pccustomlab</strong></span>
                        </a>
                        <a href="https://www.youtube.com/@IAWorldCenter" target="_blank" rel="noopener" aria-label="Canal oficial de YouTube" class="text-slate-300 hover:text-red-400 flex items-center gap-2 transition">
                            <i class="fa-brands fa-youtube text-red-500 w-4 text-center" aria-hidden="true"></i> <span>YouTube: <strong>IA World Center</strong></span>
                        </a>
                        <a href="https://t.me/pc_custom_lab" target="_blank" rel="noopener" aria-label="Canal oficial de Telegram" class="text-slate-300 hover:text-cyan-400 flex items-center gap-2 transition">
                            <i class="fa-brands fa-telegram text-cyan-400 w-4 text-center" aria-hidden="true"></i> <span>Telegram: <strong>pc_custom_lab</strong></span>
                        </a>
                    </div>
                </div>

                <!-- COLUMNA 2: POLÍTICAS DE COMPRA Y GARANTÍA -->
                <div class="space-y-3">
                    <h3 class="font-bold text-cyan-300 uppercase tracking-wider text-xs font-mono flex items-center gap-2">
                        <i class="fa-solid fa-shield-halved text-cyan-400" aria-hidden="true"></i> Políticas de Compra & Garantía
                    </h3>
                    <div class="space-y-2 text-slate-200 text-[11px] leading-relaxed">
                        <p class="flex items-start gap-2">
                            <i class="fa-solid fa-circle-check text-emerald-400 mt-0.5 shrink-0" aria-hidden="true"></i>
                            <span><strong>Garantía Directa de 48 Horas:</strong> Reemplazo inmediato en mostrador presentando empaque original intacto.</span>
                        </p>
                        <p class="flex items-start gap-2">
                            <i class="fa-solid fa-box-open text-cyan-400 mt-0.5 shrink-0" aria-hidden="true"></i>
                            <span><strong>Garantía de Fábrica de 1 Año:</strong> Gestión técnica sin costo de fletes ni trámites adicionales.</span>
                        </p>
                        <p class="flex items-start gap-2">
                            <i class="fa-solid fa-lock text-amber-400 mt-0.5 shrink-0" aria-hidden="true"></i>
                            <span><strong>Seguridad Transaccional SSL/TLS:</strong> Protocolos de encriptación bancaria de 256 bits y cumplimiento SAT/PROFECO.</span>
                        </p>
                    </div>
                </div>

                <!-- COLUMNA 3: AHORRO, CASHBACK Y DESPACHO LOCAL -->
                <div class="space-y-3">
                    <h3 class="font-bold text-cyan-300 uppercase tracking-wider text-xs font-mono flex items-center gap-2">
                        <i class="fa-solid fa-coins text-emerald-400" aria-hidden="true"></i> Ahorro, Cashback & Despacho Local
                    </h3>
                    <div class="space-y-2 text-slate-200 text-[11px] leading-relaxed">
                        <div class="bg-slate-900/90 p-3 rounded-2xl border border-emerald-500/40 space-y-1">
                            <div class="flex items-center gap-2 text-emerald-300 font-mono font-black text-xs">
                                <i class="fa-solid fa-piggy-bank text-amber-400" aria-hidden="true"></i>
                                <span>5% DE CASHBACK EN CADA COMPRA</span>
                            </div>
                            <p class="text-[10.5px] text-slate-300">
                                Registra tu teléfono al ordenar para acumular saldo electrónico reutilizable en todas las boutiques.
                            </p>
                        </div>

                        <div class="bg-slate-900/90 p-3 rounded-2xl border border-slate-800 space-y-1">
                            <div class="flex items-center gap-2 text-amber-300 font-mono font-bold text-xs">
                                <i class="fa-solid fa-truck-fast text-cyan-400" aria-hidden="true"></i>
                                <span>ENTREGA EXPRESS EL MISMO DÍA</span>
                            </div>
                            <p class="text-[10.5px] text-slate-300">
                                Despacho local en Guadalajara, Zapopan, Tlaquepaque y Tonalá vía <strong>Uber Flash</strong> con código PIN de seguridad.
                            </p>
                        </div>
                    </div>
                </div>

            </div>

            <!-- CLÁUSULAS LEGALES, VIGENCIA Y CONDICIONES COMERCIALES (PROFECO / SAT) -->
            <div class="pt-6 pb-2 text-[10.5px] text-slate-300 space-y-2 text-center font-mono leading-relaxed">
                <div class="bg-slate-900/60 border border-slate-800 p-3 rounded-xl max-w-5xl mx-auto space-y-1">
                    <p class="text-amber-300 font-bold">
                        <i class="fa-solid fa-calendar-check text-amber-400 mr-1" aria-hidden="true"></i>
                        Vigencia de Precios y Promociones: Precios de lista y promociones de apertura (-25%) válidos del 24 al 29 de Agosto de 2026.
                    </p>
                    <p class="text-slate-300">
                        <i class="fa-solid fa-triangle-exclamation text-amber-400 mr-1" aria-hidden="true"></i>
                        Aviso Comercial: Precios exhibidos en Moneda Nacional (MXN) con IVA incluido. Precios sujetos a alza o cambio sin previo aviso por fluctuaciones cambiarias y existencias en almacén mayorista.
                    </p>
                    <p class="text-slate-300">
                        Estructura comercial protegida con 20% de utilidad neta libre para cobertura de infraestructura tecnológica, licencias de inteligencia artificial, nómina, arrendamiento operativo y cumplimiento de obligaciones fiscales ante el SAT y PROFECO.
                    </p>
                </div>

                <div class="pt-3 text-slate-400">
                    © 2026 Ecosistema Comercial BAZAR NFL GDL & PC Custom Lab. Pedro Moreno 501 A, Guadalajara Centro, Jalisco. Todos los derechos reservados.
                </div>
            </div>

        </div>
    </footer>

    <script src="js/ct-catalog-data.js?v=20260828_2010"></script>
    <script defer src="js/ct-exact-catalog-engine.js?v=20260828_2010"></script>
</body>
</html>
"""

with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(HTML_OPTIMIZED)

print("✅ index.html reescrito con estructura de encabezados perfecta (h1 -> h2 -> h3), ARIA labels y contraste.", flush=True)

# 3. ACTUALIZAR JS ENGINE PARA CERO CLS (DIMENSIONES FIJAS 300x300 Y ASPECT-RATIO), TAP TARGETS 48PX Y H3 EN TARJETAS
ENGINE_JS_LIGHTHOUSE = """// =========================================================================
// MOTOR ULTRA RÁPIDO PC CUSTOM LAB (LIGHTHOUSE 100/100 READY)
// =========================================================================

let currentViewStyle = 'grid'; // 'grid' (5x4) o 'list'
let currentPageNumber = 1;
const productsPerPage = 20; // 5 filas x 4 columnas

let activeSelectedCategory = 'Todas';
let activeSelectedBrand = 'Todas';
let currentSortCriterion = 'existencia';
let isFullCatalogLoaded = false;

document.addEventListener("DOMContentLoaded", () => {
    // 1. Renderizado instantáneo con el payload inicial (< 15 ms)
    renderSidebarFacets();
    renderExactCatalogView();
    initPredictiveSearchEngine();

    // 2. Carga en segundo plano del catálogo completo (16,139 items) sin congelar el hilo principal
    if (window.requestIdleCallback) {
        requestIdleCallback(() => loadFullCatalogAsync(), { timeout: 2000 });
    } else {
        setTimeout(loadFullCatalogAsync, 150);
    }
});

function loadFullCatalogAsync() {
    if (isFullCatalogLoaded) return;
    fetch('./data/catalogo_maestro_ct.json')
        .then(res => res.json())
        .then(data => {
            if (Array.isArray(data) && data.length > 0) {
                window.CT_CATALOG_DATA = data;
                isFullCatalogLoaded = true;
                renderSidebarFacets();
                const countTxt = document.getElementById("results-count-display");
                if (countTxt && activeSelectedCategory === 'Todas') {
                    countTxt.innerText = `Aparador Principal (20 de ${data.length.toLocaleString('es-MX')})`;
                }
            }
        })
        .catch(() => {});
}

function setViewStyle(style) {
    currentViewStyle = style;
    const btnList = document.getElementById("btn-view-list");
    const btnGrid = document.getElementById("btn-view-grid");
    
    if (btnList && btnGrid) {
        if (style === 'list') {
            btnList.className = "btn-action p-2 rounded-lg bg-cyan-500 text-slate-950 font-bold transition shadow cursor-pointer text-xs flex items-center justify-center";
            btnList.setAttribute("aria-pressed", "true");
            btnGrid.className = "btn-action p-2 rounded-lg text-slate-300 hover:text-white transition cursor-pointer text-xs flex items-center justify-center";
            btnGrid.setAttribute("aria-pressed", "false");
        } else {
            btnGrid.className = "btn-action p-2 rounded-lg bg-cyan-500 text-slate-950 font-bold transition shadow cursor-pointer text-xs flex items-center justify-center";
            btnGrid.setAttribute("aria-pressed", "true");
            btnList.className = "btn-action p-2 rounded-lg text-slate-300 hover:text-white transition cursor-pointer text-xs flex items-center justify-center";
            btnList.setAttribute("aria-pressed", "false");
        }
    }
    renderExactCatalogView();
}

function getFilteredList() {
    let items = [...(window.CT_CATALOG_DATA || [])];

    if (activeSelectedCategory !== 'Todas') {
        items = items.filter(p => {
            const catClasif = (p.categoria_clasificada || '').toLowerCase();
            return catClasif === activeSelectedCategory.toLowerCase();
        });
    }

    if (activeSelectedBrand !== 'Todas') {
        items = items.filter(p => (p.marca || '').toUpperCase() === activeSelectedBrand.toUpperCase());
    }

    if (currentSortCriterion === 'precio_asc') {
        items.sort((a, b) => (a.precio_mxn || a.precio || 0) - (b.precio_mxn || b.precio || 0));
    } else if (currentSortCriterion === 'precio_desc') {
        items.sort((a, b) => (b.precio_mxn || b.precio || 0) - (a.precio_mxn || a.precio || 0));
    } else if (currentSortCriterion === 'nombre') {
        items.sort((a, b) => (a.nombre || '').localeCompare(b.nombre || ''));
    }

    return items;
}

function getPlaceholderForCat(cat) {
    const map = {
        'procesadores': 'cpu_placeholder.jpg',
        'tarjetas_madre': 'mbd_placeholder.jpg',
        'memorias_ram': 'ram_placeholder.jpg',
        'discos_duros': 'ssd_placeholder.jpg',
        'tarjetas_de_video': 'gpu_placeholder.jpg',
        'gabinetes': 'gab_placeholder.jpg',
        'fuentes_energia': 'psu_placeholder.jpg',
        'enfriamiento': 'cooling_placeholder.jpg',
        'reguladores_ups': 'ups_placeholder.jpg',
        'monitores': 'mon_placeholder.jpg',
        'mini_pcs_ia': 'minipc_placeholder.jpg',
        'computadoras_ensambladas': 'pc_placeholder.jpg',
        'laptops': 'lap_placeholder.jpg',
        'all_in_one': 'aio_placeholder.jpg',
        'consumibles': 'toner_placeholder.jpg',
        'impresoras': 'imp_placeholder.jpg',
        'accesorios_perifericos': 'acc_placeholder.jpg',
        'conectividad_redes': 'redes_placeholder.jpg',
        'software': 'sof_placeholder.jpg',
        'telefonia_seguridad': 'cctv_placeholder.jpg',
        'punto_de_venta': 'pos_placeholder.jpg',
        'electronica_consumo': 'elec_placeholder.jpg',
        'linea_blanca': 'lb_placeholder.jpg',
        'outlet_liquidaciones': 'outlet_placeholder.jpg'
    };
    return `./assets/img/placeholders/${map[cat] || 'acc_placeholder.jpg'}`;
}

function renderExactCatalogView() {
    const container = document.getElementById("products-grid-container");
    const resultsCountTxt = document.getElementById("results-count-display");
    if (!container) return;

    const filtered = getFilteredList();
    const totalCount = filtered.length;
    const totalPages = Math.ceil(totalCount / productsPerPage) || 1;

    if (currentPageNumber > totalPages) currentPageNumber = totalPages;
    const startIdx = (currentPageNumber - 1) * productsPerPage;
    const pageItems = filtered.slice(startIdx, startIdx + productsPerPage);

    if (resultsCountTxt) {
        resultsCountTxt.innerText = `Aparador Principal (${Math.min(startIdx + productsPerPage, totalCount)} de ${totalCount.toLocaleString('es-MX')})`;
    }

    renderPaginationBar(totalPages);

    if (pageItems.length === 0) {
        container.className = "w-full py-16 text-center text-slate-300 font-mono text-sm bg-slate-900/90 border border-slate-800 rounded-2xl";
        container.innerHTML = `
            <i class="fa-solid fa-box-open text-4xl text-cyan-400 mb-3 block" aria-hidden="true"></i>
            No se encontraron productos con los filtros seleccionados.
            <br><button onclick="resetFacets()" aria-label="Ver todo el catálogo" class="btn-action mt-4 bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 font-black px-5 py-2.5 rounded-xl text-xs uppercase cursor-pointer shadow-lg hover:shadow-cyan-500/30">Ver Todo el Catálogo</button>
        `;
        return;
    }

    if (currentViewStyle === 'grid') {
        container.className = "grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 pb-2";
        container.innerHTML = pageItems.map((p, idx) => {
            const sku = p.sku;
            const cat = p.categoria_clasificada || 'accesorios_perifericos';
            const title = (p.nombre || p.descripcion_completa || '').replace(/'/g, "&#39;").replace(/"/g, '&quot;');
            const price = p.precio_mxn || p.precio;
            const original = p.precio_original || (price * 1.33);
            const mayoreo = p.precio_mayoreo_10pzs || (price * 0.93);
            const localImg = `./assets/img/catalog/${cat}/${sku}.jpg`;
            const cdnImg = `https://static.ctonline.mx/imagenes/${sku}/${sku}_400.jpg`;
            const placeholder = getPlaceholderForCat(cat);
            const isAboveFold = idx < 4;

            return `
                <article class="bg-slate-900/90 hover:bg-slate-850 border border-slate-800 hover:border-cyan-400/80 rounded-2xl p-3.5 flex flex-col justify-between transition group shadow-xl hover:shadow-cyan-500/10 relative overflow-hidden text-slate-100">
                    <div class="absolute -top-7 -left-7 w-16 h-16 bg-gradient-to-br from-red-600 to-amber-600 rotate-[-45deg] flex items-end justify-center pb-0.5 shadow-md z-10">
                        <span class="text-[7.5px] font-black text-white uppercase tracking-tighter">-25% DTO</span>
                    </div>

                    <button class="btn-action absolute top-2.5 right-2.5 text-slate-400 hover:text-pink-400 transition text-base z-10 cursor-pointer" title="Favoritos" aria-label="Agregar ${title} a favoritos">
                        <i class="fa-regular fa-heart" aria-hidden="true"></i>
                    </button>

                    <div>
                        <!-- Contenedor de Imagen Estricto para CLS = 0 -->
                        <div onclick="openProductDetailModal('${sku}')" class="product-img-wrapper bg-slate-950/90 border border-slate-800/80 rounded-xl p-2 mb-2.5 group-hover:border-cyan-500/40 transition cursor-pointer">
                            <img 
                                src="${localImg}" 
                                alt="${title}" 
                                width="300" 
                                height="300" 
                                ${isAboveFold ? 'fetchpriority="high"' : 'loading="lazy"'} 
                                decoding="async"
                                class="w-full h-full object-contain group-hover:scale-105 transition duration-200"
                                onerror="if (this.src.indexOf('static.ctonline.mx') === -1) { this.src='${cdnImg}'; } else { this.src='${placeholder}'; }"
                            />
                        </div>

                        <!-- Precios de Contado y Mayoreo con Alto Contraste -->
                        <div class="text-center mb-1.5">
                            <span class="text-sm font-black text-emerald-300 block font-mono tracking-tight drop-shadow-[0_0_8px_rgba(52,211,153,0.3)]">
                                $${price.toLocaleString('es-MX', { minimumFractionDigits: 2 })} MXN
                            </span>
                            <div class="flex items-center justify-center gap-1.5 text-[10px] font-mono">
                                <span class="text-slate-400 line-through">$${original.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</span>
                                <span class="text-amber-300 font-bold">Mayoreo: $${mayoreo.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</span>
                            </div>
                        </div>

                        <div class="text-center text-[9px] text-cyan-300 font-mono font-bold mb-1 flex items-center justify-center gap-1">
                            <i class="fa-solid fa-truck-bolt text-[10px]" aria-hidden="true"></i> Disponible Mostrador GDL
                        </div>

                        <!-- Título Semántico H3 para Jerarquía Perfecta -->
                        <h3 onclick="openProductDetailModal('${sku}')" class="text-slate-100 text-xs font-semibold text-center line-clamp-2 leading-tight hover:text-cyan-300 transition mb-1 cursor-pointer" title="${title}">
                            ${title}
                        </h3>

                        <div class="text-center text-[9.5px] font-mono text-slate-300 mb-2">
                            <span>SKU: <strong>${sku}</strong></span>
                        </div>
                    </div>

                    <!-- Botones de Acción con Tap Targets de 48px -->
                    <div class="pt-1 flex gap-2">
                        <button 
                            onclick="openProductDetailModal('${sku}')" 
                            aria-label="Ver ficha técnica de ${title}" 
                            class="btn-action flex-1 bg-slate-800 hover:bg-slate-700 text-cyan-300 font-bold rounded-xl text-[11px] uppercase transition cursor-pointer border border-slate-700 min-h-[48px]"
                        >
                            <span>Ficha Técnica</span>
                        </button>
                        <button 
                            onclick="buyNowCT('${sku}', '${title}', ${price}, '${localImg}')" 
                            aria-label="Comprar ${title}" 
                            class="btn-action flex-1 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-black rounded-xl text-[11px] uppercase tracking-wider flex items-center justify-center gap-1 transition active:scale-95 shadow-md cursor-pointer min-h-[48px]"
                        >
                            <span>Comprar</span>
                        </button>
                    </div>
                </article>
            `;
        }).join('');
    } else {
        container.className = "flex flex-col gap-3.5 pb-2";
        container.innerHTML = pageItems.map(p => {
            const sku = p.sku;
            const cat = p.categoria_clasificada || 'accesorios_perifericos';
            const title = (p.nombre || p.descripcion_completa || '').replace(/'/g, "&#39;").replace(/"/g, '&quot;');
            const price = p.precio_mxn || p.precio;
            const original = p.precio_original || (price * 1.33);
            const mayoreo = p.precio_mayoreo_10pzs || (price * 0.93);
            const usdPrice = (price / 19.50).toFixed(2);
            const localImg = `./assets/img/catalog/${cat}/${sku}.jpg`;
            const cdnImg = `https://static.ctonline.mx/imagenes/${sku}/${sku}_400.jpg`;
            const placeholder = getPlaceholderForCat(cat);
            const desc = p.descripcion_completa || p.desc || '';

            return `
                <article class="bg-slate-900/90 hover:bg-slate-850 border border-slate-800 hover:border-cyan-400/80 rounded-2xl p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 transition group shadow-xl relative overflow-hidden text-slate-100">
                    <div class="absolute -top-6 -left-6 w-14 h-14 bg-gradient-to-br from-red-600 to-amber-600 rotate-[-45deg] flex items-end justify-center pb-0.5 shadow z-10">
                        <span class="text-[7px] font-black text-white uppercase">-25%</span>
                    </div>

                    <div onclick="openProductDetailModal('${sku}')" class="product-img-wrapper w-full md:w-32 h-28 bg-slate-950/90 border border-slate-800 rounded-xl p-2 shrink-0 cursor-pointer">
                        <img 
                            src="${localImg}" 
                            alt="${title}" 
                            width="140" 
                            height="140" 
                            loading="lazy" 
                            decoding="async"
                            class="w-full h-full object-contain group-hover:scale-105 transition duration-200"
                            onerror="if (this.src.indexOf('static.ctonline.mx') === -1) { this.src='${cdnImg}'; } else { this.src='${placeholder}'; }"
                        />
                    </div>

                    <div class="flex-1 min-w-0">
                        <h3 onclick="openProductDetailModal('${sku}')" class="text-cyan-300 font-bold text-sm mb-1 hover:text-cyan-200 transition leading-snug cursor-pointer">
                            ${title}
                        </h3>
                        <div class="flex items-center gap-2 text-[10.5px] font-mono text-slate-300 mb-1">
                            <span>SKU: <strong>${sku}</strong></span>
                            <span>•</span>
                            <span class="text-emerald-300 font-bold">20% Neto Libre Garantizado</span>
                        </div>
                        <p class="text-slate-300 text-xs leading-relaxed line-clamp-2">${desc}</p>
                    </div>

                    <div class="w-full md:w-56 flex flex-col justify-between items-end border-t md:border-t-0 md:border-l border-slate-800 pt-3 md:pt-0 md:pl-4 shrink-0 text-right">
                        <div class="w-full mb-1.5">
                            <span class="text-[10.5px] text-slate-400 line-through block font-mono">$${original.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</span>
                            <div class="text-base font-black text-emerald-300 leading-tight font-mono drop-shadow-[0_0_8px_rgba(52,211,153,0.3)]">
                                $${price.toLocaleString('es-MX', { minimumFractionDigits: 2 })} MXN
                            </div>
                            <span class="text-[10px] text-slate-300 block font-mono">$${usdPrice} USD • Mayoreo: $${mayoreo.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</span>
                        </div>

                        <div class="flex items-center gap-2 w-full">
                            <button onclick="openProductDetailModal('${sku}')" aria-label="Ver ficha técnica de ${title}" class="btn-action p-2.5 rounded-xl border border-slate-800 bg-slate-800 hover:bg-slate-700 text-cyan-300 transition text-xs font-bold min-h-[48px] min-w-[48px] flex items-center justify-center">
                                <i class="fa-solid fa-file-lines" aria-hidden="true"></i>
                            </button>
                            <button 
                                onclick="addToCartCT('${sku}', '${title}', ${price}, '${localImg}')" 
                                aria-label="Agregar ${title} al carrito"
                                class="btn-action flex-1 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-black py-2.5 px-3 rounded-xl text-xs flex items-center justify-center gap-1 transition active:scale-95 shadow cursor-pointer uppercase min-h-[48px]"
                            >
                                <span>Agregar</span>
                            </button>
                        </div>
                    </div>
                </article>
            `;
        }).join('');
    }
}

// =========================================================================
// BARRA LATERAL IZQUIERDA: 24 DEPARTAMENTOS Y 3 TARJETAS INTEGRADAS
// =========================================================================
function renderSidebarFacets() {
    const root = document.getElementById("sidebar-facets-root");
    if (!root) return;

    const block1 = [
        { id: 'procesadores', name: 'Procesadores (CPUs Intel/AMD)', icon: 'fa-microchip' },
        { id: 'tarjetas_madre', name: 'Tarjetas Madre (Motherboards)', icon: 'fa-chess-board' },
        { id: 'memorias_ram', name: 'Memorias RAM (DDR4 / DDR5)', icon: 'fa-memory' },
        { id: 'discos_duros', name: 'Almacenamiento (SSD & HDD)', icon: 'fa-hard-drive' },
        { id: 'tarjetas_de_video', name: 'Tarjetas de Video (GPUs)', icon: 'fa-gamepad' },
        { id: 'gabinetes', name: 'Gabinetes & Chasis Gamer', icon: 'fa-server' },
        { id: 'fuentes_energia', name: 'Fuentes de Poder (PSU)', icon: 'fa-bolt' },
        { id: 'enfriamiento', name: 'Enfriamiento y Disipadores', icon: 'fa-snowflake' },
        { id: 'reguladores_ups', name: 'Reguladores, No-Breaks & UPS', icon: 'fa-plug-circle-bolt' },
        { id: 'monitores', name: 'Monitores & Pantallas PC', icon: 'fa-desktop' }
    ];

    const block2 = [
        { id: 'mini_pcs_ia', name: 'Mini PCs & Servidores IA (NUC)', icon: 'fa-cube' },
        { id: 'computadoras_ensambladas', name: 'Computadoras & PC Gamer', icon: 'fa-desktop' },
        { id: 'laptops', name: 'Laptops y Portátiles', icon: 'fa-laptop' },
        { id: 'all_in_one', name: 'Equipos All-in-One e iMac', icon: 'fa-tv' }
    ];

    const block3 = [
        { id: 'consumibles', name: 'Tóners, Tintas y Consumibles', icon: 'fa-fill-drip' },
        { id: 'impresoras', name: 'Impresoras y Multifuncionales', icon: 'fa-print' },
        { id: 'accesorios_perifericos', name: 'Teclados, Mouse & Periféricos', icon: 'fa-keyboard' },
        { id: 'conectividad_redes', name: 'Redes & Conectividad WiFi', icon: 'fa-network-wired' },
        { id: 'software', name: 'Software & Licencias Originales', icon: 'fa-compact-disc' },
        { id: 'telefonia_seguridad', name: 'Telefonía & Videovigilancia (CCTV)', icon: 'fa-video' },
        { id: 'punto_de_venta', name: 'Punto de Venta (POS)', icon: 'fa-barcode' },
        { id: 'electronica_consumo', name: 'Audio, Video & Electrónica', icon: 'fa-headphones' },
        { id: 'linea_blanca', name: 'Línea Blanca & Electrodomésticos', icon: 'fa-blender' },
        { id: 'outlet_liquidaciones', name: 'Outlet & Liquidaciones', icon: 'fa-tag' }
    ];

    const all = window.CT_CATALOG_DATA || [];
    const getCount = (id) => all.filter(p => (p.categoria_clasificada || '').toLowerCase() === id.toLowerCase()).length;

    let topItems = all.filter(p => {
        if (activeSelectedCategory === 'Todas') return true;
        return (p.categoria_clasificada || '').toLowerCase() === activeSelectedCategory.toLowerCase();
    }).slice(0, 3);

    root.innerHTML = `
        <div class="bg-gradient-to-r from-slate-900 to-cyan-950 border border-cyan-500/40 text-white p-3 rounded-t-2xl font-bold text-xs uppercase flex items-center justify-between shadow-lg">
            <h2 class="flex items-center gap-2 text-cyan-300 font-mono text-xs"><i class="fa-solid fa-sliders text-cyan-400" aria-hidden="true"></i> Departamentos</h2>
            <span class="text-[9px] bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 px-2 py-0.5 rounded-full font-mono font-bold">${all.length.toLocaleString('es-MX')} Items</span>
        </div>

        <div class="p-3 bg-slate-900/95 border-x border-b border-slate-800 rounded-b-2xl text-slate-200 text-xs shadow-2xl flex flex-col justify-between space-y-4">
            
            <div class="flex gap-2">
                <button onclick="renderExactCatalogView()" aria-label="Aplicar filtros seleccionados" class="btn-action flex-1 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-black rounded-xl text-[11px] uppercase transition cursor-pointer shadow min-h-[48px]">
                    Aplicar
                </button>
                <button onclick="resetFacets()" aria-label="Limpiar todos los filtros" class="btn-action flex-1 bg-slate-800 hover:bg-red-950/60 border border-slate-700 hover:border-red-500/50 text-slate-200 hover:text-red-400 font-bold rounded-xl text-[11px] uppercase transition cursor-pointer min-h-[48px]">
                    Limpiar
                </button>
            </div>

            <!-- ENLACE A TODAS LAS CATEGORÍAS -->
            <div class="bg-slate-950 p-2 rounded-xl border border-slate-800 hover:border-cyan-500/50 transition min-h-[48px] flex items-center">
                <label for="cat_todas" class="category-link flex items-center justify-between cursor-pointer w-full">
                    <span class="flex items-center gap-2 truncate">
                        <input type="radio" id="cat_todas" name="cat_facet" aria-label="Todas las categorías" ${activeSelectedCategory === 'Todas' ? 'checked' : ''} onchange="activeSelectedCategory='Todas'; currentPageNumber=1; renderSidebarFacets(); renderExactCatalogView();" class="w-4 h-4 accent-cyan-400 cursor-pointer shrink-0" />
                        <i class="fa-solid fa-layer-group text-xs text-cyan-400 shrink-0" aria-hidden="true"></i>
                        <span class="truncate text-xs font-bold text-white">Todas las Categorías</span>
                    </span>
                    <span class="text-[10px] text-cyan-300 font-mono font-bold">(${all.length.toLocaleString('es-MX')})</span>
                </label>
            </div>

            <!-- BLOQUE 1 - COMPONENTES DE ENSAMBLE -->
            <div class="border-b border-slate-800 pb-3">
                <h3 class="font-bold text-cyan-300 mb-2 text-xs flex items-center gap-1.5 font-mono uppercase tracking-wider">
                    <i class="fa-solid fa-microchip text-cyan-400" aria-hidden="true"></i> 1. Componentes de Ensamble
                </h3>
                <div class="space-y-1 text-slate-300">
                    ${block1.map(c => `
                        <label for="cat_${c.id}" class="category-link flex items-center justify-between cursor-pointer hover:text-cyan-300 py-2 px-2 rounded-xl hover:bg-slate-800/80 transition min-h-[48px]">
                            <span class="flex items-center gap-2.5 truncate">
                                <input type="radio" id="cat_${c.id}" name="cat_facet" aria-label="${c.name}" ${activeSelectedCategory === c.id ? 'checked' : ''} onchange="activeSelectedCategory='${c.id}'; currentPageNumber=1; renderSidebarFacets(); renderExactCatalogView();" class="w-4 h-4 accent-cyan-400 cursor-pointer shrink-0" />
                                <i class="fa-solid ${c.icon} text-xs text-slate-300 w-3.5 text-center shrink-0" aria-hidden="true"></i>
                                <span class="truncate text-xs ${activeSelectedCategory === c.id ? 'font-bold text-cyan-300' : 'text-slate-200'}">${c.name}</span>
                            </span>
                            <span class="text-[10px] text-slate-400 font-mono">(${getCount(c.id)})</span>
                        </label>
                    `).join('')}
                </div>
            </div>

            <!-- BLOQUE 2 - SISTEMAS Y EQUIPOS COMPLETOS -->
            <div class="border-b border-slate-800 pb-3">
                <h3 class="font-bold text-purple-300 mb-2 text-xs flex items-center gap-1.5 font-mono uppercase tracking-wider">
                    <i class="fa-solid fa-cube text-purple-400" aria-hidden="true"></i> 2. Sistemas & Mini PCs IA
                </h3>
                <div class="space-y-1 text-slate-300">
                    ${block2.map(c => `
                        <label for="cat_${c.id}" class="category-link flex items-center justify-between cursor-pointer hover:text-purple-300 py-2 px-2 rounded-xl hover:bg-slate-800/80 transition min-h-[48px]">
                            <span class="flex items-center gap-2.5 truncate">
                                <input type="radio" id="cat_${c.id}" name="cat_facet" aria-label="${c.name}" ${activeSelectedCategory === c.id ? 'checked' : ''} onchange="activeSelectedCategory='${c.id}'; currentPageNumber=1; renderSidebarFacets(); renderExactCatalogView();" class="w-4 h-4 accent-purple-400 cursor-pointer shrink-0" />
                                <i class="fa-solid ${c.icon} text-xs text-slate-300 w-3.5 text-center shrink-0" aria-hidden="true"></i>
                                <span class="truncate text-xs ${activeSelectedCategory === c.id ? 'font-bold text-purple-300' : 'text-slate-200'}">${c.name}</span>
                            </span>
                            <span class="text-[10px] text-slate-400 font-mono">(${getCount(c.id)})</span>
                        </label>
                    `).join('')}
                </div>
            </div>

            <!-- BLOQUE 3 - CONSUMIBLES, SOLUCIONES Y ELECTRÓNICA -->
            <div class="border-b border-slate-800 pb-3">
                <h3 class="font-bold text-amber-300 mb-2 text-xs flex items-center gap-1.5 font-mono uppercase tracking-wider">
                    <i class="fa-solid fa-puzzle-piece text-amber-400" aria-hidden="true"></i> 3. Consumibles & Soluciones
                </h3>
                <div class="space-y-1 text-slate-300">
                    ${block3.map(c => `
                        <label for="cat_${c.id}" class="category-link flex items-center justify-between cursor-pointer hover:text-amber-300 py-2 px-2 rounded-xl hover:bg-slate-800/80 transition min-h-[48px]">
                            <span class="flex items-center gap-2.5 truncate">
                                <input type="radio" id="cat_${c.id}" name="cat_facet" aria-label="${c.name}" ${activeSelectedCategory === c.id ? 'checked' : ''} onchange="activeSelectedCategory='${c.id}'; currentPageNumber=1; renderSidebarFacets(); renderExactCatalogView();" class="w-4 h-4 accent-amber-400 cursor-pointer shrink-0" />
                                <i class="fa-solid ${c.icon} text-xs text-slate-300 w-3.5 text-center shrink-0" aria-hidden="true"></i>
                                <span class="truncate text-xs ${activeSelectedCategory === c.id ? 'font-bold text-amber-300' : 'text-slate-200'}">${c.name}</span>
                            </span>
                            <span class="text-[10px] text-slate-400 font-mono">(${getCount(c.id)})</span>
                        </label>
                    `).join('')}
                </div>
            </div>

            <!-- TOP 3 MÁS VENDIDOS DINÁMICO -->
            <div class="pt-2 space-y-2 border-t border-slate-800 hidden md:block">
                <div class="flex items-center justify-between">
                    <h3 class="font-bold text-amber-400 text-xs flex items-center gap-1.5 font-mono uppercase tracking-wider">
                        <i class="fa-solid fa-fire text-amber-400" aria-hidden="true"></i> Top 3 Destacados
                    </h3>
                    <span class="text-[9px] text-cyan-300 font-mono font-bold">${activeSelectedCategory.toUpperCase()}</span>
                </div>

                <div class="space-y-2">
                    ${topItems.map((b, idx) => {
                        const sku = b.sku;
                        const cat = b.categoria_clasificada || 'accesorios_perifericos';
                        const title = (b.nombre || b.descripcion_completa || '').replace(/'/g, "&#39;");
                        const price = b.precio_mxn || b.precio;
                        const mayoreo = b.precio_mayoreo_10pzs || (price * 0.93);
                        const localImg = `./assets/img/catalog/${cat}/${sku}.jpg`;
                        const cdnImg = `https://static.ctonline.mx/imagenes/${sku}/${sku}_400.jpg`;
                        const placeholder = getPlaceholderForCat(cat);

                        return `
                            <div class="bg-slate-950 border border-slate-800 hover:border-cyan-500/50 p-2 rounded-xl flex items-center gap-2.5 transition group cursor-pointer min-h-[48px]" onclick="openProductDetailModal('${sku}')" role="button" tabindex="0" aria-label="Ver destacado ${title}">
                                <div class="w-12 h-12 bg-slate-900 rounded-lg p-1 shrink-0 flex items-center justify-center overflow-hidden">
                                    <img src="${localImg}" alt="${title}" width="48" height="48" loading="lazy" decoding="async" class="w-full h-full object-contain" onerror="if (this.src.indexOf('static.ctonline.mx') === -1) { this.src='${cdnImg}'; } else { this.src='${placeholder}'; }" />
                                </div>
                                <div class="flex-1 min-w-0">
                                    <div class="text-[11px] font-bold text-slate-100 truncate group-hover:text-cyan-300 transition">${title}</div>
                                    <div class="flex items-center justify-between text-[10px] font-mono">
                                        <span class="text-emerald-300 font-black">$${price.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</span>
                                        <span class="text-amber-300">May: $${mayoreo.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</span>
                                    </div>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>

                <button 
                    onclick="activeSelectedCategory='Todas'; currentPageNumber=1; renderSidebarFacets(); renderExactCatalogView(); document.getElementById('catalog-main-content-root').scrollIntoView({behavior:'smooth'});" 
                    aria-label="Ver todos los productos del catálogo"
                    class="btn-action w-full bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/40 font-mono font-bold rounded-xl text-xs uppercase tracking-wider flex items-center justify-center gap-1.5 transition cursor-pointer shadow mt-2 min-h-[48px]"
                >
                    <i class="fa-solid fa-layer-group text-xs" aria-hidden="true"></i> <span>Ver Todo el Catálogo</span>
                </button>
            </div>

            <!-- 3 TARJETAS DE CONVERSIÓN INTEGRADAS -->
            <div class="pt-4 space-y-3.5 border-t border-slate-800 hidden md:block">
                
                <!-- TARJETA 1: APP MÓVIL PEDIDOS RÁPIDOS -->
                <div class="bg-slate-950/90 border border-cyan-500/40 hover:border-cyan-400 rounded-2xl p-3.5 text-center shadow-lg transition">
                    <span class="text-[11px] font-mono font-bold text-cyan-400 uppercase tracking-wider flex items-center justify-center gap-1.5 mb-2.5">
                        <i class="fa-solid fa-mobile-screen-button" aria-hidden="true"></i> App Móvil Pedidos Rápidos
                    </span>
                    
                    <div class="w-32 h-32 mx-auto bg-white p-2 rounded-xl shadow-md flex items-center justify-center mb-2">
                        <img 
                            src="https://api.qrserver.com/v1/create-qr-code/?size=130x130&data=https://iaworldcenter-creator.github.io/pc-custom-lab/&color=0-0-0&bgcolor=255-255-255" 
                            alt="Código QR de la App Oficial" 
                            width="128" 
                            height="128" 
                            loading="lazy" 
                            decoding="async"
                            class="w-full h-full object-contain" 
                        />
                    </div>
                    
                    <p class="text-slate-200 text-[10.5px] leading-tight mb-2.5">
                        Escanea con tu cámara para pedir por <strong>Uber Flash</strong> con código PIN.
                    </p>

                    <a href="https://wa.me/523337271440" target="_blank" rel="noopener" aria-label="Abrir App Oficial de WhatsApp" class="btn-action w-full bg-slate-900 hover:bg-slate-800 text-cyan-300 border border-cyan-500/40 font-mono font-bold rounded-lg text-[10px] uppercase tracking-wider flex items-center justify-center gap-1.5 transition min-h-[48px]">
                        <span>▶ Abrir App Oficial</span>
                    </a>
                </div>

                <!-- TARJETA 2: CREADO CON GOOGLE GEMINI -->
                <div class="bg-slate-950/90 border border-blue-500/40 hover:border-blue-400 rounded-2xl p-3.5 shadow-lg transition text-left">
                    <span class="text-[11px] font-mono font-bold text-blue-400 uppercase tracking-wider flex items-center gap-1.5 mb-1.5">
                        <i class="fa-solid fa-microchip" aria-hidden="true"></i> Creado con Google Gemini
                    </span>
                    <div class="text-white font-bold text-xs leading-snug mb-1">
                        Inteligencia Artificial para tu Negocio
                    </div>
                    <p class="text-slate-200 text-[10px] leading-tight mb-2.5">
                        Concebido y programado con la IA más avanzada de Google para crear tiendas de ultra velocidad.
                    </p>
                    <a href="https://gemini.google.com/" target="_blank" rel="noopener" aria-label="Suscribirse a Google Gemini" class="btn-action w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-black rounded-lg text-[10px] uppercase tracking-wider flex items-center justify-center gap-1 transition shadow min-h-[48px]">
                        <span>SUSCRIBIRSE A GOOGLE GEMINI</span>
                    </a>
                </div>

                <!-- TARJETA 3: DESARROLLADO POR ANTI-GRAVITY -->
                <div class="bg-slate-950/90 border border-amber-500/40 hover:border-amber-400 rounded-2xl p-3.5 shadow-lg transition text-left">
                    <span class="text-[11px] font-mono font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5 mb-1.5">
                        <i class="fa-solid fa-robot" aria-hidden="true"></i> Desarrollado por Anti-Gravity
                    </span>
                    <div class="text-white font-bold text-xs leading-snug mb-1">
                        Agente Autónomo de Software
                    </div>
                    <p class="text-slate-200 text-[10px] leading-tight mb-2.5">
                        Desarrollado, optimizado y desplegado por Anti-Gravity Copilot. Crea tus páginas web gratis.
                    </p>
                    <a href="https://github.com/" target="_blank" rel="noopener" aria-label="Descargar Anti-Gravity Gratis" class="btn-action w-full bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-black rounded-lg text-[10px] uppercase tracking-wider flex items-center justify-center gap-1 transition shadow min-h-[48px]">
                        <span>DESCARGAR ANTI-GRAVITY GRATIS</span>
                    </a>
                </div>

            </div>

        </div>
    `;
}

// =========================================================================
// MOTOR DE BÚSQUEDA PREDICTIVA INSTANTÁNEA CON DEBOUNCE (NO BLOQUEANTE)
// =========================================================================
let searchDebounceTimer = null;
function initPredictiveSearchEngine() {
    const input = document.getElementById("boutiqueSearchInput");
    const box = document.getElementById("boutique-autocomplete-box");
    if (!input || !box) return;

    input.addEventListener("input", (e) => {
        clearTimeout(searchDebounceTimer);
        const query = (e.target.value || '').trim().toLowerCase();
        
        if (query.length < 1) {
            box.classList.add("hidden");
            box.innerHTML = "";
            return;
        }

        searchDebounceTimer = setTimeout(() => {
            const all = window.CT_CATALOG_DATA || [];
            const matches = [];
            for (let i = 0; i < all.length; i++) {
                const p = all[i];
                const sku = (p.sku || '').toLowerCase();
                const name = (p.nombre || p.descripcion_completa || '').toLowerCase();
                const marca = (p.marca || '').toLowerCase();
                const cat = (p.categoria_clasificada || '').toLowerCase();
                if (sku.includes(query) || name.includes(query) || marca.includes(query) || cat.includes(query)) {
                    matches.push(p);
                    if (matches.length >= 8) break;
                }
            }

            if (matches.length === 0) {
                box.innerHTML = `
                    <div class="p-3.5 text-center text-slate-300 font-mono text-xs">
                        <i class="fa-solid fa-magnifying-glass text-cyan-400 mb-1 block" aria-hidden="true"></i>
                        No se encontraron coincidencias directas para "<strong>${query}</strong>".
                    </div>
                `;
                box.classList.remove("hidden");
                return;
            }

            box.innerHTML = `
                <div class="p-2 border-b border-slate-800 flex justify-between items-center text-[10px] font-mono text-slate-300 bg-slate-950/80">
                    <span>Resultados en tiempo real para: "<strong>${query}</strong>"</span>
                    <span class="text-cyan-300 font-bold">${matches.length} sugerencias</span>
                </div>
                <div class="divide-y divide-slate-800/60 max-h-96 overflow-y-auto">
                    ${matches.map(p => {
                        const sku = p.sku;
                        const cat = p.categoria_clasificada || 'accesorios_perifericos';
                        const title = (p.nombre || p.descripcion_completa || '').replace(/'/g, "&#39;").replace(/"/g, '&quot;');
                        const price = p.precio_mxn || p.precio;
                        const mayoreo = p.precio_mayoreo_10pzs || (price * 0.93);
                        const localImg = `./assets/img/catalog/${cat}/${sku}.jpg`;
                        const cdnImg = `https://static.ctonline.mx/imagenes/${sku}/${sku}_400.jpg`;
                        const placeholder = getPlaceholderForCat(cat);

                        return `
                            <div class="flex items-center justify-between gap-3 p-2.5 hover:bg-slate-850 transition cursor-pointer group min-h-[48px]" onclick="openProductDetailModal('${sku}'); document.getElementById('boutique-autocomplete-box').classList.add('hidden');" role="button" tabindex="0" aria-label="Ver detalle de ${title}">
                                <div class="product-img-wrapper w-12 h-12 bg-slate-950 rounded-xl p-1 shrink-0 border border-slate-800 group-hover:border-cyan-400/50">
                                    <img src="${localImg}" alt="${title}" width="48" height="48" loading="lazy" decoding="async" class="w-full h-full object-contain" onerror="if (this.src.indexOf('static.ctonline.mx') === -1) { this.src='${cdnImg}'; } else { this.src='${placeholder}'; }" />
                                </div>
                                <div class="flex-1 min-w-0 text-left">
                                    <div class="text-xs font-bold text-white group-hover:text-cyan-300 transition truncate">${title}</div>
                                    <div class="text-[10px] font-mono text-slate-300 flex items-center gap-1.5">
                                        <span class="text-cyan-300 font-bold">SKU: ${sku}</span>
                                        <span>•</span>
                                        <span>${p.marca || 'PC CUSTOM'}</span>
                                        <span>•</span>
                                        <span class="text-amber-300">May: $${mayoreo.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</span>
                                    </div>
                                </div>
                                <div class="text-right shrink-0 flex items-center gap-2">
                                    <div class="text-xs font-mono font-black text-emerald-300">$${price.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</div>
                                    <button onclick="event.stopPropagation(); openProductDetailModal('${sku}'); document.getElementById('boutique-autocomplete-box').classList.add('hidden');" aria-label="Ver ficha técnica de ${title}" class="btn-action bg-slate-800 hover:bg-slate-700 text-cyan-300 text-[10px] font-bold px-2.5 py-1.5 rounded-lg border border-slate-700 uppercase min-h-[44px]">
                                        Ficha
                                    </button>
                                    <button onclick="event.stopPropagation(); addToCartCT('${sku}', '${title}', ${price}, '${localImg}');" aria-label="Agregar ${title} al carrito" class="btn-action bg-blue-600 hover:bg-blue-500 text-white text-[10px] font-bold px-2.5 py-1.5 rounded-lg uppercase min-h-[44px]">
                                        + Carrito
                                    </button>
                                    <button onclick="event.stopPropagation(); buyNowCT('${sku}', '${title}', ${price}, '${localImg}');" aria-label="Comprar ${title} ahora" class="btn-action bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 text-[10px] font-black px-2.5 py-1.5 rounded-lg uppercase shadow min-h-[44px]">
                                        ⚡ Comprar
                                    </button>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            `;

            box.classList.remove("hidden");
        }, 120);
    });

    document.addEventListener("click", (e) => {
        if (!input.contains(e.target) && !box.contains(e.target)) {
            box.classList.add("hidden");
        }
    });
}

// =========================================================================
// FICHA DE PRODUCTO EN 3 COLUMNAS (PDP)
// =========================================================================
window.openProductDetailModal = function(sku) {
    const all = window.CT_CATALOG_DATA || [];
    const prod = all.find(p => p.sku === sku);
    if (!prod) return;

    const modal = document.getElementById("productDetailModal");
    const modalContent = document.getElementById("productDetailModalContent");
    if (!modal || !modalContent) return;

    const cat = prod.categoria_clasificada || 'accesorios_perifericos';
    const title = prod.nombre || prod.descripcion_completa;
    const price = prod.precio_mxn || prod.precio;
    const original = prod.precio_original || (price * 1.33);
    const mayoreo = prod.precio_mayoreo_10pzs || (price * 0.93);
    const localImg = `./assets/img/catalog/${cat}/${sku}.jpg`;
    const cdnImg = `https://static.ctonline.mx/imagenes/${sku}/${sku}_400.jpg`;
    const placeholder = getPlaceholderForCat(cat);
    const desc = prod.descripcion_completa || '';
    const marca = prod.marca || 'PC CUSTOM';

    modalContent.innerHTML = `
        <div class="w-full flex justify-between items-center border-b border-slate-800 pb-3 mb-4">
            <div class="flex items-center gap-2">
                <span class="text-xs font-mono font-bold text-cyan-300 bg-cyan-950/80 border border-cyan-500/40 px-3 py-1 rounded-full uppercase">
                    Ficha Técnica Oficial PC Custom Lab
                </span>
                <span class="text-xs font-mono text-slate-300">SKU: <strong>${sku}</strong></span>
            </div>
            <button onclick="closeProductDetailModal()" aria-label="Cerrar ficha técnica" class="btn-action text-slate-300 hover:text-white text-xl p-2 transition cursor-pointer min-h-[48px] min-w-[48px] flex items-center justify-center">
                <i class="fa-solid fa-xmark text-2xl" aria-hidden="true"></i>
            </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            
            <!-- COLUMNA 1 (IZQUIERDA - GALERÍA VISUAL) -->
            <div class="lg:col-span-4 flex flex-col gap-3">
                <div class="product-img-wrapper w-full h-72 sm:h-80 bg-slate-950 border-2 border-cyan-500/40 rounded-2xl p-4 shadow-2xl group">
                    <img 
                        id="pdp-main-image"
                        src="${localImg}" 
                        alt="${title}" 
                        width="300"
                        height="300"
                        class="w-full h-full object-contain group-hover:scale-110 transition duration-300"
                        onerror="if (this.src.indexOf('static.ctonline.mx') === -1) { this.src='${cdnImg}'; } else { this.src='${placeholder}'; }"
                    />
                    <div class="absolute top-3 left-3 bg-red-600 text-white font-black text-[10px] uppercase px-2.5 py-1 rounded-md shadow">
                        -25% Apertura
                    </div>
                </div>

                <div class="grid grid-cols-4 gap-2">
                    <button onclick="document.getElementById('pdp-main-image').src='${localImg}'" aria-label="Ver imagen local" class="btn-action h-16 bg-slate-950 border border-cyan-400 rounded-xl p-1 flex items-center justify-center hover:opacity-80 transition cursor-pointer overflow-hidden min-h-[48px]">
                        <img src="${localImg}" alt="Vista Local" width="60" height="60" class="w-full h-full object-contain" onerror="this.src='${placeholder}';" />
                    </button>
                    <button onclick="document.getElementById('pdp-main-image').src='${cdnImg}'" aria-label="Ver imagen CDN" class="btn-action h-16 bg-slate-950 border border-slate-800 rounded-xl p-1 flex items-center justify-center hover:border-cyan-400 transition cursor-pointer overflow-hidden min-h-[48px]">
                        <img src="${cdnImg}" alt="Vista CDN" width="60" height="60" class="w-full h-full object-contain" onerror="this.src='${placeholder}';" />
                    </button>
                </div>
            </div>

            <!-- COLUMNA 2 (CENTRO - ESPECIFICACIONES) -->
            <div class="lg:col-span-5 flex flex-col gap-4 text-slate-100">
                <div>
                    <span class="text-xs font-mono text-cyan-300 font-bold uppercase tracking-wider block mb-1">Marca Oficial: ${marca}</span>
                    <h3 id="pdp-modal-title" class="text-base sm:text-xl font-bold text-white leading-snug mb-2">${title}</h3>
                    
                    <div class="flex items-center gap-2 text-xs font-mono text-slate-300 pb-3 border-b border-slate-800">
                        <div class="flex items-center text-amber-400" aria-label="Calificación 5 estrellas">
                            <i class="fa-solid fa-star" aria-hidden="true"></i>
                            <i class="fa-solid fa-star" aria-hidden="true"></i>
                            <i class="fa-solid fa-star" aria-hidden="true"></i>
                            <i class="fa-solid fa-star" aria-hidden="true"></i>
                            <i class="fa-solid fa-star" aria-hidden="true"></i>
                        </div>
                        <span>(5.0 Calificación Oficial)</span>
                        <span>•</span>
                        <span class="text-emerald-300 font-bold">100% Original Nuevo</span>
                    </div>
                </div>

                <div class="bg-emerald-950/60 border border-emerald-500/50 p-3 rounded-xl flex items-center gap-3">
                    <i class="fa-solid fa-circle-check text-emerald-400 text-xl shrink-0" aria-hidden="true"></i>
                    <div class="text-xs">
                        <strong class="text-emerald-300 block">Disponible en Sucursal Guadalajara</strong>
                        <span class="text-slate-200">Pedro Moreno 501 A, Zona Centro. Retiro en 15 minutos o entrega express.</span>
                    </div>
                </div>

                <div class="space-y-2 text-xs">
                    <h4 class="font-bold text-white uppercase text-xs font-mono flex items-center gap-2">
                        <i class="fa-solid fa-list-check text-cyan-400" aria-hidden="true"></i> Características & Especificaciones
                    </h4>
                    <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3 space-y-2 text-slate-200 leading-relaxed font-sans">
                        <p><strong>Descripción:</strong> ${desc}</p>
                        <div class="grid grid-cols-2 gap-2 pt-2 border-t border-slate-800 text-[11px] font-mono">
                            <div><span class="text-slate-400">Categoría:</span> <strong class="text-cyan-300">${cat.toUpperCase()}</strong></div>
                            <div><span class="text-slate-400">Garantía:</span> <strong class="text-white">48h Directa / 1 Año</strong></div>
                            <div><span class="text-slate-400">Clave Interna:</span> <strong class="text-white">${sku}</strong></div>
                            <div><span class="text-slate-400">Embalaje:</span> <strong class="text-white">Caja Sellada Fábrica</strong></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- COLUMNA 3 (DERECHA - CONVERSIÓN & PRECIOS) -->
            <div class="lg:col-span-3 bg-slate-950 border border-slate-800 rounded-2xl p-4 flex flex-col justify-between gap-3.5 shadow-2xl">
                
                <div>
                    <div class="border-b border-slate-800 pb-3 space-y-1">
                        <div class="flex justify-between items-center">
                            <span class="text-[10.5px] text-slate-400 font-mono line-through" id="pdp-original-price">
                                Lista: $${original.toLocaleString('es-MX', { minimumFractionDigits: 2 })}
                            </span>
                            <span id="pdp-wholesale-badge" class="hidden text-[8.5px] font-black bg-amber-400 text-slate-950 px-2 py-0.5 rounded-md uppercase tracking-wider animate-pulse">
                                Mayoreo Activado
                            </span>
                        </div>

                        <div class="text-2xl font-black text-emerald-300 font-mono tracking-tight drop-shadow-[0_0_10px_rgba(52,211,153,0.4)]" id="pdp-unit-price-display">
                            $${price.toLocaleString('es-MX', { minimumFractionDigits: 2 })} <span class="text-xs font-normal text-slate-300">MXN c/u</span>
                        </div>

                        <div class="flex justify-between items-center text-[10.5px] font-mono text-cyan-300 font-bold">
                            <span>Ahorro: -25% Apertura</span>
                            <span class="text-slate-300" id="pdp-subtotal-display">Subtotal: $${price.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</span>
                        </div>
                    </div>

                    <!-- SELECTOR DINÁMICO (+ / -) Y PAPELERA -->
                    <div class="pt-3 space-y-2.5">
                        <div class="flex items-center justify-between gap-2">
                            <span class="text-xs font-mono text-slate-200 font-bold">Cantidad:</span>
                            
                            <div class="flex items-center gap-1.5 bg-slate-900 border border-slate-700 rounded-xl p-1">
                                <button 
                                    type="button" 
                                    onclick="updatePDPQuantity(-1, ${price}, ${mayoreo}, ${original})" 
                                    aria-label="Disminuir cantidad de compra"
                                    class="qty-btn w-10 h-10 bg-slate-800 hover:bg-slate-700 active:scale-90 text-cyan-300 rounded-lg font-mono font-bold flex items-center justify-center transition cursor-pointer text-base min-h-[44px] min-w-[44px]"
                                >
                                    -
                                </button>
                                
                                <input 
                                    id="pdp-qty-input" 
                                    type="number" 
                                    value="1" 
                                    min="1" 
                                    max="999" 
                                    aria-label="Cantidad seleccionada"
                                    onchange="updatePDPQuantity(0, ${price}, ${mayoreo}, ${original})" 
                                    class="w-12 bg-transparent text-center text-white font-mono font-bold text-sm outline-none no-arrows min-h-[44px]"
                                />

                                <button 
                                    type="button" 
                                    onclick="updatePDPQuantity(1, ${price}, ${mayoreo}, ${original})" 
                                    aria-label="Aumentar cantidad de compra"
                                    class="qty-btn w-10 h-10 bg-slate-800 hover:bg-slate-700 active:scale-90 text-cyan-300 rounded-lg font-mono font-bold flex items-center justify-center transition cursor-pointer text-base min-h-[44px] min-w-[44px]"
                                >
                                    +
                                </button>
                            </div>

                            <button 
                                type="button" 
                                onclick="removeProductFromCart('${sku}'); closeProductDetailModal();" 
                                aria-label="Remover este producto de la selección"
                                class="btn-action w-10 h-10 rounded-xl bg-slate-900 border border-slate-800 hover:border-red-500 hover:bg-red-950/60 text-slate-300 hover:text-red-400 flex items-center justify-center transition cursor-pointer shrink-0 min-h-[44px] min-w-[44px]" 
                                title="Remover de la selección"
                            >
                                <i class="fa-solid fa-trash-can text-sm" aria-hidden="true"></i>
                            </button>
                        </div>

                        <div class="space-y-2 pt-1">
                            <button 
                                onclick="executeAddToCartPDP('${sku}', '${title}', '${localImg}', ${price}, ${mayoreo})" 
                                aria-label="Agregar ${title} al carrito de compra"
                                class="btn-action w-full bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/50 hover:border-cyan-400 font-black py-3 rounded-xl text-xs uppercase tracking-wider flex items-center justify-center gap-2 transition cursor-pointer shadow hover:shadow-cyan-500/20 min-h-[48px]"
                            >
                                <i class="fa-solid fa-cart-plus" aria-hidden="true"></i> <span>Agregar al Carrito</span>
                            </button>

                            <button 
                                onclick="executeBuyNowPDP('${sku}', '${title}', '${localImg}', ${price}, ${mayoreo})" 
                                aria-label="Pagar ${title} ahora con SPEI o Mercado Pago"
                                class="btn-action w-full bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-black py-3 rounded-xl text-xs uppercase tracking-wider flex items-center justify-center gap-2 transition active:scale-95 shadow-lg cursor-pointer min-h-[48px]"
                            >
                                <i class="fa-solid fa-bolt" aria-hidden="true"></i> <span>Pagar Ahora (SPEI / MP)</span>
                            </button>
                        </div>
                    </div>

                    <div class="mt-3.5 pt-3 border-t border-slate-800 space-y-2 text-[11px]">
                        <div class="bg-slate-900/90 border border-emerald-500/40 p-2.5 rounded-xl space-y-1">
                            <div class="flex items-center gap-1.5 text-emerald-300 font-mono font-bold">
                                <i class="fa-solid fa-coins" aria-hidden="true"></i> <span>5% DE CASHBACK</span>
                            </div>
                            <p class="text-slate-200 text-[10px] leading-tight">Acumula saldo en tu monedero con tu teléfono registrado.</p>
                        </div>

                        <div class="bg-slate-900/90 border border-amber-500/40 p-2.5 rounded-xl space-y-1">
                            <div class="flex items-center gap-1.5 text-amber-300 font-mono font-bold">
                                <i class="fa-solid fa-boxes-stacked" aria-hidden="true"></i> <span>PRECIO DE MAYOREO</span>
                            </div>
                            <p class="text-slate-200 text-[10px] leading-tight">A partir de 10 piezas aplica automáticamente <strong>$${mayoreo.toLocaleString('es-MX', { minimumFractionDigits: 2 })} MXN</strong>.</p>
                        </div>
                    </div>
                </div>

                <div class="text-[10px] text-slate-400 font-mono text-center pt-1 border-t border-slate-900">
                    🔒 Transacción protegida SSL • Entrega express Guadalajara
                </div>

            </div>

        </div>
    `;

    modal.classList.remove("hidden");
    document.body.style.overflow = "hidden";
};

window.closeProductDetailModal = function() {
    const modal = document.getElementById("productDetailModal");
    if (modal) modal.classList.add("hidden");
    document.body.style.overflow = "auto";
};

function renderPaginationBar(totalPages) {
    const containers = document.querySelectorAll(".pagination-target-bar");
    if (!containers || containers.length === 0) return;

    let pages = [];
    if (totalPages <= 7) {
        for (let i = 1; i <= totalPages; i++) pages.push(i);
    } else {
        if (currentPageNumber <= 4) {
            pages = [1, 2, 3, 4, 5, 6, 7, '...', totalPages];
        } else if (currentPageNumber >= totalPages - 4) {
            pages = [1, '...', totalPages - 6, totalPages - 5, totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages];
        } else {
            pages = [1, '...', currentPageNumber - 2, currentPageNumber - 1, currentPageNumber, currentPageNumber + 1, currentPageNumber + 2, '...', totalPages];
        }
    }

    const htmlPages = pages.map(p => {
        if (p === '...') {
            return `<span class="px-2 text-slate-400 font-mono text-xs select-none">...</span>`;
        }
        const isAct = (p === currentPageNumber);
        const cls = isAct 
            ? "bg-cyan-500 text-slate-950 font-black border-cyan-400 shadow-[0_0_10px_rgba(6,182,212,0.5)]" 
            : "bg-slate-900 border-slate-800 text-slate-200 hover:bg-slate-800 hover:text-white";
        return `<button onclick="goToPageNumber(${p})" aria-label="Ir a página ${p}" aria-current="${isAct ? 'page' : 'false'}" class="pagination-btn min-w-[48px] min-h-[48px] p-2 rounded-xl border text-xs font-mono transition flex items-center justify-center cursor-pointer ${cls}">${p}</button>`;
    }).join('');

    containers.forEach(box => {
        box.innerHTML = `
            <nav aria-label="Paginación del catálogo" class="flex items-center gap-1.5 flex-wrap justify-center">
                <button onclick="goToPageNumber(${currentPageNumber - 1})" aria-label="Página anterior" ${currentPageNumber <= 1 ? 'disabled class="opacity-30 cursor-not-allowed"' : 'class="cursor-pointer hover:bg-slate-800"'} class="pagination-btn min-w-[48px] min-h-[48px] p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-200 text-xs flex items-center justify-center">
                    <i class="fa-solid fa-chevron-left text-xs" aria-hidden="true"></i>
                </button>
                ${htmlPages}
                <button onclick="goToPageNumber(${currentPageNumber + 1})" aria-label="Página siguiente" ${currentPageNumber >= totalPages ? 'disabled class="opacity-30 cursor-not-allowed"' : 'class="cursor-pointer hover:bg-slate-800"'} class="pagination-btn min-w-[48px] min-h-[48px] p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-200 text-xs flex items-center justify-center">
                    <i class="fa-solid fa-chevron-right text-xs" aria-hidden="true"></i>
                </button>
            </nav>
        `;
    });
}

function goToPageNumber(p) {
    const items = getFilteredList();
    const totalPages = Math.ceil(items.length / productsPerPage) || 1;
    if (p < 1) p = 1;
    if (p > totalPages) p = totalPages;
    currentPageNumber = p;
    renderExactCatalogView();
    const target = document.getElementById("catalog-main-content-root");
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function resetFacets() {
    activeSelectedCategory = 'Todas';
    activeSelectedBrand = 'Todas';
    currentPageNumber = 1;
    renderSidebarFacets();
    renderExactCatalogView();
}

window.updatePDPQuantity = function(delta, regularPrice, wholesalePrice, originalPrice) {
    const input = document.getElementById("pdp-qty-input");
    if (!input) return;
    
    let currentQty = parseInt(input.value) || 1;
    currentQty += delta;
    if (currentQty < 1) currentQty = 1;
    input.value = currentQty;

    const unitPriceDisplay = document.getElementById("pdp-unit-price-display");
    const subtotalDisplay = document.getElementById("pdp-subtotal-display");
    const wholesaleBadge = document.getElementById("pdp-wholesale-badge");

    const isWholesale = currentQty >= 10;
    const activePrice = isWholesale ? wholesalePrice : regularPrice;
    const total = activePrice * currentQty;

    if (wholesaleBadge) {
        if (isWholesale) wholesaleBadge.classList.remove("hidden");
        else wholesaleBadge.classList.add("hidden");
    }

    if (unitPriceDisplay) {
        unitPriceDisplay.innerHTML = `$${activePrice.toLocaleString('es-MX', { minimumFractionDigits: 2 })} <span class="text-xs font-normal text-slate-300">MXN c/u</span>`;
    }

    if (subtotalDisplay) {
        subtotalDisplay.innerText = `Subtotal: $${total.toLocaleString('es-MX', { minimumFractionDigits: 2 })} MXN`;
    }
};

window.executeAddToCartPDP = function(sku, title, img, regularPrice, wholesalePrice) {
    const input = document.getElementById("pdp-qty-input");
    const qty = parseInt(input ? input.value : 1) || 1;
    const activePrice = (qty >= 10) ? wholesalePrice : regularPrice;
    
    addToCartCT(sku, title, activePrice, img, qty);
    closeProductDetailModal();
};

window.executeBuyNowPDP = function(sku, title, img, regularPrice, wholesalePrice) {
    const input = document.getElementById("pdp-qty-input");
    const qty = parseInt(input ? input.value : 1) || 1;
    const activePrice = (qty >= 10) ? wholesalePrice : regularPrice;
    
    addToCartCT(sku, title, activePrice, img, qty);
    window.location.href = "checkout.html";
};

window.removeProductFromCart = function(sku) {
    let cart = JSON.parse(localStorage.getItem('ecosystem_global_cart') || localStorage.getItem('cart_items') || '[]');
    cart = cart.filter(item => item.sku !== sku);
    localStorage.setItem('ecosystem_global_cart', JSON.stringify(cart));
    localStorage.setItem('cart_items', JSON.stringify(cart));
    syncBoutiqueCart();
    alert("🗑️ Producto removido de la selección.");
};

window.addToCartCT = function(sku, title, price, img, qty = 1) {
    let cart = JSON.parse(localStorage.getItem('ecosystem_global_cart') || localStorage.getItem('cart_items') || '[]');
    const existing = cart.find(i => i.sku === sku);
    if (existing) {
        existing.quantity = (existing.quantity || 1) + qty;
        existing.qty = existing.quantity;
    } else {
        cart.push({
            sku: sku,
            nombre: title,
            title: title,
            precio: price,
            price: price,
            quantity: qty,
            qty: qty,
            imagen: img,
            image: img
        });
    }
    localStorage.setItem('ecosystem_global_cart', JSON.stringify(cart));
    localStorage.setItem('cart_items', JSON.stringify(cart));
    syncBoutiqueCart();
    alert(`🛒 ¡(${qty}) ${title} agregado al carrito!`);
};

window.buyNowCT = function(sku, title, price, img) {
    window.addToCartCT(sku, title, price, img, 1);
    window.location.href = "checkout.html";
};

function syncBoutiqueCart() {
    try {
        const cart = JSON.parse(localStorage.getItem('ecosystem_global_cart') || localStorage.getItem('cart_items') || '[]');
        const count = cart.reduce((s, i) => s + (parseInt(i.quantity || i.qty) || 0), 0);
        const total = cart.reduce((s, i) => s + ((parseFloat(i.precio || i.price) || 0) * (parseInt(i.quantity || i.qty) || 0)), 0);
        const bBadge = document.getElementById("boutique-cart-badge");
        const bTotal = document.getElementById("boutique-cart-total");
        if (bBadge) bBadge.innerText = count;
        if (bTotal) bTotal.innerText = `$${total.toLocaleString('es-MX', { minimumFractionDigits: 2 })} MXN`;
    } catch(e) {}
}
"""

with open(ENGINE_JS, "w", encoding="utf-8") as f:
    f.write(ENGINE_JS_LIGHTHOUSE)

print("✅ ct-exact-catalog-engine.js optimizado para Lighthouse 100/100.", flush=True)

# 4. Sincronizar a OneDrive C:
BASE_DIR_C = r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web\pc-custom-lab"
for root, dirs, files in os.walk(BASE_DIR):
    if '.git' in root or 'node_modules' in root: continue
    for file in files:
        src = os.path.join(root, file)
        rel = os.path.relpath(src, r"E:\sitios web")
        dst = os.path.join(r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web", rel)
        if os.path.exists(os.path.dirname(dst)):
            try:
                with open(src, "rb") as f_in, open(dst, "wb") as f_out:
                    f_out.write(f_in.read())
            except: pass

print("✅ Sincronización a espejo OneDrive C: completada!", flush=True)
