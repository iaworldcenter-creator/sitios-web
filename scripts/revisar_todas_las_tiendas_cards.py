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
    html_path = os.path.join(s, 'index.html')
    if not os.path.exists(html_path):
        print(f"STORE {s}: index.html NOT FOUND")
        continue
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    has_modal_script = 'shared-product-modal.js' in html
    modal_clicks = re.findall(r'onclick=[\'"][^\'"]*openProductDetailModal\([^\'"]*[\'"]', html)
    
    # check js files
    js_clicks = []
    js_dir = os.path.join(s, 'js')
    if os.path.exists(js_dir):
        for jf in os.listdir(js_dir):
            if jf.endswith('.js') and jf != 'shared-product-modal.js':
                with open(os.path.join(js_dir, jf), 'r', encoding='utf-8', errors='ignore') as fjs:
                    jtxt = fjs.read()
                    if 'openProductDetailModal' in jtxt:
                        js_clicks.append(jf)

    # check window assignments
    window_vars = re.findall(r'window\.([a-zA-Z0-9_]+)\s*=', html)
    arrays_declared = re.findall(r'(?:const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*\[', html)

    print(f"\n==================== STORE: {s} ====================")
    print(f"  Includes shared-product-modal.js: {has_modal_script}")
    print(f"  openProductDetailModal in HTML: {len(modal_clicks)}")
    print(f"  openProductDetailModal in JS files: {js_clicks}")
    print(f"  Arrays declared in HTML: {arrays_declared}")
    print(f"  window.* assignments in HTML: {window_vars}")
