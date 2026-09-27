# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Root index.html scripts:")
for s in re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', text):
    print(" ", s)

print("\nRoot index.html functions:")
for fn in re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', text):
    print(" ", fn)

print("\nRoot index.html product card clicks:")
for m in re.finditer(r'onclick=[\'"]([^\'"]+)[\'"]', text):
    c = m.group(1)
    if any(k in c for k in ['open', 'Modal', 'Product', 'addToCart', 'buyNow']):
        print(" ", c[:100])
