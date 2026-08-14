import os
import sys
import time
import subprocess
import webbrowser

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(WORKSPACE_DIR, "log_operativo.txt")

def escribir_en_bitacora(mensaje: str):
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n[{timestamp}] [HARVESTER_AGENT] {mensaje}")
    except Exception as e:
        print(f"No se pudo escribir en log_operativo.txt: {str(e)}")

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
        print(f"Package '{package}' is already installed.")
    except ImportError:
        print(f"Installing '{package}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def open_gema_and_type():
    # Target URL for the Gema (Gemini is the default target)
    gema_url = "https://gemini.google.com/gem/94ff47b7b34b/d78e0b88e1dba16a"
    
    escribir_en_bitacora(f"Abriendo explorador para visitar Gema en {gema_url}...")
    print(f"Abriendo explorador para visitar Gema en {gema_url}...")
    
    # Open the browser
    webbrowser.open(gema_url)
    
    # Wait for browser window to launch
    time.sleep(5)
    
    try:
        import pyautogui
        import pyperclip
        
        escribir_en_bitacora("Intentando escribir instrucción de búsqueda en la ventana de contexto...")
        
        # Focus search bar by pressing Tab or Ctrl+L then Tab
        # Copy instructions to clipboard
        instruccion = """INSTRUCCIONES DE BÚSQUEDA INVERSA PARA AFILIADOS VÍAMX:
1. **Comprobar Enlace de Compra Directo (Paso Inicial Obligatorio)**: Antes de proponer cualquier producto en tendencia para la temporada 2026, debes localizar y validar una URL real y directa de compra (PDP - Product Detail Page o pasarela de pago del proveedor) en tiendas oficiales de México (Liverpool, El Palacio de Hierro, Sears México, La Comer, Amazon México, Mercado Libre). Queda estrictamente prohibido usar URLs a páginas principales (homepages) o a listados de búsquedas generales. El enlace debe llevar directamente al artículo para que el cliente pueda pagar de inmediato sin tener que volver a buscarlo.
2. **Obtener Detalles y Descripción**: Solo si el enlace anterior es verificado y directo, procede a recopilar el título exacto, la descripción comercial detallada del producto y sus características de valor.
3. **Imágenes Reales del Producto**: Asocia la URL directa de la imagen oficial del producto ofrecido. Si no está disponible en la web oficial, debes girar instrucciones específicas en el campo 'instrucciones_imagen' indicando al usuario cómo generarla o buscarla usando Google Opal o Google Flow de forma óptima para la web.
4. **Formato de Salida**: Genera únicamente un arreglo JSON de 30 productos con la siguiente estructura exacta:
   - id: correlativo único (rango sugerido: LUX-2026-061 a LUX-2026-090)
   - source: nombre de la tienda oficial (Amazon México, Mercado Libre, Liverpool, Sears México, El Palacio de Hierro, La Comer)
   - title: nombre comercial exacto del artículo
   - category: categoría del portal (e.g. Perfumería Fina, Gadgets de Vanguardia, Calzado Premium, Moda Exclusiva, Bienestar y Cuidado Personal, Accesorios de Viaje)
   - subcategory: subcategoría
   - price: precio actual en MXN (número)
   - originalPrice: precio de lista anterior (número)
   - directUrl: URL directa de compra/checkout del producto en la tienda oficial (e.g. https://www.amazon.com.mx/dp/... o https://www.liverpool.com.mx/tienda/pdp/...)
   - image: URL de la imagen del producto
   - instrucciones_imagen: (opcional) instrucciones de generación en Google Flow/Opal si no hay imagen real disponible
   - viral_platform: plataforma donde es tendencia (TikTok, Instagram, YouTube)"""
        pyperclip.copy(instruccion)
        
        # Give a small window focus delay
        time.sleep(2)
        
        # Paste the instruction in the browser window
        # Press Tab multiple times to focus the text area or use Ctrl+V assuming focus is in search bar
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        
        escribir_en_bitacora("Instrucción enviada a la ventana de contexto de la Gema.")
        print("Instrucción enviada con éxito.")
    except Exception as e:
        escribir_en_bitacora(f"No se pudo automatizar el teclado (detalles: {str(e)}). La URL se abrió correctamente para interacción manual.")
        print(f"La URL se abrió correctamente, pero la automatización del teclado falló: {str(e)}")

if __name__ == "__main__":
    # Ensure pyautogui and pyperclip are installed
    try:
        install_and_import("pyautogui")
        install_and_import("pyperclip")
    except Exception as e:
        print(f"Advertencia: No se pudieron instalar dependencias de automatización de interfaz ({str(e)}).")

    open_gema_and_type()
