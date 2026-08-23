import os
import subprocess

BASE_DIR = r"E:\sitios web"
portal_paths = [
    os.path.join(BASE_DIR, "index.html"),
    os.path.join(BASE_DIR, "sitios-web", "index.html")
]

print("=" * 75)
print("REESTRUCTURANDO ECOSISTEMA MATRIZ: SEARCH-FIRST + DIRECTORIO DINÁMICO")
print("=" * 75)

PORTAL_REESTRUCTURADO_HTML = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Ecosistema Comercial Pedro Moreno 501 A | Portal Matriz 2026</title>
    <meta name="description" content="Hub central del ecosistema comercial multi-boutique: Hardware de PC, Vía MX Curaduría, Tabacos, Dulcería, Kiosco Digital, Bazar y Liquidaciones con Carrito Global Unificado." />
    <meta name="google-site-verification" content="2xIPYIU_imoZjFogZhoFRuepS7PFhXQloOamPV7ex6Q" />
    
    <!-- Open Graph -->
    <meta property="og:type" content="website" />
    <meta property="og:title" content="Ecosistema Comercial Pedro Moreno 501 A | 7 Boutiques Especializadas" />
    <meta property="og:description" content="7 boutiques especializadas en un solo lugar con Carrito Global, 5% de Cashback y Envíos Gratis desde $1,500 MXN." />
    <meta property="og:url" content="https://iaworldcenter-creator.github.io/sitios-web/" />

    <!-- Tailwind CSS y FontAwesome -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />

    <style>
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen flex flex-col justify-between overflow-x-hidden selection:bg-cyan-500 selection:text-slate-950">

    <!-- TOP BAR DE NAVEGACIÓN CRUZADA CON ACCESO RECARGABLE -->
    <header class="bg-slate-900 border-b border-slate-800 sticky top-0 z-50 shadow-xl">
        <div class="max-w-7xl mx-auto px-4 py-2.5 flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-3 cursor-pointer" onclick="window.location.reload();">
                <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-amber-500 to-amber-300 flex items-center justify-center text-slate-950 font-black shadow-md shadow-amber-500/20">
                    <i class="fa-solid fa-cubes text-base"></i>
                </div>
                <div>
                    <span class="font-black text-base text-white tracking-wider block leading-tight">ECOSISTEMA MATRIZ</span>
                    <span class="text-[10px] font-mono text-cyan-400 uppercase tracking-widest block">Pedro Moreno 501 A &bull; GDL Centro</span>
                </div>
            </div>

            <!-- Accesos directos a las 7 Boutiques -->
            <nav class="hidden xl:flex items-center gap-1 text-[11px] font-bold text-slate-300">
                <a href="https://iaworldcenter-creator.github.io/sitios-web/" onclick="if(window.location.pathname.includes('sitios-web')){ event.preventDefault(); window.location.reload(); }" class="px-2.5 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400 hover:bg-amber-500 hover:text-slate-950 transition flex items-center gap-1"><i class="fa-solid fa-house text-[10px]"></i> Portal Matriz</a>
                <a href="https://iaworldcenter-creator.github.io/pc-custom-lab/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-cyan-400 transition">PC Custom</a>
                <a href="https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-cyan-300 transition flex items-center gap-1"><i class="fa-solid fa-gem text-[10px] text-cyan-400"></i> Vía MX</a>
                <a href="https://iaworldcenter-creator.github.io/cigarros-bazar/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-amber-400 transition">Cigarros</a>
                <a href="https://iaworldcenter-creator.github.io/dulces-bazar/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-pink-400 transition">Dulces</a>
                <a href="https://iaworldcenter-creator.github.io/kiosco-digital/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-indigo-400 transition">Kiosco</a>
                <a href="https://iaworldcenter-creator.github.io/mi-puesto-bazar/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-emerald-400 transition">Mi Puesto</a>
                <a href="https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-red-400 transition">Liquidaciones</a>
            </nav>

            <!-- Acceso a Carrito Global & Gemini -->
            <div class="flex items-center gap-2.5">
                <a href="https://gemini.google.com" target="_blank" rel="noopener noreferrer" class="px-3 py-1.5 bg-slate-800/80 hover:bg-slate-800 border border-slate-700/80 rounded-xl text-[11px] font-bold text-cyan-300 transition flex items-center gap-1.5 shadow-sm">
                    <i class="fa-solid fa-wand-magic-sparkles text-cyan-400"></i> Gemini AI
                </a>
                <a href="https://iaworldcenter-creator.github.io/pc-custom-lab/checkout.html" class="px-3.5 py-1.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-black rounded-xl text-[11px] uppercase tracking-wider transition flex items-center gap-1.5 shadow-md shadow-amber-500/20 active:scale-95">
                    <i class="fa-solid fa-cart-shopping"></i> Carrito Global <span id="portal-cart-badge" class="bg-slate-950 text-white font-mono px-1.5 py-0.2 rounded-full text-[10px] ml-0.5">0</span>
                </a>
            </div>
        </div>
    </header>

    <!-- HERO CENTRAL CON SÚPER-BARRA SEARCH-FIRST INMEDIATA -->
    <section class="relative py-10 px-4 border-b border-slate-800/80 bg-gradient-to-b from-slate-900/60 via-slate-950 to-slate-950">
        <div class="max-w-4xl mx-auto text-center flex flex-col items-center gap-4">
            <span class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-mono font-bold uppercase tracking-wider">
                <i class="fa-solid fa-shield-halved"></i> Hub Matriz 2026
            </span>
            <h1 class="text-3xl sm:text-4xl font-black text-white tracking-tight leading-tight">
                7 Boutiques Especializadas.<br /><span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-amber-200 to-cyan-400">Un Solo Carrito Global y Envíos Consolidados.</span>
            </h1>

            <!-- SÚPER-BARRA BLANCA SEARCH-FIRST EN EL PORTAL MATRIZ -->
            <div class="w-full max-w-2xl mt-2 relative">
                <div class="flex items-center bg-white rounded-full border-2 border-cyan-400 shadow-[0_0_22px_rgba(6,182,212,0.4)] px-4 py-2 gap-2">
                    <i class="fa-solid fa-magnifying-glass text-slate-400 text-sm"></i>
                    <input 
                        type="text" 
                        id="portalSearchInput" 
                        placeholder="Busca en todo el ecosistema (ej. 'RTX', 'Puros', 'Paletas', 'Revistas', 'Ofertas')..." 
                        class="flex-1 bg-transparent border-0 outline-none text-slate-950 font-bold text-sm placeholder-slate-400 selection:bg-cyan-500 selection:text-white"
                        oninput="onPortalSearch(event)"
                    />
                </div>
            </div>
        </div>
    </section>

    <!-- CUERPO PRINCIPAL: SIDEBAR DE TIENDAS + CATÁLOGO CENTRAL DE BOUTIQUES -->
    <main class="max-w-7xl mx-auto px-4 py-8 flex-1 w-full">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            
            <!-- COLUMNA IZQUIERDA: LISTADO DE LAS 7 BOUTIQUES -->
            <aside class="lg:col-span-4 w-full bg-slate-900/90 border border-slate-800 rounded-3xl p-4 shadow-xl">
                <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
                    <h3 class="font-mono text-xs font-black text-white uppercase tracking-wider flex items-center gap-2">
                        <i class="fa-solid fa-store text-amber-400"></i> Directorio de Boutiques
                    </h3>
                    <span class="text-[9px] font-mono text-cyan-400 font-bold bg-cyan-950/40 border border-cyan-500/30 px-2 py-0.5 rounded">7 Tiendas</span>
                </div>

                <nav class="flex flex-col gap-1.5" id="sidebar-boutiques-nav">
                    <a href="https://iaworldcenter-creator.github.io/pc-custom-lab/" class="p-3 rounded-2xl bg-slate-950/60 hover:bg-slate-800 border border-slate-800/80 hover:border-cyan-500/50 flex justify-between items-center transition group">
                        <div class="flex items-center gap-3">
                            <i class="fa-solid fa-microchip text-cyan-400 w-5 text-center text-base"></i>
                            <div>
                                <strong class="text-white text-xs block group-hover:text-cyan-300">PC Custom Lab</strong>
                                <span class="text-[10px] text-slate-400">Hardware, GPUs & Ensambles IA</span>
                            </div>
                        </div>
                        <i class="fa-solid fa-chevron-right text-[10px] text-slate-600 group-hover:text-cyan-400"></i>
                    </a>

                    <a href="https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/" class="p-3 rounded-2xl bg-slate-950/60 hover:bg-slate-800 border border-slate-800/80 hover:border-cyan-500/50 flex justify-between items-center transition group">
                        <div class="flex items-center gap-3">
                            <i class="fa-solid fa-gem text-cyan-400 w-5 text-center text-base"></i>
                            <div>
                                <strong class="text-white text-xs block group-hover:text-cyan-300">Vía MX Curaduría</strong>
                                <span class="text-[10px] text-slate-400">30 Deptos, Electrónica & B2B</span>
                            </div>
                        </div>
                        <i class="fa-solid fa-chevron-right text-[10px] text-slate-600 group-hover:text-cyan-400"></i>
                    </a>

                    <a href="https://iaworldcenter-creator.github.io/cigarros-bazar/" class="p-3 rounded-2xl bg-slate-950/60 hover:bg-slate-800 border border-slate-800/80 hover:border-amber-500/50 flex justify-between items-center transition group">
                        <div class="flex items-center gap-3">
                            <i class="fa-solid fa-smoking text-amber-400 w-5 text-center text-base"></i>
                            <div>
                                <strong class="text-white text-xs block group-hover:text-amber-300">Cigarros Bazar</strong>
                                <span class="text-[10px] text-slate-400">Puros Habanos & Tabaco Selecto</span>
                            </div>
                        </div>
                        <i class="fa-solid fa-chevron-right text-[10px] text-slate-600 group-hover:text-amber-400"></i>
                    </a>

                    <a href="https://iaworldcenter-creator.github.io/dulces-bazar/" class="p-3 rounded-2xl bg-slate-950/60 hover:bg-slate-800 border border-slate-800/80 hover:border-pink-500/50 flex justify-between items-center transition group">
                        <div class="flex items-center gap-3">
                            <i class="fa-solid fa-candy-cane text-pink-400 w-5 text-center text-base"></i>
                            <div>
                                <strong class="text-white text-xs block group-hover:text-pink-300">Dulces Bazar</strong>
                                <span class="text-[10px] text-slate-400">Paletas, Botanas & Confitería</span>
                            </div>
                        </div>
                        <i class="fa-solid fa-chevron-right text-[10px] text-slate-600 group-hover:text-pink-400"></i>
                    </a>

                    <a href="https://iaworldcenter-creator.github.io/kiosco-digital/" class="p-3 rounded-2xl bg-slate-950/60 hover:bg-slate-800 border border-slate-800/80 hover:border-indigo-500/50 flex justify-between items-center transition group">
                        <div class="flex items-center gap-3">
                            <i class="fa-solid fa-newspaper text-indigo-400 w-5 text-center text-base"></i>
                            <div>
                                <strong class="text-white text-xs block group-hover:text-indigo-300">Kiosco Digital</strong>
                                <span class="text-[10px] text-slate-400">Revistas, Periódicos & Lectura</span>
                            </div>
                        </div>
                        <i class="fa-solid fa-chevron-right text-[10px] text-slate-600 group-hover:text-indigo-400"></i>
                    </a>

                    <a href="https://iaworldcenter-creator.github.io/mi-puesto-bazar/" class="p-3 rounded-2xl bg-slate-950/60 hover:bg-slate-800 border border-slate-800/80 hover:border-emerald-500/50 flex justify-between items-center transition group">
                        <div class="flex items-center gap-3">
                            <i class="fa-solid fa-store text-emerald-400 w-5 text-center text-base"></i>
                            <div>
                                <strong class="text-white text-xs block group-hover:text-emerald-300">Mi Puesto Bazar</strong>
                                <span class="text-[10px] text-slate-400">Novedades & Tienda Matriz</span>
                            </div>
                        </div>
                        <i class="fa-solid fa-chevron-right text-[10px] text-slate-600 group-hover:text-emerald-400"></i>
                    </a>

                    <a href="https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/" class="p-3 rounded-2xl bg-slate-950/60 hover:bg-slate-800 border border-slate-800/80 hover:border-red-500/50 flex justify-between items-center transition group">
                        <div class="flex items-center gap-3">
                            <i class="fa-solid fa-tags text-red-400 w-5 text-center text-base"></i>
                            <div>
                                <strong class="text-white text-xs block group-hover:text-red-300">Ofertas & Liquidaciones</strong>
                                <span class="text-[10px] text-slate-400">Remates hasta 50% de Descuento</span>
                            </div>
                        </div>
                        <i class="fa-solid fa-chevron-right text-[10px] text-slate-600 group-hover:text-red-400"></i>
                    </a>
                </nav>
            </aside>

            <!-- COLUMNA DERECHA: TARJETAS DE LAS BOUTIQUES / RESULTADOS -->
            <section class="lg:col-span-8 w-full flex flex-col gap-4">
                <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                    <span class="text-xs font-mono text-cyan-400 font-bold uppercase tracking-wider" id="portal-status-txt">
                        Departamentos y Tiendas Especializadas
                    </span>
                    <span class="text-xs font-mono text-slate-400">Pedro Moreno 501 A</span>
                </div>

                <div id="portal-cards-grid" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <!-- Tarjeta 1: PC Custom -->
                    <div class="bg-slate-900/80 border border-slate-800 hover:border-cyan-500/60 rounded-2xl p-5 flex flex-col justify-between shadow-xl transition group">
                        <div class="flex flex-col gap-2.5">
                            <div class="flex justify-between items-center">
                                <span class="text-[10px] font-mono font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 px-2 py-0.5 rounded">TECNOLOGÍA</span>
                                <i class="fa-solid fa-microchip text-cyan-400 text-lg"></i>
                            </div>
                            <h4 class="text-base font-bold text-white group-hover:text-cyan-300 transition">PC Custom Lab</h4>
                            <p class="text-xs text-slate-400 leading-relaxed">Ensambles de alto rendimiento, GPUs NVIDIA RTX, procesadores Ryzen y refacciones para gaming e IA.</p>
                        </div>
                        <a href="https://iaworldcenter-creator.github.io/pc-custom-lab/" class="mt-4 w-full bg-slate-800 hover:bg-cyan-500 hover:text-slate-950 text-white font-bold py-2 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2">
                            Entrar a Boutique &rarr;
                        </a>
                    </div>

                    <!-- Tarjeta 2: Vía MX Curaduría -->
                    <div class="bg-slate-900/80 border border-cyan-500/40 hover:border-cyan-400 rounded-2xl p-5 flex flex-col justify-between shadow-xl shadow-cyan-950/20 transition group">
                        <div class="flex flex-col gap-2.5">
                            <div class="flex justify-between items-center">
                                <span class="text-[10px] font-mono font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 px-2 py-0.5 rounded">CURADURÍA B2B</span>
                                <i class="fa-solid fa-gem text-cyan-400 text-lg"></i>
                            </div>
                            <h4 class="text-base font-bold text-white group-hover:text-cyan-300 transition">Vía MX Curaduría</h4>
                            <p class="text-xs text-slate-400 leading-relaxed">200 productos de alta rotación en 30 departamentos: electrónica, electrodomésticos, herramientas y smart home.</p>
                        </div>
                        <a href="https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/" class="mt-4 w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-black py-2 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2 shadow-md shadow-cyan-500/20">
                            Entrar a Boutique &rarr;
                        </a>
                    </div>

                    <!-- Tarjeta 3: Cigarros -->
                    <div class="bg-slate-900/80 border border-slate-800 hover:border-amber-500/60 rounded-2xl p-5 flex flex-col justify-between shadow-xl transition group">
                        <div class="flex flex-col gap-2.5">
                            <div class="flex justify-between items-center">
                                <span class="text-[10px] font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30 px-2 py-0.5 rounded">TABACOS</span>
                                <i class="fa-solid fa-smoking text-amber-400 text-lg"></i>
                            </div>
                            <h4 class="text-base font-bold text-white group-hover:text-amber-300 transition">Cigarros Bazar</h4>
                            <p class="text-xs text-slate-400 leading-relaxed">Puros habanos de importación, tabaco para liar, encendedores especiales y cortapuros de titanio.</p>
                        </div>
                        <a href="https://iaworldcenter-creator.github.io/cigarros-bazar/" class="mt-4 w-full bg-slate-800 hover:bg-amber-500 hover:text-slate-950 text-white font-bold py-2 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2">
                            Entrar a Boutique &rarr;
                        </a>
                    </div>

                    <!-- Tarjeta 4: Dulces -->
                    <div class="bg-slate-900/80 border border-slate-800 hover:border-pink-500/60 rounded-2xl p-5 flex flex-col justify-between shadow-xl transition group">
                        <div class="flex flex-col gap-2.5">
                            <div class="flex justify-between items-center">
                                <span class="text-[10px] font-mono font-bold bg-pink-500/10 text-pink-400 border border-pink-500/30 px-2 py-0.5 rounded">DULCERÍA</span>
                                <i class="fa-solid fa-candy-cane text-pink-400 text-lg"></i>
                            </div>
                            <h4 class="text-base font-bold text-white group-hover:text-pink-300 transition">Dulces Bazar</h4>
                            <p class="text-xs text-slate-400 leading-relaxed">Paletas tradicionales, mazapanes, botanas saladas y confitería mexicana al mayoreo y menudeo.</p>
                        </div>
                        <a href="https://iaworldcenter-creator.github.io/dulces-bazar/" class="mt-4 w-full bg-slate-800 hover:bg-pink-500 hover:text-white text-white font-bold py-2 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2">
                            Entrar a Boutique &rarr;
                        </a>
                    </div>

                    <!-- Tarjeta 5: Kiosco -->
                    <div class="bg-slate-900/80 border border-slate-800 hover:border-indigo-500/60 rounded-2xl p-5 flex flex-col justify-between shadow-xl transition group">
                        <div class="flex flex-col gap-2.5">
                            <div class="flex justify-between items-center">
                                <span class="text-[10px] font-mono font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 px-2 py-0.5 rounded">LECTURA</span>
                                <i class="fa-solid fa-newspaper text-indigo-400 text-lg"></i>
                            </div>
                            <h4 class="text-base font-bold text-white group-hover:text-indigo-300 transition">Kiosco Digital</h4>
                            <p class="text-xs text-slate-400 leading-relaxed">Suscripciones digitales a revistas de ciencia, tecnología, cómics y periódicos con entrega local.</p>
                        </div>
                        <a href="https://iaworldcenter-creator.github.io/kiosco-digital/" class="mt-4 w-full bg-slate-800 hover:bg-indigo-500 hover:text-white text-white font-bold py-2 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2">
                            Entrar a Boutique &rarr;
                        </a>
                    </div>

                    <!-- Tarjeta 6: Mi Puesto -->
                    <div class="bg-slate-900/80 border border-slate-800 hover:border-emerald-500/60 rounded-2xl p-5 flex flex-col justify-between shadow-xl transition group">
                        <div class="flex flex-col gap-2.5">
                            <div class="flex justify-between items-center">
                                <span class="text-[10px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded">MATRIZ</span>
                                <i class="fa-solid fa-store text-emerald-400 text-lg"></i>
                            </div>
                            <h4 class="text-base font-bold text-white group-hover:text-emerald-300 transition">Mi Puesto Bazar</h4>
                            <p class="text-xs text-slate-400 leading-relaxed">Novedades, artículos de conveniencia diaria, papelería y consumibles de paso en Guadalajara Centro.</p>
                        </div>
                        <a href="https://iaworldcenter-creator.github.io/mi-puesto-bazar/" class="mt-4 w-full bg-slate-800 hover:bg-emerald-500 hover:text-slate-950 text-white font-bold py-2 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2">
                            Entrar a Boutique &rarr;
                        </a>
                    </div>

                    <!-- Tarjeta 7: Ofertas -->
                    <div class="bg-slate-900/80 border border-slate-800 hover:border-red-500/60 rounded-2xl p-5 flex flex-col justify-between shadow-xl transition group sm:col-span-2">
                        <div class="flex flex-col gap-2.5">
                            <div class="flex justify-between items-center">
                                <span class="text-[10px] font-mono font-bold bg-red-500/10 text-red-400 border border-red-500/30 px-2 py-0.5 rounded">OUTLET DIRECTO</span>
                                <i class="fa-solid fa-tags text-red-400 text-lg"></i>
                            </div>
                            <h4 class="text-base font-bold text-white group-hover:text-red-300 transition">Liquidaciones y Ofertas</h4>
                            <p class="text-xs text-slate-400 leading-relaxed">Excedentes de almacén y piezas únicas de liquidación con descuentos de hasta el 50% y entrega inmediata.</p>
                        </div>
                        <a href="https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/" class="mt-4 w-full bg-slate-800 hover:bg-red-500 hover:text-white text-white font-bold py-2 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2">
                            Entrar a Boutique &rarr;
                        </a>
                    </div>
                </div>
            </section>

        </div>
    </main>

    <!-- ========================================================================
         LOS 3 PILARES MOVIDOS AL FONDO (JUSTO ANTES DEL FOOTER)
         ======================================================================== -->
    <section class="max-w-7xl mx-auto px-4 py-8 w-full border-t border-slate-800/80">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="p-4 bg-slate-900/60 border border-slate-800 rounded-2xl flex items-center gap-3.5">
                <div class="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 text-lg shrink-0">
                    <i class="fa-solid fa-truck-fast"></i>
                </div>
                <div>
                    <strong class="text-white text-xs block font-bold">Envío Gratis Local</strong>
                    <span class="text-slate-400 text-[11px]">En compras consolidadas desde $1,500 MXN</span>
                </div>
            </div>

            <div class="p-4 bg-slate-900/60 border border-slate-800 rounded-2xl flex items-center gap-3.5">
                <div class="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 text-lg shrink-0">
                    <i class="fa-solid fa-percent"></i>
                </div>
                <div>
                    <strong class="text-white text-xs block font-bold">15% Mayoreo B2B</strong>
                    <span class="text-slate-400 text-[11px]">Descuento directo al llevar 10 o más piezas</span>
                </div>
            </div>

            <div class="p-4 bg-slate-900/60 border border-slate-800 rounded-2xl flex items-center gap-3.5">
                <div class="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 text-lg shrink-0">
                    <i class="fa-solid fa-coins"></i>
                </div>
                <div>
                    <strong class="text-white text-xs block font-bold">5% Cashback</strong>
                    <span class="text-slate-400 text-[11px]">Acumulable con tu registro activo</span>
                </div>
            </div>
        </div>
    </section>

    <!-- FOOTER UNIVERSAL (3 COLUMNAS) -->
    <footer class="bg-slate-950 border-t border-slate-900 pt-16 pb-8 text-slate-400 text-xs">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 pb-12 border-b border-slate-800/80">
                
                <!-- COLUMNA 1: CONTACTO LOCAL -->
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-location-dot text-amber-400"></i> Contacto Local
                    </h4>
                    <p class="flex items-start gap-2 text-slate-300">
                        <i class="fa-solid fa-map-pin text-slate-500 mt-0.5 shrink-0"></i>
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
                    
                    <div class="flex flex-col gap-1.5 pt-2 border-t border-slate-900 text-[11px] text-slate-400">
                        <a href="https://www.facebook.com/profile.php?id=61593020515115" target="_blank" rel="noopener" class="hover:text-blue-400 transition flex items-center gap-2">
                            <i class="fa-brands fa-facebook text-blue-500 w-4 text-center"></i> Facebook: Ecosistema Pedro Moreno
                        </a>
                        <a href="https://www.instagram.com/pccustomlab/" target="_blank" rel="noopener" class="hover:text-pink-400 transition flex items-center gap-2">
                            <i class="fa-brands fa-instagram text-pink-500 w-4 text-center"></i> Instagram: @pccustomlab
                        </a>
                        <a href="https://www.youtube.com/@IAWorldCenter" target="_blank" rel="noopener" class="hover:text-red-400 transition flex items-center gap-2">
                            <i class="fa-brands fa-youtube text-red-500 w-4 text-center"></i> YouTube: IA World Center
                        </a>
                        <a href="https://t.me/pc_custom_lab" target="_blank" rel="noopener" class="hover:text-cyan-400 transition flex items-center gap-2">
                            <i class="fa-brands fa-telegram text-cyan-400 w-4 text-center"></i> Telegram: pc_custom_lab
                        </a>
                        <a href="mailto:iaworldcenter@gmail.com" class="hover:text-amber-400 transition flex items-center gap-2">
                            <i class="fa-solid fa-envelope text-amber-400 w-4 text-center"></i> Correo: iaworldcenter@gmail.com
                        </a>
                    </div>
                </div>

                <!-- COLUMNA 2: POLÍTICAS DE COMPRA -->
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-shield-halved text-cyan-400"></i> Políticas de Compra
                    </h4>
                    <div class="flex items-start gap-2.5">
                        <i class="fa-solid fa-rotate-left text-amber-400 mt-1 shrink-0"></i>
                        <div>
                            <strong class="text-slate-200 block text-xs">Devoluciones Directas:</strong>
                            <span class="text-slate-400 text-[11px] leading-relaxed">Permitidas físicamente en tienda dentro de las primeras 48 horas con empaque íntegro.</span>
                        </div>
                    </div>
                    <div class="flex items-start gap-2.5">
                        <i class="fa-solid fa-certificate text-emerald-400 mt-1 shrink-0"></i>
                        <div>
                            <strong class="text-slate-200 block text-xs">Garantía Certificada:</strong>
                            <span class="text-slate-400 text-[11px] leading-relaxed">Productos de calidad garantizada con soporte técnico local y reemplazo inmediato.</span>
                        </div>
                    </div>
                    <div class="flex items-start gap-2.5">
                        <i class="fa-solid fa-cookie-bite text-slate-500 mt-1 shrink-0"></i>
                        <div>
                            <strong class="text-slate-200 block text-xs">Políticas de Cookies:</strong>
                            <span class="text-slate-400 text-[11px] leading-relaxed">Usadas exclusivamente para mantener activa la sesión de tu carrito global y mejorar el servicio.</span>
                        </div>
                    </div>
                </div>

                <!-- COLUMNA 3: AHORRO Y CASHBACK -->
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-coins text-emerald-400"></i> Ahorro y Cashback
                    </h4>
                    <p class="text-slate-300 font-bold flex items-center gap-2">
                        <i class="fa-solid fa-piggy-bank text-amber-400 text-base shrink-0"></i>
                        <span>5% de Cashback en cada compra de forma directa.</span>
                    </p>
                    <p class="text-[11px] text-slate-400 leading-relaxed bg-slate-900/60 p-3 rounded-xl border border-slate-800/80">
                        <strong class="text-slate-300 block mb-1">Aclaración Importante:</strong>
                        El cashback es acumulable únicamente con registro activo. Regístrate en nuestro portal para recibir beneficios acumulados y ofertas exclusivas.
                    </p>
                    <div class="pt-2 text-[10px] font-mono text-slate-500 flex items-center gap-2">
                        <i class="fa-solid fa-robot text-cyan-400"></i>
                        <span>Potenciado por la tecnología de Anti-Gravity Copilot.</span>
                    </div>
                </div>

            </div>

            <div class="pt-8 text-center text-slate-500 text-[11px]">
                <p>&copy; 2026 Ecosistema Comercial Pedro Moreno 501 A. Guadalajara Centro. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>

    <!-- SCRIPT DE BÚSQUEDA Y BADGE DEL PORTAL -->
    <script>
    function onPortalSearch(e) {
        const q = e.target.value.toLowerCase().trim();
        const cards = document.querySelectorAll("#portal-cards-grid > div");
        const statusTxt = document.getElementById("portal-status-txt");
        let matches = 0;

        cards.forEach(card => {
            const text = card.innerText.toLowerCase();
            if (!q || text.includes(q)) {
                card.style.display = "flex";
                matches++;
            } else {
                card.style.display = "none";
            }
        });

        if (statusTxt) {
            statusTxt.innerText = q ? `Coincidencias para "${q}": ${matches} boutique(s)` : "Departamentos y Tiendas Especializadas";
        }
    }

    function syncPortalCartBadge() {
        try {
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) {
                const cart = JSON.parse(raw);
                const count = Array.isArray(cart) ? cart.reduce((sum, i) => sum + (parseInt(i.quantity) || 0), 0) : 0;
                const badge = document.getElementById('portal-cart-badge');
                if (badge) badge.innerText = count;
            }
        } catch(e) {}
    }
    document.addEventListener('DOMContentLoaded', syncPortalCartBadge);
    window.addEventListener('storage', syncPortalCartBadge);
    </script>
</body>
</html>
"""

for path in portal_paths:
    if os.path.exists(os.path.dirname(path)) or os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(PORTAL_REESTRUCTURADO_HTML)
        print(f"✓ Portal Matriz actualizado en: {path}")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
sitios_web_repo = os.path.join(BASE_DIR, "sitios-web")
if os.path.exists(os.path.join(sitios_web_repo, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=sitios_web_repo, check=True)
    subprocess.run(["git", "commit", "-m", "refactor(matriz): busqueda central search-first, directorio lateral y pilares al fondo", "--allow-empty"], cwd=sitios_web_repo, capture_output=True)
    res_sub = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sitios_web_repo, capture_output=True, text=True)
    print(f"🟢 Submódulo sitios-web -> Push: {'OK' if res_sub.returncode == 0 else res_sub.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "refactor(portal): estructura optimizada de 7 boutiques con search-first desplegada", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
