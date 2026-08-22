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
    print("Error: No se encontró index.html en", VIAMX_DIR)
    exit(1)

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

print("=" * 70)
print("CONFIGURANDO 5 IMÁGENES LIMPIAS DE LA FAMILIA TIGRE EN VÍA MX")
print("=" * 70)

# Estructura del carrusel con las 5 imágenes exactas sin textos encimados
NUEVO_CARRUSEL_HTML = """
<!-- HERO SLIDER (5 FOTOS LIMPIAS FAMILIA TIGRE - 5S INTERVALO + 2S FADE) -->
<div class="relative w-full h-[520px] sm:h-[600px] md:h-[700px] lg:h-[780px] overflow-hidden border-b border-slate-800 bg-slate-950 select-none" id="hero-slider-container">
    <div class="relative w-full h-full" id="hero-slider">
        <div class="hero-slide active absolute inset-0 w-full h-full opacity-100 z-10 transition-opacity duration-[2000ms] ease-in-out bg-cover bg-center" style="background-image: url('assets/img/carucel (1).jpeg');"></div>
        <div class="hero-slide absolute inset-0 w-full h-full opacity-0 z-0 transition-opacity duration-[2000ms] ease-in-out bg-cover bg-center" style="background-image: url('assets/img/carucel (2).jpeg');"></div>
        <div class="hero-slide absolute inset-0 w-full h-full opacity-0 z-0 transition-opacity duration-[2000ms] ease-in-out bg-cover bg-center" style="background-image: url('assets/img/carucel (3).jpeg');"></div>
        <div class="hero-slide absolute inset-0 w-full h-full opacity-0 z-0 transition-opacity duration-[2000ms] ease-in-out bg-cover bg-center" style="background-image: url('assets/img/carucel (4).jpeg');"></div>
        <div class="hero-slide absolute inset-0 w-full h-full opacity-0 z-0 transition-opacity duration-[2000ms] ease-in-out bg-cover bg-center" style="background-image: url('assets/img/carucel (5).jpeg');"></div>
    </div>

    <!-- Controles Izquierda / Derecha -->
    <button type="button" aria-label="Anterior" class="absolute left-4 sm:left-6 top-1/2 -translate-y-1/2 z-20 w-12 h-12 rounded-full bg-slate-950/70 hover:bg-cyan-500 hover:text-slate-950 text-white border border-slate-700 transition flex items-center justify-center shadow-2xl cursor-pointer backdrop-blur-md" onclick="prevSlide()">
        <i class="fa-solid fa-chevron-left text-lg"></i>
    </button>
    <button type="button" aria-label="Siguiente" class="absolute right-4 sm:right-6 top-1/2 -translate-y-1/2 z-20 w-12 h-12 rounded-full bg-slate-950/70 hover:bg-cyan-500 hover:text-slate-950 text-white border border-slate-700 transition flex items-center justify-center shadow-2xl cursor-pointer backdrop-blur-md" onclick="nextSlide()">
        <i class="fa-solid fa-chevron-right text-lg"></i>
    </button>

    <!-- 5 Indicadores Inferiores -->
    <div class="absolute bottom-6 left-0 right-0 z-20 flex justify-center items-center gap-3">
        <button type="button" aria-label="Foto 1" class="hero-dot bg-cyan-400 w-8 shadow-lg shadow-cyan-500/50 h-3 rounded-full transition-all duration-500 cursor-pointer" onclick="goToSlide(0)"></button>
        <button type="button" aria-label="Foto 2" class="hero-dot bg-slate-600/80 w-3 h-3 rounded-full transition-all duration-500 cursor-pointer" onclick="goToSlide(1)"></button>
        <button type="button" aria-label="Foto 3" class="hero-dot bg-slate-600/80 w-3 h-3 rounded-full transition-all duration-500 cursor-pointer" onclick="goToSlide(2)"></button>
        <button type="button" aria-label="Foto 4" class="hero-dot bg-slate-600/80 w-3 h-3 rounded-full transition-all duration-500 cursor-pointer" onclick="goToSlide(3)"></button>
        <button type="button" aria-label="Foto 5" class="hero-dot bg-slate-600/80 w-3 h-3 rounded-full transition-all duration-500 cursor-pointer" onclick="goToSlide(4)"></button>
    </div>
</div>
"""

JS_SLIDER_LOGIC = """
<script id="viamx-slider-clean-script">
window.currentSlideIndex = 0;
window.sliderAutoInterval = null;

window.showSlide = function(index) {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-dot');
    if (!slides || slides.length === 0) return;

    const current = slides[window.currentSlideIndex];
    if (current) {
        current.classList.remove('active', 'opacity-100', 'z-10');
        current.classList.add('opacity-0', 'z-0');
    }
    const currentDot = dots[window.currentSlideIndex];
    if (currentDot) {
        currentDot.classList.remove('bg-cyan-400', 'w-8', 'shadow-lg', 'shadow-cyan-500/50');
        currentDot.classList.add('bg-slate-600/80', 'w-3');
    }

    window.currentSlideIndex = (index + slides.length) % slides.length;

    const next = slides[window.currentSlideIndex];
    if (next) {
        next.classList.remove('opacity-0', 'z-0');
        next.classList.add('active', 'opacity-100', 'z-10');
    }
    const nextDot = dots[window.currentSlideIndex];
    if (nextDot) {
        nextDot.classList.remove('bg-slate-600/80', 'w-3');
        nextDot.classList.add('bg-cyan-400', 'w-8', 'shadow-lg', 'shadow-cyan-500/50');
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
    print("Error: No se encontró </header> en el archivo.")
    exit(1)

# 2. Localizar el inicio del catálogo o contenido posterior
cat_pos = html.find("// CATÁLOGO OFICIAL")
if cat_pos == -1:
    cat_pos = html.find("Artículos en Curaduría")
if cat_pos == -1:
    cat_pos = html.find("<main")
if cat_pos == -1:
    cat_pos = html.find("<section")

if cat_pos != -1:
    # Retroceder al inicio de la etiqueta de esa sección
    tag_start = max(html.rfind("<div", header_end, cat_pos), html.rfind("<section", header_end, cat_pos), html.rfind("<main", header_end, cat_pos))
    if tag_start != -1 and tag_start > header_end:
        cat_pos = tag_start

# 3. Ensamblar sustituyendo todo lo que estaba entre el header y el catálogo
parte_header = html[:header_end + 9]
parte_catalogo_final = html[cat_pos:]

html_limpio = f"{parte_header}\n\n{NUEVO_CARRUSEL_HTML.strip()}\n\n{parte_catalogo_final}"

# 4. Reemplazar o inyectar el script del carrusel
html_limpio = re.sub(r'<script id="viamx-slider[^"]*">[\s\S]*?<\/script>', '', html_limpio, flags=re.IGNORECASE)
html_limpio = html_limpio.replace("</body>", f"{JS_SLIDER_LOGIC.strip()}\n</body>")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html_limpio)

print("✓ Carrusel reemplazado con éxito en bazar-viamx-nfl.gdl/index.html")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "fix(hero): 5 imagenes limpias de familia tigre carucel(1-5).jpeg sin textos", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(viamx): carrusel de 5 fotos limpias familia tigre activo", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
