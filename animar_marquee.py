import os, re, subprocess

BASE_DIR = r"E:\sitios web"
STORES = [
    "pc-custom-lab", "cigarros-bazar", "dulces-bazar",
    "kiosco-digital", "mi-puesto-bazar", "ofertas-y-liquidaciones",
    "bazar-viamx-nfl.gdl"
]

ANIMATED_MARQUEE = '''<!-- BANDA PROMOCIONAL MARQUEE ANIMADA -->
<div class="w-full bg-[#f0c14b] border-b border-[#ddb347] text-slate-950 py-2.5 overflow-hidden select-none shadow-sm relative z-40">
    <style>
        @keyframes marqueeContinuousMove {
            0% { transform: translateX(0%); }
            100% { transform: translateX(-50%); }
        }
        .marquee-track-active {
            display: flex;
            width: max-content;
            animation: marqueeContinuousMove 30s linear infinite;
            will-change: transform;
        }
        .marquee-track-active:hover {
            animation-play-state: paused;
        }
    </style>
    <div class="marquee-track-active flex gap-8 items-center text-xs font-black uppercase tracking-wider whitespace-nowrap">
        <span class="flex items-center gap-1.5">🚚 ¡ENVÍO GRATIS en compras a partir de ,500 MXN!</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">💰 5% DE CASHBACK acumulable con registro activo.</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">📦 PRECIO DE MAYOREO: 15% de descuento directo a partir de 10 piezas.</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">⚠️ CONDICIÓN: Sin registro no hay cashback acumulable.</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">🛒 BOUTIQUES ESPECIALIZADAS, UN SOLO CARRITO GLOBAL.</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">💳 Pagos con tarjeta bancaria y transferencias SPEI.</span>
        <span class="text-slate-900 font-bold">•</span>
        <!-- Bucle duplicado para ciclo continuo -->
        <span class="flex items-center gap-1.5">🚚 ¡ENVÍO GRATIS en compras a partir de ,500 MXN!</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">💰 5% DE CASHBACK acumulable con registro activo.</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">📦 PRECIO DE MAYOREO: 15% de descuento directo a partir de 10 piezas.</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">⚠️ CONDICIÓN: Sin registro no hay cashback acumulable.</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">🛒 BOUTIQUES ESPECIALIZADAS, UN SOLO CARRITO GLOBAL.</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">💳 Pagos con tarjeta bancaria y transferencias SPEI.</span>
    </div>
</div>'''

def clean_marquees(text):
    text = re.sub(r'<!--\s*BANDA PROMOCIONAL MARQUEE[\s\S]*?<!--\s*FIN BANDA PROMOCIONAL MARQUEE\s*-->', '', text)
    text = re.sub(r'<!--\s*BANDA PROMOCIONAL MARQUEE[\s\S]*?</div>\s*</div>', '', text)
    text = re.sub(r'<div class="[^"]*bg-\[\#f0c14b\][^"]*"[\s\S]*?</div>\s*</div>', '', text)
    return text

for store in STORES:
    store_dir = os.path.join(BASE_DIR, store)
    
    # 1. Asegurar portada limpia (index.html)
    idx_path = os.path.join(store_dir, "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8") as f:
            idx = clean_marquees(f.read())
        with open(idx_path, "w", encoding="utf-8") as f:
            f.write(idx)
            
    # 2. Inyectar animación en producto y checkout
    for page in ["producto.html", "checkout.html"]:
        p_path = os.path.join(store_dir, page)
        if os.path.exists(p_path):
            with open(p_path, "r", encoding="utf-8") as f:
                c = clean_marquees(f.read())
            if "</header>" in c:
                c = re.sub(r'(</header>)', r'\1\n' + ANIMATED_MARQUEE, c, count=1)
            with open(p_path, "w", encoding="utf-8") as f:
                f.write(c)

print("Animación aplicada a todas las boutiques.")
