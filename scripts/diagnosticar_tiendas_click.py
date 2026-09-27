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
        html = f.read()
    
    # check what global variables are declared
    vars_found = re.findall(r'(?:const|let|var|window\.)\s*([a-zA-Z0-9_]+)\s*=\s*\[', html)
    print(f"=== {s} ===")
    print("  Arrays in HTML:", [v for v in vars_found if any(k in v.lower() for k in ['product', 'item', 'catalog', 'invent', 'boutique', 'local'])])
    
    # Check card rendering templates in HTML or JS
    for m in re.finditer(r'onclick=[\'"]([^\'"]*(?:openProductDetailModal|openQuickView)[^\'"]*)[\'"]', html):
        print("  HTML card click:", m.group(1)[:100])
        break

    # If no inline onclick in HTML, look in js files of that store
    js_dir = os.path.join(s, 'js')
    if os.path.exists(js_dir):
        for jf in os.listdir(js_dir):
            if jf.endswith('.js') and jf not in ['shared-product-modal.js', 'shared-flyout.js', 'shared-instant-search.js', 'shared-cart-whatsapp.js']:
                jp = os.path.join(js_dir, jf)
                with open(jp, 'r', encoding='utf-8', errors='ignore') as fjs:
                    jtxt = fjs.read()
                    clicks = re.findall(r'onclick=[\'"]([^\'"]*(?:openProductDetailModal|openQuickView)[^\'"]*)[\'"]', jtxt)
                    if clicks:
                        print(f"  In {jf}: clicks ({len(clicks)}), sample:", clicks[0][:100])
