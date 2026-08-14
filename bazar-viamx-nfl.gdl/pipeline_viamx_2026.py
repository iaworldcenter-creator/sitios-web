#!/usr/bin/env python3
"""
Módulo de Software: Engine de Extracción, Sanitización y Geotargeting de Enlaces ViaMX.
Diseñado para la ingesta asíncrona de alta frecuencia y redirección transnacional inteligente.
Habilitado para resolver bloqueos regionales en Veracruz, Panamá, Canadá, Australia y el mundo.
"""

import asyncio
import logging
import urllib.parse
import urllib.request
import re
import json
import sys
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Configuración básica de telemetría y logging de ViaMX
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ViaMX_Engine")

# ==========================================
# 1. Esquemas de Datos Robustos (Contratos)
# ==========================================

class ProductoRelacionado(BaseModel):
    product_id: str
    title: str
    current_price: float
    affiliate_link: str

class PricingModel(BaseModel):
    original_price: float
    current_price: float
    discount_percentage: int
    currency: str = "MXN"
    display_discount_in_red: bool = True

class ProductoSanitizado(BaseModel):
    product_id: str
    platform_source: str
    category: str
    title: str
    description: str
    pricing: PricingModel
    clean_affiliate_link: str
    stock_status: str = "IN_STOCK"
    related_products: List[ProductoRelacionado] = Field(default_factory=list)

# ==========================================
# 2. Módulo de Geotargeting e Inyección Transnacional
# ==========================================

class ViaMXGeotargeting:
    """
    Motor reactivo encargado de geolocalizar la IP del comprador en milisegundos
    y reescribir dinámicamente los enlaces de Amazon/Meli para evitar bloqueos regionales.
    """
    
    # Equivalencias de Mercado Libre MX hacia Amazon US/Búsquedas para visitantes fuera de México
    # Evita que un comprador de Panamá, Canadá o Australia vea un error 404 en Mercado Libre México.
    MELI_INTERNATIONAL_EQUIVALENTS = {
        "card_adidas_ball": "https://www.amazon.com/dp/B09B2L4HHL",  # Balón Adidas Al Rihla League
        "card_oster_airfryer": "https://www.amazon.com/dp/B08B1F54DF",  # Freidora digital Oster
        "card_ring_doorbell": "https://www.amazon.com/dp/B08CKYXL5B",  # Ring Doorbell Wired
        "card_silla_ergo": "https://www.amazon.com/s?k=Ergonomic+Office+Chair+Lumbar+Support+Mesh",
        "card_power_bank_10": "https://www.amazon.com/dp/B07S829LBX",  # Anker Power Bank compact
        "card_portable_grill": "https://www.amazon.com/s?k=Portable+Charcoal+Grill+Foldable+Suitcase"
    }

    @staticmethod
    def obtener_pais_por_ip(ip_address: str) -> str:
        """
        Consulta rápida no bloqueante a una API de Geo-IP pública con timeout estricto.
        Si falla o es IP privada, aplica fallback al mercado principal (MX).
        """
        # Filtrar IPs locales o de pruebas
        if not ip_address or ip_address in ["127.0.0.1", "localhost", "::1"] or ip_address.startswith("192.168.") or ip_address.startswith("10."):
            logger.info(f"Detección Geo-IP: IP local/privada '{ip_address}'. Retornando fallback 'MX'.")
            return "MX"
            
        try:
            # Query asíncrona simulada o llamada directa sincrónica rápida con timeout de 200ms
            url = f"http://ip-api.com/json/{ip_address}?fields=status,countryCode"
            req = urllib.request.Request(url, headers={'User-Agent': 'ViaMX-GeoEngine/2026'})
            with urllib.request.urlopen(req, timeout=0.25) as response:
                data = json.loads(response.read().decode())
                if data.get("status") == "success":
                    country_code = data.get("countryCode", "MX")
                    logger.info(f"Detección Geo-IP: IP '{ip_address}' geolocalizada en '{country_code}'.")
                    return country_code
        except Exception as e:
            logger.warning(f"Detección Geo-IP: Error al consultar API de geolocalización ({str(e)}). Fallback a 'MX'.")
            
        return "MX"

    @classmethod
    def reescribir_enlace_internacional(cls, url_base: str, country_code: str, tracking_id: str, product_id: Optional[str] = None) -> str:
        """
        Reescribe dinámicamente un enlace regional de Amazon o Mercado Libre según el país origen del usuario
        para evitar que se rompa y sembrar correctamente la cookie de comisión.
        """
        country_code = country_code.upper()
        
        # 1. CASO AMAZON: Extraer ASIN y cambiar de storefront local a internacional
        if "amazon." in url_base:
            # Extraer ASIN (código de 10 caracteres alfanuméricos)
            asin_match = re.search(r'/dp/([A-Z0-9]{10})', url_base) or re.search(r'/gp/product/([A-Z0-9]{10})', url_base)
            if asin_match:
                asin = asin_match.group(1)
                
                # Mapear país del visitante a su storefront de Amazon local o más conveniente
                if country_code == "MX":
                    target_domain = "amazon.com.mx"
                elif country_code == "CA":
                    target_domain = "amazon.ca"
                elif country_code == "AU":
                    target_domain = "amazon.com.au"
                else:
                    # US, Panamá, Puerto Rico, Costa Rica, Europa Occidental, etc.
                    # Amazon.com (US) ofrece envíos globales directos y mayor compatibilidad
                    target_domain = "amazon.com"
                    
                # Reconstruir URL con ASIN preservado y tag de afiliación integrado
                clean_url = f"https://www.{target_domain}/dp/{asin}?tag={tracking_id}"
                logger.info(f"Geotargeting Amazon: {url_base} -> Redirigido a {clean_url} [País: {country_code}]")
                return clean_url
            
        # 2. CASO MERCADO LIBRE: Redirigir internacionalmente a equivalentes en Amazon US
        elif "mercadolibre.com" in url_base:
            if country_code != "MX":
                # Si el usuario es internacional, Mercado Libre MX le dará error de disponibilidad.
                # Redirigimos al equivalente verificado de Amazon US.
                equiv_url = cls.MELI_INTERNATIONAL_EQUIVALENTS.get(product_id or "")
                if equiv_url:
                    # Inyectar el tag comisionable de Amazon a la URL equivalente
                    separator = "&" if "?" in equiv_url else "?"
                    clean_url = f"{equiv_url}{separator}tag={tracking_id}"
                    logger.info(f"Geotargeting Meli: {url_base} -> Redirigido a Equivalente Amazon {clean_url} [País: {country_code}]")
                    return clean_url
                else:
                    # Búsqueda general en Amazon US con el título del producto
                    search_term = urllib.parse.quote_plus("soccer ball premium" if "ball" in url_base else "home appliances")
                    clean_url = f"https://www.amazon.com/s?k={search_term}&tag={tracking_id}"
                    logger.info(f"Geotargeting Meli: Fallback a búsqueda Amazon {clean_url} [País: {country_code}]")
                    return clean_url
                    
        # Retornar URL original si no es Amazon o Mercado Libre, o si es local MX
        separator = "&" if "?" in url_base else "?"
        if "tag=" not in url_base and "utm_source" not in url_base:
            if "mercadolibre." in url_base:
                return f"{url_base}{separator}utm_source=affiliate&utm_medium={tracking_id}"
            return f"{url_base}{separator}tag={tracking_id}"
        return url_base

# ==========================================
# 3. Motor Core: Sanitizador y Filtrador
# ==========================================

class ViaMXSanitizer:
    @staticmethod
    def sanitizar_enlace(url_sucia: str, tracking_id: str, plataforma: str) -> str:
        """
        Limpia enlaces de ganchos fraudulentos y prepara el redireccionador perimetral de VíaMX.
        """
        parsed_url = urllib.parse.urlparse(url_sucia)
        
        if "temu.com" in parsed_url.netloc:
            query_params = urllib.parse.parse_qs(parsed_url.query)
            clean_params = {}
            if "goods_id" in query_params:
                clean_params["goods_id"] = query_params["goods_id"][0]
            clean_query = urllib.parse.urlencode(clean_params)
            url_limpia = urllib.parse.urlunparse(("https", "www.temu.com", "/checkout_direct.html", "", clean_query, ""))
            return f"https://viamx.pro/redirect?target={urllib.parse.quote_plus(url_limpia)}&tag={tracking_id}"
            
        elif "aliexpress.com" in parsed_url.netloc:
            product_id = parsed_url.path.split("/")[-1]
            url_limpia = f"https://www.aliexpress.com/item/{product_id}"
            return f"https://viamx.pro/redirect?target={urllib.parse.quote_plus(url_limpia)}&tag={tracking_id}&platform=aliexpress"
            
        else:
            # Enrutamiento controlado estándar
            return f"https://viamx.pro/redirect?target={urllib.parse.quote_plus(url_sucia)}&tag={tracking_id}&platform={plataforma}"

# ==========================================
# 4. Pipeline de Extracción de Alta Frecuencia
# ==========================================

class ViaMXPipeline:
    def __init__(self, tracking_id: str):
        self.tracking_id = tracking_id
        self.sanitizer = ViaMXSanitizer()

    async def consultar_bodega_stock(self, product_id: str, source: str) -> bool:
        await asyncio.sleep(0.01)
        if product_id in ["viamx-2026-prod-099", "viamx-2026-prod-empty"]:
            return False
        return True

    async def procesar_ingesta_producto(self, raw_data: Dict) -> Optional[ProductoSanitizado]:
        product_id = raw_data.get("id", "generico")
        platform = raw_data.get("platform", "desconocido")
        
        tiene_stock = await self.consultar_bodega_stock(product_id, platform)
        if not tiene_stock:
            logger.warning(f"Purga en Caliente: Producto '{product_id}' sin stock en {platform}. Removido.")
            return None

        link_sanitizado = self.sanitizer.sanitizar_enlace(
            raw_data.get("url_sucia", ""),
            self.tracking_id,
            platform
        )

        original = raw_data.get("original_price", 0.0)
        current = raw_data.get("current_price", 0.0)
        descuento = int(((original - current) / original) * 100) if original > 0 else 0

        producto = ProductoSanitizado(
            product_id=product_id,
            platform_source=platform,
            category=raw_data.get("category", "OTROS"),
            title=raw_data.get("title", "Producto ViaMX"),
            description=raw_data.get("description", ""),
            pricing=PricingModel(
                original_price=original,
                current_price=current,
                discount_percentage=descuento,
                display_discount_in_red=(descuento > 10)
            ),
            clean_affiliate_link=link_sanitizado,
            related_products=raw_data.get("related_raw_payload", [])
        )

        return producto

# ==========================================
# 5. Microservicio HTTP Gateway de Redirección (Localhost 8082)
# ==========================================

class ViaMXRedirectHandler(BaseHTTPRequestHandler):
    """
    Servidor de redirección rápida asíncrono para enrutamiento local y control de S2S.
    Detecta la IP remota del comprador, calcula el Geotargeting y redirige al instante.
    """
    def log_message(self, format, *args):
        # Desactivar logs por defecto de http.server en consola para no ensuciar la salida
        return

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == "/redirect":
            query_params = urllib.parse.parse_qs(parsed_path.query)
            target_url = query_params.get("target", [""])[0]
            tracking_id = query_params.get("tag", ["viamx2026-20"])[0]
            product_id = query_params.get("product_id", [""])[0]
            
            if not target_url:
                self.send_response(400)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write("Error 400: Parámetro 'target' requerido.".encode("utf-8"))
                return
                
            # Obtener IP del cliente (si hay balanceador Cloudflare, lee CF-Connecting-IP)
            client_ip = self.headers.get("CF-Connecting-IP") or self.headers.get("X-Forwarded-For") or self.client_address[0]
            if "," in client_ip:
                client_ip = client_ip.split(",")[0].strip()
                
            # Detectar país de procedencia de la IP
            country = ViaMXGeotargeting.obtener_pais_por_ip(client_ip)
            
            # Adaptar enlace dinámicamente con Geotargeting
            final_redirect_url = ViaMXGeotargeting.reescribir_enlace_internacional(
                url_base=target_url,
                country_code=country,
                tracking_id=tracking_id,
                product_id=product_id
            )
            
            logger.info(f"GATEWAY REDIRECT: Cliente IP [{client_ip}] ({country}) -> {final_redirect_url}")
            
            # Responder con redirección temporal 307
            self.send_response(307)
            self.send_header("Location", final_redirect_url)
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("VíaMX Redirector Gateway - 404 No Encontrado".encode("utf-8"))

def iniciar_servidor_gateway(puerto=8082):
    """Arranque del servidor gateway local en un hilo en segundo plano"""
    server_address = ('', puerto)
    httpd = HTTPServer(server_address, ViaMXRedirectHandler)
    logger.info(f"GATEWAY INICIADO: Escuchando redirecciones en http://localhost:{puerto}/redirect")
    
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    return httpd

# ==========================================
# 6. Demostración y Puesta en Marcha
# ==========================================

async def main():
    # Levantar el servidor gateway dinámico en segundo plano
    httpd = iniciar_servidor_gateway(puerto=8082)
    
    # Simulación de Ingesta y Sanitización
    pipeline = ViaMXPipeline(tracking_id="viamx2026-20")
    
    raw_products = [
        {
            "id": "card_tv_65",
            "platform": "amazon",
            "category": "Tecnología",
            "title": "Pantalla Hisense 65\" 4K QLED 120Hz (65U7N)",
            "original_price": 18999.00,
            "current_price": 14999.00,
            "url_sucia": "https://www.amazon.com.mx/dp/B0D1898VNW",
        },
        {
            "id": "card_adidas_ball",
            "platform": "mercadolibre",
            "category": "Coleccionables",
            "title": "Balón Adidas Oficial de Entrenamiento",
            "original_price": 999.00,
            "current_price": 799.00,
            "url_sucia": "https://www.mercadolibre.com.mx/balon-de-futbol-adidas-al-rihla-league/p/MLM19024090",
        }
    ]

    logger.info("Procesando payloads del catálogo local de VíaMX Pro...")
    tareas = [pipeline.procesar_ingesta_producto(prod) for prod in raw_products]
    resultados = await asyncio.gather(*tareas)
    productos_finales = [res for res in resultados if res is not None]

    print("\n--- INVENTARIO RESULTANTE SANITIZADO ---")
    for prod in productos_finales:
        print(prod.model_dump_json(indent=2))
        print("-" * 50)
        
    print("\n--- EJEMPLOS DE REDIRECCIÓN Y GEOTARGETING EN CALIENTE ---")
    # Prueba 1: Comprador de Canadá accediendo a la TV de Amazon México
    print("Simulación Canadá -> Amazon MX:")
    url_ca = ViaMXGeotargeting.reescribir_enlace_internacional(
        "https://www.amazon.com.mx/dp/B0D1898VNW", "CA", "viamx2026-20"
    )
    print(f"Resultado: {url_ca}\n")
    
    # Prueba 2: Comprador de Panamá accediendo a Balón Adidas de Mercado Libre México
    print("Simulación Panamá -> Mercado Libre MX:")
    url_pa = ViaMXGeotargeting.reescribir_enlace_internacional(
        "https://www.mercadolibre.com.mx/balon-de-futbol-adidas-al-rihla-league/p/MLM19024090", "PA", "viamx2026-20", "card_adidas_ball"
    )
    print(f"Resultado: {url_pa}\n")

    print("[INFO] El Gateway local se mantendrá en ejecución en segundo plano.")
    print("Para probar la redirección con Geotargeting real abre en tu navegador:")
    print("http://localhost:8082/redirect?target=https%3A%2F%2Fwww.amazon.com.mx%2Fdp%2FB0D1898VNW&tag=viamx2026-20")
    print("-" * 75)

    # Dejar el hilo principal corriendo brevemente para poder probar peticiones si es necesario
    await asyncio.sleep(5.0)

if __name__ == "__main__":
    asyncio.run(main())
