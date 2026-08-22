import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
VIAMX_DIR = os.path.join(BASE_DIR, "bazar-viamx-nfl.gdl")

if not os.path.exists(VIAMX_DIR):
    alt = os.path.join(BASE_DIR, "bazar-viamx-NFL.GDL")
    if os.path.exists(alt):
        VIAMX_DIR = alt

print("=" * 70)
print("ACTUALIZANDO SPEECH: ECOSISTEMA 100% DIGITAL Y GESTIÓN DE GARANTÍAS")
print("=" * 70)

files_to_update = ["index.html", "producto.html"]

for filename in files_to_update:
    filepath = os.path.join(VIAMX_DIR, filename)
    if not os.path.exists(filepath):
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Ajustar alertas de punto de entrega en barra superior
    content = re.sub(
        r"alert\(['\"]Punto de entrega: Pedro Moreno 501 A[^'\"]*['\"]\)",
        "alert('Tienda 100% Digital: Los pedidos se envían directamente a la puerta de tu domicilio. Oficina de garantías y devoluciones: Pedro Moreno 501 A.')",
        content
    )

    # 2. Corregir textos de entregas físicas por envíos directos a domicilio
    content = content.replace("entrega directa en Guadalajara Centro", "envío directo a la puerta de tu domicilio")
    content = content.replace("Entrega física directa en Pedro Moreno 501 A", "Envíos directos a tu domicilio. Recepción de garantías en Pedro Moreno 501 A")
    content = content.replace("Revisión y entrega física directa en Pedro Moreno 501 A.", "Oficina de recepción y gestión de devoluciones con proveedor en Pedro Moreno 501 A.")
    content = content.replace("Revisión y entrega directa en Pedro Moreno 501 A.", "Recepción de garantías y canalización con proveedor en Pedro Moreno 501 A.")
    content = content.replace("Garantía física en Pedro Moreno 501 A", "Módulo de recepción de devoluciones: Pedro Moreno 501 A")
    content = content.replace("En Stock Guadalajara Centro", "Envío Directo a Domicilio")
    content = content.replace("En Stock Guadalajara", "Envío Directo a Domicilio")
    
    # 3. Ajustar Buy Box y panel de entrega en producto.html
    content = content.replace(
        "Aplica en pedidos de $1,500 MXN o retiro directo en Pedro Moreno 501 A.",
        "Envío directo a la puerta de tu casa. En caso de falla, recepción en oficina central para trámite con proveedor."
    )
    content = content.replace(
        "📍 <strong>Entrega directa:</strong> Sucursal Pedro Moreno 501 A, Guadalajara Centro.",
        "🚚 <strong>Envío directo:</strong> Directo a tu domicilio. 🏢 <strong>Oficina de Garantías:</strong> Pedro Moreno 501 A."
    )

    # 4. Ajustar políticas y speech corporativo en la ficha técnica
    content = content.replace(
        "Soporte local y garantía oficial directa en la zona Centro.",
        "Garantía oficial cubierta por el fabricante/proveedor. Vía MX gestiona la recepción y devolución."
    )
    content = content.replace(
        "Este producto oficial del Ecosistema es el favorito por su durabilidad superior, componentes certificados y garantía local directa inmediata de fábrica.",
        "Comercio 100% digital. Producto original con respaldo oficial del fabricante. En caso de defecto de fábrica, se recibe en oficina central para canalización inmediata con el proveedor."
    )

    # 5. Ajustar Footer Universal
    content = content.replace(
        "Permitidas físicamente en tienda dentro de las primeras 48 horas con empaque íntegro.",
        "Recepción de artículos con falla en oficina administrativa (Pedro Moreno 501 A) para trámite directo de garantía y reembolso con el proveedor oficial."
    )
    content = content.replace(
        "<span>Pedro Moreno 501 A, Guadalajara Centro, Jalisco (CP 44100)</span>",
        "<span>Oficina Administrativa & Centro de Garantías: Pedro Moreno 501 A, Guadalajara Centro (CP 44100)</span>"
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  ✓ {filename} adaptado al modelo 100% digital.")

print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
if os.path.exists(os.path.join(VIAMX_DIR, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=VIAMX_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "fix(speech): modelo 100% digital con envios a domicilio y oficina de recepcion de garantias", "--allow-empty"], cwd=VIAMX_DIR, capture_output=True)
    res_viamx = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=VIAMX_DIR, capture_output=True, text=True)
    print(f"🟢 Vía MX NFL -> Push: {'OK' if res_viamx.returncode == 0 else res_viamx.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "fix(viamx): politicas de envio directo y modulo administrativo de garantias", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
