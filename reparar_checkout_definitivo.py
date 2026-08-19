#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reparar_checkout_definitivo.py
==============================
Correccion critica de checkout.html en 7 tiendas:
1. Paso 2 (Metodos de Pago): Remover hidden y opacity-60 para que los
   4 metodos sean visibles desde el inicio con formularios funcionales.
2. Paso 3 (Carrito): Imagenes contenidas estrictamente a 150px con inline
   styles, onerror fallback, y layout flex-row fijo.
3. OXXO: Folio 14 digitos con formato de guiones (XXXX-XXXX-XXXX-XX).
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
# REGEX: Match ANY version of the cart item innerHTML template
# Anchored on div.innerHTML = `...${controlsHtml}...`;
# Works for both original and v2-patched files.
# =====================================================================
RE_CART_INNER = re.compile(
    r'div\.innerHTML\s*=\s*`[\s\S]*?\$\{controlsHtml\}[\s\S]*?`;'
)

NEW_CART_INNER = '''div.innerHTML = `
                <img src="${imgUrl}" style="width:150px;height:150px;min-width:150px;max-width:150px;max-height:150px;object-fit:contain;" class="bg-slate-950 p-2 rounded-xl border border-slate-700 shrink-0" alt="${item.nombre}" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='flex';" />
                <div style="display:none;width:150px;height:150px;min-width:150px" class="bg-slate-900 rounded-xl border border-slate-700 items-center justify-center shrink-0">
                    <i class="fa-solid fa-image text-slate-600 text-3xl"></i>
                </div>
                <div class="flex-1 flex flex-col gap-1.5 min-w-0">
                    <span class="text-white font-bold text-sm leading-snug">${item.nombre}</span>
                    <span class="text-[10px] font-mono text-slate-500 uppercase">${item.sku}</span>
                    ${statusTagHtml}
                    <div class="flex items-center gap-3 flex-wrap mt-1">
                        ${controlsHtml}
                    </div>
                </div>
            `;'''

# New row class: always flex-row, fixed gap, contained card
NEW_ROW_CLASS = 'let rowClass = "flex flex-row items-center gap-4 p-4 bg-slate-900/80 rounded-xl border border-slate-800 mb-3 transition-all duration-300";'

# All known row class variants (original + v2 patch)
ROW_CLASS_VARIANTS = [
    'let rowClass = "flex items-center justify-between gap-3 bg-slate-950/40 p-3 rounded-xl border border-slate-800 transition-all duration-300";',
    'let rowClass = "flex flex-col sm:flex-row items-center gap-6 p-4 bg-slate-900/70 rounded-2xl border border-slate-800 my-3 transition-all duration-300";',
]


def patch_file(filepath, store_name):
    """Apply all definitive patches to a single checkout.html."""
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    original_bytes = len(html.encode("utf-8"))
    report = []

    def do_replace(old, new, label):
        nonlocal html
        c = html.count(old)
        if c > 0:
            html = html.replace(old, new)
        report.append((label, c))
        return c

    # =================================================================
    # FIX 1: PASO 2 - METODOS DE PAGO VISIBLES
    # =================================================================

    # 1a. Remove opacity-60 from payment card container
    do_replace(
        'opacity-60 flex flex-col gap-4" id="step-payment-card"',
        'flex flex-col gap-4" id="step-payment-card"',
        "Pago: quitar opacity-60",
    )

    # 1b. Remove hidden from payment options (show 4 methods)
    do_replace(
        'id="payment-options" class="hidden flex flex-col gap-3"',
        'id="payment-options" class="flex flex-col gap-3"',
        "Pago: opciones visibles",
    )

    # 1c. Payment badge: gray -> cyan (active state)
    do_replace(
        'bg-slate-800 text-slate-400 flex items-center justify-center text-xs font-black" id="step-payment-badge"',
        'bg-cyan-500 text-slate-950 flex items-center justify-center text-xs font-black" id="step-payment-badge"',
        "Pago: badge activo cyan",
    )

    # =================================================================
    # FIX 2: PASO 3 - IMAGENES 150px CONTENIDAS + FALLBACK
    # =================================================================

    # 2a. Replace the entire innerHTML template (any version -> definitive)
    count_inner = len(list(RE_CART_INNER.finditer(html)))
    html = RE_CART_INNER.sub(NEW_CART_INNER, html)
    report.append(("Imagenes: 150px inline-style", count_inner))

    # 2b. Replace row container class (any version -> definitive)
    total_row = 0
    for variant in ROW_CLASS_VARIANTS:
        c = html.count(variant)
        if c > 0:
            html = html.replace(variant, NEW_ROW_CLASS)
            total_row += c
    report.append(("Row: flex-row estricto", total_row))

    # 2c. Increase cart scroll area for bigger cards
    for old_h in ["max-h-[45vh]", "max-h-[70vh]"]:
        c = html.count(old_h)
        if c > 0:
            html = html.replace(old_h, "max-h-[75vh]")
            break

    # =================================================================
    # FIX 3: OXXO FOLIO 14 DIGITOS CON GUIONES
    # =================================================================

    # 3a. Replace original 6-digit generator if still present
    do_replace(
        "const folio = 'OX-' + Math.floor(100000 + Math.random() * 900000);",
        "const digits = Array.from({length:14}, () => Math.floor(Math.random()*10));\n        const folio = digits.join('');",
        "OXXO: generador 14 digitos",
    )

    # 3b. Add dash formatting to folio display (idempotent)
    old_display = "if (el) el.innerText = folio;"
    new_display = "if (el) el.innerText = folio.replace(/(\\d{4})(?=\\d)/g, '$1-');"
    if new_display not in html and old_display in html:
        c = html.count(old_display)
        html = html.replace(old_display, new_display)
        report.append(("OXXO: formato guiones", c))
    else:
        report.append(("OXXO: formato guiones", 0))

    # 3c. Ensure barcode HTML div exists
    if 'id="oxxo-barcode"' not in html:
        marker = 'id="oxxo-folio">---</span>'
        if marker in html:
            bc_html = (
                marker
                + '\n                                <div id="oxxo-barcode" class="hidden mt-3 flex justify-center items-end gap-[1px] h-14 mx-auto w-full max-w-[220px]"></div>'
            )
            html = html.replace(marker, bc_html, 1)
            report.append(("OXXO: barcode div", 1))
        else:
            report.append(("OXXO: barcode div", 0))

    # 3d. Update folio label
    do_replace(
        ">Folio de Referencia</span>",
        ">Folio de Referencia (14 d\u00edgitos)</span>",
        "OXXO: label 14 digitos",
    )

    # =================================================================
    # FIX 4: SPEI CLABE (ensure updated)
    # =================================================================
    do_replace(
        "0121 8001 5847 6329 04",
        "012 180 01542584394 9",
        "SPEI: CLABE actualizada",
    )

    # =================================================================
    # WRITE OUTPUT
    # =================================================================
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    new_bytes = os.path.getsize(filepath)

    # Print per-file report
    print(f"\n  {store_name}/checkout.html")
    print(f"  {original_bytes:,} -> {new_bytes:,} bytes")
    for label, count in report:
        marker = "[+]" if count > 0 else "[ ]"
        print(f"    {marker} {label} ({count}x)")

    return new_bytes


def main():
    print("=" * 60)
    print("  REPARACION DEFINITIVA CHECKOUT.HTML")
    print("  Paso2 visible | 150px contenido | OXXO guiones")
    print("=" * 60)

    results = []
    for store in STORES:
        fp = os.path.join(BASE, store, "checkout.html")
        if os.path.exists(fp):
            sz = patch_file(fp, store)
            results.append((store, "OK", sz))
        else:
            print(f"\n  SKIP: {store}/checkout.html no encontrado")
            results.append((store, "SKIP", 0))

    # Final summary
    print(f"\n{'=' * 60}")
    print("  REPORTE FINAL")
    print(f"{'=' * 60}")
    print(f"{'Tienda':<30} {'Estado':<8} {'Bytes':>10}")
    print("-" * 50)
    for name, status, size in results:
        print(f"{name:<30} {status:<8} {size:>10,}")
    ok_count = sum(1 for _, s, _ in results if s == "OK")
    print("-" * 50)
    print(f"Total: {ok_count}/7 archivos corregidos")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
