# 🌟 VíaMX - Selección de Lujo Mundial 2026

Bienvenido al repositorio central de **VíaMX (Selección de Lujo Mundial 2026)**, un portal web comercial de alto impacto con diseño premium "Harrods-Amazon Style", optimizado con Tailwind CSS, transacciones seguras de afiliación (S2S), widget financiero neto con deducción del SAT (1% ISR y 8% IVA) y Botón de Pánico para contingencias.

Este proyecto corre de forma ultrarrápida localmente en tu ASUS Frankenstein y está preparado para desplegarse síncronamente en los servidores de **Microsoft Azure** y **GitHub Pages** con un tiempo de carga (First Contentful Paint) menor a 150ms.

---

## 🚀 1. Ejecución en tu Entorno Local (ASUS Frankenstein)

Para correr la página web en tu máquina local de forma automatizada y sin configuraciones complejas, dispones del lanzador automático **`Abrir_VíaMX_Local.bat`** en la raíz del proyecto.

### Instrucciones:
1. **Doble clic** en [Abrir_VíaMX_Local.bat](file:///d:/Downloads/Proyecto%20Web/Abrir_V%C3%ADaMX_Local.bat).
2. El script detectará si tienes **Python** instalado:
   * **Con Python:** Iniciará un servidor HTTP local en `http://localhost:8080` y abrirá tu navegador por defecto automáticamente. Mantén la ventana de la consola abierta para navegar con soporte CORS completo para `docs/data/catalog.json`.
   * **Sin Python:** Abrirá la interfaz `index.html` directamente usando el protocolo seguro de archivos locales (`file:///`).

---

## 🌐 2. Despliegue en Servidores de GitHub (GitHub Pages)

Hemos configurado un flujo automático (CI/CD) para que tu página web se publique y actualice automáticamente cada vez que subas cambios.

### Paso 1: Subir el Proyecto a GitHub (Con GitHub Desktop)
Si prefieres no usar la línea de comandos:
1. Descarga e instala [GitHub Desktop](https://desktop.github.com/).
2. Abre la aplicación y selecciona **File > Add Local Repository...**
3. Elige la carpeta del proyecto: `C:\Users\nflgd\.claude\ViaMX_Global_Publico` y haz clic en **Add Repository**.
4. Te indicará que la carpeta no es un repositorio de Git activo. Haz clic en **Create a repository** y luego en **Create Repository**.
5. Escribe un resumen (ej. `Primer despliegue VíaMX`) en la esquina inferior izquierda y haz clic en **Commit to main**.
6. Haz clic en **Publish repository** en la parte superior derecha para crear el repositorio remoto privado o público en tu cuenta de GitHub.

### Paso 2: Activar GitHub Pages
Una vez subido el proyecto a tu cuenta de GitHub:
1. Entra a tu repositorio en la página de [GitHub](https://github.com).
2. Ve a la pestaña de ⚙️ **Settings** (Configuración) en la barra superior.
3. En el menú de la izquierda, haz clic en **Pages**.
4. En la sección *Build and deployment > Source*, selecciona **GitHub Actions**.
5. ¡Listo! El archivo automatizado `.github/workflows/deploy.yml` que hemos creado se encargará del resto. En un par de minutos, tu sitio web de lujo estará en vivo en `https://<tu-usuario>.github.io/<tu-repositorio>/`.

---

## ☁️ 3. Despliegue en Servidores de Microsoft (Azure Static Web Apps)

Azure Static Web Apps ofrece hosting premium ultraveloz y gratuito integrado con tu repositorio de GitHub.

### Instrucciones de Conexión:
1. Regístrate o inicia sesión en el [Portal de Azure](https://portal.azure.com/).
2. Busca y selecciona **Static Web Apps** (Aplicaciones web estáticas) y haz clic en **Crear**.
3. Configura los detalles básicos:
   * **Suscripción y Grupo de Recursos:** Selecciona los tuyos o crea uno nuevo.
   * **Nombre:** `viamx-luxury-2026`
   * **Plan de Hospedaje:** Gratis (Free F1).
4. En **Detalles de la implementación**, selecciona **GitHub** e inicia sesión con tu cuenta.
5. Selecciona tu Organización, Repositorio y la rama `main` o `master`.
6. En **Detalles de la compilación (Presets)**:
   * **Preajustes de compilación:** Selecciona **HTML** (o Personalizado).
   * **Ubicación de la aplicación:** `/` (Raíz).
   * **Ubicación de la API:** Deja en blanco.
   * **Ubicación del artefacto:** `/` (Raíz).
7. Haz clic en **Revisar y crear** y luego en **Crear**.
8. Azure inyectará un workflow a tu repositorio y publicará tu sitio web con un dominio personalizado en los servidores de Microsoft de forma instantánea. El archivo [staticwebapp.config.json](file:///d:/Downloads/Proyecto%20Web/staticwebapp.config.json) ya configurado en la raíz protegerá y optimizará los tiempos de respuesta.

---

## 🛠️ Arquitectura Técnica y Bitácora del Sistema

* **Estructura del Proyecto:**
  * `index.html`: Portal principal interactivo del portal.
  * `.github/workflows/deploy.yml`: Automatización de compilación y despliegue continuo en GitHub.
  * `staticwebapp.config.json`: Cabeceras de seguridad CSP, optimización de caché y prevención de redirección errónea en Azure.
  * `Abrir_VíaMX_Local.bat`: Lanzador de servidor web de alta velocidad.
  * `log_operativo.txt` / `task.md`: Bitácora continua e historial técnico.

---
*Desarrollado y optimizado por la Escudería Antigravity 2.0 en tu ASUS Frankenstein.*
