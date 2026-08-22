import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
PC_LAB_INDEX = os.path.join(BASE_DIR, "pc-custom-lab", "index.html")

if not os.path.exists(PC_LAB_INDEX):
    print("Error: No se encontró pc-custom-lab/index.html")
    exit(1)

with open(PC_LAB_INDEX, "r", encoding="utf-8") as f:
    html = f.read()

# 1. DEFINICIÓN DE LOS DOS BLOQUES LIMPIOS Y EXACTOS

REFACCIONES_HTML = """
    <!-- BOUTIQUE DE REFACCIONES (INMEDIATAMENTE DEBAJO DEL HERO CAROUSEL) -->
    <section class="py-12 bg-slate-900 border-y border-slate-800 text-center relative overflow-hidden" id="boutique-refacciones">
        <div class="max-w-5xl mx-auto px-4 relative z-10">
            <span class="text-[11px] font-mono font-bold uppercase tracking-widest text-amber-400 bg-amber-400/10 px-3 py-1 rounded-full border border-amber-400/30 inline-block mb-3">Tu almacén virtual: Catálogo Inmenso</span>
            <h2 class="text-2xl sm:text-4xl font-black text-white tracking-tight mb-3">Miles de Piezas & Refacciones Sueltas</h2>
            <p class="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto mb-6">Accede a componentes de oportunidad al mejor precio de mayoreo y entrega inmediata.</p>
            <a href="#catalogo" class="inline-flex items-center gap-2 px-8 py-3.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-xs uppercase tracking-wider rounded-xl shadow-lg transition active:scale-95">
                <i class="fa-solid fa-microchip"></i> Explorar Boutique de Refacciones
            </a>
        </div>
    </section>
"""

TIGRE_HTML = """
    <!-- SECCIÓN GARANTÍA, CALIDAD Y RESPALDO (CARRUSEL TIGRE EN CÁMARA LENTA ENTRE COTIZADOR Y LEALTAD) -->
    <section class="py-16 bg-slate-950 border-t border-slate-900 overflow-hidden relative" id="garantia-calidad-tigre">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center mb-8">
            <span class="text-[10px] font-mono text-cyan-400 uppercase tracking-widest bg-cyan-500/10 px-3 py-1 rounded-full border border-cyan-500/30 font-bold inline-block mb-2">PC CUSTOM LAB & TECH SERVICE</span>
            <h2 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Garantía, Calidad y Respaldo</h2>
            <p class="text-xs text-slate-400 max-w-xl mx-auto mt-2">Conoce a nuestra mascota y los pilares que respaldan cada uno de nuestros ensambles y servicios técnicos.</p>
        </div>

        <!-- Track animado en cámara lenta para lectura cómoda -->
        <div class="relative w-full overflow-hidden select-none">
            <div class="tigre-slow-marquee flex gap-6 w-max py-4">
                <!-- Tarjeta 1 -->
                <div class="w-[280px] sm:w-[320px] bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden p-4 flex flex-col items-center text-center shrink-0 shadow-xl">
                    <div class="w-full h-44 rounded-xl overflow-hidden bg-slate-950 mb-3 border border-slate-800">
                        <img src="assets/img/slider_ia_human_thumb.webp" class="w-full h-full object-cover hover:scale-105 transition duration-500" alt="Muro de Marcas Global" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp'" />
                    </div>
                    <span class="text-[11px] font-black text-cyan-400 uppercase font-mono tracking-wider">Muro de Marcas Global</span>
                    <p class="text-[10px] text-slate-400 mt-1">Componentes certificados con soporte oficial de fabricantes.</p>
                </div>
                <!-- Tarjeta 2 -->
                <div class="w-[280px] sm:w-[320px] bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden p-4 flex flex-col items-center text-center shrink-0 shadow-xl">
                    <div class="w-full h-44 rounded-xl overflow-hidden bg-slate-950 mb-3 border border-slate-800">
                        <img src="assets/img/slider_ia_human_thumb.webp" class="w-full h-full object-cover hover:scale-105 transition duration-500" alt="Periféricos & Accesorios" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp'" />
                    </div>
                    <span class="text-[11px] font-black text-emerald-400 uppercase font-mono tracking-wider">Periféricos & Accesorios</span>
                    <p class="text-[10px] text-slate-400 mt-1">Variedad radical y ergonomía para setups profesionales.</p>
                </div>
                <!-- Tarjeta 3 -->
                <div class="w-[280px] sm:w-[320px] bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden p-4 flex flex-col items-center text-center shrink-0 shadow-xl">
                    <div class="w-full h-44 rounded-xl overflow-hidden bg-slate-950 mb-3 border border-slate-800">
                        <img src="assets/img/slider_ia_human_thumb.webp" class="w-full h-full object-cover hover:scale-105 transition duration-500" alt="PC Custom Lab Tech Service" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp'" />
                    </div>
                    <span class="text-[11px] font-black text-amber-400 uppercase font-mono tracking-wider">PC Custom Lab | Tech Service</span>
                    <p class="text-[10px] text-slate-400 mt-1">Ensambles de precisión con pruebas de estrés y garantía local.</p>
                </div>
                <!-- Tarjeta 4 (Loop) -->
                <div class="w-[280px] sm:w-[320px] bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden p-4 flex flex-col items-center text-center shrink-0 shadow-xl">
                    <div class="w-full h-44 rounded-xl overflow-hidden bg-slate-950 mb-3 border border-slate-800">
                        <img src="assets/img/slider_ia_human_thumb.webp" class="w-full h-full object-cover hover:scale-105 transition duration-500" alt="Muro de Marcas Global" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp'" />
                    </div>
                    <span class="text-[11px] font-black text-cyan-400 uppercase font-mono tracking-wider">Muro de Marcas Global</span>
                    <p class="text-[10px] text-slate-400 mt-1">Componentes certificados con soporte oficial de fabricantes.</p>
                </div>
                <!-- Tarjeta 5 (Loop) -->
                <div class="w-[280px] sm:w-[320px] bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden p-4 flex flex-col items-center text-center shrink-0 shadow-xl">
                    <div class="w-full h-44 rounded-xl overflow-hidden bg-slate-950 mb-3 border border-slate-800">
                        <img src="assets/img/slider_ia_human_thumb.webp" class="w-full h-full object-cover hover:scale-105 transition duration-500" alt="Periféricos & Accesorios" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp'" />
                    </div>
                    <span class="text-[11px] font-black text-emerald-400 uppercase font-mono tracking-wider">Periféricos & Accesorios</span>
                    <p class="text-[10px] text-slate-400 mt-1">Variedad radical y ergonomía para setups profesionales.</p>
                </div>
            </div>
        </div>

        <style>
            @keyframes tigreMarqueeSlow {
                0% { transform: translateX(0); }
                100% { transform: translateX(-50%); }
            }
            .tigre-slow-marquee {
                animation: tigreMarqueeSlow 45s linear infinite;
            }
            .tigre-slow-marquee:hover {
                animation-play-state: paused;
            }
        </style>
    </section>
"""

# 2. PURGAR CUALQUIER INSTANCIA PREVIA DE ESTOS DOS BLOQUES
html_clean = html

# Eliminar instancias antiguas de Boutique de Refacciones
html_clean = re.sub(r'<!--\s*BOUTIQUE DE REFACCIONES[\s\S]*?<\/section>', '', html_clean, flags=re.IGNORECASE)
html_clean = re.sub(r'<section[^>]*id=["\']boutique-refacciones["\'][\s\S]*?<\/section>', '', html_clean, flags=re.IGNORECASE)
html_clean = re.sub(r'<div[^>]*>\s*TU ALMAC[EÉ]N VIRTUAL[\s\S]*?<\/a>\s*<\/div>\s*<\/div>', '', html_clean, flags=re.IGNORECASE)

# Eliminar instancias antiguas del Carrusel de Tigre
html_clean = re.sub(r'<!--\s*SECCI[ÓO]N GARANT[ÍI]A, CALIDAD Y RESPALDO[\s\S]*?<\/section>', '', html_clean, flags=re.IGNORECASE)
html_clean = re.sub(r'<section[^>]*id=["\']garantia-calidad-tigre["\'][\s\S]*?<\/section>', '', html_clean, flags=re.IGNORECASE)
html_clean = re.sub(r'<div[^>]*class="[^"]*bg-slate-900[^"]*"[^>]*>\s*<h2[^>]*>Garant[íi]a, Calidad y Respaldo<\/h2>[\s\S]*?<\/div>\s*<\/div>\s*<\/div>', '', html_clean, flags=re.IGNORECASE)

# 3. INSERTAR 'BOUTIQUE DE REFACCIONES' JUSTO ANTES DEL CATÁLOGO DE PRODUCTOS
cat_match = re.search(r'(<!--\s*(?:CAT[ÁA]LOGO|PRODUCTOS|SECCI[ÓO]N PRINCIPAL)|\s*<main|\s*<section[^>]*id=["\'](?:catalogo|productos|filtros)["\']|\s*<div[^>]*class="[^"]*(?:max-w-7xl|container)[^"]*"[^>]*>\s*<div[^>]*class="[^"]*grid[^"]*"[^>]*>\s*<!--\s*BARRA LATERAL|\s*Navegaci[óo]n y Filtros)', html_clean, re.IGNORECASE)

if cat_match:
    pos_cat = cat_match.start()
    html_clean = html_clean[:pos_cat] + REFACCIONES_HTML + "\n\n" + html_clean[pos_cat:]
    print("✓ Boutique de Refacciones insertada en la 3ra etapa (después del Hero Carousel).")
else:
    print("Aviso: No se encontró etiqueta de catálogo, buscando contenedor alterno...")
    hero_end = html_clean.find("</header>")
    if hero_end != -1:
        html_clean = html_clean[:hero_end+9] + "\n\n" + REFACCIONES_HTML + "\n\n" + html_clean[hero_end+9:]

# 4. INSERTAR 'CARRUSEL TIGRE' ENTRE COTIZADOR Y PROGRAMA DE LEALTAD
lealtad_match = re.search(r'(<!--\s*(?:PROGRAMA DE LEALTAD|CLUB DE SOCIOS)|\s*<section[^>]*id=["\'](?:lealtad|recompensas|club)["\']|\s*<div[^>]*class="[^"]*max-w-7xl[^"]*"[^>]*>\s*<div[^>]*class="[^"]*bg-slate-900[^"]*"[^>]*>\s*<div[^>]*>\s*<span[^>]*>CLUB DE SOCIOS|\s*Programa de Lealtad &amp; Recompensas|\s*Programa de Lealtad & Recompensas)', html_clean, re.IGNORECASE)

if lealtad_match:
    pos_lealtad = lealtad_match.start()
    # Buscar apertura de etiqueta contenedora hacia atrás si coincide en texto
    tag_start = max(html_clean.rfind('<section', 0, pos_lealtad), html_clean.rfind('<div class="max-w', 0, pos_lealtad), html_clean.rfind('<div class="relative', 0, pos_lealtad))
    insert_pos = tag_start if tag_start != -1 and (pos_lealtad - tag_start < 250) else pos_lealtad
    
    html_clean = html_clean[:insert_pos] + TIGRE_HTML + "\n\n" + html_clean[insert_pos:]
    print("✓ Carrusel Tigre insertado exactamente entre Cotizador y Programa de Lealtad.")
else:
    print("Aviso: No se encontró bloque de lealtad, insertando antes del footer...")
    footer_pos = html_clean.rfind("<footer")
    if footer_pos != -1:
        html_clean = html_clean[:footer_pos] + TIGRE_HTML + "\n\n" + html_clean[footer_pos:]

with open(PC_LAB_INDEX, "w", encoding="utf-8") as f:
    f.write(html_clean)

print("\n=== DESPLEGANDO A GITHUB PAGES ===")
pc_dir = os.path.join(BASE_DIR, "pc-custom-lab")
if os.path.exists(os.path.join(pc_dir, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=pc_dir, check=True)
    subprocess.run(["git", "commit", "-m", "fix(layout): posicion exacta de refacciones (etapa 3) y carrusel tigre (entre cotizador y lealtad)", "--allow-empty"], cwd=pc_dir, capture_output=True)
    res_pc = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=pc_dir, capture_output=True, text=True)
    print(f"🟢 pc-custom-lab -> Push: {'OK' if res_pc.returncode == 0 else res_pc.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(pc-custom-lab): orden jerarquico definitivo de refacciones y carrusel tigre", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
