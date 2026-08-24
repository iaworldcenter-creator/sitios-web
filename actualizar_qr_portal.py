import os
import subprocess
import urllib.parse

BASE_DIR = r"E:\sitios web"
APP_URL = "https://iaworldcenter-creator.github.io/sitios-web/app.html"

print("=" * 80)
print("GENERANDO CÓDIGO QR PURO (SVG/PNG) Y ACTUALIZANDO EL PORTAL MATRIZ")
print("=" * 80)

# Descargar imagen física de alta calidad para imprimir en el mostrador
try:
    import urllib.request
    qr_img_url = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote(APP_URL)}&bgcolor=ffffff&color=000000&margin=2"
    local_qr_png = os.path.join(BASE_DIR, "codigo_qr_bazar_nfl.png")
    urllib.request.urlretrieve(qr_img_url, local_qr_png)
    print(f"✓ Archivo físico de QR para impresión generado en: {local_qr_png}")
except Exception as e:
    print(f"Nota imagen local: {e}")

# Módulo HTML del Código QR con respaldo multi-fuente (Garantizado que se ve)
QR_EMBEDDED_HTML = f"""
                <!-- ================================================================
                     TARJETA DE DESCARGA: CÓDIGO QR DIRECTO Y BADGES OFICIALES
                     ================================================================ -->
                <div class="mt-4 p-4 bg-slate-950 border-2 border-cyan-400 rounded-3xl shadow-[0_0_25px_rgba(6,182,212,0.25)] text-center space-y-3">
                    <div class="flex items-center justify-center gap-2">
                        <i class="fa-solid fa-qrcode text-cyan-400 text-lg"></i>
                        <span class="text-xs font-mono font-black text-white uppercase tracking-wider">App Móvil para Talleres</span>
                    </div>

                    <!-- Cuadro del Código QR (Respaldo directo de alta visibilidad) -->
                    <div class="w-44 h-44 mx-auto bg-white p-2.5 rounded-2xl shadow-xl flex items-center justify-center">
                        <img 
                            src="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(APP_URL)}&margin=1" 
                            alt="Código QR App BAZAR NFL" 
                            class="w-full h-full object-contain rounded-lg"
                            onerror="this.onerror=null; this.src='https://quickchart.io/qr?text={urllib.parse.quote(APP_URL)}&size=300';"
                        />
                    </div>

                    <p class="text-[11px] text-slate-300 leading-snug font-medium">
                        Apunta con la cámara de tu celular a este código para abrir e instalar la App en tu teléfono.
                    </p>

                    <!-- Enlaces Directos PWA / Tiendas -->
                    <div class="flex flex-col gap-2 pt-1">
                        <a href="{APP_URL}" target="_blank" class="flex items-center justify-center gap-3 bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-emerald-400 py-2.5 px-3 rounded-xl text-left transition shadow group">
                            <i class="fa-brands fa-google-play text-xl text-emerald-400 group-hover:scale-110 transition"></i>
                            <div>
                                <span class="text-[8px] font-mono text-slate-400 block uppercase leading-none">Disponible vía Web / PWA</span>
                                <strong class="text-xs text-white block leading-none font-bold">Instalar en Android</strong>
                            </div>
                        </a>
                        <a href="{APP_URL}" target="_blank" class="flex items-center justify-center gap-3 bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-cyan-400 py-2.5 px-3 rounded-xl text-left transition shadow group">
                            <i class="fa-brands fa-apple text-2xl text-white group-hover:scale-110 transition"></i>
                            <div>
                                <span class="text-[8px] font-mono text-slate-400 block uppercase leading-none">Compatible con iPhone</span>
                                <strong class="text-xs text-white block leading-none font-bold">Instalar en iOS / Apple</strong>
                            </div>
                        </a>
                    </div>
                </div>
"""

# Inyectar en el Portal Matriz (index.html y sitios-web/index.html)
portal_files = [
    os.path.join(BASE_DIR, "index.html"),
    os.path.join(BASE_DIR, "sitios-web", "index.html")
]

for p in portal_files:
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            html = f.read()

        # Si ya existe una versión previa del bloque QR, reemplazarla limpiamente
        if "<!-- TARJETA DE DESCARGA: CÓDIGO QR DIRECTO" in html:
            start = html.find("<!-- TARJETA DE DESCARGA: CÓDIGO QR DIRECTO")
            end = html.find("<!-- BLOQUE DE PRESTIGIO", start)
            if end != -1:
                html = html[:start] + QR_EMBEDDED_HTML.strip() + "\n\n                " + html[end:]
        elif "<!-- BLOQUE DE PRESTIGIO" in html:
            html = html.replace("<!-- BLOQUE DE PRESTIGIO", QR_EMBEDDED_HTML.strip() + "\n\n                <!-- BLOQUE DE PRESTIGIO")
        elif "<!-- BLOQUE DE RECONOCIMIENTO" in html:
            html = html.replace("<!-- BLOQUE DE RECONOCIMIENTO", QR_EMBEDDED_HTML.strip() + "\n\n                <!-- BLOQUE DE RECONOCIMIENTO")

        with open(p, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ Portal Matriz actualizado con QR visible en: {p}")

# Desplegar cambios a GitHub Pages
print("\n=== DESPLEGANDO A GITHUB PAGES ===")
sitios_repo = os.path.join(BASE_DIR, "sitios-web")
if os.path.exists(os.path.join(sitios_repo, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=sitios_repo, check=True)
    subprocess.run(["git", "commit", "-m", "feat(qr): codigo QR de alta visibilidad y enlaces de descarga PWA", "--allow-empty"], cwd=sitios_repo, capture_output=True)
    res_sub = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sitios_repo, capture_output=True, text=True)
    print(f"🟢 Submódulo sitios-web -> Push: {'OK' if res_sub.returncode == 0 else res_sub.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(ecosistema): Codigo QR visible en portal y archivo png para impresion generado", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
