import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"

STORES = {
    "pc-custom-lab": "PC Custom Lab",
    "bazar-viamx-nfl.gdl": "Bazar Viamx NFL",
    "cigarros-bazar": "Cigarros Bazar",
    "dulces-bazar": "Dulces Bazar",
    "kiosco-digital": "Kiosco Digital",
    "mi-puesto-bazar": "Mi Puesto Bazar",
    "ofertas-y-liquidaciones": "Liquidaciones y Ofertas"
}

def generate_universal_footer(store_name):
    return f"""
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
                            <i class="fa-brands fa-facebook text-blue-500 w-4 text-center"></i> Facebook: {store_name}
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
                <p>&copy; 2026 {store_name}. Pedro Moreno 501 A, Guadalajara Centro. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>
    """

def update_all_footers():
    print("=== HOMOLOGANDO FOOTER UNIVERSAL (3 COLUMNAS) EN 14 ARCHIVOS ===")
    
    for store_slug, store_title in STORES.items():
        store_dir = os.path.join(BASE_DIR, store_slug)
        if not os.path.exists(store_dir):
            continue

        for html_file in ["index.html", "producto.html"]:
            file_path = os.path.join(store_dir, html_file)
            if not os.path.exists(file_path):
                continue

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 1. Eliminar bloques antiguos de "Ubicación y Contacto Directo"
            content = re.sub(r'<section[^>]*id=["\'](?:contacto|ubicacion)["\'][\s\S]*?<\/section>', '', content, flags=re.IGNORECASE)
            content = re.sub(r'<div[^>]*id=["\'](?:contacto|ubicacion)["\'][\s\S]*?<\/div>\s*<\/div>\s*<\/div>', '', content, flags=re.IGNORECASE)
            content = re.sub(r'<!--\s*(?://\s*)?UBICACI[ÓO]N Y CONTACTO DIRECTO[\s\S]*?<\/div>\s*<\/div>\s*<\/div>', '', content, flags=re.IGNORECASE)
            content = re.sub(r'<div[^>]*>\s*// UBICACI[ÓO]N Y CONTACTO DIRECTO[\s\S]*?<\/div>\s*<\/div>\s*<\/div>', '', content, flags=re.IGNORECASE)

            # 2. Reemplazar footer antiguo por el footer homologado
            pattern = r'<footer[\s\S]*?<\/footer>'
            new_footer = generate_universal_footer(store_title)
            
            if re.search(pattern, content):
                content = re.sub(pattern, new_footer, content)
            else:
                content = content.replace("</body>", f"{new_footer}\n</body>")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"  ✓ {store_slug}/{html_file} -> Footer 3 columnas integrado.")

    print("\n=== DESPLIEGUE GIT MASIVO ===")
    for store_slug in STORES.keys():
        sdir = os.path.join(BASE_DIR, store_slug)
        if os.path.exists(os.path.join(sdir, ".git")):
            subprocess.run(["git", "add", "-A"], cwd=sdir, check=True)
            subprocess.run(["git", "commit", "-m", "feat(footer): homologacion universal de 3 columnas", "--allow-empty"], cwd=sdir, capture_output=True)
            res_store = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sdir, capture_output=True, text=True)
            status = "OK" if res_store.returncode == 0 else f"Error: {res_store.stderr.strip()}"
            print(f"  🟢 {store_slug.ljust(26)} -> Push: {status}")

    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(footer): homologacion corporativa de 3 columnas en las 7 boutiques", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
    res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
    print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    update_all_footers()
