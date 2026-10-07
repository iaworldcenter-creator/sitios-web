#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
descargar_imagenes_ct_nuevos.py
Descargador y normalizador de imágenes para los nuevos SKUs de CT Internacional (Semana 1314):
1. Extrae los SKUs nuevos de la lista 1314.
2. Consulta la fotografía oficial vía:
   - Coincidencia local previa / MPN.
   - Portal CT Internacional (Columna L: https://ctonline.mx/buscar/productos?b={sku}).
   - Búsqueda web / catálogo de fabricante (DuckDuckGo).
   - Placeholder temático de alta resolución como respaldo.
3. Convierte cada imagen a formato WebP (calidad 85) normalizada como {sku}.webp en pc-custom-lab/assets/img/.
"""

import os
import sys
import io
import re
import json
import ssl
import shutil
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

BASE_DIR = r"D:\Proyectos\sitios web"
PCC_DIR = os.path.join(BASE_DIR, "pc-custom-lab")
IMG_DIR = os.path.join(PCC_DIR, "assets", "img")
PCC_DATA_DIR = os.path.join(PCC_DIR, "data")
PLACEHOLDERS_DIR = os.path.join(IMG_DIR, "placeholders")
PRICE_XLSX = os.path.join(PCC_DATA_DIR, "1314 LISTA DE PRECIOS DE CT TOL 100526.xlsx")
COMPACT_JSON = os.path.join(PCC_DATA_DIR, "catalogo_maestro_compact.json")

sys.path.insert(0, BASE_DIR)
from scripts.sincronizar_fuente_datos import read_xlsx_workbook, clean_text, clean_sku, infer_brand
from scripts.clasificador_semantico_vectec import clasificar_producto_semantico

os.makedirs(IMG_DIR, exist_ok=True)

SSL_CTX = ssl._create_unverified_context()
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8"
}


def save_as_webp(img_bytes, dest_path, quality=85):
    try:
        with Image.open(io.BytesIO(img_bytes)) as img:
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")
            img.save(dest_path, "WEBP", quality=quality)
            return True
    except Exception as e:
        return False


def download_bytes(url, timeout=7):
    try:
        req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=timeout) as resp:
            data = resp.read()
            if len(data) > 1000:
                return data
    except Exception:
        pass
    return None


def fetch_ct_product_image(sku):
    url = f"https://ctonline.mx/buscar/productos?b={sku}"
    try:
        req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=7) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            # Extraer enlaces de imágenes de productos de CT (CloudFront / ctonline)
            matches = re.findall(r'(https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp))', html)
            for m in matches:
                # Descartar iconos, banners, logos
                m_low = m.lower()
                if any(ign in m_low for ign in ["logo", "banner", "icon", "placeholder", "sprite", "social", "header"]):
                    continue
                if "ctonline" in m_low or "cloudfront" in m_low or "product" in m_low or "art" in m_low or sku.lower() in m_low:
                    return m
            # Si hay alguna imagen de producto genérica
            for m in matches:
                if any(k in m.lower() for k in ["/prod/", "/articulos/", "/img_prod/", "d22px5h6uo995f"]):
                    return m
    except Exception:
        pass
    return None


def fetch_ddg_brand_image(brand, sku, name):
    # Consulta de búsqueda limpia
    query = f"{brand} {sku} {name} producto"
    ddg_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(ddg_url, headers=DEFAULT_HEADERS)
        with urllib.request.urlopen(req, timeout=7) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            cand_urls = re.findall(r'//duckduckgo\.com/l/\?uddg=([^\s"\'&]+)', html)
            for raw_link in cand_urls[:3]:
                unq = urllib.parse.unquote(raw_link)
                if unq.startswith("http") and not any(x in unq for x in ["facebook", "youtube", "tiktok", "instagram"]):
                    try:
                        p_req = urllib.request.Request(unq, headers=DEFAULT_HEADERS)
                        with urllib.request.urlopen(p_req, timeout=5) as p_resp:
                            p_html = p_resp.read().decode("utf-8", errors="ignore")
                            p_imgs = re.findall(r'(https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp))', p_html)
                            for pi in p_imgs:
                                pi_low = pi.lower()
                                if any(ign in pi_low for ign in ["logo", "icon", "banner", "thumb", "avatar"]):
                                    continue
                                if any(x in pi_low for x in ["product", "large", "zoom", "gallery", sku.lower()]):
                                    return pi
                    except Exception:
                        continue
    except Exception:
        pass
    return None


def procesar_sku(item):
    sku = item["sku"]
    name = item["name"]
    brand = item["brand"]
    cat = item["categoria"]

    target_path = os.path.join(IMG_DIR, f"{sku}.webp")
    target_path_0 = os.path.join(IMG_DIR, f"{sku}_0.webp")

    # 1. Ya existe en disco
    if os.path.exists(target_path) and os.path.getsize(target_path) > 500:
        return {"sku": sku, "status": "existente", "path": f"assets/img/{sku}.webp"}
    if os.path.exists(target_path_0) and os.path.getsize(target_path_0) > 500:
        return {"sku": sku, "status": "existente_0", "path": f"assets/img/{sku}_0.webp"}

    # 2. Coincidencia local B-{sku}.webp
    b_cand = os.path.join(IMG_DIR, f"B-{sku}.webp")
    if os.path.exists(b_cand) and os.path.getsize(b_cand) > 500:
        try:
            shutil.copy2(b_cand, target_path)
            return {"sku": sku, "status": "heredado_local", "path": f"assets/img/{sku}.webp"}
        except Exception:
            pass

    # 3. Descarga desde ficha técnica oficial CT (Columna L)
    ct_img_url = fetch_ct_product_image(sku)
    if ct_img_url:
        b_data = download_bytes(ct_img_url)
        if b_data and save_as_webp(b_data, target_path, quality=85):
            return {"sku": sku, "status": "descargado_ct", "path": f"assets/img/{sku}.webp", "url": ct_img_url}

    # 4. Descarga desde catálogo de fabricante / DDG
    brand_img_url = fetch_ddg_brand_image(brand, sku, name)
    if brand_img_url:
        b_data = download_bytes(brand_img_url)
        if b_data and save_as_webp(b_data, target_path, quality=85):
            return {"sku": sku, "status": "descargado_fabricante", "path": f"assets/img/{sku}.webp", "url": brand_img_url}

    # 5. Generación de WebP a partir de placeholder temático
    pl_cand = os.path.join(PLACEHOLDERS_DIR, f"{cat}.jpg")
    if not os.path.exists(pl_cand):
        pl_cand = os.path.join(PLACEHOLDERS_DIR, "acc_placeholder.jpg")

    if os.path.exists(pl_cand):
        try:
            with open(pl_cand, "rb") as pf:
                save_as_webp(pf.read(), target_path, quality=85)
            return {"sku": sku, "status": "placeholder_generado", "path": f"assets/img/{sku}.webp"}
        except Exception:
            pass

    return {"sku": sku, "status": "error", "path": None}


def main():
    print("=" * 80)
    print("   DESCARGADOR Y NORMALIZADOR DE IMAGENES WEBP - PRODUCTOS NUEVOS CT 1314")
    print("=" * 80)

    # Identificar SKUs previos
    old_skus = set()
    if os.path.exists(COMPACT_JSON):
        with open(COMPACT_JSON, "r", encoding="utf-8") as f:
            for x in json.load(f):
                old_skus.add(clean_sku(x.get("s", "")))

    print(f"[*] SKUs previos indexados: {len(old_skus):,}")

    # Parsear lista de precios CT 1314
    price_sheets = read_xlsx_workbook(PRICE_XLSX)
    nuevos_items = []
    seen = set()

    for sname, rows in price_sheets.items():
        if sname in ['LISTA DE PRECIOS', 'INDICE', 'DIRECTORIO', 'DIRECTORIO DE COORDINADORES']:
            continue
        subg = sname
        for r_num, cells in rows:
            f = cells.get('F', '')
            if f.upper() == 'CLAVE' and 'G' in cells:
                subg = clean_text(cells['G'])
                continue
            if f and f.upper() not in ['CLAVE', 'NAN'] and len(f) >= 5:
                raw = clean_sku(f)
                if raw not in old_skus and raw not in seen:
                    seen.add(raw)
                    desc = clean_text(cells.get('G', ''))
                    brand = infer_brand(desc, raw)
                    cat = clasificar_producto_semantico(
                        raw, desc[:120], brand, sheet_name=sname,
                        subgrupo_header=subg, desc=desc
                    )
                    nuevos_items.append({
                        "sku": raw,
                        "name": desc[:120],
                        "brand": brand,
                        "categoria": cat,
                        "desc": desc
                    })

    print(f"[+] Total productos nuevos a procesar en imágenes: {len(nuevos_items)}")

    # Procesar con ThreadPoolExecutor
    stats = {"existente": 0, "existente_0": 0, "heredado_local": 0, "descargado_ct": 0, "descargado_fabricante": 0, "placeholder_generado": 0, "error": 0}
    resultados = []

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(procesar_sku, it): it for it in nuevos_items}
        for future in as_completed(futures):
            res = future.result()
            st = res.get("status", "error")
            stats[st] = stats.get(st, 0) + 1
            resultados.append(res)
            sys.stdout.write(f"\r   -> Progreso: {len(resultados)}/{len(nuevos_items)} (CT/Fabricante: {stats.get('descargado_ct', 0) + stats.get('descargado_fabricante', 0)}, Heredados: {stats.get('heredado_local', 0)}, Placeholders: {stats.get('placeholder_generado', 0)})")
            sys.stdout.flush()

    print("\n\n" + "=" * 80)
    print("   RESUMEN DE PROCESAMIENTO DE IMAGENES WEBP")
    print("=" * 80)
    for k, v in stats.items():
        print(f"   - {k}: {v}")

    # Guardar reporte de imágenes
    out_rep = os.path.join(PCC_DATA_DIR, "reporte_imagenes_1314.json")
    with open(out_rep, "w", encoding="utf-8") as f:
        json.dump({"total": len(nuevos_items), "stats": stats, "detalles": resultados}, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] Reporte detallado guardado en: {out_rep}")


if __name__ == "__main__":
    main()
