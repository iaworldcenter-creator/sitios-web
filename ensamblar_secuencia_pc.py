import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
PC_INDEX_PATH = os.path.join(BASE_DIR, "pc-custom-lab", "index.html")

def build_perfect_pc_custom_lab():
    print("=" * 75)
    print("ENSAMBLANDO SECUENCIA FÍSICA EXACTA DE PC CUSTOM LAB (INDEX.HTML)")
    print("=" * 75)

    if not os.path.exists(PC_INDEX_PATH):
        print(f"[Error] No se encontró: {PC_INDEX_PATH}")
        return

    with open(PC_INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # A. Inyectar animación fluida para el Carrusel del Tigre
    tiger_css = """
    <style id="tiger-continuous-marquee">
        @keyframes marqueeTigerFlow {
            0% { transform: translateX(0%); }
            100% { transform: translateX(-50%); }
        }
        .tiger-track-flow {
            display: flex;
            width: max-content;
            animation: marqueeTigerFlow 25s linear infinite;
            will-change: transform;
        }
        .tiger-track-flow:hover {
            animation-play-state: paused;
        }
    </style>
    """
    if 'id="tiger-continuous-marquee"' not in content:
        content = content.replace("</head>", f"{tiger_css}\n</head>")

    # B. Definir la Sección de Garantía (Carrusel del Tigre)
    seccion_garantia = """
<!-- 4. GARANTÍA, CALIDAD Y RESPALDO (CARRUSEL CONTINUO DEL TIGRE) -->
<section class="py-16 bg-slate-950 border-y border-slate-900 overflow-hidden" id="garantia">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 text-center mb-8">
        <span class="px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/30 text-teal-400 font-mono text-xs uppercase tracking-widest inline-block mb-3">
            PC Custom Lab &bull; Tech Service
        </span>
        <h2 class="text-3xl font-black text-white">Garantía, Calidad y Respaldo</h2>
        <p class="text-slate-400 text-xs sm:text-sm max-w-2xl mx-auto mt-1">Conoce a nuestra mascota y los pilares que respaldan cada uno de nuestros ensambles y servicios técnicos.</p>
    </div>

    <div class="w-full overflow-hidden select-none py-2">
        <div class="tiger-track-flow flex gap-6 items-center">
            <!-- Bloque Original -->
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_6jn16r6jn16r6jn1.webp?v=1.1.0" class="w-full h-full object-cover" alt="Muro de Marcas Global" loading="lazy" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">MURO DE MARCAS GLOBAL<br /><span class="text-[10px] text-slate-300 font-normal">Componentes Originales Certificados</span></span></div>
            </div>
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_om0amuom0amuom0a.webp?v=1.1.0" class="w-full h-full object-cover" alt="Periféricos" loading="lazy" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">PERIFÉRICOS & ACCESORIOS<br /><span class="text-[10px] text-slate-300 font-normal">Diseño Ergonómico y Alta Precisión</span></span></div>
            </div>
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_e3hrtre3hrtre3hr.webp?v=1.1.0" class="w-full h-full object-cover" alt="Calidad Certificada" loading="lazy" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">PC CUSTOM LAB | TECH SERVICE<br /><span class="text-[10px] text-slate-300 font-normal">Calidad Corporativa Certificada</span></span></div>
            </div>
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_9u70jp9u70jp9u70.webp?v=1.1.0" class="w-full h-full object-cover" alt="Servicio Técnico" loading="lazy" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">HONESTIDAD | TRANSPARENCIA<br /><span class="text-[10px] text-slate-300 font-normal">Servicio Técnico Especializado</span></span></div>
            </div>
            <!-- Bloque Duplicado para loop sin saltos -->
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_6jn16r6jn16r6jn1.webp?v=1.1.0" class="w-full h-full object-cover" alt="Muro de Marcas Global" loading="lazy" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">MURO DE MARCAS GLOBAL<br /><span class="text-[10px] text-slate-300 font-normal">Componentes Originales Certificados</span></span></div>
            </div>
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_om0amuom0amuom0a.webp?v=1.1.0" class="w-full h-full object-cover" alt="Periféricos" loading="lazy" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">PERIFÉRICOS & ACCESORIOS<br /><span class="text-[10px] text-slate-300 font-normal">Diseño Ergonómico y Alta Precisión</span></span></div>
            </div>
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_e3hrtre3hrtre3hr.webp?v=1.1.0" class="w-full h-full object-cover" alt="Calidad Certificada" loading="lazy" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">PC CUSTOM LAB | TECH SERVICE<br /><span class="text-[10px] text-slate-300 font-normal">Calidad Corporativa Certificada</span></span></div>
            </div>
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_9u70jp9u70jp9u70.webp?v=1.1.0" class="w-full h-full object-cover" alt="Servicio Técnico" loading="lazy" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">HONESTIDAD | TRANSPARENCIA<br /><span class="text-[10px] text-slate-300 font-normal">Servicio Técnico Especializado</span></span></div>
            </div>
        </div>
    </div>
</section>
"""

    # C. Limpiar títulos duplicados en la sección de Productos
    clean_cat_header = """<div class="text-center mb-12">
    <h2 class="text-3xl font-black text-white">Catálogo de Componentes Esenciales</h2>
    <p class="text-slate-400 text-sm sm:text-base mt-3 max-w-2xl mx-auto">Encuentra componentes esenciales, periféricos y oportunidades para reparar, actualizar o armar tu equipo.</p>
</div>"""

    content = re.sub(
        r'<div class="text-center mb-12">[\s\S]*?Catálogo de Componentes Esenciales[\s\S]*?<\/p>\s*<\/div>',
        clean_cat_header,
        content,
        flags=re.IGNORECASE
    )

    # D. Extraer las secciones individuales limpias
    def extract_sec(sec_id):
        m = re.search(rf'(<section[^>]*id=["\']{sec_id}["\'][\s\S]*?<\/section>)', content, re.IGNORECASE)
        return m.group(1) if m else ""

    sec_productos = extract_sec("productos")
    sec_niveles = extract_sec("niveles")
    sec_cotizador = extract_sec("cotizador")
    sec_lealtad = extract_sec("lealtad")

    # E. Eliminar el JavaScript desordenador (ordenarFlujoComercial)
    content = re.sub(r'\(function\s*ordenarFlujoComercial[\s\S]*?\}\)\(\);', '', content)

    # F. Ensamblar el <main id="main-content"> en el orden exacto de las imágenes
    main_encadenado = f"""<main id="main-content">
{sec_productos}

{sec_niveles}

{sec_cotizador}

{seccion_garantia}

{sec_lealtad}
</main>"""

    content = re.sub(r'<main[\s\S]*?<\/main>', main_encadenado, content)

    with open(PC_INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("✓ pc-custom-lab/index.html reensamblado con la secuencia física exacta.")

def deploy():
    print("\n" + "=" * 75)
    print("SUBIENDO CAMBIOS A GITHUB PAGES")
    print("=" * 75)
    pc_dir = os.path.join(BASE_DIR, "pc-custom-lab")
    subprocess.run(["git", "add", "-A"], cwd=pc_dir, check=True)
    subprocess.run(["git", "commit", "-m", "fix(pc-custom-lab): secuencia exacta de secciones y carrusel continuo", "--allow-empty"], cwd=pc_dir, capture_output=True)
    res_pc = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=pc_dir, capture_output=True, text=True)
    print(f"🟢 pc-custom-lab -> Push: {'OK' if res_pc.returncode == 0 else res_pc.stderr.strip()}")

    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "fix(pc-custom-lab): reordenamiento secuencial e inmunidad de DOM", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
    res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
    print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    build_perfect_pc_custom_lab()
    deploy()
