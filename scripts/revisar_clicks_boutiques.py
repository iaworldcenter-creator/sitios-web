# -*- coding: utf-8 -*-
import re

stores = [
    'ofertas-y-liquidaciones',
    'bazar-viamx-nfl.gdl',
    'kiosco-digital',
    'dulces-bazar',
    'cigarros-bazar'
]

for s in stores:
    path = f'{s}/index.html'
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        txt = f.read()
    clicks = re.findall(r'onclick=["\']([^"\']*openProductDetailModal[^"\']*)["\']', txt)
    print(f"=== {s} ===")
    for c in clicks:
        print("  Click handler:", c[:100])
