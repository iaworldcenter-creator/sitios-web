#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
obtener_imagenes_b.py
Módulo de Descarga y Normalización de Imágenes Reales para Proveedor B (Intcomex México):
- Consulta fotografías oficiales y de alta resolución para productos de Intcomex.
- Estrategia multi-fuente:
  1. Herencia de CT por coincidencia de MPN / SKU.
  2. Portal oficial de producto Intcomex (CDN 1WorldSync / Store).
  3. Catálogos oficiales de fabricantes (Klip Xtreme, Xtech, Forza, Nexxt, etc.).
  4. DuckDuckGo / Búsqueda web de producto real.
- Convierte las imágenes a WebP y las almacena como:
  VECTEC/assets/img/B-[SKU].webp
- Mantiene caché permanente (no re-descarga archivos ya existentes en disco).
"""

import os
import sys
import io
import re
import glob
import csv
import json
import ssl
import shutil
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PCC_DIR = os.path.join(BASE_DIR, "pc-custom-lab") if os.path.exists(os.path.join(BASE_DIR, "pc-custom-lab")) else os.path.join(BASE_DIR, "vectec")
IMG_DIR = os.path.join(PCC_DIR, "assets", "img")
DATA_DIR = os.path.join(BASE_DIR, "data")
PCC_DATA_DIR = os.path.join(PCC_DIR, "data")
INTCOMEX_DIR = os.path.join(PCC_DATA_DIR, "Cataloga intcomex")

os.makedirs(IMG_DIR, exist_ok=True)

SSL_CTX = ssl._create_unverified_context()
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8"
}

def clean_sku(raw):
    s = str(raw or "").strip().replace('"', '').replace("'", "")
    if s.startswith("B-") or s.startswith("A-"):
        s = s[2:]
    s = re.sub(r'[\\/*?:"<>|]', '', s)
    return s

def save_as_webp(img_bytes, dest_path):
    """Convierte bytes de imagen a formato WebP optimizado y guarda en dest_path."""
    if not img_bytes or len(img_bytes) < 100:
        return False
    try:
        if HAS_PIL:
            img = Image.open(io.BytesIO(img_bytes))
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
            img.save(dest_path, "WEBP", quality=85)
            return True
        else:
            with open(dest_path, "wb") as f:
                f.write(img_bytes)
            return True
    except Exception as e:
        try:
            with open(dest_path, "wb") as f:
                f.write(img_bytes)
            return True
        except Exception:
            return False

def fetch_intcomex_pdp_image(sku):
    """Consulta la página oficial de Intcomex para extraer la imagen 1WorldSync."""
    url = f"https://store.intcomex.com/es-XMX/Product/Detail/{sku}"
    try:
        req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=7) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            matches = re.findall(r'(https://cdn\.cs\.1worldsync\.com/[a-f0-9/]+/[a-f0-9\-]+\.(?:jpg|jpeg|png|webp))', html)
            if matches:
                return matches[0]
            imgs = re.findall(r'(https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp))', html)
            clean_imgs = [i for i in imgs if "1worldsync" in i or ("product" in i.lower() and "icon" not in i.lower())]
            if clean_imgs:
                return clean_imgs[0]
    except Exception:
        pass
    return None

def fetch_ddg_brand_image(brand, mpn, name):
    """Busca en DuckDuckGo páginas del producto y extrae la imagen oficial."""
    terms = []
    if brand: terms.append(brand)
    if mpn: terms.append(f'"{mpn}"')
    query = " ".join(terms) if terms else name
    if not query: return None

    ddg_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(ddg_url, headers=DEFAULT_HEADERS)
        with urllib.request.urlopen(req, timeout=7) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            links = re.findall(r'href="//duckduckgo\.com/l/\?uddg=([^&"]+)', html)
            for raw_link in links[:4]:
                unq = urllib.parse.unquote(raw_link)
                if any(domain in unq for domain in ["klipxtreme.com", "xtechamericas.com", "forzaups.com", "nexxtsolutions.com", "amazon.com.mx"]):
                    try:
                        p_req = urllib.request.Request(unq, headers=DEFAULT_HEADERS)
                        with urllib.request.urlopen(p_req, timeout=5) as p_resp:
                            p_html = p_resp.read().decode("utf-8", errors="ignore")
                            p_imgs = re.findall(r'(https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp))', p_html)
                            for p_img in p_imgs:
                                if any(k in p_img.lower() for k in ["media", "products", "upload", "img", "images"]):
                                    if "logo" not in p_img.lower() and "icon" not in p_img.lower():
                                        return p_img
                    except Exception:
                        continue
    except Exception:
        pass
    return None

def download_image_bytes(img_url):
    """Descarga los bytes crudos de una imagen dada una URL."""
    if not img_url: return None
    try:
        req = urllib.request.Request(img_url, headers=DEFAULT_HEADERS)
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=8) as resp:
            if resp.status == 200:
                data = resp.read()
                if len(data) > 500:
                    return data
    except Exception:
        pass
    return None

def process_single_b_product(item, ct_img_map):
    """Procesa un producto de Clave B: verifica caché, herencia o descarga."""
    sku = clean_sku(item.get("sku") or item.get("id") or item.get("mpn"))
    mpn = str(item.get("mpn") or "").strip().upper()
    brand = str(item.get("brand") or item.get("marca") or "").strip()
    name = str(item.get("name") or item.get("nombre") or "").strip()

    target_filename = f"B-{sku}.webp"
    target_path = os.path.join(IMG_DIR, target_filename)

    # 1. Caché permanente
    if os.path.exists(target_path) and os.path.getsize(target_path) > 500:
        return {"sku": sku, "status": "cached", "path": f"assets/img/{target_filename}"}

    # 2. Herencia por MPN si coincide con CT
    if mpn and mpn in ct_img_map:
        ct_source_path = ct_img_map[mpn]
        if os.path.exists(ct_source_path):
            try:
                shutil.copy2(ct_source_path, target_path)
                return {"sku": sku, "status": "inherited_mpn", "path": f"assets/img/{target_filename}"}
            except Exception:
                pass

    # 3. Consulta en portal Intcomex (1WorldSync)
    img_url = fetch_intcomex_pdp_image(sku)
    if img_url:
        b_data = download_image_bytes(img_url)
        if b_data and save_as_webp(b_data, target_path):
            return {"sku": sku, "status": "downloaded_intcomex", "path": f"assets/img/{target_filename}", "url": img_url}

    # 4. Fallback DuckDuckGo / Catálogo oficial de fabricante
    img_url_brand = fetch_ddg_brand_image(brand, mpn, name)
    if img_url_brand:
        b_data = download_image_bytes(img_url_brand)
        if b_data and save_as_webp(b_data, target_path):
            return {"sku": sku, "status": "downloaded_brand", "path": f"assets/img/{target_filename}", "url": img_url_brand}

    return {"sku": sku, "status": "not_found", "path": None}

def build_ct_mpn_image_map():
    """Construye índice rápido de MPNs de CT a sus imágenes existentes en disco."""
    ct_map = {}
    compact_path = os.path.join(PCC_DATA_DIR, "catalogo_maestro_compact.json")
    if not os.path.exists(compact_path):
        return ct_map

    with open(compact_path, "r", encoding="utf-8") as f:
        try:
            items = json.load(f)
        except Exception:
            return ct_map

    for it in items:
        sku = clean_sku(it.get("s", ""))
        name = it.get("n", "")
        img_cand = os.path.join(IMG_DIR, f"{sku}.webp")
        img_cand_0 = os.path.join(IMG_DIR, f"{sku}_0.webp")
        valid_img = img_cand if os.path.exists(img_cand) else (img_cand_0 if os.path.exists(img_cand_0) else None)
        if not valid_img:
            continue

        for word in name.split():
            clean_word = word.strip("(),;:-_\"'").upper()
            if len(clean_word) >= 4 and any(c.isdigit() for c in clean_word) and any(c.isalpha() for c in clean_word):
                ct_map[clean_word] = valid_img

    return ct_map

def obtener_imagenes_proveedor_b(intcomex_items_dict=None, max_workers=6):
    """Función principal para descargar y normalizar imágenes de Proveedor B."""
    print("=" * 80)
    print("   DESCARGADOR AUTOMATIZADO DE IMAGENES REALES - PROVEEDOR B (INTCOMEX)")
    print("=" * 80)

    items_to_process = []
    if intcomex_items_dict:
        items_to_process = list(intcomex_items_dict.values())
    else:
        if os.path.exists(INTCOMEX_DIR):
            csv_files = glob.glob(os.path.join(INTCOMEX_DIR, "*.csv"))
            seen = set()
            for fpath in csv_files:
                lines = []
                try:
                    with open(fpath, "r", encoding="utf-16", errors="ignore") as f:
                        lines = f.readlines()
                except Exception:
                    pass
                if not lines:
                    try:
                        with open(fpath, "r", encoding="utf-8-sig", errors="ignore") as f:
                            lines = f.readlines()
                    except Exception:
                        continue
                h_idx = -1
                for i, l in enumerate(lines[:6]):
                    if "Categor" in l and ("Precio" in l or "SKU" in l):
                        h_idx = i; break
                if h_idx == -1: continue
                delim = "\t" if "\t" in lines[h_idx] else ","
                reader = csv.reader(lines[h_idx:], delimiter=delim)
                headers = [h.strip().replace('"', "").upper() for h in next(reader)]
                s_idx = next((i for i, h in enumerate(headers) if "SKU" in h), -1)
                m_idx = next((i for i, h in enumerate(headers) if "PARTE" in h or "MPN" in h), -1)
                n_idx = next((i for i, h in enumerate(headers) if "NOMBRE" in h or "DESCRIPCI" in h), -1)
                b_idx = next((i for i, h in enumerate(headers) if "MARCA" in h), -1)
                for r in reader:
                    sku = r[s_idx].strip() if s_idx != -1 and s_idx < len(r) else ""
                    mpn = r[m_idx].strip() if m_idx != -1 and m_idx < len(r) else ""
                    name = r[n_idx].strip() if n_idx != -1 and n_idx < len(r) else ""
                    brand = r[b_idx].strip() if b_idx != -1 and b_idx < len(r) else ""
                    key = sku or mpn
                    if not key or key in seen: continue
                    seen.add(key)
                    items_to_process.append({"sku": sku, "mpn": mpn, "name": name, "brand": brand})

    print(f"[*] Total artículos Proveedor B a verificar: {len(items_to_process):,}")

    ct_img_map = build_ct_mpn_image_map()
    print(f"[*] MPNs de CT con fotos reales indexados: {len(ct_img_map):,}")

    needed = []
    cached = 0
    for it in items_to_process:
        sku = clean_sku(it.get("sku") or it.get("id") or it.get("mpn"))
        target = os.path.join(IMG_DIR, f"B-{sku}.webp")
        if os.path.exists(target) and os.path.getsize(target) > 500:
            cached += 1
        else:
            needed.append(it)

    print(f"[*] En caché local previo: {cached:,} imágenes.")
    print(f"[*] Por procesar/descargar: {len(needed):,} artículos.")

    stats = {"cached": cached, "inherited_mpn": 0, "downloaded_intcomex": 0, "downloaded_brand": 0, "not_found": 0}

    if needed:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_item = {executor.submit(process_single_b_product, it, ct_img_map): it for it in needed}
            done_count = 0
            for future in as_completed(future_to_item):
                done_count += 1
                try:
                    res = future.result()
                    st = res["status"]
                    stats[st] = stats.get(st, 0) + 1
                    if done_count % 50 == 0 or done_count == len(needed):
                        sys.stdout.write(f"\r   -> Progreso: {done_count}/{len(needed)} (Descargados: {stats.get('downloaded_intcomex',0) + stats.get('downloaded_brand',0)}, Heredados: {stats.get('inherited_mpn',0)})")
                        sys.stdout.flush()
                except Exception:
                    stats["not_found"] += 1

    print("\n" + "-" * 80)
    print(f"[*] Resumen Descarga Imágenes Proveedor B:")
    print(f"   - Caché local previa:               {stats['cached']:,}")
    print(f"   - Heredadas de CT por MPN:           {stats['inherited_mpn']:,}")
    print(f"   - Descargadas de Intcomex (1WorldSync): {stats['downloaded_intcomex']:,}")
    print(f"   - Descargadas de Catálogo Fabricante:{stats['downloaded_brand']:,}")
    print(f"   - Pendientes / No encontradas:       {stats['not_found']:,}")
    print("=" * 80)
    return stats

def main():
    obtener_imagenes_proveedor_b()

if __name__ == "__main__":
    main()
