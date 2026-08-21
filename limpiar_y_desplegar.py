import os, re, subprocess

BASE_DIR = r"E:\sitios web"
STORES = [
    "pc-custom-lab", "cigarros-bazar", "dulces-bazar",
    "kiosco-digital", "mi-puesto-bazar", "ofertas-y-liquidaciones",
    "bazar-viamx-nfl.gdl"
]

AUTO_RESET_SCRIPT = '''<script>
(function() {
    try {
        const vKey = "ecosystem_reset_v2026_clean";
        if (!localStorage.getItem(vKey)) {
            const cart = localStorage.getItem("ecosystem_global_cart");
            if (cart && (cart.includes("GPU-001") || cart === "[object Object]")) {
                localStorage.setItem("ecosystem_global_cart", "[]");
            }
            const history = localStorage.getItem("user_purchases_history");
            if (history && history.includes("AGY-4982")) {
                localStorage.setItem("user_purchases_history", "[]");
            }
            localStorage.setItem(vKey, "true");
        }
    } catch(e) {}
})();
</script>'''

for store in STORES:
    store_dir = os.path.join(BASE_DIR, store)
    
    # 1. Procesar index.html
    idx_path = os.path.join(store_dir, "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8") as f:
            idx_c = f.read()
        
        # Eliminar mocks de historial
        idx_c = re.sub(r'if\s*\(\s*history\.length\s*===\s*0\s*\)\s*\{[\s\S]*?reorderItems\s*=\s*JSON\.parse[\s\S]*?\}', '', idx_c)
        
        # Inyectar auto-reset
        if "ecosystem_reset_v2026_clean" not in idx_c:
            idx_c = idx_c.replace("</head>", f"{AUTO_RESET_SCRIPT}\n</head>")
            
        with open(idx_path, "w", encoding="utf-8") as f:
            f.write(idx_c)
            
    # 2. Procesar checkout.html
    co_path = os.path.join(store_dir, "checkout.html")
    if os.path.exists(co_path):
        with open(co_path, "r", encoding="utf-8") as f:
            co_c = f.read()
            
        # Actualizar miniaturas a 170x170
        co_c = re.sub(
            r'<img\s+src="\$\{imgUrl\}"[^>]*style="[^"]*"[^>]*class="([^"]*)"[^>]*>',
            r'<div class="w-[170px] h-[170px] min-w-[170px] max-w-[170px] rounded-2xl overflow-hidden bg-slate-950 border border-slate-700/80 shrink-0 p-1 flex items-center justify-center"><img src="" class="w-full h-full object-cover rounded-xl" alt="" loading="lazy" /></div>',
            co_c
        )
        
        # Inyectar auto-reset
        if "ecosystem_reset_v2026_clean" not in co_c:
            co_c = co_c.replace("</head>", f"{AUTO_RESET_SCRIPT}\n</head>")
            
        with open(co_path, "w", encoding="utf-8") as f:
            f.write(co_c)

print("Archivos normalizados con éxito.")
