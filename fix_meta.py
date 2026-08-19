import os, re
BASE = r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web"
CORRECT_TAG = '<meta name="google-site-verification" content="BwSy5nNuFFrHJUtxe189nJtPxM4h5QY-SxK1V8wqYDE" />'

FILES = [
    os.path.join(BASE, "index.html"),
    os.path.join(BASE, "pc-custom-lab", "index.html"),
    os.path.join(BASE, "bazar-viamx-nfl.gdl", "index.html"),
    os.path.join(BASE, "cigarros-bazar", "index.html"),
    os.path.join(BASE, "dulces-bazar", "index.html"),
    os.path.join(BASE, "kiosco-digital", "index.html"),
    os.path.join(BASE, "mi-puesto-bazar", "index.html"),
    os.path.join(BASE, "ofertas-y-liquidaciones", "index.html"),
]

for fp in FILES:
    name = fp.replace(BASE + os.sep, "")
    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()

    # Remove any existing google-site-verification tag (any content value)
    html_clean = re.sub(r'[ \t]*<meta\s+name=["\']google-site-verification["\'][^>]*/?>[ \t]*\n?', '', html)

    # Insert the correct tag right after <head...>
    html_new = re.sub(r'(<head[^>]*>)', r'\1\n    ' + CORRECT_TAG, html_clean, count=1)

    if html_new != html:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(html_new)
        print(f"  [FIXED] {name}")
    else:
        print(f"  [OK]    {name}")

print("Done: 8 archivos verificados")
