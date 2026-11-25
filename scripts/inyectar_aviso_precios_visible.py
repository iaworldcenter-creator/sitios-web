#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inyectar_aviso_precios_visible.py
Inyecta de forma idempotente la barra visible fija (en <header>) de aviso legal
"Precios en MXN sujetos a cambio sin previo aviso por fluctuación cambiaria del dólar y disponibilidad."
en todas las páginas activas de los 8 sitios del ecosistema VECTEC.
"""

import os
import glob

BASE_DIR = r"D:\Proyectos\sitios web"
STORES = [
    ".",
    "pc-custom-lab",
    "bazar-viamx-nfl.gdl",
    "cigarros-bazar",
    "dulces-bazar",
    "kiosco-digital",
    "mi-puesto-bazar",
    "ofertas-y-liquidaciones",
]

MARKER = "<!-- AVISO-LEGAL-PRECIOS-VISIBLE-VECTEC -->"
BANNER_HTML = (
    f"\n        {MARKER}\n"
    '        <div class="w-full bg-amber-500/15 border-t border-amber-500/40 px-3 py-1 text-center text-[10px] sm:text-xs font-mono font-bold text-amber-300 tracking-wide">\n'
    '            <i class="fa-solid fa-triangle-exclamation text-amber-400 mr-1"></i>\n'
    '            Precios en MXN sujetos a cambio sin previo aviso por fluctuación cambiaria del dólar y disponibilidad de inventario.\n'
    '        </div>\n'
)


def main():
    updated = []
    skipped = []
    for sub in STORES:
        folder = os.path.join(BASE_DIR, sub)
        for fpath in sorted(glob.glob(os.path.join(folder, "*.html"))):
            bname = os.path.basename(fpath)
            if bname.startswith("prototipo_"):
                continue
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if MARKER in content:
                skipped.append(f"{sub}/{bname} (already injected)")
                continue
            idx = content.find("</header>")
            if idx == -1:
                skipped.append(f"{sub}/{bname} (no </header>)")
                continue
            new_content = content[:idx] + BANNER_HTML + "    " + content[idx:]
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated.append(f"{sub}/{bname}")

    print(f"[OK] Aviso legal visible inyectado en {len(updated)} paginas HTML:")
    for u in updated:
        print(f"  + {u}")
    if skipped:
        print(f"[*] Omitidas ({len(skipped)}): {skipped[:10]}")


if __name__ == "__main__":
    main()
