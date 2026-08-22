import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"

# Identificar rutas del portal matriz
portal_paths = [
    os.path.join(BASE_DIR, "index.html"),
    os.path.join(BASE_DIR, "sitios-web", "index.html")
]

print("=" * 75)
print("INTEGRANDO VÍA MX CURADURÍA COMO 8.ª BOUTIQUE EN EL PORTAL MATRIZ")
print("=" * 75)

PORTAL_8_BOUTIQUES_HTML = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Ecosistema Comercial Pedro Moreno 501 A | Portal Matriz 2026</title>
    <meta name="description" content="Hub central del ecosistema comercial multi-boutique: Hardware de PC, Vía MX Curaduría, Ropa NFL Internacional, Puros & Tabacos, Dulcería, Kiosco Digital, Bazar y Liquidaciones con Carrito Global Unificado." />
    <meta name="google-site-verification" content="2xIPYIU_imoZjFogZhoFRuepS7PFhXQloOamPV7ex6Q" />
    
    <!-- Open Graph -->
    <meta property="og:type" content="website" />
    <meta property="og:title" content="Ecosistema Comercial Pedro Moreno 501 A | 8 Boutiques Especializadas" />
    <meta property="og:description" content="8 boutiques especializadas en un solo lugar con Carrito Global, 5% de Cashback y Envíos Gratis desde $1,500 MXN." />
    <meta property="og:url" content="https://iaworldcenter-creator.github.io/sitios-web/" />

    <!-- Tailwind CSS y FontAwesome -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/css/tailwind-built.css?v=1.1.0" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />

    <!-- Schema.org Organization -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "Ecosistema Comercial Pedro Moreno 501 A",
      "url": "https://iaworldcenter-creator.github.io/sitios-web/",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Pedro Moreno 501 A",
        "addressLocality": "Guadalajara",
        "addressRegion": "Jalisco",
        "postalCode": "44100",
        "addressCountry": "MX"
      },
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+52-33-3727-1440",
        "contactType": "customer service"
      }
    }
    </script>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen flex flex-col justify-between overflow-x-hidden selection:bg-cyan-500 selection:text-slate-950">

    <!-- TOP BAR DE NAVEGACIÓN CRUZADA (8 BOUTIQUES) -->
    <header class="bg-slate-900/95 backdrop-blur border-b border-slate-800 sticky top-0 z-50 shadow-xl">
        <div class="max-w-7xl mx-auto px-4 py-2.5 flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-amber-500 to-amber-300 flex items-center justify-center text-slate-950 font-black shadow-md shadow-amber-500/20">
                    <i class="fa-solid fa-cubes text-base"></i>
                </div>
                <div>
                    <span class="font-black text-base text-white tracking-wider block leading-tight">ECOSISTEMA MATRIZ</span>
                    <span class="text-[10px] font-mono text-cyan-400 uppercase tracking-widest block">Pedro Moreno 501 A &bull; GDL Centro</span>
                </div>
            </div>

            <!-- Accesos directos a las 8 Boutiques -->
            <nav class="hidden xl:flex items-center gap-1 text-[11px] font-bold text-slate-300">
                <a href="https://iaworldcenter-creator.github.io/pc-custom-lab/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-cyan-400 transition">PC Custom</a>
                <a href="https://iaworldcenter-creator.github.io/bazar-viamx-nfl.gdl/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-cyan-300 transition flex items-center gap-1"><i class="fa-solid fa-gem text-[10px] text-cyan-400"></i> Vía MX</a>
                <a href="https://iaworldcenter-creator.github.io/bazar-viamx-nfl.gdl/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-blue-400 transition">Viamx NFL</a>
                <a href="https://iaworldcenter-creator.github.io/cigarros-bazar/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-amber-400 transition">Cigarros</a>
                <a href="https://iaworldcenter-creator.github.io/dulces-bazar/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-pink-400 transition">Dulces</a>
                <a href="https://iaworldcenter-creator.github.io/kiosco-digital/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-indigo-400 transition">Kiosco</a>
                <a href="https://iaworldcenter-creator.github.io/mi-puesto-bazar/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-emerald-400 transition">Mi Puesto</a>
                <a href="https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones/" class="px-2.5 py-1.5 rounded-lg hover:bg-slate-800 hover:text-red-400 transition">Liquidaciones</a>
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

    <!-- HERO CENTRAL -->
    <section class="relative py-12 px-4 border-b border-slate-800/80 bg-gradient-to-b from-slate-900/60 via-slate-950 to-slate-950">
        <div class="max-w-5xl mx-auto text-center flex flex-col items-center gap-4">
            <span class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-mono font-bold uppercase tracking-wider">
                <i class="fa-solid fa-shield-halved"></i> Ecosistema Comercial Multicuentas 2026
            </span>
            <h1 class="text-3xl sm:text-5xl font-black text-white tracking-tight leading-tight">
                8 Boutiques Especializadas.<br /><span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-amber-200 to-cyan-400">Un Solo Carrito Global y Envíos Consolidados.</span>
            </h1>
            <p class="text-sm sm:text-base text-slate-400 max-w-2xl leading-relaxed">
                Selecciona tus artículos en cualquiera de nuestras tiendas. Todo se acumula en una misma canasta para aprovechar <strong>Envío Gratis desde $1,500 MXN</strong>, <strong>15% de Descuento de Mayoreo (10+ piezas)</strong> y <strong>5% de Cashback</strong> con registro activo.
            </p>

            <!-- Pilares -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full max-w-3xl mt-4 text-xs">
                <div class="p-3 bg-slate-900/80 border border-slate-800 rounded-xl flex items-center gap-3 text-left">
                    <i class="fa-solid fa-truck-fast text-amber-400 text-lg"></i>
                    <div>
                        <strong class="text-white block">Envío Gratis</strong>
                        <span class="text-slate-400 text-[11px]">En compras desde $1,500 MXN</span>
                    </div>
                </div>
                <div class="p-3 bg-slate-900/80 border border-slate-800 rounded-xl flex items-center gap-3 text-left">
                    <i class="fa-solid fa-percent text-cyan-400 text-lg"></i>
                    <div>
                        <strong class="text-white block">15% Mayoreo</strong>
                        <span class="text-slate-400 text-[11px]">Automático al llevar 10+ piezas</span>
                    </div>
                </div>
                <div class="p-3 bg-slate-900/80 border border-slate-800 rounded-xl flex items-center gap-3 text-left">
                    <i class="fa-solid fa-coins text-emerald-400 text-lg"></i>
                    <div>
                        <strong class="text-white block">5% Cashback</strong>
                        <span class="text-slate-400 text-[11px]">Acumulable con registro activo</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- RETÍCULA EXACTA DE 8 BOUTIQUES (2 FILAS DE 4 TARJETAS) -->
    <main class="max-w-7xl mx-auto px-4 py-12 flex-1 w-full">
        <div class="flex flex-col gap-8">
            
            <div class="text-center mb-2">
                <h2 class="text-2xl font-black text-white tracking-tight">Directorio de Boutiques del Ecosistema</h2>
                <p class="text-xs font-mono text-slate-400 uppercase tracking-wider mt-1">Haz clic en cualquier departamento para comprar</p>
            </div>

            <!-- GRID PERFECTO DE 8 TARJETAS (4 EN FILA SUPERIOR + 4 EN FILA INFERIOR) -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

                <!-- 1. PC CUSTOM LAB -->
                <div class="bg-slate-900/90 border border-slate-800 hover:border-cyan-500/50 rounded-2xl p-5 shadow-xl transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between group">
                    <div class="flex flex-col gap-3">
                        <div class="flex items-center justify-between">
                            <span class="text-[10px] font-mono font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 px-2.5 py-0.5 rounded-full uppercase tracking-wider">Tecnología</span>
                            <i class="fa-solid fa-microchip text-cyan-400 text-lg group-hover:scale-110 transition"></i>
                        </div>
                        <h3 class="text-lg font-bold text-white group-hover:text-cyan-400 transition">PC Custom Lab</h3>
                        <p class="text-xs text-slate-400 leading-relaxed">
                            Tarjetas gráficas NVIDIA RTX y AMD Radeon, ensambles gamers personalizados, procesadores y refacciones para equipos de alto rendimiento.
                        </p>
                    </div>
                    <a href="https://iaworldcenter-creator.github.io/pc-custom-lab/" class="mt-5 w-full bg-slate-800 hover:bg-cyan-500 hover:text-slate-950 text-white font-bold py-2.5 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2">
                        Visitar Boutique <i class="fa-solid fa-arrow-right text-[10px]"></i>
                    </a>
                </div>

                <!-- 2. VÍA MX | CURADURÍA INTERNACIONAL (NUEVA INCORPORACIÓN) -->
                <div class="bg-slate-900/90 border border-cyan-500/40 hover:border-cyan-400 rounded-2xl p-5 shadow-xl shadow-cyan-950/20 transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between group relative overflow-hidden">
                    <div class="absolute -top-10 -right-10 w-24 h-24 bg-cyan-500/10 rounded-full blur-xl pointer-events-none"></div>
                    <div class="flex flex-col gap-3">
                        <div class="flex items-center justify-between">
                            <span class="text-[10px] font-mono font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 px-2.5 py-0.5 rounded-full uppercase tracking-wider">Curaduría B2B</span>
                            <i class="fa-solid fa-gem text-cyan-400 text-lg group-hover:scale-110 transition"></i>
                        </div>
                        <h3 class="text-lg font-bold text-white group-hover:text-cyan-300 transition">Vía MX Curaduría</h3>
                        <p class="text-xs text-slate-400 leading-relaxed">
                            Catálogo selecto de 200 artículos con 30 departamentos: electrónica de consumo, electrodomésticos, herramientas pro, smart home y oportunidades B2B.
                        </p>
                    </div>
                    <a href="https://iaworldcenter-creator.github.io/bazar-viamx-nfl.gdl/" class="mt-5 w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-black py-2.5 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2 shadow-md shadow-cyan-500/20">
                        Visitar Boutique <i class="fa-solid fa-arrow-right text-[10px]"></i>
                    </a>
                </div>

                <!-- 3. BAZAR VIAMX NFL -->
                <div class="bg-slate-900/90 border border-slate-800 hover:border-blue-500/50 rounded-2xl p-5 shadow-xl transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between group">
                    <div class="flex flex-col gap-3">
                        <div class="flex items-center justify-between">
                            <span class="text-[10px] font-mono font-bold bg-blue-500/10 text-blue-400 border border-blue-500/30 px-2.5 py-0.5 rounded-full uppercase tracking-wider">Internacional</span>
                            <i class="fa-solid fa-football text-blue-400 text-lg group-hover:scale-110 transition"></i>
                        </div>
                        <h3 class="text-lg font-bold text-white group-hover:text-blue-400 transition">Bazar Viamx NFL</h3>
                        <p class="text-xs text-slate-400 leading-relaxed">
                            Ropa deportiva importada, jerseys originales de la NFL, chamarras, gorras oficiales y artículos de colección para aficionados exigentes.
                        </p>
                    </div>
                    <a href="https://iaworldcenter-creator.github.io/bazar-viamx-nfl.gdl/" class="mt-5 w-full bg-slate-800 hover:bg-blue-500 hover:text-white text-white font-bold py-2.5 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2">
                        Visitar Boutique <i class="fa-solid fa-arrow-right text-[10px]"></i>
                    </a>
                </div>

                <!-- 4. CIGARROS BAZAR -->
                <div class="bg-slate-900/90 border border-slate-800 hover:border-amber-500/50 rounded-2xl p-5 shadow-xl transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between group">
                    <div class="flex flex-col gap-3">
                        <div class="flex items-center justify-between">
                            <span class="text-[10px] font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30 px-2.5 py-0.5 rounded-full uppercase tracking-wider">Tabaco</span>
                            <i class="fa-solid fa-smoking text-amber-400 text-lg group-hover:scale-110 transition"></i>
                        </div>
                        <h3 class="text-lg font-bold text-white group-hover:text-amber-400 transition">Cigarros Bazar</h3>
                        <p class="text-xs text-slate-400 leading-relaxed">
                            Puros finos y habanos de importación, tabaco selecto para liar, encendedores especiales, cortapuros y accesorios de alta categoría.
                        </p>
                    </div>
                    <a href="https://iaworldcenter-creator.github.io/cigarros-bazar/" class="mt-5 w-full bg-slate-800 hover:bg-amber-500 hover:text-slate-950 text-white font-bold py-2.5 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2">
                        Visitar Boutique <i class="fa-solid fa-arrow-right text-[10px]"></i>
                    </a>
                </div>

                <!-- 5. DULCES BAZAR -->
                <div class="bg-slate-900/90 border border-slate-800 hover:border-pink-500/50 rounded-2xl p-5 shadow-xl transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between group">
                    <div class="flex flex-col gap-3">
                        <div class="flex items-center justify-between">
                            <span class="text-[10px] font-mono font-bold bg-pink-500/10 text-pink-400 border border-pink-500/30 px-2.5 py-0.5 rounded-full uppercase tracking-wider">Dulcería</span>
                            <i class="fa-solid fa-candy-cane text-pink-400 text-lg group-hover:scale-110 transition"></i>
                        </div>
                        <h3 class="text-lg font-bold text-white group-hover:text-pink-400 transition">Dulces Bazar</h3>
                        <p class="text-xs text-slate-400 leading-relaxed">
                            Botanas tradicionales, confitería mexicana e importada, dulces típicos y opciones al mayoreo para eventos y negocios.
                        </p>
                    </div>
                    <a href="https://iaworldcenter-creator.github.io/dulces-bazar/" class="mt-5 w-full bg-slate-800 hover:bg-pink-500 hover:text-white text-white font-bold py-2.5 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2">
                        Visitar Boutique <i class="fa-solid fa-arrow-right text-[10px]"></i>
                    </a>
                </div>

                <!-- 6. KIOSCO DIGITAL -->
                <div class="bg-slate-900/90 border border-slate-800 hover:border-indigo-500/50 rounded-2xl p-5 shadow-xl transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between group">
                    <div class="flex flex-col gap-3">
                        <div class="flex items-center justify-between">
                            <span class="text-[10px] font-mono font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 px-2.5 py-0.5 rounded-full uppercase tracking-wider">Lectura</span>
                            <i class="fa-solid fa-newspaper text-indigo-400 text-lg group-hover:scale-110 transition"></i>
                        </div>
                        <h3 class="text-lg font-bold text-white group-hover:text-indigo-400 transition">Kiosco Digital</h3>
                        <p class="text-xs text-slate-400 leading-relaxed">
                            Periódicos del día, revistas de interés especializado, cómics coleccionables y material editorial selecto con entregas locales.
                        </p>
                    </div>
                    <a href="https://iaworldcenter-creator.github.io/kiosco-digital/" class="mt-5 w-full bg-slate-800 hover:bg-indigo-500 hover:text-white text-white font-bold py-2.5 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2">
                        Visitar Boutique <i class="fa-solid fa-arrow-right text-[10px]"></i>
                    </a>
                </div>

                <!-- 7. MI PUESTO BAZAR -->
                <div class="bg-slate-900/90 border border-slate-800 hover:border-emerald-500/50 rounded-2xl p-5 shadow-xl transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between group">
                    <div class="flex flex-col gap-3">
                        <div class="flex items-center justify-between">
                            <span class="text-[10px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2.5 py-0.5 rounded-full uppercase tracking-wider">Bazar Matriz</span>
                            <i class="fa-solid fa-store text-emerald-400 text-lg group-hover:scale-110 transition"></i>
                        </div>
                        <h3 class="text-lg font-bold text-white group-hover:text-emerald-400 transition">Mi Puesto Bazar</h3>
                        <p class="text-xs text-slate-400 leading-relaxed">
                            La tienda matriz con surtido misceláneo completo: novedades, papelería, artículos de conveniencia diaria y consumibles de paso.
                        </p>
                    </div>
                    <a href="https://iaworldcenter-creator.github.io/mi-puesto-bazar/" class="mt-5 w-full bg-slate-800 hover:bg-emerald-500 hover:text-slate-950 text-white font-bold py-2.5 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2">
                        Visitar Boutique <i class="fa-solid fa-arrow-right text-[10px]"></i>
                    </a>
                </div>

                <!-- 8. OFERTAS & LIQUIDACIONES -->
                <div class="bg-slate-900/90 border border-slate-800 hover:border-red-500/50 rounded-2xl p-5 shadow-xl transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between group">
                    <div class="flex flex-col gap-3">
                        <div class="flex items-center justify-between">
                            <span class="text-[10px] font-mono font-bold bg-red-500/10 text-red-400 border border-red-500/30 px-2.5 py-0.5 rounded-full uppercase tracking-wider">Outlet</span>
                            <i class="fa-solid fa-tags text-red-400 text-lg group-hover:scale-110 transition"></i>
                        </div>
                        <h3 class="text-lg font-bold text-white group-hover:text-red-400 transition">Ofertas & Liquidaciones</h3>
                        <p class="text-xs text-slate-400 leading-relaxed">
                            Oportunidades únicas de remate, piezas únicas de liquidación, excedentes de catálogo con hasta 50% de descuento y disponibilidad inmediata.
                        </p>
                    </div>
                    <a href="https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones/" class="mt-5 w-full bg-slate-800 hover:bg-red-500 hover:text-white text-white font-bold py-2.5 rounded-xl text-xs uppercase tracking-wider transition text-center flex items-center justify-center gap-2">
                        Visitar Boutique <i class="fa-solid fa-arrow-right text-[10px]"></i>
                    </a>
                </div>

            </div>

        </div>
    </main>

    <!-- FOOTER UNIVERSAL (3 COLUMNAS) -->
    <footer class="bg-slate-950 border-t border-slate-900 pt-16 pb-8 text-slate-400 text-xs mt-16">
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

    <!-- SINCRONIZADOR DE BADGE GLOBAL -->
    <script>
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

# Actualizar ambos archivos
for path in portal_paths:
    if os.path.exists(os.path.dirname(path)) or os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(PORTAL_8_BOUTIQUES_HTML)
        print(f"✓ Portal actualizado con 8 boutiques en: {path}")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
sitios_web_repo = os.path.join(BASE_DIR, "sitios-web")
if os.path.exists(os.path.join(sitios_web_repo, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=sitios_web_repo, check=True)
    subprocess.run(["git", "commit", "-m", "feat(portal): integrar Via MX Curaduria como 8va boutique completando reticula 4x2", "--allow-empty"], cwd=sitios_web_repo, capture_output=True)
    res_sub = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sitios_web_repo, capture_output=True, text=True)
    print(f"🟢 Submódulo sitios-web -> Push: {'OK' if res_sub.returncode == 0 else res_sub.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(portal): reticula simetrica de 8 boutiques con Via MX Curaduria desplegada", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
