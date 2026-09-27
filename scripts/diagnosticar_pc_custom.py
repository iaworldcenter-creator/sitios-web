# -*- coding: utf-8 -*-
with open('pc-custom-lab/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', text)
for s in scripts:
    print('pc-custom-lab script:', s)
