# -*- coding: utf-8 -*-
import os
import re

stores = [
    'pc-custom-lab',
    'ofertas-y-liquidaciones',
    'bazar-viamx-nfl.gdl',
    'mi-puesto-bazar',
    'kiosco-digital',
    'dulces-bazar',
    'cigarros-bazar',
    '.'
]

for s in stores:
    path = os.path.join(s, 'index.html')
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    modals = re.findall(r'id=[\'"]([^\'"]*modal[^\'"]*)[\'"]', content, re.I)
    funcs = [fn for fn in re.findall(r'function\s+([A-Za-z0-9_]+)\s*\(', content) if any(x in fn.lower() for x in ['modal', 'quick', 'detail', 'product'])]
    scripts = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', content)
    
    print(f"=== {s} ===")
    print(f"  Modals en HTML: {modals}")
    print(f"  Funciones en HTML: {funcs}")
    print(f"  Scripts: {scripts}")
    
    # Check if there is an onclick on product cards
    onclicks = re.findall(r'onclick=[\'"]([^\'"]+)[\'"]', content)
    prod_clicks = [c for c in onclicks if any(x in c for x in ['openProduct', 'openQuick', 'Modal', 'quickView'])]
    print(f"  Onclicks de productos ({len(prod_clicks)}): {prod_clicks[:5]}")
