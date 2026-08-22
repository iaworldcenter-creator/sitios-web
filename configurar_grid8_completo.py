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
print("CONFIGURANDO 8 COLUMNAS + 30 DEPARTAMENTOS CON SUBMENÚS FLYOUT EN VÍA MX")
print("=" * 70)

# Base de 20 productos de Electrónica y Oportunidades
productos_data = [
    {"sku": "VMX-EL-001", "nombre": "Sony Audífonos Inalámbricos On-Ear WH-CH520", "precio": 699.00, "original": 1177.00, "categoria": "electronica", "marca": "Sony", "rating": "4.8", "reviews": "9.7k", "descripcion": "Audífonos Bluetooth con hasta 50h de batería, carga rápida y conexión multipunto.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-002", "nombre": "Amazon Echo Pop Bocina Inteligente Alexa (Negro)", "precio": 999.00, "original": 999.00, "categoria": "smarthome", "marca": "Amazon", "rating": "4.8", "reviews": "30.6k", "descripcion": "Bocina inteligente compacta de sonido envolvente con asistente Alexa integrado.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-003", "nombre": "1 Hora Bocina Bluetooth Portátil 5W (Radio FM/SD)", "precio": 141.99, "original": 169.99, "categoria": "electronica", "marca": "1 Hora", "rating": "4.6", "reviews": "2.4k", "descripcion": "Mini bocina inalámbrica de 5W con 25h de reproducción continua y ranura MicroSD.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-HR-004", "nombre": "Juego de Destornilladores de Precisión 117 en 1 AXIDUN", "precio": 149.00, "original": 199.00, "categoria": "herramientas", "marca": "AXIDUN", "rating": "4.6", "reviews": "7.3k", "descripcion": "Kit magnético profesional de puntas intercambiables para electrónica y celulares.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-005", "nombre": "INIU Power Bank 20000mAh 22.5W Carga Rápida", "precio": 599.99, "original": 699.99, "categoria": "electronica", "marca": "INIU", "rating": "4.7", "reviews": "82.8k", "descripcion": "Batería externa con display digital LED y puertos USB-C de entrega de energía veloz.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-006", "nombre": "Amazon Echo Dot (5ta Gen) Bocina Alexa (Negro)", "precio": 1699.00, "original": 1699.00, "categoria": "smarthome", "marca": "Amazon", "rating": "4.8", "reviews": "48.6k", "descripcion": "Bocina inteligente con audio HD, voces nítidas y control de dispositivos del hogar.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-007", "nombre": "Amazon Echo Pop Bocina Alexa (Lavanda)", "precio": 999.00, "original": 999.00, "categoria": "smarthome", "marca": "Amazon", "rating": "4.8", "reviews": "30.6k", "descripcion": "Altavoz compacto con sonido direccional en color lavanda con Alexa integrada.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-008", "nombre": "Skullcandy Dime 3 Auriculares In-Ear Inalámbricos", "precio": 447.00, "original": 749.00, "categoria": "electronica", "marca": "Skullcandy", "rating": "4.4", "reviews": "9.5k", "descripcion": "Auriculares True Wireless con micrófono, protección IPX4 y hasta 20h de batería.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-009", "nombre": "Soundcore by Anker V20i Audífonos Open-Ear", "precio": 498.98, "original": 899.00, "categoria": "electronica", "marca": "Anker", "rating": "4.5", "reviews": "17.6k", "descripcion": "Audífonos de diseño ergonómico de oído abierto con sonido nítido y confort total.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-010", "nombre": "Soundcore by Anker P30i Cancelación Activa de Ruido", "precio": 537.98, "original": 999.00, "categoria": "electronica", "marca": "Anker", "rating": "4.5", "reviews": "40.3k", "descripcion": "Auriculares con cancelación de ruido híbrida y estuche con soporte para smartphone.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-011", "nombre": "AXIDUN Barra de Sonido RGB Estéreo Bluetooth 5.0", "precio": 298.00, "original": 399.00, "categoria": "electronica", "marca": "AXIDUN", "rating": "4.3", "reviews": "1.4k", "descripcion": "Soundbar para escritorio con iluminación dinámica RGB y conexión Bluetooth 5.0.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-HR-012", "nombre": "Kit de Soldadura Electrónica 80W LCD Regulable", "precio": 349.99, "original": 429.00, "categoria": "herramientas", "marca": "Tech Tool", "rating": "4.1", "reviews": "161", "descripcion": "Cautín profesional de 80W con display digital LCD y rango térmico 180°C - 520°C.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-013", "nombre": "ISTENTINFY Kit Electrónica Protoboard Arduino Uno", "precio": 262.24, "original": 298.00, "categoria": "maker", "marca": "Arduino Comp", "rating": "4.7", "reviews": "191", "descripcion": "Set de prototipado con cables jumper, LEDs, resistencias y botones para proyectos.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-014", "nombre": "JBL Tune 520BT Audífonos Diadema Pure Bass", "precio": 699.00, "original": 999.00, "categoria": "electronica", "marca": "JBL", "rating": "4.8", "reviews": "11.5k", "descripcion": "Audífonos Bluetooth con sonido Pure Bass y hasta 57 horas continuas de batería.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-015", "nombre": "FANDBO Multicontacto Extensión 12 en 1 USB-C / CA", "precio": 263.11, "original": 298.99, "categoria": "electronica", "marca": "FANDBO", "rating": "4.7", "reviews": "985", "descripcion": "Estación de energía con 8 tomas CA, puertos USB de carga rápida y cable de 1.5m.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-016", "nombre": "Amazon Echo Pop Bocina Inteligente Alexa (Blanco)", "precio": 999.00, "original": 999.00, "categoria": "smarthome", "marca": "Amazon", "rating": "4.8", "reviews": "30.6k", "descripcion": "Bocina compacta en acabado blanco con asistente Alexa y audio HD en streaming.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-017", "nombre": "Uplayteck Antena TV Digital Interior HDTV 1080P/4K", "precio": 220.15, "original": 259.00, "categoria": "lineablanca", "marca": "Uplayteck", "rating": "4.2", "reviews": "3.7k", "descripcion": "Antena para sintonización abierta en alta definición 1080P/4K con amplificador.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-018", "nombre": "Motorola Moto G06 Azul (4GB RAM / 256GB)", "precio": 2368.00, "original": 2999.00, "categoria": "telefonia", "marca": "Motorola", "rating": "4.4", "reviews": "111", "descripcion": "Smartphone desbloqueado con 256GB de almacenamiento interno y batería de 5000mAh.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-019", "nombre": "Kit de Robótica y Electrónica Compatible Arduino R3", "precio": 544.00, "original": 598.00, "categoria": "maker", "marca": "Maker Pro", "rating": "4.7", "reviews": "4", "descripcion": "Kit de componentes y módulos de aprendizaje para robótica con microcontrolador R3.", "imagen": "assets/img/mascota_tigre_thumb.webp"},
    {"sku": "VMX-EL-020", "nombre": "Qiilu Altavoces Estéreo USB de Escritorio", "precio": 209.00, "original": 209.00, "categoria": "electronica", "marca": "Qiilu", "rating": "3.0", "reviews": "1", "descripcion": "Par de bocinas compactas para PC/laptop con alimentación USB y audio auxiliar 3.5mm.", "imagen": "assets/img/mascota_tigre_thumb.webp"}
]

with open(CATALOG_PATH, "w", encoding="utf-8") as f:
    json.dump(productos_data, f, indent=4, ensure_ascii=False)

JSON_EMBEDDED = json.dumps(productos_data, ensure_ascii=False)

# Definición de los 30 Departamentos con sus Subcategorías para el Flyout Menu
departamentos_menu = [
    {"id": "electronica", "nombre": "Electrónica & Audio", "icon": "fa-headphones", "subs": ["Pantallas y Smart TV", "Estéreos y Bocinas", "Barras de Sonido RGB", "Audífonos In-Ear", "Audífonos de Diadema", "Bocinas Portátiles"]},
    {"id": "lineablanca", "nombre": "Línea Blanca & Climas", "icon": "fa-snowflake", "subs": ["Refrigeradores Inverter", "Lavadoras y Secadoras", "Aires Acondicionados", "Estufas y Hornos", "Hornos de Microondas", "Dispensadores de Agua"]},
    {"id": "smarthome", "nombre": "Smart Home & Domótica", "icon": "fa-robot", "subs": ["Bocinas Alexa y Echo", "Focos Inteligentes RGB", "Cámaras de Seguridad WiFi", "Cerraduras Digitales", "Enchufes Programables", "Sensores de Movimiento"]},
    {"id": "telefonia", "nombre": "Telefonía & Celulares", "icon": "fa-mobile-screen", "subs": ["Smartphones Desbloqueados", "Power Banks Carga Rápida", "Cargadores y Cables USB-C", "Fundas de Alta Protección", "Smartwatches y Bandas", "Soportes de Escritorio"]},
    {"id": "computacion", "nombre": "Computación & Laptops", "icon": "fa-laptop", "subs": ["Laptops Gamer y Trabajo", "Monitores Curvos y Planos", "Teclados Mecánicos", "Mouse Ergonómicos", "Discos SSD y M.2", "Memorias RAM DDR4/DDR5"]},
    {"id": "cocina", "nombre": "Cocina & Electrodomésticos", "icon": "fa-kitchen-set", "subs": ["Freidoras de Aire (Air Fryers)", "Licuadoras de Alta Potencia", "Cafeteras Espresso y Goteo", "Batidoras de Inmersión", "Tostadores Eléctricos", "Parrillas de Inducción"]},
    {"id": "herramientas", "nombre": "Herramientas & Ferretería", "icon": "fa-screwdriver-wrench", "subs": ["Kits de Destornilladores 117 en 1", "Cautines y Soldadura 80W", "Multímetros Digitales", "Taladros Inalámbricos", "Juegos de Llaves y Dados", "Cajas de Herramientas"]},
    {"id": "maker", "nombre": "Maker & Robótica Arduino", "icon": "fa-microchip", "subs": ["Placas Arduino Uno y R3", "Kits de Electrónica y Protoboard", "Sensores de Ultrasonido y Gas", "Servomotores y Drivers", "Cables Jumper y Pines", "Módulos ESP32 y Bluetooth"]},
    {"id": "cristaleria", "nombre": "Cristalería & Vajillas", "icon": "fa-wine-glass", "subs": ["Copas de Cristal de Lujo", "Juegos de Vasos Térmicos", "Vajillas de Cerámica Fina", "Decantadores de Vino", "Jarras de Vidrio Borosilicato", "Cubiertos de Acero Inoxidable"]},
    {"id": "moda", "nombre": "Ropa & Moda Internacional", "icon": "fa-shirt", "subs": ["Jerseys Deportivos Oficiales", "Chamarras y Rompevientos", "Sudaderas Urbanas", "Playeras de Algodón Premium", "Pantalones y Joggers", "Gorras y Sombreros"]},
    {"id": "calzado", "nombre": "Calzado & Sneakers", "icon": "fa-shoe-prints", "subs": ["Tenis Urbanos y Deportivos", "Botas de Trabajo y Senderismo", "Zapatos Casuales de Piel", "Sandalias Confort", "Plantillas Ortopédicas"]},
    {"id": "bano", "nombre": "Baño & Grifería", "icon": "fa-shower", "subs": ["Regaderas Tipo Lluvia", "Monolandos y Grifos Modernos", "Espejos Touch con Luz LED", "Accesorios de Acero Negro", "Toalleros y Repisas"]},
    {"id": "hogar", "nombre": "Hogar, Muebles & Sala", "icon": "fa-couch", "subs": ["Sillones Reclinables", "Mesas de Centro Elevables", "Lámparas de Pie Modernas", "Estantes y Libreros", "Cuadros y Arte Decorativo"]},
    {"id": "iluminacion", "nombre": "Iluminación & Neón Flex", "icon": "fa-lightbulb", "subs": ["Letreros Neón Personalizados", "Tiras LED RGBIC Inteligentes", "Lámparas de Escritorio Regulables", "Reflectores Solares LED", "Focos Vintage Edison"]},
    {"id": "joyeria", "nombre": "Joyería & Relojería", "icon": "fa-gem", "subs": ["Relojes Automáticos de Lujo", "Cadenas de Plata 925", "Pulseras de Cuero Trenzado", "Anillos de Titanio", "Estuches Organizadores"]},
    {"id": "deportes", "nombre": "Deportes & Fitness", "icon": "fa-dumbbell", "subs": ["Balones Coleccionables NFL", "Mancuernas y Pesas Rusas", "Bandas de Resistencia Pro", "Tapetes de Yoga Antideslizantes", "Cilindros Térmicos de Agua"]},
    {"id": "belleza", "nombre": "Belleza & Cuidado Personal", "icon": "fa-wand-magic", "subs": ["Rasuradoras Profesionales", "Secadoras de Pelo Iónicas", "Cepillos Alaciadores", "Masajeadores Cervicales", "Cuidado Facial y Skincare"]},
    {"id": "juguetes", "nombre": "Juguetes & Coleccionables", "icon": "fa-gamepad", "subs": ["Figuras de Acción y Anime", "Autos de Colección a Escala", "Juegos de Mesa y Estrategia", "Bloques de Construcción", "Drones con Cámara HD"]},
    {"id": "automotriz", "nombre": "Automotriz & Accesorios", "icon": "fa-car", "subs": ["Cámaras Dashcam 4K", "Transmisores FM Bluetooth", "Soportes Magnéticos para Auto", "Aspiradoras Portátiles 12V", "Arrancadores de Batería"]},
    {"id": "bebes", "nombre": "Bebés & Maternidad", "icon": "fa-baby", "subs": ["Monitores de Video para Bebé", "Esterilizadores de Biberones", "Sillas de Seguridad para Auto", "Juguetes de Estimulación", "Mochilas Pañaleras Térmicas"]},
    {"id": "mascotas", "nombre": "Mascotas & Accesorios", "icon": "fa-paw", "subs": ["Comederos Automáticos WiFi", "Fuentes de Agua para Gatos", "Camas Térmicas para Perros", "Arneses y Correas Tácticas", "Juguetes Interactivos"]},
    {"id": "oficina", "nombre": "Oficina & Papelería", "icon": "fa-briefcase", "subs": ["Sillas Ergonómicas Ejecutivas", "Organizadores de Escritorio", "Destructoras de Documentos", "Plumas Ejecutivas", "Pizarrones Blancos Magnéticos"]},
    {"id": "musica", "nombre": "Instrumentos Musicales", "icon": "fa-guitar", "subs": ["Guitarras Eléctricas y Acústicas", "Teclados y Sintetizadores", "Micrófonos de Condensador", "Interfaces de Audio USB", "Soportes y Fundas"]},
    {"id": "jardineria", "nombre": "Jardinería & Exteriores", "icon": "fa-seedling", "subs": ["Luces Solares para Jardín", "Mangueras Retráctiles 30m", "Macetas Autorriego", "Herramientas de Poda y Cuidado", "Fumigadores Manuales"]},
    {"id": "gourmet", "nombre": "Vinos & Coctelería Gourmet", "icon": "fa-martini-glass-citrus", "subs": ["Cavas Enfriadoras de Vino", "Sacacorchos Eléctricos USB", "Kits de Barman y Coctelería", "Vasos Térmicos y Shakers", "Hieleras de Acero Doble Pared"]},
    {"id": "fotografia", "nombre": "Fotografía & Video Pro", "icon": "fa-camera", "subs": ["Aros de Luz LED 18 Pulgadas", "Trípodes Profesionales 2m", "Micrófonos Inalámbricos Lavalier", "Gimbals Estabilizadores 3 Ejes", "Fondos Verdes y Softboxes"]},
    {"id": "seguridad", "nombre": "Seguridad & Vigilancia", "icon": "fa-shield-halved", "subs": ["Cámaras PTZ 360 Exterior", "Alarmas Vecinales con Sirena", "Cajas Fuertes Digitales", "Intercomunicadores con Video", "Sensores de Apertura Puerta/Ventana"]},
    {"id": "camping", "nombre": "Camping & Aventura", "icon": "fa-campground", "subs": ["Casas de Campaña Impermeables", "Lámparas de Campamento LED", "Mochilas Militares 50L", "Navajas Multiusos Suizas", "Colchones Inflables con Bomba"]},
    {"id": "salud", "nombre": "Salud & Cuidado Médico", "icon": "fa-heart-pulse", "subs": ["Baumanómetros Digitales de Brazo", "Oxímetros de Pulso Pediátrico/Adulto", "Termómetros Infrarrojos Sin Contacto", "Básculas Inteligentes con App", "Nebulizadores Portátiles"]},
    {"id": "oportunidades", "nombre": "Liquidaciones & Remates B2B", "icon": "fa-tags", "subs": ["Lotes de Importación Directa", "Remates de Almacén Guadalajara", "Artículos de Exposición Grado A", "Cajas Sorpresa de Electrónica", "Ofertas Exclusivas al Mayoreo"]}
]

# Construir HTML de los 30 Departamentos con Flyout Submenús
dept_sidebar_html = """
    <div class="flex flex-row lg:flex-col gap-1.5 w-full pr-1">
        <div class="relative group/dept">
            <button onclick="filterByDept('todos', this)" class="dept-btn w-full text-left px-3 py-2 rounded-xl text-xs font-bold transition flex items-center justify-between bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 cursor-pointer">
                <span class="flex items-center gap-2 truncate"><i class="fa-solid fa-border-all text-cyan-400 w-4 text-center"></i> Todos los Artículos</span>
                <span class="text-[10px] font-mono text-cyan-400 font-bold hidden lg:inline">20</span>
            </button>
        </div>
"""

for d in departamentos_menu:
    subs_links = "".join([f"""<a href="#catalogo" onclick="handleSearch('{s}')" class="text-xs text-slate-300 hover:text-cyan-300 hover:bg-slate-900/90 px-3 py-1.5 rounded-lg transition flex items-center gap-2"><i class="fa-solid fa-chevron-right text-[8px] text-cyan-400"></i> {s}</a>""" for s in d["subs"]])
    
    dept_sidebar_html += f"""
        <div class="relative group/dept">
            <button onclick="filterByDept('{d["id"]}', this)" class="dept-btn w-full text-left px-3 py-2 rounded-xl text-xs font-bold text-slate-300 hover:text-white hover:bg-slate-900 border border-transparent transition flex items-center justify-between cursor-pointer">
                <span class="flex items-center gap-2.5 truncate"><i class="fa-solid {d["icon"]} text-cyan-400 w-4 text-center"></i> {d["nombre"]}</span>
                <i class="fa-solid fa-chevron-right text-[9px] text-slate-500 group-hover/dept:text-cyan-400 group-hover/dept:translate-x-1 transition hidden lg:inline"></i>
            </button>
            <!-- Menú Flotante Flyout al pasar el ratón (Hover) -->
            <div class="hidden lg:group-hover/dept:flex flex-col absolute left-full top-0 ml-2.5 w-64 bg-slate-950/98 border-2 border-cyan-500/60 rounded-2xl p-4 shadow-[0_10px_35px_rgba(6,182,212,0.35)] z-50 backdrop-blur-xl animate-in fade-in duration-200">
                <div class="border-b border-slate-800 pb-2 mb-2">
                    <span class="text-[10px] font-mono text-cyan-400 font-bold uppercase tracking-wider block flex items-center gap-1.5">
                        <i class="fa-solid {d["icon"]}"></i> {d["nombre"]}
                    </span>
                    <span class="text-[10px] text-slate-400 font-semibold">Subcategorías & Modelos</span>
                </div>
                <div class="flex flex-col gap-1 max-h-64 overflow-y-auto pr-1">
                    {subs_links}
                </div>
            </div>
        </div>
    """

dept_sidebar_html += "</div>"

INDEX_COMPLETO = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="BwSy5nNuFFrHJUtxe189nJtPxM4h5QY-SxK1V8wqYDE" />
    <title>VíaMX | Curaduría y Boutique Internacional</title>
    <meta name="description" content="Boutique oficial VíaMX en Guadalajara Centro. Curaduría de artículos selectos e importaciones dentro del ecosistema Anti-Gravity. Pedro Moreno 501 A.">
    
    <link rel="preload" as="image" href="assets/img/mascota_tigre_thumb.webp" fetchpriority="high">
    
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

        <!-- Nivel 2: Fila Principal (Izquierda: Carrito/Cuenta, Centro: Buscador Amplio, Derecha: Vía MX) -->
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
         CATÁLOGO PRINCIPAL EN GRID EXACTO DE 8 COLUMNAS SIMÉTRICAS
         ======================================================================== -->
    <main class="flex-1 w-full py-16 bg-slate-900/90 border-t border-slate-800 text-slate-100" id="catalogo">
        <div class="w-full px-2 sm:px-4 lg:px-8">
            
            <!-- Encabezado de Sección Centrado -->
            <div class="text-center mb-12">
                <span class="text-xs font-mono text-cyan-400 uppercase tracking-widest block mb-2">// VíaMX Curaduría Selecta & Boutique Internacional</span>
                <h2 class="text-3xl sm:text-4xl font-black text-white">Catálogo de Oportunidades & Electrónica 2026</h2>
                <p class="text-slate-400 text-sm sm:text-base mt-2 max-w-2xl mx-auto">Selección de artículos garantizados, electrónica de consumo, herramientas y oportunidades de importación directa en Guadalajara Centro.</p>
            </div>

            <!-- GRID MAESTRO DE 8 COLUMNAS SIMÉTRICAS -->
            <div class="grid grid-cols-8 gap-4 sm:gap-6">
                
                <!-- COLUMNA 1: Margen Izquierdo Vacío -->
                <div class="hidden lg:block col-span-1"></div>

                <!-- COLUMNA 2: Sidebar de 30 Departamentos con Submenús Flyout on Hover -->
                <aside class="col-span-8 lg:col-span-1 w-full bg-slate-950/95 border border-slate-800 rounded-3xl p-3 sm:p-4 shadow-2xl sticky lg:top-24 top-16 z-30 self-start flex flex-row lg:flex-col overflow-x-auto lg:overflow-visible gap-4 lg:gap-2 whitespace-nowrap lg:whitespace-normal scrollbar-none items-center lg:items-stretch">
                    <div class="border-b border-slate-800 pb-3 mb-2 hidden lg:flex items-center justify-between">
                        <h3 class="text-xs font-mono font-black text-white uppercase tracking-wider flex items-center gap-2">
                            <i class="fa-solid fa-layer-group text-amber-400"></i> Departamentos
                        </h3>
                        <span class="text-[9px] font-mono text-slate-500">30 Áreas</span>
                    </div>
                    
                    {dept_sidebar_html}

                    <div class="pt-4 border-t border-slate-800 hidden lg:block mt-2">
                        <span class="text-[10px] font-mono text-slate-400 uppercase tracking-wider block mb-1">Garantía Local</span>
                        <p class="text-[11px] text-slate-300 leading-relaxed font-semibold">
                            Revisión y entrega física directa en Pedro Moreno 501 A.
                        </p>
                    </div>
                </aside>

                <!-- COLUMNAS 3 A 7: Cuadrícula de 5 Columnas de Productos (Tipo Amazon) -->
                <div class="col-span-8 lg:col-span-5">
                    
                    <!-- Barra de Conteo y Garantía -->
                    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6 pb-3 border-b border-slate-800">
                        <span class="text-xs font-mono text-cyan-400 font-bold uppercase tracking-wider" id="catalog-count-text">
                            Mostrando 20 artículos disponibles
                        </span>
                        <div class="flex items-center gap-2 text-xs text-slate-400 font-mono">
                            <i class="fa-solid fa-shield-check text-emerald-400"></i> Pago Seguro & 5% Cashback Acumulable
                        </div>
                    </div>

                    <!-- CUADRÍCULA INTERIOR DE 5 COLUMNAS EN DESKTOP (TIPO AMAZON) -->
                    <div id="catalog-grid" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 sm:gap-5">
                        <!-- Se poblará síncronamente desde JavaScript -->
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
            <div class="bg-slate-950/90 border border-slate-800/90 hover:border-cyan-500/60 rounded-2xl p-3.5 flex flex-col justify-between transition duration-300 shadow-xl group cursor-pointer hover:shadow-cyan-950/20">
                <div>
                    <!-- Contenedor Imagen -->
                    <div class="w-full h-36 sm:h-40 overflow-hidden rounded-xl bg-slate-900 border border-slate-800/80 flex items-center justify-center mb-3 p-1.5 relative">
                        <img 
                            src="${{item.imagen || 'assets/img/mascota_tigre_thumb.webp'}}" 
                            alt="${{item.nombre}}" 
                            loading="lazy" 
                            decoding="async" 
                            width="250" 
                            height="250" 
                            class="w-full h-full object-contain group-hover:scale-105 transition duration-300" 
                            onerror="this.onerror=null;this.src='assets/img/mascota_tigre_thumb.webp';"
                        />
                        <span class="absolute top-2 left-2 bg-amber-500/10 border border-amber-500/30 text-amber-400 text-[9px] font-mono font-black px-1.5 py-0.5 rounded shadow">
                            Oferta
                        </span>
                    </div>

                    <!-- Datos y Rating -->
                    <div class="flex items-center justify-between gap-1 mb-1">
                        <span class="text-[10px] font-mono text-cyan-400 font-bold uppercase tracking-wider block">${{item.marca || 'Vía MX'}}</span>
                        <div class="flex items-center gap-1 text-[10px] text-amber-400 font-bold">
                            <i class="fa-solid fa-star text-[9px]"></i> ${{item.rating || '4.8'}}
                        </div>
                    </div>

                    <!-- Título -->
                    <h4 class="text-white font-bold text-xs mb-1.5 line-clamp-2 leading-snug group-hover:text-cyan-300 transition" title="${{item.nombre}}">${{item.nombre}}</h4>
                    <p class="text-slate-400 text-[11px] mb-3 line-clamp-2 leading-tight font-normal">${{item.descripcion || ''}}</p>
                </div>

                <!-- Precio y Botón de Compra -->
                <div class="flex flex-col gap-2 pt-2.5 border-t border-slate-800/80">
                    <div class="flex items-baseline justify-between">
                        <span class="text-amber-400 font-black text-sm sm:text-base font-mono">${{formatCurrency(item.precio)}}</span>
                        ${{item.original && item.original > item.precio ? `<span class="text-slate-500 line-through text-[10px] font-mono">$${{item.original.toFixed(2)}}</span>` : ''}}
                    </div>
                    <button onclick="addToCart('${{item.sku}}')" class="w-full bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black py-2 rounded-xl text-xs flex items-center justify-center gap-1.5 transition active:scale-95 shadow-md shadow-amber-500/20 cursor-pointer">
                        <i class="fa-solid fa-cart-plus"></i> Agregar al carrito
                    </button>
                </div>
            </div>
        `).join('');
    }}

    function filterByDept(dept, btn) {{
        document.querySelectorAll('.dept-btn').forEach(b => {{
            b.className = "dept-btn w-full text-left px-3 py-2 rounded-xl text-xs font-bold text-slate-300 hover:text-white hover:bg-slate-900 border border-transparent transition flex items-center justify-between cursor-pointer";
        }});
        if (btn) {{
            btn.className = "dept-btn w-full text-left px-3 py-2 rounded-xl text-xs font-bold transition flex items-center justify-between bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 cursor-pointer";
        }}

        if (dept === 'todos') {{
            currentFilteredCatalog = [...viamxCatalog];
        }} else {{
            currentFilteredCatalog = viamxCatalog.filter(i => i.categoria === dept);
        }}
        renderCatalog(currentFilteredCatalog);
    }}

    function handleSearch(q) {{
        const input = document.getElementById("siteSearch");
        if (input) input.value = q;
        handleSearchSubmit();
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
            alert(`"${{item.nombre}}" agregado al carrito.`);
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

print("✓ index.html configurado con 8 columnas, 30 departamentos con flyout y 5 columnas de productos.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(catalog): grid estricto de 8 columnas con 30 departamentos flyout y 5 columnas de productos tipo Amazon", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(viamx): grid simetrico 8 columnas, 30 departamentos con hover flyout y 5 cols de articulos", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
