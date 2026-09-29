# -*- coding: utf-8 -*-
import glob
import os
import re

NEW_TAG = '<meta name="google-site-verification" content="BwSy5nNuFFrHJUtxe189nJtPxM4h5QY-SxK1V8wqYDE" />'
TOKEN = 'BwSy5nNuFFrHJUtxe189nJtPxM4h5QY-SxK1V8wqYDE'

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

    if TOKEN in content:
        already_had.append(h)
        continue

    # Prefer inserting right after existing google-site-verification tag if present
    if 'google-site-verification' in content:
        pattern = r'(<meta\s+name=["\']google-site-verification["\'][^>]*>)'
        replacement = r'\1\n    ' + NEW_TAG
        new_content, count = re.subn(pattern, replacement, content, count=1, flags=re.IGNORECASE)
        if count > 0:
            with open(h, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified.append(h)
            continue

    # Alternatively insert right after viewport meta line
    if '<meta name="viewport"' in content or "<meta name='viewport'" in content:
        pattern = r'(<meta\s+name=["\']viewport["\'][^>]*>)'
        replacement = r'\1\n    <!-- GOOGLE SEARCH CONSOLE VERIFICATION -->\n    ' + NEW_TAG
        new_content, count = re.subn(pattern, replacement, content, count=1, flags=re.IGNORECASE)
        if count > 0:
            with open(h, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified.append(h)
            continue

    # Fallback: insert right after <head>
    if '<head>' in content:
        new_content = content.replace('<head>', '<head>\n    ' + NEW_TAG, 1)
        with open(h, 'w', encoding='utf-8') as f:
            f.write(new_content)
        modified.append(h)

print(f"Total archivos HTML activos procesados: {len(active_html)}")
print(f"Modificados con la nueva etiqueta ({len(modified)}):")
for m in modified:
    print(f"  [+] {m}")
print(f"Ya contaban con la etiqueta: {len(already_had)}")
