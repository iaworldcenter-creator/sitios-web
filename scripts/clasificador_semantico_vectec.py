# -*- coding: utf-8 -*-
"""
MOTOR SEMANTICO DE CLASIFICACION UNIVERSAL VECTEC (67 DEPARTAMENTOS)
Auditoria Forense 18 Asistentes Especializados + Motor JEV (Semana 1321).
Aplica reglas positivas y negativas estrictas, limites de palabra (\b),
evaluacion diferenciada titulo/subgrupo vs descripcion y priorizacion taxonomica
para garantizar congruencia total en vitrinas y catalogo.
"""

import re

# 67 Departamentos Oficiales VECTEC en orden canonico
DEPARTAMENTOS_OFICIALES = [
    {"id": "procesadores", "name": "1. Procesadores (CPUs)", "icon": "fa-microchip", "order": 1},
    {"id": "tarjetas_madre", "name": "2. Tarjetas Madre (Motherboards)", "icon": "fa-chess-board", "order": 2},
    {"id": "memorias_ram_pc", "name": "3. Memorias RAM PC (DIMM)", "icon": "fa-memory", "order": 3},
    {"id": "gabinetes", "name": "4. Gabinetes & Chasis Gamer", "icon": "fa-server", "order": 4},
    {"id": "tarjetas_video", "name": "5. Tarjetas de Video (GPUs)", "icon": "fa-vr-cardboard", "order": 5},
    {"id": "enfriamiento", "name": "6. Sistemas de Enfriamiento Líquido & Aire", "icon": "fa-fan", "order": 6},
    {"id": "fuentes_energia", "name": "7. Fuentes de Poder Certificadas", "icon": "fa-bolt", "order": 7},
    {"id": "ssds_m2_nvme", "name": "8. Unidades SSD M.2 NVMe PCIe", "icon": "fa-hard-drive", "order": 8},
    {"id": "discos_duros_hdd_internos", "name": "9. Discos Duros Internos HDD", "icon": "fa-hard-drive", "order": 9},
    {"id": "monitores_pantallas", "name": "10. Monitores & Pantallas PC", "icon": "fa-desktop", "order": 10},
    {"id": "teclados", "name": "11. Teclados Mecánicos & Oficina", "icon": "fa-keyboard", "order": 11},
    {"id": "ratones_mouse", "name": "12. Ratones & Mouse Gamer", "icon": "fa-mouse", "order": 12},
    {"id": "combos_teclado_mouse", "name": "13. Kits de Teclado y Ratón", "icon": "fa-keyboard", "order": 13},
    {"id": "laptops_portatiles", "name": "14. Laptops & Computadoras Portátiles", "icon": "fa-laptop", "order": 14},
    {"id": "mini_pcs_nuc", "name": "15. Mini PCs Ultracompactas & NUCs", "icon": "fa-cube", "order": 15},
    {"id": "computadoras_ensambladas", "name": "16. Computadoras de Escritorio & Gaming PCs", "icon": "fa-computer", "order": 16},
    {"id": "computadoras_all_in_one", "name": "17. Computadoras All-in-One (AIO)", "icon": "fa-tv", "order": 17},
    {"id": "servidores_enterprise", "name": "18. Servidores Torre & Rack Enterprise", "icon": "fa-server", "order": 18},
    {"id": "no_breaks_ups", "name": "19. No-Breaks & Sistemas UPS", "icon": "fa-car-battery", "order": 19},
    {"id": "reguladores_voltaje", "name": "20. Reguladores de Voltaje & Supresores", "icon": "fa-bolt", "order": 20},
    {"id": "cargadores_baterias_powerbanks", "name": "21. Cargadores, Baterías & Power Banks", "icon": "fa-plug-circle-bolt", "order": 21},
    {"id": "discos_duros_externos", "name": "22. Unidades & Discos Externos (SSD & HDD)", "icon": "fa-hard-drive", "order": 22},
    {"id": "tarjetas_microsd", "name": "23. Tarjetas de Memoria MicroSD & SD", "icon": "fa-sd-card", "order": 23},
    {"id": "memorias_usb_pendrives", "name": "24. Memorias USB Flash & Pendrives", "icon": "fa-usb", "order": 24},
    {"id": "memorias_ram_laptop", "name": "25. Memorias RAM para Laptop (SODIMM)", "icon": "fa-laptop", "order": 25},
    {"id": "memorias_ram_servidor", "name": "26. Memorias RAM para Servidor (ECC)", "icon": "fa-server", "order": 26},
    {"id": "diademas_headsets", "name": "27. Diademas & Headsets Gamer", "icon": "fa-headphones", "order": 27},
    {"id": "bocinas_sonido", "name": "28. Bocinas, Barras de Sonido & Bafles", "icon": "fa-volume-high", "order": 28},
    {"id": "microfonos", "name": "29. Micrófonos para Streaming & Voz", "icon": "fa-microphone", "order": 29},
    {"id": "webcams_videoconferencia", "name": "30. Cámaras Web & Videoconferencia", "icon": "fa-camera", "order": 30},
    {"id": "proyectores_presentacion", "name": "31. Proyectores de Video & Pantallas Murales", "icon": "fa-video", "order": 31},
    {"id": "camaras_seguridad_cctv", "name": "32. Cámaras de Seguridad (IP, Bala, Domo)", "icon": "fa-video", "order": 32},
    {"id": "grabadores_dvr_nvr", "name": "33. Grabadores de Video DVR & NVR", "icon": "fa-compact-disc", "order": 33},
    {"id": "control_acceso_biometricos", "name": "34. Control de Acceso, Asistencia & Biometría", "icon": "fa-fingerprint", "order": 34},
    {"id": "alarmas_sensores_seguridad", "name": "35. Alarmas, Sensores de Intrusión & Sirenas", "icon": "fa-shield-halved", "order": 35},
    {"id": "telefonia_conmutadores", "name": "36. Conmutadores & Telefonía IP", "icon": "fa-phone", "order": 36},
    {"id": "switches_red", "name": "37. Switches Ethernet & PoE+", "icon": "fa-network-wired", "order": 37},
    {"id": "routers_access_points", "name": "38. Routers Inalámbricos & Access Points WiFi", "icon": "fa-wifi", "order": 38},
    {"id": "antenas_radioenlaces", "name": "39. Antenas de Largo Alcance & Radioenlaces", "icon": "fa-satellite-dish", "order": 39},
    {"id": "cableado_estructurado", "name": "40. Bobinas UTP, Patch Cords & Conectores RJ45", "icon": "fa-network-wired", "order": 40},
    {"id": "fibra_optica_transceivers", "name": "41. Módulos Transceivers SFP & Fibra Óptica", "icon": "fa-network-wired", "order": 41},
    {"id": "racks_gabinetes_servidor", "name": "42. Racks de Telecomunicaciones & Gabinetes", "icon": "fa-server", "order": 42},
    {"id": "impresoras_multifuncionales", "name": "43. Impresoras de Inyección & Multifuncionales", "icon": "fa-print", "order": 43},
    {"id": "toners_laser", "name": "44. Tóners para Impresoras Láser", "icon": "fa-cubes", "order": 44},
    {"id": "tintas_cartuchos", "name": "45. Tintas Originales & Cartuchos", "icon": "fa-droplet", "order": 45},
    {"id": "plotters_gran_formato", "name": "46. Plotters de Impresión en Gran Formato", "icon": "fa-ruler-combined", "order": 46},
    {"id": "etiquetas_ribbons", "name": "47. Cintas Ribbon, Etiquetas & Papel Térmico", "icon": "fa-tags", "order": 47},
    {"id": "escaneres_digitalizadores", "name": "48. Escáneres de Documentos & Cama Plana", "icon": "fa-scanner", "order": 48},
    {"id": "sistemas_operativos", "name": "49. Sistemas Operativos Windows Oficiales", "icon": "fa-compact-disc", "order": 49},
    {"id": "ofimatica_productividad", "name": "50. Microsoft 365 & Suites de Oficina", "icon": "fa-file-lines", "order": 50},
    {"id": "software_contable_administrativo", "name": "51. Software Aspel & CONTPAQi Administrativo", "icon": "fa-calculator", "order": 51},
    {"id": "antivirus_seguridad_digital", "name": "52. Antivirus & Seguridad Digital", "icon": "fa-shield", "order": 52},
    {"id": "garantias_polizas_servicio", "name": "53. Pólizas & Extensiones de Garantía Oficial", "icon": "fa-certificate", "order": 53},
    {"id": "punto_de_venta", "name": "54. Sistemas de Punto de Venta (POS)", "icon": "fa-barcode", "order": 54},
    {"id": "smartphones_celulares", "name": "55. Teléfonos Celulares & Smartphones", "icon": "fa-mobile-screen-button", "order": 55},
    {"id": "tablets_ipads", "name": "56. Tablets & iPads", "icon": "fa-tablet-screen-button", "order": 56},
    {"id": "smartwatches_wearables", "name": "57. Smartwatches & Relojes Inteligentes", "icon": "fa-clock", "order": 57},
    {"id": "limpieza_mantenimiento", "name": "58. Aire Comprimido, Espumas & Limpieza", "icon": "fa-spray-can-sparkles", "order": 58},
    {"id": "cables_adaptadores", "name": "59. Cables de Video, USB & Adaptadores", "icon": "fa-plug", "order": 59},
    {"id": "mochilas_fundas_maletines", "name": "60. Mochilas, Fundas & Maletines para Laptop", "icon": "fa-briefcase", "order": 60},
    {"id": "soportes_ergonomia", "name": "61. Soportes Articulados & Bases para Monitor", "icon": "fa-tv", "order": 61},
    {"id": "hubs_docks_estaciones", "name": "62. Hubs USB-C & Docking Stations", "icon": "fa-layer-group", "order": 62},
    {"id": "herramientas_servicio_tecnico", "name": "63. Herramientas de Red & Ensamble Técnico", "icon": "fa-wrench", "order": 63},
    {"id": "candados_seguridad_laptop", "name": "64. Candados de Seguridad Kensington", "icon": "fa-lock", "order": 64},
    {"id": "climatizacion_aires_acondicionados", "name": "65. Climatización & Minisplits", "icon": "fa-snowflake", "order": 65},
    {"id": "gaming_consolas_sillas", "name": "66. Sillas Gamer, Consolas & Videojuegos", "icon": "fa-gamepad", "order": 66},
    {"id": "accesorios_perifericos", "name": "67. Accesorios de Cómputo & Misceláneos", "icon": "fa-boxes-stacked", "order": 67}
]

DEPT_ID_SET = {d["id"] for d in DEPARTAMENTOS_OFICIALES}


def clasificar_producto_semantico(sku, name, brand="", subgrupo_header="", sheet_name="", intc_cat="", intc_sub="", desc=""):
    s = (sku or "").upper().strip()
    raw_s = re.sub(r'^[AB]-', '', s)
    extra = f" {subgrupo_header} {intc_sub} {intc_cat} {sheet_name}".strip()
    n = f"{name or ''} {desc or ''} {extra}".upper().strip()
    name_u = (name or "").upper().strip()
    sub_u = f"{subgrupo_header or ''} {intc_sub or ''}".upper().strip()
    sheet_raw_u = (sheet_name or "").upper().strip()
    sheet_u = f"{sheet_name or ''} {intc_cat or ''}".upper().strip()
    icat_u = (intc_cat or "").upper().strip()
    isub_u = (intc_sub or "").upper().strip()
    title_sub = f"{name_u} {sub_u}".strip()

    def has(*words):
        return any(w in n for w in words)

    def lacks(*words):
        return not any(w in n for w in words)

    def name_has(*words):
        return any(w in name_u for w in words)

    def name_lacks(*words):
        return not any(w in name_u for w in words)

    def sub_has(*words):
        return any(w in sub_u for w in words)

    def sku_starts(*prefixes):
        return any(raw_s.startswith(p) or s.startswith(p) for p in prefixes)

    def has_word(pattern, text=None):
        return bool(re.search(pattern, n if text is None else text))

    # =========================================================================
    # TIER 1: EQUIPOS COMPLETOS, SERVIDORES Y DISPOSITIVOS MOVILES
    # =========================================================================

    # 18. SERVIDORES ENTERPRISE (Hardware: Torre, Rack, Storage Enterprise & Tape Libraries)
    is_cloud_service = sku_starts("SERCLO")
    is_srv_hardware = (
        (sku_starts("SRV", "SVR", "SER", "STO", "NW1") and not is_cloud_service) or
        name_has("SERVIDOR TORRE", "SERVIDOR RACK", "SERVIDOR DE RACK", "PROLIANT", "POWEREDGE",
                 "DELL PE T", "DELL PE R", "SERVER TORRE", "SERVER RACK", "THINKSYSTEM",
                 "FUSIONSERVER", "POWERVAULT", "HPE MSA ", "HPE STORAGE", "STORAGE ARRAY",
                 "TAPE AUTOLOADER", "TAPE LIBRARY", "RACKSTATION", "DISKSTATION", "SYNOLOGY NAS") or
        (name_u.startswith(("SERVIDOR ", "SERVER ", "STORAGE ", "DELL - SERVIDOR")) and not is_cloud_service) or
        (sub_u == "SERVIDORES" and name_lacks("LICENCIA", "WINDOWS SERVER", "CAL ", "ROK"))
    )
    is_srv_part_or_sw = (
        name_u.startswith(("MEMORIA", "MEMORY", "DISCO ", "UNIDAD DE ESTADO", "SSD ", "HDD ",
                           "LICENCIA", "PAQUETE DE ", "WINDOWS SERVER", "CAL(", "CAL ",
                           "GABINETE", "FUENTE", "CABLE", "TARJETA RISER", "TORNILLO",
                           "ADMINISTRADOR GRAFICO", "ADMINISTRADOR GRÁFICO", "KIT EN BLANCO",
                           "CARRITO", "RIEL", "KIT DE RIELES", "CERTIFICADO", "REGISTRO DE DOMINIO",
                           "ANCHO DE BANDA", "BACKUP", "INSTALACIÓN", "INSTALACION", "CLIENTE VPN",
                           "VALIDACIÓN", "ACTUALIZACIÓN", "ACTUALIZACION")) or
        sku_starts("ACC", "CAB", "MEM", "DDU", "SSD", "FUE", "SOF", "CSP", "ESD", "LIC", "SS0", "NBK", "UPS", "RCK") or
        name_has("WINDOWS SERVER ROK", "WINDOWS SERVER CAL", "XCLARITY CONTROL", "TARJETA RISER", "TORNILLO SUJETADOR")
    )
    if is_srv_hardware and not is_srv_part_or_sw:
        return "servidores_enterprise"

    # 17. COMPUTADORAS ALL IN ONE (AIO)
    is_aio_excl = (
        sku_starts("PAN", "TER", "KIO", "LCT") or
        "PUNTO DE VENTA" in sheet_u or "PUNTOS DE VENTA" in sheet_u or
        name_has("PUNTO DE VENTA", "TERMINAL POS", "ELOPOS", "ELO I-SERIES") or
        has("ALL IN ONE LED", "TERMINAL POS", "TERMINAL DE PUNTO DE VENTA", "PUNTO DE VENTA", "PUNTOS DE VENTA",
            "IMPRESORA TERMICA", "IMPRESORA TÉRMICA", "MINI PC", "MINIPC", "LIVA ")
    )
    is_imac = has_word(r'\bIMAC\b', name_u) and not sku_starts("ACC", "CAB", "MEM") and not name_u.startswith(("KIT ", "SOPORTE", "ADAPTADOR", "FUNDA"))
    is_aio_cooling = has("ENFRIADOR", "ENFRIAMIENTO", "REFRIGERACION", "REFRIGERACIÓN", "LIQUIDO", "LÍQUIDO", "LIQUID", "WATER", "LOOP", "PURE LOOP", "SILENT LOOP", "KRAKEN", "CORSAIR HYDRO", "VENTILADOR", "COOLER", "DISIPADOR", "FAN", "ARGB", "RADIADOR", "HERRAMIENTA", "BASE", "SOPORTE", "BRAZO")
    if (is_imac or ((sku_starts("AIO") or ((has("ALL IN ONE", "ALL-IN-ONE", "TODO EN UNO") or has_word(r'\bAIO\b', name_u)) and not is_aio_cooling)) and not is_aio_excl)) \
       and not sku_starts("VEN", "ENF", "ACC", "CAB", "MOU", "TEC"):
        if is_imac or sku_starts("AIO", "CPUDDL") or isub_u == "TODO-EN-UNO" or has("PROONE", "PROSTUDIO", "IDEACENTRE", "OPTIPLEX", "PAVILION AIO", "VERITON", "PC ALL IN ONE", "COMPUTADORA ALL IN ONE", "COMPUTADORA DE ESCRITORIO ALL IN ONE") or has_word(r'\b(INTEL|AMD|RYZEN|CELERON|CORE|PANTALLA|FHD|23\.8|21\.5|27"|24")\b'):
            return "computadoras_all_in_one"

    # 14. LAPTOPS & COMPUTADORAS PORTATILES
    is_mobile_wks = sku_starts("WKS") and (
        has_word(r'\b(THINKPAD|LENOVO TP\b|PRO MAX 16)\b', name_u) or
        has("LAPTOP GPU", "GPU PARA PORTÁTIL", "GPU PARA PORTATIL", "BATERÍA ESTÁNDAR DE 6 CELDAS", "BATERIA ESTANDAR DE 6 CELDAS")
    )
    is_laptop_name = (
        name_u.startswith(("LAPTOP ", "NOTEBOOK ", "COMPUTADORA PORTATIL", "COMPUTADORA PORTÁTIL", "PORTATIL ", "PORTÁTIL ", "MICROSOFT SURFACE PRO", "SURFACE PRO ")) or
        name_has("MACBOOK", "THINKPAD", "THINKBOOK", "IDEAPAD", "VIVOBOOK", "ZENBOOK", "EXPERTBOOK", "LATITUDE", "VOSTRO", "INSPIRON", "ASPIRE", "CHROMEBOOK", "LEGION", "LOQ ", "VICTUS", "PREDATOR", "NITRO ", "SURFACE LAPTOP", "GALAXY BOOK", "DELL PRO - NOTEBOOK") or
        has_word(r'\b(HP OMEN|OMEN BY HP|OMEN \d|LENOVO TP|LENOVO TB|LENOVO V14|LENOVO V15)\b', name_u)
    )
    is_laptop_accessory = (
        name_u.startswith(("FUNDA", "MOCHILA", "MALETIN", "MALETÍN", "MALETA", "PORTAFOLIO", "CARGADOR", "BATERIA", "BATERÍA", "ELIMINADOR", "CANDADO", "BASE", "SOPORTE", "TECLADO", "PANTALLA", "DISPLAY", "MONITOR", "VENTILADOR", "MEMORIA", "DISCO", "MOUSEPAD", "IMPRESORA", "ESCANER", "ESCÁNER", "TARJETA", "REGULADOR", "CAMARA", "CÁMARA", "LAPTOP CLEANER", "LIMPIADOR", "CARCASA", "FILTRO", "UBIQUITI", "LENOVO GARANTIA", "LENOVO GARANTÍA", "LENOVO EXTENSIÓN", "LENOVO EXTENSION", "LENOVO RATÓN", "LENOVO RATON", "DOCKING", "LENOVO THINKPAD USB4 DOCK", "ESTACIÓN DE ACOPLAMIENTO", "ESTACION DE ACOPLAMIENTO")) or
        name_has("FUNDA PARA", "MOCHILA PARA", "MALETIN PARA", "CANDADO DE SEGURIDAD", "BASE ENFRIADORA", "LAPTOP CLEANER", "ESTACIÓN DE CONEXIÓN", "ESTACION DE CONEXION", "DOCKING", "USB-C DOCK", "USB4 DOCK", "EVOSHELL", "CASE - ", "COMPATIBILIDAD CON DISPOSITIVOS MÓVILES", "A NOTEBOOKS", "PARA THINKPAD", "PARA MACBOOK", "CARCASA PARA MACBOOK") or
        icat_u in ("MALETINES", "ACCESORIOS PARA COMPUTADORES")
    )
    if (sku_starts("COM", "POR", "LAP", "NOTE", "NT0") or is_mobile_wks or (icat_u == "COMPUTADORES" and isub_u in ("PORTÁTILES", "2-EN-1")) or is_laptop_name) \
       and not is_laptop_accessory \
       and not sku_starts("ACC", "CAB", "MEM", "SSD", "DDU", "TEC", "MOU", "FUE", "GAB", "VEN", "BAT", "CAR", "SOF", "LIC", "MON", "PAN", "SCA", "IMP", "MLT", "TAR", "NVR", "DVR", "MAL", "SLX", "CAM", "REG", "NBK", "UPS", "AN0", "AN1", "AN7"):
        return "laptops_portatiles"

    # 15. MINI PCS & NUCS
    has_nuc_token = has_word(r'\b(NUC\d*|BOXNUC|RNUC|BNUC)\b') and has("INTEL", "ASUS", "CORE", "BAREBONE", "MINI", "CELERON", "PENTIUM")
    has_tiny_pc = has_word(r'\bTINY\b', name_u) and has("THINKCENTRE", "THINKSTATION", "THINKSMART", "LENOVO", "CORE", "RYZEN", "PC") and lacks("TINY-IN-ONE", "BOCINA", "AUDIFONO", "AUDÍFONO", "AURICULAR")
    has_mini_pc = (
        has_word(r'\bMINI\s*PC\b(?!-\d)') or
        has("MINIPC", "CHOMP", "ELITEDESK MINI", "PRODESK MINI", "MICRO DESKTOP", "TITAN MINI", "MAC MINI", "MÓDULO OPS", "MODULO OPS", "BENQ OPS") or
        has_word(r'\b(LIVA\s+(ONE|Z|Q)|PRODESK\s+\d+\s+MINI|ELITEDESK\s+\d+\s+MINI|M70Q|M75Q|M80Q|M90Q|NEO\s*50Q|PRO\s+MFF|PRO\s+MICRO)\b') or
        has_nuc_token or has_tiny_pc or sku_starts("RNUC", "CPUMTD", "CPUBNQ")
    )
    if has_mini_pc \
       and not name_u.startswith(("CANDADO", "SOPORTE", "BASE", "MONITOR", "PANTALLA", "FUNDA", "CABLE", "ADAPTADOR", "BOCINA", "AUDIFONO", "AUDÍFONO", "AURICULAR", "MOUSE", "RATON", "RATÓN", "TECLADO", "TABLET", "TABLETA")) \
       and lacks("TINY-IN-ONE", "SOPORTE VESA HP", "FUNDA DE SEGURIDAD") \
       and not sku_starts("ACC", "CAB", "MEM", "SSD", "DDU", "BOC", "MOU", "TEC", "MON", "PAN", "TAB", "TLC", "IPD", "CAM", "IMP", "MAL"):
        return "mini_pcs_nuc"

    # 16. COMPUTADORAS ENSAMBLADAS / GAMING PCs / WORKSTATIONS
    is_pc_not_nonpc = (
        not name_u.startswith(("MONITOR", "PANTALLA", "TARJETA", "MOCHILA", "CARGADOR", "LENOVO CARGADOR", "LENOVO GARANTIA", "LENOVO GARANTÍA", "LENOVO EXTENSIÓN", "LENOVO EXTENSION", "LENOVO MONITOR", "LENOVO RATÓN", "LENOVO RATON", "LENOVO CABLE", "CANDADO", "GARANTIA", "GARANTÍA", "EXTENSIÓN DE GARANT", "EXTENSION DE GARANT", "PROCESADOR ", "SOPORTE", "BASE", "CABLE", "ADAPTADOR", "SISTEMA POS", "TERMINAL POS")) and
        lacks("ALL IN ONE", "ALL-IN-ONE", "TODO EN UNO", "TINY-IN-ONE", "4 CORE 4GHZ", "6 CORE 4.2GHZ", "RETAIL PLATAFORMA", "SISTEMA POS", "PUNTO DE VENTA", "CANDADO", "CABLE DE SEGURIDAD") and
        not any(w in name_u for w in ("LAPTOP", "NOTEBOOK", "PORTATIL", "PORTÁTIL"))
    )
    is_pc_name = (
        name_has("THINKSTATION", "THINKCENTRE", "THINCENTER", "THINKSMART CORE", "THINKSMART HUB", "WORKSTATION", "PC GAMER", "PC GAMING", "PC OFFICE", "PC DE OFICINA", "PC DESKTOP", "PC ASUS EXPERTCENTER", "EXPERTCENTER", "COMPUTADORA DE ESCRITORIO", "COMPUTADORA ESCRITORIO", "COMPUTADORA GAMING", "COMPUTADORA GAMER", "COMPUTADORA EVOTEC", "COMPUTADORA PC ", "EQUIPO DE ESCRITORIO", "COMPUTADORA ENSAMBLADA", "PC ENSAMBLADA", "DESKTOP VORAGO", "OPTIPLEX TOWER", "OPTIPLEX SFF", "PRODESK", "ELITEDESK", "VERITON", "DELL PRO SLIM", "DELL SFF", "SLIM TOWER", "SMALL FORM FACTOR", "PCHYCERBERUS", "FUSIONXPARK") or
        sku_starts("CFG-", "WKS", "CPUDDL", "CPULEV", "CPUGET", "CPUQIA", "CPUYEY", "CPUVGO", "CPULEN", "CPUHYU", "CPUHPI", "CPUACT", "CPUEVO", "CPUNCB", "CPUACR", "CPUASS", "PC9") or
        (icat_u == "COMPUTADORES" and isub_u == "COMPUTADORES DE MESA")
    )
    if is_pc_name and is_pc_not_nonpc \
       and not sku_starts("CPUINT", "CPUAMD", "CPUNEX", "MBD", "GAB", "FUE", "MEM", "SSD", "DDU", "ACC", "CAB", "TVI", "SOF", "LIC", "MON", "PAN", "TAR", "MAL", "CAR", "BAT", "MOU", "TEC", "BOC", "CAM"):
        return "computadoras_ensambladas"

    # 55. SMARTPHONES & CELULARES
    is_phone = (
        sku_starts("CEL", "SMA", "CE0") or
        (icat_u == "CELULARES" and isub_u == "CELULARES DESBLOQUEADOS") or
        name_u.startswith(("CELULAR ", "SMARTPHONE", "TELEFONO CELULAR", "TELÉFONO CELULAR", "APPLE IPHONE", "IPHONE ", "GALAXY S", "GALAXY A", "REDMI ", "MOTO G", "POCO ")) or
        has_word(r'\b(SMARTPHONE|IPHONE \d|GALAXY S2\d|GALAXY A\d\d|REDMI NOTE|PIXEL \d+)\b', name_u)
    )
    if is_phone \
       and not name_u.startswith(("KIT ", "FUNDA", "MICA", "CRISTAL", "PROTECTOR", "ESTUCHE", "CARGADOR", "CABLE", "SOPORTE", "BASE", "AUDIFONO", "AUDÍFONO", "DIADEMA", "HEADSET", "GABINETE", "CARRO DE CARGA", "UPS", "NO BREAK", "NO-BREAK", "CAMARA", "CÁMARA", "TECLADO", "MOUSE", "RATON", "RATÓN")) \
       and lacks("ANCLA", "RANURA K-SLOT", "CANDADO", "BRAZALETE", "SOPORTE PARA CELULAR", "FUNDA PARA CELULAR", "FUNDA PARA IPHONE", "MICA PARA CELULAR", "MICA PARA IPHONE", "CRISTAL TEMPLADO PARA", "VIDEOPORTERO", "PARA IPHONE", "PARA SMARTPHONE", "PARA CELULAR", "GABINETE DE CARGA", "CARRO DE CARGA", "GABINETE MÓVIL DE CARGA", "KIT DE HERRAMIENTAS", "KIT TECLADO") \
       and not sku_starts("ACC", "CAB", "BAT", "TEC", "MOU", "SOF", "LIC", "BOC", "GAB", "NBK", "NOB", "UPS", "CAM", "DVR", "NVR", "ROU", "SWT", "IMP", "MON", "PAN", "TAB", "TLC", "IPD", "DDU", "SSD", "MEM", "KIT"):
        return "smartphones_celulares"

    # 56. TABLETS & IPADS
    is_tablet_name = (
        name_u.startswith(("TABLET", "TABLETA", "IPAD", "GALAXY TAB", "MATEPAD")) or
        has_word(r'\bIPAD\b(?!OS)', name_u) or
        name_has("GALAXY TAB", "MATEPAD", "LENOVO TAB", "IDEA TAB", "HYTAB", "XTAB")
    )
    is_tablet_non = (
        name_u.startswith(("FUNDA", "PROTECTOR", "CRISTAL", "MICA", "PLUMA", "STYLUS", "SOPORTE", "BASE", "TECLADO", "MOUSE", "RATON", "RATÓN", "CABLE", "ADAPTADOR", "CARGADOR", "SSD", "DISCO", "SERVIDOR", "MICROSOFT 365", "LICENCIA", "MODULO", "MÓDULO", "PAQ SR", "TABLETA DE USO RUDO", "TABLETA INDUSTRIAL", "WACOM")) or
        has("TERMINAL POS", "PUNTO DE VENTA", "TABLETA DE USO RUDO", "TABLETA INDUSTRIAL", "SCANPAL", "SOFT RESTAURANT", "DIGITALIZADOR", "TABLETA DE LÁPIZ", "TABLETA DE LAPIZ", "PARA TABLET", "PARA TABLETA", "PARA IPAD", "FUNDA CON TECLADO")
    )
    if (sku_starts("TAB", "TLC", "IPD") or is_tablet_name) \
       and not is_tablet_non \
       and not sku_starts("ACC", "CAB", "CAR", "CPU", "BOC", "MIC", "CAM", "MOU", "TEC", "DDU", "SSD", "MEM", "SER", "SRV", "SVR", "ESD", "SOF", "LIC", "CSP", "KIT", "TER", "LCT", "HDH"):
        return "tablets_ipads"

    # 57. SMARTWATCHES & WEARABLES
    is_wearable = (
        name_has("SMARTWATCH", "SMARWATCH", "SMARTWACHT", "SMARTWACTH", "SMART WATCH", "RELOJ INTELIGENTE", "GALAXY WATCH", "APPLE WATCH", "BANDA INTELIGENTE", "SMART BAND", "PULSERA INTELIGENTE", "HUAWEI BAND", "WATCH FIT", "MI BAND", "OURA - RING") or
        (icat_u == "TECNOLOGÍA PORTÁTIL" and isub_u == "TRACKERS DE ACTIVIDAD") or
        sub_u in ("SMARTWATCH", "SMART WATCH", "SMART BAND", "SMARTWATCH MARCA VORAGO", "SMARWATCH KOSPET", "WATCH FIT HUAWEI")
    )
    if is_wearable \
       and not name_u.startswith(("AUDIFONO", "AUDÍFONO", "CARGADOR", "CABLE", "WATCH CHARGE CABLE", "CORREA", "FUNDA", "MICA", "CRISTAL", "BASE", "SOPORTE", "ESTUCHE", "RELOJ CHECADOR")) \
       and lacks("AIRPODS", "CARGADOR 3 EN 1", "CORREA PARA", "CARGADOR PARA", "CABLE PARA", "CHARGE CABLE", "PARA EL APPLE WATCH", "PARA APPLE WATCH", "PARA SMARTWATCH", "MICA PARA", "FUNDA PARA", "RELOJ CHECADOR"):
        return "smartwatches_wearables"

    # =========================================================================
    # TIER 2: COMPONENTES CORE DE ENSAMBLE, MONITORES Y PROYECTORES
    # =========================================================================

    # 1. PROCESADORES (CPUs)
    if sku_starts("CPUINT", "CPUAMD"):
        return "procesadores"

    is_non_cpu_pc_sku = sku_starts("CPU") and not sku_starts("CPUINT", "CPUAMD")
    if (name_u.startswith(("PROCESADOR ", "INTEL CORE ", "INTEL XEON ", "AMD RYZEN ", "AMD EPYC ", "AMD ATHLON ")) or has("PROCESADOR INTEL", "PROCESADOR AMD", "PROCESADOR RYZEN", "PROCESADOR XEON", "PROCESADOR EPYC")) \
       and not is_non_cpu_pc_sku \
       and lacks("TARJETA MADRE", "MOTHERBOARD", "PLACA BASE", "PLACA MADRE", "GABINETE", "LAPTOP", "NOTEBOOK", "COMPUTADORA", "PORTATIL", "PORTÁTIL", "PC ", "ALL-IN-ONE", "ALL IN ONE", "TODO EN UNO", "AIO", "MINI PC", "MINIPC", "BAREBONE", "NUC", "LIVA", "SERVIDOR", "SERVER", "TABLET", "IPAD", "WORKSTATION", "PASTA TERMICA", "PASTA TÉRMICA", "THINKSTATION", "THINKCENTRE", "THINKBOOK", "THINKPAD", "EXPERTCENTER", "VERITON", "OPTIPLEX", "PRODESK", "ELITEDESK", "ALIENWARE", "IMAC", "MAC MINI", "MODULO OPS", "MÓDULO OPS", "TOWER", "ESCRITORIO", "ENFRIAMIENTO", "LIQUIDO", "LÍQUIDO", "VENTILADOR", "COOLER", "DISIPADOR", "UNIDAD OPTICA", "ESCANER", "ESCÁNER", "KIOSCO", "QUIOSCO", "PUNTO DE VENTA", "POS", "TERMINAL", "MOUSE", "RATON", "RATÓN", "PROCESADOR DE AUDIO", "MEMORIA RAM", "SSD ", "HDD ") \
       and not sku_starts("CFG-", "COM", "MBD", "IPD", "TAB", "WKS", "LAP", "POR", "CEL", "SMA", "GAB", "FUE", "TVI", "ACC", "CAB", "CAR", "SER", "SRV", "SVR", "REL", "PC", "DES", "EQU", "SYS", "VEN", "ENF", "SCA", "KIO", "POS", "LCT", "TER", "CDR", "MOU", "PAN", "AIO", "MEM", "DDU", "SSD", "NT0", "NW1", "MM0"):
        return "procesadores"

    # 2. TARJETAS MADRE (Motherboards)
    is_mb_explicit = sku_starts("MBD", "MOT") or name_u.startswith(("MB ", "TARJETA MADRE", "MOTHERBOARD", "PLACA MADRE", "PLACA BASE"))
    is_mb_chipset = (has("TARJETA MADRE", "MOTHERBOARD", "PLACA MADRE", "PLACA BASE") and any(ch in n for ch in ["B650", "B660", "B760", "Z790", "B550", "A520", "A620", "B840", "B850", "B860", "H810", "H610", "H510", "Z890", "X870", "X670", "A320", "B450", "H410", "TRX50", "WRX90"]))
    if (is_mb_explicit or is_mb_chipset) \
       and not name_u.startswith(("GABINETE", "CHASIS", "CASE ", "FUENTE", "KIT ", "SOPORTE", "COMPUTADORA", "PC ", "MINI PC", "LAPTOP", "NOTEBOOK", "SERVIDOR", "WORKSTATION", "TERMINAL")) \
       and not sku_starts("GAB", "FUE", "CPU", "COM", "POR", "LAP", "TAB", "IPD", "AIO", "WKS", "REL", "SRV", "SVR", "SER", "RNUC", "KIT", "ACC", "CAB", "VEN", "ENF", "TVI", "TER", "PC", "NT0", "MEM", "DDU", "SSD") \
       and lacks("COMPUTADORA ENSAMBLADA", "ALL-IN-ONE", "ALL IN ONE", "TODO EN UNO", "LAPTOP", "NOTEBOOK", "PORTATIL", "PORTÁTIL", "MINI PC", "MINIPC", "BAREBONE", "NUC ", "NUC:", "BOXNUC", "LIVA", "SERVIDOR", "SERVER", "WALLABY", "MONTAJE", "SOPORTE PARA TARJETA MADRE", "SOPORTE DE TARJETA MADRE", "SOPORTE DE PLACA"):
        return "tarjetas_madre"

    # 5. TARJETAS DE VIDEO (GPUs)
    is_gpu_name = (name_u.startswith(("TARJETA DE VIDEO", "TARJETA DE VÍDEO", "TARJETA GRAFICA", "TARJETA GRÁFICA", "PLACA DE VIDEO")) or
                   name_has("GEFORCE RTX", "RADEON RX", "GEFORCE GTX"))
    if (sku_starts("TVI", "GPU") or (is_gpu_name and any(k in n for k in ["GDDR6", "GDDR6X", "GDDR7", "VRAM", "8GB", "12GB", "16GB", "24GB", "OC EDITION"]))) \
       and not name_u.startswith(("ADAPTADOR", "CABLE", "SOPORTE", "BRACKET", "RISER")) \
       and lacks("GABINETE", "CHASIS", "CASE GAMER", "WORKSTATION", "THINKSTATION", "LAPTOP", "NOTEBOOK", "COMPUTADORA", "TELEVISOR", "TELEVISIÓN", "PANTALLA NANO", "NANO LG", "SOPORTE PARA TARJETA", "BRACKET", "ADAPTADOR DE USB", "ADAPTADOR USB") \
       and not sku_starts("GAB", "WKS", "REL", "COM", "COMMAC", "POR", "LAP", "PAN", "MON", "TEL", "SER", "CPU", "MBD", "ACC", "CAB"):
        return "tarjetas_video"

    # 7. FUENTES DE ENERGIA (PSUs)
    is_psu = (
        sku_starts("FUE")
        or ((sku_starts("GAB") or "FUENTE" in title_sub) and (
            name_u.startswith(("FUENTE", "FUENTA", "FUENTRE", "POWER SUPPLY"))
            or any(k in title_sub for k in ["FUENTE DE PODER", "FUENTE PODER", "FUENTE ASUS", "POWER SUPPLY", "FUENTE ATX", "FUENTE SLIM", "FUENTE EVOTEC", "FUENTE XZEAL", "FUENTES DE PODER"])
        ))
    )
    is_pc_psu_spec = has("ATX", "SFX", "TFX", "80 PLUS", "80PLUS", "CYBENETICS", "FULL MODULAR", "SEMI MODULAR", "NO MODULAR")
    is_low_amp_dc = bool(re.search(r'(?<!\d)(0\.5|1|1\.5|2)\s*A\b', n)) and not is_pc_psu_spec
    if is_psu \
       and not name_u.startswith(("GABINETE", "CHASIS", "CASE ", "TORRE ", "MEDIA TORRE", "VENTILADOR", "MONITOR", "PANTALLA", "CABLE", "DIVISOR", "ESTACION", "ESTACIÓN", "CARRO", "IMPRESORA", "MULTIFUNCIONAL", "PLOTTER", "KIT", "CAMARA", "CÁMARA", "KIOSCO", "VERIFICADOR", "ADAPTADOR", "ELIMINADOR")) \
       and not is_low_amp_dc \
       and lacks("GABINETE CON FUENTE", "INCLUYE FUENTE", "NO BREAK", "NO-BREAK", "REGULADOR", "BATERIA", "POWER BANK", "VENTILADOR PARA FUENTES", "VENTILADOR DE FUENTE", "CCTV", "DIVISOR DE FUENTE", "REGULADA DE 12", "12 VCC", "12 VCD", "DAHUA", "SAXXON", "PROVISION", "IMPRESORA", "PRINTER", "PLOTTER", "MULTIFUNCIONAL", "ETIQUETA", "TRANSFERENCIA TERMICA", "TRANSFERENCIA TÉRMICA", "TURBOHD", "COLORVU", "DVR", "NVR", "KIT DE CAMARAS", "KIT DE CÁMARAS", "HIKVISION", "EPCOM", "CAMARA", "CÁMARA", "KIOSCO", "VERIFICADOR DE PRECIOS", "PUNTO DE VENTA", "ESCANER", "LECTOR", "STORAGE", "POWERVAULT", "FIREWALL") \
       and not has_word(r'\b(UPS|NO[- ]BREAK)\b') \
       and not sku_starts("VEN", "ENF", "MON", "PAN", "CAB", "ACC", "MBD", "CPU", "CAM", "DVR", "NVR", "IMP", "PRN", "PRO", "COM", "WKS", "LAP", "SVR", "SER", "KIT", "CCT", "SEC", "KIO", "POS", "LEC", "SCA", "TRM", "STO", "FIR", "FDP"):
        return "fuentes_energia"

    # 10. MONITORES & PANTALLAS
    is_proj_screen = (
        sku_starts("PANSCR") or
        has("PROYECCION", "PROYECCIÓN", "PANTALLA DE PROYECCION", "PANTALLA DE PROYECCIÓN", "PANTALLA PROYECCION", "PANTALLA PROYECCIÓN", "PANTALLA PARA PROYECTOR", "PANTALLA DE PARED MANUAL", "PANTALLA MURAL", "SCREENBEN")
    )
    is_monitor_excl = (
        name_u.startswith(("SOPORTE", "BRAZO", "BASE P/", "BASE PARA", "LIMPIADOR", "TOALLITAS", "CABLE", "FILTRO", "PANTALLA DE PRIVACIDAD", "TIRA DE LED", "BARRA DE LUZ", "BARRA DE SONIDO", "DECODIFICADOR", "PLATAFORMA DE SEÑALIZACION", "PLATAFORMA DE SEÑALIZACIÓN", "PLAYER BOX", "STAND MONITOR", "CONVERTIDOR", "OXIMETRO", "OXÍMETRO", "PIZARRON BLANCO", "PIZARRÓN BLANCO", "LAPTOP", "NOTEBOOK", "COMPUTADORA", "ALL IN ONE PC", "PANEL DE CONTROL", "CHAROLA", "QUIOSCO", "KIOSCO")) or
        has("SOPORTE PARA MONITOR", "BRAZO PARA MONITOR", "BASE PARA MONITOR", "LIMPIADOR DE PANTALLAS", "TOALLITAS ANTIESTATICAS", "PROTECTOR DE PANTALLA", "PANEL DE CONTROL DE ACCESO", "CONTROL DE ACCESO", "PANEL DE ALARMA", "KIOSCO", "QUIOSCO", "AUTOCOBRO", "AUTOSERVICIO", "PIZARRON BLANCO", "PIZARRÓN BLANCO", "VIDEOPORTERO", "VIDEO PORTERO") or
        sku_starts("CAB", "COM", "POR", "LAP", "NT0", "AIO", "WKS", "CPU", "PANECL") or
        (sku_starts("ACC") and not name_u.startswith(("MONITOR PORTATIL", "MONITOR PORTÁTIL")))
    )
    is_monitor_pos = (
        sku_starts("MON", "LFD", "BIZ", "HTV", "MT0", "MT1", "MT6", "MT8") or
        (sku_starts("PAN") and not is_proj_screen) or
        (icat_u == "MONITORES" and isub_u == "MONITORES") or
        (icat_u == "PUNTOS DE VENTA" and isub_u == "MONITORES") or
        name_u.startswith(("MONITOR ", "LENOVO MONITOR ", "PANTALLA PROFESIONAL", "PANTALLA SEMI-PROFESIONAL", "PANTALLA HOTELERA", "E-BOARD INTERACTIVO", "VIDEO WALL", "ALL IN ONE LED LG", "SMART TV ")) or
        has("MONITOR GAMER", "PANTALLA GAMER", "SMART MONITOR")
    )
    if is_monitor_pos and not is_proj_screen and not is_monitor_excl:
        return "monitores_pantallas"

    # 31. PROYECTORES DE VIDEO & PANTALLAS MURALES
    is_proj_pos = (
        (sku_starts("PRO") and not sku_starts("PROLMP")) or
        sku_starts("PANSCR") or
        (sku_starts("PAN") and is_proj_screen) or
        (icat_u == "PROYECTORES" and isub_u in ("PROYECTORES", "PANTALLAS")) or
        name_u.startswith(("PROYECTOR", "PROYECTO BENQ", "MINI PROYECTOR", "EL PROYECTOR", "VANKYO PROYECTOR", "YABER PROYECTOR", "VIDEOPROYECTOR", "PANTALLA DE PROYECCION", "PANTALLA DE PROYECCIÓN", "PANTALLA PROYECCION", "PANTALLA PROYECCIÓN", "PANTALLA PARA PROYECTOR")) or
        has("PROYECTOR PORTATIL", "PROYECTOR PORTÁTIL", "VIDEOPROYECTOR", "PANTALLA DE PROYECCION", "PANTALLA DE PROYECCIÓN", "PROJECTION SCREEN")
    )
    is_proj_non = (
        name_u.startswith(("LAMPARA", "LÁMPARA", "LAMP ", "LENTE ", "SOPORTE", "BRAZO", "TRIPIE", "TRÍPIE", "TRIPIÉ", "TRIPODE", "TRÍPODE", "CAJA P/MESA", "MODULO", "MÓDULO", "LICENCIA", "VENTILADOR", "PRESENTADOR", "KIT DE MONTAJE", "CARRITO", "SCREENBAR", "CABLE", "ADAPTADOR")) or
        name_has("LAMPARA PARA PROYECTOR", "LÁMPARA PARA PROYECTOR", "LENTE PARA PROYECTOR", "SOPORTE PARA PROYECTOR", "SOPORTE DE TECHO", "SOPORTE DE PARED", "CAJA P/MESA", "KIT DE MONTAJE") or
        sku_starts("LMP", "CAB", "PROLMP") or
        (sku_starts("ACC") and not (icat_u == "PROYECTORES" and isub_u == "PANTALLAS"))
    )
    if is_proj_pos and not is_proj_non:
        return "proyectores_presentacion"

    # =========================================================================
    # TIER 3: MEMORIAS, ALMACENAMIENTO, GABINETES PC Y ENFRIAMIENTO
    # =========================================================================

    # 23. TARJETAS MICROSD & SD
    is_msd_title = (
        sku_starts("MSD", "MEN")
        or name_u.startswith(("MICROSD", "MICRO SD", "MEMORIA MICRO SD", "MEMORIA MICROSD", "TARJETA MICROSD", "TARJETA MICRO SD", "TARJETA SD", "TARJETA DE MEMORIA SD", "MICRO SECURE DIGITAL", "SECURE DIGITAL", "SDXC ", "SDHC ", "MICRO ENDURANCE"))
        or (sku_starts("MEM", "DDU") and any(k in title_sub for k in ["MICROSD", "MICRO SD", "MICRO SECURE DIGITAL", "SECURE DIGITAL", "SDHC", "SDXC", "TARJETA SD", "CANVAS SELECT", "CANVAS GO", "CANVAS REACT", "ULTRA MICROSD", "EXTREME PRO", "MICRO ENDURANCE"]))
    )
    if is_msd_title \
       and not name_u.startswith(("CAMARA", "CÁMARA", "BOCINA", "BAFLE", "DIADEMA", "AUDIFONO", "AUDÍFONO", "TABLET", "TABLETA", "IPAD", "CELULAR", "SMARTPHONE", "PROYECTOR", "KIOSCO", "QUIOSCO", "IMPRESORA", "MULTIFUNCIONAL", "TERMINAL", "KIT ", "COMPUTADORA", "MINI PC", "LECTOR", "ADAPTADOR", "GABINETE", "CASE", "DOCKING", "HUB", "ACCESORIO ")) \
       and lacks("LECTOR", "CARD READER", "ADAPTADOR USB", "GABINETE", "CASE", "DOCKING", "HUB USB", "XBOX EXPANSION", "XBOX EXPANSIÓN") \
       and not sku_starts("ACC", "CAB", "CAM", "BOC", "TAB", "TLC", "IPD", "KIT", "CPU", "CEL", "SMA", "PRO", "KIO", "IMP", "MLT", "TER", "HDH", "DVR", "NVR", "GRD", "GAB", "COM", "POR", "LAP", "AIO", "POS", "LCT"):
        return "tarjetas_microsd"

    # 24. MEMORIAS USB FLASH & PENDRIVES
    is_usb_title = (
        sku_starts("USB")
        or any(k in title_sub for k in ["MEMORIA USB", "MEMORIA FLASH USB", "PENDRIVE", "FLASH DRIVE", "DUAL DRIVE", "CRUZER", "DATATRAVELER", "ULTRA FLAIR", "DRIVE TYPE-C", "UNIDAD FLASH USB", "DT EXODIA", "DTXM", "DT70", "DTSE9", "DTDUO", "SDCZ", "IRONKEY"])
        or (sku_starts("MEM") and bool(re.search(r'\bDTX[MG2]?\b', title_sub)))
    )
    if is_usb_title \
       and not name_u.startswith(("GABINETE", "CHASIS", "PLOTTER", "IMPRESORA", "MULTIFUNCIONAL", "PROYECTOR", "CAMARA", "CÁMARA", "BOCINA", "CORREA", "LECTOR", "ADAPTADOR", "CABLE", "HUB", "ESTACION", "ESTACIÓN")) \
       and lacks("SISTEMA OPERATIVO", "LICENCIA", "WINDOWS 11 PRO", "WINDOWS 11 HOME", "WINDOWS 10 PRO", "WINDOWS 10 HOME", "CABLE", "HUB", "ADAPTADOR", "RED USB", "WIFI USB", "BLUETOOTH", "ANTENA", "CARGADOR", "DIMM", "UDIMM", "SODIMM", "DDR4", "DDR5", "DDR3", "DDR2", "MICROSD", "MICRO SD", "SDHC", "SDXC", "CORREA PARA MEMORIA", "LECTOR USB", "LECTOR DE MEMORIA", "LECTOR DE TARJETAS") \
       and not sku_starts("ACC", "CAB", "MSD", "GAB", "PLO", "IMP", "MLT", "PRO", "CAM", "DVR", "NVR", "BOC", "TAB", "TLC", "CPU", "MBD", "COM", "POR", "LAP", "KIO", "TER", "SCA"):
        return "memorias_usb_pendrives"

    # Guard común para los 3 departamentos de Memoria RAM física
    is_ram_product = (
        sku_starts("MEM") or
        name_u.startswith(("MEMORIA ", "MEMORY ", "RAM ", "DDR", "KIT DE MEMORIA", "SYNOLOGY D4", "SYNOLOGY D5"))
    ) and not sku_starts(
        "COM", "TER", "WKS", "CPU", "REL", "AIO", "SER", "SRV", "SVR", "PC", "NT0", "POR", "LAP",
        "NBK", "NOB", "UPS", "BAT", "REG", "SUP", "ACC", "CAB", "SOF", "ESD", "CSP", "LIC", "NCE", "SS0", "B-SS", "B-SO", "B-SE",
        "DDU", "SSD", "HDD", "PLO", "IMP", "MLT", "MBD", "MOT", "GAB", "FUE", "VEN", "ENF", "TVI", "MSD", "USB", "MON", "PAN", "STO"
    ) and not name_u.startswith((
        "SERVIDOR", "SERVER", "NO BREAK", "NO-BREAK", "UPS", "BATERIA", "BATERÍA", "CHAROLA", "RACK",
        "IMPRESORA", "PLOTTER", "DISCO", "UNIDAD DE ESTADO", "TERMINAL", "WORKSTATION", "COMPUTADORA",
        "PC ", "LAPTOP", "NOTEBOOK", "MINI PC", "THINKPAD", "THINKBOOK", "THINKCENTRE", "THINCENTER",
        "THINKSTATION", "LENOVO TP", "LENOVO TB", "ALL IN ONE", "WINDOWS", "MICROSOFT", "LICENCIA",
        "KIT EN BLANCO", "TARJETA RISER", "TORNILLO", "ADMINISTRADOR", "HPE PROLIANT", "IRONKEY",
        "TARJETA DE EXPANSION", "TARJETA DE EXPANSIÓN"
    )) and lacks(
        "KIT EN BLANCO", "ESPACIOS DE MEMORIA", "ESPACIO EN BLANCO", "DUMMY", "TAPA",
        "SERVIDOR VIRTUAL", "VIRTUAL EN LA NUBE", "EN LA NUBE", "CT CLOUD", "WINDOWS SERVER", "ROK ", "CAL ",
        "UNIDAD DE ESTADO SOLIDO", "UNIDAD DE ESTADO SÓLIDO", "ESTADO SOLIDO", "ESTADO SÓLIDO", "NVME", "M.2",
        "DISCO DURO", "NO BREAK", "NO-BREAK", "SISTEMA UPS", "TERMINAL ALL IN ONE", "TERMINAL PUNTO DE VENTA",
        "ELOPOS", "ELOTOUCH", "HISTONE", "WORKSTATION", "THINKCENTRE", "THINCENTER", "THINKBOOK", "THINKPAD",
        "EXPERTCENTER", "LENOVO TP ", "LENOVO TB ", "MEMORIA DE IMPRESION", "MEMORIA DE IMPRESIÓN",
        "MICROSD", "MICRO SD", "SECURE DIGITAL", "MICRO SECURE DIGITAL", "USB", "FLASH DRIVE", "PENDRIVE", "IRONKEY",
        "XBOX EXPANSION", "XBOX EXPANSIÓN", "CLASS 10", "CLASS 4", "UHS-I", "UHS-II", "V30", "V60"
    )

    # 25. MEMORIAS RAM LAPTOP (SODIMM)
    if is_ram_product and has("SODIMM", "SO-DIMM", "SO DIMM", "RAM PARA LAPTOP", "RAM LAPTOP", "DDR4 SODIMM", "DDR5 SODIMM") \
       and lacks("MINI PC", "NUC", "LIVA", "HERRAMIENTAS", "KIT DE HERRAMIENTAS", "COMPUTADORA", "LAPTOP", "NOTEBOOK", "SURFACE", "MOTHERBOARD", "TARJETA MADRE"):
        return "memorias_ram_laptop"

    # 26. MEMORIAS RAM SERVIDOR (ECC / NAS Enterprise)
    is_non_ecc = has("NON-ECC", "NON ECC")
    is_kcp_desktop = bool(re.search(r'\bKCP\d', n))
    is_server_oem_pn = bool(re.search(r'\b(KTH-PL|KTD-PE|KTL-TS|D4ES\d|D4EC\d|D4ER\d|D5NS\d|D5ES\d)', n)) or sku_starts("MEMHPE", "MEMDLL", "MEMLEN", "MEMXFN")
    is_true_ecc = bool(re.search(r'(?<!NON[- ])\bECC\b', n))
    if is_ram_product and not is_kcp_desktop and (
        is_server_oem_pn
        or has("ECC REG", "ECC REGISTERED", "RDIMM", "LRDIMM", "TRUDDR4", "TRUDDR5", "PARA SERVIDOR", "PARA POWEREDGE", "PARA NAS SYNOLOGY", "NAS SYNOLOGY")
        or (is_true_ecc and not is_non_ecc)
        or (has("RAM SERVIDOR", "RAM SERVER", "SERVER MEMORY", "THINKSYSTEM", "POWEREDGE") and has("DIMM") and not is_non_ecc)
    ):
        return "memorias_ram_servidor"

    # 3. MEMORIAS RAM PC (DIMM)
    if is_ram_product \
       and (sku_starts("MEM") or has("MEMORIA RAM", "FURY BEAST", "VENGEANCE", "XPG SPECTRIX", "TRIDENT", "FURY RENEGADE", "RIPJAWS")) \
       and (has("DIMM", "UDIMM", "DDR4", "DDR5", "DDR3", "DDR2", "DDR ", "PC3200", "PC2100", "PC4-", "PC5-") or has("FURY BEAST", "VENGEANCE", "TRIDENT", "LANCER")) \
       and not is_server_oem_pn \
       and (not has("ECC REG", "ECC REGISTERED", "RDIMM", "TRUDDR", "PARA SERVIDOR", "POWEREDGE") or is_non_ecc) \
       and lacks("SODIMM", "SO-DIMM", "SO DIMM", "LAPTOP", "PORTATIL", "PORTÁTIL", "PARA SERVIDOR", "POWEREDGE", "MINI PC", "MOTHERBOARD", "TARJETA MADRE", "PROCESADOR", "RYZEN", "INTEL CORE") \
       and not has_word(r'\bMB\b', name_u):
        return "memorias_ram_pc"

    # 22. DISCOS DUROS EXTERNOS
    is_acc_real_ext_drive = sku_starts("ACC") and (
        name_u.startswith(("DISCO DURO EXTERNO", "DISCO EXTERNO", "SSD EXTERNO", "SSD PORTATIL", "SSD PORTÁTIL", "SSD PORTABLE"))
        or "DISCO DURO EXTERNO" in sub_u
    )
    is_ext_drive = (
        any(k in title_sub for k in ["DISCO DURO EXTERNO", "DISCO DUROS EXTERNOS", "DISCOS DUROS EXTERNOS", "DISCO EXTERNO", "SSD EXTERNO", "SSD PORTATIL", "SSD PORTÁTIL", "SSD PORTABLE", "CANVIO", "MY PASSPORT", "WD ELEMENTS", "ELEMENTS SE", "ELEMENT SE", "BACKUP PLUS", "HD710 PRO", "HD330", "HV620S", "HV300", "HM800", "XS1000", "XS2000", "EXPANSION XBOX", "EXPANSIÓN XBOX", "XBOX EXPANSION SLOT", "XBOX EXPANSIÓN SLOT"])
        or (any(k in title_sub for k in ["DISCO PORTATIL", "DISCO PORTÁTIL", "PORTABLE", "PORTATIL", "PORTÁTIL"]) and sku_starts("DDU", "SSD", "MEM") and any(k in n for k in ["USB", "TYPE-C", "TIPO C", "MICRO-B", "TOSHIBA", "WD", "WESTERN DIGITAL", "SEAGATE", "ADATA", "SANDISK", "KINGSTON"]))
    )
    if is_ext_drive \
       and not name_u.startswith(("ESCANER", "ESCÁNER", "CARCASA", "GABINETE", "ENCLOSURE", "FUNDA", "ESTUCHE", "PROTECTOR", "CABLE", "ADAPTADOR", "CONVERTIDOR", "BASE", "SOPORTE", "DOCKING", "ESTACION", "ESTACIÓN")) \
       and lacks("PROTECTOR", "FUNDA", "SILICON", "SILICÓN", "ESTUCHE", "CARCASA PARA", "CARCASA EXTERNA", "CARCASA M.2", "CARCASA DE ALUMINIO", "GABINETE EXTERNO", "GABINETE PARA DISCO", "GABINETE DE DISCO", "GABINETE DISCO", "GABINETE PARA SSD", "GABINETE USB", "ENCLOSURE", "CONVERTIDOR", "ADAPTADOR", "DOCKING", "ESTACION DE ACOPLAMIENTO", "ESTACIÓN DE ACOPLAMIENTO") \
       and (not sku_starts("ACC") or is_acc_real_ext_drive) \
       and not sku_starts("CAB", "CAR", "SCA", "SCN", "IMP", "PRO", "CAM", "GAB"):
        return "discos_duros_externos"

    # 8. SSDS M.2 NVME & PCIE
    is_sata_25_name = bool(re.search(r'\b2\.5\b|2\.5["\'\u201d]|2\.5\s*(IN|INCH|PULG)|\b(DC600M|KC600|SA400S37|SU630|SU650|SU800|MSATA)\b', name_u))
    is_m2_name = bool(re.search(r'\b(M\.2|M2|NVME|2280|2230|2242)\b', name_u)) or ("LEGEND" in name_u and "PCIE" in name_u)
    if (is_m2_name and (sku_starts("SSD", "DDU") or any(k in title_sub for k in ["SSD", "ESTADO SOLIDO", "ESTADO SÓLIDO", "SOLID STATE", "DISCO DURO"]))) \
       and not is_sata_25_name \
       and not any(w in name_u for w in ["EXTERNO", "PORTATIL", "PORTÁTIL", "PORTABLE", "CANVIO", "LAPTOP", "NOTEBOOK", "COMPUTADORA", "MINI PC", "NUC", "PROCESADOR", "INTEL CORE", "CORE ULTRA", "RYZEN", "MOTHERBOARD", "TARJETA MADRE", "GABINETE", "CARCASA", "ENCLOSURE", "ADAPTADOR", "CABLE", "DOCKING", "ESTACION", "ESTACIÓN"]) \
       and lacks("GABINETE PARA SSD", "ENCLOSURE", "CARCASA PARA", "ESTACION DE ACOPLAMIENTO", "ESTACIÓN DE ACOPLAMIENTO", "CLONACION DE SSD", "CLONACIÓN DE SSD") \
       and not sku_starts("ACC", "CAB", "CAR", "CPU", "MBD", "GAB", "COM", "POR", "LAP", "AIO", "WKS", "SRV", "SVR", "SER", "RNUC", "TAB", "IPD", "CEL", "SMA", "STO"):
        return "ssds_m2_nvme"

    # 9. DISCOS DUROS INTERNOS HDD (y SSDs internos SATA/SAS 2.5"/3.5"/mSATA)
    is_internal_drive_ddu = sku_starts("DDU", "HDD") and sheet_raw_u != "CONSUMIBLES" and (
        bool(re.search(r'\b(3\.5|2\.5|SATA|MSATA|SAS|HDD|SSD|RPM|7\.2K|10K|15K|5400|7200|SFF|LFF|HOT[- ]?PLUG|HOT[- ]?SWAP|SURVEILLANCE|EXOS|IRONWOLF|BARRACUDA|SKYHAWK|PURPLE|RED|BLUE|GREEN|GOLD|KC600|DC600M|SA400|SU630|SU650|SU800|SSD PLUS)\b', n))
        or has("DISCO DURO", "ESTADO SOLIDO", "ESTADO SÓLIDO", "HARD DRIVE", "SOLID STATE")
    )
    is_internal_drive_name = (
        name_u.startswith(("DISCO DURO", "DISCO DE ESTADO", "DISCO ESTADO", "UNIDAD DE ESTADO", "SSD ", "HDD "))
        and bool(re.search(r'\b(3\.5|2\.5|SATA|MSATA|SAS|HDD|RPM|7\.2K|10K|BARRACUDA|IRONWOLF|SKYHAWK|WD PURPLE|WD BLUE|WD RED|WD GOLD|WD GREEN|SURVEILLANCE|KC600|DC600M|SA400|SU630|SU650|SU800)\b', n))
        and sheet_raw_u != "CONSUMIBLES"
    )
    if (is_internal_drive_ddu or is_internal_drive_name) \
       and not bool(re.search(r'\b(M\.2|M2|NVME)\b', name_u)) \
       and not any(w in title_sub for w in ["EXTERNO", "EXTERNOS", "CANVIO", "PORTATIL", "PORTÁTIL", "PORTABLE", "BACKUP PLUS", "PASSPORT", "ELEMENTS", "ELEMENT SE"]) \
       and not name_u.startswith(("GABINETE", "CHASIS", "CASE ", "LAPTOP", "NOTEBOOK", "COMPUTADORA", "SERVIDOR", "STORAGE ", "NVR", "DVR", "EDVR", "CARCASA", "ENCLOSURE", "CABLE", "ADAPTADOR", "CONVERTIDOR", "RIEL", "SOPORTE", "BASE", "ESTACION", "ESTACIÓN", "DOCKING", "ACCESORIO")) \
       and lacks("GABINETE PARA", "GABINETE DE DISCO", "GABINETE EXTERNO", "CARCASA PARA", "ENCLOSURE", "DOCKING", "ESTACION DE ACOPLAMIENTO", "XEROX", "KYOCERA", "VERSALINK", "TASKALFA") \
       and not sku_starts("ACC", "CAB", "CAR", "GAB", "FUE", "CPU", "MBD", "COM", "POR", "LAP", "AIO", "WKS", "SRV", "SVR", "SER", "NVR", "DVR", "GRD", "STO", "CAM", "TAB", "IPD", "MEM", "MEN", "RCK", "KIO", "TER"):
        return "discos_duros_hdd_internos"

    # 4. GABINETES & CHASIS GAMER
    is_pc_case_form = any(k in n for k in ["ATX", "M-ATX", "MATX", "MICRO ATX", "MICRO-ATX", "MINI ITX", "MINI-ITX", "E-ATX", "EATX", "GAMER", "GAMING", "MID TOWER", "MIDTOWER", "FULL TOWER", "MIDI-TOWER", "MINI TORRE", "MEDIA TORRE", "MINI TOWER", "TORRE MEDIA", "TORRE COMPLETA", "MINITORRE", "GABINETE PARA PC"])
    is_telecom_rack_gab = (
        sheet_raw_u in ("CONECTIVIDAD", "TELEFONIA Y VIDEO VIGILANCIA", "ENERGIA", "CONSUMIBLES")
        or name_has("GABINETE MURAL", "GABINETE DE PARED", "GABINETE DE PISO", "GABINETE DE PISA", "GABINETE 15U", "GABINETE DE EXTERIOR", "SMARTRACK", "WALL MOUNT")
        or (bool(re.search(r'\b(RACK|SMARTRACK|MURAL|DE\s+PARED|EN\s+PARED|DE\s+PISO|DE\s+PISA|MONTAJE\s+EN\s+PARED|PARED\s+FIJ|19\s*["°\u201d]|19\s+PULGADAS|19\s+IN|([2-9]|[1-4]\d)\s*UR?)\b', n)) and not is_pc_case_form)
    )
    is_gab = (
        (sku_starts("GAB") and sheet_raw_u not in ("CONECTIVIDAD", "TELEFONIA Y VIDEO VIGILANCIA", "ENERGIA", "CONSUMIBLES", "ACCESORIOS"))
        or (isub_u == "CAJAS / GABINETES" and "COMPONENTES" in icat_u)
        or (name_u.startswith(("GABINETE", "CHASIS", "CASE GAMER", "TORRE GAMER", "MID TOWER", "FULL TOWER", "MINI TORRE", "MEDIA TORRE")) and is_pc_case_form)
    )
    if is_gab \
       and not is_telecom_rack_gab \
       and not name_u.startswith(("FUENTE", "FUENTA", "FUENTRE", "CHAROLA", "BANDEJA", "VENTILADOR", "CAMARA", "CÁMARA", "ESTACION", "ESTACIÓN", "CARRO", "CARRITO", "CANALETA", "TORNILLERIA", "TORNILLERÍA", "TARJETA", "CABLE", "REGULADOR", "AIRE", "CAJON", "CAJÓN", "SILIMPO", "ESPUMA", "SUPRESOR", "NO BREAK", "NO-BREAK", "UPS", "CARCASA", "ENCLOSURE", "DVR", "NVR", "SAXXON", "SOPORTE", "TOALLAS", "ESTUCHE", "PROTECTOR")) \
       and lacks("GABINETE DE DISCO", "GABINETE PARA DISCO", "GABINETE DISCO DURO", "GABINETE EXTERNO", "GABINETE PARA SSD", "GABINETE PARA HDD", "GABINETE USB-C SSD", "GABINETE USB A", "GABINETES HDD", "GABINETES DE DISCO", "ENCLOSURE", "CARCASA PARA", "ESTUCHE PROTECTOR", "TORNILLERIA", "TORNILLERÍA", "TUERCA ENJAULADA", "PATCH PANEL", "COMPUTADORA ENSAMBLADA", "VENTILADOR DE FUENTE", "REGULADA DE 12", "12 VCC", "12 VCD", "SAXXON", "ESTACION DE CARGA", "ESTACIÓN DE CARGA", "PARA CARGA DE ENERG", "GABINETE DE CARGA", "GABINETE MOVIL DE CARGA", "GABINETE MÓVIL DE CARGA", "CARRITO DE CARGA", "CARRO DE CARGA", "ESTACION DE ACOPLAMIENTO", "ESTACIÓN DE ACOPLAMIENTO", "CLONACION DE SSD", "CLONACIÓN DE SSD", "SIRENA", "ALARMA", "CANALETA", "TARJETA DE SONIDO", "TARJETA DE AUDIO", "SOUND CARD", "TARJETA DE RED", "NO BREAK", "NO-BREAK", "AIRE ACONDICIONADO", "CAJON DE DINERO", "CAJÓN DE DINERO", "ESPUMA LIMPIADORA", "SILIMEX", "BATERIA EXTERNA", "BATERÍA EXTERNA", "CICLO PROFUNDO") \
       and not sku_starts("ACC", "CAB", "CAR", "CPU", "MBD", "FUE", "VEN", "ROU", "SWT", "MSD", "USB", "DVR", "NVR", "CAM", "TEL", "RCK", "TAR", "IMP", "PRN", "AIR", "CJN", "SLX", "REG", "NBK", "UPS", "BAT"):
        return "gabinetes"

    # 6. ENFRIAMIENTO (Líquido & Aire)
    is_cooling_pos = (
        sku_starts("VEN", "ENF", "VER") or
        has("ENFRIAMIENTO LIQUIDO", "ENFRIAMIENTO LÍQUIDO", "WATER COOLING", "DISIPADOR", "COOLER CPU",
            "VENTILADOR PARA PROCESADOR", "VENTILADOR PARA CPU", "VENTILADOR PARA GABINETE", "VENTILADOR DE FUENTE",
            "VENTILADOR ENSON", "FAN RGB", "PURE LOOP", "SILENT LOOP", "NZXT KRAKEN",
            "KIT DE 3 VENTILADORES", "KIT 3 VENTILADORES", "KIT DE VENTILADORES", "KIT VENTILADORES",
            "KIT DE VENTILADOR", "KIT DE 3 VENTILADOR")
    )
    is_cooling_non = (
        name_u.startswith(("GABINETE", "CHASIS", "CASE ", "MINI TORRE", "TORRE GAMER", "RACK", "EXTERIOR", "UNIDAD DE ESTADO", "DISCO", "PASTA TERMICA", "PASTA TÉRMICA", "GRASA TERMICA", "NO-BREAK", "NO BREAK", "UPS", "BASE ENFRIADORA", "KIT GAMING", "TECLADO", "AUDIFONO", "AUDÍFONO", "AURICULAR", "RAZER KRAKEN", "VENTILADOR NEXTEP", "VENTILADOR DE PROYECCION", "VENTILADOR DE PROYECCIÓN", "CONTROL CON VENTILADORES", "FILTRO DE VENTILADOR", "SISTEMA DE ENFRIAMIENTO EN RACK")) or
        sku_starts("GAB", "RCK", "LIN", "MBD", "CPU", "FUE", "DDU", "SSD", "HDD", "SLX", "NBK", "NOB", "UPS", "BAT", "REG", "SUP", "BOC", "MM0", "CON", "TVI") or
        has("NO-BREAK", "NO BREAK", "SISTEMA UPS", "PASTA TERMICA", "PASTA TÉRMICA", "GRASA TERMICA", "GRASA TÉRMICA", "GABINETE ATX", "GABINETE GAMER", "CHASIS GAMER", "GABINETE CON VENTILADORES", "UNIDAD DE ESTADO SOLIDO", "UNIDAD DE ESTADO SÓLIDO", "AURICULAR", "KIT GAMING 4 EN 1", "BASE ENFRIADORA", "DE ESCRITORIO 3 ASPAS", "HOLOGRAMAS", "FILTRO DE VENTILADOR")
    )
    if is_cooling_pos and not is_cooling_non:
        if sku_starts("VEN", "ENF", "VER") or name_u.startswith(("VENTILADOR", "DISIPADOR", "ENFRIADOR", "ENFRIAMIENTO", "KIT DE DISIPADOR", "KIT DE VENTILADOR", "KIT VENTILADOR", "KIT DE 3 VENTILADOR", "KIT 3 VENTILADOR", "KIT GAMER 3 VENTILADOR", "NACEB KIT 3 VENTILADOR", "YEYIAN ", "HPE DL380")):
            return "enfriamiento"

    # =========================================================================
    # TIER 4: SOFTWARE, LICENCIAS Y GARANTIAS
    # =========================================================================

    # 49. SISTEMAS OPERATIVOS (Windows Oficial & SQL Server)
    has_compat_phrase = any(cp in n for cp in ["COMPATIBLE CON WINDOWS", "COMPATIBILIDAD CON WINDOWS", "SOPORTA WINDOWS", "FUNCIONA CON WINDOWS", "REQUIERE WINDOWS", "COMPATIBLE CON WIN", "COMPATIBLE CON SISTEMA", "SOPORTE PARA WINDOWS"])
    is_sw_sku = sku_starts("SOF", "ESD", "CSP", "LIC", "B-SS", "B-SE", "B-SO", "B-ZZ") or "SISTEMA OPERATIVO" in sub_u or ("WINDOWS" in sub_u and "SOFTWARE" in sheet_u)
    is_os_name = name_has("WINDOWS 11", "WINDOWS 10", "WINDOWS SERVER", "WIN SVR", "WINDOWS GGWA", "KIT DE LEGALIZACION", "KIT DE LEGALIZACIÓN", "CAL FOR WINDOWS", "USER CAL", "DEVICE CAL", "RDS 1 USER", "RDS 1 DEVICE", "WINDOWS 10/11", "SQL SERVER", "SQL SVR", "LICENCIAS DE ACCESO (CAL)", "LICENCIAS DE ACCESO DE CLIENTE (CAL)", "USUARIOS REMOTOS PARA WINDOWS")
    is_genuine_software = has("LICENCIA", "OEM", "COA", "DSP", "ESD", "RETAIL", "FPP", "64-BIT", "64 BITS", "32-BIT", "32 BITS", "ELECTRONIC SOFTWARE", "DIGITAL", "MEDIA PACK", "ROK", "CAL", "SISTEMA OPERATIVO", "PRODUCT KEY", "ACTIVACION", "GGWA", "SQL SERVER") or sku_starts("SOF", "ESD", "CSP", "LIC", "B-SS")

    if sku_starts("SOF", "ESD", "CSP", "LIC", "B-SS", "B-SE", "B-SO", "B-ZZ") and is_os_name \
       and not sku_starts("SOFAVZ", "SOFZKT", "SOFING", "LICZKT") \
       and lacks("ASPEL", "CONTPAQ", "CONTROL DE ACCESO", "BIOMETRICO", "BIOMÉTRICO", "HUELLA", "TORNIQUETE"):
        return "sistemas_operativos"

    if (is_sw_sku or is_os_name) and (is_os_name or has("WINDOWS 11", "WINDOWS 10", "WINDOWS SERVER")) \
       and not has_compat_phrase and is_genuine_software \
       and lacks("IMPRESORA", "MULTIFUNCIONAL", "SCANNER", "ESCÁNER", "ESCANER", "APUNTADOR", "PRESENTADOR", "TECLADO", "MOUSE", "RATON", "RATÓN", "ROUTER", "SWITCH", "ADAPTADOR", "CABLE", "DOCKING", "HUB", "PROCESADOR", "TARJETA MADRE", "LAPTOP", "COMPUTADORA", "NOTEBOOK", "TABLET", "MONITOR", "MEMORIA USB", "PENDRIVE", "FLASH DRIVE", "DISCO DURO", "SSD", "RAM", "GABINETE", "FUENTE", "ENFRIAMIENTO", "DISIPADOR", "VENTILADOR", "WEBCAM", "DIADEMA", "HEADSET", "BOCINA", "MICROFONO", "MICRÓFONO", "CAMARA", "CÁMARA", "DVR", "NVR", "REGULADOR", "NO BREAK", "UPS", "BIOMETRICO", "BIOMÉTRICO", "TERMINAL", "LECTOR") \
       and not sku_starts("ACC", "CAB", "IMP", "MTF", "PRN", "SCA", "SCN", "TEC", "MOU", "ROU", "SWT", "SWI", "TAR", "TARTPL", "KIT", "COM", "WKS", "POR", "LAP", "AIO", "MEM", "USB", "DDU", "SSD", "GAB", "FUE", "VEN", "ENF", "CAM", "DVR", "NVR", "SER", "SOFAVZ", "SOFZKT", "SOFING", "LICZKT"):
        return "sistemas_operativos"

    # 52. ANTIVIRUS & SEGURIDAD DIGITAL
    is_av_brand = has_word(r'\b(KASPERSKY|NORTON|BITDEFENDER|ESET|MCAFEE|MALWAREBYTES|ACRONIS)\b')
    if (is_av_brand or (has("ANTIVIRUS", "TOTAL SECURITY", "INTERNET SECURITY", "TOTAL PROTECTION") and lacks("DECO", "ROUTER", "MESH", "FIREWALL", "HILLSTONE", "FORTINET", "APPLIANCE", "SWITCH", "CAMARA", "CÁMARA", "NVR", "DVR", "POE", "ADAPTADOR", "LAPTOP", "CANDADO"))) \
       and not sku_starts("GAB", "CAM", "ACP", "ACC", "SUP", "REG", "NBK", "ROU", "SWT", "NVR", "DVR", "CAB"):
        if has("USUARIO", "DISPOSITIVO", "AÑO", "AÑOS", "LICENCIA", "LICENSE", "YEAR", "SUSCRIPCION", "SUSCRIPCIÓN", "ESD", "RENOVACION", "SECURITY", "ANTIVIRUS", "STANDARD", "PLUS", "PREMIUM", "DELUXE", "GAMERS", "ADVANCED", "TOTAL PROTECTION", "TRUE IMAGE", "NORTON 360", "1A", "3D", "5D", "10D"):
            return "antivirus_seguridad_digital"

    # 50. OFIMATICA & PRODUCTIVIDAD
    is_office_kw = has("MICROSOFT 365", "OFFICE 2021", "OFFICE 2024", "OFFICE LTSC", "OFFICE HOGAR", "OFFICE HOME", "OFFICE PERSONAL", "M365", "OFFICE BUSINESS", "VISIO", "PROJECT STD", "PROJECT PRO", "PROJECT PLAN", "POWER BI", "PLANNER", "EXCHANGE ONLINE", "SHAREPOINT", "AUTOCAD", "COPILOT") or (has("OFFICE") and has("FAMILIA", "PERSONAL", "HOGAR", "EMPRESA", "MEDIO ELECTRONICO", "ESD", "FPP", "CSP", "NCE"))
    if sku_starts("NCE", "CSP", "ESD", "SOF", "B-SE") and not sku_starts("SOFAVZ", "SOFZKT", "SOFING", "SOFPDV", "SOFDES", "SOFDAH", "SOFAPL", "SOFCPC") and is_office_kw:
        return "ofimatica_productividad"
    if is_office_kw and not name_u.startswith(("LAPTOP", "NOTEBOOK", "COMPUTADORA", "PC ", "ALL-IN-ONE", "BANDEJA")) \
       and lacks("ALL-IN-ONE", "BANDEJA") and not sku_starts("COM", "LAP", "POR", "AIO", "WKS", "CPU", "MON", "IMP", "ACC"):
        return "ofimatica_productividad"

    # 51. SOFTWARE CONTABLE Y ADMINISTRATIVO
    if sku_starts("SOFAPL", "SOFCPC", "B-SM410ASP", "B-SS000ASP"):
        return "software_contable_administrativo"
    if (has_word(r'\b(ASPEL|CONTPAQI|CONTPAQ)\b') or has("FACTURA ELECTRONICA", "CFDI")) \
       and lacks("SOFT RESTAURANT", "AUDIFONOS", "AUDÍFONOS", "HEADSET", "NOISE", "CANCELLING", "TWS", "NVR", "DVR", "CAMARA", "CÁMARA", "COLORES", "BACO", "CABLE", "LECTOR", "TERMINAL", "FLASH USB", "BATERIA", "BATERÍA") \
       and not sku_starts("BOC", "NVR", "DVR", "ACC", "CAB", "CAR", "KITNTS"):
        return "software_contable_administrativo"

    # 53. GARANTIAS & POLIZAS DE SERVICIO
    is_garantia_sku = sku_starts("EXT") or name_u.startswith(("GARANTIA ", "GARANTÍA ", "EXTENSION DE GARANTIA", "EXTENSIÓN DE GARANTÍA", "LENOVO GARANTIA", "LENOVO GARANTÍA", "LENOVO EXTENSIÓN", "LENOVO EXTENSION", "POLIZA ", "PÓLIZA ", "CARE PACK", "SERVICIO DE GARANTIA")) or name_has("GARANTIA 5", "GARANTÍA 5", "PREMIER SUPPORT PARA", "GARANTIA PARA THINKPAD", "GARANTÍA PARA THINKPAD")
    is_net_or_av_license = sku_starts("LIC") and not sku_starts("LICZKT") and name_u.startswith(("LICENCIA", "GARANTIA", "GARANTÍA"))
    if (is_garantia_sku or is_net_or_av_license or has("CARE PACK", "GARANTIA EXTENDIDA", "GARANTÍA EXTENDIDA", "POLIZA DE SERVICIO", "PÓLIZA DE SERVICIO", "EXTENSION DE GARANTIA", "EXTENSIÓN DE GARANTÍA", "CON-SNT") or (has("SMARTNET") and lacks("SMARTNET CON COSTO", "NI SMARTNET")) or (has("ON-SITE") and sku_starts("EXT", "LIC", "ACC"))) \
       and not sku_starts("SWT", "SWI", "ROU", "ACP", "TEL", "SERHPE", "SERLEN", "SERDDL", "SERDEL", "SERXFN", "STO", "NW1", "WKS", "COM", "LAP", "POR", "MON", "IMP", "NBK", "REG", "SUP", "CAM", "NVR", "DVR"):
        return "garantias_polizas_servicio"

    # =========================================================================
    # TIER 5: MANTENIMIENTO, CANDADOS, HERRAMIENTAS, HUBS, MOCHILAS, BIOMETRIA
    # =========================================================================

    # 58. LIMPIEZA & MANTENIMIENTO
    is_cleaning_item = (
        sku_starts("SLX", "PROLMP", "SABLMP") or
        name_u.startswith(("SILIMPO", "ESPUMA LIMPIADORA", "AIRE COMPRIMIDO", "ALCOHOL ISOPROPILICO", "ALCOHOL ISOPROPÍLICO",
                           "PASTA TERMICA", "PASTA TÉRMICA", "GRASA TERMICA", "GRASA TÉRMICA",
                           "TOALLAS LIMPIADORAS", "TOALLITAS", "LIMPIADOR", "KIT DE LIMPIEZA", "KIT PARA LIMPIEZA",
                           "REMOVEDOR DE POLVO", "REMOVEDOR DE ETIQUETAS", "LUBRICANTE DIELECTRICO", "LUBRICANTE DIELÉCTRICO",
                           "E-FOAM", "E-DEGREASER", "CONTACT CLEANER", "MULTISURFACE CLEANER", "DUSTER ")) or
        name_has("AIRE COMPRIMIDO", "REMOVEDOR DE POLVO", "ESPUMA LIMPIADORA", "TOALLITAS ANTIESTATICAS", "TOALLITAS ANTIESTÁTICAS",
                 "ALCOHOL ISOPROPILICO", "ALCOHOL ISOPROPÍLICO", "LIMPIADOR DE PANTALLAS", "KIT DE LIMPIEZA", "KIT LIMPIADOR",
                 "PASTA TERMICA", "PASTA TÉRMICA", "GRASA TERMICA", "GRASA TÉRMICA", "CLEANING WIPES", "COMPRESSED AIR",
                 "LIMPIEZA DE CIRCUITOS", "TOALLAS HUMEDAS PARA LIMPIEZA", "TOALLAS HÚMEDAS PARA LIMPIEZA",
                 "SILIMEX", "SILIMPO", "PROLICOM", "AFLOJA TODO")
    )
    is_not_cleaning = (
        name_u.startswith(("LAMPARA", "LÁMPARA", "LAMP ", "PROYECTOR", "TINTA", "TONER", "TÓNER", "CARTUCHO",
                           "IMPRESORA", "MULTIFUNCIONAL", "ESCANER", "ESCÁNER", "ROBOT LIMPIADOR", "XEROX ")) or
        sku_starts("SCA", "IMP", "LMP", "TON", "TIN", "PLO") or
        name_has("BANDA DE TRANSFERENCIA", "CONSUMIBLE PARA BADGY")
    )
    if is_cleaning_item and not is_not_cleaning:
        return "limpieza_mantenimiento"

    # 64. CANDADOS DE SEGURIDAD KENSINGTON
    is_lock_name = (
        name_u.startswith(("CANDADO", "N17 CANDADO", "EL CANDADO", "CABLE CON CANDADO", "CABLE DE BLOQUEO",
                           "BLOQUEO DE CHASIS", "BLOQUEO DE CABLE", "ANCLA ADHESIVA", "ANCLA DE ESCRITORIO",
                           "ANCLA PARA CANDADO", "DISPOSITIVO DE ANCLAJE", "ANCLAJE DE SEGURIDAD",
                           "KIT ADAPTADOR DE RANURA DE SEGURIDAD", "KIT DE SEGURIDAD ADAPTADOR DE RANURA",
                           "LLAVE MAESTRA DE 5 MM", "T-LOCK RESETTABLE")) or
        name_has("CANDADO DE SEGURIDAD", "CANDADO PARA LAPTOP", "CANDADO PARA NOTEBOOK", "CANDADO PARA COMPUTADORA",
                 "CANDADO CON LLAVE", "CANDADO DE LLAVE", "CANDADO CON COMBINACION", "CANDADO CON COMBINACIÓN",
                 "CANDADO DE COMBINACION", "CANDADO DE COMBINACIÓN", "CANDADO UNIVERSAL PARA PORTATIL",
                 "CANDADO UNIVERSAL PARA PORTÁTIL", "CANDADO PORTATIL CON LLAVE", "CANDADO PORTÁTIL CON LLAVE",
                 "CANDADO DELGADO CON COMBINACION", "CANDADO DELGADO CON COMBINACIÓN", "CANDADO DOBLE CON LLAVE",
                 "CANDADO LAPTOP", "CANDADO CABLE NANO", "CANDADO SLOT UNIVERSAL", "CANDADO KENSINGTON",
                 "CANDADO T-BAR", "CANDADO NANOSAVER", "CANDADO MICROSAVER", "GUAYA DE SEGURIDAD",
                 "BLOQUEO DE CABLE DE SEGURIDAD", "LENOVO CABLE DE SEGURIDAD", "KEYED CABLE LOCK",
                 "ANCLA ADHESIVA CON RANURA K-SLOT", "ANCLA PARA CANDADO DE SEGURIDAD")
    )
    is_not_lock = (
        name_u.startswith(("MOCHILA", "MALETA", "MALETIN", "MALETÍN", "SWISSMOBILITY", "FUNDA",
                           "ESTACION DE ACOPLAMIENTO", "ESTACIÓN DE ACOPLAMIENTO", "DOCKING",
                           "CABLE DE SEGURIDAD Y SONIDO", "MINI PC", "LAPTOP", "NOTEBOOK", "MONITOR")) or
        sku_starts("PRO", "COM", "WKS", "MON", "PAN", "IMP", "TAB", "CPU", "SER", "RCK", "MAL", "CAB")
    )
    if is_lock_name and not is_not_lock:
        return "candados_seguridad_laptop"

    # 63. HERRAMIENTAS DE SERVICIO TECNICO
    is_tool_name = (
        name_u.startswith(("PONCHADORA", "CRIMPADORA", "PINZA", "PINZAS", "PROBADOR ", "TESTER ",
                           "DESARMADOR", "DESTORNILLADOR", "JUEGO DE DESTORNILLADORES", "JUEGO DE HERRAMIENTAS",
                           "KIT DE HERRAMIENTAS", "KIT BÁSICO NEXXT", "KIT BASICO NEXXT",
                           "CAUTIN", "CAUTÍN", "PELACABLE", "MULTIMETRO", "MULTÍMETRO",
                           "INSERTADORA DE IMPACTO", "HERRAMIENTA DE ", "HERRAMIENTA PARA ", "HERRAMIENTA NEXXT",
                           "CORTADOR Y QUITA FORRO", "530514 CORTADOR")) or
        name_has("PONCHADORA", "CRIMPADORA", "CRIMP TOOL", "PINZA PONCHADORA", "PINZAS PONCHADORAS",
                 "PINZA P/CRIMPIAR", "PINZA P/PONCHAR", "PINZA DE IMPACTO", "PINZA TERMINADO RAPIDO",
                 "PINZA CORTE ", "PROBADOR DE CABLE", "PROBADOR DE VIDEO", "PROBADOR EPCOM",
                 "TESTER DE CABLE", "TESTER DE RED", "JUEGO DE DESTORNILLADORES", "JUEGO DE HERRAMIENTAS",
                 "KIT DE HERRAMIENTAS", "HERRAMIENTA DE CRIMPEO", "HERRAMIENTA PARA CRIMPEAR",
                 "HERRAMIENTA DE PERFORACIÓN", "HERRAMIENTA DE FUSIÓN",
                 "HERRAMIENTA PARA SOSTENER", "PELACABLE", "MULTIMETRO", "MULTÍMETRO", "INSERTADORA DE IMPACTO")
    )
    is_not_tool = (
        name_u.startswith(("PANEL DE PARCHEO", "PATCH PANEL", "CONECTOR", "JACK ", "PLUG ", "PATCH CORD",
                           "BOBINA", "SOPORTE", "BRAZO", "RING ", "CARCASA", "TECLADO", "KIT DE LEGALIZ", "PLANNER ",
                           "MOUSE PAD", "MOUSEPAD", "FOLKSAFE -BNC-CONECTOR")) or
        name_has("WINDOWS", "LICENCIA", "ROK", "MICROSOFT", "SOFTWARE", "KIT DE LEGALIZACION")
    )
    if is_tool_name and not is_not_tool:
        return "herramientas_servicio_tecnico"

    # 62. HUBS, DOCKS & ESTACIONES
    is_hub_dock = (
        sku_starts("DOC", "ACCSTY580") or
        name_u.startswith(("HUB ", "DOCKING", "ESTACION DE ACOPLAMIENTO", "ESTACIÓN DE ACOPLAMIENTO",
                           "CONCENTRADOR USB", "NACEB HUB", "HP DOCKING", "LENOVO THINKPAD USB4 DOCK",
                           "SURFACE USB4 DOCK", "MICROSOFT USB-C TRAVEL HUB", "USB TIPO C DE 6 PUERTOS",
                           "USB TIPO C DE 9 PUERTOS", "ADAPTADOR NACEB HUB", "LOGITECH - DOCKING STATION",
                           "LOGITECH SWYTCH")) or
        name_has("DOCKING STATION", "ESTACION DE ACOPLAMIENTO", "ESTACIÓN DE ACOPLAMIENTO",
                 "HUB USB", "HUB MULTIPUERTO", "HUB MULTIPUESTO", "HUB MULTIPUESTOS",
                 "CONCENTRADOR USB", "TRAVEL HUB", "USB4 DOCK", "THUNDERBOLT DOCK",
                 "ADAPTADOR MULTIPUERTO", " - HUB - ", "HUB CONTROLADOR", "HUB DBUGG",
                 "HUB 3 EN 1", "HUB 4 EN 1", "HUB 5 EN 1", "HUB 6 EN 1", "HUB 7 EN 1",
                 "HUB 8 EN 1", "HUB 9 EN 1", "HUB 10 EN 1", "HUB 11 EN 1", "HUB 12 EN 1",
                 "HUB DE 4 PUERTOS", "HUB DE 7 PUERTOS")
    )
    is_not_hub = (
        name_u.startswith(("PANTALLA ", "MONITOR ", "SMART TV", "KIT DE ALARMA", "SMARTHUB", "HUB INTELIGENTE",
                           "CABLE DE CARGA", "LOGITECH RALLY TABLE HUB", "VIDEO CONFERENCIA")) or
        name_has("TAPO H1", "TAPO(", "ALARMA", "ORVIBO", "SMART TV", "SEÑALIZACIÓN DIGITAL", "RALLY TABLE HUB", "TECLADO", "MONITOR") or
        sku_starts("BIZ", "MON", "TV", "KITHKV", "TEC", "MT0", "MT1", "MT6", "MT8")
    )
    if is_hub_dock and not is_not_hub:
        return "hubs_docks_estaciones"

    # 60. MOCHILAS, FUNDAS Y MALETINES
    is_bag_name = (
        (sku_starts("MAL", "AN1", "AN7") and name_lacks("NOTEBOOK STAND", "SOPORTE", "BASE")) or
        name_u.startswith(("MOCHILA", "MALETIN", "MALETÍN", "MALETA ", "BACKPACK", "BOLSO ", "MINI BOLSA",
                           "PORTAFOLIO", "FUNDA PARA LAPTOP", "FUNDA PARA NOTEBOOK", "FUNDA UNIVERSAL PARA NETBOOK",
                           "FUNDA NEOPRENO", "SLEEVE ", "SWISSMOBILITY MALETA")) or
        name_has("MOCHILA PARA", "MOCHILA DELL", "MOCHILA HP", "MOCHILA LENOVO", "MOCHILA VORAGO",
                 "FUNDA PARA LAPTOP", "FUNDA PARA NOTEBOOK", "MALETIN PARA", "MALETÍN PARA",
                 "PORTAFOLIO PARA LAPTOP", "BOLSO PARA LAPTOP", "MALETA PARA LAPTOP",
                 "NOTEBOOK CARRYING BACKPACK", "CARRYING CASE", "CASE LOGIC", "FUNDA NEOPRENO",
                 "MALETIN BACKPACK", "MALETÍN BACKPACK", "ECOLOOP ESSENTIAL BACKPACK", "ECOLOOP SLIM BRIEFCASE")
    )
    is_not_bag = (
        name_u.startswith(("LAPTOP", "NOTEBOOK", "COMPUTADORA", "TABLET", "TABLETA", "IPAD", "MATEPAD",
                           "ROTULADOR", "PROYECTOR", "BOCINA", "AUDIFONO", "AUDÍFONO", "DIADEMA",
                           "MOUSE", "RATON", "RATÓN", "MINI RATON", "MINI RATÓN", "KIT DE TECLADO",
                           "TECLADO", "EXTENSOR", "GABINETE", "ESTUCHE PROTECTOR PARA GABINETE",
                           "CARCASA PARA MACBOOK", "TECH 21 - CASE - CASE FOR AIRPODS",
                           "FUNDA PROTECTORA DE GOMA HONEYWELL", "FUNDA DE AGARRE", "FUNDA DE USO RUDO",
                           "MALETA DE DEMOSTRACIÓN", "MALETA DE DEMOSTRACION")) or
        sku_starts("BOC", "ROT", "KIT", "MOU", "PRO", "LAP", "POR", "COM", "TAB", "IPD") or
        name_has("POWER STRIP", "MULTICONTACTO", "REGULADOR", "GOMA HONEYWELL", "TERMINAL CK", "TERMINAL EDA",
                 "PARA TERMINAL", "PARA SAMSUNG GALAXY", "PARA LENOVO TAB", "PARA LENOVO M9", "PARA LENOVO P11",
                 "AIRPODS", "MALETA DE DEMOSTRACIÓN", "MALETA DE DEMOSTRACION")
    )
    if is_bag_name and not is_not_bag:
        return "mochilas_fundas_maletines"

    # 34. BIOMETRIA Y ACCESO (Escuadrones 4 + 5)
    if (has("CONTROL DE ACCESO", "CONTROL DE ASISTENCIA", "CONTROL DE TIEMPO Y ASISTENCIA", "LECTOR DE HUELLA", "LECTORA DE HUELLA", "HUELLA DIGITAL",
            "TERMINAL BIOMETRICA", "TERMINAL BIOMÉTRICA", "TERMINAL FACIAL", "MIN MOE", "BIOMETRICO", "BIOMÉTRICO", "RELOJ CHECADOR",
            "CHECADOR DE HUELLA", "CHECADOR BIOMÉTRICO", "CHECADOR BIOMETRICO", "ENROLADOR",
            "CHAPA MAGNETICA", "CHAPA MAGNÉTICA", "CERRADURA INTELIGENTE", "CERRADURA DE PUERTA WI-FI", "CERRADURA MAGNÉTICA", "CERRADURA MAGNETICA",
            "CERRADURA ELÉCTRICA", "CERRADURA ELECTRICA", "TARJETA RFID", "TAG RFID", "BOTON LIBERADOR", "BOTÓN LIBERADOR", "CONTRACERRADURA",
            "LECTORA DE PROXIMIDAD", "LECTORA DE TARJETAS MIFARE", "TORNIQUETE", "VIDEOPORTERO", "VIDEO PORTERO", "FRENTE DE CALLE", "INTERFONO IP")
        or ("CONTROL ACCESO" in sub_u and not name_u.startswith("MALETA DE DEMOSTRAC"))) \
       and lacks("IPAD", "TABLET", "TABLETA", "APPLE", "M2", "WIFI + CELL", "SPACE GRAY", "MATEPAD", "SMARTPHONE", "DVR", "NVR", "GALAXY ",
                 "ALARM SYSTEM", "Z-PERFORM", "DYE SUB OVERLAY", "ADHESIVO ACRÍLICO", "ADHESIVO ACRILICO",
                 "MALETA DE DEMOSTRACIÓN", "MALETA DE DEMOSTRACION", "ESTACIÓN MOBILIARIA") \
       and not sku_starts("CEL", "SMA", "IMP", "MTF", "PLO", "SCA", "SWT", "SWI", "ROU", "ACP", "ANT", "CAM", "NVR", "DVR", "GRD", "TEL", "EST"):
        return "control_acceso_biometricos"

    # =========================================================================
    # TIER 6: PERIFERICOS, AUDIO, CABLES, ENERGIA Y PUNTO DE VENTA
    # =========================================================================

    # 13. COMBOS TECLADO Y RATON
    is_combo_name = (
        name_has("KIT TECLADO Y", "KIT DE TECLADO Y", "KIT TECLADO+MOUSE", "KIT TECLADO + MOUSE",
                 "KIT TECLADO MOUSE", "KIT TECLADO CON BOCINAS Y MOUSE", "KIT TECLADO ESTANDAR Y MOUSE",
                 "KIT DE MOUSE Y TECLADO", "COMBO TECLADO", "TECLADO Y MOUSE", "TECLADO Y RATON",
                 "TECLADO Y RATÓN", "TECLADO, MOUSE", "TECLADO, RATÓN", "TECLADO, RATON",
                 "KEYBOARD AND MOUSE SET", "KEYPAD AND MOUSE SET", "KEYBOARD, MOUSE AND",
                 "WIRELESS COMBO", "MK250", "MK295", "KM726") or
        (sku_starts("KIT") and name_has("TECLADO") and name_has("MOUSE", "RATON", "RATÓN")) or
        (sku_starts("KIT") and name_has("4 EN 1", "3 EN 1") and has("TECLADO") and has("MOUSE", "RATON", "RATÓN"))
    )
    is_not_combo = (
        name_u.startswith(("BANDEJA", "DESCANSAPIES", "REPOSAMUÑECAS", "REPOSAMUNECAS", "ALFOMBRILLA",
                           "MOUSEPAD", "MOUSE PAD", "TAPETE", "COMPUTADORA", "WORKSTATION", "SERVIDOR",
                           "PC ", "CONSOLA LCD", "IMAC", "LAPTOP", "NOTEBOOK", "ALL IN ONE")) or
        sku_starts("CPU", "WKS", "SER", "LAP", "POR", "AIO", "COM", "STO", "NW1") or
        (name_u.startswith("TECLADO ") and not name_has("MOUSE", "RATON", "RATÓN", "MK250", "MK295", "COMBO", "KIT "))
    )
    if is_combo_name and not is_not_combo:
        return "combos_teclado_mouse"

    # 29. MICROFONOS
    is_mic_name = (
        sku_starts("MIC") or
        name_u.startswith(("MICROFONO", "MICRÓFONO", "MICROPHONE", "YEYIAN MICRÓFONO", "YEYIAN MICROFONO")) or
        name_has("MICRÓFONO DE", "MICROFONO DE", "MICRÓFONO PROFESIONAL", "MICROFONO PROFESIONAL",
                 "MICRÓFONO CONDENSADOR", "MICROFONO CONDENSADOR", "MICRÓFONO INALÁMBRICO", "MICROFONO INALAMBRICO",
                 "MICRÓFONO GAMER", "MICROFONO GAMER", "MICRÓFONO OMNIDIRECCIONAL", "MICROFONO OMNIDIRECCIONAL",
                 "MICRÓFONO MINI", "MICROFONO MINI", "KIT DE MICRÓFONO", "KIT DE MICROFONO",
                 "RALLY MIC POD", "EXPANSION MIC", "QUANTUM STREAM", " - MICRÓFONO - ", " - MICROFONO - ")
    )
    is_not_mic = (
        name_u.startswith(("BOCINA", "BAFLE", "HOMEPOD", "MY5G", "MY5H", "MJ2C", "COMPUTADORA", "PROYECTOR",
                           "SISTEMA DE PUNTO DE VENTA", "TERMINAL", "TECLADO", "MOUSE", "DIADEMA", "AUDIFONO",
                           "AUDÍFONO", "AURICULAR", "HEADSET", "CAMARA", "CÁMARA", "WEBCAM", "WEBCAB",
                           "SWITCH KVM", "BENQ INSTANT", "PUENTE DE AUDIO", "BASE ", "SOPORTE", "BRAZO",
                           "CABLE", "ADAPTADOR", "LOGITECH RALLY MIC POD MOUNT", "LOGITECH RALLY TABLE",
                           "MÓDULO OPS", "MODULO OPS")) or
        sku_starts("CPU", "PRO", "TER", "TEC", "MOU", "CAM", "DVR", "NVR", "GAB", "CAB", "AB0") or
        name_has("MOUNT", "SOPORTE DE MICRÓFONO", "SOPORTE PARA MICRÓFONO", "ABRAZADERA", "KARAOKE", "BAFLE", "BAFFLE",
                 "DIADEMA", "HEADSET", "AUDIFONOS", "AUDÍFONOS", "AURICULAR", "HOMEPOD", "COUPLER", "AUDIO CONFERENCIA TRIO")
    )
    if is_mic_name and not is_not_mic:
        return "microfonos"

    # 30. WEBCAMS & VIDEOCONFERENCIA
    is_webcam_vc = (
        name_has("CAMARA WEB", "CÁMARA WEB", "WEBCAM", "WEBCAB", "PANACAST", "POLY STUDIO",
                 "VIDEO CONFERENCIA", "VIDEOCONFERENCIA", "VÍDEOCONFERENCIA", "CONFERENCECAM",
                 "RALLY BAR", "RALLY PLUS", "LOGITECH RALLY - KIT", "LOGITECH RALLY - CÁMERA",
                 "LOGITECH GROUP", "LOGITECH ROOMMATE", "LOGITECH SIGHT", "LOGITECH SCRIBE",
                 "LOGITECH TAP", "BRIO 100", "BRIO 105", "BRIO 300", "BRIO 305", "BRIO 500",
                 "MEETUP", "EQUIO DE AUDIO CONFERENCIA TRIO", "AUDIO CONFERENCIA TRIO", "INSTANT SHOW") or
        has_word(r'\b(C920[SE]?|C922[X]?|C925E?|C930[EC]?)\b', name_u)
    )
    is_not_webcam_vc = (
        name_u.startswith(("BATERIA", "BATERÍA", "CORREA", "FUNDA", "CABLE", "153737 CABLE", "SOPORTE", "BRAZO",
                           "MONTURA", "KIT DE MONTAJE", "KIT DE INSTALACIÓN", "KIT DE INSTALACION",
                           "MANDO A DISTANCIA", "REMOTE CONTROL", "TAPA DE PRIVACIDAD", "TRIPIE", "TRÍPIE", "TRIPIÉ",
                           "TRIPODE", "TRÍPODE", "LOGITECH - POWER ADAPTER", "LOGITECH CAT5E",
                           "LOGITECH EXPANSION MIC", "MICRÓFONO", "MICROFONO", "PUENTE DE AUDIO",
                           "KIT DE ADAPTADOR DE CORRIENTE", "DIADEMA", "AUDIFONO", "AUDÍFONO",
                           "JABRA - EVOLVE", "LAPTOP", "NOTEBOOK", "COMPUTADORA", "MONITOR", "SWITCH", "ROUTER", "LICENCIA")) or
        sku_starts("BAT", "CAB", "AB0", "MM0", "BOC", "LIC") or
        name_has("TAPA DE PRIVACIDAD", "POWER ADAPTER KIT", "MANDO A DISTANCIA", "REMOTE CONTROL",
                 "KIT DE MONTAJE", "KIT DE INSTALACION", "KIT DE INSTALACIÓN", "MONTURA PARA",
                 "SOPORTE PARA MONTAJE", "SOPORTE UNIVERSAL PARA PROYECTOR", "EXTENSIÓN ACTIVA", "EXTENSION ACTIVA")
    )
    if is_webcam_vc and not is_not_webcam_vc:
        return "webcams_videoconferencia"

    # 21. CARGADORES, BATERIAS & POWER BANKS
    is_ups_battery = (sku_starts("BAT") and not has("SISTEMA UPS DE CC", "UPS DE CC")) or has("REPLACEMENT BATTERY CARTRIDGE", "BATTERY PACK", "CARTUCHO DE BATERIA", "CARTUCHO DE BATERÍA", "CARTUCHO DE BATERIAS", "CARTUCHO DE BATERÍAS", "BANCO DE BATERIA", "BANCO DE BATERÍA", "BANCO DE BATERIAS", "BANCO DE BATERÍAS", "BATERIA DE REEMPLAZO", "BATERÍA DE REEMPLAZO", "BATERIAS DE REEMPLAZO", "BATERÍAS DE REEMPLAZO")
    is_power_station = sku_starts("CEN") or has("POWER STATION", "CENTRAL ELECTRICA PORTATIL", "CENTRAL ELÉCTRICA PORTÁTIL", "PANEL SOLAR PORTATIL", "PANEL SOLAR PORTÁTIL")
    if (is_ups_battery or is_power_station or name_u.startswith(("BATERIA", "BATERÍA", "CARGADOR", "POWER BANK", "ELIMINADOR")) or has("POWER BANK", "POWERBANK", "BATERIA PORTATIL", "BATERÍA PORTÁTIL", "BATERIA EXTERNA", "BATERÍA EXTERNA", "BATERIA PARA LAPTOP", "BATERÍA PARA LAPTOP", "CARGADOR PARA LAPTOP") or (has("CARGADOR") and has("PARED", "LAPTOP", "TIPO C", "USB-C", "CARRO", "AUTO", "INALAMBRICO", "INALÁMBRICO", "RAPIDO", "RÁPIDO")) or has("ELIMINADOR UNIVERSAL", "ELIMINADOR DE CORRIENTE")) \
       and not sku_starts("CEL", "SMA", "NBK", "NOB", "UPS", "CAB", "SIL", "MAL", "AUD", "BOC", "CAM", "IMP", "PRN", "PRO", "INV", "REG", "SUP", "PDU") \
       and not name_u.startswith(("SMARTPHONE", "CELULAR", "NO BREAK", "NO-BREAK", "UPS ", "REGULADOR", "CABLE ", "SILLA ", "MALETIN", "MALETÍN", "MOCHILA", "IMPRESORA", "BASE CARGADORA PARA CONSOLA")) \
       and not (has("POWER BANK") and has("NO INCLUIDA", "NO INCLUIDO")) \
       and lacks("TAPE", "AUTOLOADER", "STORAGE MSL", "LTO-8", "LTO-9", "SAS DRIVE", "FIBRE CHANNEL", "KIOSCO", "MINI KIOSCO", "TERMINAL DE COBRO", "PLUG PARA CARGADOR", "BASE DE CARGA HONEYWELL", "CARGADOR AUTOMATICO DE 50 TARJETAS", "CARGADOR AUTOMÁTICO DE 50 TARJETAS", "IMPRESORA EVOLIS"):
        return "cargadores_baterias_powerbanks"

    # 27. DIADEMAS & HEADSETS
    is_headset_name = (
        name_has("DIADEMA", "HEADSET", "AUDIFONO", "AUDÍFONO", "EARBUD", "EARPHONE", "AURICULAR",
                 "AIRPODS", "FREEBUDS", "BLACKWIRE", "EVOLVE2", "EVOLVE3", "EVOLVE 10", "EVOLVE 20",
                 "EVOLVE 30", "EVOLVE 40", "EVOLVE 65", "EVOLVE 75", "EVOLVE - ", "BIZ 1100", "BIZ 1500",
                 "BIZ 2300", "BIZ 2400", "VOYAGER 5200", "VOYAGER 43", "VOYAGER FOCUS", "ENGAGE 30",
                 "ENGAGE 40", "ENGAGE 50", "ENGAGE 65", "ENGAGE 75", "ENGAGE - ", "HW510", "HW520",
                 "H390 ", "G535", "RAZER KRAKEN", "BLACKSHARK", "ASTRO GAMING A10", "LOGITECH ZONE") or
        (name_has("MANOS LIBRES") and name_lacks("MONITOR", "VIDEO PORTERO", "VIDEOPORTERO", "PORTERO", "ALTAVOZ", "SPEAKER")) or
        (sku_starts("BOC", "MM0", "MM1", "MM2", "100") and sub_has("AUDIFONO", "AUDÍFONO", "DIADEMA", "HEADSET", "AURICULARES Y MANOS LIBRES"))
    )
    is_not_headset = (
        name_u.startswith(("CABLE", "ADAPTADOR", "CONVERTIDOR", "DIVISOR", "BASE ", "SOPORTE", "ESPONJA",
                           "ALMOHADILLA", "EAR CUSHION", "EARCUSHION", "JABRA ENGAGE 40/50II EARCUSHION",
                           "JABRA - EAR CUSHION", "JABRA LINK", "JABRA GN12", "JABRA SMART CORD",
                           "JABRA SPEAK", "TELEFONO", "TELÉFONO", "PROYECTOR", "ESCRITORIO",
                           "KIT DE LIMPIEZA", "KIT TECLADO", "KIT ", "MICRÓFONO", "MICROFONO",
                           "TECH 21 - CASE", "CARGADOR ", "BOCINA", "BARRA DE SONIDO", "BAFLE",
                           "XTECH XTH-690 - BASE", "MONITOR ", "VIDEOPORTERO", "VIDEO PORTERO")) or
        sku_starts("CAB", "AB0", "ESC", "PRO", "TEL", "KIT", "MIC") or
        name_has("ESPONJA PARA AURICULARES", "EAR CUSHION", "EARCUSHION", "BASE HEADSET", "BASE PARA AURICULAR",
                 "CABLE PARA AURICULARES", "ADAPTADOR PARA AURICULAR", "ADAPTADOR DE INTERRUPTOR",
                 "GANCHO PARA AURICULARES", "PROCESADOR DE AUDIO PARA TELÉFONO", "CASE FOR AIRPODS",
                 "CABLE STEREO", "JBL CLIP 4", "VIDEO PORTERO", "VIDEOPORTERO") or
        (name_has("HANDSET") and name_lacks("JABRA"))
    )
    if is_headset_name and not is_not_headset:
        return "diademas_headsets"

    # 28. BOCINAS, BARRAS DE SONIDO & BAFLES
    is_speaker_name = (
        sku_starts("BOC", "AUD") or
        name_u.startswith(("BOCINA", "BARRA DE SONIDO", "SOUNDBAR", "BAFLE", "TORRE DE SONIDO", "ALTAVOZ",
                           "AMAZON ECHO", "HOMEPOD", "MY5G", "MY5H", "MJ2C", "CREATIVE STAGE", "JABRA SPEAK",
                           "SISTEMA DE AUDIO", "JBL ", "SOUNDCORE", "LOGITECH - SPEAKER", "LOGITECH RALLY - ALTAVOZ",
                           "KLIP XTREME KBS-", "KLIP XTREME KSB-", "KLIP XTREME PORT TWS", "XTECH XTS-",
                           "LENOVO - AUDIO SYSTEM")) or
        name_has("BOCINA", "BOCINAS", "BARRA DE SONIDO", "SOUNDBAR", "BAFLE", "BAFFLE", "TORRE DE SONIDO",
                 "ALTAVOZ", "ALTAVOCES", "SPEAKERPHONE", "SPEAKER", "ECHO DOT", "ECHO SHOW", "HOMEPOD",
                 "WONDERBOOM", "PARTYBOX", "THINKSMART BAR", "AUDIO SYSTEM")
    )
    is_not_speaker = (
        name_u.startswith(("MONITOR", "PANTALLA", "PROYECTOR", "PROYECTO ", "MINI PROYECTOR", "LASER CINEMA",
                           "LASER TV", "SMARTWATCH", "CONSOLA", "SWITCH KVM", "CONVERTIDOR", "CABLE",
                           "SOPORTE", "BRAZO", "BASE PARA BOCINAS", "TÓTEM", "TOTEM", "SISTEMA POS", "FIRE TV",
                           "AMAZON FIRE TV", "TARJETA DE SONIDO", "KIT ", "NVR", "DVR", "CAMARA", "CÁMARA",
                           "VIDEO PORTERO", "PORTERO", "TELEFONO", "TELÉFONO", "TROMPETA", "SIRENA",
                           "JBL QUANTUM", "MINI BOLSA", "BOSCH")) or
        sku_starts("PRO", "CAB", "KIT", "LTV", "CPU", "TAR", "MON", "PAN", "NVR", "DVR", "CAM", "TEL", "MIC", "MAL", "ID0", "ID2") or
        name_has("BASE PARA BOCINAS", "SOPORTE BARRA DE SONIDO", "COVER PB", "TROMPETA", "SIRENA",
                 "FIRE TV", "SMARTWATCH", "CONSOLA ARCADE", "SWITCH KVM", "TARJETA DE SONIDO", "TÓTEM INTERACTIVO")
    )
    if is_speaker_name and not is_not_speaker:
        return "bocinas_sonido"

    # 40. CABLEADO ESTRUCTURADO (Escuadrones 4 + 5: antes de cables_adaptadores para capturar Patch Cords UTP)
    is_cabling_title = name_has(
        "BOBINA", "PATCH", "CABLE UTP", "CABLE DE RED", "CABLE DE PARCHEO", "CABLE DE INTERCONEX",
        "CABLE ETHERNET", "CONECTOR RJ45", "CONECTOR PLUG", "CONECTOR JACK", "CONECTOR MODULAR",
        "PLUG RJ", "PLUG MODULAR", "PLUGS PASS", "RJ45 CONNECTOR", "JACK ", "KEYSTONE", "KEYST. JACK",
        "FACEPLATE", "TAPA DE PARED", "TAPA (FACEPLATE)", "TAPA PARA CAJA", "TAPA HDMI", "TAPA SVGA",
        "PLACA KEYSTONE", "PLACA DE MONTAJE", "PLACA FRONTAL", "TABLERO DE CONEXIONES", "PANEL DE PARCHEO",
        "SURFACE MOUNT", "TERMINACIÓN MODULAR", "TERMINACION MODULAR", "MODULAR INSERT", "INSERTO ",
        "COPLE MODULAR", "MODULO CIEGO", "CLIP MONTAJE PATCH", "TERMINADORA PARA PATCH",
        "BOTA RJ45", "BOTA PARA RJ45", "NETWORK COUPLER"
    )
    if (is_cabling_title or has("BOBINA UTP", "BOBINA DE CABLE", "CABLE UTP", "CONECTOR RJ45", "JACK RJ45", "PATCH CORD", "PATCH PANEL", "FACEPLATE") or sub_has("PATCH CORD", "PATCH PANEL", "BOBINAS DE CABLES")) \
       and not sku_starts("SWT", "SWI", "ROU", "WIF", "ACP", "ANT", "IMP", "MTF", "PLO", "SCA", "CAM", "NVR", "DVR", "GRD", "ROT", "LFD", "MON", "PAN", "CJS", "CJN") \
       and not name_u.startswith(("SWITCH", "ROUTER", "PINZA", "PROBADOR", "HERRAMIENTA", "NEXXT - HERRAMIENTA", "KIT DE HERRAMIENTAS", "ORGANIZADOR", "GABINETE", "RACK", "CABLE COAXIAL", "CABLE DAHUA PFM941", "SAXXON WB", "SAXXON SX", "CARRO DE CARGA", "CONVERTIDOR USB", "PAR DE TRANSCEPTORES", "VIDEO BALUN", "TRANSCEPTOR", "MODULO SFP", "MÓDULO SFP", "ADAPTADOR POE", "INYECTOR", "EXTENSOR", "DOCKING", "E-BOARD", "KIT EXTENSOR", "ROTULADOR", "ZEBRA - PLACA", "CABLE HDMI")) \
       and lacks("MONOMODO", "MULTIMODO", "OS2", "OM3", "OM4", "FIBRA ÓPTICA", "FIBRA OPTICA", "SFP+", "QSFP+", "PINZA", "PONCHADORA", "PROBADOR DE CABLE", "CARRO DE CARGA", "VIDEO BALUN", "TRANSCEPTOR PASIVO", "CONVERTIDOR USB", "ADAPTADOR USB", "ADAPTADOR POE", "INYECTOR POE", "EXTENSOR DE VIDEO", "DOCKING", "HERRAMIENTA", "ESCÁNER DE CÓDIGO", "ESCANER DE CODIGO", "CABLE HDMI", "RG59", "RG6"):
        return "cableado_estructurado"

    # 59. CABLES & ADAPTADORES
    is_cable_adapt = (
        (sku_starts("CAB", "AB0", "AB3") and not name_u.startswith(("UBIQUITI DREAM ROUTER", "KLIP XTREME - MOUNTING BRACKET"))) or
        name_u.startswith(("CABLE ", "CONVERTIDOR", "COMPACTO CONVERTIDOR", "DIVISOR ",
                           "EXTENSOR HDMI", "EXTENSOR WIRELESS HD", "VIDEO SPLITTER", "SPLITTER HDMI",
                           "TRANSMISOR DE VIDEO", "HPE CABLE", "CISCO CABLE", "153737 CABLE", "5501UE ",
                           "SAXXON WB", "XTECH - ALTA VELOCIDAD - CABLE", "XTECH - HDMI SPLITTER",
                           "XTECH - USB CABLE", "XTECH XTC", "LOGITECH STRONG - CABLE", "ZEBRA - CABLE",
                           "DATAMAX - CABLE", "HONEYWELL - PC42E-T - POWER CORD", "XPLORE - CABLE",
                           "APC - CABLE PROLONGADOR", "JABRA GN12", "JABRA SMART CORD",
                           "JABRA LINK 230", "JABRA LINK 265")) or
        (name_u.startswith("ADAPTADOR") and name_has("HDMI", "VGA", "DVI", "DISPLAYPORT", "MINI DISPLAYPORT",
                                                     "USB", "TIPO C", "TYPE-C", "LIGHTNING", "STEREO", "3.5",
                                                     "AUDIO", "SERIAL", "DB9", "RJ45", "ETHERNET", "OTG",
                                                     "BALUN", "BNC", "CABLE", "VIDEO", "NIC")) or
        name_has("CABLE HDMI", "CABLE DISPLAYPORT", "CABLE MINI DISPLAY", "CABLE USB", "CABLE TIPO C",
                 "CABLE LIGHTNING", "CABLE VGA", "CABLE DVI", "CABLE AUDIO", "CABLE STEREO",
                 "CABLE PODER", "CABLE DE PODER", "CABLE DE CORRIENTE", "CABLE DE ALIMENTACIÓN",
                 "CABLE DE ALIMENTACION", "CABLE ALIMENTACION", "CABLE SATA", "CABLE COAXIAL",
                 "CABLE DE CARGA", "CABLE ROLLOVER", "CABLE ÓPTICO ACTIVO HDMI", "CABLE OPTICO ACTIVO HDMI",
                 "CABLE EXTENSIÓN", "CABLE EXTENSION", "USB CABLE", "HDMI CABLE", "POWER CORD",
                 "ADAPTADOR HDMI", "ADAPTADOR DISPLAYPORT", "ADAPTADOR MINI DISPLAYPORT", "ADAPTADOR VGA",
                 "ADAPTADOR DVI", "ADAPTADOR USB", "ADAPTADOR TIPO C", "ADAPTADOR DE CABLE",
                 "ADAPTADOR OTG", "ADAPTADOR STEREO", "CONVERTIDOR DE VIDEO", "CONVERTIDOR VGA",
                 "CONVERTIDOR HDMI", "VIDEO SPLITTER", "HDMI SPLITTER", "EXTENSOR HDMI", "EXTENSOR WIRELESS HD")
    )
    is_not_cable = (
        sku_starts("TAR", "BOC", "LCT", "MOU", "TEC", "IMP", "SCA", "KIT", "CON", "GAB", "NBK", "NOB", "UPS", "INV", "CPU",
                   "ROU", "SUP", "REG", "ROT", "ROB", "CJN", "CJS", "CAM", "PDU", "SWT", "SWI", "RCK",
                   "MON", "PAN", "LAP", "POR", "COM", "WKS", "SER", "STO", "DDU", "SSD", "MEM", "BAT", "NVR", "DVR", "GRD") or
        name_u.startswith(("MONITOR", "PANTALLA", "LAPTOP", "NOTEBOOK", "DESKTOP", "COMPUTADORA",
                           "ORGANIZADOR", "FUENTE DE PODER", "SAXXON PSU", "CARGADOR", "MODULO INTERACTIVO",
                           "ENFRIADOR", "HUB ", "DOCKING", "CONCENTRADOR", "DIADEMA", "AUDIFONO", "AUDÍFONO",
                           "AURICULAR", "KIT DE ", "TARJETA ", "PDU ", "BARRA ", "SWITCH ", "ROUTER",
                           "BASE DE CARGA", "ADAPTADOR DE CORRIENTE", "ADAPTADOR DE BUS", "ADAPTADOR EPCOM",
                           "ADAPTADOR DE ENERG", "ADAPTADOR POE", "ADAPTADOR PARA RACK")) or
        name_has("INALÁMBRIC", "INALAMBRIC", "WI-FI", "WIFI", "WIRELESS LAN", "BLUETOOTH", "MBPS", "DUAL BAND",
                 "DOBLE BANDA", "REDES INALAMBRICAS", "REDES INALÁMBRICAS", "PCI-EXPRESS", "PCIE",
                 "BUS DE HOST", "SFP+", "FIBRA ÓPTICA", "FIBRA OPTICA", "CONVERTIDOR DE MEDIOS", "BOBINA UTP", "BOBINA DE CABLE", "PATCH CORD", "CABLE DE PARCHEO",
                 "CABLE UTP", "ENFRIADOR NEXTEP", "MODULO INTERACTIVO", "CARGADOR INALÁMBRICO",
                 "BASE DE CARGA", "ADAPTADOR DE CORRIENTE", "INTERRUPTOR DE GANCHO")
    )
    if is_cable_adapt and (not is_not_cable or name_has("EXTENSOR WIRELESS HD", "TRANSMISOR DE VIDEO INALÁMBRICO HDMI")):
        return "cables_adaptadores"

    # 19. NO BREAKS & UPSS
    is_ups = (
        sku_starts("NBK", "NOB", "UPS", "INV")
        or name_u.startswith(("NO BREAK", "NO-BREAK", "UPS ", "SISTEMA UPS", "INVERSOR"))
        or has("NO-BREAK", "NO BREAK", "SISTEMA UPS", "UPS INTERACTIVO", "UPS ON-LINE", "SMART-UPS", "BACK-UPS", "EASY UPS", "BATTERY BACKUP", " - UPS - ", "UPS - LINE INTERACTIVE", "UPS DE CC")
    )
    if is_ups \
       and not name_u.startswith(("TARJETA", "KIT DE RIELES", "RIEL", "CABLE", "TRANSFORMADOR", "BATERIA DE REEMPLAZO", "BATERÍA DE REEMPLAZO", "CARTUCHO DE BATERIA", "CARTUCHO DE BATERÍA", "BANCO DE BATERIA", "BANCO DE BATERÍA")) \
       and lacks("BATERIA PORTATIL", "BATERÍA PORTÁTIL", "POWER BANK", "STEP-DOWN TRANSFORMER", "TRANSFORMADOR DE BAJADA", "BATTERY PACK", "REPLACEMENT BATTERY") \
       and not sku_starts("ACC", "CAB", "TAR", "BAT", "REG", "SUP", "PDU"):
        return "no_breaks_ups"

    # 20. REGULADORES DE VOLTAJE & SUPRESORES / PDUs
    if (sku_starts("REG", "SUP", "PDU") or name_u.startswith(("REGULADOR", "SUPRESOR", "PDU ", "PROTECTOR DE VOLTAJE")) or has("REGULADOR DE VOLTAJE", "REGULADOR AUTOMATICO", "REGULADOR AUTOMÁTICO", "SUPRESOR DE PICOS", "SUPRESOR DE SOBREVOLTAJE", "BARRA DE CONTACTOS", "MULTICONTACTO", "CENTRO MULTICONTACTO", "AUTOMATIC VOLTAGE REGULATOR", "SURGE PROTECTOR", "FORZA SURGE", "BASIC RACK-MOUNT PDU", "UNIDAD DE DISTRIBUCION DE ALIMENTACION", "UNIDAD DE DISTRIBUCIÓN DE ALIMENTACIÓN", "PROTECTOR DE VOLTAJE")) \
       and lacks("NO-BREAK", "NO BREAK", "UPS", "VENTILADORES", "ARGB", "ESTACION DE CARGA", "ESTACIÓN DE CARGA") \
       and not sku_starts("NBK", "NOB", "UPS", "CPU", "COM", "WKS", "LAP", "AIO", "SER"):
        return "reguladores_voltaje"

    # 47. ETIQUETAS & RIBBONS (Escuadrones 4 + 5: antes de Punto de Venta!)
    is_label_ribbon = (
        sku_starts("RIB", "ETI", "CIN") or
        name_u.startswith(("ROLLO TÉRMICO", "ROLLO TERMICO", "ROLLO BOND", "ROLLO AUTOCOPIANTE",
                           "ROLLO ETIQUETA", "ETIQUETA TÉRMIC", "ETIQUETA TERMIC", "ETIQUETA TRANSFERENCIA",
                           "ETIQUETA LASER", "ETIQUETA ZEBRA", "ETIQUETA DE POLIPROPILENO",
                           "ETIQUETA DE POLYESTER", "ETIQUETA CON RECUBRIMIENTO",
                           "CINTA ZEBRA", "CINTA DE COLOR", "CINTA MONOCROMÁTICA",
                           "CINTA DE LAMINACION", "CINTA DE LAMINACIÓN", "LAMINACIÓN ZEBRA", "LAMINACION ZEBRA",
                           "RIBBON ", "CINTA RIBBON", "CINTA LAMINADA", "CINTA LEXMARK", "ZEBRA Z-PERFORM",
                           "CARTUCHO DE BRAZALETE")) or
        has("RIBBON", "CINTA RIBBON", "YMCKO", "YMCKOK", "YMCK", "CINTA HOLOGRAMA",
            "CINTAS MONOCROMATICAS", "CINTAS DE COLOR", "CINTA ZEBRA", "CINTA LAMINADA",
            "CINTA TERMORETRÁCTIL", "CINTA CONTINUA", "CINTA DE IMPRESIÓN", "CINTA DE IMPRESION",
            "CINTA DE TELA", "CINTA EPSON", "CINTA LEXMARK", "CINTAS BROTHER",
            "ETIQUETAS TERMICAS", "ETIQUETAS TÉRMICAS", "ETIQUETA TERMICA", "ETIQUETA TÉRMICA",
            "ETIQUETA TÉRMICO", "ETIQUETA TERMICO", "ETIQUETA TRANSFERENCIA TÉRMICA",
            "ETIQUETAS DE PAPEL", "ETIQUETA AMARILLA", "ETIQUETA TRANSPARENTE", "ETIQUETA ZEBRA",
            "ETIQUETA DE POLYESTER", "ROLLO TERMICO", "ROLLO TÉRMICO", "ROLLOS TÉRMICO",
            "PAPEL TERMICO", "PAPEL TÉRMICO", "ROLLO DE ETIQUETAS", "ROLLO ETIQUETA",
            "ROLLO BOND", "ROLLO AUTOCOPIANTE", "WAX RIBBON", "RESIN RIBBON",
            "ROLL LABEL", "LABEL PAPER", "Z-PERFORM", "Z-XTREME", "Z-ULTIMATE",
            "ZIPSHIP", "5095 RESIN", "DYE SUB OVERLAY") or
        (sku_starts("CAR") and has("CINTA NEGRA", "CINTA MOD.", "CINTA DE COLOR"))
    )
    if is_label_ribbon and not sku_starts("IMP", "MTF", "PLO", "SCA", "KIT", "LCT", "TER", "PAQ", "ROT", "CAB") \
       and not name_u.startswith(("IMPRESORA", "MULTIFUNCIONAL", "PAQUETE DE IMPRESORA", "KIT DE CREDENCIALIZ", "ZEBRA IMPRESORA", "LECTOR ", "SISTEMA POS", "KIT DE LIMPIEZA", "SOFTWARE", "ROTULADOR", "UNIDAD DE IMAGEN")) \
       and lacks("UNIDAD DE IMAGEN"):
        return "etiquetas_ribbons"

    # 54. PUNTO DE VENTA (POS)
    is_pos_item = (
        sku_starts("KIO", "CJN", "CJS", "HDH", "LCT", "PANECL", "ROBECL", "PAQEVL") or
        (sku_starts("TER") and not name_u.startswith(("TERMOMETRO", "TERMÓMETRO"))) or
        name_u.startswith(("PUNTO DE VENTA", "SISTEMA POS", "SISTEMA DE PUNTO DE VENTA", "TERMINAL POS",
                           "TERMINAL PUNTO DE VENTA", "TERMINAL ALL IN ONE", "TERMINAL ALL-IN-ONE",
                           "TERMINAL PORTÁTIL", "TERMINAL PORTATIL", "TERMINAL MÓVIL", "TERMINAL MOVIL",
                           "CAJON DE DINERO", "CAJÓN DE DINERO", "CAJA PARA DINERO",
                           "KIOSCO", "QUIOSCO", "TÓTEM INTERACTIVO", "TOTEM INTERACTIVO",
                           "VERIFICADOR DE PRECIOS", "LECTOR DE CÓDIGO", "LECTOR DE CODIGO",
                           "LECTOR LASER DE CÓDIGO", "LECTOR IMAGER", "LECTOR AREA-IMAGING", "KIT DE LECTOR DE CÓDIGO",
                           "ESCÁNER DE CÓDIGO DE BARRAS", "ESCANER DE CODIGO DE BARRAS", "ESCANER DE CODIGOS DE BARRAS",
                           "IMPRESORA TÉRMICA", "IMPRESORA TERMICA", "IMPRESORA DE TICKET", "IMPRESORA PORTÁTIL DE TICKETS",
                           "IMPRESORA DE ETIQUETAS", "IMPRESORAS DE ETIQUETAS", "IMPRESORA MÓVIL DE ETIQUETAS",
                           "IMPRESORA DE TRANSFERENCIA TÉRMICA", "IMPRESORA DE CREDENCIALES", "IMPRESORA EVOLIS",
                           "IMPRESORA STAR MICRONICS", "KIT DE CREDENCIALIZACIÓN", "KIT DE CREDENCIALIZACION",
                           "MULTIFUNCIONAL STAR MICRONICS MPOP", "MINIPRINTER", "MINI PRINTER", "NS TECH MINI PRINTER",
                           "POS NSTECH", "COMPUTADORA MÓVIL ZEBRA", "KIT COMPUTADORA MÓVIL ZEBRA",
                           "TABLETA INDUSTRIAL UROVO", "DIGITALIZADOR DE FIRMA", "EL DIGITALIZADOR DE FIRMA",
                           "SEWOO - RECEIPT PRINTER", "SEWOO - MOBILE PRINTER", "ZEBRA HANDHELD", "ZEBRA TC",
                           "ZEBRA ET40", "NEWLAND - MT", "ELO I-SERIES", "ELO WALLABY", "COMANDERA MÓVIL",
                           "PAGO EN MESA", "SOFT RESTAURANT", "SOFTWARE DE PUNTO DE VENTA", "SOFTWARE POS",
                           "ACTUALIZACIÓN MYBUSINESS POS", "ACTUALIZACIÓN A LA VERSIÓN DESS", "LICENCIA ELECTRÓNICA DESS",
                           "SERVICIO DE NUBE DESS", "SERVICIO DE RENTA ANUAL DE SERVICIOS EN LA NUBE",
                           "ROBOT DE REPARTO", "ROBOT INTERACTIVO DE REPARTO", "MÓDULO DE LAMINACIÓN EVOLIS",
                           "LECTOR DE BANDA MAGNETICA", "MANGO DISPARADOR", "BASE PARA LECTOR", "BASE DE PEDESTAL")) or
        name_has("PUNTO DE VENTA", "LECTOR DE CODIGO", "LECTOR DE CÓDIGO", "ESCÁNER DE CÓDIGO DE BARRAS",
                 "ESCANER DE CODIGO DE BARRAS", "BARCODE SCANNER", "IMPRESORA TERMICA", "IMPRESORA TÉRMICA",
                 "IMPRESORA DE TICKET", "IMPRESORA DE RECIBOS", "RECEIPT PRINTER", "MINIPRINTER",
                 "CAJON DE DINERO", "CAJÓN DE DINERO", "CAJA PARA DINERO", "TERMINAL POS",
                 "VERIFICADOR DE PRECIOS", "KIOSCO", "QUIOSCO", "MOBILE COMPUTER",
                 "TERMINAL DE RECOPILACIÓN DE DATOS", "TERMINAL DE RECOPILACION DE DATOS",
                 "POS TOOLS", "POSTOOLS", "MYBUSINESS POS", "SOFT RESTAURANT", "CARDSTUDIO",
                 "IMPRESORA DE CREDENCIALES", "IMPRESORA DE ETIQUETAS", "TECLADO POS") or
        (sub_has("IMPRESORAS PARA RECIBOS") and name_has("PRINTER", "IMPRESORA", "MINIPRINTER", "TM-T", "TM-U")) or
        (sub_has("ESCÁNERES DE CÓDIGO DE BARRAS") and name_has("SCANNER", "ESCÁNER", "ESCANER", "LECTOR", "DS9308", "DS2208", "DS2278", "LS2208", "HH492", "VERIFICADOR")) or
        ("PUNTO DE VENTA" in sheet_u and sku_starts("ACC", "FDP", "KIT") and name_lacks("CABLE", "BATERIA", "BATERÍA", "CARGADOR", "CINTA", "ROLLO", "ETIQUETA", "HUB USB", "KIT DE LIMPIEZA", "SOFTWARE ASPEL"))
    )
    is_not_pos = (
        name_u.startswith(("TERMOMETRO", "TERMÓMETRO", "CABLE", "BATERIA", "BATERÍA", "CARGADOR",
                           "CORREA", "CARCASA", "PROTECTOR DE PANTALLA", "MONTURA PARA MUÑECA",
                           "EMPUÑADURA", "MONITOR PORTÁTIL", "MONITOR TOUCHSCREEN",
                           "SOFTWARE ASPEL CAJA")) or
        (not sku_starts("IMP", "CJN", "CJS", "LCT", "TER", "KIO", "HDH") and name_has("RFID", "HUELLA", "BIOMETR", "BIOMÉTR", "MIN MOE", "TORNIQUETE"))
    )
    if is_pos_item and not is_not_pos:
        return "punto_de_venta"

    # 11. TECLADOS
    is_kbd_name = (
        (sku_starts("TEC") and not name_has("TECLADO POS", "INCLUYE MOUSE")) or
        name_u.startswith(("TECLADO", "MAGIC KEYBOARD", "MINI TECLADO", "STEELSERIES APEX", "G515 ")) or
        name_has(" - TECLADO", " - KEYBOARD", "TECLADO PARA GAMING", "TECLADO MECÁNICO", "TECLADO MECANICO",
                 "TECLADO NUMÉRICO", "TECLADO NUMERICO", "TECLADO INALÁMBRICO", "TECLADO INALAMBRICO",
                 "TECLADO ALÁMBRICO", "TECLADO ALAMBRICO", "TECLADO GAMER", "TECLADO USB")
    )
    is_not_kbd = (
        name_u.startswith(("CHAROLA", "BANDEJA", "CERRADURA", "LECTORA", "JOYSTICK", "TECLADO JOYSTICK",
                           "TECLADO INALÁMBRICO DHI-", "TECLADO NUMÉRICO INALÁMBRICO DHI-", "DAHUA DHI-",
                           "IMPRESORA", "MULTIFUNCIONAL", "TABLET", "NVR", "TELÉFONO", "TELEFONO",
                           "KIOSCO", "LECTOR", "ANVIZ", "BRAZO", "SOPORTE", "PROTECTOR PARA",
                           "EQUIO DE AUDIO", "ROTULADOR", "CONTROL REMOTO", "REPOSAMUÑECAS", "ALFOMBRILLA",
                           "TAPETE", "MOUSEPAD")) or
        sku_starts("COMMAC", "POR", "LAP", "AIO", "WKS", "REL", "COM", "CPU", "IMP", "TAB", "NVR", "TEL", "KIO", "LCT", "SOF", "ROT", "CON") or
        name_has("ARMADO Y DESARMADO", "CONTROLADOR DE RED HD", "CONTROLADOR IP CON JOYSTICK",
                 "PARA PTZS", "PROTECTOR PARA TABLET", "PROTECTOR PARA GALAXY TAB", "TECLADO POS", "REPOSAMUÑECAS", "REPOSAMUNECAS")
    )
    if is_kbd_name and not is_not_kbd:
        return "teclados"

    # 12. RATONES & MOUSE
    is_mouse_name = (
        (sku_starts("MOU") and not name_u.startswith(("MOUSEPAD", "MOUSE PAD", "TAPETE", "ALFOMBRILLA", "PRESENTADOR"))) or
        name_u.startswith(("MOUSE ", "RATON ", "RATÓN ", "MINI RATON", "MINI RATÓN", "MAGIC MOUSE",
                           "TRACKBALL", "KIT DE MOUSE", "KIT MOUSE +", "LOGITECH G705", "LOGITECH G502")) or
        name_has(" - RATÓN", " - RATON", " - MOUSE", "MOUSE GAMER", "MOUSE INALÁMBRICO", "MOUSE INALAMBRICO",
                 "MOUSE ALÁMBRICO", "MOUSE ALAMBRICO", "MOUSE ÓPTICO", "MOUSE OPTICO", "MOUSE RECARGABLE",
                 "MOUSE VERTICAL", "EXPERT MOUSE", "TRACKBALL PRO FIT")
    )
    is_not_mouse = (
        name_u.startswith(("MOUSEPAD", "MOUSE PAD", "TAPETE", "ALFOMBRILLA", "COJÍN PARA MOUSE", "COJIN PARA MOUSE",
                           "HUB ", "FUNDA ", "PRESENTADOR", "TRIPIÉ", "TRIPIE", "IMAC", "COMPUTADORA",
                           "LAPTOP", "NOTEBOOK", "CONSOLA", "BANDEJA", "CONTROL REMOTO")) or
        sku_starts("CPU", "LAP", "POR", "COM", "WKS", "AIO", "CON") or
        name_has("MOUSEPAD", "MOUSE PAD", "ALFOMBRILLA", "COJÍN PARA MOUSE", "COJIN PARA MOUSE", "HUB DE ")
    )
    if is_mouse_name and not is_not_mouse:
        return "ratones_mouse"

    # =========================================================================
    # TIER 7: CCTV, REDES, CLIMATIZACION, RACKS, IMPRESION, SOPORTES Y GAMING
    # =========================================================================

    # 32. CAMARAS DE SEGURIDAD CCTV (Escuadrón 4)
    if (sku_starts("CAM") or has("CAMARA BALA", "CÁMARA BALA", "CAMARA DOMO", "CÁMARA DOMO", "CAMARA IP", "CÁMARA IP", "CAMARA TURBOHD", "CÁMARA TURBOHD", "CAMARA DE SEGURIDAD", "CÁMARA DE SEGURIDAD", "CAMARA PTZ", "CÁMARA PTZ", "CAMARA MINI PTZ", "CÁMARA MINI PTZ", "CÁMARA DE VIGILANCIA", "CAMARA DE VIGILANCIA", "BULLET SECURITY CAMERA")) \
       and not sku_starts("ACC", "CAB", "SWT", "SWI", "ROU", "ACP", "NVR", "DVR", "GRD", "SOF", "LIC") \
       and not name_u.startswith(("SWITCH", "SWTICH", "ROUTER", "NVR", "DVR", "GRABADOR", "KIT DE VIDEOVIGILANCIA", "KIT CCTV", "CAJA ", "BRAZO ", "SOPORTE ", "MONTAJE ", "WEBCAM", "CÁMARA WEB", "CAMARA WEB", "WEB ", "LICENCIA")) \
       and lacks("WEBCAM", "WEBCAB", "CAMARA WEB", "CÁMARA WEB", "FOTOGRAFICA", "FOTOGRÁFICA", "EOS REBEL", "CAJA CONEXION", "CAJA DE CONEXION", "CAJA DE CONEXIÓN", "CAJA CONEXIÓN", "KIT DE VIDEOVIGILANCIA", "KIT CCTV"):
        return "camaras_seguridad_cctv"

    # 33. GRABADORES DVR & NVR (Escuadrón 4: sin lacks('DISCO DURO', 'CAMARA')!)
    if (sku_starts("NVR", "DVR", "GRD") or has("DVR ", "NVR ", "GRABADOR DVR", "GRABADOR NVR", "GRABADOR DE VIDEO DIGITAL", "TURBOHD DVR", "XVR ", "KIT DE VIDEOVIGILANCIA", "KITS CCTV")) \
       and not sku_starts("ACC", "CAB", "CAM", "DDU", "SSD", "HDD", "RCK", "GAB", "MEM", "MSD") \
       and not name_u.startswith(("CÁMARA", "CAMARA", "DISCO ", "GABINETE", "SOPORTE", "OREJAS", "RACK KIT", "MONTAJE", "KIT DE ALARMA", "KIT ALARMA")) \
       and lacks("OREJAS", "RACK KIT", "GABINETE METÁLICO", "GABINETE METALICO", "KIT DE ALARMA", "KIT ALARMA"):
        return "grabadores_dvr_nvr"

    # 35. ALARMAS Y SENSORES (Escuadrón 4)
    if (has("SENSOR DE MOVIMIENTO", "SENSOR MOVIMIENTO", "DETECTOR DE MOVIMIENTO", "DETECTOR PIR", "SIRENA", "PANEL DE ALARMA", "KIT DE ALARMA", "KIT ALARMA", "ALARM SYSTEM", "EXPANSOR WIFI ALARMA", "REPETIDOR WIFI ALARMA", "SENSOR MAGNETICO", "SENSOR MAGNÉTICO", "CONTACTO MAGNETICO", "CONTACTO MAGNÉTICO", "SENSOR DE PUERTA", "DETECTOR DE HUMO", "DETECTOR HUMO", "DETECTOR INTELIGENTE DE HUMO", "DETECTOR DE RUPTURA", "DETECTOR DE ROTURA", "DETECTOR DE MONÓXIDO", "DETECTOR DE MONOXIDO", "DETECTOR DE GAS", "DETECTOR DE TEMPERATURA", "BOTÓN DE PÁNICO", "BOTON DE PANICO", "BOTÓN MANUAL DE ALARMA", "BOTON MANUAL DE ALARMA", "SENSOR DE PRESENCIA", "ESTROBO")) \
       and not sku_starts("CAM", "NVR", "DVR", "GRD", "SWT", "SWI", "ROU", "ACP", "IMP", "MTF", "PLO", "SCA") \
       and not name_u.startswith(("MONTAJE ", "SOPORTE ", "CÁMARA", "CAMARA", "NVR", "DVR", "SWITCH", "ROUTER")):
        return "alarmas_sensores_seguridad"

    # 36. TELEFONIA & CONMUTADORES (Escuadrón 4)
    if (sku_starts("TEL") or (sku_starts("CON") and has("CONMUTADOR", "CENTRAL TELEF", "IP-PBX", "PBX", "FXO", "FXS", "UCM6", "TELEFONIA", "TELEFONÍA")) or has("TELEFONO IP", "TELÉFONO IP", "TELÉFONO HOTELERO", "CONMUTADOR IP", "CENTRAL TELEFÓNICA", "CENTRAL TELEFONICA", "IP-PBX", "TELEFONO SIP", "TELÉFONO SIP", "IP PHONE", "TELEFONO EJECUTIVO", "TELÉFONO EJECUTIVO", "GRANDSTREAM GXP", "GRANDSTREAM GRP", "GRANDSTREAM DP7", "GRANDSTREAM WP8", "TELEFONO INALAMBRICO", "TELÉFONO INALÁMBRICO", "TELÉFONO UNILÍNEA", "TELEFONO UNILINEA", "TELÉFONO ANÁLOGO", "BASE INALÁMBRICO DECT", "ESTACIÓN BASE VOIP")) \
       and not sku_starts("ACC", "CAB", "CAM", "SWT", "SWI", "ROU", "ACP") \
       and not name_u.startswith(("JABRA LINK", "ADAPTADOR ")):
        return "telefonia_conmutadores"

    # 37. SWITCHES DE RED (Escuadrón 4)
    if (sku_starts("SWI", "SWT") or has("SWITCH DE RED", "SWITCH ETHERNET", "SWITCH POE", "SWITCH GIGABIT", "SWITCH GESTIONABLE", "SWITCH NO ADMINISTRABLE", "UNIFI SWITCH") or (isub_u == "HUBS & SWITCHES" and has("SWITCH", "CONMUTADOR"))) \
       and not sku_starts("LIC", "SOF", "ANT", "CAB") \
       and not name_u.startswith(("MODULO SFP", "MÓDULO SFP", "TRANSCEIVER", "TRANSCEPTOR", "EPCOM POWER LINE", "KIT DE ENERGIA SOLAR", "LICENCIA", "SCREENBEAM", "HPE CABLE")) \
       and lacks("NINTENDO", "TECLADO", "MODULO SFP", "MÓDULO SFP", "ENERGIA SOLAR", "ENERGÍA SOLAR", "LICENCIA PARA SWITCH", "USB PRO SWITCH", "INTERRUPTOR PARA COMPARTIR"):
        return "switches_red"

    # 38. ROUTERS & ACCESS POINTS (Escuadrón 4)
    if (sku_starts("ROU", "WIF", "ACP") or has("ROUTER INALAMBRICO", "ROUTER INALÁMBRICO", "ROUTER WIFI", "WIRELESS ROUTER", "ACCESS POINT", "ACCES POINT", "ACCESS POIINT", "PUNTO DE ACCESO", "REPETIDOR WIFI", "REPETIDOR WI-FI", "EXTENSOR DE RANGO", "EXPANSOR DE RANGO", "EXTENSOR WIFI", "EXTENSOR WI-FI", "EXTENSOR MESH", "SISTEMA MESH", "SISTEMA WIFI", "SISTEMA WI-FI", "WIRELESS MESH", "MESH WIFI", "DECO ", "HALO H", "UX7 MESH", "UCG-MAX", "UDM-PRO", "DREAM MACHINE", "DREAM ROUTER")) \
       and not sku_starts("LIC", "ANT", "SWT", "SWI", "CAM", "NVR", "DVR", "GRD", "IMP", "MTF", "PLO", "SCA") \
       and not name_u.startswith(("LICENCIA", "ANTENA", "INYECTOR", "SOPORTE", "KIT DE MONTAJE", "ADAPTADOR DE CA", "ADAPTADOR POE", "RADIO ", "ESTACIÓN BASE", "ESTACION BASE", "REPETIDOR WIFI ALARMA", "EXTENSOR POE")) \
       and lacks("LICENCIA PARA", "RADIO BACKHAUL", "AIRMAX", "ALARMA", "POWERADAPTER", "POWER ADAPTER", "ADAPTADOR DE CA", "INYECTOR POE", "MIDSPAN INJECTOR", "SOPORTE DE PARED", "KIT DE MONTAJE", "PUNTO A PUNTO", "MULTIPUNTO", "EXTENSOR POE"):
        return "routers_access_points"

    # 39. ANTENAS & RADIOENLACES (Escuadrón 4)
    if (sku_starts("ANT") or name_u.startswith(("ANTENA", "RADIO BACKHAUL", "RADIO UBIQUITI", "RADIO MODULAR", "ESTACIÓN BASE EPMP", "ESTACION BASE EPMP")) or has("RADIOENLACE", "RADIO BACKHAUL", "AIRMAX", "AIRFIBER", "NANOLIGHT", "LITEBEAM", "POWERBEAM", "ROCKETDISH", "UNIFI OUTDOOR", "EPMP ", "PTP B5", "PTP B24", "PUNTO A PUNTO", "PUNTO-PUNTO", "PUENTE INALÁMBRICO", "PUENTE INALAMBRICO")) \
       and lacks("ADAPTADOR DE RED", "ADAPTADOR DUAL BAND", "ADAPTADOR USB", "EXTENSOR DE RANGO", "EXPANSOR DE RANGO", "SOPORTE PARA ANTENA", "COMPUTADORA", "RASTREADOR GPS", "TERMINAL DE RASTREO", "GNSS", "CÁMARA", "CAMARA", "NVR", "DVR") \
       and not sku_starts("TAR", "CAB", "CPU", "COM", "NVR", "DVR", "GRD", "CAM", "TER", "RAS", "ROU", "SWT", "IMP", "MTF", "PLO", "SCA"):
        return "antenas_radioenlaces"

    # 41. FIBRA OPTICA & TRANSCEIVERS (Escuadrón 4: 1000BASE/10GBASE/SFP solo con contexto óptico!)
    has_fiber_core = (
        sku_starts("SFP", "TRA", "FIB") or
        has("FIBRA OPTICA", "FIBRA ÓPTICA", "TRANSCEIVER", "TRANSCEPTOR", "MODULO SFP", "MÓDULO SFP", "SFP+", "QSFP", "SFP28", "MINI-GBIC", "MINIGBIC", "CABLE DROP", "PIGTAIL", "ACOPLADOR DE FIBRA", "CONVERTIDOR DE MEDIOS", "CONECTOR FX BRILLIANCE", "GPON", "TERMINAL DE LÍNEA ÓPTICA", "JUMPER UBIQUITI UDC") or
        (has("10GBASE", "1000BASE", "SFP ") and has("TRANSCEIVER", "TRANSCEPTOR", "SFP", "MINI-GBIC", "MINIGBIC", "FIBRA", "MONOMODO", "MULTIMODO", "LC ", "OLT"))
    )
    if has_fiber_core \
       and not sku_starts("IMP", "MTF", "PLO", "SCA", "STO", "SWT", "ROU", "ACP", "CAM", "NVR", "DVR", "GRD", "SRV", "SER", "CAB") \
       and not name_u.startswith(("IMPRESORA", "MULTIFUNCIONAL", "PLOTTER", "ESCÁNER", "ESCANER", "SCANNER", "HUB ", "INYECTOR", "CONECTOR JACK", "CONECTOR PLUG", "UDM-PRO")) \
       and lacks("BROADCOM", "TAPA HDMI", "WALLPLATE", "TAPA", "PLACA DE PARED", "MICROFIBRA", "FIBRA DE CARBON", "FIBRA DE CARBÓN", "ESCRITORIO", "SILLA", "TABLA", "MOUSEPAD", "PAD", "BALUN", "BALUM", "TRANSCEPTOR PASIVO", "TRANSCEPTORES PASIVOS", "RECEPTOR ACTIVO", "CCTV", "HDCVI", "TURBOHD", "AHD", "CÁMARAS DE SEGURIDAD", "CAMARAS DE SEGURIDAD", "SAXXON", "PARA VIDEO", "VB-", "LASERJET", "STORAGE ARRAY", "DREAM MACHINE", "UDM-PRO", "HUB USB", "INYECTOR DE POTENCIA", "CABLE HDMI"):
        return "fibra_optica_transceivers"

    # 65. CLIMATIZACION & MINISPLITS
    is_climate = (
        sku_starts("AIR", "DESHSE") or
        name_u.startswith(("AIRE ", "MINISPLIT", "DESHUMIDIFICADOR", "DESHUMIFICADOR",
                           "UNIDAD DE AIRE ACONDICIONADO", "SISTEMA DE ENFRIAMIENTO , TRIPP LITE")) or
        name_has("MINISPLIT", "AIRE ACONDICIONADO", "AIRE DE VENTANA", "INVERTER 1 TON",
                 "INVERTER 1.5 TON", "INVERTER 2 TON", "DESHUMIDIFICADOR", "DESHUMIFICADOR", "SRCOOLDXRW", "SRCOOL7K")
    )
    if is_climate and not name_u.startswith(("MÓDULO DE INTERFAZ", "MODULO DE INTERFAZ", "AMAZON FIRE TV")):
        return "climatizacion_aires_acondicionados"

    # 42. RACKS & GABINETES DE SERVIDOR
    is_rack_item = (
        sku_starts("RCK", "AW2", "AW3", "AU5") or
        (sku_starts("GAB") and is_telecom_rack_gab) or
        name_u.startswith(("RACK ", "GABINETE DE PARED", "GABINETE MURAL", "GABINETE DE PISO", "GABINETE DE PISA",
                           "GABINETE 15U", "GABINETE RACK", "GABINETE SMARTRACK", "GABINETE DE EXTERIOR CON RACK",
                           "GABINETE DE 19\"", "GABINETE PARA CONVERTIDOR",
                           "CHAROLA PARA RACK", "CHAROLA LISA PARA RACK", "CHAROLA PARA TECLADO", "CHAROLA CORREDIZA",
                           "CHAROLA MULTIUSOS", "CHAROLA DESLIZABLE", "CHAROLA PARA MONITOR", "CHAROLA PARA MISCEL",
                           "CHAROLA PARA SOPORTAR EQUIPOS EN RACK", "ENTREPAÑO", "ENTREPANO",
                           "ORGANIZADOR HORIZONTAL", "ORGANIZADOR VERTICAL", "ORGANIZADOR DE CABLE",
                           "ADMINISTRADOR DE CABLES", "PANEL CIEGO", "TAPA CIEGA PARA RACK",
                           "KIT DE SOPORTES DE PARED PARA RACK", "VENTILADOR DE TECHO. PARA MONTAJE EN RACK")) or
        name_has("RACK ABIERTO", "RACK DE PARED", "RACK DE PISO", "RACK VERTICAL", "RACK DE 2 POSTES",
                 "RACK DE 19", "RACK 19", "RACK MARCO ABIERTO", "GABINETE DE PARED", "GABINETE MURAL",
                 "GABINETE DE PISO", "GABINETE RACK", "SMARTRACK", "RACKS DE 19", "WALL MOUNT ENCLOSURE",
                 "WALL MOUNT CABLE DISTRIBUTION BOX", "RACK BLANKING PANEL", "RACK MOUNT SHELF",
                 "JUEGO DE RIELES PARA RACK", "CONDUCTO DE ORGANIZACIÓN DE CABLES DE BASTIDOR",
                 "ORGANIZADOR VERTICAL", "ORGANIZADOR HORIZONTAL", "BANDEJA PARA RACK", "CHAROLA PARA RACK",
                 "PANEL CIEGO", "PARA RACK DE 19", "PARA RACK 19")
    )
    is_not_rack = (
        name_u.startswith(("CABLE", "PATCH", "PANEL DE PARCHEO", "CONECTOR", "HERRAMIENTA",
                           "NO-BREAK", "NO BREAK", "UPS ", "UNIDAD DE AIRE", "BARRA MULTICONTACTOS",
                           "BARRA PARA RACK", "PDU ", "SWITCH ", "SERVIDOR", "STORAGE")) or
        sku_starts("NBK", "UPS", "AIR", "REG", "SUP", "PDU", "SER", "STO", "SWT", "SWI") or
        name_has("PANEL DE PARCHEO", "PATCH PANEL", "TABLERO DE CONEXIONES", "PROBADOR DE CABLES")
    )
    if is_rack_item and not is_not_rack:
        return "racks_gabinetes_servidor"

    # 46. PLOTTERS DE GRAN FORMATO (Escuadrón 4)
    if (sku_starts("PLO") or name_u.startswith(("PLOTTER", "IMPRESORA DE FORMATO ANCHO", "IMPRESORA DE FORMATO LARGO", "IMPRESORA DE GRAN FORMATO")) or (has("PLOTTER", "DESIGNJET", "SURECOLOR", "IMAGEPROGRAF") and name_u.startswith("IMPRESORA"))) \
       and not sku_starts("CAR", "TIN", "TON", "PAP", "ACC", "CAB", "APL", "IMP", "MTF", "SCA") \
       and not name_u.startswith(("ESCÁNER", "ESCANER", "SCANNER", "PAPEL", "ROLLO", "TINTA", "CARTUCHO", "TANQUE", "BOTELLA", "CABEZAL", "ALIMENTADOR", "BASE", "SOPORTE", "PEDESTAL", "CORTADOR", "REPUESTO", "KIT")):
        return "plotters_gran_formato"

    # 43. IMPRESORAS & MULTIFUNCIONALES (Escuadrón 4: +MTF/+COP, \bPOS\b, aislar Intcomex)
    is_pos_or_label_printer = (
        has("PUNTO DE VENTA", "PUNTOS DE VENTA", "MINIPRINTER", "MINI IMPRESORA", "IMPRESORA TERMICA", "IMPRESORA TÉRMICA", "IMPRESORA DE TICKET", "IMPRESORA DE RECIBOS", "RECEIPT PRINTER", "IMPRESORAS PARA RECIBOS", "58MM", "80MM", "IMPRESORA DE CREDENCIALES", "TARJETAS PVC", "CÓDIGOS DE BARRA", "CODIGOS DE BARRA", "IMPRESORA DE ETIQUETAS", "IMPRESORAS DE ETIQUETAS", "TRANSFERENCIA TÉRMICA", "TRANSFERENCIA TERMICA", "TÉRMICA DIRECTA", "TERMICA DIRECTA", "TÉRMICA 2\"", "TERMICA 2\"") or
        has_word(r'\bPOS\b')
    )
    is_intc_printer = (icat_u == "IMPRESORAS Y ESCÁNERES" and isub_u not in ("ESCÁNERES", "ESCANERES", "ACCESORIOS"))
    is_printer = (
        sku_starts("IMP", "MTF", "MLT", "COP") or is_intc_printer or
        name_u.startswith(("IMPRESORA", "MULTIFUNCIONAL", "COPIADORA", "ECOTANK", "SMART TANK", "LASERJET", "DESKJET", "HP LASERJET", "HP COLOR LASERJET")) or
        (has("IMPRESORA") and has("LASER", "LÁSER", "INYECCION", "INYECCIÓN", "MULTIFUNCIONAL", "WIFI", "DUPLEX", "DÚPLEX", "BROTHER", "EPSON", "CANON", "HP ", "XEROX", "RICOH", "KYOCERA", "PANTUM") and icat_u != "IMPRESORAS Y ESCÁNERES")
    )
    if is_printer \
       and not name_u.startswith(("CARTUCHO", "BOTELLA", "TINTA", "TONER", "TÓNER", "CINTA", "RIBBON", "CABEZAL", "RODILLO", "PAPEL", "DEPOSITO", "DEPÓSITO", "ETIQUETA", "ESCÁNER", "ESCANER", "SCANNER", "CAJA DE MANTENIMIENTO", "BANDEJA", "SOPORTE", "KIT DE", "ROTULADOR", "HERRAMIENTA")) \
       and not sku_starts("CAR", "TON", "TIN", "RIB", "ETI", "PAP", "BAT", "CAB", "ACC", "SCA", "SCN", "PLO", "ROT") \
       and not is_pos_or_label_printer \
       and lacks("PLOTTER", "DESIGNJET", "SURECOLOR", "TRIPIE", "TRÍPIE", "TRIPIÉ", "TRIPODE", "TRÍPODE", "MOCHILA", "FUNDA", "CINTA RIBBON", "CINTA DE TELA", "CAJA DE MANTENIMIENTO", "DOCUMENT SCANNER", "ESCÁNER DE DOCUMENTOS", "ESCÁNER DE SOBREMESA"):
        return "impresoras_multifuncionales"

    # 44. TONERS LASER (Escuadrón 4: rescata 219 Xerox CARXRX* + tambores láser; excluye MTF/COP/PLO)
    is_toner = (
        sku_starts("TON") or
        name_u.startswith(("CARTUCHO TÓNER", "CARTUCHO TONER", "TONER", "TÓNER", "TAMBOR ", "FOTOCONDUCTOR", "FOTORECEPTOR", "UNIDAD DE IMAGEN")) or
        (sku_starts("CAR") and has("TONER", "TÓNER", "TAMBOR ", "FOTOCONDUCTOR", "FOTORECEPTOR")) or
        has_word(r'\bT[OÓ]NER\b', name_u) or
        has("CARTUCHO DE TÓNER", "CARTUCHO DE TONER", "TÓNER HP", "TONER HP", "TÓNER BROTHER", "TONER BROTHER", "TÓNER CANON", "TONER CANON", "TÓNER XEROX", "TONER XEROX", "TÓNER SAMSUNG", "TONER SAMSUNG", "TÓNER PANTUM", "TONER PANTUM")
    )
    if is_toner \
       and not (sku_starts("IMP", "MTF", "MLT", "COP", "PLO", "SCA") or name_u.startswith(("IMPRESORA", "MULTIFUNCIONAL", "COPIADORA", "PLOTTER", "HP LASERJET", "HP COLOR LASERJET", "BANDEJA", "SOPORTE", "CARTUCHO DE GRAPAS", "FUSOR", "BOTELLA RESIDUAL", "BOTELLA DE DESPERDICIO", "CONTENEDOR", "CHAROLA", "DEPÓSITO", "DEPOSITO"))) \
       and lacks("SENSOR", "PCB", "BOTONERA", "ORVIBO", "DEPOSITO DE DESECHO", "DEPÓSITO DE DESECHO", "DEPOSITO DE RESIDUOS", "DEPÓSITO DE RESIDUOS", "BOTELLA RESIDUAL", "BOTELLA DE DESPERDICIO", "TONER RESIDUAL", "TÓNER RESIDUAL", "CONTENEDOR DE DESECHO", "FUSOR", "FUSER MODULE") \
       and not sku_starts("ACC", "CAB"):
        return "toners_laser"

    # 45. TINTAS & CARTUCHOS (Escuadrón 4: rescata 45 Canon PFI-* + 54 Intcomex; purga cintas/tambores)
    is_intc_ink = (
        (isub_u == "CARTUCHOS DE TONER E INK-JET" and not has_word(r'\bT[OÓ]NER\b', name_u)) or
        (isub_u == "CONSUMIBLES" and "EPSON" in name_u and "SJIC" in name_u)
    )
    is_ink = (
        sku_starts("TIN") or is_intc_ink or
        name_u.startswith(("BOTELLA DE TINTA", "CARTUCHO DE TINTA", "TINTA ", "TANQUE CANON", "TANQUE DE TINTA", "COMBO BOTELLA DE TINTA")) or
        (sku_starts("CAR") and has("TINTA", "CARTUCHO", "BOTELLA", "PFI-", "TANQUE CANON") and not name_u.startswith(("CINTA", "ETIQUETA", "TAMBOR", "CINTURÓN", "CINTURON", "CAJA DE MANTENIMIENTO", "ZEBRA"))) or
        has("BOTELLA DE TINTA", "CARTUCHO DE TINTA", "TINTA ORIGINAL", "TINTA EPSON", "TINTA HP", "TINTA CANON", "TINTA BROTHER", "TANQUE CANON", "PFI-", "INK REFILL", "INK BOTTLE", "INK TANK", "INK CARTRIDGE")
    )
    if is_ink \
       and not (sku_starts("IMP", "MTF", "MLT", "COP", "PLO", "TON", "RIB", "ETI", "ACC", "CAB") or name_u.startswith(("IMPRESORA", "MULTIFUNCIONAL", "PLOTTER", "CINTA", "ETIQUETA", "TAMBOR", "CINTURÓN", "CINTURON", "CAJA DE MANTENIMIENTO", "FUSOR", "ZEBRA"))) \
       and not has_word(r'\bT[OÓ]NER\b', name_u) \
       and lacks("CINTA RIBBON", "CINTA LAMINADA", "CINTA TERMORETRÁCTIL", "CINTA DE IMPRESIÓN", "CINTA DE IMPRESION", "CINTA DE TELA", "CINTA EPSON", "CINTAS BROTHER", "CINTAS PARA MINI IMPRESORAS", "CINTAS PARA IMPRESORAS EPSON DE MATRIZ", "CINTAS PARA ROTULADOR", "WAX RIBBON", "CAJA DE MANTENIMIENTO", "MANTENIMIENTO DE TINTA", "CINTURÓN DE ARRASTE", "CINTURON DE ARRASTE", "TAMBOR"):
        return "tintas_cartuchos"

    # 48. ESCANERES & DIGITALIZADORES (Escuadrón 4)
    is_barcode_scanner_or_acc = (
        name_u.startswith(("LECTOR DE CÓDIGO", "LECTOR DE CODIGO", "PROTECTOR DE PANTALLA", "MONTURA ", "BASE ", "FUNDA ", "CORREA ", "CABLE ")) or
        "LECTOR DE CÓDIGOS DE BARRA" in sub_u or "LECTOR DE CODIGOS DE BARRA" in sub_u or
        "ESCÁNERES DE CÓDIGO DE BARRAS" in isub_u or
        has("ESCÁNER DE CÓDIGOS DE BARRAS", "ESCANER DE CODIGOS DE BARRAS", "ESCÁNER DE CÓDIGO DE BARRAS", "ESCANER DE CODIGO DE BARRAS", "BARCODE SCANNER", "LECTOR DE CODIGO DE BARRAS", "LECTOR DE CÓDIGO DE BARRAS", "EVOTEC ESCÁNER", "EVOTEC ESCANER")
    )
    if (sku_starts("SCN", "SCA") or name_u.startswith(("ESCÁNER", "ESCANER", "SCANNER")) or isub_u in ("ESCÁNERES", "ESCANERES") or has("SCANJET", "DIGITALIZADOR DE DOCUMENTOS", "DOCUMENT SCANNER", "CAMA PLANA", "ESCÁNER DE DOCUMENTOS", "ESCÁNER DE SOBREMESA")) \
       and not is_barcode_scanner_or_acc \
       and not sku_starts("ACC", "CAB", "LCT", "IMP", "MTF", "TER") \
       and not name_u.startswith(("IMPRESORA", "MULTIFUNCIONAL", "PLOTTER")) \
       and lacks("HUELLAS", "ENROLADOR", "CONVERTIDOR", "SERIAL", "DB9", "FUNDA", "CORREA", "PUNTO DE VENTA", "STAR MICRONICS"):
        return "escaneres_digitalizadores"

    # 61. SOPORTES & ERGONOMIA
    is_soporte_excl = (
        sku_starts("GAB", "SIL", "RCK", "CAM", "MON", "PAN", "PRO", "COM", "CPU", "WKS", "NBK", "UPS", "BOC", "TEC", "MOU") or
        sheet_raw_u == "TELEFONIA Y VIDEO VIGILANCIA" or
        icat_u == "CÁMARAS & VIDEOCÁMARAS" or
        name_u.startswith(("GABINETE", "SILLA", "RACK", "CAMARA", "CÁMARA", "MONITOR", "PANTALLA", "PROYECTOR", "TECLADO", "MOUSE", "RATON", "RATÓN", "FUNDA", "ESTUCHE", "CARCASA", "CAJA ", "KIT DE LIMPIEZA", "LENTE", "LAMPARA", "LÁMPARA", "BASE DE CARGA", "SOPORTE DE CARGA", "SOPORTE PARA ROLLO", "SOPORTE PARA TERMINAL", "SOPORTE UNIVERSAL CON GIRO PARA TERMINAL", "BASE DE PEDESTAL")) or
        has("PARA CAMARAS", "PARA CÁMARAS", "PROVISION ISR", "CAMARAS IP", "CÁMARAS IP", "DOMO Y BALA", "SMARTRACK", "RACKS DE 19", "TERMINAL POS", "TERMINAL DE PUNTO DE VENTA", "VERIFONE", "ZEBRA", "HONEYWELL", "CONSOLA PS5", "PARA CONSOLA", "PARA XBOX", "PANELES SOLARES", "HEADSER STAND", "BASE GAMING HEADSET", "SOPORTE PARA DIADEMA", "BASE PARA HEADSET", "SOPORTE DE CARGA", "BASE DE CARGA")
    )
    is_soporte_pos = (
        has("SOPORTE PARA MONITOR", "BRAZO PARA MONITOR", "BRAZO PARA DOS MONITORES", "BRAZO PARA MONITORES", "BRAZO ARTICULADO",
            "BASE PARA MONITOR", "SOPORTE ARTICULADO", "SOPORTE DE TV", "SOPORTE PARA TV", "SOPORTE TV", "SOPORTE DE TECHO",
            "SOPORTE DE PARED", "SOPORTE DE PISO", "SOPORTE DE ESCRITORIO", "SOPORTE DOBLE PARA MONITOR", "SOPORTE PARA PANTALLA",
            "SOPORTE PARA PROYECTOR", "SOPORTE UNIVERSAL PARA PROYECTOR", "SOPORTE UNIVERSAL MULTIMEDIA",
            "SOPORTE PARA TABLETA", "SOPORTE PARA TABLET", "SOPORTE PARA CELULAR", "SOPORTE PARA LAPTOP", "SOPORTE LAPTOP",
            "SOPORTE VENTILADO", "SOPORTE DE MONTAJE", "SOPORTE PORTATIL CON RUEDAS", "SOPORTE PORTÁTIL CON RUEDAS",
            "SOPORTE DE COMPUTADORA/CPU", "SOPORTE VESA", "SOPORTE GETTTECH", "SOPORTE MARCA UP", "SOPORTE BARRA DE SONIDO",
            "SOPORTE DE ALUMINIO CON PISTÓN", "SOPORTE DE ALUMINIO CON PISTON", "SOPORTE BSH01",
            "BASE ENFRIADORA", "BASE PARA LAPTOP", "STAND MONITOR", "ESTACION DE TRABAJO DE PIE", "ESTACIÓN DE TRABAJO DE PIE",
            "TAPETE ANTIFATIGA", "DESCANSA PIES", "DESCANSAPIES", "REPOSAMUÑECAS", "REPOSAMUNECAS", "RESPALDO LUMBAR",
            "WALL MOUNT BRACKET", "TV MOUNT", "NOTEBOOK STAND", "MONITOR MOUNTING KIT", "KX BRKT FIX",
            "KIT DE MONTAJE - PARA PANTALLA", "KIT DE MONTAJE (PIES", "ABRAZADERA - PARA PANTALLA",
            "ABRAZADERA - PERFIL BAJO", "TRIPIÉ PARA PROYECTOR", "TRIPIE PARA PROYECTOR",
            "CARRITO CON RUEDAS - PARA PANTALLAS", "BANDEJA DE TECLADO Y MOUSE") or
        (name_u.startswith("SOPORTE ") and sub_u in ("SOPORTE TV P/PARED", "SOPORTES", "SOPORTES PARA TV OVALTECH", "SOPORTES Y BASES", "SOPORTES PARA MONITOR", "SOPORTES PARA PROYECTOR", "SOPORTE Y BRAZO", "SOPORTE GETTTECH", "SOPORTES PARA TABLETA", "SOPORTES MARCA UP"))
    )
    if is_soporte_pos and not is_soporte_excl:
        return "soportes_ergonomia"

    # 66. GAMING, CONSOLAS & SILLAS
    is_gaming_item = (
        sku_starts("SIL", "ESC", "XBO", "AM1") or
        (sku_starts("CON") and not name_u.startswith(("CONMUTADOR", "QIAN PRESENTADOR", "CONTROL REMOTO"))) or
        name_u.startswith(("SILLA ", "OFFICE CHAIR", "ESCRITORIO GAM", "ESCRITORIO ERG", "ESCRITORIO EJEC", "ESCRITORIO DE TRABAJO",
                           "NACEB GAMING ESCRITORIO", "CONSOLA NINTENDO", "CONSOLA MICROSOFT XBOX", "SONY PLAYSTATION",
                           "PLAYSTATION", "XBOX", "NINTENDO", "CONSOLA DE JUEGOS", "CONSOLA ARCADE", "CONSOLA RETRO",
                           "GAMEPAD", "VOLANTE", "CONTROL ARCADE", "CONTROL PARA JUEGOS", "CONTROL CON VENTILADORES",
                           "CONTROL RAZER", "PALANCA DE CAMBIOS", "LOGITECH G923", "RAZER - JOYSTICK", "RAZER - FREYJA",
                           "BASE ENFRIADORA PARA CONSOLA", "BASE ENFRIADORA PARA XBOX", "BASE CARGADORA DE BATERÍAS CHARGECORE")) or
        name_has("SILLA GAMER", "SILLA DE JUEGO", "SILLA DE OFICINA", "SILLA ERGONOMICA", "SILLA ERGONÓMICA",
                 "SILLA EJECUTIVA", "SILLA PARA COMPUTADOR", "CHAIR EXEC", "MARVEL CHAIR", "LICENCED CHAIR",
                 "GAMING - CHAIR", "ESCRITORIO GAMER", "ESCRITORIO GAMING", "MESA GAMER",
                 "CONSOLA NINTENDO", "CONSOLA DE JUEGOS", "CONSOLA ARCADE", "CONSOLA RETRO",
                 "PLAYSTATION 5", "XBOX SERIES", "NINTENDO SWITCH", "RUMBLEPAD", "DRIVING FORCE",
                 "HAPTIC GAMING CUSHION", "HAPTIC GAMING CUSHI", "PARA JUEGOS DE CONSOLA")
    )
    is_not_gaming = (
        sku_starts("CAB", "MON", "BOC", "DDU", "BAT", "TEC", "KIT", "LTV", "MEM", "CPU") or
        name_u.startswith(("CABLE", "MONITOR", "DIADEMA", "AUDIFONO", "AUDÍFONO", "HEADSET",
                           "DISCO DURO", "UNIDAD DE ESTADO", "BATERIA", "BATERÍA", "BANCO DE BATERÍAS",
                           "SWITCH KVM", "MUX KVM", "CONSOLA KVM", "CONSOLA MULTIPLEXOR", "CONSOLA LCD",
                           "VIDEO SPLITTER", "KIT EXTENSOR", "TRANSMISOR", "SOPORTE DE MONTAJE",
                           "RESPALDO LUMBAR", "ADAPTADOR", "USB TIPO C", "TARJETA DE EXPANSIÓN",
                           "LASER CINEMA", "CONMUTADOR", "COMPUTADORA"))
    )
    if is_gaming_item and not is_not_gaming:
        return "gaming_consolas_sillas"

    # 67. ACCESORIOS & MISCELANEOS (Default fallback)
    return "accesorios_perifericos"
