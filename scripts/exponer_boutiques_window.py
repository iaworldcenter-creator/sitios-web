# -*- coding: utf-8 -*-
import os

stores = [
    'ofertas-y-liquidaciones',
    'bazar-viamx-nfl.gdl',
    'kiosco-digital',
    'dulces-bazar',
    'cigarros-bazar'
]

for s in stores:
    path = os.path.join(s, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    target = "let filteredProducts = [...boutiqueProducts];"
    replacement = "let filteredProducts = [...boutiqueProducts];\n    window.boutiqueProducts = boutiqueProducts;\n    window.filteredProducts = filteredProducts;"

    if "window.boutiqueProducts = boutiqueProducts;" not in html:
        if target in html:
            html = html.replace(target, replacement, 1)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Updated {s}: window.boutiqueProducts exposed.")
        else:
            print(f"Target not found in {s}")
    else:
        print(f"Already exposed in {s}")
