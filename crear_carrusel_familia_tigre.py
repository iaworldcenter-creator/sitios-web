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
IMG_DIR = os.path.join(VIAMX_DIR, "assets", "img")

print("=" * 70)
print("INTEGRANDO CARRUSEL DE 5 DIAPOSITIVAS (FAMILIA TIGRE) EN VÍA MX")
print("=" * 70)

# 1. Detectar las imágenes en assets/img
candidate_images = []
if os.path.exists(IMG_DIR):
    all_files = [os.path.join(IMG_DIR, f) for f in os.listdir(IMG_DIR) if f.lower().endswith(('.webp', '.png', '.jpg', '.jpeg'))]
    # Ordenar por fecha de modificación (más recientes primero) o buscar palabras clave
    all_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    # Filtrar imágenes que hagan referencia a familia/tigre/hero/slider o tomar las más recientes
    for full_p in all_files:
        fname = os.path.basename(full_p)
        if any(k in fname.lower() for k in ['familia', 'family', 'tigre', 'tiger', 'viamx', 'nfl', 'hero', 'slider', 'gemini']):
            candidate_images.append(f"assets/img/{fname}")
    
    # Si faltan para completar 5, rellenar con las más recientes del directorio
    for full_p in all_files:
        rel = f"assets/img/{os.path.basename(full_p)}"
        if rel not in candidate_images:
            candidate_images.append(rel)

# Garantizar exactamente 5 imágenes
if not candidate_images:
    candidate_images = ["assets/img/mascota_tigre.webp"]

while len(candidate_images) < 5:
    candidate_images += list(candidate_images)
selected_5_imgs = candidate_images[:5]

# Títulos y eslóganes temáticos para las 5 diapositivas de Vía MX
slides_data = [
    {
        "tag": "Boutique Internacional & Curaduría 2026",
        "title": "VíaMX Curaduría Selecta",
        "highlight": "Calidad & Estilo Familiar",
        "desc": "Accede a artículos exclusivos, tecnología de vanguardia y oportunidades de importación con entrega directa en Guadalajara Centro.",
        "btn_text": "Explorar Catálogo",
        "btn_link": "#catalogo",
        "btn_icon": "fa-solid fa-tags",
        "img": selected_5_imgs[0]
    },
    {
        "tag": "Coleccionables & Deporte Oficial",
        "title": "Pasión NFL & Jerseys",
        "highlight": "Ediciones Originales",
        "desc": "Indumentaria oficial, chamarras, gorras y piezas conmemorativas para aficionados que exigen autenticidad total.",
        "btn_text": "Ver Colección Deportiva",
        "btn_link": "#catalogo",
        "btn_icon": "fa-solid fa-football",
        "img": selected_5_imgs[1]
    },
    {
        "tag": "Importación Exclusiva & Vanguardia",
        "title": "Tendencias Globales",
        "highlight": "Selección Premium",
        "desc": "Prendas de alta categoría y accesorios internacionales seleccionados rigurosamente bajo el estándar de calidad Vía MX.",
        "btn_text": "Descubrir Novedades",
        "btn_link": "#catalogo",
        "btn_icon": "fa-solid fa-gem",
        "img": selected_5_imgs[2]
    },
    {
        "tag": "Familia Tigre & Respaldo Corporativo",
        "title": "Confianza y Calidad",
        "highlight": "Garantía Local 48h",
        "desc": "Compra con seguridad y respaldo físico en Pedro Moreno 501 A. Atención técnica y soporte personalizado en cada pedido.",
        "btn_text": "Conocer Beneficios",
        "btn_link": "#contacto",
        "btn_icon": "fa-solid fa-shield-halved",
        "img": selected_5_imgs[3]
    },
    {
        "tag": "Beneficios de Ecosistema Unificado",
        "title": "Envíos Consolidados &",
        "highlight": "5% de Cashback",
        "desc": "Combina tus compras de las 7 tiendas en un solo carrito global y obtén envío gratis a partir de $1,500 MXN.",
        "btn_text": "Ir al Carrito Global",
        "btn_link": "checkout.html",
        "btn_icon": "fa-solid fa-cart-shopping",
        "img": selected_5_imgs[4]
    }
]

# Construir HTML de las 5 diapositivas
slides_html = ""
dots_html = ""
for idx, s in enumerate(slides_data):
    active_class = "active opacity-100 z-10" if idx == 0 else "opacity-0 z-0"
    dot_active = "bg-cyan-400 w-8" if idx == 0 else "bg-slate-600 w-3"
    
    slides_html += f"""
        <!-- Slide {idx + 1} -->
        <div class="hero-slide {active_class} absolute inset-0 w-full h-full transition-opacity duration-1000 ease-in-out bg-cover bg-center" style="background-image: url('{s["img"]}');">
            <div class="absolute inset-0 bg-slate-950/75 backdrop-blur-[1px]"></div>
            <div class="relative z-10 max-w-5xl mx-auto h-full flex flex-col items-center justify-center text-center px-4 sm:px-6 pb-16">
                <span class="px-4 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 font-mono text-xs uppercase tracking-widest inline-block mb-4 shadow-sm">
                    {s["tag"]}
                </span>
                <h1 class="text-3xl sm:text-5xl font-black text-white tracking-tight mb-4 leading-tight">
                    {s["title"]} <br class="hidden sm:inline"/><span class="bg-gradient-to-r from-cyan-400 via-sky-300 to-amber-300 bg-clip-text text-transparent">{s["highlight"]}</span>
                </h1>
                <p class="text-sm sm:text-base text-slate-300 mb-8 max-w-2xl mx-auto font-normal leading-relaxed">
                    {s["desc"]}
                </p>
                <div class="flex flex-wrap items-center justify-center gap-3">
                    <a class="bg-amber-400 hover:bg-amber-300 text-slate-950 font-black px-7 py-3 rounded-xl shadow-xl transition text-xs sm:text-sm flex items-center gap-2 border border-amber-500/50 active:scale-95 cursor-pointer" href="{s["btn_link"]}">
                        <i class="{s["btn_icon"]} text-slate-950"></i> {s["btn_text"]}
                    </a>
                    <a class="bg-slate-900/80 hover:bg-slate-800 text-slate-200 border border-slate-700 font-bold px-6 py-3 rounded-xl shadow-lg transition text-xs sm:text-sm flex items-center gap-2 active:scale-95 cursor-pointer" href="checkout.html">
                        Ir al Checkout <i class="fa-solid fa-arrow-right text-xs"></i>
                    </a>
                </div>
            </div>
        </div>
    """
    dots_html += f"""<button aria-label="Slide {idx + 1}" class="hero-dot {dot_active} h-3 rounded-full transition-all duration-300 cursor-pointer" onclick="goToSlide({idx})"></button>\n"""

HERO_CAROUSEL_BLOCK = f"""
<!-- HERO SLIDER SECTION (5 DIAPOSITIVAS - FAMILIA TIGRE - 5 SEGUNDOS) -->
<div class="relative w-full h-[580px] sm:h-[640px] overflow-hidden border-b border-slate-800 bg-slate-950 hero-slider-container">
    <div class="relative w-full h-full" id="hero-slider">
        {slides_html}
    </div>

    <!-- Controles Izquierda / Derecha -->
    <button aria-label="Anterior Diapositiva" class="hero-slider-control absolute left-4 top-1/2 -translate-y-1/2 z-20 w-11 h-11 rounded-full bg-slate-900/60 hover:bg-cyan-500 hover:text-slate-950 text-slate-200 border border-slate-700 transition flex items-center justify-center shadow-xl cursor-pointer" onclick="prevSlide()">
        <i class="fa-solid fa-chevron-left text-sm"></i>
    </button>
    <button aria-label="Siguiente Diapositiva" class="hero-slider-control absolute right-4 top-1/2 -translate-y-1/2 z-20 w-11 h-11 rounded-full bg-slate-900/60 hover:bg-cyan-500 hover:text-slate-950 text-slate-200 border border-slate-700 transition flex items-center justify-center shadow-xl cursor-pointer" onclick="nextSlide()">
        <i class="fa-solid fa-chevron-right text-sm"></i>
    </button>

    <!-- Indicadores Inferiores (5 Dots) -->
    <div class="hero-slider-dots absolute bottom-7 left-0 right-0 z-20 flex justify-center items-center gap-2.5">
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

    // Ocultar slide actual
    const current = slides[currentSlideIndex];
    if (current) {
        current.classList.remove('active', 'opacity-100', 'z-10');
        current.classList.add('opacity-0', 'z-0');
    }
    const currentDot = dots[currentSlideIndex];
    if (currentDot) {
        currentDot.classList.remove('bg-cyan-400', 'w-8');
        currentDot.classList.add('bg-slate-600', 'w-3');
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
        nextDot.classList.remove('bg-slate-600', 'w-3');
        nextDot.classList.add('bg-cyan-400', 'w-8');
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

# 2. Reemplazar o insertar el Hero Slider justo debajo del </header>
pattern_hero = re.compile(r'(<!--\s*HERO SLIDER[\s\S]*?<\/div>\s*<\/div>|<div class="relative w-full h-\[\d+px\][\s\S]*?hero-slider-dots[\s\S]*?<\/div>\s*<\/div>)', re.IGNORECASE)

if pattern_hero.search(html):
    html = pattern_hero.sub(HERO_CAROUSEL_BLOCK.strip(), html, count=1)
    print("✓ Hero Slider anterior reemplazado por el nuevo carrusel de 5 diapositivas.")
else:
    # Insertar justo después de </header>
    if "</header>" in html:
        html = html.replace("</header>", f"</header>\n\n{HERO_CAROUSEL_BLOCK.strip()}", 1)
        print("✓ Carrusel de 5 diapositivas insertado inmediatamente después de </header>.")

# 3. Integrar la lógica JavaScript del temporizador de 5 segundos
if 'id="viamx-slider-script"' in html:
    html = re.sub(r'<script id="viamx-slider-script">[\s\S]*?<\/script>', JS_SLIDER_LOGIC.strip(), html)
else:
    html = html.replace("</body>", f"{JS_SLIDER_LOGIC.strip()}\n</body>")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(hero): carrusel de 5 imagenes de familia tigre con transicion a 5s", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(viamx): carrusel hero de 5 diapositivas familia tigre sincronizado", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
