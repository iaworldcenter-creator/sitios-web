import os
import subprocess
import re
import urllib.parse

BASE_DIR = r"E:\sitios web"
APP_URL = "https://iaworldcenter-creator.github.io/sitios-web/app.html"

print("=" * 80)
print("ELIMINANDO DUPLICADOS Y PROPAGANDO CÓDIGO QR ÚNICO A LOS 8 SITIOS")
print("=" * 80)

# MÓDULO ÚNICO Y LIMPIO DEL CÓDIGO QR
QR_CARD_CLEAN_HTML = f"""
                <!-- TARJETA CÓDIGO QR DIRECTO -->
                <div class="mt-4 p-4 bg-slate-950 border-2 border-cyan-400 rounded-3xl shadow-[0_0_25px_rgba(6,182,212,0.25)] text-center space-y-3">
                    <div class="flex items-center justify-center gap-2">
                        <i class="fa-solid fa-qrcode text-cyan-400 text-lg"></i>
                        <span class="text-xs font-mono font-black text-white uppercase tracking-wider">App Móvil para Talleres</span>
                    </div>

                    <!-- Cuadro del Código QR -->
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

def clean_and_inject_qr(file_path):
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Eliminar cualquier bloque QR previo (incompleto o duplicado)
    # Eliminar patrones de TARJETA CÓDIGO QR previos
    content = re.sub(r'<!--\s*(?:TARJETA|BLOQUE)?\s*(?:DE\s+DESCARGA:)?\s*CÓDIGO\s*QR.*?</div>\s*</div>', '', content, flags=re.DOTALL)
    
    # También limpiar si quedaron fragmentos huérfanos con "Código QR App BAZAR NFL"
    content = re.sub(r'<div class="mt-4 p-4 bg-slate-950 border-2 border-cyan-500/40.*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)

    # 2. Insertar el bloque limpio exactamente arriba de las tarjetas de Gemini / Anti-Gravity
    target_markers = [
        "<!-- BLOQUE DE PRESTIGIO Y DESCARGA",
        "<!-- BLOQUE DE RECONOCIMIENTO Y DESCARGA",
        "<!-- BLOQUE DE PRESTIGIO",
        "<!-- BLOQUE DE RECONOCIMIENTO"
    ]

    injected = False
    for marker in target_markers:
        if marker in content:
            content = content.replace(marker, QR_CARD_CLEAN_HTML.strip() + "\n\n                " + marker)
            injected = True
            break

    if not injected:
        # Si no encontró el marcador, insertarlo al final del sidebar antes de </aside>
        if "</aside>" in content:
            content = content.replace("</aside>", QR_CARD_CLEAN_HTML.strip() + "\n\n            </aside>")
            injected = True

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return True

# 1. Procesar Portal Matriz (raíz y sitios-web)
portal_files = [
    os.path.join(BASE_DIR, "index.html"),
    os.path.join(BASE_DIR, "sitios-web", "index.html")
]

for pf in portal_files:
    if clean_and_inject_qr(pf):
        print(f"✓ Portal Matriz corregido (sin duplicados): {pf}")

# 2. Procesar las 7 Boutiques
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
            if clean_and_inject_qr(idx_file):
                print(f"✓ Boutique {d} actualizada con Código QR único.")

            # Git push en el submódulo
            sub_repo = os.path.join(BASE_DIR, d)
            if os.path.exists(os.path.join(sub_repo, ".git")):
                subprocess.run(["git", "add", "-A"], cwd=sub_repo, check=True)
                subprocess.run(["git", "commit", "-m", "fix(qr): eliminar duplicados y asegurar QR unico con badges PWA", "--allow-empty"], cwd=sub_repo, capture_output=True)
                res = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sub_repo, capture_output=True, text=True)
                print(f"   🟢 Submódulo {d} -> Push: {'OK' if res.returncode == 0 else res.stderr.strip()}")
            break

# 3. Desplegar Monorepositorio Central
print("\n=== DESPLEGANDO MONOREPOSITORIO CENTRAL ===")
sitios_repo = os.path.join(BASE_DIR, "sitios-web")
if os.path.exists(os.path.join(sitios_repo, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=sitios_repo, check=True)
    subprocess.run(["git", "commit", "-m", "fix(qr): codigo QR unico sin duplicados desplegado", "--allow-empty"], cwd=sitios_repo, capture_output=True)
    res_sub = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sitios_repo, capture_output=True, text=True)
    print(f"🟢 Submódulo sitios-web -> Push: {'OK' if res_sub.returncode == 0 else res_sub.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(ecosistema): QR unico y limpio estandarizado en los 8 sitios web", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
