import os, re, subprocess

BASE_DIR = r"E:\sitios web"
STORES = [
    "pc-custom-lab", "cigarros-bazar", "dulces-bazar",
    "kiosco-digital", "mi-puesto-bazar", "ofertas-y-liquidaciones",
    "bazar-viamx-nfl.gdl"
]

HTML_FILES = ["index.html", "producto.html", "checkout.html"]
CSS_INJECTION = '<link rel="stylesheet" href="assets/css/tailwind-built.css?v=1.1.0" />\n<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />'
BODY_CLASSES = 'class="bg-slate-950 text-slate-100 font-sans antialiased overflow-x-hidden"'

for store in STORES:
    store_dir = os.path.join(BASE_DIR, store)
    for filename in HTML_FILES:
        filepath = os.path.join(store_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()

        # Limpiar enlaces asíncronos o preloads rotos
        html = re.sub(r'<link\s+[^>]*tailwind-built\.css[^>]*>', '', html, flags=re.IGNORECASE)
        html = re.sub(r'<link\s+[^>]*font-awesome[^>]*>', '', html, flags=re.IGNORECASE)
        html = re.sub(r'<link\s+[^>]*fontawesome[^>]*>', '', html, flags=re.IGNORECASE)
        html = re.sub(r'<noscript>\s*<link[^>]*>\s*</noscript>', '', html, flags=re.IGNORECASE)

        # Inserción síncrona en el <head>
        if "</head>" in html:
            html = re.sub(r'(</head>)', f'{CSS_INJECTION}\n\\1', html, count=1, flags=re.IGNORECASE)

        # Asegurar clases globales en <body>
        if re.search(r'<body[^>]*class="[^"]*"', html, flags=re.IGNORECASE):
            html = re.sub(r'<body([^>]*)class="[^"]*"', f'<body\\1{BODY_CLASSES}', html, flags=re.IGNORECASE)
        elif '<body' in html:
            html = re.sub(r'<body', f'<body {BODY_CLASSES}', html, count=1, flags=re.IGNORECASE)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[OK] Estilos restaurados en: {store}/{filename}")

print("Restauración local completada.")
