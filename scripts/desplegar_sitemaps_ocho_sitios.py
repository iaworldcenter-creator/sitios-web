# -*- coding: utf-8 -*-
import subprocess

STORES = [
    'pc-custom-lab',
    'ofertas-y-liquidaciones',
    'bazar-viamx-nfl.gdl',
    'mi-puesto-bazar',
    'kiosco-digital',
    'dulces-bazar',
    'cigarros-bazar',
    '.'
]

MSG = "SEO: Armonizacion de sitemap.xml 2026-09-28, robots.txt y CI/CD en los 8 sitios"

for s in STORES:
    print("=" * 60)
    print(f"DESPLEGANDO: {s}")
    print("=" * 60)
    subprocess.run(["git", "add", "-A"], cwd=s)
    r_com = subprocess.run(["git", "commit", "-m", MSG], cwd=s, capture_output=True, text=True)
    out_com = r_com.stdout.strip() or r_com.stderr.strip()
    print(f"Commit: {out_com[:150]}")

    r_push = subprocess.run(["git", "push", "origin", "main"], cwd=s, capture_output=True, text=True)
    out_push = r_push.stdout.strip() or r_push.stderr.strip()
    if r_push.returncode == 0:
        print(f"[OK] Push exitoso a main: {out_push}")
    else:
        print(f"[ERROR] Push falló en {s}: {out_push}")

print("=" * 60)
print("[COMPLETO] Despliegue de los 8 repositorios finalizado.")
print("=" * 60)
