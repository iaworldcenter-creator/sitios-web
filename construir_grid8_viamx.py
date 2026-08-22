import os
import json
import subprocess

BASE_DIR = r"E:\sitios web"
VIAMX_DIR = os.path.join(BASE_DIR, "bazar-viamx-nfl.gdl")

if not os.path.exists(VIAMX_DIR):
    alt = os.path.join(BASE_DIR, "bazar-viamx-NFL.GDL")
    if os.path.exists(alt):
        VIAMX_DIR = alt

INDEX_PATH = os.path.join(VIAMX_DIR, "index.html")
CATALOG_PATH = os.path.join(VIAMX_DIR, "catalog.json")

print("=" * 70)
print("INTEGRANDO ESTRUCTURA DE 8 COLUMNAS Y 20 PRODUCTOS SÍNCRONOS EN VÍA MX")
print("=" * 70)

productos_data = [
    {
        "sku": "VMX-EL-001",
        "nombre": "Sony Audífonos Inalámbricos On-Ear WH-CH520 (Hasta 50h)",
        "precio": 699.00,
        "categoria": "electronica",
        "marca": "Sony",
        "descripcion": "Audífonos de diadema Bluetooth con hasta 50 horas de batería, carga rápida y conexión multipunto.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-002",
        "nombre": "Amazon Echo Pop Bocina Inteligente Alexa (Negro)",
        "precio": 999.00,
        "categoria": "smarthome",
        "marca": "Amazon",
        "descripcion": "Bocina inteligente compacta de sonido envolvente con asistente virtual Alexa integrado.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-003",
        "nombre": "1 Hora Bocina Bluetooth Portátil 5W (Radio FM / MicroSD)",
        "precio": 141.99,
        "categoria": "electronica",
        "marca": "1 Hora",
        "descripcion": "Mini bocina inalámbrica de 5W con 25 horas de reproducción, radio FM y ranura MicroSD.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-HR-004",
        "nombre": "Juego de Destornilladores de Precisión 117 en 1 AXIDUN",
        "precio": 149.00,
        "categoria": "herramientas",
        "marca": "AXIDUN",
        "descripcion": "Kit magnético profesional de puntas intercambiables para electrónica y celulares.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-005",
        "nombre": "INIU Power Bank 20000mAh 22.5W Carga Rápida",
        "precio": 599.99,
        "categoria": "electronica",
        "marca": "INIU",
        "descripcion": "Batería externa de alta capacidad con display digital LED y puertos USB-C de carga veloz.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-006",
        "nombre": "Amazon Echo Dot (5ta Gen) Bocina Alexa (Negro)",
        "precio": 1699.00,
        "categoria": "smarthome",
        "marca": "Amazon",
        "descripcion": "Bocina inteligente con audio de alta fidelidad, voces nítidas y control domótico.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-007",
        "nombre": "Amazon Echo Pop Bocina Alexa (Lavanda)",
        "precio": 999.00,
        "categoria": "smarthome",
        "marca": "Amazon",
        "descripcion": "Altavoz compacto con sonido direccional en acabado lavanda con Alexa integrada.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-008",
        "nombre": "Skullcandy Dime 3 Auriculares In-Ear Inalámbricos",
        "precio": 447.00,
        "categoria": "electronica",
        "marca": "Skullcandy",
        "descripcion": "Auriculares True Wireless compactos con micrófono, resistencia al agua IPX4 y estuche.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-009",
        "nombre": "Soundcore by Anker V20i Audífonos Open-Ear",
        "precio": 498.98,
        "categoria": "electronica",
        "marca": "Anker",
        "descripcion": "Audífonos ergonómicos de oído abierto con sonido ultra claro para jornadas prolongadas.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-010",
        "nombre": "Soundcore by Anker P30i con Cancelación de Ruido",
        "precio": 537.98,
        "categoria": "electronica",
        "marca": "Anker",
        "descripcion": "Auriculares inalámbricos con cancelación activa de ruido híbrida y graves profundos.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-011",
        "nombre": "AXIDUN Barra de Sonido RGB Estéreo Bluetooth 5.0",
        "precio": 298.00,
        "categoria": "electronica",
        "marca": "AXIDUN",
        "descripcion": "Soundbar para escritorio con iluminación dinámica RGB y conexión Bluetooth 5.0.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-HR-012",
        "nombre": "Kit de Soldadura Electrónica 80W LCD Regulable",
        "precio": 349.99,
        "categoria": "herramientas",
        "marca": "Tech Tool",
        "descripcion": "Cautín profesional de 80W con display digital LCD y control térmico 180°C - 520°C.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-013",
        "nombre": "ISTENTINFY Kit Electrónica Protoboard Arduino Uno",
        "precio": 262.24,
        "categoria": "maker",
        "marca": "Arduino Compatible",
        "descripcion": "Set de prototipado con cables jumper, LEDs, resistencias y botones para proyectos.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-014",
        "nombre": "JBL Tune 520BT Audífonos Diadema Pure Bass (Negro)",
        "precio": 699.00,
        "categoria": "electronica",
        "marca": "JBL",
        "descripcion": "Audífonos Bluetooth con sonido Pure Bass y hasta 57 horas continuas de autonomía.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-015",
        "nombre": "FANDBO Multicontacto Extensión 12 en 1 (USB-C / CA)",
        "precio": 263.11,
        "categoria": "electronica",
        "marca": "FANDBO",
        "descripcion": "Estación de energía con 8 tomas CA, puertos USB de carga rápida y cable de 1.5m.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-016",
        "nombre": "Amazon Echo Pop Bocina Inteligente Alexa (Blanco)",
        "precio": 999.00,
        "categoria": "smarthome",
        "marca": "Amazon",
        "descripcion": "Bocina inteligente compacta en elegante color blanco con asistente Alexa y audio HD.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-017",
        "nombre": "Uplayteck Antena TV Digital Interior HDTV 1080P/4K",
        "precio": 220.15,
        "categoria": "lineablanca",
        "marca": "Uplayteck",
        "descripcion": "Antena para sintonización abierta en alta definición 1080P/4K con amplificador.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-018",
        "nombre": "Motorola Moto G06 Azul (4GB RAM / 256GB)",
        "precio": 2368.00,
        "categoria": "telefonia",
        "marca": "Motorola",
        "descripcion": "Smartphone desbloqueado con 256GB de almacenamiento interno y batería de larga duración.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-019",
        "nombre": "Kit de Robótica y Electrónica Compatible Arduino R3",
        "precio": 544.00,
        "categoria": "maker",
        "marca": "Maker Pro",
        "descripcion": "Kit de componentes y módulos de aprendizaje para robótica con microcontrolador R3.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-020",
        "nombre": "Qiilu Altavoces Estéreo USB de Escritorio",
        "precio": 209.00,
        "categoria": "electronica",
        "marca": "Qiilu",
        "descripcion": "Par de bocinas compactas para PC/laptop con alimentación USB y audio 3.5mm.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    }
]

# Guardar catalog.json
with open(CATALOG_PATH, "w", encoding="utf-8") as f:
    json.dump(productos_data, f, indent=4, ensure_ascii=False)

JSON_EMBEDDED = json.dumps(productos_data, ensure_ascii=False)

INDEX_COMPLETO = f"""<!DOCTYPE html>
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
    @font-face {{ font-family: 'FontAwesome'; font-display: swap; }}
    @font-face {{ font-family: 'Font Awesome 6 Free'; font-display: swap; }}
    @font-face {{ font-family: 'Font Awesome 6 Brands'; font-display: swap; }}
    body {{ font-display: swap; }}
    </style>
    
    <script>
    window.addEventListener('error', function(e) {{ e.preventDefault(); return true; }}, true);
    window.addEventListener('unhandledrejection', function(e) {{ e.preventDefault(); }});
    </script>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased overflow-x-hidden min-h-screen flex flex-col justify-between">

    <!-- ========================================================================
         CABECERA OFICIAL VIAMX (2 NIVELES CON BUSCADOR AMPLIO)
         ======================================================================== -->
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

        <!-- Nivel 2: Fila Principal en UNA SOLA LÍNEA -->
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

            <!-- 2. CENTRO: Buscador Amplio con Fondo Color Hueso -->
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
         HERO SLIDER SECTION (5 FOTOS FAMILIA TIGRE - 720PX - COBERTURA COMPLETA)
         ======================================================================== -->
    <div id="hero-slider-container" style="position: relative; width: 100%; height: 720px; min-height: 720px; overflow: hidden; background-color: #020617; border-bottom: 1px solid #1e293b; user-select: none;">
        <div id="hero-slider" style="position: relative; width: 100%; height: 100%;">
            <div class="hero-slide active" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 1; z-index: 10; transition: opacity 1000ms ease-in-out; background-image: url('assets/img/carucel (1).jpeg'); background-size: cover; background-position: center;"></div>
            <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 1000ms ease-in-out; background-image: url('assets/img/carucel (2).jpeg'); background-size: cover; background-position: center;"></div>
            <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 1000ms ease-in-out; background-image: url('assets/img/carucel (3).jpeg'); background-size: cover; background-position: center;"></div>
            <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 1000ms ease-in-out; background-image: url('assets/img/carucel (4).jpeg'); background-size: cover; background-position: center;"></div>
            <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 1000ms ease-in-out; background-image: url('assets/img/carucel (5).jpeg'); background-size: cover; background-position: center;"></div>
        </div>

        <!-- Controles Izquierda / Derecha -->
        <button type="button" aria-label="Anterior" onclick="prevSlide()" style="position: absolute; left: 24px; top: 50%; transform: translateY(-50%); z-index: 20; width: 48px; height: 48px; border-radius: 9999px; background-color: rgba(2, 6, 23, 0.75); color: #ffffff; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 10px 25px rgba(0,0,0,0.5); backdrop-filter: blur(8px); transition: all 0.3s;">
            <i class="fa-solid fa-chevron-left" style="font-size: 18px;"></i>
        </button>
        <button type="button" aria-label="Siguiente" onclick="nextSlide()" style="position: absolute; right: 24px; top: 50%; transform: translateY(-50%); z-index: 20; width: 48px; height: 48px; border-radius: 9999px; background-color: rgba(2, 6, 23, 0.75); color: #ffffff; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 10px 25px rgba(0,0,0,0.5); backdrop-filter: blur(8px); transition: all 0.3s;">
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
         CATÁLOGO PRINCIPAL EN GRID DE 8 COLUMNAS SIMÉTRICAS (TIPO AMAZON / B2B)
         ======================================================================== -->
    <main class="flex-1 w-full py-16 bg-slate-900/90 border-t border-slate-800 text-slate-100" id="catalogo">
        <div class="w-full px-4 sm:px-6 lg:px-8">
            
            <!-- Encabezado de Sección -->
            <div class="text-center mb-12">
                <span class="text-xs font-mono text-cyan-400 uppercase tracking-widest block mb-2">// VíaMX Curaduría Selecta & Boutique Internacional</span>
                <h2 class="text-3xl sm:text-4xl font-black text-white">Catálogo de Oportunidades & Electrónica 2026</h2>
                <p class="text-slate-400 text-sm sm:text-base mt-2 max-w-2xl mx-auto">Selección de artículos garantizados, electrónica de consumo, herramientas y oportunidades de importación directa en Guadalajara Centro.</p>
            </div>

            <!-- GRID VIRTUAL DE 8 COLUMNAS SIMÉTRICAS -->
            <div class="grid grid-cols-8 gap-6">
                
                <!-- COLUMNA 1: Margen Izquierdo Vacío -->
                <div class="hidden lg:block col-span-1"></div>

                <!-- COLUMNA 2: Sidebar de Departamentos y Divisiones -->
                <aside class="col-span-8 lg:col-span-1 w-full bg-slate-950/90 border border-slate-800 rounded-2xl p-4 lg:p-5 shadow-xl sticky lg:top-24 top-16 z-30 self-start flex flex-row lg:flex-col overflow-x-auto lg:overflow-visible gap-4 lg:gap-6 whitespace-nowrap lg:whitespace-normal scrollbar-none items-center lg:items-stretch">
                    <h3 class="text-sm font-black text-white hidden lg:flex items-center gap-2 border-b border-slate-800 pb-3">
                        <i class="fa-solid fa-layer-group text-amber-400"></i> Departamentos
                    </h3>
                    
                    <div class="flex flex-row lg:flex-col gap-2 lg:gap-1.5 w-full">
                        <button onclick="filterByDept('todos', this)" class="dept-btn text-left px-3 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 cursor-pointer">
                            <i class="fa-solid fa-border-all text-[11px]"></i> Todos los Artículos
                        </button>
                        <button onclick="filterByDept('electronica', this)" class="dept-btn text-left px-3 py-2 rounded-xl text-xs font-bold text-slate-300 hover:text-white hover:bg-slate-900 border border-transparent transition flex items-center gap-2 cursor-pointer">
                            <i class="fa-solid fa-headphones text-[11px] text-cyan-400"></i> Electrónica & Audio
                        </button>
                        <button onclick="filterByDept('smarthome', this)" class="dept-btn text-left px-3 py-2 rounded-xl text-xs font-bold text-slate-300 hover:text-white hover:bg-slate-900 border border-transparent transition flex items-center gap-2 cursor-pointer">
                            <i class="fa-solid fa-robot text-[11px] text-amber-400"></i> Smart Home & Alexa
                        </button>
                        <button onclick="filterByDept('herramientas', this)" class="dept-btn text-left px-3 py-2 rounded-xl text-xs font-bold text-slate-300 hover:text-white hover:bg-slate-900 border border-transparent transition flex items-center gap-2 cursor-pointer">
                            <i class="fa-solid fa-screwdriver-wrench text-[11px] text-emerald-400"></i> Herramientas Pro
                        </button>
                        <button onclick="filterByDept('maker', this)" class="dept-btn text-left px-3 py-2 rounded-xl text-xs font-bold text-slate-300 hover:text-white hover:bg-slate-900 border border-transparent transition flex items-center gap-2 cursor-pointer">
                            <i class="fa-solid fa-microchip text-[11px] text-purple-400"></i> Maker & Arduino
                        </button>
                        <button onclick="filterByDept('telefonia', this)" class="dept-btn text-left px-3 py-2 rounded-xl text-xs font-bold text-slate-300 hover:text-white hover:bg-slate-900 border border-transparent transition flex items-center gap-2 cursor-pointer">
                            <i class="fa-solid fa-mobile-screen text-[11px] text-blue-400"></i> Telefonía Móvil
                        </button>
                        <button onclick="filterByDept('lineablanca', this)" class="dept-btn text-left px-3 py-2 rounded-xl text-xs font-bold text-slate-300 hover:text-white hover:bg-slate-900 border border-transparent transition flex items-center gap-2 cursor-pointer">
                            <i class="fa-solid fa-tv text-[11px] text-pink-400"></i> Video & TV Abierta
                        </button>
                    </div>

                    <div class="pt-4 border-t border-slate-800 hidden lg:block">
                        <span class="text-[10px] font-mono text-slate-400 uppercase tracking-wider block mb-1">Garantía Local</span>
                        <p class="text-[11px] text-slate-300 leading-relaxed font-semibold">
                            Revisión y entrega directa en Pedro Moreno 501 A.
                        </p>
                    </div>
                </aside>

                <!-- COLUMNAS 3 A 7: Cuadrícula de Productos (5 columnas interiores) -->
                <div class="col-span-8 lg:col-span-5">
                    
                    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6 pb-3 border-b border-slate-800">
                        <span class="text-xs font-mono text-cyan-400 font-bold uppercase tracking-wider" id="catalog-count-text">
                            Mostrando 20 artículos disponibles
                        </span>
                        <div class="flex items-center gap-2 text-xs text-slate-400 font-mono">
                            <i class="fa-solid fa-shield-check text-emerald-400"></i> Pago Seguro & 5% Cashback
                        </div>
                    </div>

                    <!-- Cuadrícula Dinámica -->
                    <div id="catalog-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                        <!-- Poblado síncronamente desde JavaScript -->
                    </div>

                </div>

                <!-- COLUMNA 8: Margen Derecho Vacío -->
                <div class="hidden lg:block col-span-1"></div>

            </div>

        </div>
    </main>

    <!-- ========================================================================
         FOOTER UNIVERSAL
         ======================================================================== -->
    <footer class="py-12 border-t border-slate-800 bg-slate-950 text-center text-xs text-slate-400 font-mono">
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
         BASE DE DATOS SÍNCRONA, LÓGICA DE TIENDA Y CARRUSEL
         ======================================================================== -->
    <script>
    const viamxCatalog = {JSON_EMBEDDED};
    let currentFilteredCatalog = [...viamxCatalog];

    function formatCurrency(amount) {{
        const num = parseFloat(amount) || 0;
        return '$' + num.toLocaleString('es-MX', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
    }}

    function renderCatalog(items) {{
        const grid = document.getElementById("catalog-grid");
        const countText = document.getElementById("catalog-count-text");
        if (!grid) return;
        
        if (countText) countText.textContent = `Mostrando ${{items.length}} artículo(s) disponibles`;

        if (!items || items.length === 0) {{
            grid.innerHTML = '<div class="col-span-full text-center text-slate-400 text-sm py-12 bg-slate-950/60 rounded-2xl border border-slate-800"><i class="fa-solid fa-magnifying-glass text-3xl mb-2 text-slate-600 block"></i>No se encontraron artículos con ese criterio de búsqueda.</div>';
            return;
        }}

        grid.innerHTML = items.map(item => `
            <div class="bg-slate-950/90 border border-slate-800/90 hover:border-cyan-500/60 rounded-2xl p-4 flex flex-col justify-between transition duration-300 shadow-xl group cursor-pointer hover:shadow-cyan-950/20">
                <div>
                    <div class="w-full h-44 overflow-hidden rounded-xl bg-slate-900 border border-slate-800/80 flex items-center justify-center mb-3 p-2 relative">
                        <img 
                            src="${{item.imagen || 'assets/img/mascota_tigre_thumb.webp'}}" 
                            alt="${{item.nombre}}" 
                            loading="lazy" 
                            decoding="async" 
                            width="300" 
                            height="300" 
                            class="w-full h-full object-contain group-hover:scale-105 transition duration-300" 
                            onerror="this.onerror=null;this.src='assets/img/mascota_tigre_thumb.webp';"
                        />
                    </div>
                    <div class="flex items-center justify-between gap-1 mb-1">
                        <span class="text-[10px] font-mono text-cyan-400 font-bold uppercase tracking-wider block">${{item.marca || 'Vía MX'}}</span>
                        <span class="text-[9px] font-mono text-slate-500 uppercase">${{item.sku}}</span>
                    </div>
                    <h4 class="text-white font-bold text-xs sm:text-sm mb-1.5 line-clamp-2 leading-snug group-hover:text-cyan-300 transition" title="${{item.nombre}}">${{item.nombre}}</h4>
                    <p class="text-slate-400 text-xs mb-3 line-clamp-2 leading-relaxed font-normal">${{item.descripcion || ''}}</p>
                </div>
                <div class="flex justify-between items-center pt-3 border-t border-slate-800/80">
                    <div>
                        <span class="text-[9px] font-mono text-slate-400 block uppercase">Precio</span>
                        <span class="text-amber-400 font-black text-sm sm:text-base font-mono">${{formatCurrency(item.precio)}}</span>
                    </div>
                    <button onclick="addToCart('${{item.sku}}')" class="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black px-3.5 py-2 rounded-xl text-xs flex items-center gap-1.5 transition active:scale-95 shadow-md shadow-cyan-500/20 cursor-pointer">
                        <i class="fa-solid fa-cart-plus"></i> Agregar
                    </button>
                </div>
            </div>
        `).join('');
    }}

    function filterByDept(dept, btn) {{
        document.querySelectorAll('.dept-btn').forEach(b => {{
            b.className = "dept-btn text-left px-3 py-2 rounded-xl text-xs font-bold text-slate-300 hover:text-white hover:bg-slate-900 border border-transparent transition flex items-center gap-2 cursor-pointer";
        }});
        if (btn) {{
            btn.className = "dept-btn text-left px-3 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 cursor-pointer";
        }}

        if (dept === 'todos') {{
            currentFilteredCatalog = [...viamxCatalog];
        }} else {{
            currentFilteredCatalog = viamxCatalog.filter(i => i.categoria === dept);
        }}
        renderCatalog(currentFilteredCatalog);
    }}

    function handleSearchSubmit(e) {{
        if (e) e.preventDefault();
        const input = document.getElementById("siteSearch");
        if (!input) return;
        
        const q = input.value.toLowerCase().trim();
        let filtered = viamxCatalog;
        if (q) {{
            filtered = filtered.filter(i => 
                (i.nombre || '').toLowerCase().includes(q) || 
                (i.descripcion || '').toLowerCase().includes(q) ||
                (i.marca || '').toLowerCase().includes(q) ||
                (i.sku || '').toLowerCase().includes(q)
            );
        }}
        renderCatalog(filtered);
        const catSec = document.getElementById("catalogo");
        if (catSec) catSec.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}

    function addToCart(sku) {{
        try {{
            const item = viamxCatalog.find(i => i.sku === sku);
            if (!item) return;
            
            const stored = localStorage.getItem("ecosystem_global_cart");
            let cart = stored ? JSON.parse(stored) : [];
            if (!Array.isArray(cart)) cart = [];
            
            const existIdx = cart.findIndex(i => i.sku === sku);
            if (existIdx > -1) {{
                cart[existIdx].quantity = (cart[existIdx].quantity || 1) + 1;
            }} else {{
                cart.push({{
                    sku: item.sku,
                    nombre: item.nombre,
                    precio: item.precio,
                    imagen: item.imagen || 'assets/img/mascota_tigre_thumb.webp',
                    categoria: item.categoria || 'viamx',
                    quantity: 1
                }});
            }}
            
            localStorage.setItem("ecosystem_global_cart", JSON.stringify(cart));
            updateCartBadge();
            alert(`"${{item.nombre}}" agregado al carrito con éxito.`);
        }} catch(e) {{}}
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

    // Control del Carrusel
    window.currentSlide = 0;
    window.sliderInterval = null;

    window.showSlide = function(index) {{
        const slides = document.querySelectorAll('.hero-slide');
        const dots = document.querySelectorAll('.hero-dot span');
        if (slides.length === 0) return;
        
        const current = slides[window.currentSlide];
        if (current) {{
            current.style.opacity = '0';
            current.style.zIndex = '0';
        }}
        const currentDot = dots[window.currentSlide];
        if (currentDot) {{
            currentDot.style.width = '12px';
            currentDot.style.backgroundColor = '#64748b';
            currentDot.style.boxShadow = 'none';
        }}
        
        window.currentSlide = (index + slides.length) % slides.length;
        
        const next = slides[window.currentSlide];
        if (next) {{
            next.style.opacity = '1';
            next.style.zIndex = '10';
        }}
        const nextDot = dots[window.currentSlide];
        if (nextDot) {{
            nextDot.style.width = '32px';
            nextDot.style.backgroundColor = '#22d3ee';
            nextDot.style.boxShadow = '0 0 10px rgba(34,211,238,0.6)';
        }}
        window.resetSliderInterval();
    }};

    window.resetSliderInterval = function() {{
        if (window.sliderInterval) clearInterval(window.sliderInterval);
        if (window.innerWidth < 640) return;
        window.sliderInterval = setInterval(() => {{
            window.nextSlide();
        }}, 5000);
    }};

    window.nextSlide = function() {{
        window.showSlide(window.currentSlide + 1);
    }};

    window.prevSlide = function() {{
        window.showSlide(window.currentSlide - 1);
    }};

    window.goToSlide = function(index) {{
        window.showSlide(index);
    }};

    document.addEventListener("DOMContentLoaded", () => {{
        renderCatalog(viamxCatalog);
        updateCartBadge();
        syncHeaderAccountStatus();
        window.showSlide(0);
        window.resetSliderInterval();
    }});
    </script>
</body>
</html>
"""

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(INDEX_COMPLETO)

print(f"✓ index.html reconstruido con Grid de 8 columnas y 20 productos síncronos.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(catalog): grid de 8 columnas y carga sincrona de 20 articulos con departamentos", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(viamx): grid simetrico 8 columnas y 20 productos visibles de inmediato", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
