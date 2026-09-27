# -*- coding: utf-8 -*-
import os
import re
import json

BASE_DIR = r"d:\Proyectos\sitios web"
stores = [
    "pc-custom-lab",
    "ofertas-y-liquidaciones",
    "bazar-viamx-nfl.gdl",
    "mi-puesto-bazar",
    "kiosco-digital",
    "dulces-bazar",
    "cigarros-bazar",
    "."
]

print("=" * 80)
print("AUDITORÍA DE ARMONÍA EN LOS 8 SITIOS DEL ECOSISTEMA VECTEC")
print("=" * 80)

for s in stores:
    s_dir = os.path.join(BASE_DIR, s)
    idx_path = os.path.join(s_dir, "index.html")
    data_dir = os.path.join(s_dir, "data")
    js_dir = os.path.join(s_dir, "js")
    
    has_idx = os.path.exists(idx_path)
    has_data = os.path.exists(data_dir)
    has_js = os.path.exists(js_dir)
    has_modal_js = os.path.exists(os.path.join(js_dir, "shared-product-modal.js"))
    has_cart_js = os.path.exists(os.path.join(js_dir, "shared-cart-whatsapp.js"))
    has_search_js = os.path.exists(os.path.join(js_dir, "shared-instant-search.js"))
    has_inv = os.path.exists(os.path.join(data_dir, "inventario_maestro_buscador.json"))
    has_compact = os.path.exists(os.path.join(data_dir, "catalogo_maestro_compact.json"))
    has_depts = os.path.exists(os.path.join(data_dir, "departments"))
    
    title = "N/A"
    modal_in_html = False
    open_in_html = False
    if has_idx:
        with open(idx_path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()
        m_title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
        if m_title:
            title = m_title.group(1).strip()
        modal_in_html = "shared-product-modal" in html
        open_in_html = "openProductDetailModal" in html or "openQuickView" in html
        fetches = re.findall(r"fetch\(['\"]([^'\"]+)['\"]\)", html)
        catalog_refs = [f for f in fetches if "json" in f or "data" in f]
        scripts = re.findall(r"<script[^>]*src=['\"]([^'\"]+)['\"]", html)
    
    card_clicks = []
    if has_idx:
        card_clicks = [m for m in re.findall(r"onclick=['\"]([^'\"]+)['\"]", html) if any(k in m for k in ['openProduct', 'openQuick', 'Modal', 'producto.html'])]

    modal_md5 = "N/A"
    has_scoped_css = False
    if has_modal_js:
        import hashlib
        with open(os.path.join(js_dir, "shared-product-modal.js"), "rb") as fm:
            raw = fm.read()
            modal_md5 = hashlib.md5(raw).hexdigest()[:10]
            has_scoped_css = b"vectec-pdp-modal-styles" in raw

    window_exposed = False
    if has_idx:
        with open(idx_path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()
        window_exposed = any(k in html for k in [
            "window.boutiqueProducts", "window.localProducts", "window.masterItems", "window.CT_CATALOG_DATA", "window.CT_CATALOG_DATA_INITIAL"
        ])
        if not window_exposed and has_js:
            for jf in os.listdir(js_dir):
                if jf.endswith(".js"):
                    with open(os.path.join(js_dir, jf), "r", encoding="utf-8", errors="ignore") as fjs:
                        if any(k in fjs.read() for k in ["window.CT_CATALOG_DATA_INITIAL", "window.CT_CATALOG_DATA", "window.boutiqueProducts"]):
                            window_exposed = True
                            break

    print(f"\n[SITIO] {s}")
    print(f"  Título: {title}")
    print(f"  index.html: {has_idx} | data/: {has_data} | js/: {has_js}")
    print(f"  Modal 3-Cols Scoped CSS: {has_scoped_css} | Modal MD5: {modal_md5}")
    print(f"  shared-product-modal.js en js/: {has_modal_js} | Incluido en HTML: {modal_in_html}")
    print(f"  Card onclicks encontrados ({len(card_clicks)}): {card_clicks[:3]}")
    print(f"  Catálogo expuesto en window: {window_exposed}")
    print(f"  Data: inventario={has_inv} | compact={has_compact} | departments/={has_depts}")

print("\n" + "=" * 80)
