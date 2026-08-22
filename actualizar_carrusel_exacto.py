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

print("=" * 70)
print("CONFIGURANDO CARRUSEL LIMPIO (5 IMÁGENES DE LA FAMILIA TIGRE)")
print("=" * 70)

# Nombres exactos de las imágenes detectadas
carousel_imgs = [
    "assets/img/carucel%20(1).jpeg",
    "assets/img/carucel%20(2).jpeg",
    "assets/img/carucel%20(3).jpeg",
    "assets/img/carucel%20(4).jpeg",
    "assets/img/carucel%20(5).jpeg"
]

slides_html = ""
dots_html = ""

for idx, img_url in enumerate(carousel_imgs):
    active_class = "active opacity-100 z-10" if idx == 0 else "opacity-0 z-0"
    dot_active = "bg-cyan-400 w-8 shadow-lg shadow-cyan-500/50" if idx == 0 else "bg-slate-600/80 w-3"
    
    slides_html += f"""
        <!-- Slide {idx + 1} -->
        <div class="hero-slide {active_class} absolute inset-0 w-full h-full transition-opacity duration-[2000ms] ease-in-out bg-cover bg-center" style="background-image: url('{img_url}');"></div>
    """
    dots_html += f"""<button aria-label="Slide {idx + 1}" class="hero-dot {dot_active} h-3 rounded-full transition-all duration-500 cursor-pointer hover:bg-cyan-300" onclick="goToSlide({idx})"></button>\n"""

HERO_CAROUSEL_CLEAN = f"""
<!-- HERO SLIDER SECTION (5 IMÁGENES FAMILIA TIGRE - FOTO LIMPIA - 5S INTERVALO + 2S TRANSICIÓN) -->
<div class="relative w-full h-[500px] sm:h-[580px] md:h-[660px] lg:h-[720px] overflow-hidden border-b border-slate-800 bg-slate-950 hero-slider-container">
    <div class="relative w-full h-full" id="hero-slider">
        {slides_html}
    </div>

    <!-- Controles Izquierda / Derecha -->
    <button aria-label="Anterior Diapositiva" class="hero-slider-control absolute left-4 sm:left-6 top-1/2 -translate-y-1/2 z-20 w-12 h-12 rounded-full bg-slate-950/60 hover:bg-cyan-500 hover:text-slate-950 text-white border border-slate-700/80 transition flex items-center justify-center shadow-2xl cursor-pointer backdrop-blur-md" onclick="prevSlide()">
        <i class="fa-solid fa-chevron-left text-lg"></i>
    </button>
    <button aria-label="Siguiente Diapositiva" class="hero-slider-control absolute right-4 sm:right-6 top-1/2 -translate-y-1/2 z-20 w-12 h-12 rounded-full bg-slate-950/60 hover:bg-cyan-500 hover:text-slate-950 text-white border border-slate-700/80 transition flex items-center justify-center shadow-2xl cursor-pointer backdrop-blur-md" onclick="nextSlide()">
        <i class="fa-solid fa-chevron-right text-lg"></i>
    </button>

    <!-- Indicadores Inferiores (5 Dots) -->
    <div class="hero-slider-dots absolute bottom-6 left-0 right-0 z-20 flex justify-center items-center gap-3">
        {dots_html}
    </div>
</div>
"""

JS_SLIDER_LOGIC = """
<script id="viamx-slider-script">
let currentSlideIndex = 0;
let sliderAutoInterval = null;

function showSlide(index) {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-dot');
    if (!slides || slides.length === 0) return;

    // Desvanecer slide actual (duración 2s)
    const current = slides[currentSlideIndex];
    if (current) {
        current.classList.remove('active', 'opacity-100', 'z-10');
        current.classList.add('opacity-0', 'z-0');
    }
    const currentDot = dots[currentSlideIndex];
    if (currentDot) {
        currentDot.classList.remove('bg-cyan-400', 'w-8', 'shadow-lg', 'shadow-cyan-500/50');
        currentDot.classList.add('bg-slate-600/80', 'w-3');
    }

    currentSlideIndex = (index + slides.length) % slides.length;

    // Mostrar nuevo slide
    const next = slides[currentSlideIndex];
    if (next) {
        next.classList.remove('opacity-0', 'z-0');
        next.classList.add('active', 'opacity-100', 'z-10');
    }
    const nextDot = dots[currentSlideIndex];
    if (nextDot) {
        nextDot.classList.remove('bg-slate-600/80', 'w-3');
        nextDot.classList.add('bg-cyan-400', 'w-8', 'shadow-lg', 'shadow-cyan-500/50');
    }
    resetSliderInterval();
}

function resetSliderInterval() {
    if (sliderAutoInterval) clearInterval(sliderAutoInterval);
    sliderAutoInterval = setInterval(() => {
        nextSlide();
    }, 5000);
}

function nextSlide() {
    showSlide(currentSlideIndex + 1);
}

function prevSlide() {
    showSlide(currentSlideIndex - 1);
}

function goToSlide(index) {
    showSlide(index);
}

document.addEventListener('DOMContentLoaded', () => {
    resetSliderInterval();
});
</script>
"""

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Reemplazar la sección del carrusel existente
pattern_hero = re.compile(r'(<!--\s*HERO SLIDER[\s\S]*?<\/div>\s*<\/div>|<div class="relative w-full h-\[\d+px\][\s\S]*?hero-slider-dots[\s\S]*?<\/div>\s*<\/div>)', re.IGNORECASE)

if pattern_hero.search(html):
    html = pattern_hero.sub(HERO_CAROUSEL_CLEAN.strip(), html, count=1)
else:
    if "</header>" in html:
        html = html.replace("</header>", f"</header>\n\n{HERO_CAROUSEL_CLEAN.strip()}", 1)

# Actualizar el script de control del carrusel
if 'id="viamx-slider-script"' in html:
    html = re.sub(r'<script id="viamx-slider-script">[\s\S]*?<\/script>', JS_SLIDER_LOGIC.strip(), html)
else:
    html = html.replace("</body>", f"{JS_SLIDER_LOGIC.strip()}\n</body>")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("✓ pc-custom-lab/index.html actualizado con las 5 fotos exactas.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(hero): carrusel de 5 fotos limpias familia tigre (5s intervalo + 2s fade)", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(viamx): carrusel con imagenes exactas carucel (1-5).jpeg sincronizado", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
