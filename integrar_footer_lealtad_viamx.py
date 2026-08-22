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
print("INTEGRANDO SECCIÓN DE LEALTAD Y FOOTER UNIVERSAL DE 3 COLUMNAS EN VÍA MX")
print("=" * 70)

# 1. Sección de Lealtad y Recompensas (Club de Socios Vía MX con espacio de video)
SECCION_LEALTAD_HTML = """
    <!-- ========================================================================
         PROGRAMA DE LEALTAD & RECOMPENSAS (CLUB DE SOCIOS VÍAMX)
         ======================================================================== -->
    <section class="py-16 bg-slate-900/60 border-t border-slate-800 overflow-hidden" id="lealtad">
        <div class="max-w-7xl mx-auto px-4 sm:px-6">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
                
                <!-- Contenedor reservado para Video / Media -->
                <div class="lg:col-span-5 flex flex-col items-center text-center">
                    <div class="relative w-72 h-72 sm:w-[352px] sm:h-[352px] rounded-3xl overflow-hidden border border-slate-800 shadow-2xl bg-slate-950">
                        <div class="w-full h-full object-cover overflow-hidden" id="video-container-viamx">
                            <img src="assets/img/mascota_tigre_thumb.webp" alt="Club de Socios Vía MX" class="w-full h-full object-cover rounded-2xl" loading="lazy" decoding="async" width="352" height="352" />
                        </div>
                        <div class="absolute bottom-0 inset-x-0 bg-slate-950/85 border-t border-slate-800 p-3 z-10">
                            <span class="text-[10px] text-slate-400 font-mono tracking-wider">
                                <i class="fa-solid fa-wand-magic-sparkles text-cyan-400 mr-1"></i> Ecosistema Anti-Gravity & Vía MX
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Formulario de Suscripción / Acumulación de Cashback -->
                <div class="lg:col-span-7 space-y-6 text-left">
                    <span class="px-3.5 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 font-mono text-xs uppercase tracking-widest inline-block">
                        Club de Socios Vía MX
                    </span>
                    <h2 class="text-3xl sm:text-4xl font-black text-white leading-tight">
                        Programa de Lealtad & Recompensas
                    </h2>
                    <p class="text-slate-300 text-sm sm:text-base leading-relaxed">
                        Recibe recompensas exclusivas, acceso prioritario a oportunidades de importación y regalos sorpresa. Para acumular y validar tu <strong>5% de Cashback</strong> en cada compra, es requisito mantener activa tu suscripción a nuestra newsletter.
                    </p>
                    <form class="bg-slate-950/90 border border-slate-800 rounded-3xl p-6 sm:p-7 space-y-4 shadow-2xl" id="form-lealtad-viamx" onsubmit="registrarLealtadViamx(event)">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label for="lealtad-email" class="block text-xs font-mono text-slate-400 mb-1.5 uppercase font-bold">Correo Electrónico</label>
                                <input aria-label="Correo electrónico para lealtad" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-cyan-500" id="lealtad-email" placeholder="correo@ejemplo.com" required="" type="email"/>
                            </div>
                            <div>
                                <label for="lealtad-phone" class="block text-xs font-mono text-slate-400 mb-1.5 uppercase font-bold">WhatsApp</label>
                                <input aria-label="WhatsApp para lealtad" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-cyan-500" id="lealtad-phone" placeholder="33 3727 1440" required="" type="tel"/>
                            </div>
                        </div>
                        <button class="w-full bg-gradient-to-r from-amber-400 via-amber-500 to-yellow-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black py-3.5 rounded-xl text-sm transition shadow-lg active:scale-95 cursor-pointer flex items-center justify-center gap-2" type="submit">
                            <i class="fa-solid fa-user-plus"></i> Registrarme y Acumular Cashback (5%)
                        </button>
                    </form>
                </div>

            </div>
        </div>
    </section>
"""

# 2. Footer Universal de 3 Columnas Homologado
FOOTER_3_COLUMNAS_HTML = """
    <!-- ========================================================================
         FOOTER UNIVERSAL HOMOLOGADO (3 COLUMNAS)
         ======================================================================== -->
    <footer class="bg-slate-950 border-t border-slate-900 pt-16 pb-8 text-slate-400 text-xs">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 pb-12 border-b border-slate-800/80">
                
                <!-- COLUMNA 1: CONTACTO LOCAL -->
                <div class="flex flex-col gap-3">
                    <h3 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-location-dot text-amber-400"></i> Contacto Local
                    </h3>
                    <p class="flex items-start gap-2 text-slate-300">
                        <i class="fa-solid fa-map-pin text-slate-400 mt-0.5 shrink-0"></i>
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
                            <i class="fa-brands fa-facebook text-blue-500 w-4 text-center"></i> Facebook: Vía MX Curaduría
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
                    <h3 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-shield-halved text-cyan-400"></i> Políticas de Compra
                    </h3>
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
                        <i class="fa-solid fa-cookie-bite text-slate-400 mt-1 shrink-0"></i>
                        <div>
                            <strong class="text-slate-200 block text-xs">Políticas de Cookies:</strong>
                            <span class="text-slate-400 text-[11px] leading-relaxed">Usadas exclusivamente para mantener activa la sesión de tu carrito y mejorar el servicio.</span>
                        </div>
                    </div>
                </div>

                <!-- COLUMNA 3: AHORRO Y CASHBACK -->
                <div class="flex flex-col gap-3">
                    <h3 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-coins text-emerald-400"></i> Ahorro y Cashback
                    </h3>
                    <p class="text-slate-300 font-bold flex items-center gap-2">
                        <i class="fa-solid fa-piggy-bank text-amber-400 text-base shrink-0"></i>
                        <span>5% de Cashback en cada compra de forma directa.</span>
                    </p>
                    <p class="text-[11px] text-slate-400 leading-relaxed bg-slate-900/60 p-3 rounded-xl border border-slate-800/80">
                        <strong class="text-slate-300 block mb-1">Aclaración Importante:</strong>
                        El cashback es acumulable únicamente con registro activo. Si quieres obtener cashback, tienes que mantener tu suscripción a nuestra newsletter activa. Regístrate en nuestro portal para recibir beneficios acumulados y ofertas exclusivas.
                    </p>
                    <div class="pt-2 text-[10px] font-mono text-slate-400 flex items-center gap-2">
                        <i class="fa-solid fa-robot text-cyan-400"></i>
                        <span>Potenciado por el software de Anti-Gravity Copilot.</span>
                    </div>
                </div>

            </div>

            <!-- COPYRIGHT INFERIOR -->
            <div class="pt-8 text-center text-slate-400 text-[11px] flex flex-col sm:flex-row items-center justify-between gap-4">
                <div class="flex items-center gap-2">
                    <img src="assets/img/mascota_tigre_thumb.webp" alt="Vía MX" width="20" height="20" class="rounded-full">
                    <span class="text-white font-bold">Vía MX Curaduría Internacional</span>
                </div>
                <p>© 2026 Vía MX — Ecosistema Anti-Gravity & Alfa. Pedro Moreno 501 A, Guadalajara Centro. Todos los derechos reservados.</p>
                <div class="flex items-center gap-4 text-slate-300">
                    <a href="checkout.html" class="hover:text-cyan-400">Checkout</a>
                    <span>•</span>
                    <a href="https://iaworldcenter-creator.github.io/sitios-web/" class="hover:text-cyan-400">Portal Central</a>
                </div>
            </div>
        </div>
    </footer>
"""

# Reemplazar la etiqueta <footer> previa con la Sección de Lealtad + Nuevo Footer
pattern_footer = re.compile(r'(?:<section id="lealtad"[\s\S]*?<\/section>\s*)?<footer[\s\S]*?<\/footer>', re.IGNORECASE)

if pattern_footer.search(html):
    html = pattern_footer.sub(f"{SECCION_LEALTAD_HTML.strip()}\n\n{FOOTER_3_COLUMNAS_HTML.strip()}", html, count=1)
else:
    main_end = html.find("</main>")
    if main_end != -1:
        html = html[:main_end + 7] + "\n\n" + SECCION_LEALTAD_HTML.strip() + "\n\n" + FOOTER_3_COLUMNAS_HTML.strip() + "\n\n" + html[main_end + 7:]

# Asegurar la función de registro de lealtad en el JavaScript
if "function registrarLealtadViamx" not in html:
    loyalty_script = """
    function registrarLealtadViamx(event) {
        event.preventDefault();
        const email = document.getElementById('lealtad-email').value;
        const phone = document.getElementById('lealtad-phone').value;
        alert(`¡Registro en Vía MX exitoso!\\nCorreo: ${email}\\nWhatsApp: ${phone}\\nTu suscripción a la newsletter ha quedado activa para acumular el 5% de Cashback.`);
        document.getElementById('form-lealtad-viamx').reset();
    }
    """
    html = html.replace("</script>\n</body>", f"{loyalty_script}\n    </script>\n</body>")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("✓ Sección de Lealtad y Footer de 3 Columnas integrados con éxito en index.html")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(footer): programa de lealtad Via MX con cashback y footer homologado de 3 columnas", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(viamx): seccion de lealtad, politicas y contacto 3 columnas desplegado", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
