import os
import subprocess
import re

BASE_DIR = r"E:\sitios web"

print("=" * 80)
print("HOMOLOGANDO PIE DE PÁGINA CON REDES SOCIALES Y CONTACTO COMPLETO EN LOS 8 SITIOS")
print("=" * 80)

# MÓDULO UNIVERSAL DEL PIE DE PÁGINA COMPLETO
FOOTER_HTML = """
    <footer class="bg-slate-950 border-t border-slate-900 pt-16 pb-8 text-slate-400 text-xs" id="pie-de-pagina">
        <div class="max-w-[99%] 2xl:max-w-[1850px] mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 pb-12 border-b border-slate-800/80">
                
                <!-- Columna 1: Contacto Local y Redes Sociales Completas -->
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-location-dot text-amber-400"></i> Contacto y Redes Oficiales
                    </h4>
                    <p class="flex items-start gap-2 text-slate-300">
                        <i class="fa-solid fa-map-pin text-slate-500 mt-0.5 shrink-0"></i>
                        <span>Pedro Moreno 501 A, Guadalajara Centro, Jalisco (CP 44100)</span>
                    </p>
                    <p class="flex items-center gap-2">
                        <i class="fa-solid fa-phone text-cyan-400 shrink-0"></i>
                        <span>Teléfono Fijo: <a href="tel:3336136348" class="text-slate-200 hover:text-cyan-400 font-mono font-bold">(33) 3613 6348</a></span>
                    </p>
                    <p class="flex items-center gap-2">
                        <i class="fa-brands fa-whatsapp text-emerald-400 shrink-0 text-sm"></i>
                        <span>WhatsApp: <a href="https://wa.me/523337271440" target="_blank" rel="noopener" class="text-slate-200 hover:text-emerald-400 font-mono font-bold">+52 33 3727 1440</a></span>
                    </p>
                    
                    <!-- Enlaces a Redes Sociales y Canales -->
                    <div class="flex flex-col gap-2 pt-2 border-t border-slate-900 text-[11px] text-slate-400">
                        <a href="https://www.facebook.com/profile.php?id=61593020515115" target="_blank" rel="noopener" class="hover:text-blue-400 transition flex items-center gap-2 font-medium">
                            <i class="fa-brands fa-facebook text-blue-500 w-4 text-center text-sm"></i> <span>Facebook: BAZAR NFL.GDL</span>
                        </a>
                        <a href="https://www.instagram.com/pccustomlab/" target="_blank" rel="noopener" class="hover:text-pink-400 transition flex items-center gap-2 font-medium">
                            <i class="fa-brands fa-instagram text-pink-500 w-4 text-center text-sm"></i> <span>Instagram: @pccustomlab</span>
                        </a>
                        <a href="https://www.youtube.com/@IAWorldCenter" target="_blank" rel="noopener" class="hover:text-red-400 transition flex items-center gap-2 font-medium">
                            <i class="fa-brands fa-youtube text-red-500 w-4 text-center text-sm"></i> <span>YouTube: IA World Center</span>
                        </a>
                        <a href="https://t.me/pc_custom_lab" target="_blank" rel="noopener" class="hover:text-cyan-400 transition flex items-center gap-2 font-medium">
                            <i class="fa-brands fa-telegram text-cyan-400 w-4 text-center text-sm"></i> <span>Telegram: pc_custom_lab</span>
                        </a>
                        <a href="mailto:iaworldcenter@gmail.com" class="hover:text-amber-400 transition flex items-center gap-2 font-medium">
                            <i class="fa-solid fa-envelope text-amber-400 w-4 text-center text-sm"></i> <span>Correo: iaworldcenter@gmail.com</span>
                        </a>
                    </div>
                </div>

                <!-- Columna 2: Políticas y Garantías -->
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-shield-halved text-cyan-400"></i> Políticas de Compra
                    </h4>
                    <div class="flex items-start gap-2.5">
                        <i class="fa-solid fa-rotate-left text-amber-400 mt-1 shrink-0"></i>
                        <div>
                            <strong class="text-slate-200 block text-xs font-bold">Devoluciones Directas:</strong>
                            <span class="text-slate-400 text-[11px] leading-relaxed">Permitidas en tienda dentro de las 48 horas con empaque íntegro.</span>
                        </div>
                    </div>
                    <div class="flex items-start gap-2.5">
                        <i class="fa-solid fa-certificate text-emerald-400 mt-1 shrink-0"></i>
                        <div>
                            <strong class="text-slate-200 block text-xs font-bold">Garantía Certificada:</strong>
                            <span class="text-slate-400 text-[11px] leading-relaxed">Calidad garantizada con soporte técnico local y reemplazo inmediato en Guadalajara.</span>
                        </div>
                    </div>
                    <div class="flex items-start gap-2.5">
                        <i class="fa-solid fa-cookie-bite text-slate-500 mt-1 shrink-0"></i>
                        <div>
                            <strong class="text-slate-200 block text-xs font-bold">Políticas de Cookies:</strong>
                            <span class="text-slate-400 text-[11px] leading-relaxed">Usadas exclusivamente para mantener activa la sesión y los artículos de tu carrito unificado.</span>
                        </div>
                    </div>
                </div>

                <!-- Columna 3: Ahorro, Cashback y Despacho Uber Flash -->
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-coins text-emerald-400"></i> Ahorro y Despacho Local
                    </h4>
                    <p class="text-slate-300 font-bold flex items-center gap-2 text-xs">
                        <i class="fa-solid fa-piggy-bank text-amber-400 text-base shrink-0"></i>
                        <span>5% de Cashback acumulable en cada compra.</span>
                    </p>
                    <p class="text-[11px] text-slate-400 leading-relaxed bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                        <strong class="text-slate-300 block mb-1 font-bold">Despacho Exprés con PIN de Seguridad:</strong>
                        Entregas locales el mismo día vía Uber Flash con código PIN obligatorio de entrega para proteger tu paquete.
                    </p>
                    <div class="pt-2 text-[10px] font-mono text-slate-500 flex items-center gap-2">
                        <i class="fa-solid fa-robot text-cyan-400"></i>
                        <span>Potenciado por Google Gemini AI & Anti-Gravity Copilot.</span>
                    </div>
                </div>

            </div>

            <div class="pt-8 text-center text-slate-500 text-[11px]">
                <p>&copy; 2026 Ecosistema Comercial BAZAR NFL.GDL & Pedro Moreno 501 A. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>
"""

def update_footer_in_file(file_path):
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Reemplazar cualquier <footer ... </footer> existente
    footer_pattern = re.compile(r'<footer[\s\S]*?</footer>', re.IGNORECASE)
    if footer_pattern.search(content):
        new_content = footer_pattern.sub(FOOTER_HTML.strip(), content)
    else:
        # Si no tiene footer, insertarlo antes de los scripts o de </body>
        if "<script" in content:
            idx = content.find("<script")
            new_content = content[:idx] + FOOTER_HTML.strip() + "\n\n    " + content[idx:]
        else:
            new_content = content.replace("</body>", FOOTER_HTML.strip() + "\n</body>")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True

# 1. Actualizar Portal Matriz (raíz y submódulo sitios-web)
portal_files = [
    os.path.join(BASE_DIR, "index.html"),
    os.path.join(BASE_DIR, "sitios-web", "index.html"),
    os.path.join(BASE_DIR, "app.html"),
    os.path.join(BASE_DIR, "sitios-web", "app.html")
]

for pf in portal_files:
    if update_footer_in_file(pf):
        print(f"✓ Pie de página con redes sociales actualizado en: {pf}")

# 2. Actualizar las 7 Boutiques
all_dirs = os.listdir(BASE_DIR)
boutique_folders = [
    "pc-custom-lab",
    "bazar-viamx",
    "cigarros-bazar",
    "dulces-bazar",
    "kiosco-digital",
    "mi-puesto-bazar",
    "ofertas-y-liquidaciones"
]

for bf in boutique_folders:
    for d in all_dirs:
        if bf.lower() in d.lower() and os.path.isdir(os.path.join(BASE_DIR, d)):
            idx_file = os.path.join(BASE_DIR, d, "index.html")
            if update_footer_in_file(idx_file):
                print(f"✓ Redes y contacto agregados en boutique: {d}")

            # Subir submódulo
            sub_repo = os.path.join(BASE_DIR, d)
            if os.path.exists(os.path.join(sub_repo, ".git")):
                subprocess.run(["git", "add", "-A"], cwd=sub_repo, check=True)
                subprocess.run(["git", "commit", "-m", "feat(footer): redes sociales oficiales completas y contacto local", "--allow-empty"], cwd=sub_repo, capture_output=True)
                res = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sub_repo, capture_output=True, text=True)
                print(f"   🟢 Submódulo {d} -> Push: {'OK' if res.returncode == 0 else res.stderr.strip()}")
            break

# 3. Desplegar Monorepositorio Central
print("\n=== DESPLEGANDO MONOREPOSITORIO CENTRAL ===")
sitios_repo = os.path.join(BASE_DIR, "sitios-web")
if os.path.exists(os.path.join(sitios_repo, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=sitios_repo, check=True)
    subprocess.run(["git", "commit", "-m", "feat(footer): redes sociales completas (FB, IG, YT, TG, Correo) desplegadas", "--allow-empty"], cwd=sitios_repo, capture_output=True)
    res_sub = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sitios_repo, capture_output=True, text=True)
    print(f"🟢 Submódulo sitios-web -> Push: {'OK' if res_sub.returncode == 0 else res_sub.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(ecosistema): pie de pagina homologado con todas las redes sociales en los 8 portales", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
