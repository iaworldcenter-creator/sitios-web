# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath('.'))
import json
from scripts.clasificador_semantico_vectec import clasificar_producto_semantico

with open('data/catalogo_maestro_compact.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

for p in cat:
    sku = p.get('sku') or p.get('s') or ''
    if any(k in sku for k in ['GABACT340', 'GABNCB350', 'GABBLR810']):
        n = p.get('nombre') or p.get('n') or ''
        c = clasificar_producto_semantico(sku, n, '')
        print(f"SKU: {sku}")
        print(f"Name: {n}")
        print(f"Current cat in compact: {p.get('categoria')}")
        print(f"Classified as: {c}")
        print("-" * 60)
