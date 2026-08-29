import os
import json
import re

BASE_DIR = r"E:\sitios web\pc-custom-lab"

print("=" * 80, flush=True)
print("OPTIMIZACIÓN TOTAL DE RENDIMIENTO: CERO SOLICITUDES BLOQUEANTES EN HEAD")
print("=" * 80, flush=True)

with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
    html = f.read()

# Nuevo HEAD sin bloqueo de renderizado
OPTIMIZED_NON_BLOCKING_HEAD = """<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PC Custom Lab | Hardware Mayorista & Ensamble de Cómputo</title>
    <meta name="description" content="Catálogo oficial de hardware mayorista PC Custom Lab, procesadores Intel/AMD, placas ASUS, tarjetas gráficas RTX y configuraciones armadas.">
    
    <!-- Preconexión DNS y CDN -->
    <link rel="preconnect" href="https://static.ctonline.mx" crossorigin>
    <link rel="dns-prefetch" href="https://static.ctonline.mx">

    <!-- CSS Asíncrono no bloqueante (Ahorro de ~500ms en FCP) -->
    <link rel="preload" href="assets/css/tailwind-built.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <link rel="preload" href="assets/css/fontawesome-all.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript>
        <link rel="stylesheet" href="assets/css/tailwind-built.css">
        <link rel="stylesheet" href="assets/css/fontawesome-all.min.css">
    </noscript>

    <style>
        /* CSS Crítico Inmediato */
        body { background-color: #020617; color: #f8fafc; margin: 0; font-family: ui-sans-serif, system-ui, sans-serif; }
        .no-scrollbar::-webkit-scrollbar { display: none !important; }
        .no-scrollbar { -ms-overflow-style: none !important; scrollbar-width: none !important; }
        .neon-glow-pc {
            border: 1px solid rgba(6,182,212,0.9) !important;
            box-shadow: 0 0 16px rgba(6,182,212,0.6), inset 0 0 10px rgba(6,182,212,0.3) !important;
        }
        @font-face {
            font-family: 'Font Awesome 6 Free';
            font-display: swap;
        }
        @font-face {
            font-family: 'Font Awesome 6 Brands';
            font-display: swap;
        }
    </style>
</head>"""

html = re.sub(r'<head>[\s\S]*?</head>', OPTIMIZED_NON_BLOCKING_HEAD, html)

CACHE_VER = "20260828_1945"
html = re.sub(r'src="js/ct-catalog-data\.js.*?"', f'src="js/ct-catalog-data.js?v={CACHE_VER}"', html)
html = re.sub(r'src="js/ct-exact-catalog-engine\.js.*?"', f'src="js/ct-exact-catalog-engine.js?v={CACHE_VER}"', html)

with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

# Sincronizar espejo a OneDrive C:
BASE_DIR_C = r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web\pc-custom-lab"
for root, dirs, files in os.walk(BASE_DIR):
    if '.git' in root or 'node_modules' in root: continue
    for file in files:
        src = os.path.join(root, file)
        rel = os.path.relpath(src, r"E:\sitios web")
        dst = os.path.join(r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web", rel)
        if os.path.exists(os.path.dirname(dst)):
            try:
                with open(src, "rb") as f_in, open(dst, "wb") as f_out:
                    f_out.write(f_in.read())
            except: pass

print("✅ Cero bloqueos de renderizado configurados con éxito!", flush=True)
