# -*- coding: utf-8 -*-
import os
import glob
import re

STORES = [
    'pc-custom-lab',
    'ofertas-y-liquidaciones',
    'bazar-viamx-nfl.gdl',
    'mi-puesto-bazar',
    'kiosco-digital',
    'dulces-bazar',
    'cigarros-bazar',
    '.'
]

for s in STORES:
    if s == '.':
        htmls = [f for f in glob.glob('*.html') if 'backups' not in f]
    else:
        htmls = [f for f in glob.glob(f'{s}/**/*.html', recursive=True) if 'backups' not in f and '.venv' not in f]

    index_file = os.path.join(s, 'index.html')
    canonical = 'N/A'
    base_url = 'N/A'
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if 'canonical' in line.lower():
                    m = re.search(r'href=["\']([^"\']+)["\']', line)
                    if m:
                        canonical = m.group(1)
                        base_url = canonical.rstrip('/') + '/'
                        break

    has_robots = os.path.exists(os.path.join(s, 'robots.txt'))
    has_sitemap = os.path.exists(os.path.join(s, 'sitemap.xml'))
    print(f"=== TIENDA: {s} ===")
    print(f"  Base URL: {base_url}")
    print(f"  HTMLs ({len(htmls)}): {[os.path.relpath(h, s) for h in htmls]}")
    print(f"  robots.txt: {has_robots} | sitemap.xml: {has_sitemap}\n")
