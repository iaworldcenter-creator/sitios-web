import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
VIAMX_DIR = os.path.join(BASE_DIR, "bazar-viamx-nfl.gdl")

if not os.path.exists(VIAMX_DIR):
    alt = os.path.join(BASE_DIR, "bazar-viamx-NFL.GDL")
    if os.path.exists(alt):
        VIAMX_DIR = alt

INDEX_PATH = os.path.join(VIAMX_DIR, "index.html")

if not os.path.exists(INDEX_PATH):
    print(f"[Error] No se encontró {INDEX_PATH}")
    exit(1)

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

print("=" * 70)
print("EXPANDIENDO IMÁGENES AL 100% DE ANCHO (EDGE-TO-EDGE) EN VÍA MX")
print("=" * 70)

NUEVO_SLIDER_FULL_WIDTH = """
    <!-- ========================================================================
         HERO SLIDER SECTION (COBERTURA TOTAL DE PANTALLA: IZQUIERDA A DERECHA)
         ======================================================================== -->
    <div id="hero-slider-container" style="position: relative; width: 100%; height: 560px; max-height: 65vh; overflow: hidden; background-color: #020617; border-bottom: 1px solid #1e293b; user-select: none;">
        <div id="hero-slider" style="position: relative; width: 100%; height: 100%;">
            <!-- Slide 1 -->
            <div class="hero-slide active" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 1; z-index: 10; transition: opacity 2000ms ease-in-out;">
                <img src="assets/img/carucel (1).jpeg" alt="Familia Tigre 1" style="width: 100%; height: 100%; object-fit: fill; display: block;" />
            </div>
            <!-- Slide 2 -->
            <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 2000ms ease-in-out;">
                <img src="assets/img/carucel (2).jpeg" alt="Familia Tigre 2" style="width: 100%; height: 100%; object-fit: fill; display: block;" />
            </div>
            <!-- Slide 3 -->
            <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 2000ms ease-in-out;">
                <img src="assets/img/carucel (3).jpeg" alt="Familia Tigre 3" style="width: 100%; height: 100%; object-fit: fill; display: block;" />
            </div>
            <!-- Slide 4 -->
            <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 2000ms ease-in-out;">
                <img src="assets/img/carucel (4).jpeg" alt="Familia Tigre 4" style="width: 100%; height: 100%; object-fit: fill; display: block;" />
            </div>
            <!-- Slide 5 -->
            <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 2000ms ease-in-out;">
                <img src="assets/img/carucel (5).jpeg" alt="Familia Tigre 5" style="width: 100%; height: 100%; object-fit: fill; display: block;" />
            </div>
        </div>

        <!-- Controles Izquierda / Derecha -->
        <button type="button" aria-label="Anterior" onclick="prevSlide()" style="position: absolute; left: 24px; top: 50%; transform: translateY(-50%); z-index: 20; width: 48px; height: 48px; border-radius: 9999px; background-color: rgba(2, 6, 23, 0.75); color: #ffffff; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 10px 25px rgba(0,0,0,0.5); backdrop-filter: blur(8px); transition: all 0.3s;">
            <i class="fa-solid fa-chevron-left" style="font-size: 18px;"></i>
        </button>
        <button type="button" aria-label="Siguiente" onclick="nextSlide()" style="position: absolute; right: 24px; top: 50%; transform: translateY(-50%); z-index: 20; width: 48px; height: 48px; border-radius: 9999px; background-color: rgba(2, 6, 23, 0.75); color: #ffffff; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 10px 25px rgba(0,0,0,0.5); backdrop-filter: blur(8px); transition: all 0.3s;">
            <i class="fa-solid fa-chevron-right" style="font-size: 18px;"></i>
        </button>

        <!-- Indicadores Inferiores (5 Dots) -->
        <div style="position: absolute; bottom: 20px; left: 0; right: 0; z-index: 20; display: flex; justify-content: center; align-items: center; gap: 10px;">
            <button type="button" aria-label="Foto 1" class="hero-dot" onclick="goToSlide(0)" style="width: 32px; height: 10px; border-radius: 9999px; background-color: #22d3ee; border: none; cursor: pointer; transition: all 0.4s; box-shadow: 0 0 10px rgba(34,211,238,0.6);"></button>
            <button type="button" aria-label="Foto 2" class="hero-dot" onclick="goToSlide(1)" style="width: 12px; height: 10px; border-radius: 9999px; background-color: #475569; border: none; cursor: pointer; transition: all 0.4s;"></button>
            <button type="button" aria-label="Foto 3" class="hero-dot" onclick="goToSlide(2)" style="width: 12px; height: 10px; border-radius: 9999px; background-color: #475569; border: none; cursor: pointer; transition: all 0.4s;"></button>
            <button type="button" aria-label="Foto 4" class="hero-dot" onclick="goToSlide(3)" style="width: 12px; height: 10px; border-radius: 9999px; background-color: #475569; border: none; cursor: pointer; transition: all 0.4s;"></button>
            <button type="button" aria-label="Foto 5" class="hero-dot" onclick="goToSlide(4)" style="width: 12px; height: 10px; border-radius: 9999px; background-color: #475569; border: none; cursor: pointer; transition: all 0.4s;"></button>
        </div>
    </div>
"""

# Reemplazo del bloque del carrusel
pattern = re.compile(r'<!--\s*=+\s*HERO SLIDER[\s\S]*?<\/div>\s*<\/div>', re.IGNORECASE)
if pattern.search(html):
    html = pattern.sub(NUEVO_SLIDER_FULL_WIDTH.strip(), html, count=1)
else:
    pattern_id = re.compile(r'<div id="hero-slider-container"[\s\S]*?<\/div>\s*<\/div>', re.IGNORECASE)
    if pattern_id.search(html):
        html = pattern_id.sub(NUEVO_SLIDER_FULL_WIDTH.strip(), html, count=1)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("✓ Cobertura total de pantalla (de izquierda a derecha) aplicada.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "style(hero): cobertura total de izquierda a derecha sin barras laterales", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "style(viamx): carrusel full width edge-to-edge", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
