import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
PC_INDEX_PATH = os.path.join(BASE_DIR, "pc-custom-lab", "index.html")

def fix_pc_custom_lab_structure():
    print("=" * 70)
    print("REESTRUCTURANDO PC CUSTOM LAB (INDEX.HTML)")
    print("=" * 70)

    if not os.path.exists(PC_INDEX_PATH):
        print(f"[Error] No se encontró {PC_INDEX_PATH}")
        return

    with open(PC_INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Inyectar estilos CSS para la animación continua del Carrusel del Tigre
    tiger_marquee_css = """
    <style id="tiger-marquee-style">
        @keyframes marqueeTigerMove {
            0% { transform: translateX(0%); }
            100% { transform: translateX(-50%); }
        }
        .tiger-track-active {
            display: flex;
            width: max-content;
            animation: marqueeTigerMove 28s linear infinite;
            will-change: transform;
        }
        .tiger-track-active:hover {
            animation-play-state: paused;
        }
    </style>
    """
    if 'id="tiger-marquee-style"' not in content:
        content = content.replace("</head>", f"{tiger_marquee_css}\n</head>")

    # 2. Limpiar encabezados duplicados del Catálogo de Productos
    catalogo_header_clean = """<!-- TÍTULO LIMPIO DEL CATÁLOGO -->
<div class="text-center mb-10">
    <h2 class="text-3xl font-black text-white">Catálogo de Componentes Esenciales</h2>
    <p class="text-slate-400 text-sm sm:text-base mt-2 max-w-2xl mx-auto">Encuentra componentes esenciales, periféricos y oportunidades para reparar, actualizar o armar tu equipo.</p>
</div>"""

    # Neutralizar encabezados dobles y banners residuales sobre el título
    content = re.sub(
        r'<div class="text-center mb-12">[\s\S]*?Catálogo de Componentes Esenciales[\s\S]*?<\/p>\s*<\/div>',
        catalogo_header_clean,
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'<section[^>]*id=["\']boutique-refacciones["\'][\s\S]*?<\/section>',
        '',
        content,
        flags=re.IGNORECASE
    )

    # 3. Construir la Sección de Garantía (Carrusel del Tigre en movimiento continuo)
    seccion_garantia_animada = """
<!-- SECCIÓN GARANTÍA: CARRUSEL CONTINUO DEL TIGRE -->
<section class="py-16 bg-slate-950 border-y border-slate-900 overflow-hidden" id="garantia">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 text-center mb-8">
        <span class="px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/30 text-teal-400 font-mono text-xs uppercase tracking-widest inline-block mb-3">
            PC Custom Lab &bull; Tech Service
        </span>
        <h2 class="text-2xl sm:text-3xl font-black text-white">Garantía, Calidad y Respaldo</h2>
        <p class="text-slate-400 text-xs sm:text-sm max-w-2xl mx-auto mt-1">Conoce los pilares y marcas certificadas que respaldan cada uno de nuestros ensambles.</p>
    </div>

    <!-- Pista de Animación Infinita -->
    <div class="w-full overflow-hidden select-none py-2">
        <div class="tiger-track-active flex gap-6 items-center">
            <!-- Set 1 -->
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_6jn16r6jn16r6jn1.webp?v=1.1.0" class="w-full h-full object-cover" alt="Muro de Marcas Global" loading="lazy" onerror="this.src='assets/img/slider_ia_human_thumb.webp';" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">MURO DE MARCAS GLOBAL<br /><span class="text-[10px] text-slate-300 font-normal">Componentes Originales Certificados</span></span></div>
            </div>
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_om0amuom0amuom0a.webp?v=1.1.0" class="w-full h-full object-cover" alt="Periféricos y Accesorios" loading="lazy" onerror="this.src='assets/img/slider_ia_human_thumb.webp';" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">PERIFÉRICOS & ACCESORIOS<br /><span class="text-[10px] text-slate-300 font-normal">Diseño Ergonómico y Alta Precisión</span></span></div>
            </div>
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_e3hrtre3hrtre3hr.webp?v=1.1.0" class="w-full h-full object-cover" alt="Calidad Corporativa" loading="lazy" onerror="this.src='assets/img/slider_ia_human_thumb.webp';" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">PC CUSTOM LAB | TECH SERVICE<br /><span class="text-[10px] text-slate-300 font-normal">Calidad Corporativa Certificada</span></span></div>
            </div>
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_9u70jp9u70jp9u70.webp?v=1.1.0" class="w-full h-full object-cover" alt="Servicio Técnico" loading="lazy" onerror="this.src='assets/img/slider_ia_human_thumb.webp';" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">HONESTIDAD | TRANSPARENCIA<br /><span class="text-[10px] text-slate-300 font-normal">Servicio Técnico Especializado</span></span></div>
            </div>
            <!-- Set 2 (Duplicado exacto para bucle continuo) -->
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_6jn16r6jn16r6jn1.webp?v=1.1.0" class="w-full h-full object-cover" alt="Muro de Marcas Global" loading="lazy" onerror="this.src='assets/img/slider_ia_human_thumb.webp';" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">MURO DE MARCAS GLOBAL<br /><span class="text-[10px] text-slate-300 font-normal">Componentes Originales Certificados</span></span></div>
            </div>
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_om0amuom0amuom0a.webp?v=1.1.0" class="w-full h-full object-cover" alt="Periféricos y Accesorios" loading="lazy" onerror="this.src='assets/img/slider_ia_human_thumb.webp';" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">PERIFÉRICOS & ACCESORIOS<br /><span class="text-[10px] text-slate-300 font-normal">Diseño Ergonómico y Alta Precisión</span></span></div>
            </div>
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_e3hrtre3hrtre3hr.webp?v=1.1.0" class="w-full h-full object-cover" alt="Calidad Corporativa" loading="lazy" onerror="this.src='assets/img/slider_ia_human_thumb.webp';" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">PC CUSTOM LAB | TECH SERVICE<br /><span class="text-[10px] text-slate-300 font-normal">Calidad Corporativa Certificada</span></span></div>
            </div>
            <div class="flex-shrink-0 w-72 sm:w-80 bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-xl hover:border-teal-500 transition">
                <div class="w-full h-56 bg-slate-950 flex items-center justify-center overflow-hidden"><img src="assets/img/Gemini_Generated_Image_9u70jp9u70jp9u70.webp?v=1.1.0" class="w-full h-full object-cover" alt="Servicio Técnico" loading="lazy" onerror="this.src='assets/img/slider_ia_human_thumb.webp';" /></div>
                <div class="bg-teal-950/80 border-t border-teal-500/30 p-3.5 text-center"><span class="text-xs font-mono font-bold text-teal-300 uppercase tracking-wide block">HONESTIDAD | TRANSPARENCIA<br /><span class="text-[10px] text-slate-300 font-normal">Servicio Técnico Especializado</span></span></div>
            </div>
        </div>
    </div>
</section>
"""

    def extract_section(sec_id, source):
        pattern = rf'(<section[^>]*id=["\']{sec_id}["\'][\s\S]*?<\/section>)'
        match = re.search(pattern, source, re.IGNORECASE)
        return match.group(1) if match else None

    sec_productos = extract_section("productos", content)
    if not sec_productos:
        sec_productos = extract_section("catalogo", content)
    sec_cotizador = extract_section("cotizador", content)
    sec_niveles = extract_section("niveles", content)
    sec_lealtad = extract_section("lealtad", content)

    # 4. Eliminar el script desordenador (ordenarFlujoComercial)
    content = re.sub(r'\(function\s*ordenarFlujoComercial[\s\S]*?\}\)\(\);', '', content)
    content = re.sub(r'function\s+ordenarFlujoComercial[\s\S]*?\}', '', content)

    # 5. Ensamblaje estricto en el DOM
    if sec_productos and sec_cotizador and sec_niveles and sec_lealtad:
        main_content_ordered = f"""
<main id="main-content">
    {sec_productos}
    {seccion_garantia_animada}
    {sec_cotizador}
    {sec_niveles}
    {sec_lealtad}
</main>
"""
        content = re.sub(r'<main[\s\S]*?<\/main>', main_content_ordered, content)
        print("✓ Secciones reordenadas físicamente en el DOM.")
    else:
        print("[Aviso] Ensamblando por reemplazo modular de garantía y títulos...")
        content = re.sub(r'<section[^>]*id=["\']garantia["\'][\s\S]*?<\/section>', seccion_garantia_animada, content)
        content = re.sub(r'<div[^>]*id=["\']garantia["\'][\s\S]*?<\/div>\s*<\/div>\s*<\/div>', seccion_garantia_animada, content)

    with open(PC_INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("✓ pc-custom-lab/index.html corregido y estructurado.")

def deploy_fix():
    print("\n" + "=" * 70)
    print("DESPLEGANDO CORRECCIÓN A GITHUB PAGES")
    print("=" * 70)

    pc_dir = os.path.join(BASE_DIR, "pc-custom-lab")
    subprocess.run(["git", "add", "-A"], cwd=pc_dir, check=True)
    subprocess.run(["git", "commit", "-m", "fix(layout): reordenar secciones, limpiar titulos dobles y animar carrusel tigre", "--allow-empty"], cwd=pc_dir, capture_output=True)
    res_pc = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=pc_dir, capture_output=True, text=True)
    print(f"🟢 pc-custom-lab -> Push: {'OK' if res_pc.returncode == 0 else res_pc.stderr.strip()}")

    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "fix(pc-custom-lab): estructura fisica corregida y carrusel continuo", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
    res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
    print(f"🟢 Monorepositorio Raíz -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    fix_pc_custom_lab_structure()
    deploy_fix()
