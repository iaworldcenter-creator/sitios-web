#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bump_cache_v110.py
==================
1. Actualiza sw.js en 6 boutiques: CACHE_NAME = 'ecosystem-cache-v1.1.0' y purga de cachés viejas.
2. Reemplaza '?v=1.0.9' por '?v=1.1.0' en index.html y checkout.html.
3. Valida e inyecta la banda promocional marquee amarilla (#f0c14b) tras </header>.
4. Ejecuta Git Add, Commit y Push en cada boutique y en el monorepositorio central.
"""

import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"

BOUTIQUES = [
    "pc-custom-lab",
    "cigarros-bazar",
    "dulces-bazar",
    "kiosco-digital",
    "mi-puesto-bazar",
    "ofertas-y-liquidaciones"
]

MARQUEE_CSS = """
/* BANDA MARQUEE CONTINUA UNIVERSAL */
@keyframes marqueeContinuous {
    0% { transform: translateX(0%); }
    100% { transform: translateX(-50%); }
}
.marquee-track {
    display: inline-flex;
    width: max-content;
    animation: marqueeContinuous 35s linear infinite;
}
.marquee-track:hover {
    animation-play-state: paused;
}
"""

MARQUEE_HTML = """<!-- BANDA PROMOCIONAL MARQUEE UNIVERSAL -->
<div class="w-full bg-[#f0c14b] border-b border-[#ddb347] text-slate-950 py-2 overflow-hidden">
    <div class="marquee-track flex gap-8 items-center text-xs font-black uppercase tracking-wider">
        <span class="flex items-center gap-1.5">🚚 ¡ENVÍO GRATIS en compras a partir de $499!</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">💳 5% DE CASHBACK acumulable con registro</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">📦 PRECIO DE MAYOREO: 15% de descuento directo al llevar 3+</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">🔔 CONDICIÓN: Sin registro no hay cashback</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">🏬 BOUTIQUES ESPECIALIZADAS, UN SOLO CARRITO</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">🔒 Pagos con tarjeta y transferencia</span>
        <!-- Bucle continuo -->
        <span class="flex items-center gap-1.5">🚚 ¡ENVÍO GRATIS en compras a partir de $499!</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">💳 5% DE CASHBACK acumulable con registro</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">📦 PRECIO DE MAYOREO: 15% de descuento directo al llevar 3+</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">🔔 CONDICIÓN: Sin registro no hay cashback</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">🏬 BOUTIQUES ESPECIALIZADAS, UN SOLO CARRITO</span>
        <span class="text-slate-900 font-bold">•</span>
        <span class="flex items-center gap-1.5">🔒 Pagos con tarjeta y transferencia</span>
    </div>
</div>"""

def update_service_worker(store):
    sw_path = os.path.join(BASE_DIR, store, "sw.js")
    if not os.path.exists(sw_path):
        return

    with open(sw_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Actualizar nombre de caché
    content = re.sub(
        r"const\s+CACHE_NAME\s*=\s*['\"][^'\"]+['\"];?",
        "const CACHE_NAME = 'ecosystem-cache-v1.1.0';",
        content
    )

    # Bumping de versiones de recursos cacheados
    content = content.replace("v=1.0.9", "v=1.1.0")

    with open(sw_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] sw.js actualizado a v1.1.0: {store}")

def update_html_files(store):
    for filename in ["index.html", "checkout.html"]:
        filepath = os.path.join(BASE_DIR, store, filename)
        if not os.path.exists(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()

        # 1. Bumping de query strings v=1.0.9 -> v=1.1.0
        html = html.replace("?v=1.0.9", "?v=1.1.0")
        html = html.replace("v1.0.9", "v1.1.0")

        # 2. Verificación de la banda Marquee en index.html
        if filename == "index.html":
            if "marqueeContinuous" not in html:
                if "<style>" in html:
                    html = re.sub(r"(<style[^>]*>)", r"\1\n" + MARQUEE_CSS, html, count=1)
                else:
                    html = html.replace("</head>", f"<style>{MARQUEE_CSS}</style>\n</head>")

            if "BANDA PROMOCIONAL MARQUEE UNIVERSAL" not in html:
                html = re.sub(r"(</header>)", r"\1\n" + MARQUEE_HTML, html, count=1)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[OK] {filename} actualizado: {store}")

def execute_deploy():
    print("\n=== EJECUTANDO DESPLIEGUE GIT ===")
    # 1. Boutiques individuales
    for store in BOUTIQUES:
        store_path = os.path.join(BASE_DIR, store)
        if os.path.exists(os.path.join(store_path, ".git")):
            subprocess.run(["git", "add", "-A"], cwd=store_path, check=True)
            subprocess.run(
                ["git", "commit", "-m", "fix(cache): forzar actualizacion a v1.1.0 y activar marquee"],
                cwd=store_path,
                capture_output=True,
                text=True
            )
            subprocess.run(["git", "push", "origin", "main"], cwd=store_path, check=True)
            print(f" Desplegado: {store}")

    # 2. Monorepositorio raíz
    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
    subprocess.run(
        ["git", "commit", "-m", "fix(cache): forzar actualizacion a v1.1.0 y activar marquee"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )
    subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, check=True)
    print(" Desplegado: Portal Central (Raíz)")

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    print("=== INICIANDO INVALIDACIÓN DE CACHÉ (BUMP v1.1.0) ===")
    for store in BOUTIQUES:
        update_service_worker(store)
        update_html_files(store)
    execute_deploy()
    print("\nProceso y despliegue finalizados con éxito.")