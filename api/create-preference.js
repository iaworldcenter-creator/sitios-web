/**
 * api/create-preference.js
 * Micro-servicio Serverless para Generación de Preferencias Mercado Pago Checkout Pro
 * Ecosistema Comercial VECTEC / 8 Tiendas
 */

const MP_ACCESS_TOKEN = process.env.MP_ACCESS_TOKEN || "APP_USR-783757506325362-082612-60b30fdf842397608a8cfcc2a9221837-202684121";

module.exports = async (req, res) => {
    // Habilitar CORS
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader(
        'Access-Control-Allow-Headers',
        'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, Authorization'
    );

    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Método no permitido. Utiliza POST.' });
    }

    try {
        const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
        const { items, customer, shipping, orderId, paymentMethod, returnUrl } = body;

        if (!items || !Array.isArray(items) || items.length === 0) {
            return res.status(400).json({ error: 'La lista de artículos es requerida y debe contener al menos 1 producto.' });
        }

        // Sanitización de artículos
        const mpItems = items.map((item, idx) => {
            const rawPrice = parseFloat(item.price || item.unitPrice || item.precio || 0);
            const qty = parseInt(item.quantity || item.qty || 1);
            return {
                id: String(item.sku || item.id || `ITEM-${idx + 1}`),
                title: String(item.name || item.nombre || item.title || 'Artículo VECTEC').slice(0, 120),
                description: String(item.description || item.name || '').slice(0, 200),
                quantity: qty > 0 ? qty : 1,
                currency_id: 'MXN',
                unit_price: isNaN(rawPrice) || rawPrice <= 0 ? 10.00 : parseFloat(rawPrice.toFixed(2)),
                picture_url: item.img || item.image || item.imagen || undefined
            };
        });

        // Agregar costo de envío si aplica
        const shippingCost = parseFloat(shipping?.cost || 0);
        if (shippingCost > 0) {
            mpItems.push({
                id: 'SHIPPING-UBER-FLASH',
                title: 'Envío Express Uber Flash / Paquetería Asegurada',
                quantity: 1,
                currency_id: 'MXN',
                unit_price: parseFloat(shippingCost.toFixed(2))
            });
        }

        // Configuración de pagador (Payer)
        const payer = {
            name: customer?.name || 'Cliente VECTEC',
            email: customer?.email || 'cliente@ejemplo.com',
            phone: {
                number: String(customer?.phone || '').replace(/[^0-9]/g, '') || undefined
            },
            address: {
                street_name: customer?.street || customer?.address || '',
                zip_code: customer?.cp || ''
            }
        };

        // Red multitienda en efectivo y tarjetas
        // No se excluye ningún método para permitir tanto tarjetas como tiendas de conveniencia (ticket: OXXO, 7-Eleven, Farmacias GDL, Soriana, etc.)
        const paymentMethods = {
            excluded_payment_methods: [],
            excluded_payment_types: [],
            installments: 12
        };

        const defaultBack = returnUrl || 'https://iaworldcenter-creator.github.io/sitios-web/checkout.html';
        const backUrls = {
            success: `${defaultBack}?status=approved&order=${orderId || 'VT-000000'}`,
            failure: `${defaultBack}?status=failure&order=${orderId || 'VT-000000'}`,
            pending: `${defaultBack}?status=pending&order=${orderId || 'VT-000000'}`
        };

        const preferencePayload = {
            items: mpItems,
            payer: payer,
            payment_methods: paymentMethods,
            back_urls: backUrls,
            auto_return: 'approved',
            external_reference: String(orderId || `VT-${Date.now()}`),
            statement_descriptor: 'VECTEC'
        };

        const mpResponse = await fetch('https://api.mercadopago.com/checkout/preferences', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${MP_ACCESS_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(preferencePayload)
        });

        const mpData = await mpResponse.json();

        if (!mpResponse.ok) {
            console.error('Error Mercado Pago API:', mpData);
            return res.status(mpResponse.status).json({
                error: 'Error al generar preferencia en Mercado Pago',
                details: mpData
            });
        }

        return res.status(200).json({
            success: true,
            preferenceId: mpData.id,
            init_point: mpData.init_point,
            sandbox_init_point: mpData.sandbox_init_point
        });

    } catch (err) {
        console.error('Error interno micro-servicio:', err);
        return res.status(500).json({
            error: 'Error interno en el servidor',
            message: err.message
        });
    }
};
