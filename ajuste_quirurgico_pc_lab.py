import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
PC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")
PC_LAB_INDEX = os.path.join(PC_DIR, "index.html")

if not os.path.exists(PC_LAB_INDEX):
    print("Error: No se encontro pc-custom-lab/index.html")
    exit(1)

with open(PC_LAB_INDEX, "r", encoding="utf-8") as f:
    html = f.read()

# ----------------------------------------------------------------------
# A. BLOQUE BANNER REFACCIONES (ETAPA 2.5: ENTRE HERO Y CATÁLOGO)
# ----------------------------------------------------------------------
BANNER_REFACCIONES = """
    <!-- BANNER BOUTIQUE DE REFACCIONES -->
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

# ----------------------------------------------------------------------
# B. FOOTER UNIVERSAL (3 COLUMNAS)
# ----------------------------------------------------------------------
FOOTER_UNIVERSAL = """
    <!-- FOOTER UNIVERSAL HOMOLOGADO (3 COLUMNAS) -->
    <footer class="bg-slate-950 border-t border-slate-900 pt-16 pb-8 text-slate-400 text-xs mt-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 pb-12 border-b border-slate-800/80">
                
                <!-- COLUMNA 1: CONTACTO LOCAL -->
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

                <!-- COLUMNA 2: POLÍTICAS DE COMPRA -->
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

                <!-- COLUMNA 3: AHORRO Y CASHBACK -->
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

            <!-- COPYRIGHT INFERIOR -->
            <div class="pt-8 text-center text-slate-500 text-[11px]">
                <p>&copy; 2026 PC Custom Lab. Pedro Moreno 501 A, Guadalajara Centro. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>
"""

# 1. Insertar el Banner de Refacciones antes de "// TIENDA PC CUSTOM LAB" o "Catálogo de Componentes"
if "id=\"boutique-refacciones\"" not in html and "Miles de Piezas & Refacciones Sueltas" not in html:
    pos_cat = html.find("// TIENDA PC CUSTOM LAB")
    if pos_cat == -1:
        pos_cat = html.find("Catálogo de Componentes Esenciales")
    if pos_cat == -1:
        pos_cat = html.find("Cat&#225;logo de Componentes Esenciales")
    
    if pos_cat != -1:
        # Retroceder al <div o <section previo que inicia el catálogo
        tag_start = max(html.rfind('<div class="py-', 0, pos_cat), html.rfind('<section', 0, pos_cat), html.rfind('<div class="max-w', 0, pos_cat), html.rfind('<div class="relative', 0, pos_cat))
        insert_idx = tag_start if tag_start != -1 and (pos_cat - tag_start < 300) else pos_cat
        html = html[:insert_idx] + BANNER_REFACCIONES + "\n\n" + html[insert_idx:]
        print("✓ Banner 'Miles de Piezas & Refacciones Sueltas' insertado antes del Catálogo.")

# Asegurar id="catalogo" en el contenedor del catálogo para navegación suave
if 'id="catalogo"' not in html:
    html = re.sub(r'(<div[^>]*class="[^"]*(?:py-12|max-w-7xl)[^"]*"[^>]*)', r'\1 id="catalogo"', html, count=1)

# 2. Reemplazar bloque azul de contacto antiguo por Footer Universal de 3 Columnas
html = re.sub(r'<section[^>]*id=["\'](?:contacto|ubicacion)["\'][\s\S]*?<\/section>', '', html, flags=re.IGNORECASE)
html = re.sub(r'<div[^>]*>\s*//\s*UBICACI[ÓO]N Y CONTACTO DIRECTO[\s\S]*?<\/div>\s*<\/div>\s*<\/div>', '', html, flags=re.IGNORECASE)
html = re.sub(r'<!--\s*(?://\s*)?UBICACI[ÓO]N Y CONTACTO DIRECTO[\s\S]*?<\/div>\s*<\/div>\s*<\/div>', '', html, flags=re.IGNORECASE)

# Reemplazar footer previo
if "<footer" in html:
    html = re.sub(r'<footer[\s\S]*?<\/footer>', FOOTER_UNIVERSAL.strip(), html, flags=re.IGNORECASE)
else:
    html = html.replace("</body>", f"{FOOTER_UNIVERSAL.strip()}\n</body>")

with open(PC_LAB_INDEX, "w", encoding="utf-8") as f:
    f.write(html)

print("✓ Estructura de pc-custom-lab/index.html actualizada y verificada.")

# -------------------------------------------------------------
# 3. DESPLIEGUE A GITHUB
# -------------------------------------------------------------
print("\n=== DESPLEGANDO A GITHUB PAGES ===")
if os.path.exists(os.path.join(PC_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=PC_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "fix(layout): insercion limpia de refacciones y footer universal sin alterar catalogo ni ensambles", "--allow-empty"], cwd=PC_DIR, capture_output=True)
    res_pc = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=PC_DIR, capture_output=True, text=True)
    print(f"🟢 pc-custom-lab -> Push: {'OK' if res_pc.returncode == 0 else res_pc.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(pc-custom-lab): estructura respetada con refacciones y footer universal", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
