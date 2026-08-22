import os
import glob
import re

STORES = ['ofertas-y-liquidaciones', 'cigarros-bazar', 'dulces-bazar', 'kiosco-digital', 'mi-puesto-bazar']
BASE = r"E:\sitios web"

for s in STORES:
    idx_path = os.path.join(BASE, s, "index.html")
    print(f"\n==================== {s}/index.html ====================")
    with open(idx_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    print(f"File size: {len(content):,} chars")
    
    # 1. Check head tags (fonts, css, preload)
    head_m = re.search(r'<head>([\s\S]*?)</head>', content)
    if head_m:
        head_lines = [l.strip() for l in head_m.group(1).split('\n') if l.strip()]
        print("Head snippet:")
        for l in head_lines[:8]:
            print("  ", l[:100])
            
    # 2. Check headings hierarchy (h1, h2, h3, h4, h5, h6)
    headings = re.findall(r'<(h[1-6])[^>]*>([\s\S]*?)</\1>', content)
    print(f"Headings count: {len(headings)}")
    for htag, htext in headings[:8]:
        clean_t = re.sub(r'<[^>]+>', '', htext).strip()
        print(f"  <{htag}> {clean_t[:60]}")
        
    # 3. Check hero image / banner
    hero_m = re.search(r'<(?:img|picture)[^>]*(?:hero|slider|banner|portada)[^>]*>', content, re.IGNORECASE)
    if hero_m:
        print("Hero/Banner image tag:", hero_m.group(0)[:120])
    else:
        # first 2 img tags
        imgs = re.findall(r'<img[^>]+>', content)
        print(f"First img tags ({len(imgs)} total):")
        for im in imgs[:2]:
            print("  ", im[:120])
