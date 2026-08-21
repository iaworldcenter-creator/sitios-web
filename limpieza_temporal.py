import os, re, subprocess

BASE_DIR = r"E:\sitios web"
STORES = [
    "pc-custom-lab", "cigarros-bazar", "dulces-bazar",
    "kiosco-digital", "mi-puesto-bazar", "ofertas-y-liquidaciones",
    "bazar-viamx-nfl.gdl"
]

CANONICAL_MARQUEE = '''<!-- BANDA PROMOCIONAL MARQUEE UNIVERSAL -->
<div class="w-full bg-[#f0c14b] border-b border-[#ddb347] text-slate-950 py-2 overflow-hidden select-none shadow-sm relative z-40">
    <div class="marquee-track flex gap-8 items-center text-xs font-black uppercase tracking-wider whitespace-nowrap">
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

def strip_all_marquees(text):
    text = re.sub(r'<!--\s*BANDA PROMOCIONAL MARQUEE[\s\S]*?<!--\s*FIN BANDA PROMOCIONAL MARQUEE\s*-->', '', text)
    text = re.sub(r'<!--\s*BANDA PROMOCIONAL MARQUEE UNIVERSAL[\s\S]*?</div>\s*</div>', '', text)
    text = re.sub(r'<div class="[^"]*bg-\[\#f0c14b\][^"]*"[\s\S]*?</div>\s*</div>', '', text)
    return text

for store in STORES:
    store_dir = os.path.join(BASE_DIR, store)
    
    # 1. Portada (index.html): Eliminar completamente la marquesina
    idx_path = os.path.join(store_dir, "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8") as f:
            idx = strip_all_marquees(f.read())
        with open(idx_path, "w", encoding="utf-8") as f:
            f.write(idx)
            
    # 2. Páginas de producto y checkout: Dejar exactamente 1 marquesina
    for internal in ["producto.html", "checkout.html"]:
        int_path = os.path.join(store_dir, internal)
        if os.path.exists(int_path):
            with open(int_path, "r", encoding="utf-8") as f:
                c = strip_all_marquees(f.read())
            if "</header>" in c:
                c = re.sub(r'(</header>)', r'\1\n' + CANONICAL_MARQUEE, c, count=1)
            with open(int_path, "w", encoding="utf-8") as f:
                f.write(c)

print("Modificaciones aplicadas con éxito.")
