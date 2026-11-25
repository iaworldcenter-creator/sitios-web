# Cloudflare Worker — Pasarela Segura Mercado Pago (VECTEC / 8 Tiendas)

Este Worker actúa como proxy serverless seguro para crear preferencias de pago en Mercado Pago sin exponer `MP_ACCESS_TOKEN` en el código JavaScript público de GitHub Pages.

## Despliegue en 3 comandos

1. Autenticarse en Cloudflare (abre el navegador una vez):
   ```bash
   npx wrangler login
   ```
2. Guardar tu **nuevo** token rotado de Producción de Mercado Pago como secreto cifrado en Cloudflare:
   ```bash
   cd cloudflare-worker
   npx wrangler secret put MP_ACCESS_TOKEN
   ```
3. Desplegar el Worker gratuito (`workers.dev`):
   ```bash
   npx wrangler deploy
   ```

Al terminar, copia la URL entregada por Cloudflare (ej. `https://vectec-mp-checkout.<tu-subdominio>.workers.dev`) y colócala en `DEFAULT_MP_WORKER_ENDPOINT` dentro de `js/shared-cart-whatsapp.js` (sincronizando hacia las 8 tiendas).
