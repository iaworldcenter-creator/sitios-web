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
print("CLONANDO ESTRUCTURA EXACTA DE PC CUSTOM LAB PARA CARRUSEL EN VÍA MX")
print("=" * 70)

# 1. Asegurar estilos CSS de altura física estricta idénticos a PC Custom Lab
CSS_SLIDER_REGLAS = """
    .hero-slider-container {
        min-height: 600px;
    }
    @media (min-width: 640px) {
        .hero-slider-container {
            min-height: 650px;
        }
    }
"""

if ".hero-slider-container" not in html:
    html = html.replace("</style>", f"{CSS_SLIDER_REGLAS}\n    </style>", 1)

# 2. Estructura HTML idéntica a PC Custom Lab con las 5 fotos de la Familia Tigre
HERO_SLIDER_PC_LAB_FORMAT = """
<!-- HERO SLIDER SECTION (ESTRUCTURA IDÉNTICA A PC CUSTOM LAB - 5 FOTOS FAMILIA TIGRE) -->
<div class="relative w-full h-[600px] sm:h-[650px] min-h-[600px] sm:min-h-[650px] overflow-hidden border-b border-slate-800 bg-slate-950 hero-slider-container">
    <!-- Slides Container -->
    <div class="relative w-full h-full" id="hero-slider">
        <!-- Slide 1 -->
        <div class="hero-slide active absolute inset-0 w-full h-full opacity-100 transition-opacity duration-1000 ease-in-out z-10 bg-cover bg-center" style="background-image: url('assets/img/carucel (1).jpeg');"></div>
        <!-- Slide 2 -->
        <div class="hero-slide absolute inset-0 w-full h-full opacity-0 transition-opacity duration-1000 ease-in-out z-0 bg-cover bg-center" style="background-image: url('assets/img/carucel (2).jpeg');"></div>
        <!-- Slide 3 -->
        <div class="hero-slide absolute inset-0 w-full h-full opacity-0 transition-opacity duration-1000 ease-in-out z-0 bg-cover bg-center" style="background-image: url('assets/img/carucel (3).jpeg');"></div>
        <!-- Slide 4 -->
        <div class="hero-slide absolute inset-0 w-full h-full opacity-0 transition-opacity duration-1000 ease-in-out z-0 bg-cover bg-center" style="background-image: url('assets/img/carucel (4).jpeg');"></div>
        <!-- Slide 5 -->
        <div class="hero-slide absolute inset-0 w-full h-full opacity-0 transition-opacity duration-1000 ease-in-out z-0 bg-cover bg-center" style="background-image: url('assets/img/carucel (5).jpeg');"></div>
    </div>

    <!-- Slider Controls -->
    <button aria-label="Anterior" class="hero-slider-control absolute left-4 top-1/2 -translate-y-1/2 z-20 w-12 h-12 min-w-[48px] min-h-[48px] rounded-full bg-slate-900/60 hover:bg-slate-900 text-slate-300 hover:text-white border border-slate-800 transition flex items-center justify-center cursor-pointer shadow-xl backdrop-blur-md" onclick="prevSlide()">
        <i class="fa-solid fa-chevron-left"></i>
    </button>
    <button aria-label="Siguiente" class="hero-slider-control absolute right-4 top-1/2 -translate-y-1/2 z-20 w-12 h-12 min-w-[48px] min-h-[48px] rounded-full bg-slate-900/60 hover:bg-slate-900 text-slate-300 hover:text-white border border-slate-800 transition flex items-center justify-center cursor-pointer shadow-xl backdrop-blur-md" onclick="nextSlide()">
        <i class="fa-solid fa-chevron-right"></i>
    </button>

    <!-- Slider Pagination Dots (bottom-8 con 5 puntos) -->
    <div class="hero-slider-dots absolute bottom-8 left-0 right-0 z-20 flex justify-center gap-2.5">
        <button aria-label="Ir a diapositiva 1" class="hero-dot min-w-[44px] min-h-[44px] p-3 flex items-center justify-center cursor-pointer" onclick="goToSlide(0)"><span class="w-3 h-3 rounded-full bg-cyan-400 transition-all duration-300 block shadow-lg shadow-cyan-500/50"></span></button>
        <button aria-label="Ir a diapositiva 2" class="hero-dot min-w-[44px] min-h-[44px] p-3 flex items-center justify-center cursor-pointer" onclick="goToSlide(1)"><span class="w-3 h-3 rounded-full bg-slate-500 transition-all duration-300 block"></span></button>
        <button aria-label="Ir a diapositiva 3" class="hero-dot min-w-[44px] min-h-[44px] p-3 flex items-center justify-center cursor-pointer" onclick="goToSlide(2)"><span class="w-3 h-3 rounded-full bg-slate-500 transition-all duration-300 block"></span></button>
        <button aria-label="Ir a diapositiva 4" class="hero-dot min-w-[44px] min-h-[44px] p-3 flex items-center justify-center cursor-pointer" onclick="goToSlide(3)"><span class="w-3 h-3 rounded-full bg-slate-500 transition-all duration-300 block"></span></button>
        <button aria-label="Ir a diapositiva 5" class="hero-dot min-w-[44px] min-h-[44px] p-3 flex items-center justify-center cursor-pointer" onclick="goToSlide(4)"><span class="w-3 h-3 rounded-full bg-slate-500 transition-all duration-300 block"></span></button>
    </div>
</div>
"""

# 3. Lógica JavaScript de Rotación Idéntica a PC Custom Lab
JS_SLIDER_PCLAB = """
<script id="viamx-slider-clean-script">
window.currentSlide = 0;
window.sliderInterval = null;

window.showSlide = function(index) {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-dot span');
    if (slides.length === 0) return;
    
    // Ocultar slide actual
    const current = slides[window.currentSlide];
    if (current) {
        current.classList.remove('active', 'opacity-100', 'z-10');
        current.classList.add('opacity-0', 'z-0');
    }
    const currentDot = dots[window.currentSlide];
    if (currentDot) {
        currentDot.classList.remove('bg-cyan-400', 'shadow-lg', 'shadow-cyan-500/50');
        currentDot.classList.add('bg-slate-500');
    }
    
    window.currentSlide = (index + slides.length) % slides.length;
    
    // Mostrar siguiente slide
    const next = slides[window.currentSlide];
    if (next) {
        next.classList.remove('opacity-0', 'z-0');
        next.classList.add('active', 'opacity-100', 'z-10');
    }
    const nextDot = dots[window.currentSlide];
    if (nextDot) {
        nextDot.classList.remove('bg-slate-500');
        nextDot.classList.add('bg-cyan-400', 'shadow-lg', 'shadow-cyan-500/50');
    }
    window.resetSliderInterval();
};

window.resetSliderInterval = function() {
    if (window.sliderInterval) clearInterval(window.sliderInterval);
    if (window.innerWidth < 640) return;
    window.sliderInterval = setInterval(() => {
        window.nextSlide();
    }, 5000);
};

window.nextSlide = function() {
    window.showSlide(window.currentSlide + 1);
};

window.prevSlide = function() {
    window.showSlide(window.currentSlide - 1);
};

window.goToSlide = function(index) {
    window.showSlide(index);
};

document.addEventListener('DOMContentLoaded', () => {
    window.showSlide(0);
    window.resetSliderInterval();
});
</script>
"""

# Reemplazo del Hero Slider
pattern = re.compile(r'(<!--\s*=*\s*HERO SLIDER[\s\S]*?hero-slider-dots[\s\S]*?<\/div>\s*<\/div>|<div id="hero-slider-container"[\s\S]*?hero-slider-dots[\s\S]*?<\/div>\s*<\/div>|<div class="[^"]*hero-slider-container[^"]*"[\s\S]*?hero-slider-dots[\s\S]*?<\/div>\s*<\/div>)', re.IGNORECASE)

if pattern.search(html):
    html = pattern.sub(HERO_SLIDER_PC_LAB_FORMAT.strip(), html, count=1)
else:
    header_end = html.find("</header>")
    if header_end != -1:
        html = html[:header_end + 9] + "\n\n" + HERO_SLIDER_PC_LAB_FORMAT.strip() + "\n\n" + html[header_end + 9:]

# Reemplazo del script
html = re.sub(r'<script id="viamx-slider[^"]*">[\s\S]*?<\/script>', '', html, flags=re.IGNORECASE)
html = html.replace("</body>", f"{JS_SLIDER_PCLAB.strip()}\n</body>")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("✓ Medidas y comportamiento de PC Custom Lab (600px/650px) replicados con éxito.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "fix(hero): medidas y marco exacto de PC Custom Lab con 5 fotos familia tigre", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(viamx): carrusel con estructura y dimensiones de PC Custom Lab", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
