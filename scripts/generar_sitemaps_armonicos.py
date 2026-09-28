# -*- coding: utf-8 -*-
import os
import shutil
import subprocess

TODAY = "2026-09-28"

WORKFLOW_YAML = """name: Deploy Static Portal to Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v5
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""

STORES_CONFIG = {
    "pc-custom-lab": {
        "base_url": "https://iaworldcenter-creator.github.io/vectec/",
        "pages": [
            ("", "daily", "1.0"),
            ("checkout.html", "weekly", "0.8"),
            ("producto.html", "weekly", "0.8"),
            ("catalogo.html", "daily", "0.9"),
            ("ensamble.html", "weekly", "0.8"),
            ("mostrador.html", "daily", "0.9"),
            ("procesadores/", "daily", "0.9"),
            ("tarjetas-madre/", "daily", "0.9"),
            ("tarjetas-de-video/", "daily", "0.9"),
            ("memorias-ram/", "daily", "0.9"),
            ("almacenamiento-ssd/", "daily", "0.9"),
            ("gabinetes/", "daily", "0.9"),
            ("monitores/", "daily", "0.9"),
            ("laptops/", "daily", "0.9"),
            ("punto-de-venta/", "daily", "0.9"),
            ("impresoras/", "daily", "0.9"),
            ("catalogo-01-tarjetas-madre.html", "weekly", "0.8"),
            ("catalogo-02-procesadores.html", "weekly", "0.8"),
            ("catalogo-03-tarjetas-de-video.html", "weekly", "0.8"),
            ("catalogo-04-memorias-ram.html", "weekly", "0.8"),
            ("catalogo-05-discos-duros.html", "weekly", "0.8"),
            ("catalogo-06-fuentes-de-poder.html", "weekly", "0.8"),
            ("catalogo-07-gabinetes.html", "weekly", "0.8"),
            ("catalogo-08-enfriamiento.html", "weekly", "0.8"),
            ("catalogo-09-perifericos.html", "weekly", "0.8"),
            ("catalogo-10-conectividad-redes.html", "weekly", "0.8"),
            ("catalogo-11-monitores-software.html", "weekly", "0.8"),
        ]
    },
    "ofertas-y-liquidaciones": {
        "base_url": "https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/",
        "pages": [
            ("", "daily", "1.0"),
            ("producto.html", "weekly", "0.8"),
            ("checkout.html", "weekly", "0.8"),
        ]
    },
    "bazar-viamx-nfl.gdl": {
        "base_url": "https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/",
        "pages": [
            ("", "daily", "1.0"),
            ("producto.html", "weekly", "0.8"),
            ("checkout.html", "weekly", "0.8"),
        ]
    },
    "mi-puesto-bazar": {
        "base_url": "https://iaworldcenter-creator.github.io/mi-puesto-bazar/",
        "pages": [
            ("", "daily", "1.0"),
            ("ofertas.html", "daily", "0.9"),
            ("revistas.html", "daily", "0.9"),
            ("dulces.html", "weekly", "0.8"),
            ("cigarros.html", "weekly", "0.8"),
            ("electronica.html", "weekly", "0.8"),
            ("producto.html", "weekly", "0.8"),
            ("checkout.html", "weekly", "0.8"),
        ]
    },
    "kiosco-digital": {
        "base_url": "https://iaworldcenter-creator.github.io/kiosco-digital/",
        "pages": [
            ("", "daily", "1.0"),
            ("producto.html", "weekly", "0.8"),
            ("checkout.html", "weekly", "0.8"),
        ]
    },
    "dulces-bazar": {
        "base_url": "https://iaworldcenter-creator.github.io/dulces-bazar/",
        "pages": [
            ("", "daily", "1.0"),
            ("producto.html", "weekly", "0.8"),
            ("checkout.html", "weekly", "0.8"),
        ]
    },
    "cigarros-bazar": {
        "base_url": "https://iaworldcenter-creator.github.io/cigarros-bazar/",
        "pages": [
            ("", "daily", "1.0"),
            ("producto.html", "weekly", "0.8"),
            ("checkout.html", "weekly", "0.8"),
        ]
    },
    ".": {
        "base_url": "https://iaworldcenter-creator.github.io/sitios-web/",
        "pages": [
            ("", "daily", "1.0"),
            ("checkout.html", "weekly", "0.8"),
            ("app.html", "weekly", "0.8"),
            # Enlaces canónicos del ecosistema
            ("https://iaworldcenter-creator.github.io/vectec/", "daily", "0.9", True),
            ("https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/", "daily", "0.85", True),
            ("https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/", "daily", "0.85", True),
            ("https://iaworldcenter-creator.github.io/mi-puesto-bazar/", "daily", "0.85", True),
            ("https://iaworldcenter-creator.github.io/kiosco-digital/", "daily", "0.85", True),
            ("https://iaworldcenter-creator.github.io/dulces-bazar/", "daily", "0.85", True),
            ("https://iaworldcenter-creator.github.io/cigarros-bazar/", "daily", "0.85", True),
        ]
    }
}

def generar_sitemaps():
    print("=" * 80)
    print("GENERANDO Y ARMONIZANDO SITEMAP.XML Y ROBOTS.TXT EN LOS 8 SITIOS")
    print(f"Fecha de actualización: {TODAY}")
    print("=" * 80)

    for store, cfg in STORES_CONFIG.items():
        base = cfg["base_url"].rstrip("/") + "/"
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        ]

        for item in cfg["pages"]:
            path = item[0]
            changefreq = item[1]
            priority = item[2]
            is_full_url = len(item) > 3 and item[3]

            if is_full_url:
                url = path
            else:
                url = base + path

            xml_lines.append("  <url>")
            xml_lines.append(f"    <loc>{url}</loc>")
            xml_lines.append(f"    <lastmod>{TODAY}</lastmod>")
            xml_lines.append(f"    <changefreq>{changefreq}</changefreq>")
            xml_lines.append(f"    <priority>{priority}</priority>")
            xml_lines.append("  </url>")

        xml_lines.append("</urlset>\n")

        sitemap_path = os.path.join(store, "sitemap.xml")
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write("\n".join(xml_lines))

        # robots.txt
        robots_lines = [
            "User-agent: *",
            "Allow: /",
            "",
            f"Sitemap: {base}sitemap.xml\n"
        ]
        robots_path = os.path.join(store, "robots.txt")
        with open(robots_path, "w", encoding="utf-8") as f:
            f.write("\n".join(robots_lines))

        # workflow deploy.yml
        wf_dir = os.path.join(store, ".github", "workflows")
        os.makedirs(wf_dir, exist_ok=True)
        wf_path = os.path.join(wf_dir, "deploy.yml")
        with open(wf_path, "w", encoding="utf-8") as f:
            f.write(WORKFLOW_YAML)

        print(f"[OK] {store}: sitemap.xml ({len(cfg['pages'])} URLs) + robots.txt + deploy.yml actualizados.")

if __name__ == "__main__":
    generar_sitemaps()
