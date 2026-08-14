# 🧠 CAJA NEGRA DE MEMORIA - ECOSISTEMA DIVERSIFICADO VÍAMX 2026
## REGISTRO DE MEMORIA DE LARGO ALCANCE (MEMORY.md)

Este documento es el bloque de memoria de alta densidad del ecosistema **VíaMX**. Ha sido diseñado bajo el **Principio Seis** del *Manifiesto de Principios Dinámicos* para erradicar la parálisis por análisis y transferir de forma instantánea todo el contexto técnico, lógico y estructural a cualquier agente del enjambre (como Claude Code u Ollama) que herede la ASUS Frankenstein.

---

## 🛠️ 1. INFRAESTRUCTURA Y CRÓNICA TÉCNICA DEL CHASIS

El portal VíaMX es una vitrina e-commerce premium de alta velocidad. Su arquitectura combina un chasis visual elegante con motores de ingesta, auditoría en caliente y redirección dinámica transnacional.

### A. Chasis Visual e Interacciones Premium (`index.html`)
* **Paleta de Colores**: Estilo Harrods británico (Verde `#003e29`, Dorado `#c5a059`) fusionado con la agresividad comercial y psicología de precios de Amazon (porcentaje de descuento e indicador de oferta en rojo gigante `#cc0c39`).
* **Lupa Interactiva (Magnifying Hover Zoom)**: Implementación de alto rendimiento en JS puro. Amplifica la zona de la imagen principal a un 2.2x, cambiando la posición del cursor de manera proporcional en milisegundos (`transformOrigin` dinámico en hover, y retorno a escala original al salir).
* **Visor Avanzado**: Carrusel de miniaturas asociadas. Pasar el puntero cambia la imagen activa, doble clic la fija permanentemente en la tarjeta de detalle.
* **Marca de Agua Corporativa**: Imagen con opacidad del 25% del Guerrero Espartano y León, colocada en el hero banner superior y flotando sobre un recuadro de vidrio en la esquina inferior izquierda.

---

## 🗺️ 2. MOTOR DE GEOTARGETING E INYECCIÓN DE AFILIADOS

### A. Geotargeting en Frontend (`index.html`)
* **Propósito**: Resolver el "Misterio del enlace inexistente". Evita que los visitantes fuera de México se topen con errores de disponibilidad regional al hacer clic en enlaces de Amazon México o Mercado Libre.
* **Detección IP**: Realiza una consulta asíncrona no bloqueante a `https://ipapi.co/json/`.
* **Reescritura en Caliente**:
  - Si el país es **Canadá (CA)** -> Mapea URLs a `amazon.ca/dp/ASIN`.
  - Si el país es **Australia (AU)** -> Mapea URLs a `amazon.com.au/dp/ASIN`.
  - Si es **Panamá, Puerto Rico, EE. UU. o internacional** -> Mapea URLs a `amazon.com` (Amazon US con envíos directos).
  - Si es **México (MX)** -> Mantiene `amazon.com.mx/dp/ASIN`.
* **Mapeo para Mercado Libre**: Mercado Libre MX restringe compras a residentes mexicanos. Si un usuario internacional ingresa, el JS intercepta el ID del producto y lo reescribe automáticamente a su equivalente exacto en Amazon US (ej. bocina Bose, termo Yeti, asador de maletín) o a una búsqueda directa optimizada en Amazon US, inyectando siempre tu tag `viamx2026-20`.
* **Simulador de Región**: Permite forzar la geolocalización agregando el parámetro **`?sim_country=XX`** a la URL (ej. `?sim_country=AU` para simular Australia, `?sim_country=PA` para Panamá).

### B. Gateway Redirector en Backend (`pipeline_viamx_2026.py`)
* Levanta un servidor asíncrono local HTTP en el puerto **`8082`** (`/redirect`).
* Cuando un rotador de enlaces o webhook de tendencias externa le envía tráfico, el gateway lee la IP remota del cliente, calcula el Geotargeting en el backend y devuelve una redirección `307` limpia hacia la pasarela adaptada del comerciante internacional con el tag sembrado.

---

## 🤖 3. AGENTE DE INGESTA E INTELIGENCIA LOCAL (OLLAMA)

### A. Monitoreo Silencioso (`agent_checker_ollama.py`)
* Demonio que corre de forma perpetua cada 15 minutos en segundo plano.
* Escanea mediante peticiones HEAD/GET optimizadas el estado de los 12 productos mundiales en `catalog.json`.
* **Interconexión Ollama (Port 11434)**: Si un enlace devuelve error 404, caída de stock o bloqueo por región, se comunica de forma asíncrona con el modelo `llama3` local de la ASUS Frankenstein para recibir una sugerencia de URL alternativa de reemplazo.
* **Fallback Determinista**: Si Ollama se encuentra inactivo, el script aplica una base de datos local unificada de URLs secundarias verificadas para que el catálogo jamás muestre enlaces rotos.

---

## 🚀 4. BLUEPRINT DE EXPANSIÓN MULTINICHO DINÁMICA

La arquitectura de VíaMX ha sido diseñada como un marco líquido, permitiendo la inyección de nuevos mercados de alta facturación de manera inmediata:

### A. Ecosistema de Acompañamiento Digital (Salud Mental y Soporte Emocional)
* **Idioma**: Flujo clínico automatizado e interactivo estrictamente en español.
* **Fases del Embudo Comercial**:
  1. **Diagnóstico Interactivo**: Cuestionario dinámico inicial evaluando causas de crisis del consultante (procesos de divorcio, duelo familiar, desempleo repentino, disputas domésticas, enfermedades).
  2. **Estrategia de Conversión**: Ofrece la primera consulta evaluativa/informativa con un **50% de descuento**, empaquetando el tratamiento posterior en módulos recurrentes de **3, 5 u 8 sesiones**.
  3. **Protocolo de Enlace Clínico de Emergencia (Bypass en Milisegundos)**:
     - Si el test de salud detecta respuestas indicadoras de un trastorno neurodivergente severo (bipolaridad, ideación autolítica) y el usuario confirma la ausencia de su medicación psiquiátrica prescrita:
     - **Acción:** El sistema omite de inmediato el carrito comercial o pasarela de pago.
     - **Telemedicina Activa:** Abre al instante un puente de comunicación por videoconferencia en vivo con el psiquiatra o psicólogo clínico asociado de guardia más apto para contención de crisis, mitigando riesgos existenciales de forma oportuna.

### B. Cuidado Especializado y Logística para Mascotas de Cualquier Especie
* Diversificación comercial abarcando productos de nutrición, hábitats artificiales y logística de seguridad para animales exóticos o domésticos (desde perros y gatos domésticos hasta mambas negras e hipopótamos), enlazando a pasarelas mundiales específicas.

### C. Belleza, Cuidado de la Piel e Importaciones Globales
* Expansión modular para catálogos de alta rotación (maquillaje orgánico, tratamientos premium de skincare) integrando enlaces de afiliados a marcas coreanas, europeas o japonesas.

---

## 🔒 5. BLINDAJE DE FIERROS Y SEGURIDAD SAT
* **Aislamiento Criptográfico**: El archivo `.env` aloja las claves de AliExpress Portals, Awin (Sears y Liverpool), eBay Network, tokens de Cloudflare y porcentajes contables del SAT (1% ISR y 8% IVA).
* **Escudo Git**: Bloqueado mediante `.gitignore`. Jamás debe subirse al servidor de Microsoft o GitHub.
* **Seguridad Visual**: El botón de pánico en el frontend enmascara las comisiones y purga las cookies del navegador al instante en caso de auditorías externas.
