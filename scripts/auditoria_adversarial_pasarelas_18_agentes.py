#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auditoria_adversarial_pasarelas_18_agentes.py
=============================================
Gauntlet Adversarial de Pasarelas de Pago Mercado Pago en el Ecosistema de 8 Tiendas.
Diseñado para ejecución local o paralela en GitHub Actions.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path

# Resolver raíz
BASE_DIR = Path("D:/Proyectos/sitios web") if Path("D:/Proyectos/sitios web").exists() else Path(".")

# Cargar .env si existe
env_file = BASE_DIR / ".env"
token = os.environ.get("MP_ACCESS_TOKEN", "")
if not token and env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("MP_ACCESS_TOKEN="):
            token = line.split("=", 1)[1].strip().strip('"').strip("'")
            break

# Fallback al token de producción oficial verificado
if not token:
    token = "APP_USR-783757506325362-082612-60b30fdf842397608a8cfcc2a9221837-202684121"

TIENDAS_CONFIG = {
    "pc-custom-lab": {
        "title": "VECTEC PC Custom Lab",
        "path": "/vectec/checkout.html",
        "sku": "A-MB-B650M",
        "item": "Tarjeta Madre ASUS Prime B650M-A WiFi",
        "price": 2899.00
    },
    "bazar-viamx-nfl.gdl": {
        "title": "Bazar Vía MX GDL",
        "path": "/bazar-viamx-NFL.GDL/checkout.html",
        "sku": "BZ-JER-KC",
        "item": "Jersey NFL Kansas City Chiefs Edición Especial",
        "price": 1250.00
    },
    "cigarros-bazar": {
        "title": "Cigarros Bazar",
        "path": "/cigarros-bazar/checkout.html",
        "sku": "CB-MAR-RED",
        "item": "Cajetilla Clásica Premium 20s",
        "price": 75.00
    },
    "dulces-bazar": {
        "title": "Dulces Bazar",
        "path": "/dulces-bazar/checkout.html",
        "sku": "DB-MAZ-12P",
        "item": "Caja Dulces Típicos y Mazapán 12 pzas",
        "price": 95.00
    },
    "kiosco-digital": {
        "title": "Kiosco Digital",
        "path": "/kiosco-digital/checkout.html",
        "sku": "KD-USB-64G",
        "item": "Memoria USB Alta Velocidad 64GB",
        "price": 145.00
    },
    "mi-puesto-bazar": {
        "title": "Mi Puesto Bazar",
        "path": "/mi-puesto-bazar/checkout.html",
        "sku": "MP-REV-NAT",
        "item": "Revista Ilustrada Colección Especial",
        "price": 85.00
    },
    "ofertas-y-liquidaciones": {
        "title": "Ofertas y Liquidaciones",
        "path": "/ofertas-y-liquidaciones-/checkout.html",
        "sku": "OF-AUR-BT",
        "item": "Auriculares In-Ear Bluetooth Cancelación Ruido",
        "price": 299.00
    },
    "sitios-web": {
        "title": "Ecosistema Matriz",
        "path": "/sitios-web/checkout.html",
        "sku": "MX-COMBO-01",
        "item": "Kit de Mantenimiento y Conectividad Pro",
        "price": 380.00
    }
}

def ejecutar_auditoria_tienda(tienda_id, info):
    print(f"\n{'='*75}")
    print(f"[*] AUDITANDO TIENDA: {info['title']} ({tienda_id})")
    print(f"{'='*75}")
    
    reporte = {"tienda": tienda_id, "pruebas": [], "passed": 0, "failed": 0}

    # 1. VERIFICACIÓN CORS PREFLIGHT
    try:
        req_cors = urllib.request.Request(
            "https://api.mercadopago.com/checkout/preferences",
            headers={
                "Origin": "https://iaworldcenter-creator.github.io",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "authorization, content-type",
                "User-Agent": "Mozilla/5.0"
            },
            method="OPTIONS"
        )
        with urllib.request.urlopen(req_cors, timeout=10) as resp:
            cors_origin = resp.headers.get("Access-Control-Allow-Origin", "")
            if resp.status == 200 and cors_origin:
                print(f"  [PASS] Test 1: Preflight CORS OPTIONS (Status 200, Allow-Origin: {cors_origin})")
                reporte["pruebas"].append({"nombre": "CORS Preflight", "status": "PASS"})
                reporte["passed"] += 1
            else:
                print(f"  [FAIL] Test 1: CORS Preflight rechazada (Status {resp.status})")
                reporte["pruebas"].append({"nombre": "CORS Preflight", "status": "FAIL"})
                reporte["failed"] += 1
    except Exception as e:
        print(f"  [FAIL] Test 1: Error CORS: {e}")
        reporte["pruebas"].append({"nombre": "CORS Preflight", "status": "FAIL", "error": str(e)})
        reporte["failed"] += 1

    # 2. CREACIÓN DE PREFERENCIA CHECKOUT PRO (PRODUCCIÓN)
    order_id = f"VT-ADV-{tienda_id[:4].upper()}-01"
    return_url = f"https://iaworldcenter-creator.github.io{info['path']}"
    payload_normal = {
        "items": [
            {
                "id": info["sku"],
                "title": info["item"],
                "quantity": 1,
                "currency_id": "MXN",
                "unit_price": float(info["price"])
            },
            {
                "id": "SHIPPING-UBER",
                "title": "Envío Uber Flash Express (A Domicilio)",
                "quantity": 1,
                "currency_id": "MXN",
                "unit_price": 99.00
            }
        ],
        "payer": {
            "name": "Cliente Auditoría",
            "email": "cliente.auditoria@viamx.com",
            "phone": {"number": "3337271440"},
            "address": {
                "street_name": "Pedro Moreno 501 A, Centro",
                "zip_code": "44100"
            }
        },
        "payment_methods": {
            "excluded_payment_methods": [],
            "excluded_payment_types": [],
            "installments": 12
        },
        "back_urls": {
            "success": f"{return_url}?status=approved&order={order_id}",
            "failure": f"{return_url}?status=failure&order={order_id}",
            "pending": f"{return_url}?status=pending&order={order_id}"
        },
        "auto_return": "approved",
        "external_reference": order_id,
        "statement_descriptor": "VECTEC"
    }

    try:
        req_pref = urllib.request.Request(
            "https://api.mercadopago.com/checkout/preferences",
            data=json.dumps(payload_normal).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        with urllib.request.urlopen(req_pref, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pref_id = data.get("id")
            init_point = data.get("init_point")
            if resp.status == 201 and pref_id and init_point:
                print(f"  [PASS] Test 2: Checkout Pro Producción (Status 201 Created | ID: {pref_id[:20]}...)")
                print(f"         URL Pago: {init_point}")
                reporte["pruebas"].append({"nombre": "Checkout Pro Preference", "status": "PASS", "init_point": init_point})
                reporte["passed"] += 1
            else:
                print(f"  [FAIL] Test 2: Respuesta incompleta de Mercado Pago")
                reporte["pruebas"].append({"nombre": "Checkout Pro Preference", "status": "FAIL"})
                reporte["failed"] += 1
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        print(f"  [FAIL] Test 2: HTTPError {e.code}: {err}")
        reporte["pruebas"].append({"nombre": "Checkout Pro Preference", "status": "FAIL", "error": err})
        reporte["failed"] += 1

    # 3. ATAQUE ADVERSARIAL: PAYLOAD MUTANTE / EXTREMO
    payload_adversarial = {
        "items": [
            {
                "id": "SKU-ADVERSARIAL-99",
                "title": "Producto Caracteres Especiales: ¿¡Gabinete RGB & Enfriamiento Líquido!? #100%",
                "quantity": 2,
                "currency_id": "MXN",
                "unit_price": 1499.99
            }
        ],
        "payer": {
            "name": "Ñoño Pérez Ávila",
            "email": "nono.avila@dominio-raro.com.mx"
        },
        "back_urls": {
            "success": f"{return_url}?status=approved&order=VT-ADV-EXTREME",
            "failure": f"{return_url}?status=failure&order=VT-ADV-EXTREME",
            "pending": f"{return_url}?status=pending&order=VT-ADV-EXTREME"
        },
        "auto_return": "approved",
        "external_reference": "VT-ADV-EXTREME"
    }

    try:
        req_adv = urllib.request.Request(
            "https://api.mercadopago.com/checkout/preferences",
            data=json.dumps(payload_adversarial).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        with urllib.request.urlopen(req_adv, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if resp.status == 201 and data.get("id"):
                print(f"  [PASS] Test 3: Resistencia a Payload Adversarial (Aceptó UTF-8, símbolos y centavos)")
                reporte["pruebas"].append({"nombre": "Payload Adversarial", "status": "PASS"})
                reporte["passed"] += 1
            else:
                print(f"  [FAIL] Test 3: No procesó payload adversarial")
                reporte["pruebas"].append({"nombre": "Payload Adversarial", "status": "FAIL"})
                reporte["failed"] += 1
    except Exception as e:
        print(f"  [FAIL] Test 3: Fallo con payload adversarial: {e}")
        reporte["pruebas"].append({"nombre": "Payload Adversarial", "status": "FAIL", "error": str(e)})
        reporte["failed"] += 1

    # 4. AUDITORÍA ESTÁTICA DEL ARCHIVO CHECKOUT.HTML Y JS ASOCIADO
    local_dir = BASE_DIR / tienda_id if tienda_id != "sitios-web" else BASE_DIR
    checkout_file = local_dir / "checkout.html"
    cart_js_file = local_dir / "js" / "shared-cart-whatsapp.js"

    if checkout_file.exists():
        txt_chk = checkout_file.read_text(encoding="utf-8", errors="ignore")
        has_click = "executeFinalCheckoutFlow" in txt_chk
        has_shared = "shared-cart-whatsapp.js" in txt_chk
        if has_click and has_shared:
            print(f"  [PASS] Test 4: Enlaces DOM en checkout.html (executeFinalCheckoutFlow + shared-cart)")
            reporte["pruebas"].append({"nombre": "DOM Checkout Wiring", "status": "PASS"})
            reporte["passed"] += 1
        else:
            print(f"  [FAIL] Test 4: Discrepancia en checkout.html (click: {has_click}, js: {has_shared})")
            reporte["pruebas"].append({"nombre": "DOM Checkout Wiring", "status": "FAIL"})
            reporte["failed"] += 1
    else:
        print(f"  [FAIL] Test 4: checkout.html no existe en {local_dir}")
        reporte["pruebas"].append({"nombre": "DOM Checkout Wiring", "status": "FAIL"})
        reporte["failed"] += 1

    # 5. AUDITORÍA DE RETORNO Y MODALES DE MERCADO PAGO EN JS
    if cart_js_file.exists():
        txt_js = cart_js_file.read_text(encoding="utf-8", errors="ignore")
        has_return_handler = "checkMercadoPagoReturnStatus" in txt_js
        has_approved_modal = "mp-success-modal" in txt_js
        has_localhost_shield = "localhost" in txt_js and "currentOrigin" in txt_js
        if has_return_handler and has_approved_modal and has_localhost_shield:
            print(f"  [PASS] Test 5: Blindaje en shared-cart-whatsapp.js (Return Handler + Modales + Anti-Localhost)")
            reporte["pruebas"].append({"nombre": "JS Return & Shield", "status": "PASS"})
            reporte["passed"] += 1
        else:
            print(f"  [FAIL] Test 5: Falta módulo de retorno en {cart_js_file}")
            reporte["pruebas"].append({"nombre": "JS Return & Shield", "status": "FAIL"})
            reporte["failed"] += 1
    else:
        print(f"  [FAIL] Test 5: shared-cart-whatsapp.js no existe en {cart_js_file}")
        reporte["pruebas"].append({"nombre": "JS Return & Shield", "status": "FAIL"})
        reporte["failed"] += 1

    return reporte

def main():
    parser = argparse.ArgumentParser(description="Auditoría Adversarial Pasarelas Mercado Pago")
    parser.add_argument("--tienda", type=str, default="", help="ID de la tienda específica")
    args = parser.parse_args()

    print("================================================================================")
    print("  SUPERVISOR ADVERSARIAL: GAUNTLET DE AUDITORÍA MERCADO PAGO (18 AGENTES)      ")
    print("================================================================================")

    if args.tienda:
        if args.tienda in TIENDAS_CONFIG:
            res = ejecutar_auditoria_tienda(args.tienda, TIENDAS_CONFIG[args.tienda])
            print(f"\nResumen para {args.tienda}: {res['passed']} PASS / {res['failed']} FAIL")
            if res['failed'] > 0:
                sys.exit(1)
        else:
            print(f"Error: Tienda '{args.tienda}' no reconocida.")
            sys.exit(1)
    else:
        todos_reportes = []
        for tid, tinfo in TIENDAS_CONFIG.items():
            rep = ejecutar_auditoria_tienda(tid, tinfo)
            todos_reportes.append(rep)
        
        total_p = sum(r["passed"] for r in todos_reportes)
        total_f = sum(r["failed"] for r in todos_reportes)
        print("\n================================================================================")
        print(f"  RESULTADO FINAL CONSOLIDADO: {total_p} PRUEBAS SUPERADAS / {total_f} FALLIDAS")
        print("================================================================================")
        if total_f > 0:
            sys.exit(1)

if __name__ == "__main__":
    main()
