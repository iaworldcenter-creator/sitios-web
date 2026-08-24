import os
import subprocess

BASE_DIR = r"E:\sitios web"
APP_URL = "https://iaworldcenter-creator.github.io/sitios-web/app.html"
QR_API_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={APP_URL}&bgcolor=0f172a&color=38bdf8&margin=1"

print("=" * 80)
print("INTEGRANDO CÓDIGO QR Y BADGES DE DESCARGA GOOGLE PLAY & APPLE APP STORE")
print("=" * 80)

# --------------------------------------------------------------------------
# 1. ACTUALIZAR PORTAL MATRIZ (index.html y sitios-web/index.html)
# --------------------------------------------------------------------------
portal_paths = [
    os.path.join(BASE_DIR, "index.html"),
    os.path.join(BASE_DIR, "sitios-web", "index.html")
]

for p in portal_paths:
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()

        # Inyectar tarjeta del QR en el sidebar debajo de las 7 boutiques
        qr_card_html = f"""
                <!-- TARJETA CÓDIGO QR: DESCARGA DIRECTA AL CELULAR -->
                <div class="mt-4 p-4 bg-slate-950 border-2 border-cyan-500/40 rounded-2xl shadow-xl text-center space-y-3">
                    <div class="flex items-center justify-center gap-2">
                        <i class="fa-solid fa-qrcode text-cyan-400 text-base"></i>
                        <span class="text-xs font-mono font-bold text-white uppercase tracking-wider">App Móvil para Talleres</span>
                    </div>
                    
                    <div class="w-40 h-40 mx-auto bg-slate-900 p-2 rounded-2xl border border-cyan-500/30 flex items-center justify-center shadow-inner">
                        <img src="{QR_API_URL}" alt="Código QR App BAZAR NFL" class="w-full h-full rounded-xl object-contain" />
                    </div>

                    <p class="text-[11px] text-slate-300 leading-tight">
                        Apunta con la cámara de tu celular para abrir e instalar la App en tu teléfono.
                    </p>

                    <!-- BADGES GOOGLE PLAY Y APPLE APP STORE -->
                    <div class="flex flex-col gap-2 pt-1">
                        <a href="{APP_URL}" class="flex items-center justify-center gap-2.5 bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-cyan-400 py-2 px-3 rounded-xl text-left transition shadow group">
                            <i class="fa-brands fa-google-play text-lg text-emerald-400 group-hover:scale-110 transition"></i>
                            <div>
                                <span class="text-[8px] font-mono text-slate-400 block uppercase leading-none">Disponible en</span>
                                <strong class="text-xs text-white block leading-none font-bold">Google Play</strong>
                            </div>
                        </a>
                        <a href="{APP_URL}" class="flex items-center justify-center gap-2.5 bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-cyan-400 py-2 px-3 rounded-xl text-left transition shadow group">
                            <i class="fa-brands fa-apple text-xl text-white group-hover:scale-110 transition"></i>
                            <div>
                                <span class="text-[8px] font-mono text-slate-400 block uppercase leading-none">Consíguelo en el</span>
                                <strong class="text-xs text-white block leading-none font-bold">App Store</strong>
                            </div>
                        </a>
                    </div>
                </div>
        """

        if "<!-- BLOQUE DE RECONOCIMIENTO" in content and "<!-- TARJETA CÓDIGO QR" not in content:
            content = content.replace("<!-- BLOQUE DE RECONOCIMIENTO", qr_card_html + "\n\n                <!-- BLOQUE DE RECONOCIMIENTO")
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✓ Código QR y Badges integrados en Portal: {p}")

# --------------------------------------------------------------------------
# 2. ACTUALIZAR APP MÓVIL (app.html) CON MODAL DE INSTALACIÓN
# --------------------------------------------------------------------------
app_paths = [
    os.path.join(BASE_DIR, "app.html"),
    os.path.join(BASE_DIR, "sitios-web", "app.html")
]

for ap in app_paths:
    if os.path.exists(ap):
        with open(ap, "r", encoding="utf-8") as f:
            app_code = f.read()

        store_badges_app_html = f"""
        <!-- BADGES OFICIALES EN LA APP -->
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-3xl shadow-xl space-y-3">
            <div class="flex items-center justify-between">
                <span class="text-xs font-mono font-bold text-white flex items-center gap-1.5">
                    <i class="fa-solid fa-mobile-screen text-cyan-400"></i> Descargar Aplicación Oficial
                </span>
                <span class="text-[9px] font-mono font-bold text-emerald-400 bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-500/30">PWA 2026</span>
            </div>

            <div class="grid grid-cols-2 gap-2.5">
                <button onclick="installPWA()" class="flex items-center justify-center gap-2 bg-slate-950 border border-slate-800 hover:border-emerald-400 py-2 px-2.5 rounded-2xl transition active:scale-95 shadow cursor-pointer">
                    <i class="fa-brands fa-google-play text-base text-emerald-400"></i>
                    <div class="text-left">
                        <span class="text-[8px] font-mono text-slate-400 block leading-none">Android</span>
                        <strong class="text-[11px] text-white block leading-none font-bold">Google Play</strong>
                    </div>
                </button>
                <button onclick="showiOSInstallGuide()" class="flex items-center justify-center gap-2 bg-slate-950 border border-slate-800 hover:border-cyan-400 py-2 px-2.5 rounded-2xl transition active:scale-95 shadow cursor-pointer">
                    <i class="fa-brands fa-apple text-lg text-white"></i>
                    <div class="text-left">
                        <span class="text-[8px] font-mono text-slate-400 block leading-none">iPhone / iOS</span>
                        <strong class="text-[11px] text-white block leading-none font-bold">App Store</strong>
                    </div>
                </button>
            </div>
        </div>
        """

        if "<!-- CALCULADORA DINÁMICA" in app_code and "<!-- BADGES OFICIALES EN LA APP -->" not in app_code:
            app_code = app_code.replace("<!-- CALCULADORA DINÁMICA", store_badges_app_html + "\n\n        <!-- CALCULADORA DINÁMICA")
            
            # Agregar función guía para iOS si no existe
            ios_script = """
    function showiOSInstallGuide() {
        alert('📲 Para instalar en iPhone / iPad:\\n\\n1. Toca el botón de Compartir (icono de caja con flecha arriba).\\n2. Desliza hacia abajo y selecciona \"Agregar a la pantalla de inicio\".\\n3. ¡Listo! Tendrás el icono del Tigre en tu teléfono.');
    }
            """
            app_code = app_code.replace("function installPWA() {", ios_script + "\n    function installPWA() {")

            with open(ap, "w", encoding="utf-8") as f:
                f.write(app_code)
            print(f"✓ Badges de instalación integrados en App: {ap}")

# --------------------------------------------------------------------------
# 3. DESPLEGAR A GITHUB PAGES
# --------------------------------------------------------------------------
print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
sitios_repo = os.path.join(BASE_DIR, "sitios-web")
if os.path.exists(os.path.join(sitios_repo, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=sitios_repo, check=True)
    subprocess.run(["git", "commit", "-m", "feat(pwa): QR code para escaneo con celular y badges oficiales de Google Play / App Store", "--allow-empty"], cwd=sitios_repo, capture_output=True)
    res_sub = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sitios_repo, capture_output=True, text=True)
    print(f"🟢 Submódulo sitios-web -> Push: {'OK' if res_sub.returncode == 0 else res_sub.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(ecosistema): Codigo QR y enlaces de descarga de App Store y Google Play desplegados", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
