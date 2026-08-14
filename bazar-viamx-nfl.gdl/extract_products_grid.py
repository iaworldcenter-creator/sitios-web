with open(r"d:\Downloads\Proyecto Web\index.html", 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Look for products-grid div
idx = content.find('id="products-grid"')
if idx != -1:
    print("Found products-grid in HTML. Printing next 3000 characters:")
    print(content[idx:idx+3000])
else:
    print("products-grid not found in HTML")
