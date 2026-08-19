#!/usr/bin/env python3
"""
propagar_checkout.py
====================
Replica el MOLDE MAESTRO de pc-custom-lab/checkout.html hacia las 6 tiendas
del ecosistema, adaptando dinámicamente nombre de tienda, logotipos, enlaces
de navegación y catálogo de productos para cada carpeta.

Reglas implementadas:
1. Estructura 2 columnas idéntica: Paso1 Domicilio → Paso2 Acordeón 4 métodos
   de pago → Paso3 Artículos | Columna derecha: Resumen financiero en tiempo real.
2. Adaptación dinámica de branding por tienda.
3. Sincronización asimétrica: todas usan ecosystem_global_cart en localStorage.
4. Etiquetas <head> y clases compiladas se mantienen intactas, solo se adaptan
   textos de identidad.
"""

import os
import re
import shutil

# ── CONFIGURACIÓN ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_FILE = os.path.join(BASE_DIR, "pc-custom-lab", "checkout.html")

STORES = {
    "bazar-viamx-nfl.gdl": {
        "display_name": "VíaMX",
        "header_name": "VÍAMX",
        "title": "VíaMX | Curaduría Internacional de Artículos Elite",
        "description": "En VíaMX seleccionamos meticulosamente los artículos más prestigiosos e indispensables para tu estilo de vida.",
        "logo_url": "https://viamx.pro/images/viamx_eagle_mascot.png",
        "og_image": "https://viamx.pro/images/viamx_eagle_mascot.png",
        "site_url": "https://iaworldcenter-creator.github.io/bazar-viamx-nfl.gdl/",
        "schema_type": "Store",
        "footer_text": "© 2026 VíaMX. Curaduría Internacional de Artículos Elite. Todos los derechos reservados.",
    },
    "cigarros-bazar": {
        "display_name": "Cigarros Bazar",
        "header_name": "CIGARROS BAZAR",
        "title": "Cigarros & Tabaco | Puesto de Revistas y Bazar",
        "description": "Cigarros, tabaco y accesorios premium con entrega local express en Guadalajara Centro.",
        "logo_url": "https://iaworldcenter-creator.github.io/cigarros-bazar/assets/img/mascota_tigre.webp",
        "og_image": "https://iaworldcenter-creator.github.io/cigarros-bazar/assets/img/mascota_tigre.webp",
        "site_url": "https://iaworldcenter-creator.github.io/cigarros-bazar/",
        "schema_type": "Store",
        "footer_text": "© 2026 Cigarros Bazar. Pedro Moreno 501 A, Guadalajara Centro. Todos los derechos reservados.",
    },
    "dulces-bazar": {
        "display_name": "Dulces Bazar",
        "header_name": "DULCES BAZAR",
        "title": "Dulcería & Botanas | Puesto de Revistas y Bazar",
        "description": "Dulces, botanas, chocolates y golosinas con entrega local express en Guadalajara Centro.",
        "logo_url": "https://iaworldcenter-creator.github.io/dulces-bazar/assets/img/mascota_tigre.webp",
        "og_image": "https://iaworldcenter-creator.github.io/dulces-bazar/assets/img/mascota_tigre.webp",
        "site_url": "https://iaworldcenter-creator.github.io/dulces-bazar/",
        "schema_type": "Store",
        "footer_text": "© 2026 Dulces Bazar. Pedro Moreno 501 A, Guadalajara Centro. Todos los derechos reservados.",
    },
    "kiosco-digital": {
        "display_name": "Kiosco Digital",
        "header_name": "KIOSCO DIGITAL",
        "title": "Kiosco Digital | Revistas, Periódicos y Lectura",
        "description": "Revistas, periódicos, libros y contenido digital con entrega local express en Guadalajara Centro.",
        "logo_url": "https://iaworldcenter-creator.github.io/kiosco-digital/assets/img/mascota_tigre.webp",
        "og_image": "https://iaworldcenter-creator.github.io/kiosco-digital/assets/img/mascota_tigre.webp",
        "site_url": "https://iaworldcenter-creator.github.io/kiosco-digital/",
        "schema_type": "Store",
        "footer_text": "© 2026 Kiosco Digital. Pedro Moreno 501 A, Guadalajara Centro. Todos los derechos reservados.",
    },
    "mi-puesto-bazar": {
        "display_name": "Puesto Bazar",
        "header_name": "PUESTO BAZAR",
        "title": "Mi Puesto Periódicos y Bazar | Venta y Catálogo en Guadalajara",
        "description": "Tu puesto de periódicos, revistas y bazar con entrega local express en Guadalajara Centro.",
        "logo_url": "https://iaworldcenter-creator.github.io/mi-puesto-bazar/assets/img/mascota_tigre.webp",
        "og_image": "https://iaworldcenter-creator.github.io/mi-puesto-bazar/assets/img/mascota_tigre.webp",
        "site_url": "https://iaworldcenter-creator.github.io/mi-puesto-bazar/",
        "schema_type": "Store",
        "footer_text": "© 2026 Puesto Bazar. Pedro Moreno 501 A, Guadalajara Centro. Todos los derechos reservados.",
    },
    "ofertas-y-liquidaciones": {
        "display_name": "Liquidaciones y Ofertas",
        "header_name": "LIQUIDACIONES Y OFERTAS",
        "title": "Ofertas y Liquidaciones Anti-Gravity | Tienda de Descuentos Outlet Guadalajara",
        "description": "Ofertas, liquidaciones y descuentos outlet con entrega local express en Guadalajara Centro.",
        "logo_url": "https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones/assets/img/mascota_tigre.webp",
        "og_image": "https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones/assets/img/mascota_tigre.webp",
        "site_url": "https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones/",
        "schema_type": "Store",
        "footer_text": "© 2026 Liquidaciones y Ofertas. Pedro Moreno 501 A, Guadalajara Centro. Todos los derechos reservados.",
    },
}


def read_master():
    """Lee el molde maestro completo."""
    with open(MASTER_FILE, "r", encoding="utf-8") as f:
        return f.read()


def adapt_checkout(master_html: str, folder_name: str, store_cfg: dict) -> str:
    """
    Adapta el HTML maestro para una tienda específica.
    Sustituye branding sin alterar estructura, clases ni lógica de checkout.
    """
    html = master_html

    # ── 1. <title> ──────────────────────────────────────────────────────────
    html = re.sub(
        r"<title>.*?</title>",
        f"<title>{store_cfg['title']}</title>",
        html,
        count=1,
    )

    # ── 2. Meta description ────────────────────────────────────────────────
    html = re.sub(
        r'(<meta\s+content=")([^"]*?)("\s+name="description"\s*/>)',
        rf'\g<1>{store_cfg["description"]}\3',
        html,
        count=1,
    )

    # ── 3. Open Graph meta tags ────────────────────────────────────────────
    html = re.sub(
        r'(<meta\s+content=")([^"]*?)("\s+property="og:title"\s*>)',
        rf'\g<1>{store_cfg["title"]}\3',
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta\s+content=")([^"]*?)("\s+property="og:description"\s*>)',
        rf'\g<1>{store_cfg["description"]}\3',
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta\s+content=")([^"]*?)("\s+property="og:image"\s*/?>)',
        rf'\g<1>{store_cfg["og_image"]}\3',
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta\s+content=")([^"]*?)("\s+property="og:url"\s*/?>)',
        rf'\g<1>{store_cfg["site_url"]}\3',
        html,
        count=1,
    )

    # ── 4. Schema.org JSON-LD ──────────────────────────────────────────────
    html = re.sub(
        r'"name":\s*"PC Custom Lab"',
        f'"name": "{store_cfg["display_name"]}"',
        html,
    )
    html = re.sub(
        r'"@type":\s*"ComputerStore"',
        f'"@type": "{store_cfg["schema_type"]}"',
        html,
        count=1,
    )
    html = re.sub(
        r'("image":\s*")[^"]*(")',
        rf'\g<1>{store_cfg["og_image"]}\2',
        html,
        count=1,
    )
    html = re.sub(
        r'("url":\s*")[^"]*(")',
        rf'\g<1>{store_cfg["site_url"]}\2',
        html,
        count=1,
    )

    # ── 5. Header logo image ──────────────────────────────────────────────
    html = re.sub(
        r'(<img\s+alt="Logo Oficial Anti-Gravity"[^>]*src=")[^"]*("[^>]*/>)',
        rf'\g<1>{store_cfg["logo_url"]}\2',
        html,
        count=1,
    )

    # ── 6. Header store name text ─────────────────────────────────────────
    html = re.sub(
        r"(text-xl md:text-2xl font-black text-white tracking-wider uppercase\">)PC CUSTOM LAB(</span>)",
        rf"\g<1>{store_cfg['header_name']}\2",
        html,
    )

    # ── 7. Footer ─────────────────────────────────────────────────────────
    html = re.sub(
        r"(<footer[^>]*>)\s*<p>.*?</p>",
        rf"\g<1>\n<p>{store_cfg['footer_text']}</p>",
        html,
        count=1,
    )

    # ── 8. Purchase completion alert ──────────────────────────────────────
    html = html.replace(
        "Gracias por tu compra en PC Custom Lab.",
        f"Gracias por tu compra en {store_cfg['display_name']}.",
    )

    # ── 9. Chatbot greeting ───────────────────────────────────────────────
    # Keep it generic - already says "Ecosistema de Tiendas"

    # ── 10. SPEI beneficiary ──────────────────────────────────────────────
    html = re.sub(
        r'(<span class="text-white font-bold">)PC Custom Lab(</span>\s*</div>\s*<div class="flex justify-between"><span class="text-slate-500">Referencia:)',
        rf"\g<1>{store_cfg['display_name']}\2",
        html,
        count=1,
    )

    # ── 11. path detection in JS (isPcCustomLab) ──────────────────────────
    html = html.replace(
        'window.location.pathname.includes("pc-custom-lab")',
        f'window.location.pathname.includes("{folder_name}")',
    )

    # ── 12. Guarantee/support footer banner text adaptation ───────────────
    html = html.replace(
        "Soporte y garantía en Pedro Moreno 501 A, Centro GDL.",
        f"Soporte y garantía de {store_cfg['display_name']} en Pedro Moreno 501 A, Centro GDL.",
    )

    # ── 13. Remove pc-custom-lab productCatalog (not needed for other stores) ──
    # Each store reads from ecosystem_global_cart (localStorage) which is
    # populated from their own index.html catalogs. The checkout only renders
    # items already in the cart, so the productCatalog block can be replaced
    # with an empty array to keep the file light.
    html = re.sub(
        r"(const productCatalog = )\[[\s\S]*?\];",
        r"\1[];  // Products loaded from each store's index.html into ecosystem_global_cart",
        html,
        count=1,
    )

    # ── 14. Image path adaptation ─────────────────────────────────────────
    # For stores using mascota_tigre.webp from their own assets
    if "mascota_tigre" in store_cfg["logo_url"]:
        html = re.sub(
            r'(assets/img/)slider_ia_human\.webp',
            r'\1mascota_tigre.webp',
            html,
        )

    # ── 15. Ensure the checkout opens relative index.html ─────────────────
    # All links to index.html are already relative - no changes needed

    return html


def propagate():
    """Ejecuta la propagación completa."""
    print("=" * 70)
    print("  PROPAGACIÓN AUTOMATIZADA DE CHECKOUT.HTML")
    print("  Molde Maestro: pc-custom-lab/checkout.html")
    print("=" * 70)

    if not os.path.exists(MASTER_FILE):
        print(f"\n❌ ERROR: No se encontró el molde maestro en:\n   {MASTER_FILE}")
        return False

    master_html = read_master()
    master_size = len(master_html.encode("utf-8"))
    print(f"\n📄 Molde maestro leído: {master_size:,} bytes ({master_html.count(chr(10))+1} líneas)")

    results = []

    for folder_name, store_cfg in STORES.items():
        store_dir = os.path.join(BASE_DIR, folder_name)
        target_file = os.path.join(store_dir, "checkout.html")

        if not os.path.isdir(store_dir):
            print(f"\n⚠️  SKIP: Carpeta no encontrada → {folder_name}/")
            results.append((folder_name, "SKIP", 0))
            continue

        # Backup existing checkout.html if present
        if os.path.exists(target_file):
            backup_path = target_file + ".bak"
            shutil.copy2(target_file, backup_path)

        # Adapt and write
        adapted_html = adapt_checkout(master_html, folder_name, store_cfg)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(adapted_html)

        written_size = os.path.getsize(target_file)
        results.append((folder_name, "OK", written_size))
        print(f"\n✅ {folder_name}/checkout.html")
        print(f"   → Tienda: {store_cfg['display_name']}")
        print(f"   → Logo: {store_cfg['logo_url'][:60]}...")
        print(f"   → Tamaño: {written_size:,} bytes")

    # ── REPORTE FINAL ─────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("  REPORTE DE PROPAGACIÓN")
    print("=" * 70)
    print(f"{'Tienda':<30} {'Estado':<10} {'Bytes':>10}")
    print("-" * 50)
    for name, status, size in results:
        print(f"{name:<30} {status:<10} {size:>10,}")
    
    ok_count = sum(1 for _, s, _ in results if s == "OK")
    skip_count = sum(1 for _, s, _ in results if s == "SKIP")
    print("-" * 50)
    print(f"Total: {ok_count} exitosos, {skip_count} omitidos")
    print("=" * 70)

    return ok_count > 0


if __name__ == "__main__":
    success = propagate()
    if success:
        print("\n🎯 Propagación completada exitosamente.")
    else:
        print("\n❌ La propagación falló.")
    exit(0 if success else 1)
