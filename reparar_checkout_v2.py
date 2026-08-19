#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reparar_checkout_v2.py
=====================
Refactorizacion estructural de checkout.html (7 tiendas):
- Imagenes de articulos ampliadas 3X/4X con clases CSS obligatorias
- Folio OXXO de 14 digitos con codigo de barras simulado
- CLABE SPEI actualizada: 012 180 01542584394 9
- Layout tipo tarjeta ancha para articulos del carrito
- Preserva <head>, Tailwind, footers y logica financiera intacta
"""
import os
import re
import sys

BASE = r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web"

STORES = [
    "pc-custom-lab",
    "bazar-viamx-nfl.gdl",
    "cigarros-bazar",
    "dulces-bazar",
    "kiosco-digital",
    "mi-puesto-bazar",
    "ofertas-y-liquidaciones",
]

# =====================================================================
# REGEX: Cart item innerHTML template (matches the full div.innerHTML block)
# =====================================================================
RE_CART_TEMPLATE = re.compile(
    r'div\.innerHTML\s*=\s*`'
    r'\s*<div class="flex items-center gap-2\.5 min-w-0 flex-1">'
    r'\s*<img src="\$\{imgUrl\}"\s+class="w-10 h-10 object-contain bg-white rounded-lg p-0\.5 shrink-0"\s+alt="\$\{item\.nombre\}"\s+loading="lazy"\s*/>'
    r'\s*<div class="min-w-0 flex-1">'
    r'\s*<span class="text-white font-bold block truncate text-xs leading-tight">\$\{item\.nombre\}</span>'
    r'\s*<span class="text-\[9px\] font-mono text-slate-600 uppercase block">\$\{item\.sku\}</span>'
    r'\s*\$\{statusTagHtml\}'
    r'\s*</div>'
    r'\s*</div>'
    r'\s*<div class="flex items-center gap-2 shrink-0">'
    r'\s*\$\{controlsHtml\}'
    r'\s*</div>'
    r'\s*`;',
    re.DOTALL
)

NEW_CART_TEMPLATE = '''div.innerHTML = `
                <img src="${imgUrl}" class="w-44 h-44 md:w-52 md:h-52 min-w-[176px] min-h-[176px] max-w-[208px] max-h-[208px] object-contain rounded-xl bg-slate-950/80 p-2 shrink-0 border border-slate-700/50" alt="${item.nombre}" loading="lazy" />
                <div class="flex-1 flex flex-col gap-2 min-w-0 w-full">
                    <span class="text-white font-bold block text-sm sm:text-base leading-snug">${item.nombre}</span>
                    <span class="text-[10px] font-mono text-slate-500 uppercase block">${item.sku}</span>
                    ${statusTagHtml}
                    <div class="flex items-center gap-3 flex-wrap mt-2">
                        ${controlsHtml}
                    </div>
                </div>
            `;'''

# =====================================================================
# REGEX: generateOxxoFolio function (6-digit -> 14-digit + barcode)
# =====================================================================
RE_OXXO_FN = re.compile(
    r"function generateOxxoFolio\(\)\s*\{"
    r"\s*const folio = 'OX-' \+ Math\.floor\(100000 \+ Math\.random\(\) \* 900000\);"
    r"\s*const el = document\.getElementById\('oxxo-folio'\);"
    r"\s*if \(el\) el\.innerText = folio;"
    r"\s*return folio;"
    r"\s*\}",
    re.DOTALL
)

NEW_OXXO_FN = '''function generateOxxoFolio() {
        const digits = Array.from({length:14}, () => Math.floor(Math.random()*10));
        const folio = digits.join('');
        const el = document.getElementById('oxxo-folio');
        if (el) el.innerText = folio;
        const bc = document.getElementById('oxxo-barcode');
        if (bc) {
            bc.innerHTML = folio.split('').map(function(d, i) {
                var n = parseInt(d) || 0;
                var h = 26 + n * 2;
                var w = (n % 3) + 1;
                return '<div style="width:'+w+'px;height:'+h+'px;background:#f59e0b"></div>';
            }).join('');
            bc.classList.remove('hidden');
        }
        return folio;
    }'''

# =====================================================================
# REGEX: OXXO barcode HTML insertion point
# =====================================================================
RE_OXXO_BARCODE_INSERT = re.compile(
    r'(id="oxxo-folio">---</span>)'
    r'(\s*)'
    r'(<p class="text-\[9px\] text-slate-500 mt-1">)'
)

OXXO_BARCODE_DIV = (
    r'\1\2'
    r'<div id="oxxo-barcode" class="hidden mt-3 flex justify-center items-end gap-[1px] h-14 mx-auto w-full max-w-[220px]"></div>'
    r'\2\3'
)


def patch_file(filepath, store_name):
    """Apply all structural patches to a single checkout.html."""
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    original_size = len(html.encode("utf-8"))
    report = []

    def log(label, count):
        status = "OK" if count > 0 else "SKIP"
        report.append((label, status, count))

    # ── 1. Cart item innerHTML template: 3X/4X images + card layout ──
    count = len(list(RE_CART_TEMPLATE.finditer(html)))
    html = RE_CART_TEMPLATE.sub(NEW_CART_TEMPLATE, html)
    log("innerHTML template 3X/4X images", count)

    # ── 2. Row container class: card-style wide layout ──
    old_row = 'let rowClass = "flex items-center justify-between gap-3 bg-slate-950/40 p-3 rounded-xl border border-slate-800 transition-all duration-300";'
    new_row = 'let rowClass = "flex flex-col sm:flex-row items-center gap-6 p-4 bg-slate-900/70 rounded-2xl border border-slate-800 my-3 transition-all duration-300";'
    c = html.count(old_row)
    html = html.replace(old_row, new_row)
    log("Row container -> card layout", c)

    # ── 3. generateOxxoFolio: 14-digit folio + barcode ──
    count = len(list(RE_OXXO_FN.finditer(html)))
    html = RE_OXXO_FN.sub(NEW_OXXO_FN, html)
    log("OXXO folio 14-digit + barcode JS", count)

    # ── 4. OXXO barcode HTML div insertion (idempotent) ──
    if 'id="oxxo-barcode"' not in html:
        count = len(list(RE_OXXO_BARCODE_INSERT.finditer(html)))
        html = RE_OXXO_BARCODE_INSERT.sub(OXXO_BARCODE_DIV, html)
        log("OXXO barcode HTML div", count)
    else:
        log("OXXO barcode HTML div", 0)

    # ── 5. OXXO folio label update ──
    old_label = '>Folio de Referencia</span>'
    new_label = '>Folio de Referencia (14 d\u00edgitos)</span>'
    if old_label in html:
        c = html.count(old_label)
        html = html.replace(old_label, new_label)
        log("OXXO folio label (14 digitos)", c)
    else:
        log("OXXO folio label (14 digitos)", 0)

    # ── 6. SPEI CLABE update ──
    old_clabe = "0121 8001 5847 6329 04"
    new_clabe = "012 180 01542584394 9"
    c = html.count(old_clabe)
    html = html.replace(old_clabe, new_clabe)
    log("SPEI CLABE actualizada", c)

    # ── 7. Cart items scroll container: increase max-height for larger cards ──
    old_scroll = 'max-h-[45vh]'
    new_scroll = 'max-h-[70vh]'
    c = html.count(old_scroll)
    html = html.replace(old_scroll, new_scroll)
    log("Cart scroll max-height 70vh", c)

    # ── WRITE ──
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    new_size = os.path.getsize(filepath)

    # Print report
    print(f"\n{'='*60}")
    print(f"  {store_name}/checkout.html")
    print(f"  Original: {original_size:,} bytes -> Nuevo: {new_size:,} bytes")
    print(f"{'='*60}")
    for label, status, count in report:
        marker = "[+]" if status == "OK" else "[ ]"
        print(f"  {marker} {label} ({count}x)")

    return new_size


def main():
    print("=" * 60)
    print("  REPARACION CHECKOUT V2")
    print("  Imagenes 3X/4X + Pagos completos + Barcode OXXO")
    print("=" * 60)

    results = []
    for store in STORES:
        fp = os.path.join(BASE, store, "checkout.html")
        if os.path.exists(fp):
            sz = patch_file(fp, store)
            results.append((store, "OK", sz))
        else:
            print(f"\n  SKIP: {store}/checkout.html not found")
            results.append((store, "SKIP", 0))

    print(f"\n{'='*60}")
    print("  REPORTE FINAL")
    print(f"{'='*60}")
    print(f"{'Tienda':<30} {'Estado':<8} {'Bytes':>10}")
    print("-" * 50)
    for name, status, size in results:
        print(f"{name:<30} {status:<8} {size:>10,}")
    ok = sum(1 for _, s, _ in results if s == "OK")
    print("-" * 50)
    print(f"Total: {ok}/7 archivos actualizados")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
