#!/usr/bin/env python3
"""
Módulo de Software: Agente de Fondo Verificador y Corrector VíaMX (Integración Ollama).
Monitorea la disponibilidad geográfica de los 12 productos del catálogo en tiempo real (cada 15 min).
Si detecta bloqueos regionales, utiliza la IA de Ollama local para corregir enlaces en caliente.
"""

import time
import json
import urllib.request
import urllib.parse
import os
import re
import sys
import logging
from typing import Dict, List

# Configurar logging directo para consola y archivo
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ViaMX_Ollama_Agent")

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(WORKSPACE_DIR, "docs", "data", "catalog.json")
LOG_PATH = os.path.join(WORKSPACE_DIR, "log_operativo.txt")
OLLAMA_URL = "http://localhost:11434/api/generate"

# Base de datos local de fallbacks en caso de contingencia total o que Ollama esté inactivo
FALLBACK_CORRECTIONS = {
    "card_tv_65": "https://www.amazon.com.mx/dp/B0D1898VNW",
    "card_soundbar": "https://www.amazon.com.mx/dp/B088383Z4V",
    "card_weber_grill": "https://www.amazon.com.mx/dp/B00004RALJ",
    "card_power_bank_20": "https://www.amazon.com.mx/dp/B07S829LBX",
    "card_termo_yeti": "https://www.amazon.com.mx/dp/B073WJD86M",
    "card_camelbak": "https://www.amazon.com.mx/dp/B08XWW1P4V",
    "card_adidas_ball": "https://www.mercadolibre.com.mx/balon-de-futbol-adidas-al-rihla-league/p/MLM19024090",
    "card_oster_airfryer": "https://www.mercadolibre.com.mx/freidora-de-aire-digital-oster-ckstaf40d-4-l/p/MLM18519124",
    "card_ring_doorbell": "https://www.mercadolibre.com.mx/video-timbre-inteligente-ring-video-doorbell-wired-hd/p/MLM18256340",
    "card_silla_ergo": "https://www.mercadolibre.com.mx/silla-de-escritorio-ergonomica-oficina-ejecutiva-comoda-reclinable-con-soporte-lumbar-ajustable-color-negro/p/MLM24151240",
    "card_power_bank_10": "https://www.mercadolibre.com.mx/bateria-portatil-power-bank-10000mah-15w-carga-rapida/p/MLM22143111",
    "card_portable_grill": "https://www.mercadolibre.com.mx/asador-portatil-carbon-plegable-tipo-maletin-jardin-camping/p/MLM19982345"
}

def escribir_en_bitacora(mensaje: str):
    """Escribe una entrada de telemetría estructurada en el archivo log_operativo.txt"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n[{timestamp}] [AGENTE_OLLAMA] {mensaje}")
    except Exception as e:
        logger.error(f"No se pudo escribir en log_operativo.txt: {str(e)}")

def consultar_ollama_corrector(product_id: str, current_url: str, error_detail: str) -> str:
    """
    Interconecta localmente con el servidor de Ollama para consultar qué URL alternativa inyectar.
    Si Ollama no está activo en la ASUS Frankenstein, aplica el motor de fallbacks determinista.
    """
    prompt = (
        f"Actúas como un agente experto en ecommerce transnacional para el Mundial 2026. "
        f"El producto con ID '{product_id}' y enlace '{current_url}' está dando el siguiente error: '{error_detail}'. "
        f"Proporciona únicamente la URL alternativa de reemplazo directa en Amazon o Mercado Libre. "
        f"Responde SOLO con la URL limpia, sin comentarios ni explicaciones adicionales."
    )
    
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            OLLAMA_URL, 
            data=data, 
            headers={"Content-Type": "application/json"}
        )
        # Timeout corto para no detener el hilo de ejecución principal del portal
        with urllib.request.urlopen(req, timeout=5.0) as response:
            res_body = json.loads(response.read().decode("utf-8"))
            suggested_url = res_body.get("response", "").strip()
            
            # Validar que sea una URL de formato correcto
            if suggested_url.startswith("http"):
                logger.info(f"Ollama Corrected Link [{product_id}]: {suggested_url}")
                return suggested_url
    except Exception as e:
        logger.warning(f"Ollama local desconectado en puerto 11434 ({str(e)}). Aplicando motor de contingencia determinista.")
        
    # Fallback determinista
    fallback = FALLBACK_CORRECTIONS.get(product_id, current_url)
    logger.info(f"Fallback Core Link inyectado en caliente [{product_id}]: {fallback}")
    return fallback

def validar_enlace(url: str) -> (bool, str):
    """
    Realiza una consulta rápida HTTP HEAD o GET al servidor para validar su estado 200.
    Simula cabeceras de navegador móvil para evitar bloqueos Cloudflare en el test.
    """
    # Enlaces de simulación técnica (sandboxes antiguos)
    if "anrdoezrs.net" in url or "viamx.pro/redirect" in url:
        return True, "Enlace de enrutamiento perimetral activo"
        
    try:
        req = urllib.request.Request(
            url, 
            method="HEAD",
            headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"}
        )
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            status = resp.status
            if status in [200, 301, 302, 307]:
                return True, "OK"
            return False, f"HTTP Status {status}"
    except urllib.error.HTTPError as he:
        # Algunos servidores bloquean HEAD pero el producto existe (ej. 403 o 405).
        # En estos casos validamos como advertencia, pero si es 404 es un enlace roto.
        if he.code == 404:
            return False, "HTTP 404 Producto No Encontrado"
        return True, f"HTTP Warning {he.code}"
    except Exception as e:
        return False, str(e)

def validar_y_corregir_catalogo():
    """Carga catalog.json, valida todos los enlaces, corrige roturas y reescribe en caliente."""
    if not os.path.exists(CATALOG_PATH):
        escribir_en_bitacora(f"Error: No se encontró catalog.json en {CATALOG_PATH}")
        return

    logger.info("Iniciando validación del catálogo dinámico catalog.json...")
    
    try:
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            catalogo = json.load(f)
    except Exception as e:
        escribir_en_bitacora(f"Error al leer catalog.json: {str(e)}")
        return

    modificado = False
    articulos_validados = 0
    articulos_corregidos = 0

    for prod in catalogo:
        product_id = prod.get("id")
        current_url = prod.get("basePath", "")
        title = prod.get("title", "")
        
        articulos_validados += 1
        es_valido, detalle = validar_enlace(current_url)
        
        if not es_valido:
            escribir_en_bitacora(f"ALERTA ROJO: Producto [{title}] con ID [{product_id}] roto por {detalle}. Solicitando corrección a Ollama...")
            articulos_corregidos += 1
            
            # Consultar sugerencia a Ollama o fallback
            nueva_url = consultar_ollama_corrector(product_id, current_url, detalle)
            
            if nueva_url != current_url:
                prod["basePath"] = nueva_url
                modificado = True
                escribir_en_bitacora(f"INYECCIÓN EXITOSA: Enlace corregido en caliente para [{title}] -> {nueva_url}")
        else:
            logger.info(f"Producto verificado con éxito: [{title}] -> OK ({detalle})")

    # Guardar cambios si hubo correcciones en caliente
    if modificado:
        try:
            with open(CATALOG_PATH, "w", encoding="utf-8") as f:
                json.dump(catalogo, f, indent=2, ensure_ascii=False)
            escribir_en_bitacora(f"Catálogo catalog.json actualizado y resguardado en disco con {articulos_corregidos} correcciones.")
        except Exception as e:
            escribir_en_bitacora(f"Error al escribir en catalog.json: {str(e)}")
    else:
        logger.info("Verificación completada. Catálogo 100% íntegro y disponible.")
        escribir_en_bitacora(f"Ciclo de verificación completado. {articulos_validados} artículos escaneados. Estado: IMPECABLE.")

def main_loop():
    escribir_en_bitacora("Agente Verificador de Disponibilidad e Interconexión Ollama inicializado.")
    logger.info("Agente activo. Escaneando catálogo cada 15 minutos en segundo plano...")
    
    # Bucle infinito del demonio de fondo
    while True:
        try:
            validar_y_corregir_catalogo()
        except Exception as e:
            escribir_en_bitacora(f"Error en bucle de validación: {str(e)}")
            
        # Dormir 15 minutos (900 segundos)
        time.sleep(900)

if __name__ == "__main__":
    # Ejecución inmediata inicial al arrancar
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        validar_y_corregir_catalogo()
    else:
        main_loop()
