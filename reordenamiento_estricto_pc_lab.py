import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
PC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")
PC_LAB_INDEX = os.path.join(PC_DIR, "index.html")
IMG_DIR = os.path.join(PC_DIR, "assets", "img")

if not os.path.exists(PC_LAB_INDEX):
    print("Error: No se encontró pc-custom-lab/index.html")
    exit(1)

with open(PC_LAB_INDEX, "r", encoding="utf-8") as f:
    html = f.read()

# -------------------------------------------------------------
# 1. EXTRAER BLOQUES FUNDAMENTALES
# -------------------------------------------------------------

# Extraer Cabecera + Hero Carousel
hero_match = re.search(r'([\s\S]*?)(?=<!--\s*(?:BOUTIQUE DE REFACCIONES|TU ALMAC[EÉ]N|SECCI[ÓO]N GARANT[ÍI]A|CONFIGURADOR|CAT[ÁA]LOGO)|\s*<section[^>]*id=["\'](?:boutique-refacciones|garantia-calidad-tigre|catalogo)["\']|\s*Miles de Piezas & Refacciones)', html, re.IGNORECASE)
header_hero_part = hero_match.group(1) if hero_match else ""

# Si no capturó el inicio completo, capturar hasta el cierre del hero
if not header_hero_part or "<header" not in header_hero_part:
    idx_hero_end = html.find("</section>")
    header_hero_part = html[:idx_hero_end+10] if idx_hero_end != -1 else html[:1500]

# Extraer Bloque Catálogo (Filtros + Grid + Paginación)
cat_start = re.search(r'(<!--\s*CAT[ÁA]LOGO[\s\S]*?-->|\s*<main[\s\S]*?>|\s*<section[^>]*id=["\']catalogo["\']|\s*//\s*TIENDA PC CUSTOM LAB|\s*Cat[áa]logo de Componentes Esenciales)', html, re.IGNORECASE)
cat_block = ""
if cat_start:
    pos_c = cat_start.start()
    # Buscar hasta donde empieza el configurador o lealtad o footer
    pos_c_end = re.search(r'(<!--\s*(?:CONFIGURADOR|PROGRAMA DE LEALTAD|SECCI[ÓO]N GARANT[ÍI]A)|\s*<section[^>]*id=["\'](?:configurador|lealtad|garantia)["\']|\s*CONFIGURADOR MATRIZ|\s*Configura tu Equipo Paso a Paso|\s*<footer)', html[pos_c:], re.IGNORECASE)
    if pos_c_end:
        cat_block = html[pos_c : pos_c + pos_c_end.start()]
    else:
        cat_block = html[pos_c:]

# Extraer Bloque Configurador / Cotizador
cfg_start = re.search(r'(<!--\s*CONFIGURADOR[\s\S]*?-->|\s*<section[^>]*id=["\']configurador["\']|\s*CONFIGURADOR MATRIZ|\s*Configura tu Equipo Paso a Paso)', html, re.IGNORECASE)
cfg_block = ""
if cfg_start:
    pos_cfg = cfg_start.start()
    pos_cfg_end = re.search(r'(<!--\s*(?:PROGRAMA DE LEALTAD|SECCI[ÓO]N GARANT[ÍI]A|CAT[ÁA]LOGO)|\s*<section[^>]*id=["\'](?:lealtad|garantia|catalogo)["\']|\s*CLUB DE SOCIOS|\s*Programa de Lealtad|\s*<footer)', html[pos_cfg:], re.IGNORECASE)
    if pos_cfg_end:
        cfg_block = html[pos_cfg : pos_cfg + pos_cfg_end.start()]
    else:
        cfg_block = html[pos_cfg:]

# Extraer Bloque Lealtad
lea_start = re.search(r'(<!--\s*PROGRAMA DE LEALTAD[\s\S]*?-->|\s*<section[^>]*id=["\']lealtad["\']|\s*CLUB DE SOCIOS PC CUSTOM LAB|\s*Programa de Lealtad &amp; Recompensas|\s*Programa de Lealtad & Recompensas)', html, re.IGNORECASE)
lea_block = ""
if lea_start:
    pos_l = lea_start.start()
    # Retroceder al contenedor <section o <div
    tag_s = max(html.rfind('<section', 0, pos_l), html.rfind('<div class="max-w', 0, pos_l), html.rfind('<div class="relative', 0, pos_l))
    if tag_s != -1 and (pos_l - tag_s < 300):
        pos_l = tag_s
    pos_l_end = re.search(r'(<!--\s*(?:CAT[ÁA]LOGO|FOOTER)|\s*<section[^>]*id=["\']catalogo["\']|\s*<footer|\s*//\s*TIENDA PC CUSTOM LAB)', html[pos_l:], re.IGNORECASE)
    if pos_l_end:
        lea_block = html[pos_l : pos_l + pos_l_end.start()]
    else:
        lea_block = html[pos_l:]

# Extraer scripts finales y cierre
scripts_match = re.search(r'(<script[\s\S]*<\/html>)', html, re.IGNORECASE)
scripts_part = scripts_match.group(1) if scripts_match else "</body></html>"

# -------------------------------------------------------------
# 2. CONSTRUCCIÓN DE COMPONENTES ESTANDARIZADOS
# -------------------------------------------------------------

REFACCIONES_SECTION = """
    <!-- 3. BOUTIQUE DE REFACCIONES (INMEDIATAMENTE DEBAJO DEL CARRUSEL DE BIENVENIDA) -->
    <section class="py-10 bg-slate-900 border-y border-slate-800 text-center relative overflow-hidden" id="boutique-refacciones">
        <div class="max-w-5xl mx-auto px-4 relative z-10">
            <span class="text-[10px] sm:text-[11px] font-mono font-bold uppercase tracking-widest text-amber-400 bg-amber-400/10 px-3 py-1 rounded-full border border-amber-400/30 inline-block mb-2">Tu almacén virtual: Catálogo Inmenso</span>
            <h2 class="text-2xl sm:text-4xl font-black text-white tracking-tight mb-2">Miles de Piezas & Refacciones Sueltas</h2>
            <p class="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto mb-5">Accede a componentes de oportunidad al mejor precio de mayoreo y entrega inmediata.</p>
            <a href="#catalogo" class="inline-flex items-center gap-2 px-7 py-3 bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-xs uppercase tracking-wider rounded-xl shadow-lg transition active:scale-95">
                <i class="fa-solid fa-microchip"></i> Explorar Boutique de Refacciones
            </a>
        </div>
    </section>
"""

# Galería de 16 tigres adaptada para pantallas grandes y móviles
tiger_images = []
if os.path.exists(IMG_DIR):
    for f in sorted(os.listdir(IMG_DIR)):
        if f.lower().endswith(('.webp', '.png', '.jpg', '.jpeg')) and any(k in f.lower() for k in ['slider', 'ia', 'tiger', 'tigre', 'human', 'mascota', 'tech', 'custom']):
            tiger_images.append(f"assets/img/{f}")

if not tiger_images:
    tiger_images = ["assets/img/slider_ia_human_thumb.webp"]
while len(tiger_images) < 16:
    tiger_images += list(tiger_images)
tiger_images = tiger_images[:16]

slogans = [
    ("Muro de Marcas Global", "Componentes certificados con soporte oficial de fabricantes."),
    ("Periféricos & Accesorios", "Diseño ergonómico y alta precisión para setups profesionales."),
    ("PC Custom Lab | Tech Service", "Calidad corporativa certificada con pruebas de estrés exhaustivas."),
    ("Honestidad y Servicio", "Atención técnica especializada y garantía directa en Guadalajara."),
    ("Potencia y Rendimiento", "Hardware de última generación para gaming y estaciones de trabajo."),
    ("Asesoría Profesional", "Atención personalizada para armar el equipo ideal a tu medida."),
    ("Calidad Certificada", "Cada pieza inspeccionada rigurosamente antes de entrega."),
    ("Entrega Inmediata", "Disponibilidad de componentes y refacciones en tienda física."),
    ("Máxima Estabilidad", "Fuentes de poder y enfriamiento líquido de alto desempeño."),
    ("Soporte Técnico Directo", "Mantenimiento preventivo y correctivo especializado."),
    ("Innovación Tecnológica", "Equipos preparados para renderizado, diseño y streaming."),
    ("Confianza Total", "Compra protegida y respaldo directo en Pedro Moreno 501 A."),
    ("Ensambles Personalizados", "Diseñados acorde a tu presupuesto y necesidades."),
    ("Atención y Rapidez", "Pedidos procesados con máxima agilidad en el ecosistema."),
    ("Mascota Oficial PC Custom", "Tu aliada en el mundo del hardware y alto rendimiento."),
    ("Club de Beneficios", "5% de cashback acumulable y promociones exclusivas.")
]

cards_html = ""
for idx, img_src in enumerate(tiger_images):
    titulo, desc = slogans[idx % len(slogans)]
    color_tag = "text-cyan-400" if idx % 3 == 0 else ("text-emerald-400" if idx % 3 == 1 else "text-amber-400")
    cards_html += f"""
        <div class="w-[220px] sm:w-[260px] md:w-[290px] bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden p-3.5 flex flex-col items-center text-center shrink-0 shadow-xl group hover:border-slate-700 transition duration-300">
            <div class="w-full h-36 sm:h-44 md:h-48 rounded-xl overflow-hidden bg-slate-950 mb-3 border border-slate-800/80 flex items-center justify-center">
                <img src="{img_src}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" alt="{titulo}" onerror="this.onerror=null;this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp';" />
            </div>
            <span class="text-[11px] font-black {color_tag} uppercase font-mono tracking-wider line-clamp-1">{titulo}</span>
            <p class="text-[10px] text-slate-400 mt-1 line-clamp-2 leading-relaxed">{desc}</p>
        </div>
    """

TIGRES_SECTION = f"""
    <!-- 6. CARRUSEL TIGRES (GARANTÍA, CALIDAD Y RESPALDO: ENTRE COTIZADOR Y LEALTAD) -->
    <section class="py-14 bg-slate-950 border-t border-slate-900 overflow-hidden relative" id="garantia-calidad-tigre">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center mb-6">
            <span class="text-[10px] font-mono text-cyan-400 uppercase tracking-widest bg-cyan-500/10 px-3 py-1 rounded-full border border-cyan-500/30 font-bold inline-block mb-2">PC CUSTOM LAB & TECH SERVICE</span>
            <h2 class="text-xl sm:text-3xl font-black text-white tracking-tight">Garantía, Calidad y Respaldo</h2>
            <p class="text-xs text-slate-400 max-w-xl mx-auto mt-1.5">Conoce a nuestra mascota y los pilares que respaldan cada uno de nuestros ensambles y servicios técnicos.</p>
        </div>

        <div class="relative w-full overflow-hidden select-none py-2">
            <div class="tigre-infinite-track flex gap-4 sm:gap-6 w-max">
                {cards_html + cards_html}
            </div>
        </div>

        <style>
            @keyframes tigreFlow {{
                0% {{ transform: translateX(0); }}
                100% {{ transform: translateX(-50%); }}
            }}
            .tigre-infinite-track {{
                animation: tigreFlow 24s linear infinite;
                will-change: transform;
            }}
            .tigre-infinite-track:hover {{
                animation-play-state: paused;
            }}
        </style>
    </section>
"""

FOOTER_SECTION = """
    <!-- 8. FOOTER UNIVERSAL (3 COLUMNAS) -->
    <footer class="bg-slate-950 border-t border-slate-900 pt-16 pb-8 text-slate-400 text-xs mt-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 pb-12 border-b border-slate-800/80">
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-location-dot text-amber-400"></i> Contacto Local
                    </h4>
                    <p class="flex items-start gap-2 text-slate-300">
                        <i class="fa-solid fa-map-pin text-slate-500 mt-0.5 shrink-0"></i>
                        <span>Pedro Moreno 501 A, Guadalajara Centro, Jalisco (CP 44100)</span>
                    </p>
                    <p class="flex items-center gap-2">
                        <i class="fa-solid fa-phone text-cyan-400 shrink-0"></i>
                        <span>Teléfono Fijo: <a href="tel:3336136348" class="text-slate-200 hover:text-cyan-400 font-mono">(33) 3613 6348</a></span>
                    </p>
                    <p class="flex items-center gap-2">
                        <i class="fa-brands fa-whatsapp text-emerald-400 shrink-0 text-sm"></i>
                        <span>WhatsApp: <a href="https://wa.me/523337271440" target="_blank" rel="noopener" class="text-slate-200 hover:text-emerald-400 font-mono">+52 33 3727 1440</a></span>
                    </p>
                    <div class="flex flex-col gap-1.5 pt-2 border-t border-slate-900 text-[11px] text-slate-400">
                        <a href="https://www.facebook.com/profile.php?id=61593020515115" target="_blank" rel="noopener" class="hover:text-blue-400 transition flex items-center gap-2">
                            <i class="fa-brands fa-facebook text-blue-500 w-4 text-center"></i> Facebook: PC Custom Lab
                        </a>
                        <a href="https://www.instagram.com/pccustomlab/" target="_blank" rel="noopener" class="hover:text-pink-400 transition flex items-center gap-2">
                            <i class="fa-brands fa-instagram text-pink-500 w-4 text-center"></i> Instagram: @pccustomlab
                        </a>
                        <a href="https://www.youtube.com/@IAWorldCenter" target="_blank" rel="noopener" class="hover:text-red-400 transition flex items-center gap-2">
                            <i class="fa-brands fa-youtube text-red-500 w-4 text-center"></i> YouTube: IA World Center
                        </a>
                        <a href="https://t.me/pc_custom_lab" target="_blank" rel="noopener" class="hover:text-cyan-400 transition flex items-center gap-2">
                            <i class="fa-brands fa-telegram text-cyan-400 w-4 text-center"></i> Telegram: pc_custom_lab
                        </a>
                        <a href="mailto:iaworldcenter@gmail.com" class="hover:text-amber-400 transition flex items-center gap-2">
                            <i class="fa-solid fa-envelope text-amber-400 w-4 text-center"></i> Correo: iaworldcenter@gmail.com
                        </a>
                    </div>
                </div>

                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-shield-halved text-cyan-400"></i> Políticas de Compra
                    </h4>
                    <div class="flex items-start gap-2.5">
                        <i class="fa-solid fa-rotate-left text-amber-400 mt-1 shrink-0"></i>
                        <div>
                            <strong class="text-slate-200 block text-xs">Devoluciones Directas:</strong>
                            <span class="text-slate-400 text-[11px] leading-relaxed">Permitidas físicamente en tienda dentro de las primeras 48 horas con empaque íntegro.</span>
                        </div>
                    </div>
                    <div class="flex items-start gap-2.5">
                        <i class="fa-solid fa-certificate text-emerald-400 mt-1 shrink-0"></i>
                        <div>
                            <strong class="text-slate-200 block text-xs">Garantía Certificada:</strong>
                            <span class="text-slate-400 text-[11px] leading-relaxed">Productos de calidad garantizada con soporte técnico local y reemplazo inmediato.</span>
                        </div>
                    </div>
                    <div class="flex items-start gap-2.5">
                        <i class="fa-solid fa-cookie-bite text-slate-500 mt-1 shrink-0"></i>
                        <div>
                            <strong class="text-slate-200 block text-xs">Políticas de Cookies:</strong>
                            <span class="text-slate-400 text-[11px] leading-relaxed">Usadas exclusivamente para mantener activa la sesión de tu carrito y mejorar el servicio.</span>
                        </div>
                    </div>
                </div>

                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-coins text-emerald-400"></i> Ahorro y Cashback
                    </h4>
                    <p class="text-slate-300 font-bold flex items-center gap-2">
                        <i class="fa-solid fa-piggy-bank text-amber-400 text-base shrink-0"></i>
                        <span>5% de Cashback en cada compra de forma directa.</span>
                    </p>
                    <p class="text-[11px] text-slate-400 leading-relaxed bg-slate-900/60 p-3 rounded-xl border border-slate-800/80">
                        <strong class="text-slate-300 block mb-1">Aclaración Importante:</strong>
                        El cashback es acumulable únicamente con registro activo. Regístrate en nuestro portal para recibir beneficios acumulados y ofertas exclusivas.
                    </p>
                    <div class="pt-2 text-[10px] font-mono text-slate-500 flex items-center gap-2">
                        <i class="fa-solid fa-robot text-cyan-400"></i>
                        <span>Potenciado por el software de Anti-Gravity Copilot.</span>
                    </div>
                </div>
            </div>

            <div class="pt-8 text-center text-slate-500 text-[11px]">
                <p>&copy; 2026 PC Custom Lab. Pedro Moreno 501 A, Guadalajara Centro. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>
"""

# -------------------------------------------------------------
# 3. ENSAMBLAJE EN EL ORDEN EXACTO
# -------------------------------------------------------------
# Asegurar ID en el contenedor del catálogo para el salto del botón amarillo
if 'id="catalogo"' not in cat_block:
    cat_block = re.sub(r'(<main[^>]*|<section[^>]*class="[^"]*(?:py-|max-w)[^"]*"[^>]*)', r'\1 id="catalogo"', cat_block, count=1)

# Limpiar posibles restos de tigres o refacciones dentro de los bloques extraídos
cat_block = re.sub(r'<!--\s*(?:BOUTIQUE DE REFACCIONES|SECCI[ÓO]N GARANT[ÍI]A)[\s\S]*?<\/section>', '', cat_block, flags=re.IGNORECASE)
cat_block = re.sub(r'<section[^>]*id=["\'](?:boutique-refacciones|garantia-calidad-tigre)["\'][\s\S]*?<\/section>', '', cat_block, flags=re.IGNORECASE)

cfg_block = re.sub(r'<!--\s*(?:BOUTIQUE DE REFACCIONES|SECCI[ÓO]N GARANT[ÍI]A)[\s\S]*?<\/section>', '', cfg_block, flags=re.IGNORECASE)
cfg_block = re.sub(r'<section[^>]*id=["\'](?:boutique-refacciones|garantia-calidad-tigre)["\'][\s\S]*?<\/section>', '', cfg_block, flags=re.IGNORECASE)

lea_block = re.sub(r'<!--\s*(?:BOUTIQUE DE REFACCIONES|SECCI[ÓO]N GARANT[ÍI]A)[\s\S]*?<\/section>', '', lea_block, flags=re.IGNORECASE)
lea_block = re.sub(r'<section[^>]*id=["\'](?:boutique-refacciones|garantia-calidad-tigre)["\'][\s\S]*?<\/section>', '', lea_block, flags=re.IGNORECASE)

FINAL_HTML = f"""{header_hero_part.strip()}

{REFACCIONES_SECTION.strip()}

{cat_block.strip()}

{cfg_block.strip()}

{TIGRES_SECTION.strip()}

{lea_block.strip()}

{FOOTER_SECTION.strip()}

{scripts_part.strip()}
"""

with open(PC_LAB_INDEX, "w", encoding="utf-8") as f:
    f.write(FINAL_HTML)

print("✓ pc-custom-lab/index.html reensamblado en el orden estricto:")
print("  1. Header + Hero Carousel")
print("  2. Boutique de Refacciones (Banner amarillo)")
print("  3. Catálogo de Componentes Esenciales (Filtros + Grid + Paginación)")
print("  4. Configurador / Cotizador de PC")
print("  5. Carrusel de los 16 Tigres (Garantía, Calidad y Respaldo)")
print("  6. Programa de Lealtad (Club de Socios)")
print("  7. Footer Universal (3 Columnas)")

# -------------------------------------------------------------
# 4. DESPLIEGUE A GITHUB
# -------------------------------------------------------------
print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(PC_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=PC_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "fix(layout): orden estricto y definitivo de 7 secciones en pc-custom-lab", "--allow-empty"], cwd=PC_DIR, capture_output=True)
    res_pc = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=PC_DIR, capture_output=True, text=True)
    print(f"🟢 pc-custom-lab -> Push: {'OK' if res_pc.returncode == 0 else res_pc.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(pc-custom-lab): reordenamiento definitivo sin duplicados", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
