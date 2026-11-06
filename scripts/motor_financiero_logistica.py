# -*- coding: utf-8 -*-
"""
motor_financiero_logistica.py
==============================================================================
MOTOR FINANCIERO Y CUBICACIÓN LOGÍSTICA VECTEC
==============================================================================
Implementación canónica de la directiva técnica de cálculo financiero:
1. Cubicación y logística por categoría física (Micro/Pequeño, Mediano, Voluminoso/Pesado).
2. Protección de Utilidad Neta Libre del 20% para el negocio.
3. Absorción de Carga Fiscal (Retención Hacienda 1% - 2%).
4. Despliegue de promociones comerciales visibles (25% inauguración, 10% mayoreo, 5% cashback).
5. Inyección estricta de la Leyenda Legal Obligatoria.
==============================================================================
"""

from typing import Dict, Tuple, Any

# Parámetros Financieros Oficiales
TASA_UTILIDAD_NETA = 0.20       # 20% de ganancia neta libre
TASA_HACIENDA = 0.02            # 2% de retención fiscal (ISR / RESICO / Plataformas)
FACTOR_DENOMINADOR = 1.0 - (TASA_UTILIDAD_NETA + TASA_HACIENDA) # 1 - 0.22 = 0.78
DESCUENTO_VITRINA = 0.25        # 25% descuento visible en vitrina
FACTOR_VITRINA = 1.0 - DESCUENTO_VITRINA # 0.75
DESCUENTO_MAYOREO = 0.10        # 10% descuento por mayoreo

# Leyenda Legal Obligatoria
LEYENDA_PRECIO_OBLIGATORIA = (
    "Precio en pesos mexicanos (MXN). Precio sujeto a cambio o variación "
    "sin previo aviso debido a la fluctuación cambiaria del dólar."
)

# ==============================================================================
# TABLA DE CUBICACIÓN Y LOGÍSTICA POR CATEGORÍA FÍSICA
# ==============================================================================
CATEGORIAS_MICRO = {
    "procesadores",
    "memorias_ram_pc",
    "memorias_ram_laptop",
    "ssds_m2_nvme",
    "unidades_ssd_25",
    "memorias_usb_flash",
    "tarjetas_memoria_sd",
    "cables_adaptadores",
    "adaptadores_red_wifi",
    "herramientas_servicio_tecnico",
    "accesorios_perifericos",
    "software_licencias"
}

CATEGORIAS_MEDIANAS = {
    "tarjetas_madre",
    "tarjetas_video",
    "fuentes_energia",
    "enfriamiento",
    "discos_duros_hdd_internos",
    "discos_duros_externos",
    "teclados_mouses_combos",
    "audifonos_headsets",
    "bocinas_barras_sonido",
    "routers_access_points",
    "switches_redes",
    "impresoras_multifuncionales",
    "escaneres_digitalizadores",
    "terminales_punto_venta",
    "lectores_codigo_barras",
    "no_breaks_ups",
    "reguladores_voltaje",
    "soportes_ergonomia",
    "camaras_seguridad_cctv",
    "video_vigilancia_cctv"
}

CATEGORIAS_VOLUMINOSAS = {
    "gabinetes",
    "monitores_pantallas",
    "laptops_portatiles",
    "computadoras_all_in_one",
    "computadoras_de_escritorio",
    "computadoras_ensambladas",
    "servidores_chasis",
    "racks_gabinetes_red",
    "plotters_gran_formato",
    "linea_blanca_hogar",
    "refrigeradores_congeladores",
    "lavadoras_secadoras",
    "sillas_gamer_ergonomicas",
    "reguladores_industriales",
    "televisiones_pantallas_smart"
}

# Costos Logísticos (Embalaje + Flete Base)
COSTOS_LOGISTICA = {
    "micro": {
        "embalaje": 20.0,
        "flete": 99.0,
        "total": 119.0,
        "descripcion": "Micro / Pequeño (Burbuja ligera + Sobre de seguridad)"
    },
    "mediano": {
        "embalaje": 45.0,
        "flete": 155.0,
        "total": 200.0,
        "descripcion": "Mediano (Caja doble corrugado + Material de amortiguación)"
    },
    "voluminoso": {
        "embalaje": 90.0,
        "flete": 260.0,
        "total": 350.0,
        "descripcion": "Voluminoso / Pesado (Embalaje industrial reforzado + Flejado)"
    }
}


def clasificar_cubicacion(categoria: str, nombre: str = "") -> str:
    """
    Deduce el nivel de cubicación logística a partir de la categoría y atributos físicos.
    """
    cat = (categoria or "").strip().lower()
    nom = (nombre or "").upper()

    # Chequeo por palabras clave de gran volumen
    if any(k in nom for k in ["GABINETE", "MONITOR", "CHASIS", "SERVER", "RACK", "SILLA", "ALL IN ONE", "AIO"]):
        return "voluminoso"

    if cat in CATEGORIAS_MICRO:
        return "micro"
    elif cat in CATEGORIAS_VOLUMINOSAS:
        return "voluminoso"
    else:
        # Por defecto mediano
        return "mediano"


def calcular_precio_financiero(
    costo_mayoreo_mxn: float,
    categoria: str,
    nombre: str = "",
    tasa_hacienda: float = TASA_HACIENDA
) -> Dict[str, Any]:
    """
    Calcula el precio de cobro real (PVP_real), precio de vitrina (PVP_lista)
    y precio de mayoreo protegiendo exactamente un 20% de utilidad neta libre.

    Fórmula:
        PVP_real = (Costo Mayoreo + Gasto Logística) / (1 - (0.20 + Tasa Hacienda))
        PVP_lista = PVP_real / 0.75  (para aplicar 25% de inauguración en vitrina)
        PVP_mayoreo = PVP_real * 0.90
    """
    tipo_cub = clasificar_cubicacion(categoria, nombre)
    logistica = COSTOS_LOGISTICA[tipo_cub]
    gasto_logistica = logistica["total"]

    denominador = 1.0 - (TASA_UTILIDAD_NETA + tasa_hacienda)
    if denominador <= 0:
        denominador = 0.78

    # 1. Precio de Venta Real (lo que el cliente paga neto en checkout)
    pvp_real = round((costo_mayoreo_mxn + gasto_logistica) / denominador, 2)

    # 2. Precio de Vitrina / Lista (tachado con 25% de descuento visible)
    pvp_lista = round(pvp_real / FACTOR_VITRINA, 2)

    # 3. Precio Mayoreo (10% descuento sobre PVP real)
    pvp_mayoreo = round(pvp_real * (1.0 - DESCUENTO_MAYOREO), 2)

    # 4. Desglose analítico de rentabilidad
    monto_hacienda = round(pvp_real * tasa_hacienda, 2)
    ganancia_neta_libre = round(pvp_real * TASA_UTILIDAD_NETA, 2)
    margen_bruto_pct = round(((pvp_real - costo_mayoreo_mxn) / pvp_real) * 100, 2)

    return {
        "pvp_real": pvp_real,
        "pvp_lista": pvp_lista,
        "pvp_mayoreo": pvp_mayoreo,
        "descuento_vitrina_pct": 25,
        "descuento_mayoreo_pct": 10,
        "costo_mayoreo_mxn": costo_mayoreo_mxn,
        "gasto_logistica": gasto_logistica,
        "tipo_cubicacion": tipo_cub,
        "descripcion_cubicacion": logistica["descripcion"],
        "retencion_hacienda_mxn": monto_hacienda,
        "utilidad_neta_libre_mxn": ganancia_neta_libre,
        "margen_bruto_pct": margen_bruto_pct,
        "leyenda_obligatoria": LEYENDA_PRECIO_OBLIGATORIA
    }


def inyectar_leyenda_descripcion(descripcion: str) -> str:
    """
    Garantiza que la leyenda obligatoria figure en la descripción del producto
    sin duplicarse.
    """
    desc = (descripcion or "").strip()
    if LEYENDA_PRECIO_OBLIGATORIA in desc:
        return desc
    if desc:
        return f"{desc}\n\n{LEYENDA_PRECIO_OBLIGATORIA}"
    return LEYENDA_PRECIO_OBLIGATORIA
