# Manual de Integración de APIs Transnacionales: ViaMX Pro

Este documento establece las especificaciones de ingeniería de software, protocolos de autenticación, firmas criptográficas y esquemas de datos obligatorios para la interconexión de la plataforma ViaMX con las pasarelas de afiliados globales y locales en 2026.

---

## 1. AliExpress Portals & Alibaba API (Conexión Transnacional)

El acceso automatizado al inventario masivo de AliExpress se realiza mediante la Alibaba Cloud API Gateway. Para el Mundial de Fútbol 2026, la pasarela exige el firmado de peticiones por seguridad para evitar la inyección de tráfico robotizado.

### Protocolo de Firma Criptográfica (Signature Algorithm)

Cada petición HTTP POST enviada a la API de AliExpress debe incluir un parámetro `sign` calculado en base a una cadena ordenada alfabéticamente de todas las variables enviadas, concatenada con la clave secreta (`app_secret`).

La ecuación de generación de la firma en formato hexadecimal es:

$$\text{Signature} = \text{SHA256}(\text{app\_secret} + \text{SortedParameters} + \text{app\_secret})$$

### Parámetros de Consulta Obligatorios
* `app_key`: Clave pública de la aplicación en AliExpress Portals.
* `method`: Método de la API (`aliexpress.affiliate.featuredpromo.products.get`).
* `timestamp`: Fecha y hora actual en milisegundos UTC.
* `format`: Siempre `json`.
* `v`: Versión de la API (fijada en `2.0`).
* `sign_method`: Algoritmo de cifrado (fijado en `sha256`).

### Guardarraíl de Marca Registrada FIFA 2026
Para evitar la suspensión de la cuenta por el uso no autorizado de marcas registradas bajo la protección de la FIFA, el script de búsqueda del backend filtrará todas las consultas antes de enviarlas a AliExpress. Queda estrictamente prohibido utilizar en el parámetro `keywords` palabras como: "FIFA", "Mundial 2026", "World Cup", "Copa del Mundo".

El filtro de sanitización reemplazará de forma segura el payload por combinaciones genéricas autorizadas:

```json
{
  "query_filter": {
    "forbidden_patterns": ["FIFA", "World Cup", "Mundial 2026", "Copa del Mundo"],
    "allowed_alternatives": ["fútbol México", "jersey verde", "balón de fútbol", "sombrero charro"]
  }
}
```

### Formato de Consulta JSON Unificado (Request Payload)
Petición en tiempo real para jalar inventario de tecnología y accesorios hacia el Edge de ViaMX:

```json
{
  "aliexpress_affiliate_featuredpromo_products_get_request": {
    "fields": "product_id,product_title,product_detail_url,target_original_price,target_sale_price,product_main_image_url,evaluate_rate,stock_status",
    "promo_id": "viamx_mx_promo_2026",
    "category_id": "509",
    "keywords": "soccer jersey mexico",
    "page_size": 10,
    "page_no": 1,
    "target_currency": "MXN",
    "target_language": "ES",
    "ship_to_country": "MX"
  }
}
```

---

## 2. eBay Partner Network (EPN) API

El acceso a los coleccionables oficiales y artículos vintage para el mundial se realiza mediante la eBay Buy Browse API v1. Se configuran filtros avanzados de persistencia y exclusión de extracción de inteligencia artificial (IA).

### Sandbox de eBay y Exclusión de Modelado de Datos de IA
Para evitar que los modelos de lenguaje de terceros (crawlers) utilicen los datos estructurados en caché y la información de precios de ViaMX dentro del Sandbox y producción, se exige inyectar cabeceras HTTP específicas en cada transacción para asegurar que los servidores perimetrales de eBay apliquen directivas de exclusión de rastreo (scraping bypass) y respeten el aislamiento de los datos.

### Cabeceras HTTP Requeridas
* **Authorization:** Token de acceso del tipo Bearer generado dinámicamente: `Bearer ID_DE_ACCESO_OAUTH`.
* **Content-Type:** `application/json`.
* **X-EBAY-C-MARKETPLACE-ID:** `EBAY-MX` (Sede México para compras directas).
* **X-EBAY-C-ENDUSERCTX:** Metadatos del usuario final (`affiliateCampaignId=5566778899, affiliateReferenceId=viamxpro-20`).
* **X-EBAY-C-IA-EXCLUDE:** `true` (Directiva de cabecera customizada para forzar la exclusión del uso de la respuesta en conjuntos de datos de entrenamiento de modelos generativos).

### Filtros Avanzados (Compra Inmediata únicamente)
Para cumplir con la directiva de evitar subastas dinámicas que frustren al comprador por variaciones de precio por segundo, la consulta a la API de eBay filtrará estrictamente por la opción de compra inmediata utilizando el parámetro `buyingOptions:{FIXED_PRICE}`:

```http
GET https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?q=album+panini+mexico+2026&filter=buyingOptions:{FIXED_PRICE},deliveryCountry:MX,conditions:{NEW}&limit=10
```

---

## 3. Redes de Afiliación Local: Liverpool & Sears (Awin / Rakuten MX)

La monetización de las grandes cadenas comerciales con presencia en territorio nacional se unifica bajo el protocolo de la red Awin.

### Cabeceras de Autorización de Red Local
```http
Authorization: Bearer AWIN_API_TOKEN
Accept: application/json
```

### Llamadas Técnicas para Ofertas Relámpago (Flash Deals)
Para extraer el catálogo dinámico de ofertas del mundial, consumiremos el endpoint del Awin Advertiser Product Feed.

#### Endpoint de Extracción de Productos de Liverpool & Sears México
```http
GET https://api.awin.com/publishers/123456/productfeeds/download?apiKey=AWIN_API_TOKEN&advertiserId=11223&format=json&compression=zip&relation=sponsored
```

### Conciliación de Retenciones Fiscales (SAT México)
Para operar el flujo de comisiones de ViaMX conforme a las regulaciones de la Constancia de Situación Fiscal (CSF) en México, el motor contable del backend aplicará de forma automatizada las retenciones vigentes para plataformas tecnológicas.

De acuerdo con la legislación fiscal mexicana aplicable para los ingresos obtenidos por intermediación de terceros:
* **Retención de Impuesto sobre la Renta (ISR):** Se aplica el **1.0%** de retención directa sobre las ganancias brutas reportadas por el comerciante.
* **Retención de Impuesto al Valor Agregado (IVA):** Se aplica el **8.0%** de retención (que equivale al 50% de la tasa de IVA general del 16%).

El sistema calculará las comisiones netas de ViaMX utilizando la siguiente ecuación contable:

$$\text{Comisión Neta} = \text{Comisión Bruta} \times (1 - \text{Retención ISR} - \text{Retención IVA})$$

Sustituyendo los valores porcentuales regulados por el SAT en el año 2026:

$$\text{Comisión Neta} = \text{Comisión Bruta} \times (1 - 0.01 - 0.08) = \text{Comisión Bruta} \times 0.91$$

Esto garantiza que la interfaz de administración y el backend de ViaMX muestren con total transparencia el balance de la riqueza real neta que ingresará directamente tras impuestos.
