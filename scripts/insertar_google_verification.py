# -*- coding: utf-8 -*-
import glob
import os
import re

TAG = '<meta name="google-site-verification" content="2xIPYIU_imoZjFogZhoFRuepS7PFhXQloOamPV7ex6Q" />'

# Find all html files in active projects (exclude backups and virtual environments)
all_html = glob.glob('**/*.html', recursive=True)
active_html = [
    h for h in all_html 
    if not h.startswith('backups') 
    and '.venv' not in h 
    and 'node_modules' not in h
]

modified = []
already_had = []

for h in active_html:
    with open(h, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    if '2xIPYIU_imoZjFogZhoFRuepS7PFhXQloOamPV7ex6Q' in content:
        already_had.append(h)
        continue

    # Try inserting right after viewport meta line
    if '<meta name="viewport"' in content or "<meta name='viewport'" in content:
        pattern = r'(<meta\s+name=["\']viewport["\'][^>]*>)'
        replacement = r'\1\n    <!-- GOOGLE SEARCH CONSOLE VERIFICATION -->\n    ' + TAG
        new_content, count = re.subn(pattern, replacement, content, count=1, flags=re.IGNORECASE)
        if count > 0:
            with open(h, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified.append(h)
            continue

    # Fallback: insert right after <head>
    if '<head>' in content:
        new_content = content.replace('<head>', '<head>\n    <!-- GOOGLE SEARCH CONSOLE VERIFICATION -->\n    ' + TAG, 1)
        with open(h, 'w', encoding='utf-8') as f:
            f.write(new_content)
        modified.append(h)

print(f"Total active HTML files found: {len(active_html)}")
print(f"Modified with Google Verification tag: {len(modified)}")
for m in modified:
    print(f"  [+] {m}")
print(f"Already had tag: {len(already_had)}")
