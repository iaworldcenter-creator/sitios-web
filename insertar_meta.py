import os, re
BASE = r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web"
META_TAG = '<meta name="google-site-verification" content="BwSy5nNuFFrHJUtxe189nJtPxM4h5QY-SxK1V8wqYDE" />'
STORES = ["pc-custom-lab","bazar-viamx-nfl.gdl","cigarros-bazar","dulces-bazar","kiosco-digital","mi-puesto-bazar","ofertas-y-liquidaciones"]
for s in STORES:
    fp = os.path.join(BASE, s, "index.html")
    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()
    if "google-site-verification" in html:
        print(f"  [SKIP] {s}/index.html (ya existe)")
        continue
    html = re.sub(r"(<head[^>]*>)", r"\1\n    " + META_TAG, html, count=1)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [OK]   {s}/index.html")
print("Done: 7 tiendas procesadas")
