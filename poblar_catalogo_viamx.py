import os
import json
import subprocess

BASE_DIR = r"E:\sitios web"
VIAMX_DIR = os.path.join(BASE_DIR, "bazar-viamx-nfl.gdl")

if not os.path.exists(VIAMX_DIR):
    alt = os.path.join(BASE_DIR, "bazar-viamx-NFL.GDL")
    if os.path.exists(alt):
        VIAMX_DIR = alt

CATALOG_PATH = os.path.join(VIAMX_DIR, "catalog.json")

print("=" * 70)
print("POBLANDO CATÁLOGO OFICIAL DE VÍA MX CON LOS 20 ARTÍCULOS DE ELECTRÓNICA")
print("=" * 70)

productos_viamx = [
    {
        "sku": "VMX-EL-001",
        "nombre": "Sony Audífonos Inalámbricos On-Ear WH-CH520 (Hasta 50h de Batería)",
        "precio": 699.00,
        "categoria": "audio",
        "descripcion": "Audífonos inalámbricos de diadema Bluetooth con hasta 50 horas de autonomía, carga rápida y conexión multipunto.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-002",
        "nombre": "Amazon Echo Pop Bocina Inteligente con Alexa (Negro)",
        "precio": 999.00,
        "categoria": "smart-home",
        "descripcion": "Bocina inteligente compacta de sonido envolvente con asistente virtual Alexa integrado para control del hogar.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-003",
        "nombre": "1 Hora Bocina Bluetooth Portátil 5W (Radio FM / MicroSD)",
        "precio": 141.99,
        "categoria": "audio",
        "descripcion": "Mini bocina inalámbrica de 5W con 25 horas de reproducción continua, radio FM y ranura para tarjeta MicroSD.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-HR-004",
        "nombre": "Juego de Destornilladores de Precisión 117 en 1 AXIDUN",
        "precio": 149.00,
        "categoria": "herramientas",
        "descripcion": "Kit magnético profesional de puntas intercambiables para reparación y mantenimiento de electrónicos y celulares.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-005",
        "nombre": "INIU Power Bank 20000mAh 22.5W Carga Rápida Portátil",
        "precio": 599.99,
        "categoria": "energia",
        "descripcion": "Batería externa de alta capacidad con display digital LED y puertos USB-C de entrega de energía rápida.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-006",
        "nombre": "Amazon Echo Dot (5ta Gen) Bocina Inteligente con Alexa (Negro)",
        "precio": 1699.00,
        "categoria": "smart-home",
        "descripcion": "Bocina inteligente con audio de alta fidelidad, voces más nítidas y control de dispositivos inteligentes.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-007",
        "nombre": "Amazon Echo Pop Bocina Inteligente con Alexa (Lavanda)",
        "precio": 999.00,
        "categoria": "smart-home",
        "descripcion": "Altavoz compacto con sonido direccional en elegante color lavanda con Alexa integrada.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-008",
        "nombre": "Skullcandy Dime 3 Auriculares In-Ear Inalámbricos (20h Batería)",
        "precio": 447.00,
        "categoria": "audio",
        "descripcion": "Auriculares True Wireless compactos con micrófono integrado, resistencia al agua IPX4 y emparejamiento rápido.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-009",
        "nombre": "Soundcore by Anker V20i Audífonos de Oído Abierto (Open-Ear)",
        "precio": 498.98,
        "categoria": "audio",
        "descripcion": "Audífonos de diseño ergonómico de oído abierto con sonido nítido y ajuste cómodo para jornadas prolongadas.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-010",
        "nombre": "Soundcore by Anker P30i Audífonos con Cancelación de Ruido",
        "precio": 537.98,
        "categoria": "audio",
        "descripcion": "Auriculares inalámbricos con cancelación activa de ruido híbrida, graves potentes y estuche con soporte para teléfono.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-011",
        "nombre": "AXIDUN Barra de Sonido RGB Estéreo Bluetooth 5.0 para PC / TV",
        "precio": 298.00,
        "categoria": "audio",
        "descripcion": "Soundbar para escritorio con iluminación dinámica RGB, conexión Bluetooth 5.0 y entrada auxiliar 3.5mm.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-HR-012",
        "nombre": "Kit de Soldadura Electrónica 80W LCD con Temperatura Regulable",
        "precio": 349.99,
        "categoria": "herramientas",
        "descripcion": "Cautín profesional de 80W (180°C - 520°C) con display digital LCD, switch de encendido y puntas de repuesto.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-013",
        "nombre": "ISTENTINFY Kit de Electrónica Protoboard Compatible con Arduino Uno",
        "precio": 262.24,
        "categoria": "maker",
        "descripcion": "Set para desarrollo y prototipado con protoboard, cables jumper, LEDs, resistencias y botones.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-014",
        "nombre": "JBL Tune 520BT Audífonos Inalámbricos Diadema Pure Bass (Negro)",
        "precio": 699.00,
        "categoria": "audio",
        "descripcion": "Audífonos Bluetooth con sonido JBL Pure Bass, hasta 57 horas de batería y micrófono para llamadas claras.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-015",
        "nombre": "FANDBO Multicontacto Extensión 12 en 1 (8 Salidas CA + USB-C / USB)",
        "precio": 263.11,
        "categoria": "energia",
        "descripcion": "Estación de energía con protección contra sobretensiones, cable de 1.5m y puertos de carga rápida USB.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-016",
        "nombre": "Amazon Echo Pop Bocina Inteligente con Alexa (Blanco)",
        "precio": 999.00,
        "categoria": "smart-home",
        "descripcion": "Bocina inteligente compacta en acabado blanco con asistente virtual Alexa y audio HD en streaming.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-017",
        "nombre": "Uplayteck Antena de TV Digital Interior HDTV 1080P / 4K Amplificada",
        "precio": 220.15,
        "categoria": "video",
        "descripcion": "Antena para sintonización de canales de televisión abierta en alta definición 1080P/4K con amplificador de señal.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-018",
        "nombre": "Motorola Moto G06 Azul (4GB RAM / 256GB) Celular Desbloqueado",
        "precio": 2368.00,
        "categoria": "telefonia",
        "descripcion": "Smartphone desbloqueado con 256GB de almacenamiento interno, 4GB RAM y batería de larga duración.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-019",
        "nombre": "Kit de Electrónica Compatible con Arduino R3 Versión Mejorada",
        "precio": 544.00,
        "categoria": "maker",
        "descripcion": "Kit de componentes y módulos de aprendizaje para robótica y proyectos con microcontrolador R3.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    },
    {
        "sku": "VMX-EL-020",
        "nombre": "Qiilu Altavoces Estéreo USB de Escritorio Liquidación",
        "precio": 209.00,
        "categoria": "audio",
        "descripcion": "Par de bocinas compactas para computadora y laptop con conector de audio 3.5mm y alimentación por puerto USB.",
        "imagen": "assets/img/mascota_tigre_thumb.webp"
    }
]

with open(CATALOG_PATH, "w", encoding="utf-8") as f:
    json.dump(productos_viamx, f, indent=4, ensure_ascii=False)

print(f"✓ {len(productos_viamx)} productos registrados con éxito en {CATALOG_PATH}")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(catalog): 20 productos de electronica y curaduria cargados en Viamx", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(viamx): 20 productos en catalog.json listos para venta y carrito", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
