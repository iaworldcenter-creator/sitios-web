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
print("PURGANDO DUPLICADOS Y DEJANDO UN SOLO CARRUSEL LIMPIO EN VÍA MX")
print("=" * 70)

# 1. Definición del ÚNICO carrusel sin duplicados y con un solo set de controles
CARRUSEL_UNICO_HTML = """
<!-- ========================================================================
     HERO SLIDER (ÚNICO Y LIMPIO - 5 FOTOS FAMILIA TIGRE - 5S / 1S TRANSICIÓN)
     ======================================================================== -->
<div class="relative w-full h-[600px] sm:h-[650px] min-h-[600px] sm:min-h-[650px] overflow-hidden border-b border-slate-800 bg-slate-950 select-none">
    <!-- Contenedor de las 5 Diapositivas -->
    <div class="relative w-full h-full" id="hero-slider">
        <div class="hero-slide active absolute inset-0 w-full h-full opacity-100 transition-opacity duration-1000 ease-in-out z-10 bg-cover bg-center" style="background-image: url('assets/img/carucel (1).jpeg');"></div>
        <div class="hero-slide absolute inset-0 w-full h-full opacity-0 transition-opacity duration-1000 ease-in-out z-0 bg-cover bg-center" style="background-image: url('assets/img/carucel (2).jpeg');"></div>
        <div class="hero-slide absolute inset-0 w-full h-full opacity-0 transition-opacity duration-1000 ease-in-out z-0 bg-cover bg-center" style="background-image: url('assets/img/carucel (3).jpeg');"></div>
        <div class="hero-slide absolute inset-0 w-full h-full opacity-0 transition-opacity duration-1000 ease-in-out z-0 bg-cover bg-center" style="background-image: url('assets/img/carucel (4).jpeg');"></div>
        <div class="hero-slide absolute inset-0 w-full h-full opacity-0 transition-opacity duration-1000 ease-in-out z-0 bg-cover bg-center" style="background-image: url('assets/img/carucel (5).jpeg');"></div>
    </div>

    <!-- Único Control Izquierdo -->
    <button type="button" aria-label="Anterior" class="absolute left-4 top-1/2 -translate-y-1/2 z-20 w-12 h-12 min-w-[48px] min-h-[48px] rounded-full bg-slate-900/60 hover:bg-slate-900 text-slate-300 hover:text-white border border-slate-800 transition flex items-center justify-center cursor-pointer shadow-xl backdrop-blur-md" onclick="prevSlide()">
        <i class="fa-solid fa-chevron-left text-base"></i>
    </button>

    <!-- Único Control Derecho -->
    <button type="button" aria-label="Siguiente" class="absolute right-4 top-1/2 -translate-y-1/2 z-20 w-12 h-12 min-w-[48px] min-h-[48px] rounded-full bg-slate-900/60 hover:bg-slate-900 text-slate-300 hover:text-white border border-slate-800 transition flex items-center justify-center cursor-pointer shadow-xl backdrop-blur-md" onclick="nextSlide()">
        <i class="fa-solid fa-chevron-right text-base"></i>
    </button>

    <!-- Único Set de 5 Indicadores Inferiores -->
    <div class="hero-slider-dots absolute bottom-8 left-0 right-0 z-20 flex justify-center items-center gap-2.5">
        <button type="button" aria-label="Foto 1" class="hero-dot min-w-[44px] min-h-[44px] p-3 flex items-center justify-center cursor-pointer" onclick="goToSlide(0)"><span class="w-3 h-3 rounded-full bg-cyan-400 transition-all duration-300 block shadow-lg shadow-cyan-500/50"></span></button>
        <button type="button" aria-label="Foto 2" class="hero-dot min-w-[44px] min-h-[44px] p-3 flex items-center justify-center cursor-pointer" onclick="goToSlide(1)"><span class="w-3 h-3 rounded-full bg-slate-500 transition-all duration-300 block"></span></button>
        <button type="button" aria-label="Foto 3" class="hero-dot min-w-[44px] min-h-[44px] p-3 flex items-center justify-center cursor-pointer" onclick="goToSlide(2)"><span class="w-3 h-3 rounded-full bg-slate-500 transition-all duration-300 block"></span></button>
        <button type="button" aria-label="Foto 4" class="hero-dot min-w-[44px] min-h-[44px] p-3 flex items-center justify-center cursor-pointer" onclick="goToSlide(3)"><span class="w-3 h-3 rounded-full bg-slate-500 transition-all duration-300 block"></span></button>
        <button type="button" aria-label="Foto 5" class="hero-dot min-w-[44px] min-h-[44px] p-3 flex items-center justify-center cursor-pointer" onclick="goToSlide(4)"><span class="w-3 h-3 rounded-full bg-slate-500 transition-all duration-300 block"></span></button>
    </div>
</div>
"""

JS_SLIDER_UNICO = """
<script id="viamx-slider-clean-script">
window.currentSlide = 0;
window.sliderInterval = null;

window.showSlide = function(index) {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-dot span');
    if (slides.length === 0) return;
    
    // Desvanecer slide anterior
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
    
    // Mostrar nuevo slide
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

# 2. Localizar el cierre de </header>
header_pos = html.find("</header>")
if header_pos == -1:
    print("[Error] No se encontró </header>")
    exit(1)
header_end = header_pos + len("</header>")

# 3. Localizar el inicio del catálogo principal para eliminar TODO lo intermedio
cat_pos = html.find("<main")
if cat_pos == -1:
    cat_pos = html.find("// CATÁLOGO OFICIAL")
if cat_pos == -1:
    cat_pos = html.find("Artículos en Curaduría")

if cat_pos != -1 and cat_pos > header_end:
    # Retroceder al <main o <section correspondiente
    tag_start = max(html.rfind("<main", header_end, cat_pos), html.rfind("<section", header_end, cat_pos), html.rfind("<div class=\"flex-1", header_end, cat_pos))
    if tag_start != -1 and tag_start > header_end:
        cat_pos = tag_start
else:
    cat_pos = html.find("<footer")

# 4. Reensamblaje sin residuos intermedios
parte_arriba = html[:header_end]
parte_abajo = html[cat_pos:]

# Purgar scripts anteriores de slider
parte_abajo = re.sub(r'<script id="viamx-slider[^"]*">[\s\S]*?<\/script>', '', parte_abajo, flags=re.IGNORECASE)

html_final = f"{parte_arriba}\n\n{CARRUSEL_UNICO_HTML.strip()}\n\n{parte_abajo}"

# Inyectar el script único antes de </body>
html_final = html_final.replace("</body>", f"{JS_SLIDER_UNICO.strip()}\n</body>")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html_final)

print("✓ Carrusel duplicado eliminado. Se dejó un único carrusel limpio con 2 controles.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "fix(hero): purgar sliders duplicados y unificar en un solo carrusel de 5 fotos", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(viamx): carrusel unico sin duplicidad de botones ni imagenes", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
