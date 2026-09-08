#!/usr/bin/env python3
"""
scripts/servidor_preferencias.py
Servidor Local de Desarrollo con Soporte CORS para Preferencias de Mercado Pago
Ejecutar con: python scripts/servidor_preferencias.py [puerto]
"""

import http.server
import json
import os
import sys
import urllib.request
import urllib.error

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
MP_ACCESS_TOKEN = os.environ.get("MP_ACCESS_TOKEN", "APP_USR-783757506325362-082612-60b30fdf842397608a8cfcc2a9221837-202684121")

class MPPreferenceHandler(http.server.BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        if self.path in ["/api/create-preference", "/create-preference", "/api/crear-preferencia"]:
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            
            try:
                data = json.loads(body_bytes.decode("utf-8"))
                items = data.get("items", [])
                customer = data.get("customer", {})
                shipping = data.get("shipping", {})
                order_id = data.get("orderId", "VT-TEST")
                return_url = data.get("returnUrl", "https://iaworldcenter-creator.github.io/sitios-web/checkout.html")

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
                        "title": "Envío Express Uber Flash",
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
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    result = {
                        "success": True,
                        "preferenceId": resp_data.get("id"),
                        "init_point": resp_data.get("init_point"),
                        "sandbox_init_point": resp_data.get("sandbox_init_point")
                    }
                    self.send_response(200)
                    self._send_cors_headers()
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = http.server.HTTPServer(("", PORT), MPPreferenceHandler)
    print(f"Servidor de Preferencias Mercado Pago activo en http://localhost:{PORT}")
    print("Endpoint: POST http://localhost:{PORT}/api/create-preference")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
