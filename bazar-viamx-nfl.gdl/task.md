# MAPA DE TRÁNSITO Y BITÁCORA MÁSTER DE OBRA - SWARM VIA MX 2026
## INFRAESTRUCTURA MIGRATORIA Y CONTROL EN LA ASUS FRANKENSTEIN

Este documento ha sido estructurado de forma forense para servir como el punto de ingesta instantáneo de alta fidelidad para el enjambre de agentes locales que heredarán este espacio de trabajo mediante **Claude Code** y **Ollama**. Contiene el mapa exacto de carpetas, variables blindadas, inventario de scripts y el checklist maestro de obra.

---

## 📂 1. MAPA DE ARQUITECTURA DE ARCHIVOS LOCALES

El chasis de software de **VíaMX** y el servicio **Mic Lock** están distribuidos de la siguiente forma en el disco duro local de la ASUS Frankenstein:

```text
d:\Downloads\Proyecto Web\
│
├── .env                              <-- VARIABLES PRIVADAS (BLINDADAS / Ignorado por Git)
├── .gitignore                        <-- ESCUDO DE VARIABLES PRIVADAS (.env bloqueado)
├── index.html                        <-- PORTAL PREMIUM (Tailwind, Lupa, Detalle y Geotargeting JS)
├── Abrir_VíaMX_Local.bat             <-- INICIADOR LOCAL (Servidor de Desarrollo y Chrome)
├── README.md                         <-- MANUAL DE BIENVENIDA (Manual de usuario, Git y Nube)
├── staticwebapp.config.json          <-- PROTOCOLO DE REDIRECCIÓN Y CACHÉ (Microsoft Azure SWA)
├── viamx_sandbox.html                <-- SANDBOX ESTÁTICO DE SEGURIDAD
├── arquitectura_extraccion_viamx.md  <-- PLANO DE INGESTA Y PARÁMETROS CONTABLES
├── log_operativo.txt                 <-- BITÁCORA HISTÓRICA Y TELEMETRÍA DE RED
├── task.md                           <-- ESTE MAPA DE TRÁNSITO Y LISTADO DE TAREAS (MÁSTER)
│
├── .github/
│   └── workflows/
│       └── deploy.yml                <-- PIPELINE CI/CD (Compilación y Hosting GitHub Pages)
│
├── docs/
│   ├── manual_integracion_apis.md    <-- MANUAL DE INTERCONEXIÓN (Liverpool, Sears, eBay, AliExpress)
│   └── data/
│       └── catalog.json              <-- BASE DE DATOS LOCAL DINÁMICA (12 productos directos)
│
├── images/
│   ├── hero_viamx_banner.jpg         <-- BANNER DE CABECERA PREMIUM (Harrods / Mundial 2026)
│   ├── watermark.jpg                 <-- MARCA DE AGUA CORPORATIVA (Guerrero Espartano y León)
│   └── watermark.png                 <-- MARCA DE AGUA CORPORATIVA SIN FONDO
│
├── mic_lock/                         <-- COMPONENTE ACÚSTICO NATIVO (Protección ASUS)
│   ├── MicVolumeLock.ps1             <-- Core Service (Loop de corrección activa de volumen)
│   ├── Install.ps1                   <-- Instalador Nativo (Acceso directo a Startup Windows)
│   ├── Status.ps1                    <-- Script de Diagnóstico en Caliente
│   ├── Uninstall.ps1                 <-- Desinstalador Limpio
│   └── config.json                   <-- Configuración del umbral del micrófono (88% -> 100%)
│
├── panic_flee.ps1                    <-- REPLICADOR ASÍNCRONO DE DEFENSA (Espejo a Suiza/Panamá)
├── cloudflare_config.ps1             <-- ENRUTADOR PERIMETRAL CLOUDFLARE (API Client v4)
├── pipeline_viamx_2026.py            <-- ENGINE DE INGESTA & LIVE HTTP REDIRECTOR GATEWAY (Port 8082)
└── agent_checker_ollama.py           <-- AGENTE DE FONDO OLLAMA (Validación continua cada 15 min)
```

---

## 🔑 2. DOCUMENTACIÓN DE VARIABLES BLINDADAS (`.env`)

El archivo `.env` se encuentra físicamente configurado en la ASUS Frankenstein, **fuera del repositorio Git público** mediante las exclusiones de `.gitignore`. Contiene las siguientes claves criptográficas críticas listas para la producción:

1. **Afiliación de AliExpress**: `ALIEXPRESS_API_KEY`, `ALIEXPRESS_SECRET`, `ALIEXPRESS_TRACKING_ID`.
2. **Awin API (Liverpool y Sears México)**: `AWIN_PUBLISHER_ID`, `AWIN_API_ACCESS_TOKEN`.
3. **eBay Partner Network**: `EBAY_CAMPAIGN_ID`, `EBAY_CUSTOM_ID`.
4. **Cloudflare Gateway**: `CLOUDFLARE_ZONE_ID`, `CLOUDFLARE_API_TOKEN`, `VIAMX_DOMAIN=viamx.pro`.
5. **Configuración Contable del SAT México**:
   - `SAT_RETENCION_ISR_FACTOR=0.01` (1% de retención).
   - `SAT_RETENCION_IVA_FACTOR=0.08` (8% de retención).
   - Utilizado por el widget del frontend para conciliar la ganancia neta en caliente.

---

## 🛠️ 3. INVENTARIO DE SCRIPTS CREADOS Y SUS FUNCIONES

### A. Scripts de Ejecución Local e Ingesta
* **`pipeline_viamx_2026.py` (Python 3)**:
  - **Función 1**: Engine de ingesta asíncrona que sanitiza enlaces, calcula descuentos y genera el contrato visual de `catalog.json`.
  - **Función 2**: **IP Geotargeting Engine**: Módulo `ViaMXGeotargeting` que mapea IPs remotas a países del comprador en milisegundos (usando `ip-api.com` y fallbacks deterministas).
  - **Función 3**: **Merchant Adaptor**: Traduce enlaces de Amazon MX a Amazon CA, Amazon AU o Amazon US preservando el ASIN y el tracking de afiliación. Convierte enlaces de Mercado Libre MX a equivalentes funcionales en Amazon US para compradores internacionales.
  - **Función 4**: **HTTP Redirector Gateway**: Levanta un servidor local en el puerto `8082` (`/redirect`) para enrutar tráfico dinámico, sembrar la cookie y evitar redirecciones a páginas vacías.
* **`agent_checker_ollama.py` (Python 3)**:
  - Agente de fondo perpetuo (ejecución cada 15 minutos). Realiza peticiones HEAD/GET a los 12 productos del catálogo.
  - Si detecta bloqueos geográficos o error 404, contacta con la IA de **Ollama local** (puerto `11434`, modelo `llama3`) para solicitar una URL de reemplazo en caliente y reescribir `catalog.json` sin apagar el portal.
* **`Abrir_VíaMX_Local.bat` (Windows Batch)**:
  - Arranca un servidor local HTTP en Python en el puerto `8080` para servir el portal y abre automáticamente Google Chrome. Si Python no está en el PATH, ejecuta un fallback visual directo a través de `file://`.

### B. Scripts de Infraestructura y Despliegue Perimetral
* **`panic_flee.ps1` (PowerShell)**:
  - Script de defensa y contingencia. Monitorea señales de falla en la ASUS Frankenstein. Si se activa la señal de pánico, realiza un espejo asíncrono y clonación de la carpeta `docs` a servidores alternativos seguros en Suiza y Panamá.
* **`cloudflare_config.ps1` (PowerShell)**:
  - Consume las credenciales del `.env` y realiza llamadas Patch a Cloudflare Client API v4 para habilitar Edge Caching Agresivo de 1 año y autominificación en caliente.
* **`mic_lock\Install.ps1` y `MicVolumeLock.ps1` (PowerShell)**:
  - Habilitan el loop persistente en la ASUS Frankenstein que monitorea el volumen del micrófono a nivel de registro, autocorrigiendo bajadas bruscas (lo restaura a 100%).

---

## 🖥️ 4. ESTADO DEL CHASIS VISUAL E TAREAS PENDIENTES

### Estado del Chasis Visual (`index.html`):
- **Estética de Lujo**: Colores verde Harrods (`#003e29`) combinados con oro mate (`#c5a059`), tipografías Playfair Display e Inter.
- **Marca de Agua Blindada**: El Guerrero Espartano y León se muestra con un 25% de opacidad de manera elegante en el banner superior Hero y flotando con efecto vidrio (glassmorphism) en la esquina inferior izquierda.
- **Lupa Premium de Zoom Activo**: Implementación nativa en JavaScript sin dependencias (escala 2.2x y transformOrigin centrado en el cursor).
- **Módulo de Geotargeting de Cliente**: Script asíncrono que detecta el país del visitante por IP. Si es internacional (CA, AU, US, PA, PR), reescribe las URLs y cambia dinámicamente las insignias (badges) de entrega y origen.
- **Simulador de Regiones Integrado**: Soporta el query parameter `?sim_country=XX` (ej. `?sim_country=AU` o `?sim_country=PA`) para probar instantáneamente la redirección en Google Chrome local.

### 📋 Checklist Maestro de Obra

- [x] **Fase 1: Inicialización e Infraestructura de Trabajo** (Completo)
- [x] **Fase 2: Ejecución del Servicio Nativo de Micrófono** (Instalado y validado en la Frankenstein)
- [x] **Fase 3: Refinamiento de la Interfaz Web** (Completada UI premium con estética Harrods)
- [x] **Fase 4: Catálogo VíaMX de 12 Productos Reales** (Inyectado con ASINs de Amazon y Mercado Libre)
- [x] **Fase 5: Chasis Gráfico y Marca de Agua** (Imágenes de Opal en images/ y watermark integrada)
- [x] **Fase 6: Preparación de Carpeta Limpia y Aislada** (Sincronizada en C:\Users\nflgd\.claude\ViaMX_Global_Publico)
- [x] **Fase 7: Despliegue de Expansión Visual, Acordeones y Soporte de Salud** (Ecosistema Clínico & Flyouts Iniciales)
- [x] **Fase 8: Directiva de Reconexión y Orquestación Multinicho (AntiGravity 2.0)**
  - [x] **Absorción del Manifiesto de Autonomía**: Asimilar y extraer principios de `C:\Users\nflgd\.claude\Claude.md` (Completado).
  - [x] **Expansión Universal de Enlaces de Asociados**: Enrutamiento universal adaptable (Reino Unido, Japón, Holanda, Alemania, Europa, Mongolia, Alaska) mapeando dinámicamente Amazon MX y Mercado Libre / Sears / Liverpool hacia equivalentes o búsquedas en Amazon local, eBay, AliExpress o Alibaba.
  - [x] **Refinamiento Clínico del Acompañamiento Digital**: Perfeccionar el bypass clínico de telemedicina por video con psiquiatra en español, optimizando el reproductor en pantalla de crisis.
  - [x] **Chasis y Efectos de Tarjeta "Vivos"**: Agregar hover visual micro-animado a textos de tarjetas de catálogo y elevación suave de tarjetas a escala 101%, con redirección segura en pestaña nueva por parámetro URL `?product_id=XXX`.
  - [x] **Menú Lateral con Solución de Acople**: Resolver el recorte de flyout causado por `overflow-y-auto` en el menú lateral y añadir micro-animaciones slide-in de 250ms en hover a departamentos (Línea Blanca, Electrónica, Cómputo, etc.).

  - [x] **Consistencia del Entorno Aislado**: Sincronizar todos los refinamientos entre el repositorio privado local de descargas `d:\Downloads\Proyecto Web` y la carpeta pública `C:\Users\nflgd\.claude\ViaMX_Global_Publico\index.html`.
  - [x] **Paginación de Catálogo (10 por página)**: Implementación de la paginación fluida y elegante en el frontend de VíaMX.
  - [x] **Corrección del Motor de Validación**: Reescritura del hot-confirmation check en `viamx_validator.py` para fusionar y validar el catálogo completo de manera segura.
