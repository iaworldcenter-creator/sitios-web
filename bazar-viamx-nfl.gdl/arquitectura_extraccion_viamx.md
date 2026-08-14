# Directiva de Extracción e Ingesta Internacional de Alta Frecuencia: ViaMX

Este documento establece las especificaciones técnicas y operativas para diversificar la oferta del portal ViaMX, garantizando la integración de plataformas globales y locales con un enfoque estricto en la veracidad del stock y la honestidad de la atribución comercial para el Mundial de Fútbol 2026.

---

## 1. Guía de Trámites y Papeleo para Diversificación de Plataformas

Para romper con el duopolio tradicional y ampliar el catálogo, la infraestructura de ViaMX debe conectarse a las siguientes redes de afiliación. A continuación, se detalla el procedimiento exacto de onboarding:

### A. AliExpress & Alibaba (Segmento Global de Conveniencia)
* **Plataforma de Afiliados:** AliExpress Portals (portals.aliexpress.com).
* **Proceso de Registro:**
  1. Crear una cuenta de desarrollador utilizando el correo corporativo de `@viamx.pro` (evitar correos genéricos).
  2. Completar el perfil declarando el tráfico de la V1 (enfocado en el nicho de aficionados mundialistas de México, EE. UU. y Canadá).
  3. **API Access (Papeleo Clave):** Solicitar la firma de la clave API en la consola de desarrolladores de AliExpress. Requiere firmar digitalmente el acuerdo de uso de marca para evitar la promoción de imitaciones prohibidas por las políticas de la FIFA.
* **Tasa de Comisión:** 3% - 9% según la categoría del producto. Pago mensual tras el periodo de retención de contracargos (30 días).

### B. eBay Partner Network - EPN (Segmento Coleccionables y Retro)
* **Plataforma de Afiliados:** partnernetwork.ebay.com.
* **Proceso de Registro:**
  1. Postularse declarando de forma explícita el uso de técnicas de recomendación contextual (como guías de "Álbum Panini" y "Jerseys Históricos de México").
  2. Verificar la propiedad del dominio a través de un registro TXT en la zona DNS de `viamx.pro`.
  3. Configurar la pasarela de pagos internacionales (cuenta bancaria mexicana o Payoneer con verificación fiscal RFC/W-8BEN).
  4. **API Access:** Integración con la eBay Browse API y Buy Marketing API para jalar ofertas de vendedores reputados con más del 98% de calificaciones positivas.

### C. Liverpool & Sears México (Segmento de Distribución Local Premium)
* **Plataforma de Afiliados:** Redes intermediarias agregadoras como Awin (awin.com) y Rakuten Advertising.
* **Proceso de Registro:**
  1. Postularse a la red matriz (Awin) realizando el depósito de seguridad de $1 USD para verificación KYC.
  2. Buscar de forma individual a los anunciantes "Liverpool MX" y "Sears México" dentro del directorio comercial.
  3. **Papeleo Fiscal Obligatorio (México):** Proporcionar la Constancia de Situación Fiscal (CSF) emitida por el SAT, firma electrónica (e.firma) y cuenta CLABE para retenciones correspondientes de ISR/IVA según el régimen fiscal del operador de ViaMX.
  4. **Políticas de Cumplimiento:** Prohibición absoluta de Brand Bidding (pujar por términos como "Sears rebajas" o "Liverpool mundial" en Google Ads).

---

## 2. Lógica de Purga de Inventario Agotado (Keep-Alive de Stock)

Para garantizar cero frustración al comprador y mantener un portal 100% veraz, ViaMX implementará un bucle de comprobación asíncrona de alta frecuencia en el servidor:

```
[Bucle de Comprobación] (Cada 15 minutos en productos calientes)
       │
       ├─► Consulta API (Amazon / Mercado Libre / AliExpress)
       │
       ├──► ¿Hay stock disponible en bodega México?
       │         │
       │         ├──► SÍ: Mantener visible y actualizar precio en ROJO (Oferta).
       │         │
       │         └──► NO: Desactivar visibilidad y disparar "Purga en Caliente".
       │
       └─► Reemplazo automático del espacio visual por un producto alternativo de la misma sede.
```

* **Protocolo de Purga:**
  1. Si la API del comerciante devuelve un parámetro `stock = 0`, el backend del sitio web debe despublicar la tarjeta del frontend en un rango máximo de 5 minutos.
  2. El sistema automáticamente rellenará el slot visual de diseño con el producto relacionado de mayor EPC disponible en su base de datos.

---

## 3. Filtro de Honestidad Comercial (Cero Ganchos de Spam)

Queda estrictamente prohibido el uso de técnicas invasivas de captación. En el caso de integrar artículos de plataformas como Temu, el pipeline de ViaMX aplicará las siguientes reglas de sanitización de datos:

* **Sanitización de URL Profunda:** Se purgarán todas las variables de redirección interna que forcen la descarga de la App móvil bajo promesas de obsequios falsos. El enlace de salida de ViaMX debe ser un enlace de redirección HTTP 307 directo hacia la pasarela de pago seguro (checkout) del producto real.
* **Clasificación Heurística de Confianza:** Si un producto tiene una tasa de devolución (chargeback rate) mayor al 8% o comentarios recurrentes de entrega no completada, el pipeline de seguridad lo colocará en la blocklist e impedirá su visualización, cuidando el prestigio de ViaMX.

---

## 4. Estructura Relacional del Modelo de Datos (JSON)

Para maximizar el tiempo de retención en la página y automatizar la sección "Quienes compraron esto también adquirieron...", cada producto inyectado al frontend por la API respetará la siguiente estructura relacional estricta:

```json
{
  "product_id": "viamx-2026-prod-001",
  "category": "TECNOLOGIA",
  "title": "Pantalla Smart TV 4K QLED (65\") - 120Hz",
  "description": "Vive el estadio en tu sala con una frecuencia ideal of 120Hz, óptimo para la inauguración en el Azteca.",
  "pricing": {
    "original_price": 18999.00,
    "current_price": 14999.00,
    "discount_percentage": 21,
    "currency": "MXN",
    "display_discount_in_red": true
  },
  "affiliate_link": "https://viamx.pro/redirect?target=amazon-65qled&tag=viamx-20",
  "stock_status": "IN_STOCK",
  "related_products": [
    {
      "product_id": "viamx-2026-prod-005",
      "title": "Barra de Sonido con Subwoofer (Dolby Atmos)",
      "current_price": 4500.00,
      "affiliate_link": "https://viamx.pro/redirect?target=amazon-soundbar"
    },
    {
      "product_id": "viamx-2026-prod-003",
      "title": "Power Bank de Alta Capacidad (20k mAh)",
      "current_price": 799.00,
      "affiliate_link": "https://viamx.pro/redirect?target=amazon-pbank"
    },
    {
      "product_id": "viamx-2026-prod-002",
      "title": "Parrilla de Carbón Portátil Plegable",
      "current_price": 1200.00,
      "affiliate_link": "https://viamx.pro/redirect?target=amazon-grill"
    },
    {
      "product_id": "viamx-2026-prod-008",
      "title": "Termo Acero Inoxidable (30oz+)",
      "current_price": 450.00,
      "affiliate_link": "https://viamx.pro/redirect?target=amazon-tumbler"
    }
  ]
}
```

---

## 5. Acoplamiento entre Backend (Python) y Frontend (HTML/JS)

El puente de integración automatizada del catálogo opera bajo el siguiente acoplamiento físico en la máquina local **ASUS Frankenstein**:

1. **Escritura Asíncrona (Python Engine):** El script `pipeline_viamx_2026.py` consume de forma concurrente las APIs externas sanitizadas, depura los productos agotados y escribe el inventario resultante en:
   `C:\Users\nflgd\.claude\ViaMX_Global_Publico\docs\data\catalog.json`
2. **Lectura Dinámica (Frontend HTML):** El archivo `index.html` (o `viamx_sandbox.html`) lee en tiempo real el archivo local mediante una petición `fetch()` asíncrona al cargar el DOM. Esto evita el uso de colecciones estáticas y desacopla la lógica visual del rascador de backend.

---

## 6. Guía de Prompts de Imágenes para Google Opal (Estética Premium Harrods)

Para garantizar un Look & Feel de categoría mundial (Elitismo de Harrods fusionado con Alta Conversión de Amazon), introduce los siguientes enunciados en **Google Opal** para generar los recursos visuales del portal. Guarda las descargas en la carpeta `C:\Users\nflgd\.claude\ViaMX_Global_Publico\images\`:

### A. Imagen Principal (Banner Hero de Bienvenida)
> **Prompt:** *Ultra-luxury wide banner for World Cup 2026 Mexico edition. Panoramic view of the iconic Estadio Azteca at twilight, integrated with a sophisticated emerald green and brushed gold gradient overlay. Minimalist, premium, futuristic sports event aesthetic, soft glow lighting, ultra-high-end graphic design, 8k resolution, cinematic atmosphere.*
* **Guardar como:** `hero_viamx_banner.jpg`

### B. Catálogo de Artículos (Foco en el Detalle y Lupa)

1. **Pantalla Smart TV QLED 65" 120Hz** (ID: `card_tv_65`)
   > **Prompt:** *Sleek and thin modern 65-inch borderless QLED TV mounted in a luxury dark-green and gold accented living room. The screen displays a highly detailed close-up action shot of a soccer ball hitting the net on turf under stadium floodlights. Hyper-realistic, professional architectural interior design photography, studio lighting.*
   * **Guardar como:** `prod_tv_65.jpg`

2. **Parrilla de Carbón Portátil Plegable** (ID: `card_parrilla_carbon`)
   > **Prompt:** *Premium portable folding stainless steel charcoal grill set on a perfectly manicured lawn. Gentle wisps of clean white smoke rising. Elegant steel finishes with warm sunset backlight, luxury backyard tailgating vibe, shallow depth of field.*
   * **Guardar como:** `prod_grill.jpg`

3. **Power Bank 20k mAh Carga Rápida** (ID: `card_power_bank_20`)
   > **Prompt:** *Minimalist matte-black aluminum heavy-duty power bank connected to a modern smartphone with a clean braided cable. Soft green LED charging indicator glowing. Placed on an elegant dark leather office desk tray, luxury tech flat lay photography.*
   * **Guardar como:** `prod_pbank.jpg`

4. **Caja de Sobres Panini Mundial 2026** (ID: `card_panini_box`)
   > **Prompt:** *Premium limited-edition collector box of football trading card packs for FIFA World Cup 2026. Vibrant metallic gold and deep green packaging graphics. Close-up shot showing glossy textures on a polished dark mahogany display table, soft studio product lighting.*
   * **Guardar como:** `prod_panini.jpg`

5. **Barra de Sonido Dolby Atmos** (ID: `card_soundbar`)
   > **Prompt:** *High-end minimalist black soundbar with a matching sleek side subwoofer sitting on a floating oak wood console. Mounted under a dark wall, elegant warm atmospheric lighting, luxury home theater product shot.*
   * **Guardar como:** `prod_soundbar.jpg`

6. **Freidora de Aire Digital Familiar** (ID: `card_freidora_aire`)
   > **Prompt:** *Modern digital air fryer in dark forest green with gold trim on a white marble kitchen countertop. Glowing touch screen interface. A ceramic plate with golden crispy chicken wings rests next to it. Cinematic warm kitchen photography.*
   * **Guardar como:** `prod_airfryer.jpg`

7. **Timbre Inteligente con Video HD** (ID: `card_timbre_video`)
   > **Prompt:** *Luxury smart video doorbell with a glowing circular blue LED light ring, securely mounted on a premium dark gray textured slate stone wall next to a modern dark wood entrance door. Architectural digest photography.*
   * **Guardar como:** `prod_doorbell.jpg`

8. **Termo de Acero Inoxidable Premium (30oz+)** (ID: `card_termo_premium`)
   > **Prompt:** *Luxury double-walled insulated stainless steel tumbler in emerald green color with a subtle golden logo. Tiny realistic condensation water droplets on the matte surface. Set on an outdoor stone steps under bright morning sunlight, hyper-detailed.*
   * **Guardar como:** `prod_tumbler.jpg`

9. **Silla de Oficina Ergonómica Premium** (ID: `card_silla_ergo`)
   > **Prompt:** *State-of-the-art ergonomic office chair featuring black high-tech breathable mesh and brushed gold-anodized alloy mechanical frames. Positioned in a modern luxury minimalist home studio with floor-to-ceiling glass windows.*
   * **Guardar como:** `prod_chair.jpg`

10. **Mochila de Hidratación CamelBak** (ID: `card_mochila_hidratacion`)
    > **Prompt:** *Professional athletic hydration backpack in deep pine green color with high-durability ripstop fabric textures. Resting on a mountain hiking trail with a panoramic summer landscape in the soft focus background.*
    * **Guardar como:** `prod_hydration_bag.jpg`

