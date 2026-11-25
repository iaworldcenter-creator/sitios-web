/**
 * Cloudflare Worker: vectec-mp-checkout
 * Proxy seguro para generar preferencias de Mercado Pago Checkout Pro
 * manteniendo MP_ACCESS_TOKEN exclusivamente como Cloudflare Secret (env.MP_ACCESS_TOKEN).
 */

const ALLOWED_ORIGINS = [
  "https://iaworldcenter-creator.github.io",
  "http://localhost",
  "http://127.0.0.1"
];

function getCorsHeaders(request) {
  const origin = request.headers.get("Origin") || "";
  const isAllowed = ALLOWED_ORIGINS.some((prefix) => origin.startsWith(prefix));
  return {
    "Access-Control-Allow-Origin": isAllowed ? origin : "https://iaworldcenter-creator.github.io",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
    "Content-Type": "application/json; charset=utf-8"
  };
}

export default {
  async fetch(request, env) {
    const corsHeaders = getCorsHeaders(request);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders });
    }

    if (request.method !== "POST") {
      return new Response(
        JSON.stringify({ success: false, error: "Método no permitido. Usa POST." }),
        { status: 405, headers: corsHeaders }
      );
    }

    const token = env && env.MP_ACCESS_TOKEN ? String(env.MP_ACCESS_TOKEN).trim() : "";
    if (!token) {
      return new Response(
        JSON.stringify({
          success: false,
          error: "MP_ACCESS_TOKEN no configurado en los secretos del Cloudflare Worker."
        }),
        { status: 500, headers: corsHeaders }
      );
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return new Response(
        JSON.stringify({ success: false, error: "JSON inválido en el cuerpo de la petición." }),
        { status: 400, headers: corsHeaders }
      );
    }

    if (!body || !Array.isArray(body.items) || body.items.length === 0) {
      return new Response(
        JSON.stringify({ success: false, error: "Se requiere al menos 1 artículo en 'items'." }),
        { status: 400, headers: corsHeaders }
      );
    }

    // Sanitización estricta del payload hacia Mercado Pago API
    const sanitizedItems = body.items.map((item, idx) => {
      const unitPrice = Number(item.unit_price ?? item.unitPrice ?? item.price ?? item.precio ?? 0);
      const qty = parseInt(item.quantity ?? item.qty ?? 1, 10);
      return {
        id: String(item.id || item.sku || `ITEM-${idx + 1}`).slice(0, 64),
        title: String(item.title || item.name || item.nombre || "Artículo VECTEC").slice(0, 120),
        quantity: Number.isFinite(qty) && qty > 0 ? qty : 1,
        currency_id: "MXN",
        unit_price: Number.isFinite(unitPrice) && unitPrice > 0 ? Number(unitPrice.toFixed(2)) : 10.0
      };
    });

    const shippingCost = Number(body.shipping?.cost || 0);
    const hasShippingLine = sanitizedItems.some((i) => i.id === "SHIPPING-LOGISTICS");
    if (!hasShippingLine && Number.isFinite(shippingCost) && shippingCost > 0) {
      sanitizedItems.push({
        id: "SHIPPING-LOGISTICS",
        title: `Envío ${String(body.shipping?.carrier || "Uber Flash / Paquetería").slice(0, 80)}`,
        quantity: 1,
        currency_id: "MXN",
        unit_price: Number(shippingCost.toFixed(2))
      });
    }

    const defaultReturn = "https://iaworldcenter-creator.github.io/sitios-web/checkout.html";
    const safeOrderId = String(body.external_reference || body.orderId || `VT-${Date.now().toString().slice(-6)}`);

    const backUrls = body.back_urls && body.back_urls.success
      ? {
          success: String(body.back_urls.success),
          failure: String(body.back_urls.failure || body.back_urls.success),
          pending: String(body.back_urls.pending || body.back_urls.success)
        }
      : {
          success: `${defaultReturn}?status=approved&order=${safeOrderId}`,
          failure: `${defaultReturn}?status=failure&order=${safeOrderId}`,
          pending: `${defaultReturn}?status=pending&order=${safeOrderId}`
        };

    const mpPayload = {
      items: sanitizedItems,
      payer: body.payer || undefined,
      payment_methods: body.payment_methods || {
        excluded_payment_methods: [],
        excluded_payment_types: [],
        installments: 12
      },
      back_urls: backUrls,
      auto_return: "approved",
      external_reference: safeOrderId,
      statement_descriptor: "VECTEC"
    };

    try {
      const mpRes = await fetch("https://api.mercadopago.com/checkout/preferences", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(mpPayload)
      });

      const mpData = await mpRes.json();
      if (!mpRes.ok || !mpData.init_point) {
        return new Response(
          JSON.stringify({
            success: false,
            error: "Mercado Pago rechazó la creación de preferencia.",
            status: mpRes.status,
            details: mpData
          }),
          { status: mpRes.status >= 400 ? mpRes.status : 502, headers: corsHeaders }
        );
      }

      return new Response(
        JSON.stringify({
          success: true,
          preferenceId: mpData.id,
          init_point: mpData.init_point,
          sandbox_init_point: mpData.sandbox_init_point
        }),
        { status: 200, headers: corsHeaders }
      );
    } catch (err) {
      return new Response(
        JSON.stringify({
          success: false,
          error: "Error de red al conectar con Mercado Pago.",
          message: err instanceof Error ? err.message : String(err)
        }),
        { status: 502, headers: corsHeaders }
      );
    }
  }
};
