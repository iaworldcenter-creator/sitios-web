# api/create-preference.py
# Micro-servicio Serverless Python para Generación de Preferencias Mercado Pago
import json
import os
import urllib.request
import urllib.error

MP_ACCESS_TOKEN = os.environ.get("MP_ACCESS_TOKEN", "APP_USR-783757506325362-082612-60b30fdf842397608a8cfcc2a9221837-202684121")

def handler(event, context=None):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Content-Type": "application/json"
    }

    http_method = event.get("httpMethod", "POST") if isinstance(event, dict) else "POST"
    if http_method == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": ""}

    try:
        body_raw = event.get("body", "{}") if isinstance(event, dict) else event
        if isinstance(body_raw, str):
            body = json.loads(body_raw)
        else:
            body = body_raw

        items = body.get("items", [])
        customer = body.get("customer", {})
        shipping = body.get("shipping", {})
        order_id = body.get("orderId", f"VT-{int(time.time())}")
        return_url = body.get("returnUrl", "https://iaworldcenter-creator.github.io/sitios-web/checkout.html")

        if not items:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "La lista de artículos es requerida"})
            }

        mp_items = []
        for idx, it in enumerate(items):
            p = float(it.get("price") or it.get("unitPrice") or it.get("precio") or 0)
            q = int(it.get("quantity") or it.get("qty") or 1)
            mp_items.append({
                "id": str(it.get("sku") or it.get("id") or f"ITEM-{idx+1}"),
                "title": str(it.get("name") or it.get("nombre") or it.get("title") or "Artículo VECTEC")[:120],
                "quantity": max(1, q),
                "currency_id": "MXN",
                "unit_price": round(p if p > 0 else 10.0, 2)
            })

        ship_cost = float(shipping.get("cost") or 0)
        if ship_cost > 0:
            mp_items.append({
                "id": "SHIPPING-UBER",
                "title": "Envío Express Uber Flash / Paquetería Asegurada",
                "quantity": 1,
                "currency_id": "MXN",
                "unit_price": round(ship_cost, 2)
            })

        payload = {
            "items": mp_items,
            "payer": {
                "name": customer.get("name", "Cliente"),
                "email": customer.get("email", "cliente@ejemplo.com"),
                "phone": {"number": "".join(filter(str.isdigit, str(customer.get("phone", ""))))},
                "address": {"street_name": customer.get("street") or customer.get("address", ""), "zip_code": customer.get("cp", "")}
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
            "external_reference": str(order_id),
            "statement_descriptor": "VECTEC"
        }

        req = urllib.request.Request(
            "https://api.mercadopago.com/checkout/preferences",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {MP_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "success": True,
                    "preferenceId": data.get("id"),
                    "init_point": data.get("init_point"),
                    "sandbox_init_point": data.get("sandbox_init_point")
                })
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }
