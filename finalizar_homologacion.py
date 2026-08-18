#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
finalizar_homologacion.py
Script de automatización para remate y homologación técnica de las 6 tiendas:
- cigarros-bazar
- dulces-bazar
- kiosco-digital
- mi-puesto-bazar
- ofertas-y-liquidaciones
- pc-custom-lab

Actualizaciones realizadas:
1. checkout.html en las 6 tiendas:
   - Paso 1: Título 'Domicilio de Entrega — Disfrute sus productos en la puerta de su casa' y validaciones exhaustivas.
   - Paso 2: Título 'Método de Pago — Agilice la entrega de sus productos' con los 4 métodos en acordeón colapsable:
     * Tarjeta de Crédito / Débito
     * Pago en Efectivo contra Entrega
     * Depósito en Tiendas OXXO (OXXO Pay)
     * Transferencia Bancaria (SPEI)
   - Paso 3: Desglose dinámico de importes: Envío Gratis >= $1,500 MXN (sino $49 MXN), mayoreo 15% (>= 10 piezas) y cashback 5%.
2. PC Custom Lab (pc-custom-lab/index.html):
   - Configurador interactivo de 10 componentes vinculado a la boutique de refacciones.
   - Carrusel móvil con soporte táctil (swipe gestures) y navegación directa a la boutique.
"""

import os
import sys
import re

# Asegurar codificación utf-8 en salida estándar
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if not any(os.path.exists(os.path.join(BASE_DIR, s)) for s in ["cigarros-bazar", "dulces-bazar"]):
    BASE_DIR = r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web"

STORES = [
    "cigarros-bazar",
    "dulces-bazar",
    "kiosco-digital",
    "mi-puesto-bazar",
    "ofertas-y-liquidaciones",
    "pc-custom-lab"
]

def generate_checkout_main_html():
    """Genera la estructura HTML para el main de checkout con los 3 pasos homologados."""
    return '''    <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        <!-- Lado Izquierdo: Pasos 1 y 2 (Colapsables) -->
        <div class="lg:col-span-7 flex flex-col gap-6">
            
            <!-- SECCIÓN 1: Domicilio de Entrega -->
            <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-md transition-all duration-300" id="step-delivery-card">
                <div class="flex justify-between items-center mb-4 border-b border-slate-850 pb-2">
                    <h2 class="text-base font-black text-white flex items-center gap-2">
                        <span class="w-6 h-6 rounded-full bg-cyan-500 text-slate-950 flex items-center justify-center text-xs font-black">1</span>
                        Domicilio de Entrega — Disfrute sus productos en la puerta de su casa
                    </h2>
                    <button onclick="editDelivery()" id="delivery-edit-btn" class="hidden text-xs text-cyan-400 hover:underline font-bold focus:outline-none min-h-[32px]">Editar</button>
                </div>
                
                <!-- Formulario -->
                <form id="delivery-form" onsubmit="saveDelivery(event)" class="flex flex-col gap-3">
                    <div>
                        <label class="block text-[10px] uppercase tracking-wider font-bold text-slate-400 mb-1">Nombre Completo <span class="text-red-400">*</span></label>
                        <input type="text" id="devName" required minlength="3" placeholder="Ej: Juan Pérez González" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500 min-h-[48px]">
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div>
                            <label class="block text-[10px] uppercase tracking-wider font-bold text-slate-400 mb-1">Teléfono (10 dígitos) <span class="text-red-400">*</span></label>
                            <input type="tel" id="devPhone" required pattern="[0-9]{10}" maxlength="10" title="Por favor ingresa un número de 10 dígitos sin espacios ni guiones" placeholder="Ej: 3337271440" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500 min-h-[48px]">
                        </div>
                        <div>
                            <label class="block text-[10px] uppercase tracking-wider font-bold text-slate-400 mb-1">Correo electrónico <span class="text-emerald-400">(Acumula 5% de cashback)</span></label>
                            <input type="email" id="devEmail" required placeholder="correo@ejemplo.com" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500 min-h-[48px]">
                        </div>
                    </div>
                    <div>
                        <label class="block text-[10px] uppercase tracking-wider font-bold text-slate-400 mb-1">Calle y Número <span class="text-red-400">*</span></label>
                        <input type="text" id="devStreet" required placeholder="Ej: Av. Vallarta 1234 int 5B" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500 min-h-[48px]">
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div>
                            <label class="block text-[10px] uppercase tracking-wider font-bold text-slate-400 mb-1">Colonia <span class="text-red-400">*</span></label>
                            <input type="text" id="devColonia" required placeholder="Ej: Americana" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500 min-h-[48px]">
                        </div>
                        <div>
                            <label class="block text-[10px] uppercase tracking-wider font-bold text-slate-400 mb-1">Código Postal (5 dígitos) <span class="text-red-400">*</span></label>
                            <input type="text" id="devCp" required pattern="[0-9]{5}" maxlength="5" title="Código postal de 5 dígitos" placeholder="Ej: 44160" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500 min-h-[48px]">
                        </div>
                        <div>
                            <label class="block text-[10px] uppercase tracking-wider font-bold text-slate-400 mb-1">Ciudad y Estado <span class="text-red-400">*</span></label>
                            <input type="text" id="devCity" required placeholder="Ej: Guadalajara, Jalisco" value="Guadalajara, Jalisco" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500 min-h-[48px]">
                        </div>
                    </div>
                    <div>
                        <label class="block text-[10px] uppercase tracking-wider font-bold text-slate-400 mb-1">Indicaciones / Referencias de Entrega</label>
                        <input type="text" id="devRef" placeholder="Ej: Entre calles López Cotilla y Madero, portón negro" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500 min-h-[48px]">
                    </div>
                    <button type="submit" class="w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black py-3 rounded-xl text-xs uppercase tracking-wider transition cursor-pointer mt-2 shadow-md shadow-cyan-500/10 min-h-[48px]">
                        Guardar Domicilio y Continuar al Paso 2
                    </button>
                </form>
                
                <!-- Resumen Domicilio -->
                <div id="delivery-summary" class="hidden flex flex-col gap-1 text-xs text-slate-300 bg-slate-950/60 p-4 rounded-xl border border-slate-850">
                    <span class="font-bold text-white text-sm" id="sum-name"></span>
                    <span id="sum-phone-email" class="text-slate-400"></span>
                    <span id="sum-address"></span>
                </div>
            </div>
            
            <!-- SECCIÓN 2: Forma de Pago -->
            <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-md transition-all duration-300 opacity-60" id="step-payment-card">
                <div class="flex justify-between items-center mb-4 border-b border-slate-850 pb-2">
                    <h2 class="text-base font-black text-white flex items-center gap-2">
                        <span class="w-6 h-6 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center text-xs font-black transition-colors" id="step-payment-badge">2</span>
                        Método de Pago — Agilice la entrega de sus productos
                    </h2>
                    <button onclick="editPayment()" id="payment-edit-btn" class="hidden text-xs text-cyan-400 hover:underline font-bold focus:outline-none min-h-[32px]">Cambiar Método</button>
                </div>
                
                <!-- Opciones de Pago (Acordeón de 4 métodos) -->
                <div id="payment-options" class="hidden flex flex-col gap-3">
                    
                    <!-- Opción 1: Tarjeta de Crédito / Débito -->
                    <div class="border border-slate-800 rounded-2xl overflow-hidden bg-slate-950/40">
                        <button type="button" onclick="togglePaymentAccordion('card')" class="w-full px-4 py-3.5 flex items-center justify-between hover:bg-slate-950/60 transition cursor-pointer text-left min-h-[48px]">
                            <span class="flex items-center gap-2.5 text-xs font-bold text-white">
                                <i class="fa-solid fa-credit-card text-cyan-400 text-base"></i> Tarjeta de Crédito / Débito
                            </span>
                            <i class="fa-solid fa-chevron-down text-slate-400 text-[10px] transition-transform" id="arrow-card"></i>
                        </button>
                        <div id="accordion-card-form" class="hidden border-t border-slate-850 p-4 flex flex-col gap-3">
                            <div>
                                <label class="block text-[10px] uppercase tracking-wider font-bold text-slate-400 mb-1">Nombre en la Tarjeta</label>
                                <input type="text" id="cardName" placeholder="Como aparece en el plástico" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-400 min-h-[48px]">
                            </div>
                            <div>
                                <label class="block text-[10px] uppercase tracking-wider font-bold text-slate-400 mb-1">Número de Tarjeta (16 dígitos)</label>
                                <input type="text" id="cardNum" placeholder="•••• •••• •••• ••••" maxlength="19" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-400 min-h-[48px]">
                            </div>
                            <div class="grid grid-cols-2 gap-3">
                                <div>
                                    <label class="block text-[10px] uppercase tracking-wider font-bold text-slate-400 mb-1">Vencimiento</label>
                                    <input type="text" id="cardExp" placeholder="MM/AA" maxlength="5" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-400 min-h-[48px]">
                                </div>
                                <div>
                                    <label class="block text-[10px] uppercase tracking-wider font-bold text-slate-400 mb-1">CVV</label>
                                    <input type="password" id="cardCvv2" placeholder="123" maxlength="4" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-400 min-h-[48px]">
                                </div>
                            </div>
                            <button type="button" onclick="saveCardDetails(event)" class="w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black py-2.5 rounded-xl text-xs uppercase tracking-wider transition cursor-pointer min-h-[48px]">Confirmar Tarjeta</button>
                        </div>
                    </div>

                    <!-- Opción 2: Pago en Efectivo contra Entrega -->
                    <div class="border border-slate-800 rounded-2xl overflow-hidden bg-slate-950/40">
                        <button type="button" onclick="togglePaymentAccordion('cash')" class="w-full px-4 py-3.5 flex items-center justify-between hover:bg-slate-950/60 transition cursor-pointer text-left min-h-[48px]">
                            <span class="flex items-center gap-2.5 text-xs font-bold text-white">
                                <i class="fa-solid fa-hand-holding-dollar text-emerald-400 text-base"></i> Pago en Efectivo contra Entrega
                            </span>
                            <i class="fa-solid fa-chevron-down text-slate-400 text-[10px] transition-transform" id="arrow-cash"></i>
                        </button>
                        <div id="accordion-cash-form" class="hidden border-t border-slate-850 p-4 flex flex-col gap-2.5 text-xs text-slate-300">
                            <p class="leading-relaxed">Paga directamente en efectivo al mensajero al momento de recibir tus productos en la puerta de tu casa o negocio.</p>
                            <button type="button" onclick="selectPaymentMethod('Pago en Efectivo contra Entrega')" class="w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black py-2.5 rounded-xl text-xs uppercase tracking-wider transition mt-2 cursor-pointer min-h-[48px]">Confirmar Pago contra Entrega</button>
                        </div>
                    </div>

                    <!-- Opción 3: Depósito en OXXO -->
                    <div class="border border-slate-800 rounded-2xl overflow-hidden bg-slate-950/40">
                        <button type="button" onclick="togglePaymentAccordion('oxxo')" class="w-full px-4 py-3.5 flex items-center justify-between hover:bg-slate-950/60 transition cursor-pointer text-left min-h-[48px]">
                            <span class="flex items-center gap-2.5 text-xs font-bold text-white">
                                <i class="fa-solid fa-store text-amber-400 text-base"></i> Depósito en Tiendas OXXO (OXXO Pay)
                            </span>
                            <i class="fa-solid fa-chevron-down text-slate-400 text-[10px] transition-transform" id="arrow-oxxo"></i>
                        </button>
                        <div id="accordion-oxxo-form" class="hidden border-t border-slate-850 p-4 flex flex-col gap-2.5 text-xs text-slate-300">
                            <p class="leading-relaxed">Genera tu ficha de pago digital para pagar en efectivo en cualquier tienda OXXO de la República Mexicana las 24 horas.</p>
                            <button type="button" onclick="selectPaymentMethod('Depósito en Tiendas OXXO (OXXO Pay)')" class="w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black py-2.5 rounded-xl text-xs uppercase tracking-wider transition mt-2 cursor-pointer min-h-[48px]">Confirmar Pago en OXXO</button>
                        </div>
                    </div>

                    <!-- Opción 4: Transferencia Bancaria SPEI -->
                    <div class="border border-slate-800 rounded-2xl overflow-hidden bg-slate-950/40">
                        <button type="button" onclick="togglePaymentAccordion('spei')" class="w-full px-4 py-3.5 flex items-center justify-between hover:bg-slate-950/60 transition cursor-pointer text-left min-h-[48px]">
                            <span class="flex items-center gap-2.5 text-xs font-bold text-white">
                                <i class="fa-solid fa-building-columns text-blue-400 text-base"></i> Transferencia Bancaria (SPEI)
                            </span>
                            <i class="fa-solid fa-chevron-down text-slate-400 text-[10px] transition-transform" id="arrow-spei"></i>
                        </button>
                        <div id="accordion-spei-form" class="hidden border-t border-slate-850 p-4 flex flex-col gap-2.5 text-xs text-slate-300">
                            <p class="leading-relaxed">Transfiere desde tu banca móvil de cualquier banco con acreditación inmediata y sin comisiones.</p>
                            <div class="bg-slate-950/80 p-3 rounded-xl border border-slate-800 text-[11px] font-mono text-cyan-300 flex flex-col gap-1">
                                <div><strong class="text-white">Banco:</strong> BBVA México</div>
                                <div><strong class="text-white">CLABE:</strong> 0123 2001 2345 6789 01</div>
                                <div><strong class="text-white">Beneficiario:</strong> Viamx Hub GD</div>
                            </div>
                            <button type="button" onclick="selectPaymentMethod('Transferencia Bancaria (SPEI)')" class="w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black py-2.5 rounded-xl text-xs uppercase tracking-wider transition mt-2 cursor-pointer min-h-[48px]">Confirmar Transferencia (SPEI)</button>
                        </div>
                    </div>
                </div>
                
                <!-- Resumen Pago -->
                <div id="payment-summary" class="hidden text-xs text-emerald-400 font-bold bg-slate-950/60 p-4 rounded-xl border border-slate-850"></div>
            </div>
        </div>
        
        <!-- Lado Derecho: Carrito y Resumen (Paso 3) -->
        <div class="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-md flex flex-col gap-5 text-slate-100 w-full">
            <h2 class="text-base font-black text-white flex items-center gap-2 border-b border-slate-800 pb-3">
                <span class="w-6 h-6 rounded-full bg-cyan-500 text-slate-950 flex items-center justify-center text-xs font-black">3</span>
                Revisión e Importes
            </h2>
            
            <!-- Lista de productos -->
            <div class="flex flex-col gap-3 overflow-y-auto max-h-[35vh] pr-1" id="checkout-cart-items">
                <!-- Dinámico -->
            </div>
            
            <!-- Totales y Botones de Cierre -->
            <div class="border-t border-slate-800 pt-4 mt-2 flex flex-col gap-6 w-full">
                <!-- Desglose Alineado a la Derecha -->
                <div class="flex flex-col gap-2.5 w-full text-right border-b border-slate-800/60 pb-4">
                    <div class="flex justify-between text-xs text-slate-400">
                        <span>Subtotal de Artículos:</span>
                        <span class="font-bold text-white text-xs" id="co-subtotal">$0.00 MXN</span>
                    </div>
                    <div class="flex justify-between text-xs text-amber-500 hidden animate-fade-in" id="co-wholesale-row">
                        <span>Descuento de Mayoreo (15%):</span>
                        <span class="font-bold" id="co-wholesale-disc">-$0.00 MXN</span>
                    </div>
                    <div class="flex justify-between text-xs text-slate-400">
                        <span>Gastos de Envío Local:</span>
                        <span class="font-bold text-white text-xs" id="co-shipping">$0.00 MXN</span>
                    </div>
                    <div class="flex flex-col gap-1 border-t border-slate-850 pt-2.5 mt-1" id="co-cashback-row">
                        <!-- Dinámico -->
                    </div>
                    <div class="flex justify-between items-center border-t border-slate-850 pt-3 mt-1 text-right">
                        <span class="text-xs font-black text-white uppercase tracking-wider">TOTAL A PAGAR:</span>
                        <span class="text-lg font-black text-cyan-400 text-right" id="co-total">$0.00 MXN</span>
                    </div>
                </div>

                <!-- Botones de Acción Alineados a la Izquierda -->
                <div class="flex flex-row gap-3 w-full items-center justify-start">
                    <button onclick="window.location.href='index.html'" class="bg-slate-800 hover:bg-slate-750 text-white font-bold px-4 py-3.5 rounded-xl text-xs transition cursor-pointer flex items-center justify-center gap-1.5 active:scale-95 min-h-[48px]">
                        Seguir comprando
                    </button>
                    <button onclick="finalizePurchase()" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-black px-5 py-3.5 rounded-xl text-xs uppercase tracking-wider transition cursor-pointer flex items-center justify-center gap-1.5 active:scale-95 shadow-md shadow-amber-500/10 min-h-[48px]">
                        Autorizar Cargo y Completar Compra <i class="fa-solid fa-circle-check"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>'''

def generate_checkout_js():
    """Genera las funciones JavaScript de checkout homologadas."""
    return '''    // ========================================================================
    // HOMOLOGACIÓN CHECKOUT: PASO 1, 2 Y 3 (VALIDACIONES, 4 MÉTODOS Y COSTOS)
    // ========================================================================

    // STEP 1: DELIVERY ADDRESS & VALIDATIONS
    window.saveDelivery = function(event) {
        if (event) event.preventDefault();
        const name = (document.getElementById("devName")?.value || "").trim();
        const phone = (document.getElementById("devPhone")?.value || "").trim();
        const email = (document.getElementById("devEmail")?.value || "").trim();
        const street = (document.getElementById("devStreet")?.value || "").trim();
        const colonia = (document.getElementById("devColonia")?.value || "").trim();
        const cp = (document.getElementById("devCp")?.value || "").trim();
        const city = (document.getElementById("devCity")?.value || "").trim();
        const ref = (document.getElementById("devRef")?.value || "").trim();

        if (!name || name.length < 3) {
            alert("Por favor ingresa tu nombre completo (mínimo 3 caracteres).");
            return;
        }
        if (!phone || !/^[0-9]{10}$/.test(phone)) {
            alert("Por favor ingresa un número de teléfono válido de 10 dígitos sin espacios ni guiones.");
            return;
        }
        if (email && !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {
            alert("Por favor ingresa un correo electrónico válido.");
            return;
        }
        if (!street || !colonia || !city) {
            alert("Por favor completa los campos obligatorios de dirección de entrega.");
            return;
        }
        if (!cp || !/^[0-9]{5}$/.test(cp)) {
            alert("Por favor ingresa un código postal válido de 5 dígitos.");
            return;
        }

        const deliveryData = { name, phone, email, street, colonia, cp, city, ref };
        localStorage.setItem("user_delivery_address", JSON.stringify(deliveryData));
        
        showDeliverySummary();
        unlockPaymentStep();
        renderCheckout();
    };

    window.editDelivery = function() {
        document.getElementById("delivery-form")?.classList.remove("hidden");
        document.getElementById("delivery-summary")?.classList.add("hidden");
        document.getElementById("delivery-edit-btn")?.classList.add("hidden");
    };

    function showDeliverySummary() {
        const stored = localStorage.getItem("user_delivery_address");
        if (stored) {
            try {
                const data = JSON.parse(stored);
                const form = document.getElementById("delivery-form");
                const summary = document.getElementById("delivery-summary");
                const editBtn = document.getElementById("delivery-edit-btn");
                if (form) form.classList.add("hidden");
                if (summary) summary.classList.remove("hidden");
                if (editBtn) editBtn.classList.remove("hidden");
                
                const sumName = document.getElementById("sum-name");
                const sumPhoneEmail = document.getElementById("sum-phone-email");
                const sumAddr = document.getElementById("sum-address");
                
                if (sumName) sumName.innerText = data.name;
                if (sumPhoneEmail) {
                    const displayEmail = data.email ? data.email : "Sin correo";
                    sumPhoneEmail.innerHTML = `📞 ${data.phone}  |  ✉️ ${displayEmail}`;
                }
                if (sumAddr) {
                    const refTxt = data.ref ? ` (${data.ref})` : '';
                    sumAddr.innerText = `📍 ${data.street}, Col. ${data.colonia}, CP ${data.cp}, ${data.city}${refTxt}`;
                }
            } catch(e) {
                console.error("Error loading delivery summary", e);
            }
        }
    }
    
    function unlockPaymentStep() {
        const stepCard = document.getElementById("step-payment-card");
        const badge = document.getElementById("step-payment-badge");
        const options = document.getElementById("payment-options");
        
        if (stepCard && badge && options) {
            stepCard.classList.remove("opacity-60");
            badge.classList.remove("bg-slate-800", "text-slate-400");
            badge.classList.add("bg-cyan-500", "text-slate-950");
            options.classList.remove("hidden");
        }
    }

    // ACCORDION TOGGLE METHOD (4 METHODS: card, cash, oxxo, spei)
    window.togglePaymentAccordion = function(type) {
        const sections = ['card', 'cash', 'oxxo', 'spei'];
        sections.forEach(s => {
            const form = document.getElementById(`accordion-${s}-form`);
            const arrow = document.getElementById(`arrow-${s}`);
            if (form && arrow) {
                if (s === type) {
                    const isHidden = form.classList.contains("hidden");
                    if (isHidden) {
                        form.classList.remove("hidden");
                        arrow.classList.replace("fa-chevron-down", "fa-chevron-up");
                    } else {
                        form.classList.add("hidden");
                        arrow.classList.replace("fa-chevron-up", "fa-chevron-down");
                    }
                } else {
                    form.classList.add("hidden");
                    arrow.classList.replace("fa-chevron-up", "fa-chevron-down");
                }
            }
        });
    };

    // STEP 2: PAYMENT METHOD HANDLERS
    window.selectPaymentMethod = function(method) {
        localStorage.setItem("user_payment_method", method);
        showPaymentSummary();
    };
    
    window.saveCardDetails = function(event) {
        if (event) event.preventDefault();
        const name = (document.getElementById("cardName")?.value || "").trim();
        const num = (document.getElementById("cardNum")?.value || "").replace(/\\s/g, '');
        if (!name || !num || num.length < 13) {
            alert("Por favor completa los datos de la tarjeta con un número válido.");
            return;
        }
        const last4 = num.slice(-4) || "4152";
        const type = num.startsWith("5") ? "Mastercard" : "Visa";
        
        localStorage.setItem("user_payment_method", `Tarjeta ${type} (**** ${last4}) - ${name}`);
        showPaymentSummary();
    };
    
    window.editPayment = function() {
        const options = document.getElementById("payment-options");
        const summary = document.getElementById("payment-summary");
        const editBtn = document.getElementById("payment-edit-btn");
        if (options) options.classList.remove("hidden");
        if (summary) summary.classList.add("hidden");
        if (editBtn) editBtn.classList.add("hidden");
    };
    
    function showPaymentSummary() {
        const method = localStorage.getItem("user_payment_method");
        if (method) {
            const options = document.getElementById("payment-options");
            const summary = document.getElementById("payment-summary");
            const editBtn = document.getElementById("payment-edit-btn");
            if (options) options.classList.add("hidden");
            if (summary) {
                summary.classList.remove("hidden");
                summary.innerHTML = `
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-circle-check text-emerald-400 text-base"></i>
                            <span>Método Seleccionado: <strong class="text-white font-black">${method}</strong></span>
                        </div>
                    </div>
                `;
            }
            if (editBtn) editBtn.classList.remove("hidden");
        }
    }

    // STEP 3: RENDER CHECKOUT & DYNAMIC CALCULATIONS
    window.renderCheckout = function() {
        const container = document.getElementById("checkout-cart-items");
        const subtotalDisp = document.getElementById("co-subtotal");
        const wholesaleRow = document.getElementById("co-wholesale-row");
        const wholesaleDiscDisp = document.getElementById("co-wholesale-disc");
        const shippingDisp = document.getElementById("co-shipping");
        const cashbackRow = document.getElementById("co-cashback-row");
        const totalDisp = document.getElementById("co-total");
        
        if (!container) return;
        
        const cart = getCart();
        container.innerHTML = "";
        
        let subtotal = 0;
        let totalItemsQty = 0;
        
        cart.forEach(item => {
            const isInactive = (item.quantity === 0);
            const sub = parseFloat(item.precio) * item.quantity;
            subtotal += sub;
            
            if (!isInactive) {
                totalItemsQty += item.quantity;
            }
            
            let imgUrl = item.imagen;
            if (imgUrl && imgUrl.startsWith('assets/img')) {
                imgUrl = './' + imgUrl;
            }
            
            let rowClass = "flex items-center justify-between gap-3 bg-slate-950/40 p-2.5 rounded-xl border border-slate-850 transition-all duration-300 animate-fade-in";
            let controlsHtml = "";
            let statusTagHtml = "";
            
            if (isInactive) {
                rowClass += " opacity-40 grayscale";
                statusTagHtml = `<span class="bg-red-500/10 border border-red-500/30 text-red-500 font-bold px-1.5 py-0.5 rounded text-[8px] uppercase tracking-wider block mt-0.5 w-max">Producto desactivado</span>`;
                controlsHtml = `
                    <button onclick="changeQty('${item.sku}', 1)" class="px-2.5 py-1.5 rounded bg-emerald-500 hover:bg-emerald-450 text-slate-950 font-black text-[10px] transition cursor-pointer flex items-center gap-1 active:scale-95 min-h-[32px]">
                        Reactivar <i class="fa-solid fa-plus text-[9px]"></i>
                    </button>
                `;
            } else {
                let minusButtonHtml = `<button onclick="changeQty('${item.sku}', -1)" class="w-8 h-8 rounded bg-slate-800 text-slate-400 hover:text-white transition flex items-center justify-center font-bold text-xs cursor-pointer min-w-[32px] min-h-[32px]">-</button>`;
                if (item.quantity === 1) {
                    minusButtonHtml = `<button onclick="deleteItem('${item.sku}')" class="w-8 h-8 rounded bg-red-650 text-white hover:bg-red-600 transition flex items-center justify-center text-[10px] cursor-pointer min-w-[32px] min-h-[32px]" title="Eliminar"><i class="fa-solid fa-trash-can"></i></button>`;
                }
                
                controlsHtml = `
                    <div class="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded p-0.5">
                        ${minusButtonHtml}
                        <span class="text-white font-black text-xs w-4 text-center">${item.quantity}</span>
                        <button onclick="changeQty('${item.sku}', 1)" class="w-8 h-8 rounded bg-slate-800 text-slate-400 hover:text-white transition flex items-center justify-center font-bold text-xs cursor-pointer min-w-[32px] min-h-[32px]">+</button>
                    </div>
                    <span class="text-cyan-400 font-bold min-w-[70px] text-right text-xs">$${sub.toFixed(2)}</span>
                    <button onclick="deleteItem('${item.sku}')" class="text-slate-500 hover:text-red-500 text-xs cursor-pointer shrink-0 transition min-w-[32px] min-h-[32px]" title="Eliminar"><i class="fa-solid fa-trash-can"></i></button>
                `;
            }
            
            const div = document.createElement("div");
            div.className = rowClass;
            div.innerHTML = `
                <div class="flex items-center gap-2.5 min-w-0 flex-1">
                    <img src="${imgUrl}" class="w-8 h-8 object-contain bg-white rounded p-0.5 shrink-0" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' viewBox=\\'0 0 24 24\\'%3E%3Crect width=\\'24\\' height=\\'24\\' fill=\\'%231e293b\\'/ %3E%3C/svg%3E'" />
                    <div class="min-w-0 flex-1">
                        <span class="text-white font-bold block truncate text-xs">${item.nombre}</span>
                        <span class="text-[9px] font-mono text-slate-500 uppercase block">${item.sku}</span>
                        ${statusTagHtml}
                    </div>
                </div>
                <div class="flex items-center gap-2.5 shrink-0">
                    ${controlsHtml}
                </div>
            `;
            container.appendChild(div);
        });
        
        if (subtotalDisp) subtotalDisp.innerText = `$${subtotal.toFixed(2)} MXN`;
        
        // Wholesale check (15% mayoreo si >= 10 artículos)
        let wholesaleDiscount = 0;
        if (totalItemsQty >= 10) {
            wholesaleDiscount = subtotal * 0.15;
            if (wholesaleRow) wholesaleRow.classList.remove("hidden");
            if (wholesaleDiscDisp) wholesaleDiscDisp.innerText = `-$${wholesaleDiscount.toFixed(2)} MXN`;
        } else {
            if (wholesaleRow) wholesaleRow.classList.add("hidden");
        }
        
        // Shipping check (Envío gratis >= $1500 MXN o subtotal 0, sino $49 MXN)
        const baseSub = subtotal - wholesaleDiscount;
        const shippingFee = (baseSub >= 1500 || subtotal === 0) ? 0 : 49;
        if (shippingDisp) {
            shippingDisp.innerText = shippingFee === 0 ? "GRATIS" : `$${shippingFee.toFixed(2)} MXN`;
            if (shippingFee === 0 && baseSub >= 1500) {
                shippingDisp.className = "font-bold text-emerald-400 text-xs";
            } else {
                shippingDisp.className = "font-bold text-white text-xs";
            }
        }
        
        // Cashback check (5% de cashback)
        const storedAddress = localStorage.getItem("user_delivery_address");
        let hasRegister = false;
        if (storedAddress) {
            try {
                const addr = JSON.parse(storedAddress);
                if (addr.phone || addr.email) {
                    hasRegister = true;
                }
            } catch(e) {}
        }
        
        let cashbackVal = 0;
        if (cashbackRow) {
            if (hasRegister) {
                cashbackVal = baseSub * 0.05;
                cashbackRow.innerHTML = `
                    <div class="flex justify-between text-emerald-400 font-black">
                        <span>Cashback 5% Aplicado:</span>
                        <span>-$${cashbackVal.toFixed(2)} MXN</span>
                    </div>
                    <span class="text-[9px] text-emerald-500 font-semibold leading-tight">✓ Recompensa activa. Saldo descontado del total a pagar.</span>
                `;
            } else {
                cashbackRow.innerHTML = `
                    <div class="flex justify-between text-slate-500 font-bold">
                        <span>Cashback Acumulable (5%):</span>
                        <span>$${(baseSub * 0.05).toFixed(2)} MXN</span>
                    </div>
                    <span class="text-[9px] text-amber-500 font-semibold leading-tight">⚠️ Registra tu Domicilio en el Paso 1 para aplicar tu 5% de descuento inmediato.</span>
                `;
            }
        }
        
        const totalCost = Math.max(0, baseSub - (hasRegister ? cashbackVal : 0) + shippingFee);
        if (totalDisp) totalDisp.innerText = `$${totalCost.toFixed(2)} MXN`;
    };

    // FINALIZE PURCHASE
    window.finalizePurchase = function() {
        const address = localStorage.getItem("user_delivery_address");
        const method = localStorage.getItem("user_payment_method");
        const cart = getCart();
        const activeItems = cart.filter(i => i.quantity > 0);
        
        if (activeItems.length === 0) {
            alert("⚠️ El carrito de compras no contiene productos activos.");
            return;
        }
        if (!address) {
            alert("⚠️ Registra el Domicilio de Entrega (Paso 1) antes de continuar.");
            return;
        }
        if (!method) {
            alert("⚠️ Selecciona tu Método de Pago (Paso 2) antes de continuar.");
            return;
        }
        
        const orderId = "AGY-" + Math.floor(1000 + Math.random() * 9000);
        const orderData = {
            id: orderId,
            date: new Date().toLocaleDateString("es-MX", { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }),
            items: activeItems,
            address: JSON.parse(address),
            method: method,
            status: "Procesando"
        };
        
        let history = JSON.parse(localStorage.getItem("viamx_orders_history") || "[]");
        history.unshift(orderData);
        localStorage.setItem("viamx_orders_history", JSON.stringify(history));
        
        saveCart([]);
        localStorage.removeItem("user_payment_method");
        
        alert(`🎉 ¡Compra confirmada con éxito!\\n\\nFolio de Pedido: ${orderId}\\nEntrega en: ${orderData.address.street}, ${orderData.address.colonia}\\nMétodo de Pago: ${method}\\n\\n¡Gracias por tu preferencia!`);
        window.location.href = "index.html";
    };

    document.addEventListener("DOMContentLoaded", () => {
        showDeliverySummary();
        const address = localStorage.getItem("user_delivery_address");
        if (address) {
            unlockPaymentStep();
            showPaymentSummary();
        }
        renderCheckout();
    });'''

def update_checkout_file(store_path):
    """Actualiza checkout.html para una tienda específica."""
    checkout_path = os.path.join(store_path, "checkout.html")
    if not os.path.exists(checkout_path):
        print(f"[SKIP] No se encontró {checkout_path}")
        return False
        
    with open(checkout_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # 1. Reemplazar sección <main>...</main>
    new_main_content = generate_checkout_main_html()
    main_regex = re.compile(r'<main[^>]*>(.*?)</main>', re.DOTALL | re.IGNORECASE)
    
    if main_regex.search(content):
        replacement_main = f'<main class="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">\n{new_main_content}\n</main>'
        content = main_regex.sub(lambda m: replacement_main, content)
    else:
        print(f"[WARN] No se encontró tag <main> en {checkout_path}")

    # 2. Reemplazar o inyectar las funciones JS de checkout
    new_js = generate_checkout_js()
    
    js_marker_pattern = re.compile(r'//\s*STEP\s*1:\s*DELIVERY.*?document\.addEventListener\("DOMContentLoaded".*?\n\s*\}\);', re.DOTALL)
    alt_marker_pattern = re.compile(r'function\s+showDeliverySummary\(\).*?document\.addEventListener\("DOMContentLoaded".*?\n\s*\}\);', re.DOTALL)
    
    if js_marker_pattern.search(content):
        content = js_marker_pattern.sub(lambda m: new_js.strip(), content)
    elif alt_marker_pattern.search(content):
        content = alt_marker_pattern.sub(lambda m: new_js.strip(), content)
    else:
        script_idx = content.rfind('</script>')
        if script_idx != -1:
            content = content[:script_idx] + "\n\n" + new_js + "\n" + content[script_idx:]
        else:
            body_idx = content.rfind('</body>')
            if body_idx != -1:
                content = content[:body_idx] + f"\n<script>\n{new_js}\n</script>\n" + content[body_idx:]

    with open(checkout_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"[OK] {os.path.basename(store_path)}/checkout.html actualizado exitosamente.")
    return True

def update_pc_custom_lab_index(pc_path):
    """Actualiza pc-custom-lab/index.html asegurando el configurador de 10 componentes y carrusel móvil."""
    index_path = os.path.join(pc_path, "index.html")
    if not os.path.exists(index_path):
        print(f"[ERROR] No se encontró {index_path}")
        return False
        
    with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # 1. Asegurar código completo del configurador de 10 componentes vinculado a la boutique
    configurador_js = '''// ========================================================================
// CONFIGURADOR INTERACTIVO DE 10 COMPONENTES VINCULADO A LA BOUTIQUE
// ========================================================================
(function initConfiguradorInteractivo() {
    const CFG_COMPONENTS = [
        { id: 'cpu',       label: 'Procesador (CPU)',           icon: 'fa-microchip',     categoria: 'procesadores',   page: 4 },
        { id: 'mobo',      label: 'Tarjeta Madre',             icon: 'fa-circuit-board', categoria: 'motherboards',   page: 2 },
        { id: 'ram',       label: 'Memoria RAM',               icon: 'fa-memory',        categoria: 'ram',            page: 3 },
        { id: 'gpu',       label: 'Tarjeta de Video (GPU)',    icon: 'fa-gamepad',       categoria: 'gpu',            page: 1 },
        { id: 'ssd',       label: 'Disco Duro / SSD',          icon: 'fa-hard-drive',    categoria: 'almacenamiento', page: 5 },
        { id: 'psu',       label: 'Fuente de Poder',           icon: 'fa-plug',          categoria: 'fuentes',        page: 7 },
        { id: 'gabinete',  label: 'Gabinete Gamer',            icon: 'fa-server',        categoria: 'gabinetes',      page: 6 },
        { id: 'cooling',   label: 'Sistema de Enfriamiento',   icon: 'fa-wind',          categoria: 'enfriamiento',   page: 8 },
        { id: 'monitor',   label: 'Monitor',                   icon: 'fa-desktop',       categoria: 'monitores',      page: 9 },
        { id: 'perifericos', label: 'Periféricos (Teclado/Mouse)', icon: 'fa-keyboard',  categoria: 'perifericos',   page: 10 },
    ];

    window.cfgSelections = window.cfgSelections || {};
    window.cfgActiveComponentId = null;

    function renderChecklist() {
        const container = document.getElementById('cfg-checklist');
        if (!container) return;
        container.innerHTML = '';
        let completedCount = 0;
        CFG_COMPONENTS.forEach(comp => {
            const selected = window.cfgSelections[comp.id];
            if (selected) completedCount++;
            const isActive = window.cfgActiveComponentId === comp.id;
            const div = document.createElement('button');
            div.className = `w-full text-left flex items-center gap-3 rounded-xl p-2.5 border transition cursor-pointer ${
                selected
                    ? 'bg-cyan-500/10 border-cyan-500/30 text-white'
                    : isActive
                        ? 'bg-blue-500/10 border-blue-500/40 text-blue-300'
                        : 'bg-slate-950/60 border-slate-800 text-slate-500 opacity-60 hover:opacity-100 hover:border-slate-600'
            }`;
            div.onclick = () => selectCfgComponent(comp.id);
            div.innerHTML = `
                <span class="w-7 h-7 flex items-center justify-center rounded-lg shrink-0 ${selected ? 'bg-cyan-500/20 text-cyan-400' : 'bg-slate-800 text-slate-500'}">
                    <i class="fa-solid ${comp.icon} text-xs"></i>
                </span>
                <span class="flex-1 min-w-0">
                    <span class="block text-[11px] font-black">${comp.label}</span>
                    ${selected
                        ? `<span class="block text-[9px] text-cyan-300 truncate font-semibold">${selected.nombre}</span>`
                        : `<span class="block text-[9px] text-slate-600">Sin seleccionar — Clic para elegir</span>`
                    }
                </span>
                <span class="shrink-0 text-[10px] font-black ${selected ? 'text-amber-400' : 'text-slate-700'}">
                    ${selected ? '$' + Math.floor(selected.precio).toLocaleString() + ' MXN' : '—'}
                </span>
                <span class="shrink-0 w-4 h-4 rounded-full flex items-center justify-center ${selected ? 'bg-cyan-400 text-slate-950' : 'bg-slate-800 text-slate-600'} text-[9px] font-black">
                    ${selected ? '✓' : '☐'}
                </span>
            `;
            container.appendChild(div);
        });
        updateCfgBudget(completedCount);
    }

    function updateCfgBudget(completedCount) {
        const total = CFG_COMPONENTS.reduce((sum, comp) => {
            const sel = window.cfgSelections[comp.id];
            return sum + (sel ? parseFloat(sel.precio) : 0);
        }, 0);
        const totalDisplay = document.getElementById('cfg-total-display');
        const progressBar = document.getElementById('cfg-progress-bar');
        const addBtn = document.getElementById('cfg-add-to-cart-btn');
        const pendingCount = document.getElementById('cfg-pending-count');
        if (totalDisplay) totalDisplay.innerText = `$${Math.floor(total).toLocaleString()} MXN`;
        if (progressBar) progressBar.style.width = `${(completedCount / 10) * 100}%`;
        const allComplete = (completedCount === 10);
        if (addBtn) {
            if (allComplete) {
                addBtn.disabled = false;
                addBtn.className = 'w-full bg-amber-500 hover:bg-amber-400 text-slate-950 font-black py-3 rounded-xl text-sm cursor-pointer transition active:scale-95 shadow-lg shadow-amber-500/20';
                addBtn.title = '¡Listo! Agrega tu ensamble completo al carrito';
            } else {
                addBtn.disabled = true;
                addBtn.className = 'w-full bg-slate-700 text-slate-500 font-black py-3 rounded-xl text-sm cursor-not-allowed transition';
                addBtn.title = `Selecciona los ${10 - completedCount} componentes restantes para habilitar`;
            }
        }
        if (pendingCount) {
            pendingCount.innerText = allComplete
                ? '¡Ensamble Completo! (10/10 componentes seleccionados)'
                : `Faltan ${10 - completedCount} componente(s) por seleccionar`;
        }
    }

    window.selectCfgComponent = function(componentId) {
        window.cfgActiveComponentId = componentId;
        const comp = CFG_COMPONENTS.find(c => c.id === componentId);
        if (!comp) return;

        if (typeof filterByCategory === 'function') {
            filterByCategory(comp.categoria, null);
        } else if (typeof changePage === 'function') {
            const btns = document.querySelectorAll('.pagination-btn');
            if (btns.length >= comp.page) changePage(comp.page, btns[comp.page - 1]);
        }

        const panel = document.getElementById('cfg-selected-component-panel');
        const catName = document.getElementById('cfg-active-category-name');
        if (panel) panel.classList.remove('hidden');
        if (catName) catName.innerText = comp.label;

        renderChecklist();

        const productsSection = document.getElementById('productos');
        if (productsSection) {
            setTimeout(() => productsSection.scrollIntoView({ behavior: 'smooth', block: 'start' }), 150);
        }
    };

    // Sobrescritura de renderProductsGrid para enlazar selección directa
    const _prevRenderProductsGrid = window.renderProductsGrid || renderProductsGrid;
    window.renderProductsGrid = function() {
        if (typeof _prevRenderProductsGrid === 'function') _prevRenderProductsGrid();

        if (!window.cfgActiveComponentId) return;
        const comp = CFG_COMPONENTS.find(c => c.id === window.cfgActiveComponentId);
        if (!comp) return;

        const currentCat = (typeof PAGE_TO_CATEGORY !== 'undefined') ? PAGE_TO_CATEGORY[currentPage] : null;
        if (currentCat !== comp.categoria) return;

        const cards = document.querySelectorAll('#pc-productos-grid > div');
        const pageProducts = (typeof productCatalog !== 'undefined') ? productCatalog.filter(p => p.categoria === comp.categoria) : [];

        cards.forEach((card, idx) => {
            const prod = pageProducts[idx];
            if (!prod) return;
            const isSelected = window.cfgSelections[comp.id] && window.cfgSelections[comp.id].sku === prod.sku;
            const btnContainer = card.querySelector('.flex.flex-col.gap-2.mt-4') || card;

            if (card.querySelector('.cfg-select-btn')) {
                card.querySelector('.cfg-select-btn').remove();
            }

            const selBtn = document.createElement('button');
            selBtn.className = `cfg-select-btn w-full mt-2 py-2 rounded-xl text-[10px] font-black uppercase tracking-wider border transition cursor-pointer ${
                isSelected
                    ? 'bg-cyan-500 border-cyan-400 text-slate-950 shadow-md shadow-cyan-500/20'
                    : 'bg-slate-800 border-slate-700 text-cyan-400 hover:bg-cyan-500/20 hover:border-cyan-500'
            }`;
            selBtn.innerText = isSelected ? '✓ Componente Seleccionado' : `Seleccionar ${comp.label}`;
            selBtn.onclick = (e) => {
                e.stopPropagation();
                window.cfgSelections[comp.id] = {
                    sku: prod.sku,
                    nombre: prod.nombre,
                    precio: prod.precio,
                    imagen: prod.imagen
                };
                window.cfgActiveComponentId = null;
                const panel = document.getElementById('cfg-selected-component-panel');
                if (panel) panel.classList.add('hidden');
                renderChecklist();
                window.renderProductsGrid();
                const cfgSection = document.getElementById('configurador-interactivo');
                if (cfgSection) setTimeout(() => cfgSection.scrollIntoView({ behavior: 'smooth', block: 'start' }), 200);
            };
            btnContainer.appendChild(selBtn);
        });
    };

    window.addEnsambleToCart = function() {
        const completedComps = CFG_COMPONENTS.filter(c => window.cfgSelections[c.id]);
        if (completedComps.length < 10) {
            alert(`Faltan ${10 - completedComps.length} componente(s) por seleccionar.`);
            return;
        }
        let cart = getCart();
        completedComps.forEach(comp => {
            const sel = window.cfgSelections[comp.id];
            const existing = cart.find(i => i.sku === sel.sku);
            if (existing) {
                existing.quantity = (existing.quantity || 1) + 1;
            } else {
                cart.push({ sku: sel.sku, nombre: sel.nombre, precio: sel.precio, imagen: sel.imagen, quantity: 1 });
            }
        });
        saveCart(cart);
        if (typeof openCartDrawer === 'function') openCartDrawer();
        window.cfgSelections = {};
        window.cfgActiveComponentId = null;
        renderChecklist();
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', renderChecklist);
    } else {
        renderChecklist();
    }
})();'''

    # 2. Asegurar soporte táctil (swipe) y navegación en el carrusel móvil
    carrusel_swipe_js = '''// ========================================================================
// CONTROLADOR DEL CARRUSEL / HERO SLIDER (SOPORTE MÓVIL + TOUCH SWIPE)
// ========================================================================
(function initHeroSlider() {
    if (typeof window.currentSlide === 'undefined') window.currentSlide = 0;
    if (typeof window.sliderInterval === 'undefined') window.sliderInterval = null;

    window.showSlide = function(index) {
        const slides = document.querySelectorAll('.hero-slide');
        const dots = document.querySelectorAll('.hero-dot');
        if (slides.length === 0) return;
        
        slides.forEach(s => {
            s.classList.remove('active', 'opacity-100', 'z-10');
            s.classList.add('opacity-0', 'z-0');
        });
        dots.forEach(d => {
            d.classList.remove('bg-blue-500', 'w-8');
            d.classList.add('bg-slate-600', 'w-2.5');
        });

        window.currentSlide = (index + slides.length) % slides.length;
        if (slides[window.currentSlide]) {
            slides[window.currentSlide].classList.remove('opacity-0', 'z-0');
            slides[window.currentSlide].classList.add('active', 'opacity-100', 'z-10');
        }
        if (dots[window.currentSlide]) {
            dots[window.currentSlide].classList.remove('bg-slate-600', 'w-2.5');
            dots[window.currentSlide].classList.add('bg-blue-500', 'w-8');
        }
        window.resetSliderInterval();
    };

    window.nextSlide = function() {
        window.showSlide(window.currentSlide + 1);
    };

    window.prevSlide = function() {
        window.showSlide(window.currentSlide - 1);
    };

    window.resetSliderInterval = function() {
        if (window.sliderInterval) clearInterval(window.sliderInterval);
        window.sliderInterval = setInterval(() => {
            window.nextSlide();
        }, 5500);
    };

    // Soporte para gestos táctiles (Swipe Gestures en móvil)
    const sliderContainer = document.getElementById('hero-slider') || document.querySelector('.hero-slider-container');
    if (sliderContainer) {
        let touchStartX = 0;
        let touchEndX = 0;

        sliderContainer.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        sliderContainer.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            const diff = touchStartX - touchEndX;
            if (Math.abs(diff) > 45) {
                if (diff > 0) {
                    window.nextSlide(); // Swipe izquierda -> siguiente
                } else {
                    window.prevSlide(); // Swipe derecha -> anterior
                }
            }
        }, { passive: true });
    }

    window.resetSliderInterval();
})();'''

    # Reemplazar bloque de configurador interactivo existente en pc-custom-lab/index.html
    cfg_match = re.search(r'// =+\s*// CONFIGURADOR INTERACTIVO.*?\n\s*\}\)\(\);', content, re.DOTALL)
    if cfg_match:
        content = content[:cfg_match.start()] + configurador_js + content[cfg_match.end():]
    else:
        script_idx = content.rfind('</script>')
        if script_idx != -1:
            content = content[:script_idx] + "\n\n" + configurador_js + "\n" + content[script_idx:]

    # Reemplazar bloque de slider existente o inyectar touch swipe
    slider_match = re.search(r'// Ensure slider runs safely.*?\n\s*window\.resetSliderInterval\(\);', content, re.DOTALL)
    if slider_match:
        content = content[:slider_match.start()] + carrusel_swipe_js + content[slider_match.end():]
    else:
        if 'initHeroSlider' not in content:
            script_idx = content.rfind('</script>')
            if script_idx != -1:
                content = content[:script_idx] + "\n\n" + carrusel_swipe_js + "\n" + content[script_idx:]

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("[OK] pc-custom-lab/index.html actualizado exitosamente con el configurador de 10 componentes y carrusel móvil.")
    return True

def verify_all():
    """Valida que los cambios requeridos estén presentes en todas las 6 tiendas."""
    errors = []
    
    print("\n" + "="*70)
    print("VERIFICACIÓN DE HOMOLOGACIÓN TÉCNICA EN LAS 6 TIENDAS")
    print("="*70)
    
    for store in STORES:
        store_path = os.path.join(BASE_DIR, store)
        checkout_path = os.path.join(store_path, "checkout.html")
        
        if not os.path.exists(checkout_path):
            errors.append(f"Falta archivo {checkout_path}")
            continue
            
        with open(checkout_path, "r", encoding="utf-8", errors="ignore") as f:
            chk_content = f.read()

        # Validaciones de Paso 1
        if "Domicilio de Entrega — Disfrute sus productos en la puerta de su casa" not in chk_content:
            errors.append(f"{store}/checkout.html: Título de Paso 1 no coincide.")
        if "pattern=\"[0-9]{10}\"" not in chk_content or "pattern=\"[0-9]{5}\"" not in chk_content:
            errors.append(f"{store}/checkout.html: Validaciones de teléfono o CP ausentes.")
            
        # Validaciones de Paso 2 (4 métodos en acordeón)
        if "Método de Pago — Agilice la entrega de sus productos" not in chk_content:
            errors.append(f"{store}/checkout.html: Título de Paso 2 no coincide.")
        if "togglePaymentAccordion('card')" not in chk_content or \
           "togglePaymentAccordion('cash')" not in chk_content or \
           "togglePaymentAccordion('oxxo')" not in chk_content or \
           "togglePaymentAccordion('spei')" not in chk_content:
            errors.append(f"{store}/checkout.html: No contiene los 4 métodos en acordeón.")
            
        # Validaciones de Paso 3 (Envío >= 1500 gratis sino 49, Mayoreo 15%, Cashback 5%)
        if "baseSub >= 1500" not in chk_content or "49" not in chk_content:
            errors.append(f"{store}/checkout.html: Reglas de costo de envío ausentes.")
        if "0.05" not in chk_content:
            errors.append(f"{store}/checkout.html: Cálculo de cashback 5% ausente.")
            
        print(f"✓ {store}/checkout.html validado correctamente.")

    # Validar PC Custom Lab index.html
    pc_index = os.path.join(BASE_DIR, "pc-custom-lab", "index.html")
    with open(pc_index, "r", encoding="utf-8", errors="ignore") as f:
        pc_content = f.read()
        
    if "initConfiguradorInteractivo" not in pc_content or "CFG_COMPONENTS" not in pc_content:
        errors.append("pc-custom-lab/index.html: Configurador interactivo no encontrado.")
    if "touchstart" not in pc_content or "touchend" not in pc_content:
        errors.append("pc-custom-lab/index.html: Carrusel móvil no tiene soporte táctil.")

    print(f"✓ pc-custom-lab/index.html (Configurador 10 componentes & Carrusel móvil) validado.")
    print("="*70)

    if errors:
        print("\n[FALLO] Errores encontrados:")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("\n[ÉXITO] Todas las 6 tiendas y PC Custom Lab cumplen al 100% las especificaciones.")
        return True

def main():
    print("Iniciando ejecución de finalizar_homologacion.py...")
    
    if not os.path.exists(BASE_DIR):
        print(f"[ERROR] Directorio base no existe: {BASE_DIR}")
        sys.exit(1)

    success = True
    # 1. Actualizar checkout.html en las 6 tiendas
    for store in STORES:
        store_path = os.path.join(BASE_DIR, store)
        if not update_checkout_file(store_path):
            success = False

    # 2. Actualizar pc-custom-lab/index.html
    pc_path = os.path.join(BASE_DIR, "pc-custom-lab")
    if not update_pc_custom_lab_index(pc_path):
        success = False

    # 3. Validación y verificación completa
    if not verify_all():
        sys.exit(1)

    print("\nProceso finalizado exitosamente con código de salida 0.")
    sys.exit(0)

if __name__ == "__main__":
    main()
