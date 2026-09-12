# -*- coding: utf-8 -*-
"""
MOTOR SEMANTICO DE CLASIFICACION UNIVERSAL VECTEC (67 DEPARTAMENTOS)
Aplica reglas positivas y negativas estrictas, limites de palabra (\b)
y priorizacion taxonomica para garantizar 100% de congruencia en vitrinas y catalogo.
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

def clasificar_producto_semantico(sku, name, brand="", subgrupo_header="", sheet_name="", intc_cat="", intc_sub=""):
    s = (sku or "").upper().strip()
    raw_s = re.sub(r'^[AB]-', '', s)
    extra = f" {subgrupo_header} {intc_sub} {intc_cat}".strip()
    n = f"{name or ''} {extra}".upper().strip()
    b = (brand or "").upper().strip()

    def has(*words):
        return any(w in n for w in words)
    def lacks(*words):
        return not any(w in n for w in words)
    def sku_starts(*prefixes):
        return any(raw_s.startswith(p) or s.startswith(p) for p in prefixes)

    # -------------------------------------------------------------
    # 2. TARJETAS MADRE (Motherboards) - Evaluadas al inicio para evitar que RAM/SSD/Fans/Gabinetes/CPUs las roben
    # -------------------------------------------------------------
    if (sku_starts("MBD", "MOT") or n.startswith("MB ") or has("TARJETA MADRE", "MOTHERBOARD", "PLACA MADRE", "PLACA BASE")) \
       and lacks("COMPUTADORA ENSAMBLADA", "ALL-IN-ONE", "ALL IN ONE", "TODO EN UNO", "LAPTOP", "NOTEBOOK", "MINI PC", "MINIPC", "BAREBONE", "NUC ", "SERVIDOR", "SERVER", "WALLABY", "MONTAJE") \
       and not sku_starts("COMMAC", "POR", "LAP", "TAB", "IPD", "AIO", "WKS", "SRV", "SVR", "RNUC", "CPUDDL", "CPULEV", "CPUMAC", "CPUASS", "CPUVGO", "CPUGET", "CPUQIA", "CPUYEY", "CPULEN"):
        return "tarjetas_madre"

    # -------------------------------------------------------------
    # 1. PROCESADORES (CPUs) - Exclusivamente microprocesadores reales de escritorio y servidor
    # -------------------------------------------------------------
    if (sku_starts("CPUINT", "CPUAMD") or ((n.startswith("PROCESADOR ") or has("PROCESADOR INTEL", "PROCESADOR AMD", "PROCESADOR RYZEN")) and has("INTEL", "AMD", "RYZEN", "CORE I", "CORE ULTRA", "THREADRIPPER", "CELERON", "PENTIUM", "ATHLON", "XEON"))) \
       and lacks("MOTHERBOARD", "TARJETA MADRE", "MB ", "SOCKET", "PLACA BASE", "PLACA MADRE", "DISIPADOR", "VENTILADOR", "ENFRIAMIENTO", "COOLER", "GABINETE", "LAPTOP", "NOTEBOOK", "COMPUTADORA", "TODO EN UNO", "ALL-IN-ONE", "ALL IN ONE", "AIO", "MINI PC", "NUC", "SERVIDOR", "SERVER", "TABLET", "IPAD", "WORKSTATION", "PASTA TERMICA", "PASTA TÉRMICA") \
       and not sku_starts("MBD", "IPD", "TAB", "WKS", "LAP", "CEL", "SMA", "GAB", "FUE", "TVI", "ACC", "CAB", "CAR", "CPUDDL", "CPULEV", "CPUMAC", "CPUASS", "CPUVGO", "CPUGET", "CPUQIA", "CPUYEY", "CPULEN", "SER", "REL"):
        return "procesadores"

    # -------------------------------------------------------------
    # 5. TARJETAS DE VIDEO (GPUs)
    # -------------------------------------------------------------
    if (sku_starts("TVI", "GPU") or has("GEFORCE", "RTX ", "GTX ", "RADEON RX", "TARJETA DE VIDEO", "TARJETA GRÁFICA")) \
       and has("RTX", "GTX", "RX ", "VRAM", "GDDR6", "GDDR6X", "8GB", "12GB", "16GB", "24GB", "OC EDITION", "GAMING") \
       and lacks("LAPTOP", "NOTEBOOK", "COMPUTADORA", "PC GAMER", "PC ", "SERVIDOR", "MOTHERBOARD", "TARJETA MADRE", "MB "):
        return "tarjetas_video"

    # -------------------------------------------------------------
    # 23. TARJETAS MICROSD & SD
    # -------------------------------------------------------------
    if (sku_starts("MSD") or has("MICROSD", "MICRO SD", "TARJETA SD", "SDHC", "SDXC", "CANVAS SELECT", "EXTREME PRO", "ULTRA MICROSD", "MICRO SECURE DIGITAL", "SECURE DIGITAL")) \
       and lacks("LECTOR", "ADAPTADOR USB", "GABINETE", "CASE") and not sku_starts("ACC", "CAB"):
        return "tarjetas_microsd"

    # -------------------------------------------------------------
    # 24. MEMORIAS USB FLASH & PENDRIVES
    # -------------------------------------------------------------
    if (sku_starts("USB") or has("MEMORIA USB", "PENDRIVE", "FLASH DRIVE", "DUAL DRIVE", "CRUZER", "DATATRAVELER", "ULTRA FLAIR")) \
       and lacks("WINDOWS", "SISTEMA OPERATIVO", "CABLE", "HUB", "ADAPTADOR", "RED USB", "WIFI USB", "BLUETOOTH", "ANTENA", "CARGADOR") and not sku_starts("ACC", "CAB"):
        return "memorias_usb_pendrives"

    # -------------------------------------------------------------
    # 25. MEMORIAS RAM LAPTOP (SODIMM)
    # -------------------------------------------------------------
    if has("SODIMM", "SO-DIMM", "SO DIMM", "RAM PARA LAPTOP", "RAM LAPTOP", "DDR4 SODIMM", "DDR5 SODIMM") \
       and lacks("MINI PC", "NUC", "LIVA", "HERRAMIENTAS", "KIT DE HERRAMIENTAS", "COMPUTADORA", "LAPTOP", "NOTEBOOK", "SURFACE", "MOTHERBOARD", "TARJETA MADRE"):
        return "memorias_ram_laptop"

    # -------------------------------------------------------------
    # 26. MEMORIAS RAM SERVIDOR (ECC)
    # -------------------------------------------------------------
    if has("ECC REG", "ECC REGISTERED", "RDIMM", "ECC UNBUFFERED", "RAM SERVIDOR", "RAM SERVER", "SERVER MEMORY", "TRUDDR4") \
       and lacks("KIT EN BLANCO", "ESPACIOS DE MEMORIA", "ESPACIO EN BLANCO", "DUMMY", "TAPA"):
        return "memorias_ram_servidor"

    # -------------------------------------------------------------
    # 3. MEMORIAS RAM PC (DIMM)
    # -------------------------------------------------------------
    if (sku_starts("MEM") or has("MEMORIA RAM", "FURY BEAST", "VENGEANCE", "XPG SPECTRIX", "TRIDENT", "FURY RENEGADE", "RIPJAWS")) \
       and (has("DIMM", "UDIMM", "DDR4", "DDR5", "DDR3") or has("FURY BEAST", "VENGEANCE", "XPG SPECTRIX", "TRIDENT")) \
       and lacks("SODIMM", "SO-DIMM", "SO DIMM", "LAPTOP", "ECC", "SERVIDOR", "SERVER", "MICROSD", "MICRO SD", "SECURE DIGITAL", "MICRO SECURE DIGITAL", "USB", "FLASH DRIVE", "MINI PC", "MOTHERBOARD", "TARJETA MADRE", "MB ", "PROCESADOR", "RYZEN", "INTEL CORE", "CLASS 10", "CLASS 4", "UHS-I", "UHS-II", "A1", "A2", "V30", "V60", "KIT EN BLANCO") \
       and not sku_starts("CPU", "MBD", "ACC", "CAB", "MSD", "USB"):
        return "memorias_ram_pc"

    # -------------------------------------------------------------
    # 22. DISCOS DUROS EXTERNOS
    # -------------------------------------------------------------
    if (has("DISCO DURO EXTERNO", "DISCO EXTERNO", "SSD EXTERNO", "CANVIO", "PASSPORT", "ELEMENTS", "BACKUP PLUS") \
       or (has("DISCO PORTATIL", "DISCO PORTÁTIL", "SSD PORTABLE") and has("TOSHIBA", "WD", "SEAGATE", "ADATA", "SANDISK", "KINGSTON", "USB"))) \
       and lacks("PROTECTOR", "FUNDA", "SILICON", "SILICÓN", "ESTUCHE", "CABLE", "CARCASA", "ENCLOSURE", "ADAPTADOR") \
       and not sku_starts("ACC", "CAB", "CAR"):
        return "discos_duros_externos"

    # -------------------------------------------------------------
    # -------------------------------------------------------------
    # 8. SSDS M.2 NVME & PCIE
    # -------------------------------------------------------------
    prod_name = (name or "").upper().strip()
    if ((has("M.2 NVME", "NVME", "SSD M.2", "UNIDAD DE ESTADO SOLIDO M.2", "UNIDAD DE ESTADO SÓLIDO M.2") and ("M.2" in prod_name or "NVME" in prod_name or "PCIE" in prod_name)) or (sku_starts("SSD") and has("M.2", "NVME"))) \
       and lacks("EXTERNO", "PORTATIL", "PORTÁTIL", "CANVIO", "LAPTOP", "GABINETE PARA SSD", "ENCLOSURE", "CARCASA", "ADAPTADOR", "CABLE", "PROCESADOR", "INTEL CORE", "CORE ULTRA", "RYZEN", "MOTHERBOARD", "TARJETA MADRE", "MB ", "2.5\"", "2.5 PULGADAS", "SATAIII 2.5", "SATA 2.5", "SA400S37", "SU630") \
       and not sku_starts("ACC", "CAB", "CAR", "CPU", "MBD"):
        return "ssds_m2_nvme"

    # -------------------------------------------------------------
    # 9. DISCOS DUROS INTERNOS HDD
    # -------------------------------------------------------------
    if (has("HDD 3.5", "HDD 2.5", "BARRACUDA", "IRONWOLF", "WD PURPLE", "WD BLUE", "WD RED", "WD GOLD", "SKYHAWK", "SURVEILLANCE HDD") or (sku_starts("DDU") and has("3.5\"", "2.5\"", "SATA III", "RPM") and lacks("EXTERNO", "CANVIO", "PORTATIL", "PORTÁTIL", "PASSPORT", "ELEMENTS", "SSD"))) \
       and lacks("EXTERNO", "CANVIO", "PORTATIL", "PORTÁTIL", "BACKUP PLUS", "PASSPORT", "LAPTOP", "NOTEBOOK") and not sku_starts("ACC", "CAB"):
        return "discos_duros_hdd_internos"

    # -------------------------------------------------------------
    # 6. ENFRIAMIENTO (Líquido & Aire)
    # -------------------------------------------------------------
    if (sku_starts("VEN", "ENF") or has("ENFRIAMIENTO LIQUIDO", "ENFRIAMIENTO LÍQUIDO", "WATER COOLING", "DISIPADOR", "VENTILADOR", "COOLER CPU", "FAN RGB", "PURE LOOP", "SILENT LOOP", "KRAKEN")) \
       and lacks("PASTA TERMICA", "PASTA TÉRMICA", "GRASA TERMICA", "GRASA TÉRMICA", "LAPTOP", "COMPUTADORA", "PC ", "TODO EN UNO", "ALL-IN-ONE", "GABINETE CON VENTILADORES", "TABLETA", "TABLET", "PROCESADOR INTEL", "PROCESADOR AMD", "RYZEN", "CORE I", "CORE ULTRA") \
       and not sku_starts("CPUINT", "CPUAMD", "MBD"):
        return "enfriamiento"

    # -------------------------------------------------------------
    # 7. FUENTES DE ENERGIA (PSUs)
    # -------------------------------------------------------------
    if (sku_starts("FUE") or ((sku_starts("GAB") or has("FUENTE DE PODER", "FUENTE DE ALIMENTACION", "POWER SUPPLY")) and (has("FUENTE DE PODER", "FUENTE PODER", "FUENTE ASUS", "FUENTE DE ALIMENTACION", "POWER SUPPLY") or sku_starts("FUE")))) \
       and not n.startswith(("GABINETE", "CHASIS")) and lacks("GABINETE CON FUENTE", "INCLUYE FUENTE") \
       and (has("ATX", "SFX", "MODULAR", "80 PLUS", "80+", "BRONZE", "GOLD", "PLATINUM", "WATT", "500W", "600W", "650W", "750W", "850W", "1000W", "PSU") or sku_starts("FUE")) \
       and lacks("LAPTOP", "NOTEBOOK", "ALL IN ONE", "NO BREAK", "UPS", "REGULADOR", "BATERIA", "POWER BANK", "VENTILADOR PARA FUENTES", "CCTV", "DIVISOR", "REGULADA DE 12", "12 VCC", "12 VCD", "0.5A", "1A", "1.5A", "2A", "DAHUA", "SAXXON", "PROVISION", "BROBOTIX", "CABLE", "MOTHERBOARD", "TARJETA MADRE", "MB ") \
       and not sku_starts("CAB", "ACC", "MBD", "CPU", "CAM", "DVR", "NVR"):
        return "fuentes_energia"

    # -------------------------------------------------------------
    # 4. GABINETES & CHASIS GAMER
    # -------------------------------------------------------------
    if has("GABINETE", "CHASIS", "CASE GAMER", "TORRE GAMER", "MID TOWER", "FULL TOWER", "MINI TORRE", "MEDIA TORRE", "PECERA", "GABINETE ATX", "GABINETE MICRO ATX", "GABINETE SLIM") \
       and not n.startswith(("FUENTE", "CHAROLA", "BANDEJA", "VENTILADOR", "CAMARA", "ESTACION", "CARRO", "CARRITO", "CANALETA", "TORNILLERIA", "TARJETA")) \
       and lacks("DISCO DURO", "DISCO 2.5", "DISCO 3.5", "GABINETE DE DISCO", "GABINETE PARA DISCO", "GABINETE PARA SSD", "GABINETE PARA HDD", "ENCLOSURE", "CARCASA", "ESTUCHE", "PROTECTOR", "TORNILLO", "TORNILLERIA", "TUERCA", "PATCH", "LAPTOP", "NOTEBOOK", "SERVIDOR", "SERVER", "RACK", "COMPUTADORA ENSAMBLADA", "VENTILADOR DE FUENTE", "REGULADA DE 12", "12 VCC", "12 VCD", "0.5A", "1A", "1.5A", "2A", "SAXXON", "ESTACION DE CARGA", "CARGADOR", "CARRITO DE CARGA", "CARRO DE CARGA", "CHAROLA", "BANDEJA", "SIRENA", "ALARMA", "HUB USB", "CANALETA", "MOTHERBOARD", "TARJETA MADRE", "MB ", "TARJETA DE SONIDO", "TARJETA DE AUDIO", "SOUND CARD", "PCI EXPRESS", "TARJETA PCI", "TARJETA DE RED") \
       and not sku_starts("ACC", "CAB", "CAR", "CPU", "MBD", "FUE", "VEN", "ROU", "SWT", "MSD", "USB", "DVR", "NVR", "CAM", "TEL", "RCK", "TAR"):
        return "gabinetes"

    # -------------------------------------------------------------
    # 49. SISTEMAS OPERATIVOS (Windows Oficial)
    # -------------------------------------------------------------
    if (has("WINDOWS 11", "WINDOWS 10", "WINDOWS SERVER", "WIN 11", "WIN 10") or (has("SISTEMA OPERATIVO") and has("WINDOWS"))) \
       and has("HOME", "PRO", "PROFESSIONAL", "64-BIT", "64BIT", "ESD", "OEM", "DSP", "FPP", "COA", "LICENCIA", "LICENSE", "ROK", "CAL", "LEGALIZACION") \
       and lacks("LAPTOP", "NOTEBOOK", "COMPUTADORA", "PC ", "ALL-IN-ONE", "TODO EN UNO", "TABLET", "MONITOR", "DUAL DRIVE", "FLASH DRIVE", "PENDRIVE", "MEMORIA USB", "SSD", "HDD", "UNIDAD OPTICA", "OPTICA", "DVD"):
        return "sistemas_operativos"

    # -------------------------------------------------------------
    # 52. ANTIVIRUS & SEGURIDAD DIGITAL
    # -------------------------------------------------------------
    if has("KASPERSKY", "NORTON", "BITDEFENDER", "ESET", "MCAFEE", "MALWAREBYTES") or (has("ANTIVIRUS", "TOTAL SECURITY", "INTERNET SECURITY") and lacks("DECO", "ROUTER", "MESH", "FIREWALL", "HILLSTONE", "FORTINET", "APPLIANCE", "SWITCH", "CAMARA", "NVR", "DVR", "POE", "ADAPTADOR", "LAPTOP")):
        if has("USUARIO", "DISPOSITIVO", "AÑO", "AÑOS", "LICENCIA", "SUSCRIPCION", "ESD", "RENOVACION", "SECURITY", "ANTIVIRUS", "STANDARD", "PLUS", "PREMIUM"):
            return "antivirus_seguridad_digital"

    # -------------------------------------------------------------
    # 50. OFIMATICA & PRODUCTIVIDAD
    # -------------------------------------------------------------
    if (has("MICROSOFT 365", "OFFICE 2021", "OFFICE 2024", "OFFICE HOGAR", "OFFICE HOME", "OFFICE PERSONAL", "M365", "OFFICE BUSINESS") or (has("OFFICE") and has("FAMILIA", "PERSONAL", "HOGAR", "EMPRESA", "MEDIO ELECTRONICO", "ESD", "FPP"))) \
       and lacks("LAPTOP", "NOTEBOOK", "COMPUTADORA", "PC ", "ALL-IN-ONE", "BANDEJA"):
        return "ofimatica_productividad"

    # -------------------------------------------------------------
    # 51. SOFTWARE CONTABLE Y ADMINISTRATIVO
    # -------------------------------------------------------------
    if (re.search(r'\b(ASPEL|CONTPAQI|CONTPAQ)\b', n) or has("FACTURA ELECTRONICA", "CFDI")) \
       and lacks("AUDIFONOS", "AUDÍFONOS", "HEADSET", "NOISE", "CANCELLING", "TWS", "NVR", "DVR", "CAMARA", "CÁMARA", "COLORES", "BACO", "CABLE", "LECTOR", "TERMINAL", "FLASH USB", "BATERIA", "BATERÍA") \
       and not sku_starts("BOC", "NVR", "DVR", "ACC", "CAB", "CAR"):
        return "software_contable_administrativo"

    # -------------------------------------------------------------
    # 53. GARANTIAS & POLIZAS DE SERVICIO
    # -------------------------------------------------------------
    if has("CARE PACK", "GARANTIA EXTENDIDA", "GARANTÍA EXTENDIDA", "POLIZA DE SERVICIO", "PÓLIZA DE SERVICIO", "EXTENSION DE GARANTIA", "EXTENSIÓN DE GARANTÍA", "ON-SITE", "SMARTNET", "CON-SNT"):
        return "garantias_polizas_servicio"

    # -------------------------------------------------------------
    # 58. LIMPIEZA & MANTENIMIENTO
    # -------------------------------------------------------------
    if has("AIRE COMPRIMIDO", "REMOVEDOR DE POLVO", "ESPUMA LIMPIADORA", "TOALLITAS ANTIESTATICAS", "TOALLITAS ANTIESTÁTICAS", "ALCOHOL ISOPROPILICO", "ALCOHOL ISOPROPÍLICO", "LIMPIADOR DE PANTALLAS", "KIT DE LIMPIEZA", "PASTA TERMICA", "PASTA TÉRMICA", "GRASA TERMICA", "GRASA TÉRMICA", "CLEANING WIPES", "COMPRESSED AIR", "LIMPIEZA DE CIRCUITOS", "TOALLAS HUMEDAS PARA LIMPIEZA") \
       and lacks("LAMPARA", "LÁMPARA", "LAMP", "PROYECTOR", "TINTA", "TONER", "CARTUCHO", "IMPRESORA"):
        return "limpieza_mantenimiento"

    # -------------------------------------------------------------
    # 64. CANDADOS DE SEGURIDAD KENSINGTON
    # -------------------------------------------------------------
    if (has("CANDADO", "KENSINGTON") or (has("CABLE DE SEGURIDAD") and has("LLAVE", "COMBINACION", "COMBINACIÓN", "GUAYA", "RANURA", "LOCK"))) \
       and has("LAPTOP", "NOTEBOOK", "MONITOR", "LLAVE", "COMBINACION", "COMBINACIÓN", "GUAYA", "RANURA", "NANOSAVER", "MICROSAVER", "SLIM", "CLAVE", "SEGURIDAD", "LOCK") \
       and lacks("COMPUTADORA PORTATIL", "COMPUTADORA PORTÁTIL", "CORE I", "RYZEN", "TITAN MINI", "XBOOK", "DESKTOP", "TODO EN UNO", "ASUS TUF", "DELL INSPIRON"):
        return "candados_seguridad_laptop"

    # -------------------------------------------------------------
    # 63. HERRAMIENTAS DE SERVICIO TECNICO
    # -------------------------------------------------------------
    if has("PONCHADORA", "CRIMPADORA", "PINZA PONCHADORA", "PINZA DE IMPACTO", "PROBADOR DE CABLE", "TESTER DE CABLE", "TESTER DE RED", "DESARMADOR", "DESTORNILLADOR", "JUEGO DE DESTORNILLADORES", "KIT DE HERRAMIENTAS", "CAUTIN", "CAUTÍN", "PELACABLE", "MULTIMETRO", "MULTÍMETRO", "INSERTADORA DE IMPACTO") \
       and lacks("WINDOWS", "SERVER", "LICENCIA", "ROK", "CAL", "MICROSOFT", "SOFTWARE", "CONECTOR", "JACK RJ45", "PLUG RJ45", "PATCH CORD", "BOBINA"):
        return "herramientas_servicio_tecnico"

    # -------------------------------------------------------------
    # 60. MOCHILAS, FUNDAS Y MALETINES
    # -------------------------------------------------------------
    if has("MOCHILA", "FUNDA PARA LAPTOP", "FUNDA PARA NOTEBOOK", "MALETIN", "MALETÍN", "PORTAFOLIO PARA LAPTOP", "BACKPACK", "SLEEVE", "CASE LOGIC", "BOLSO PARA LAPTOP", "FUNDA NEOPRENO", "MALETA PARA LAPTOP") \
       and lacks("COMPUTADORA PORTATIL", "COMPUTADORA PORTÁTIL", "LAPTOP ASUS", "LAPTOP HP", "LAPTOP DELL", "LAPTOP LENOVO", "LAPTOP ACER", "TABLETA", "TABLET KIDS", "MATEPAD", "IPAD", "CORE I", "RYZEN", "VENTILADOR", "POWER STRIP", "SOCKET", "CONTACTOS", "MULTICONTACTO", "REGULADOR", "GOMA HONEYWELL", "TERMINAL CK", "TERMINAL EDA", "PARA TERMINAL"):
        return "mochilas_fundas_maletines"

    # -------------------------------------------------------------
    # 34. BIOMETRIA Y ACCESO
    # -------------------------------------------------------------
    if has("CONTROL DE ACCESO", "LECTOR DE HUELLA", "HUELLA DIGITAL", "TERMINAL BIOMETRICA", "TERMINAL BIOMÉTRICA", "BIOMETRICO", "BIOMÉTRICO", "RELOJ CHECADOR", "CHAPA MAGNETICA", "CHAPA MAGNÉTICA", "CERRADURA INTELIGENTE", "TARJETA RFID", "TAG RFID", "BOTON LIBERADOR", "BOTÓN LIBERADOR", "CONTRACERRADURA", "LECTORA DE PROXIMIDAD", "TORNIQUETE") \
       and lacks("IPAD", "TABLET", "TABLETA", "APPLE", "M2", "WIFI + CELL", "SPACE GRAY", "MATEPAD", "SMARTPHONE", "DVR", "NVR"):
        return "control_acceso_biometricos"

    # -------------------------------------------------------------
    # 29. MICROFONOS
    # -------------------------------------------------------------
    if (has("MICROFONO", "MICRÓFONO") or (has("MICROPHONE") and lacks("HEADSET", "DIADEMA"))) \
       and has("USB", "STREAMING", "PODCAST", "ESTUDIO", "VOCAL", "XLR", "OMNIDIRECCIONAL", "CARDIOIDE", "ESCRITORIO", "CONDENSADOR", "CONDENSER", "SOLAPA", "LAVALIER", "INALAMBRICO", "INALÁMBRICO", "STAND") \
       and lacks("DVR", "TURBOHD", "KIT TURBO", "KIT DVR", "CAMARA", "CÁMARA", "NVR", "CCTV", "DOMO", "BALA", "CANALES", "DIADEMA", "HEADSET", "AUDIFONOS", "AUDÍFONOS", "AURICULAR", "TELEFONO", "TELÉFONO", "GABINETE", "CONVERTIDOR", "TARJETA DE SONIDO", "TARJETA SONIDO", "SOPORTE PARA", "BASE PARA", "BRAZO PARA", "CABLE", "POLY V12", "VIDEOCONFERENCIA", "VIDEO CONFERENCIA", "POLY STUDIO", "SISTEMA DE VIDEO"):
        return "microfonos"

    # -------------------------------------------------------------
    # 30. WEBCAMS & VIDEOCONFERENCIA
    # -------------------------------------------------------------
    if (has("CAMARA WEB", "CÁMARA WEB", "WEBCAM") or (has("CAMARA") and has("VIDEOCONFERENCIA")) or has("PANACAST", "MEETUP", "BRIO 300", "BRIO 500", "C920", "C922", "C925", "C930")) \
       and lacks("COMPUTADORA PORTATIL", "COMPUTADORA PORTÁTIL", "LAPTOP", "NOTEBOOK", "SWITCH", "CATALYST", "CISCO", "GABINETE", "PANTALLA", "MONITOR", "ROUTER", "TONER", "TÓNER", "LEXMARK", "TAPA", "TAPA DE PRIVACIDAD", "PROTECTOR", "TRIPIE", "TRÍPIE", "TRIPIÉ", "TRIPODE", "TRÍPODE"):
        return "webcams_videoconferencia"

    # -------------------------------------------------------------
    # 21. CARGADORES, BATERIAS & POWER BANKS
    # -------------------------------------------------------------
    if (has("POWER BANK", "POWERBANK", "BATERIA PORTATIL", "BATERÍA PORTÁTIL", "BATERIA EXTERNA", "BATERÍA EXTERNA") or (has("CARGADOR") and has("PARED", "LAPTOP", "TIPO C", "USB-C", "CARRO", "AUTO", "INALAMBRICO", "INALÁMBRICO", "RAPIDO", "RÁPIDO")) or has("ELIMINADOR UNIVERSAL", "ELIMINADOR DE CORRIENTE")) \
       and lacks("TAPE", "AUTOLOADER", "STORAGE MSL", "LTO-8", "LTO-9", "SAS DRIVE", "FIBRE CHANNEL", "SERVIDOR", "SERVER", "UPS", "NO BREAK", "NO-BREAK", "REGULADOR", "KIOSCO", "MINI KIOSCO", "TERMINAL DE COBRO", "PLUG PARA CARGADOR", "BASE DE CARGA HONEYWELL"):
        return "cargadores_baterias_powerbanks"

    # -------------------------------------------------------------
    # 28. BOCINAS, BARRAS DE SONIDO & BAFLES
    # -------------------------------------------------------------
    if (has("BOCINA", "BOCINAS", "BARRA DE SONIDO", "SOUNDBAR", "BAFLE", "ALTAVOZ", "ALTAVOCES") or (has("SPEAKER") and lacks("HEADSET", "DIADEMA"))) \
       and lacks("MONITOR", "PANTALLA", "NVR", "DVR", "CAMARA", "CÁMARA", "VIDEO PORTERO", "PORTERO", "TELEFONO", "TELÉFONO", "ADAPTADOR STEREO", "CABLE AUDIO", "HEADSET", "DIADEMA", "AUDIFONOS", "AUDÍFONOS", "TROMPETA", "SIRENA"):
        return "bocinas_sonido"

    # -------------------------------------------------------------
    # 27. DIADEMAS & HEADSETS
    # -------------------------------------------------------------
    if has("DIADEMA", "HEADSET", "AUDIFONOS", "AUDÍFONOS", "EARBUDS", "AURICULARES") \
       and lacks("MONITOR", "PANTALLA", "CABLE", "BASE HEADSET", "ADAPTADOR", "CONVERTIDOR", "DIVISOR DE AUDIO", "MICROFONO DE SOLAPA") \
       and not sku_starts("ACC", "CAB"):
        return "diademas_headsets"

    # -------------------------------------------------------------
    # 59. CABLES & ADAPTADORES
    # -------------------------------------------------------------
    if (has("CABLE HDMI", "CABLE DISPLAYPORT", "CABLE USB", "CABLE TIPO C", "CABLE LIGHTNING", "CABLE VGA", "CABLE AUDIO", "CABLE PODER", "CABLE ALIMENTACION", "CABLE SATA", "ADAPTADOR HDMI", "ADAPTADOR DISPLAYPORT", "ADAPTADOR USB", "ADAPTADOR TIPO C", "CONVERTIDOR DE VIDEO") or (has("PATCH CORD") and lacks("BOBINA")) or (has("CABLE ") and has("METROS", "MTS", "1.8M", "2M", "3M", "1M", "0.5M"))) \
       and lacks("MONITOR", "PANTALLA", "SMART MONITOR", "NOTEBOOK", "LAPTOP", "DESKTOP", "TV ", "BOBINA UTP", "BOBINA DE CABLE"):
        return "cables_adaptadores"

    # -------------------------------------------------------------
    # 10. MONITORES & PANTALLAS
    # -------------------------------------------------------------
    if (sku_starts("MON") or (sku_starts("PAN") and lacks("PROYECCION", "PROYECCIÓN", "PANTALLA DE PROYECCION", "PANTALLA DE PROYECCIÓN", "PANTALLA DE PARED", "PANTALLA MURAL", "TRIPODE", "TRÍPODE")) or has("MONITOR ", "PANTALLA GAMER", "SMART MONITOR")) \
       and has("PULGADAS", "\"", "FHD", "QHD", "4K", "144HZ", "165HZ", "100HZ", "60HZ", "240HZ", "IPS", "VA", "OLED", "CURVO", "CURVED", "GAMING", "VIEWFINITY", "ESSENTIAL", "S3", "S5", "S7", "ODYSSEY") \
       and lacks("SOPORTE", "BRAZO", "CABLE", "LIMPIADOR", "PROTECTOR", "FUNDA", "LAPTOP", "NOTEBOOK", "ALL IN ONE", "ALL-IN-ONE", "TODO EN UNO", "MOUNTING", "KIT DE MONTAJE", "PROYECCION", "PROYECCIÓN", "PANTALLA DE PROYECCION", "PANTALLA DE PARED", "PANTALLA MURAL", "TRIPODE", "TRÍPODE") \
       and not sku_starts("ACC", "CAB", "PANSCR"):
        return "monitores_pantallas"

    # -------------------------------------------------------------
    # 19. NO BREAKS & UPSS
    # -------------------------------------------------------------
    if (sku_starts("NOB", "UPS") or has("NO-BREAK", "NO BREAK", "SISTEMA UPS", "UPS INTERACTIVO", "UPS ON-LINE", "SMART-UPS", "BACK-UPS")) \
       and lacks("BATERIA PORTATIL", "POWER BANK", "REGULADOR", "ESTAND", "STAND", "TARJETA"):
        return "no_breaks_ups"

    # -------------------------------------------------------------
    # 20. REGULADORES DE VOLTAJE
    # -------------------------------------------------------------
    if (sku_starts("REG") or has("REGULADOR DE VOLTAJE", "REGULADOR AUTOMATICO", "SUPRESOR DE PICOS", "BARRA DE CONTACTOS", "MULTICONTACTO")) \
       and lacks("NO-BREAK", "NO BREAK", "UPS"):
        return "reguladores_voltaje"

    # -------------------------------------------------------------
    # 11. TECLADOS
    # -------------------------------------------------------------
    if (sku_starts("TEC") or has("TECLADO")) and lacks("MOUSE", "RATON", "RATÓN", "KIT ", "COMBO", "FUNDA", "ROTULADOR"):
        return "teclados"

    # -------------------------------------------------------------
    # 12. RATONES & MOUSE
    # -------------------------------------------------------------
    if (sku_starts("MOU") or has("MOUSE", "RATON", "RATÓN")) and lacks("TECLADO", "KIT ", "COMBO", "MOUSEPAD", "PAD"):
        return "ratones_mouse"

    # -------------------------------------------------------------
    # 13. COMBOS TECLADO Y RATON
    # -------------------------------------------------------------
    if has("KIT TECLADO Y", "COMBO TECLADO", "TECLADO Y MOUSE", "TECLADO Y RATON", "TECLADO Y RATÓN"):
        return "combos_teclado_mouse"

    # -------------------------------------------------------------
    # 31. PROYECTORES DE VIDEO & PANTALLAS MURALES
    # -------------------------------------------------------------
    if (sku_starts("PANSCR") or has("PROYECTOR", "VIDEOPROYECTOR", "POWERLITE", "PANTALLA DE PROYECCION", "PANTALLA DE PROYECCIÓN", "PANTALLA DE PARED MANUAL")) \
       and lacks("LAMPARA", "LÁMPARA", "LAMP", "SOPORTE", "CAJA P/MESA", "TRIPIE", "TRÍPIE", "TRIPIÉ", "TRIPODE", "TRÍPODE", "KIT DE MONTAJE", "MONTAJE EN TECHO") \
       and not sku_starts("ACC", "CAB"):
        return "proyectores_presentacion"

    # -------------------------------------------------------------
    # 32. CAMARAS DE SEGURIDAD CCTV
    # -------------------------------------------------------------
    if (sku_starts("CAM") or has("CAMARA BALA", "CAMARA DOMO", "CAMARA IP", "CAMARA TURBOHD", "CAMARA DE SEGURIDAD", "CAMARA PTZ", "CÁMARA IP", "CÁMARA BALA", "CÁMARA DOMO")) \
       and lacks("WEBCAM", "CAMARA WEB", "FOTOGRAFICA", "DVR", "NVR", "CAJA CONEXION", "CAJA DE CONEXION", "CAJA DE CONEXIÓN", "CAJA CONEXIÓN", "BRAZO", "SOPORTE") \
       and not sku_starts("ACC", "CAB"):
        return "camaras_seguridad_cctv"

    # -------------------------------------------------------------
    # 33. GRABADORES DVR & NVR
    # -------------------------------------------------------------
    if (sku_starts("NVR", "DVR", "GRD") or has("DVR ", "NVR ", "GRABADOR DVR", "GRABADOR NVR", "TURBOHD DVR", "XVR ")) \
       and lacks("DISCO DURO", "CAMARA", "OREJAS", "RACK KIT", "MONTAJE") \
       and not sku_starts("ACC", "CAB"):
        return "grabadores_dvr_nvr"

    # -------------------------------------------------------------
    # 35. ALARMAS Y SENSORES
    # -------------------------------------------------------------
    if has("SENSOR DE MOVIMIENTO", "SIRENA", "PANEL DE ALARMA", "SENSOR MAGNETICO", "DETECTOR DE HUMO", "ESTROBO"):
        return "alarmas_sensores_seguridad"

    # -------------------------------------------------------------
    # 36. TELEFONIA & CONMUTADORES
    # -------------------------------------------------------------
    if has("TELEFONO IP", "TELÉFONO IP", "CONMUTADOR IP", "TELEFONO SIP", "TELEFONO EJECUTIVO", "GRANDSTREAM GXP", "TELEFONO INALAMBRICO"):
        return "telefonia_conmutadores"

    # -------------------------------------------------------------
    # 37. SWITCHES DE RED
    # -------------------------------------------------------------
    if (sku_starts("SWI", "SWT") or has("SWITCH DE RED", "SWITCH ETHERNET", "SWITCH POE", "SWITCH GIGABIT", "SWITCH GESTIONABLE", "SWITCH NO ADMINISTRABLE")) \
       and lacks("NINTENDO", "TECLADO"):
        return "switches_red"

    # -------------------------------------------------------------
    # 38. ROUTERS & ACCESS POINTS
    # -------------------------------------------------------------
    if sku_starts("ROU", "WIF") or has("ROUTER INALAMBRICO", "ROUTER WIFI", "ACCESS POINT", "PUNTO DE ACCESO", "REPETIDOR WIFI", "SISTEMA MESH", "DECO "):
        return "routers_access_points"

    # -------------------------------------------------------------
    # 39. ANTENAS & RADIOENLACES
    # -------------------------------------------------------------
    if (has("ANTENA", "RADIOENLACE", "AIRMAX", "NANOLIGHT", "LITEBEAM", "POWERBEAM", "ROCKET", "UNIFI OUTDOOR") or sku_starts("ANT")) \
       and lacks("ADAPTADOR DE RED USB", "ADAPTADOR DUAL BAND", "ADAPTADOR USB", "EXTENSOR", "SOPORTE PARA ANTENA") \
       and not sku_starts("TAR", "ACC", "CAB"):
        return "antenas_radioenlaces"

    # -------------------------------------------------------------
    # 40. CABLEADO ESTRUCTURADO
    # -------------------------------------------------------------
    if has("BOBINA UTP", "BOBINA DE CABLE", "CABLE UTP", "CONECTOR RJ45", "JACK RJ45", "PATCH PANEL", "FACEPLATE"):
        return "cableado_estructurado"

    # -------------------------------------------------------------
    # 41. FIBRA OPTICA & TRANSCEIVERS
    # -------------------------------------------------------------
    if (sku_starts("SFP", "TRA", "FIB") or has("FIBRA OPTICA", "FIBRA ÓPTICA", "TRANSCEIVER", "TRANSCEPTOR", "MODULO SFP", "MÓDULO SFP", "SFP+", "SFP ", "MINI-GBIC", "MINIGBIC", "CABLE DROP", "PIGTAIL", "ACOPLADOR DE FIBRA", "10GBASE", "1000BASE")) \
       and lacks("BROADCOM", "TAPA HDMI", "WALLPLATE", "TAPA", "PLACA DE PARED", "MICROFIBRA", "FIBRA DE CARBON", "FIBRA DE CARBÓN", "ESCRITORIO", "SILLA", "TABLA", "MOUSEPAD", "PAD", "BALUN", "BALUM", "TRANSCEPTOR PASIVO", "TRANSCEPTORES PASIVOS", "CCTV", "HDCVI", "TURBOHD", "AHD", "CÁMARAS DE SEGURIDAD", "CAMARAS DE SEGURIDAD", "SAXXON", "PARA VIDEO", "VB-") \
       and not sku_starts("CAB"):
        return "fibra_optica_transceivers"

    # -------------------------------------------------------------
    # 42. RACKS & GABINETES DE SERVIDOR
    # -------------------------------------------------------------
    if has("RACK DE PARED", "RACK DE PISO", "GABINETE DE PARED", "ORGANIZADOR VERTICAL", "ORGANIZADOR HORIZONTAL", "BANDEJA PARA RACK", "GABINETE RACK"):
        return "racks_gabinetes_servidor"

    # -------------------------------------------------------------
    # 46. PLOTTERS DE GRAN FORMATO
    # -------------------------------------------------------------
    if (has("PLOTTER", "GRAN FORMATO", "DESIGNJET", "SURECOLOR", "IMAGEPROGRAF") or sku_starts("PLO")) \
       and lacks("PAPEL", "TINTA", "CARTUCHO", "TANQUE", "PFI-", "ESCANER", "ESCÁNER", "CABEZAL", "BOTELLA") \
       and not sku_starts("CAR", "TIN", "ACC", "CAB"):
        return "plotters_gran_formato"

    # -------------------------------------------------------------
    # 43. IMPRESORAS & MULTIFUNCIONALES (Oficina & Hogar)
    # -------------------------------------------------------------
    if (sku_starts("IMP", "MLT") or has("IMPRESORA", "ECOTANK", "SMART TANK", "LASERJET", "DESKJET") or (has("MULTIFUNCIONAL") and has("IMPRESORA", "MONOCROMATICA", "MONOCROMÁTICA", "LASER", "LÁSER", "INYECCION", "INYECCIÓN", "DUPLEX", "DÚPLEX", "WIFI", "FAX", "COPIADORA", "SCANNER", "ESCÁNER", "ESCANER", "BROTHER", "EPSON", "CANON", "HP ", "XEROX", "RICOH", "KYOCERA", "PANTUM"))) \
       and lacks("TONER", "TÓNER", "TINTA", "CARTUCHO", "PAPEL", "CABEZAL", "RODILLO", "MANTENIMIENTO", "PLOTTER", "DESIGNJET", "SURECOLOR", "TRIPIE", "TRÍPIE", "TRIPIÉ", "TRIPODE", "TRÍPODE", "HERRAMIENTA", "MOCHILA", "FUNDA", "CINTA", "RIBBON", "BOTELLA RESIDUAL", "DEPOSITO DE DESECHO", "DEPÓSITO", "KIT DE LIMPIEZA", "TARJETAS ADHESIVAS", "MINIPRINTER", "MINI IMPRESORA", "IMPRESORA TERMICA", "IMPRESORA TÉRMICA", "TICKETS", "58MM", "58 MM", "80MM", "80 MM", "PUNTO DE VENTA", "POS", "BATERIA", "BATERÍA") \
       and not sku_starts("CAR", "TON", "TIN", "ACC", "CAB", "RIB", "BAT"):
        return "impresoras_multifuncionales"

    # -------------------------------------------------------------
    # 44. TONERS LASER
    # -------------------------------------------------------------
    if (sku_starts("TON") or has("TONER", "TÓNER")) \
       and lacks("IMPRESORA", "MULTIFUNCIONAL", "SENSOR", "PCB", "BOTONERA", "ORVIBO", "DEPOSITO DE DESECHO", "DEPÓSITO") \
       and not sku_starts("ACC", "CAB"):
        return "toners_laser"

    # -------------------------------------------------------------
    # 45. TINTAS & CARTUCHOS
    # -------------------------------------------------------------
    if (sku_starts("TIN") or (sku_starts("CAR") and has("TINTA", "CARTUCHO", "TANQUE")) or has("BOTELLA DE TINTA", "CARTUCHO DE TINTA", "TINTA ORIGINAL", "TINTA EPSON", "TINTA CANON", "TINTA HP", "TINTA BROTHER", "TANQUE CANON", "PFI-")) \
       and lacks("IMPRESORA", "MULTIFUNCIONAL", "PLOTTER HP", "PLOTTER CANON", "CINTA RIBBON", "SELLO") \
       and not sku_starts("ACC", "CAB"):
        return "tintas_cartuchos"

    # -------------------------------------------------------------
    # 47. ETIQUETAS & RIBBONS
    # -------------------------------------------------------------
    if has("RIBBON", "CINTA RIBBON", "ETIQUETAS TERMICAS", "ETIQUETA TERMICA", "ROLLO TERMICO", "PAPEL TERMICO", "ROLLO DE ETIQUETAS"):
        return "etiquetas_ribbons"

    # -------------------------------------------------------------
    # 48. ESCANERES & DIGITALIZADORES
    # -------------------------------------------------------------
    if (has("ESCANER", "ESCÁNER", "SCANJET", "DIGITALIZADOR DE DOCUMENTOS", "CAMA PLANA") or sku_starts("SCN")) \
       and lacks("CODIGO DE BARRAS", "CÓDIGO DE BARRAS", "CODIGO DE BARRA", "CÓDIGO DE BARRA", "BARCODE", "BARCODE SCANNER", "LECTOR DE CODIGO", "LECTOR DE CÓDIGO", "HUELLAS", "ENROLADOR", "CONVERTIDOR", "SERIAL", "DB9", "FUNDA", "CORREA") \
       and not sku_starts("ACC", "CAB", "LCT"):
        return "escaneres_digitalizadores"

    # -------------------------------------------------------------
    # 54. PUNTO DE VENTA (POS)
    # -------------------------------------------------------------
    if has("PUNTO DE VENTA", "LECTOR DE CODIGO", "LECTOR DE CÓDIGO", "IMPRESORA TERMICA", "IMPRESORA TÉRMICA", "IMPRESORA DE TICKETS", "CAJON DE DINERO", "CAJÓN DE DINERO", "MINIPRINTER", "MINIPRINTERS", "CAJA PARA DINERO", "MINI IMPRESORA", "TERMINAL POS", "BARCODE SCANNER", "EC-LINE", "QIAN ANJET", "MNP-158", "MNP-180", "SOFTWARE POS", "POS TOOLS", "POSTOOLS"):
        return "punto_de_venta"

    # -------------------------------------------------------------
    # 55. SMARTPHONES & CELULARES
    # -------------------------------------------------------------
    if (sku_starts("CEL", "SMA") or has("SMARTPHONE", "TELEFONO CELULAR", "TELÉFONO CELULAR", "IPHONE", "GALAXY S", "GALAXY A", "REDMI", "MOTO G")) \
       and lacks("ANCLA", "RANURA K-SLOT", "CANDADO", "BRAZALETE", "SOPORTE", "FUNDA", "MICA", "CRISTAL TEMPLADO", "CABLE", "VIDEOPORTERO", "BATERIA", "BATERÍA", "PLOMO", "TECLADO", "MOUSE") \
       and not sku_starts("ACC", "CAB", "BAT", "TEC", "MOU", "SOF", "LIC"):
        return "smartphones_celulares"

    # -------------------------------------------------------------
    # 56. TABLETS & IPADS
    # -------------------------------------------------------------
    if (sku_starts("TAB", "IPD") or (has("IPAD", "GALAXY TAB", "MATEPAD") or (has("TABLET", "TABLETA") and has("PULGADAS", "WIFI", "ANDROID", "PANTALLA")))) \
       and lacks("PLUMA", "STYLUS", "FUNDA", "SOPORTE", "MICA", "CRISTAL", "ADAPTADOR", "CABLE", "TECLADO PARA", "VENTILADOR", "DISIPADOR", "ANCLA", "NUC", "MINI PC", "BAREBONE", "MICROFONO", "MICRÓFONO", "BOCINA") \
       and not sku_starts("ACC", "CAB", "CAR", "CPU", "BOC", "MIC", "CAM"):
        return "tablets_ipads"

    # -------------------------------------------------------------
    # 57. SMARTWATCHES & WEARABLES
    # -------------------------------------------------------------
    if has("SMARTWATCH", "RELOJ INTELIGENTE", "GALAXY WATCH", "APPLE WATCH", "BANDA INTELIGENTE", "SMART BAND"):
        return "smartwatches_wearables"

    # -------------------------------------------------------------
    # 61. SOPORTES & ERGONOMIA
    # -------------------------------------------------------------
    if has("SOPORTE PARA MONITOR", "BRAZO PARA MONITOR", "BASE PARA MONITOR", "SOPORTE ARTICULADO", "SOPORTE DE TV", "SOPORTE DE TECHO", "SOPORTE DE PARED", "TAPETE ANTIFATIGA", "DESCANSA PIES"):
        return "soportes_ergonomia"

    # -------------------------------------------------------------
    # 62. HUBS, DOCKS & ESTACIONES
    # -------------------------------------------------------------
    if has("DOCKING STATION", "HUB USB", "ESTACION DE ACOPLAMIENTO", "ADAPTADOR MULTIPUERTO") and lacks("MOUSE", "TECLADO"):
        return "hubs_docks_estaciones"

    # -------------------------------------------------------------
    # 65. CLIMATIZACION & MINISPLITS
    # -------------------------------------------------------------
    if has("MINISPLIT", "AIRE ACONDICIONADO", "INVERTER 1 TON", "INVERTER 1.5 TON", "INVERTER 2 TON", "CLIMA"):
        return "climatizacion_aires_acondicionados"

    # -------------------------------------------------------------
    # 66. GAMING, CONSOLAS & SILLAS
    # -------------------------------------------------------------
    if has("SILLA GAMER", "SILLA DE JUEGO", "PLAYSTATION", "XBOX", "NINTENDO", "CONSOLA") and lacks("TARJETA DE EXPANSION", "SANDISK"):
        return "gaming_consolas_sillas"

    # -------------------------------------------------------------
    # 18. SERVIDORES ENTERPRISE
    # -------------------------------------------------------------
    if (sku_starts("SRV", "SVR", "SER") or has("SERVIDOR TORRE", "SERVIDOR RACK", "PROLIANT", "POWEREDGE", "SERVER TORRE", "SERVER RACK", "THINKSYSTEM")) \
       and lacks("MEMORIA RAM", "DISCO DURO", "LICENCIA", "WINDOWS SERVER ROK", "WINDOWS SERVER CAL", "GABINETE", "FUENTE", "CABLE", "USUARIO REMOTO", "CLIENTE VPN", "TARJETA RISER", "ADMINISTRADOR GRAFICO", "ADMINISTRADOR GRÁFICO", "XCLARITY") \
       and not sku_starts("ACC", "CAB", "MEM", "DDU"):
        return "servidores_enterprise"

    # -------------------------------------------------------------
    # 15. MINI PCS & NUCS
    # -------------------------------------------------------------
    if (has("MINI PC", "MINIPC", "CHOMP", "TINY", "ELITEDESK MINI", "PRODESK MINI", "MICRO DESKTOP", "TITAN MINI") or (has("NUC") and has("INTEL", "ASUS", "CORE", "BAREBONE", "MINI")) or sku_starts("RNUC")) \
       and lacks("CANDADO", "SOPORTE", "MONITOR", "DISCO DURO"):
        return "mini_pcs_nuc"

    # -------------------------------------------------------------
    # 17. COMPUTADORAS ALL IN ONE (AIO)
    # -------------------------------------------------------------
    if (sku_starts("AIO") or ((has("ALL IN ONE", "ALL-IN-ONE", "TODO EN UNO") or re.search(r'\bAIO\b', n)) and lacks("ENFRIADOR", "ENFRIAMIENTO", "REFRIGERACION", "REFRIGERACIÓN", "LIQUIDO", "LÍQUIDO", "LIQUID", "WATER", "LOOP", "PURE LOOP", "SILENT LOOP", "KRAKEN", "CORSAIR HYDRO", "VENTILADOR", "COOLER", "DISIPADOR", "FAN", "ARGB", "RADIADOR", "HERRAMIENTA", "CRIMPEAR", "CRIMPADORA", "PLUG", "BATERIA", "BATERÍA", "ROUTER", "SWITCH", "CANALETA", "CORTADORA", "PROTECTOR", "SOLAR", "PANEL SOLAR", "ENERGIA SOLAR", "ENERGÍA SOLAR", "TERMINAL POS", "TERMINAL ALL-IN-ONE", "TERMINAL ALL IN ONE", "EC-VP", "PUNTO DE VENTA", "BASE", "SOPORTE", "BRAZO"))):
        if sku_starts("AIO", "CPUDDL") or has("PROONE", "PROSTUDIO", "IDEACENTRE", "OPTIPLEX", "PAVILION AIO", "VERITON", "PC ALL IN ONE", "COMPUTADORA ALL IN ONE", "COMPUTADORA DE ESCRITORIO ALL IN ONE") or re.search(r'\b(INTEL|AMD|RYZEN|CELERON|CORE|PANTALLA|FHD|23\.8|21\.5|27"|24")\b', n):
            return "computadoras_all_in_one"

    # -------------------------------------------------------------
    # 14. LAPTOPS & COMPUTADORAS PORTATILES
    # -------------------------------------------------------------
    if (sku_starts("COMMAC", "POR", "LAP", "NOTE") or has("COMPUTADORA PORTATIL", "COMPUTADORA PORTÁTIL", "LAPTOP", "NOTEBOOK", "MACBOOK", "CHROMEBOOK") or has("THINKPAD", "IDEAPAD", "VIVOBOOK", "ZENBOOK", "ASPIRE", "LATITUDE", "VOSTRO", "INSPIRON", "EXPERTBOOK")) \
       and lacks("TARJETA", "RED GIGABIT", "ETHERNET", "TOALLA", "TOALLITAS", "LIMPIEZA", "BARRA DE LUZ", "LAMPARA", "LÁMPARA", "CARRITO", "CARRO", "GABINETE DE CARGA", "ESTACION DE CARGA", "ESTACIÓN DE CARGA", "STAND", "ELEVADOR", "BRAZO", "FILTRO DE PRIVACIDAD", "FILTRO PRIVACIDAD", "MICA", "SKIN", "VINIL", "CABLE", "ADAPTADOR", "CONVERTIDOR", "CARGADOR", "ELIMINADOR", "BATERIA", "BATERÍA", "FUNDA", "MALETIN", "MALETÍN", "MOCHILA", "CANDADO", "BASE", "SOPORTE", "COOLER", "ENFRIADOR", "VENTILADOR", "DOCK", "DOCKING", "HUB", "TECLADO PARA", "PANTALLA PARA", "DISPLAY PARA", "REPUESTO", "BISAGRA", "TOUCHPAD", "FLEX", "MEMORIA", "SODIMM", "SO-DIMM", "DISCO DURO", "SSD PORTATIL", "SSD PORTÁTIL", "DISCO PORTATIL", "DISCO EXTERNO", "MONITOR", "PANTALLA PORTATIL", "PANTALLA PORTÁTIL", "ENCLOSURE", "CANVIO", "NEW PULL", "PROTECTOR", "TAPA", "ESTUCHE"):
        if sku_starts("COMMAC", "POR", "LAP", "NOTE") or re.search(r'\b(CORE|RYZEN|CELERON|ATHLON|INTEL|AMD|M1|M2|M3|M4|M5|14"|15\.6"|16"|13\.3"|13\.6"|17\.3"|FHD|RAM|SSD|WINDOWS|FREEDOS|MACOS)\b', n):
            return "laptops_portatiles"

    # -------------------------------------------------------------
    # 16. COMPUTADORAS ENSAMBLADAS / GAMING PCs
    # -------------------------------------------------------------
    if (sku_starts("CFG-") or has("COMPUTADORA DE ESCRITORIO", "PC GAMER", "PC VECTEC", "EQUIPO DE ESCRITORIO", "COMPUTADORA ENSAMBLADA", "PC ENSAMBLADA", "DESKTOP VORAGO", "THINKCENTRE", "OPTIPLEX DESKTOP", "WORKSTATION DELL", "WORKSTATION HP", "WORKSTATION LENOVO") or (sku_starts("CPUDDL", "CPULEV", "CPUGET", "CPUQIA", "CPUYEY", "CPUVGO", "CPULEN") and has("PC", "DESKTOP", "ESCRITORIO", "TOWER", "TORRE"))) \
       and lacks("TODO EN UNO", "ALL-IN-ONE", "ALL IN ONE", "PORTATIL", "PORTÁTIL", "LAPTOP", "NOTEBOOK", "MINI PC", "NUC", "TARJETA PARALELA", "TARJETA SERIAL", "PUERTO PARALELO", "PROCESADOR RYZEN", "PROCESADOR INTEL", "PROCESADOR AMD", "4 CORE 4GHZ", "6 CORE 4.2GHZ", "6 CORE 65W", "RETAIL PLATAFORMA") \
       and not sku_starts("CPUINT", "CPUAMD", "MBD", "TAR", "ACC", "CAB"):
        return "computadoras_ensambladas"

    # -------------------------------------------------------------
    # 67. ACCESORIOS & MISCELANEOS (Default fallback)
    # -------------------------------------------------------------
    return "accesorios_perifericos"

