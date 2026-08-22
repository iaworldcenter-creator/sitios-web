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
print("INTEGRANDO VIDEO DE LEALTAD Y ENLACES A GEMINI & ANTI-GRAVITY EN VÍA MX")
print("=" * 70)

# 1. Bloque visual del video con botones interactivos en la parte inferior
NUEVO_VIDEO_LEALTAD_HTML = """
                <!-- Contenedor de Video Interactivo con Enlaces a Gemini y Anti-Gravity -->
                <div class="lg:col-span-5 flex flex-col items-center text-center">
                    <div class="relative w-full max-w-[380px] rounded-3xl overflow-hidden border border-slate-800 shadow-2xl bg-slate-950 flex flex-col">
                        
                        <!-- Video en Bucle Automático -->
                        <div class="relative w-full h-80 sm:h-96 overflow-hidden bg-slate-950" id="video-container-viamx">
                            <video autoplay muted loop playsinline preload="auto" class="w-full h-full object-cover" id="viamx-loyalty-video">
                                <source src="assets/img/Tigers_walking_in_department_store_202608220510.mp4" type="video/mp4" />
                                <source src="Tigers_walking_in_department_store_202608220510.mp4" type="video/mp4" />
                                <img src="assets/img/mascota_tigre_thumb.webp" alt="Club de Socios Vía MX" class="w-full h-full object-cover" />
                            </video>
                        </div>

                        <!-- Barra Inferior de Créditos y Botones Interactivos -->
                        <div class="w-full bg-slate-950/95 border-t border-slate-800/90 p-3.5 flex flex-col gap-2.5 z-10">
                            <div class="text-[11px] font-mono text-slate-300 font-bold flex items-center justify-center gap-1.5">
                                <i class="fa-solid fa-wand-magic-sparkles text-cyan-400"></i>
                                <span>Sitio creado con Gemini y desarrollado por Anti-Gravity</span>
                            </div>
                            
                            <div class="grid grid-cols-2 gap-2">
                                <a href="https://gemini.google.com" target="_blank" rel="noopener" class="bg-slate-900 hover:bg-slate-800 border border-cyan-500/50 hover:border-cyan-400 text-cyan-300 font-bold py-2 px-2 rounded-xl text-[11px] flex items-center justify-center gap-1.5 transition active:scale-95 shadow-sm cursor-pointer" title="Suscribirse a Google Gemini">
                                    <i class="fa-solid fa-sparkles text-cyan-400"></i> Suscribirse a Gemini
                                </a>
                                <a href="https://antigravity.google/download" target="_blank" rel="noopener" class="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black py-2 px-2 rounded-xl text-[11px] flex items-center justify-center gap-1.5 transition active:scale-95 shadow-md shadow-amber-500/20 cursor-pointer" title="Descargar Anti-Gravity">
                                    <i class="fa-solid fa-download text-slate-950"></i> Bajar Anti-Gravity
                                </a>
                            </div>
                        </div>

                    </div>
                </div>
"""

# Reemplazar la columna del contenedor de video dentro de #lealtad
pattern_col = re.compile(r'<!-- Contenedor reservado para Video[\s\S]*?<\/div>\s*<\/div>\s*<\/div>', re.IGNORECASE)

if pattern_col.search(html):
    html = pattern_col.sub(NUEVO_VIDEO_LEALTAD_HTML.strip(), html, count=1)
else:
    # Reemplazo por clase de columna en la sección lealtad
    pattern_alt = re.compile(r'<div class="lg:col-span-5 flex flex-col items-center text-center">[\s\S]*?<\/div>\s*<\/div>\s*<\/div>', re.IGNORECASE)
    if pattern_alt.search(html):
        html = pattern_alt.sub(NUEVO_VIDEO_LEALTAD_HTML.strip(), html, count=1)

# Asegurar que el video inicie su reproducción automáticamente al cargar la página
JS_VIDEO_INIT = """
    // Inicialización del video de la familia tigre en tienda departamental
    function initLoyaltyVideo() {
        const vid = document.getElementById('viamx-loyalty-video');
        if (vid) {
            vid.muted = true;
            vid.loop = true;
            vid.playbackRate = 0.85;
            const playPromise = vid.play();
            if (playPromise && typeof playPromise.catch === 'function') {
                playPromise.catch(() => {});
            }
        }
    }
    document.addEventListener('DOMContentLoaded', initLoyaltyVideo);
"""

if "function initLoyaltyVideo" not in html:
    html = html.replace("</script>\n</body>", f"{JS_VIDEO_INIT}\n    </script>\n</body>")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("✓ Video Tigers_walking_in_department_store_202608220510.mp4 y enlaces configurados en index.html")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(lealtad): integrar video familia tigre en tienda departamental y botones de Gemini y Anti-Gravity", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(viamx): video de lealtad con botones interactivos Gemini y Anti-Gravity sincronizado", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
