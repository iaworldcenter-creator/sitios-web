import os
import subprocess
import json
import urllib.parse

BASE_DIR = r"E:\sitios web"
APP_URL = "https://iaworldcenter-creator.github.io/sitios-web/app.html"

print("=" * 80)
print("ACTUALIZANDO: TEXTOS PERSUASIVOS DEL QR + SWIPE HORIZONTAL FORZADO EN TODOS LOS SITIOS")
print("=" * 80)

# Barra de navegación deslizable en móvil
NAV_BAR_MOBILE_SWIPE = """
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

# Módulo Persuasivo del Código QR con Doble Línea y Publicidad Directa
QR_PROMO_BLOCK = f"""
                <div class="mt-4 p-4 bg-slate-950 border-2 border-cyan-400 rounded-3xl shadow-[0_0_25px_rgba(6,182,212,0.25)] text-center space-y-3">
                    <div class="flex items-center justify-center gap-2">
                        <i class="fa-solid fa-mobile-screen text-cyan-400 text-lg"></i>
                        <span class="text-xs font-mono font-black text-white uppercase tracking-wider">App Móvil Pedidos Rápidos</span>
                    </div>

                    <div class="w-44 h-44 mx-auto bg-white p-2.5 rounded-2xl shadow-xl flex items-center justify-center">
                        <img 
                            src="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(APP_URL)}&margin=1" 
                            alt="Código QR App BAZAR NFL" 
                            class="w-full h-full object-contain rounded-lg"
                            onerror="this.onerror=null; this.src='https://quickchart.io/qr?text={urllib.parse.quote(APP_URL)}&size=300';"
                        />
                    </div>

                    <div class="space-y-1">
                        <strong class="text-xs text-amber-400 block font-bold uppercase">Entrega Directa a tu Domicilio</strong>
                        <p class="text-[11px] text-slate-300 leading-snug">
                            Utiliza nuestra App oficial para que tus compras lleguen volando a la puerta de tu casa o taller.
                        </p>
                    </div>

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

# Catálogos de las 7 Boutiques con soporte de Swipe Horizontal forzado
boutiques_data = {
    "pc-custom-lab": {
        "folder_pattern": "pc-custom-lab",
        "title": "PC Custom Lab | Hardware, GPUs & Ensambles IA 2026",
        "name": "PC CUSTOM LAB",
        "tag": "TECNOLOGÍA & GAMING",
        "subtitle": "Pedro Moreno 501 A • Hardware de Alto Rendimiento, GPUs & Ensambles IA",
        "color": "text-cyan-400",
        "categories": [
            {"name": "Tarjetas de Video RTX & Radeon", "icon": "fa-microchip"},
            {"name": "Procesadores Intel & AMD Ryzen", "icon": "fa-bolt"},
            {"name": "Tarjetas Madre LGA1700 & AM5", "icon": "fa-server"},
            {"name": "Memorias RAM DDR5 & DDR4", "icon": "fa-memory"},
            {"name": "Discos SSD M.2 NVMe PCIe 4.0", "icon": "fa-hard-drive"},
            {"name": "Gabinetes & Fuentes Modulares", "icon": "fa-cube"}
        ],
        "products": [
            {"sku": "PC-001", "nombre": "Gabinete Micro-ATX con Fuente 500W Incluida", "marca": "Acteck", "precio": 1250.00, "original": 1550.00, "desc": "Chasis esbelto con fuente certificada, puertos USB 3.0 frontales y bahías SSD.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/gabinete_negro.webp", "tokens": ["gabinete", "fuente", "pc", "chasis"]},
            {"sku": "PC-002", "nombre": "Tarjeta Madre ASUS Prime B760M-A WiFi DDR5", "marca": "ASUS", "precio": 3400.00, "original": 3950.00, "desc": "Placa base con soporte Intel Core 12va/13va/14va Gen y dual M.2 PCIe 4.0.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/motherboard_asus.webp", "tokens": ["tarjeta madre", "motherboard", "asus", "placa"]},
            {"sku": "PC-003", "nombre": "Procesador Intel Core i5-14400F 10C/16T con Disipador", "marca": "Intel", "precio": 4350.00, "original": 4990.00, "desc": "10 núcleos híbridos de alto rendimiento con disipador silencioso de fábrica.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/cpu_intel_ultra.webp", "tokens": ["procesador", "cpu", "intel", "i5"]},
            {"sku": "PC-004", "nombre": "Memoria RAM Kingston FURY Beast 16GB DDR5 5600MHz", "marca": "Kingston", "precio": 1250.00, "original": 1500.00, "desc": "Módulo DDR5 de alta velocidad con disipador térmico de aluminio negro.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/ram_caja.webp", "tokens": ["ram", "kingston", "fury", "ddr5", "memoria"]},
            {"sku": "PC-005", "nombre": "Disco Sólido SSD Kingston NV2 1TB NVMe PCIe 4.0", "marca": "Kingston", "precio": 1350.00, "original": 1650.00, "desc": "3,500 MB/s de lectura secuencial para carga instantánea del sistema.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/disco_solido_m2.webp", "tokens": ["ssd", "kingston", "nvme", "disco", "m2"]},
            {"sku": "PC-006", "nombre": "Tarjeta Gráfica NVIDIA RTX 4070 Ti Super 16GB", "marca": "NVIDIA", "precio": 17800.00, "original": 21500.00, "desc": "DLSS 3, Ray Tracing y 16GB GDDR6X para gaming y renderizado 4K.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/gpu_nvidia.webp", "tokens": ["gpu", "nvidia", "rtx", "4070", "grafica"]}
        ]
    },
    "bazar-viamx-nfl.gdl": {
        "folder_pattern": "bazar-viamx",
        "title": "Vía MX Boutique | Curaduría Departamental 2026",
        "name": "VÍA MX BOUTIQUE",
        "tag": "DEPARTAMENTAL & B2B",
        "subtitle": "Pedro Moreno 501 A • 30 Departamentos, Electrónica, Hogar & B2B",
        "color": "text-cyan-300",
        "categories": [
            {"name": "Pantallas Smart TV & Audio HD", "icon": "fa-tv"},
            {"name": "Refrigeradores & Línea Blanca", "icon": "fa-snowflake"},
            {"name": "Laptops & Computación Slim", "icon": "fa-laptop"},
            {"name": "Telefonía 5G & Celulares", "icon": "fa-mobile-screen"},
            {"name": "Electrodomésticos & Cocina", "icon": "fa-kitchen-set"},
            {"name": "Ropa NFL & Moda Internacional", "icon": "fa-shirt"}
        ],
        "products": [
            {"sku": "VMX-001", "nombre": "Pantalla Smart TV 55 Pulgadas 4K UHD HDR10+ WiFi", "marca": "Samsung", "precio": 7999.00, "original": 11499.00, "desc": "Panel LED 4K ultra nítido con asistente de voz y 4 puertos HDMI 2.1.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_curvo_negro.webp", "tokens": ["pantalla", "smart tv", "samsung", "4k"]},
            {"sku": "VMX-002", "nombre": "Refrigerador Inverter No Frost 14 Pies Cúbicos Acero", "marca": "LG", "precio": 11899.00, "original": 15999.00, "desc": "Doble puerta con compresor Digital Inverter de bajo consumo y despachador.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_warehouse_thumb.webp", "tokens": ["refrigerador", "lg", "linea blanca", "inverter"]},
            {"sku": "VMX-003", "nombre": "Freidora de Aire Digital 6.5 Litros con 12 Programas", "marca": "Tefal", "precio": 1499.00, "original": 2199.00, "desc": "Canastilla antiadherente libre de BPA con calor envolvente 360 grados.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp", "tokens": ["freidora", "aire", "airfryer", "tefal"]},
            {"sku": "VMX-004", "nombre": "Laptop Ultra Slim 15.6 Pulgadas Core i7 16GB RAM 512GB", "marca": "Lenovo", "precio": 14500.00, "original": 18900.00, "desc": "Chasis de aluminio ligero, teclado retroiluminado y lector de huella.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_mantenimiento_thumb.webp", "tokens": ["laptop", "lenovo", "core i7", "computadora"]},
            {"sku": "VMX-005", "nombre": "Smartphone 5G Desbloqueado 256GB / 8GB RAM 108MP", "marca": "Motorola", "precio": 4899.00, "original": 6499.00, "desc": "Pantalla AMOLED 120Hz con batería de 5000mAh y carga turbo rápida.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/perifericos_combo_1.webp", "tokens": ["celular", "telefono", "smartphone", "motorola"]}
        ]
    },
    "cigarros-bazar": {
        "folder_pattern": "cigarros-bazar",
        "title": "Cigarros Bazar | Puros Habanos & Tabacos Selectos 2026",
        "name": "CIGARROS BAZAR",
        "tag": "TABACOS & HABANOS",
        "subtitle": "Pedro Moreno 501 A • Cigarros Premium, Puros Habanos & Accesorios",
        "color": "text-amber-400",
        "categories": [
            {"name": "Cigarros Nacionales & Importación", "icon": "fa-smoking"},
            {"name": "Puros Habanos Cubanos Hechos a Mano", "icon": "fa-gem"},
            {"name": "Tabaco para Liar & Filtros Especiales", "icon": "fa-leaf"},
            {"name": "Encendedores Recargables & Antorchas", "icon": "fa-fire"}
        ],
        "products": [
            {"sku": "CIG-001", "nombre": "Cigarros Marlboro Gold Original (Cajetilla 20)", "marca": "Marlboro", "precio": 82.00, "original": 95.00, "desc": "Sabor suave y filtro blanco balanceado de importación nacional.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", "tokens": ["cigarros", "marlboro", "gold", "tabaco"]},
            {"sku": "CIG-002", "nombre": "Cigarros Benson & Hedges Black Switch (Cajetilla 20)", "marca": "Benson & Hedges", "precio": 88.00, "original": 105.00, "desc": "Cápsula de sabor mentolado premium con tabaco curado de alta calidad.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", "tokens": ["cigarros", "benson", "hedges", "mentolados"]},
            {"sku": "CIG-003", "nombre": "Puro Habanos Cohiba Siglo VI Tubo Individual", "marca": "Cohiba", "precio": 850.00, "original": 1100.00, "desc": "Puro cubano hecho a mano con notas amaderadas y especiadas.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", "tokens": ["puro", "cohiba", "siglo vi", "habano"]},
            {"sku": "CIG-004", "nombre": "Puro Romeo y Julieta Churchill en Tubo Aluminio", "marca": "Romeo y Julieta", "precio": 620.00, "original": 790.00, "desc": "Vitola clásica Churchill de fortaleza media con tiro excelente.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", "tokens": ["puro", "romeo y julieta", "churchill"]},
            {"sku": "CIG-005", "nombre": "Encendedor de Colección Vintage a Gas Recargable", "marca": "Clipper Pro", "precio": 195.00, "original": 260.00, "desc": "Cuerpo metálico cepillado con piedra intercambiable y válvula.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", "tokens": ["encendedor", "clipper", "fuego", "gas"]}
        ]
    },
    "dulces-bazar": {
        "folder_pattern": "dulces-bazar",
        "title": "Dulces Bazar | Confitería Mexicana & Mayoreo 2026",
        "name": "DULCES BAZAR",
        "tag": "CONFITERÍA & BOTANAS",
        "subtitle": "Pedro Moreno 501 A • Paletas, Chocolates Finos, Mazapanes & Botanas",
        "color": "text-pink-400",
        "categories": [
            {"name": "Paletas & Malvaviscos Tradicionales", "icon": "fa-candy-cane"},
            {"name": "Mazapanes & Dulces de Cacahuate", "icon": "fa-cookie"},
            {"name": "Caramelos Macizos con Chile & Ácidos", "icon": "fa-pepper-hot"}
        ],
        "products": [
            {"sku": "DUL-001", "nombre": "Paleta Payaso Ricolino (Caja con 15 piezas)", "marca": "Ricolino", "precio": 245.00, "original": 290.00, "desc": "Malvavisco cubierto de chocolate con gomitas de colores tradicionales.", "img": "assets/img/mascota_tigre_thumb.webp", "tokens": ["paleta", "payaso", "ricolino", "dulces"]},
            {"sku": "DUL-002", "nombre": "Mazapán De La Rosa Gigante (Caja con 20 piezas)", "marca": "De La Rosa", "precio": 160.00, "original": 195.00, "desc": "El dulce tradicional mexicano de cacahuate tostado seleccionado.", "img": "assets/img/mascota_tigre_thumb.webp", "tokens": ["mazapan", "de la rosa", "cacahuate"]},
            {"sku": "DUL-003", "nombre": "Rocaleta Sonrics con Centro de Goma (Bolsa 30)", "marca": "Sonrics", "precio": 185.00, "original": 230.00, "desc": "Caramelo con 4 capas de chile ácido y centro de chicle masticable.", "img": "assets/img/mascota_tigre_thumb.webp", "tokens": ["rocaleta", "sonrics", "chile", "paleta"]},
            {"sku": "DUL-004", "nombre": "Chocolates Finos Surtidos Artesanales Caja Regalo", "marca": "Turín", "precio": 220.00, "original": 280.00, "desc": "Bombones semiamargos rellenos de licor y crema de avellana.", "img": "assets/img/mascota_tigre_thumb.webp", "tokens": ["chocolate", "turin", "bombones"]}
        ]
    },
    "kiosco-digital": {
        "folder_pattern": "kiosco-digital",
        "title": "Kiosco Digital | Revistas, Prensa & Suscripciones 2026",
        "name": "KIOSCO DIGITAL",
        "tag": "LECTURA & CULTURA",
        "subtitle": "Pedro Moreno 501 A • Suscripciones Digitales, Revistas HD & Prensa",
        "color": "text-indigo-400",
        "categories": [
            {"name": "Revistas de Ciencia, Naturaleza & Espacio", "icon": "fa-atom"},
            {"name": "Divulgación Científica & Curiosidades", "icon": "fa-brain"},
            {"name": "Prensa Matutina & Periódicos de GDL", "icon": "fa-newspaper"}
        ],
        "products": [
            {"sku": "KIO-001", "nombre": "Suscripción Digital Anual Revista National Geographic", "marca": "RBA", "precio": 599.00, "original": 850.00, "desc": "12 ediciones digitales en alta definición + acceso al archivo fotográfico.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_plano_blanco.webp", "tokens": ["revista", "national geographic", "natgeo", "digital"]},
            {"sku": "KIO-002", "nombre": "Suscripción Digital Revista Muy Interesante (1 Año)", "marca": "Zinet", "precio": 450.00, "original": 620.00, "desc": "Acceso total multidispositivo a reportajes de ciencia, historia e innovación.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_plano_blanco.webp", "tokens": ["revista", "muy interesante", "ciencia"]},
            {"sku": "KIO-003", "nombre": "Suscripción Revista Conozca Más Digital Colección", "marca": "Editorial Televisa", "precio": 380.00, "original": 490.00, "desc": "Enciclopedia de curiosidades científicas, enigmas y avances médicos.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_plano_blanco.webp", "tokens": ["revista", "conozca mas", "cultura"]}
        ]
    },
    "mi-puesto-bazar": {
        "folder_pattern": "mi-puesto-bazar",
        "title": "Mi Puesto Bazar | Novedades, Gadgets & Conveniencia 2026",
        "name": "MI PUESTO BAZAR",
        "tag": "NOVEDADES & GADGETS",
        "subtitle": "Pedro Moreno 501 A • Lentes Inteligentes, Consolas Retro & Cables",
        "color": "text-emerald-400",
        "categories": [
            {"name": "Lentes Inteligentes Bluetooth & Audio", "icon": "fa-glasses"},
            {"name": "Consolas Retro Portátiles & Arcade", "icon": "fa-gamepad"},
            {"name": "Cables USB-C, Cargadores & Hubs", "icon": "fa-plug"}
        ],
        "products": [
            {"sku": "PUE-001", "nombre": "Lentes Inteligentes Bluetooth con Audio y Micrófono", "marca": "SmartVision", "precio": 680.00, "original": 950.00, "desc": "Contesta llamadas, sube/baja volumen y escucha música con protección UV.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_gamer_thumb.webp", "tokens": ["lentes", "inteligentes", "bluetooth", "audio"]},
            {"sku": "PUE-002", "nombre": "Consola Retro Portátil con 500 Juegos Clásicos", "marca": "Sup Game", "precio": 290.00, "original": 390.00, "desc": "Batería recargable y salida para conectar a la televisión con cable AV.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_gemini_thumb.webp", "tokens": ["consola", "retro", "videojuegos", "juegos"]},
            {"sku": "PUE-003", "nombre": "Cable de Carga Rápida USB-C a USB-C de 65W Reforzado", "marca": "Baseus", "precio": 120.00, "original": 180.00, "desc": "Cable trenzado de nailon de 2 metros compatible con celulares y laptops.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/fuente_modular.webp", "tokens": ["cable", "cargador", "usb c", "carga rapida"]}
        ]
    },
    "ofertas-y-liquidaciones": {
        "folder_pattern": "ofertas-y-liquidaciones",
        "title": "Ofertas & Liquidaciones | Outlet Directo B2B 2026",
        "name": "OFERTAS & LIQUIDACIONES",
        "tag": "OUTLET & REMATES",
        "subtitle": "Pedro Moreno 501 A • Remates de Bodega, Excedentes & Lotes con 50% Dto",
        "color": "text-red-400",
        "categories": [
            {"name": "Lotes de Remate Electrónica & B2B", "icon": "fa-layer-group"},
            {"name": "Monitores & Pantallas de Exhibición", "icon": "fa-display"},
            {"name": "Herramientas al Costo en Maletín", "icon": "fa-toolbox"}
        ],
        "products": [
            {"sku": "OFE-001", "nombre": "Lote de Remate Electrónica y Accesorios Varios Grado A", "marca": "Sony / Varios", "precio": 2490.00, "original": 3800.00, "desc": "Paquete surtido de oportunidad comercial con garantía y respaldo.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/software_estante_madera.webp", "tokens": ["lote", "remate", "liquidacion", "oferta"]},
            {"sku": "OFE-002", "nombre": "Monitor Curvo 24 Pulgadas 144Hz Full HD de Exhibición", "marca": "AOC", "precio": 2100.00, "original": 3200.00, "desc": "Equipo de vitrina estética 10/10 con caja original y cables.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_curvo_negro.webp", "tokens": ["monitor", "curvo", "aoc", "144hz"]},
            {"sku": "OFE-003", "nombre": "Kit de Herramientas Mecánicas 168 Piezas en Maletín", "marca": "Stanley", "precio": 899.00, "original": 1299.00, "desc": "Últimas piezas de importación con matraca y dados milimétricos.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/software_estante_muro.webp", "tokens": ["herramientas", "stanley", "maletin"]}
        ]
    }
}

def generate_boutique_html(data):
    js_products = json.dumps(data["products"], ensure_ascii=False)
    js_categories = json.dumps(data["categories"], ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{data["title"]}</title>
    <meta name="description" content="{data["subtitle"]}" />
    
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
                <span class="text-slate-300 hidden xl:inline text-[11px] font-semibold">Guadalajara Centro • Carrito Unificado</span>
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
                    <img src="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" alt="Logo Tigre {data["name"]}" class="w-12 h-12 rounded-full object-cover border-2 border-amber-400 shadow-[0_0_15px_rgba(251,191,36,0.5)]" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';" />
                </div>
                <div class="flex flex-col">
                    <span class="font-black text-2xl text-white tracking-wider uppercase leading-none">{data["name"]}</span>
                    <span class="text-[11px] font-mono {data["color"]} uppercase tracking-tight mt-1 flex items-center gap-1 hover:underline">
                        <i class="fa-solid fa-location-dot text-amber-400"></i> Pedro Moreno 501 A, Guadalajara Centro
                    </span>
                </div>
            </div>

            <div class="flex-1 max-w-3xl w-full relative">
                <div class="flex items-center bg-white rounded-full border-2 border-cyan-400 shadow-[0_0_22px_rgba(6,182,212,0.4)] px-4 py-1.5 gap-2">
                    <i class="fa-solid fa-magnifying-glass text-slate-400 text-sm"></i>
                    <input type="text" id="boutiqueSearchInput" autocomplete="off" spellcheck="false" placeholder="Busca en {data['name']} (ej. por producto, SKU, síntoma o marca)..." class="flex-1 bg-transparent border-0 outline-none text-slate-950 font-bold text-sm placeholder-slate-400" oninput="onBoutiqueSearch(event)" />
                    <button onclick="clearBoutiqueSearch()" id="clear-search-btn" class="hidden text-slate-400 hover:text-slate-600 text-xs px-2 font-bold cursor-pointer"><i class="fa-solid fa-xmark"></i></button>
                    <button onclick="executeBoutiqueSearch()" class="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black px-6 py-2 rounded-full text-xs uppercase tracking-wider transition active:scale-95 shrink-0 shadow cursor-pointer">BUSCAR</button>
                </div>
                <div id="boutique-autocomplete-box" class="hidden absolute top-full left-0 right-0 mt-2 bg-slate-900 border-2 border-cyan-500/60 rounded-2xl shadow-2xl z-50 p-2.5 flex flex-col gap-2 max-h-96 overflow-y-auto no-scrollbar"></div>
            </div>

            <button onclick="toggleCartDrawer()" class="flex items-center gap-3 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white px-4 py-2.5 rounded-xl transition cursor-pointer active:scale-95 shadow shrink-0 group">
                <div class="relative">
                    <i class="fa-solid fa-cart-shopping text-cyan-400 text-base group-hover:scale-110 transition"></i>
                    <span id="boutique-cart-badge" class="absolute -top-2.5 -right-2.5 bg-amber-500 text-slate-950 font-mono font-black text-[10px] rounded-full w-5 h-5 flex items-center justify-center shadow">0</span>
                </div>
                <div class="flex flex-col text-left">
                    <span class="text-[10px] font-mono text-slate-400 uppercase leading-none">Canasta Global</span>
                    <span id="boutique-cart-total" class="text-xs font-mono font-bold text-amber-400">$0.00 MXN</span>
                </div>
            </button>
        </div>
    </header>

    <main class="w-full max-w-[99%] 2xl:max-w-[1850px] mx-auto px-2 sm:px-4 py-8 flex-1">
        <div class="flex flex-col lg:flex-row gap-8 items-start justify-center">
            
            <aside class="w-full lg:w-[340px] xl:w-[370px] shrink-0 bg-slate-900/90 rounded-3xl p-5 shadow-2xl relative" id="boutique-sidebar-root">
                <div class="flex items-center justify-between border-b border-slate-800 pb-3.5 mb-3.5">
                    <h3 class="font-mono text-sm font-black text-white uppercase tracking-wider flex items-center gap-2 truncate">
                        <i class="fa-solid fa-layer-group text-amber-400"></i> Departamentos
                    </h3>
                </div>
                <div class="mb-3.5">
                    <span class="text-[10px] font-mono text-cyan-400 font-bold bg-cyan-950/40 border border-cyan-500/30 px-3 py-1 rounded-xl block text-center uppercase tracking-widest">
                        Compras Rápidas
                    </span>
                </div>

                <nav class="flex flex-col gap-2" id="sidebar-categories-list"></nav>

                <!-- UN SOLO CÓDIGO QR CON TEXTOS PERSUASIVOS -->
                {QR_PROMO_BLOCK}

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
                        <p class="text-[11px] text-slate-300 leading-snug">Desarrollado, optimizado y desplegado por Anti-Gravity Copilot.</p>
                        <a href="https://antigravity.google/download" target="_blank" class="w-full bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black py-2 rounded-xl text-xs text-center uppercase tracking-wider transition active:scale-95 shadow">Bajar Anti-Gravity Gratis</a>
                    </div>
                </div>
            </aside>

            <!-- CONTENEDOR DE PRODUCTOS CON SWIPE HORIZONTAL FORZADO EN MÓVILES -->
            <section class="flex-1 w-full flex flex-col gap-6 min-w-0">
                <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                    <span class="text-xs font-mono text-cyan-400 font-bold uppercase tracking-wider" id="results-count-txt">
                        Catálogo de Entrega Inmediata
                    </span>
                    <span class="text-xs font-mono text-slate-400">Pedro Moreno 501 A</span>
                </div>

                <!-- SWIPE FORZADO: flex-row overflow-x-auto en móvil, grid en desktop -->
                <div id="products-grid-container" class="flex flex-row overflow-x-auto flex-nowrap lg:grid lg:grid-cols-5 lg:overflow-visible gap-4 pb-3 lg:pb-0 no-scrollbar snap-x snap-mandatory">
                </div>
            </section>

        </div>
    </main>

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
                    <p class="text-[11px] text-slate-400">Devoluciones en tienda dentro de las 48 horas con empaque íntegro. Soporte técnico local y reemplazo inmediato.</p>
                </div>
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2"><i class="fa-solid fa-coins text-emerald-400"></i> Ahorro y Cashback</h4>
                    <p class="text-slate-300 font-bold">5% de Cashback en cada compra de forma directa.</p>
                </div>
            </div>
            <div class="pt-8 text-center text-slate-500 text-[11px]">
                <p>&copy; 2026 {data["name"]} & Ecosistema Comercial Pedro Moreno 501 A. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>

    <script>
    const boutiqueProducts = {js_products};
    const boutiqueCategories = {js_categories};

    function renderBoutiqueSidebar() {{
        const container = document.getElementById("sidebar-categories-list");
        if (!container) return;
        container.innerHTML = boutiqueCategories.map(c => `
            <button onclick="filterCategory('${{c.name}}')" class="w-full text-left p-3.5 rounded-2xl bg-slate-950/70 hover:bg-slate-800/90 shadow-md flex justify-between items-center transition group cursor-pointer">
                <div class="flex items-center gap-3.5 min-w-0">
                    <div class="w-8 h-8 rounded-xl bg-slate-900 flex items-center justify-center {data["color"]} shrink-0 shadow"><i class="fa-solid ${{c.icon}} text-sm"></i></div>
                    <strong class="text-white text-xs block group-hover:text-cyan-300 truncate font-bold">${{c.name}}</strong>
                </div>
                <i class="fa-solid fa-chevron-right text-[10px] text-slate-600 group-hover:{data["color"]} transition group-hover:translate-x-0.5 shrink-0 ml-2"></i>
            </button>
        `).join('');
    }}

    function renderBoutiqueGrid(items = boutiqueProducts) {{
        const container = document.getElementById("products-grid-container");
        const countTxt = document.getElementById("results-count-txt");
        if (countTxt) countTxt.innerText = `Mostrando ${{items.length}} artículos de entrega inmediata`;
        if (!container) return;

        container.innerHTML = items.map(p => {{
            const discountPct = p.original ? Math.round((1 - (p.precio / p.original)) * 100) : 0;
            return `
                <div class="min-w-[240px] w-[240px] sm:w-[260px] lg:w-auto shrink-0 snap-start bg-slate-950/90 hover:bg-slate-950 rounded-2xl p-3.5 flex flex-col justify-between transition group shadow-xl hover:shadow-[0_8px_30px_rgba(6,182,212,0.2)]">
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
        }}).join('');
    }}

    function filterCategory(catName) {{
        const filtered = boutiqueProducts.filter(p => p.nombre.toLowerCase().includes(catName.toLowerCase()) || p.desc.toLowerCase().includes(catName.toLowerCase()));
        renderBoutiqueGrid(filtered.length > 0 ? filtered : boutiqueProducts);
    }}

    function onBoutiqueSearch(e) {{
        const q = e.target.value.toLowerCase().trim();
        const clearBtn = document.getElementById("clear-search-btn");
        if (clearBtn) clearBtn.classList.toggle("hidden", q.length === 0);
        const filtered = boutiqueProducts.filter(p => {{
            const searchStr = `${{p.sku}} ${{p.nombre}} ${{p.marca}} ${{p.desc}} ${{ (p.tokens || []).join(' ') }}`.toLowerCase();
            return searchStr.includes(q);
        }});
        renderBoutiqueAutocomplete(q, filtered);
        renderBoutiqueGrid(q ? filtered : boutiqueProducts);
    }}

    function renderBoutiqueAutocomplete(val, matches) {{
        const box = document.getElementById("boutique-autocomplete-box");
        if (!val || val.length < 1) {{
            box.classList.add("hidden");
            return;
        }}
        if (matches.length === 0) {{
            box.innerHTML = `<div class="p-3 text-center text-slate-400 text-xs">No hay coincidencias para "${{val}}"</div>`;
            box.classList.remove("hidden");
            return;
        }}
        box.innerHTML = matches.slice(0, 5).map(item => `
            <div class="bg-slate-950 rounded-xl p-3 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 transition shadow border border-slate-800/80">
                <div class="flex items-center gap-2.5 min-w-0 flex-1">
                    <img src="${{item.img}}" alt="${{item.nombre}}" class="w-10 h-10 object-contain rounded-lg bg-slate-900 p-0.5 shrink-0" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';"/>
                    <div class="min-w-0">
                        <span class="text-[9px] font-mono text-cyan-400 font-bold block">${{item.sku}} &bull; ${{item.marca}}</span>
                        <h5 class="text-xs font-bold text-white truncate">${{item.nombre}}</h5>
                        <div class="flex items-center gap-2 mt-0.5">
                            <span class="text-amber-400 font-mono font-bold text-xs">$${{item.precio.toFixed(2)}} MXN</span>
                            ${{item.original ? `<span class="text-[10px] font-mono text-red-400 line-through">$${{item.original.toFixed(2)}}</span>` : ''}}
                        </div>
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

    function clearBoutiqueSearch() {{
        const input = document.getElementById("boutiqueSearchInput");
        input.value = '';
        document.getElementById("clear-search-btn").classList.add("hidden");
        document.getElementById("boutique-autocomplete-box").classList.add("hidden");
        renderBoutiqueGrid(boutiqueProducts);
    }}

    function executeBoutiqueSearch() {{
        const input = document.getElementById("boutiqueSearchInput");
        document.getElementById("boutique-autocomplete-box").classList.add("hidden");
    }}

    function addToCartDirect(sku, qty = 1) {{
        const item = boutiqueProducts.find(p => p.sku === sku);
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
        syncBoutiqueCart();
        const badge = document.getElementById("boutique-cart-badge");
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

    function syncBoutiqueCart() {{
        let cartStorage = [];
        try {{
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cartStorage = JSON.parse(raw);
        }} catch(e) {{}}
        const totalCount = cartStorage.reduce((sum, i) => sum + (parseInt(i.quantity) || 0), 0);
        const totalMoney = cartStorage.reduce((sum, i) => sum + ((parseFloat(i.precio) || 0) * (parseInt(i.quantity) || 0)), 0);
        const badge = document.getElementById("boutique-cart-badge");
        const totalTxt = document.getElementById("boutique-cart-total");
        if (badge) badge.innerText = totalCount;
        if (totalTxt) totalTxt.innerText = `$${{totalMoney.toLocaleString('es-MX', {{ minimumFractionDigits: 2 }})}} MXN`;
    }}

    function toggleCartDrawer() {{
        window.location.href = "https://iaworldcenter-creator.github.io/pc-custom-lab/checkout.html";
    }}

    document.addEventListener("DOMContentLoaded", () => {{
        renderBoutiqueSidebar();
        renderBoutiqueGrid();
        syncBoutiqueCart();
    }});
    window.addEventListener("storage", syncBoutiqueCart);
    </script>
</body>
</html>
"""

# 1. Actualizar las 7 Boutiques
all_dirs = os.listdir(BASE_DIR)
for key, b_info in boutiques_data.items():
    for d in all_dirs:
        if b_info["folder_pattern"].lower() in d.lower() and os.path.isdir(os.path.join(BASE_DIR, d)):
            target_path = os.path.join(BASE_DIR, d, "index.html")
            html_content = generate_boutique_html(b_info)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"✓ Boutique {d} actualizada con Swipe Horizontal y QR persuasivo.")

            sub_repo = os.path.join(BASE_DIR, d)
            if os.path.exists(os.path.join(sub_repo, ".git")):
                subprocess.run(["git", "add", "-A"], cwd=sub_repo, check=True)
                subprocess.run(["git", "commit", "-m", f"fix(mobile): forzar swipe horizontal en productos y QR persuasivo", "--allow-empty"], cwd=sub_repo, capture_output=True)
                res = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sub_repo, capture_output=True, text=True)
                print(f"   🟢 Submódulo {d} -> Push: {'OK' if res.returncode == 0 else res.stderr.strip()}")
            break

# 2. Actualizar Portal Matriz con Swipe Forzado
for p in [os.path.join(BASE_DIR, "index.html"), os.path.join(BASE_DIR, "sitios-web", "index.html")]:
    if os.path.exists(os.path.dirname(p)):
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()

        # Reemplazar contenedor de productos por swipe horizontal forzado
        content = content.replace('flex lg:grid lg:grid-cols-5 overflow-x-auto', 'flex flex-row overflow-x-auto flex-nowrap lg:grid lg:grid-cols-5 lg:overflow-visible')
        content = content.replace('w-[240px] sm:w-[260px] lg:w-auto shrink-0', 'min-w-[240px] w-[240px] sm:w-[260px] lg:w-auto shrink-0')
        
        # Inyectar el bloque de QR persuasivo limpio
        if "<!-- TARJETA CÓDIGO QR" in content:
            start = content.find("<!-- TARJETA CÓDIGO QR")
            end = content.find("<!-- TARJETAS DE GEMINI", start)
            if end != -1:
                content = content[:start] + QR_PROMO_BLOCK.strip() + "\n\n                " + content[end:]

        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Portal Matriz actualizado con Swipe forzado y QR persuasivo: {p}")

# 3. Desplegar Monorepositorio Central
print("\n=== DESPLEGANDO A GITHUB PAGES ===")
sitios_repo = os.path.join(BASE_DIR, "sitios-web")
if os.path.exists(os.path.join(sitios_repo, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=sitios_repo, check=True)
    subprocess.run(["git", "commit", "-m", "fix(mobile): forzar swipe horizontal y textos persuasivos en QR", "--allow-empty"], cwd=sitios_repo, capture_output=True)
    res_sub = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sitios_repo, capture_output=True, text=True)
    print(f"🟢 Submódulo sitios-web -> Push: {'OK' if res_sub.returncode == 0 else res_sub.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(ecosistema): Swipe horizontal forzado y QR persuasivo desplegados en 8 portales", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
