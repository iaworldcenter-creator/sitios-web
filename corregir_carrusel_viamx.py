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
print("RECONSTRUYENDO CARRUSEL CON ESTILOS EXPLÍCITOS (5 FOTOS FAMILIA TIGRE)")
print("=" * 70)

# HTML Estructurado y Robusto con estilos en línea (Garantiza visibilidad al 100%)
HERO_CAROUSEL_ROBUSTO = """
<!-- HERO SLIDER SECTION (5 FOTOS FAMILIA TIGRE - 5S INTERVALO + 2S FADE) -->
<div id="hero-slider-container" style="position: relative; width: 100%; height: 620px; overflow: hidden; background-color: #020617; border-bottom: 1px solid #1e293b; user-select: none;">
    <div id="hero-slider" style="position: relative; width: 100%; height: 100%;">
        <!-- Slide 1 -->
        <div class="hero-slide active" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 1; z-index: 10; transition: opacity 2000ms ease-in-out;">
            <img src="assets/img/carucel (1).jpeg" alt="Familia Tigre 1" style="width: 100%; height: 100%; object-fit: cover; object-position: center;" />
        </div>
        <!-- Slide 2 -->
        <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 2000ms ease-in-out;">
            <img src="assets/img/carucel (2).jpeg" alt="Familia Tigre 2" style="width: 100%; height: 100%; object-fit: cover; object-position: center;" />
        </div>
        <!-- Slide 3 -->
        <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 2000ms ease-in-out;">
            <img src="assets/img/carucel (3).jpeg" alt="Familia Tigre 3" style="width: 100%; height: 100%; object-fit: cover; object-position: center;" />
        </div>
        <!-- Slide 4 -->
        <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 2000ms ease-in-out;">
            <img src="assets/img/carucel (4).jpeg" alt="Familia Tigre 4" style="width: 100%; height: 100%; object-fit: cover; object-position: center;" />
        </div>
        <!-- Slide 5 -->
        <div class="hero-slide" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; z-index: 0; transition: opacity 2000ms ease-in-out;">
            <img src="assets/img/carucel (5).jpeg" alt="Familia Tigre 5" style="width: 100%; height: 100%; object-fit: cover; object-position: center;" />
        </div>
    </div>

    <!-- Controles Izquierda / Derecha -->
    <button type="button" aria-label="Anterior" onclick="prevSlide()" style="position: absolute; left: 24px; top: 50%; transform: translateY(-50%); z-index: 20; width: 48px; height: 48px; border-radius: 9999px; background-color: rgba(2, 6, 23, 0.7); color: #ffffff; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 10px 25px rgba(0,0,0,0.5); backdrop-filter: blur(8px); transition: all 0.3s;">
        <i class="fa-solid fa-chevron-left" style="font-size: 18px;"></i>
    </button>
    <button type="button" aria-label="Siguiente" onclick="nextSlide()" style="position: absolute; right: 24px; top: 50%; transform: translateY(-50%); z-index: 20; width: 48px; height: 48px; border-radius: 9999px; background-color: rgba(2, 6, 23, 0.7); color: #ffffff; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 10px 25px rgba(0,0,0,0.5); backdrop-filter: blur(8px); transition: all 0.3s;">
        <i class="fa-solid fa-chevron-right" style="font-size: 18px;"></i>
    </button>

    <!-- Indicadores Inferiores (5 Dots) -->
    <div style="position: absolute; bottom: 24px; left: 0; right: 0; z-index: 20; display: flex; justify-content: center; align-items: center; gap: 10px;">
        <button type="button" aria-label="Foto 1" class="hero-dot" onclick="goToSlide(0)" style="width: 32px; height: 10px; border-radius: 9999px; background-color: #22d3ee; border: none; cursor: pointer; transition: all 0.4s; box-shadow: 0 0 10px rgba(34,211,238,0.6);"></button>
        <button type="button" aria-label="Foto 2" class="hero-dot" onclick="goToSlide(1)" style="width: 12px; height: 10px; border-radius: 9999px; background-color: #475569; border: none; cursor: pointer; transition: all 0.4s;"></button>
        <button type="button" aria-label="Foto 3" class="hero-dot" onclick="goToSlide(2)" style="width: 12px; height: 10px; border-radius: 9999px; background-color: #475569; border: none; cursor: pointer; transition: all 0.4s;"></button>
        <button type="button" aria-label="Foto 4" class="hero-dot" onclick="goToSlide(3)" style="width: 12px; height: 10px; border-radius: 9999px; background-color: #475569; border: none; cursor: pointer; transition: all 0.4s;"></button>
        <button type="button" aria-label="Foto 5" class="hero-dot" onclick="goToSlide(4)" style="width: 12px; height: 10px; border-radius: 9999px; background-color: #475569; border: none; cursor: pointer; transition: all 0.4s;"></button>
    </div>
</div>
"""

JS_SLIDER_CONTROLLER = """
<script id="viamx-slider-clean-script">
window.currentSlideIndex = 0;
window.sliderAutoInterval = null;

window.showSlide = function(index) {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-dot');
    if (!slides || slides.length === 0) return;

    // Desvanecer slide anterior
    const current = slides[window.currentSlideIndex];
    if (current) {
        current.style.opacity = '0';
        current.style.zIndex = '0';
    }
    const currentDot = dots[window.currentSlideIndex];
    if (currentDot) {
        currentDot.style.width = '12px';
        currentDot.style.backgroundColor = '#475569';
        currentDot.style.boxShadow = 'none';
    }

    window.currentSlideIndex = (index + slides.length) % slides.length;

    // Mostrar nuevo slide
    const next = slides[window.currentSlideIndex];
    if (next) {
        next.style.opacity = '1';
        next.style.zIndex = '10';
    }
    const nextDot = dots[window.currentSlideIndex];
    if (nextDot) {
        nextDot.style.width = '32px';
        nextDot.style.backgroundColor = '#22d3ee';
        nextDot.style.boxShadow = '0 0 10px rgba(34,211,238,0.6)';
    }
    window.resetSliderInterval();
};

window.resetSliderInterval = function() {
    if (window.sliderAutoInterval) clearInterval(window.sliderAutoInterval);
    window.sliderAutoInterval = setInterval(() => {
        window.nextSlide();
    }, 5000);
};

window.nextSlide = function() {
    window.showSlide(window.currentSlideIndex + 1);
};

window.prevSlide = function() {
    window.showSlide(window.currentSlideIndex - 1);
};

window.goToSlide = function(index) {
    window.showSlide(index);
};

document.addEventListener('DOMContentLoaded', () => {
    window.resetSliderInterval();
});
</script>
"""

# 1. Localizar </header>
header_end = html.find("</header>")
if header_end == -1:
    print("[Error] No se encontró </header> en el archivo.")
    exit(1)

# 2. Localizar inicio de la sección del catálogo
cat_pos = html.find("// CATÁLOGO OFICIAL")
if cat_pos == -1:
    cat_pos = html.find("Artículos en Curaduría")
if cat_pos == -1:
    cat_pos = html.find("<main")

if cat_pos != -1:
    tag_start = max(html.rfind("<div", header_end, cat_pos), html.rfind("<section", header_end, cat_pos), html.rfind("<main", header_end, cat_pos))
    if tag_start != -1 and tag_start > header_end:
        cat_pos = tag_start
else:
    cat_pos = html.find("<footer")

# 3. Ensamblar documento
parte_header = html[:header_end + 9]
parte_catalogo = html[cat_pos:]

html_final = f"{parte_header}\n\n{HERO_CAROUSEL_ROBUSTO.strip()}\n\n{parte_catalogo}"

# 4. Inyectar controlador JavaScript antes de </body>
html_final = re.sub(r'<script id="viamx-slider[^"]*">[\s\S]*?<\/script>', '', html_final, flags=re.IGNORECASE)
html_final = html_final.replace("</body>", f"{JS_SLIDER_CONTROLLER.strip()}\n</body>")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html_final)

print("✓ Carrusel incrustado con éxito y estilos explícitos en index.html")

print("\n=== DESPLEGANDO A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "fix(hero): carrusel de 5 fotos familia tigre con estilos explicitos y transicion 2s", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(viamx): carrusel 5 fotos familia tigre garantizado", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
