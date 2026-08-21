import os, re

BASE_DIR = r"E:\sitios web"
STORES = [
    "pc-custom-lab", "cigarros-bazar", "dulces-bazar",
    "kiosco-digital", "mi-puesto-bazar", "ofertas-y-liquidaciones",
    "bazar-viamx-nfl.gdl"
]

for store in STORES:
    # 1. Limpiar index.html (eliminar mock de pedidos simulados)
    idx_path = os.path.join(BASE_DIR, store, "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8") as f:
            c = f.read()
        c = re.sub(r'if\s*\(\s*history\.length\s*===\s*0\s*\)\s*\{[\s\S]*?reorderItems\s*=\s*JSON\.parse[\s\S]*?\}', '', c)
        with open(idx_path, "w", encoding="utf-8") as f:
            f.write(c)

    # 2. Actualizar checkout.html (imagenes 170x170 y sin mocks)
    co_path = os.path.join(BASE_DIR, store, "checkout.html")
    if os.path.exists(co_path):
        with open(co_path, "r", encoding="utf-8") as f:
            c = f.read()
        c = re.sub(
            r'<img\s+src="\$\{imgUrl\}"[^>]*style="[^"]*"[^>]*class="([^"]*)"[^>]*>',
            r'<div class="w-[170px] h-[170px] min-w-[170px] max-w-[170px] rounded-2xl overflow-hidden bg-slate-950 border border-slate-700/80 shrink-0 p-1 flex items-center justify-center"><img src="" class="w-full h-full object-cover rounded-xl" alt="" loading="lazy" /></div>',
            c
        )
        with open(co_path, "w", encoding="utf-8") as f:
            f.write(c)

print("Actualizacion completada en las 7 tiendas.")
