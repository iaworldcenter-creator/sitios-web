with open(r"d:\Downloads\Proyecto Web\index.html", 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Look for controls like filter-price-range, category-select, sort-select, city-filter
controls = ['filter-price-range', 'category-select', 'sort-select', 'city-filter']
for c in controls:
    idx = content.find(c)
    if idx != -1:
        print(f"\n=== Found control: {c} ===")
        print(content[idx-100:idx+400])
