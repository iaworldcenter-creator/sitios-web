import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
PC_INDEX_PATH = os.path.join(BASE_DIR, "pc-custom-lab", "index.html")

COTIZADOR_SECTION_HTML = """<!-- COTIZADOR MATRIZ INTERACTIVO: PIRÁMIDE VISUAL + MATRIZ DE PARES + SLIDER -->
<section class="py-20 bg-slate-900/90 border-y border-slate-800" id="cotizador">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <!-- ENCABEZADO CENTRADO -->
        <div class="text-center mb-12">
            <span class="px-3.5 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 font-mono text-xs uppercase tracking-widest inline-block mb-3">
                Configurador Modular Interactivo 2026
            </span>
            <h2 class="text-3xl sm:text-4xl font-black text-white">Configura tu Equipo Paso a Paso</h2>
            <p class="text-slate-400 text-sm mt-2 max-w-2xl mx-auto">Arma tu PC a la medida, cotiza componentes sueltos o desliza tu presupuesto para encontrar tu ensamble ideal.</p>
        </div>

        <!-- CONTENEDOR PRINCIPAL EN 2 COLUMNAS (PIRÁMIDE IZQ + MATRIZ DER) -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            
            <!-- COLUMNA IZQUIERDA: PIRÁMIDE VISUAL DE COMPONENTES (4 COLUMNAS LG) -->
            <div class="lg:col-span-5 bg-slate-950 border border-slate-800 rounded-3xl p-5 sm:p-6 shadow-2xl flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
                        <h3 class="text-xs font-mono font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-2">
                            <i class="fa-solid fa-layer-group"></i> Resumen Piramidal de Piezas
                        </h3>
                        <span class="text-[10px] font-mono text-slate-500">Clic para cotizar suelta</span>
                    </div>

                    <!-- LISTA ESCALONADA PIRAMIDAL (DEL MÁS CORTO AL MÁS LARGO) -->
                    <div class="flex flex-col gap-1.5" id="pyramid-list">
                        <button type="button" onclick="focusComponent('select-ram')" class="pyramid-row w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300">1. Memoria RAM</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-ram">$0 MXN</span>
                        </button>
                        <button type="button" onclick="focusComponent('select-mouse')" class="pyramid-row w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300">2. Mouse & Mousepad</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-mouse">$0 MXN</span>
                        </button>
                        <button type="button" onclick="focusComponent('select-psu')" class="pyramid-row w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300">3. Fuente de Poder</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-psu">$0 MXN</span>
                        </button>
                        <button type="button" onclick="focusComponent('select-monitor')" class="pyramid-row w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300">4. Monitor</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-monitor">$0 MXN</span>
                        </button>
                        <button type="button" onclick="focusComponent('select-teclado')" class="pyramid-row w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300">5. Teclado Gamer / Oficina</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-teclado">$0 MXN</span>
                        </button>
                        <button type="button" onclick="focusComponent('select-gabinete')" class="pyramid-row w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300">6. Gabinete (Chasis)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-gabinete">$0 MXN</span>
                        </button>
                        <button type="button" onclick="focusComponent('select-cpu')" class="pyramid-row w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300">7. Procesador (Intel / AMD)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-cpu">$0 MXN</span>
                        </button>
                        <button type="button" onclick="focusComponent('select-ssd')" class="pyramid-row w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300">8. Almacenamiento (SSD / HDD)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-ssd">$0 MXN</span>
                        </button>
                        <button type="button" onclick="focusComponent('select-gpu')" class="pyramid-row w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300">9. Tarjeta de Video (GPU)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-gpu">$0 MXN</span>
                        </button>
                        <button type="button" onclick="focusComponent('select-mobo')" class="pyramid-row w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300">10. Tarjeta Madre (Motherboard)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-mobo">$0 MXN</span>
                        </button>
                        <button type="button" onclick="focusComponent('select-cooling')" class="pyramid-row w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300">11. Sistema de Enfriamiento</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-cooling">$0 MXN</span>
                        </button>
                        <button type="button" onclick="focusComponent('select-software')" class="pyramid-row w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300">12. Sistema Operativo & Software</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-software">$0 MXN</span>
                        </button>
                    </div>
                </div>

                <!-- SEMÁFORO DE VALIDACIÓN DE HARDWARE FUNCIONAL -->
                <div class="mt-6 pt-4 border-t border-slate-800 flex flex-col gap-2">
                    <div id="status-hardware-badge" class="p-3 rounded-xl border text-xs font-bold transition flex items-start gap-2.5">
                        <!-- Generado por JavaScript -->
                    </div>
                </div>
            </div>

            <!-- COLUMNA DERECHA: MATRIZ DE SELECCIÓN DE 13 CAMPOS + SLIDER (7 COLUMNAS LG) -->
            <div class="lg:col-span-7 bg-slate-950 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl">
                <form id="form-cotizador" onchange="recalcularCotizador()">
                    
                    <!-- 1. SELECTOR MAESTRO DE NIVEL -->
                    <div class="mb-6 pb-5 border-b border-slate-800">
                        <label class="block text-xs font-mono font-bold text-amber-400 mb-1.5 uppercase tracking-wider" for="select-nivel-filtro">
                            1. Selecciona el Nivel Base de Ensamble
                        </label>
                        <select id="select-nivel-filtro" onchange="actualizarPrefiltroNivel()" class="w-full bg-slate-900 border border-amber-500/50 text-amber-200 rounded-xl p-3 text-xs sm:text-sm font-bold focus:border-amber-400 focus:outline-none transition cursor-pointer">
                            <option value="5" selected>Nivel 5 — Entrada / Hogar / Oficina (Intel Core i3 / Ryzen 3)</option>
                            <option value="4">Nivel 4 — Gama Media Moderna (Intel Core i5 / Ryzen 5)</option>
                            <option value="3">Nivel 3 — Gama Alta / Render / CAD 3D (Intel Core i7 / Ryzen 7)</option>
                            <option value="2">Nivel 2 — Categoría Entusiasta / IA (Core i9 / Ultra 7 / Ryzen 9)</option>
                            <option value="1">Nivel 1 — TOPPING EXTREME 2026 (Core Ultra 9 / Ryzen 9 9950X / RTX 5090)</option>
                        </select>
                    </div>

                    <!-- FILA 1: GABINETE + FUENTE -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 pb-4 border-b border-slate-800/60">
                        <div>
                            <label class="block text-[11px] font-mono font-bold text-blue-400 mb-1.5 uppercase" for="select-gabinete">2. Gabinete (Chasis)</label>
                            <select id="select-gabinete" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                        <div>
                            <label class="block text-[11px] font-mono font-bold text-emerald-400 mb-1.5 uppercase" for="select-psu">3. Fuente de Poder (PSU)</label>
                            <select id="select-psu" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                    </div>

                    <!-- FILA 2: PROCESADOR + ENFRIAMIENTO -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 pb-4 border-b border-slate-800/60">
                        <div>
                            <label class="block text-[11px] font-mono font-bold text-pink-400 mb-1.5 uppercase" for="select-cpu">4. Procesador (Intel / AMD)</label>
                            <select id="select-cpu" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                        <div>
                            <label class="block text-[11px] font-mono font-bold text-teal-400 mb-1.5 uppercase" for="select-cooling">5. Sistema de Enfriamiento</label>
                            <select id="select-cooling" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                    </div>

                    <!-- FILA 3: TARJETA MADRE + TARJETA DE VIDEO -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 pb-4 border-b border-slate-800/60">
                        <div>
                            <label class="block text-[11px] font-mono font-bold text-purple-400 mb-1.5 uppercase" for="select-mobo">6. Tarjeta Madre</label>
                            <select id="select-mobo" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                        <div>
                            <label class="block text-[11px] font-mono font-bold text-indigo-400 mb-1.5 uppercase" for="select-gpu">7. Tarjeta de Video (GPU)</label>
                            <select id="select-gpu" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                    </div>

                    <!-- FILA 4: MEMORIA RAM + ALMACENAMIENTO -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 pb-4 border-b border-slate-800/60">
                        <div>
                            <label class="block text-[11px] font-mono font-bold text-cyan-400 mb-1.5 uppercase" for="select-ram">8. Memoria RAM</label>
                            <select id="select-ram" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                        <div>
                            <label class="block text-[11px] font-mono font-bold text-amber-400 mb-1.5 uppercase" for="select-ssd">9. Almacenamiento (SSD / HDD)</label>
                            <select id="select-ssd" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                    </div>

                    <!-- FILA 5: TECLADO + MOUSE -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 pb-4 border-b border-slate-800/60">
                        <div>
                            <label class="block text-[11px] font-mono font-bold text-emerald-400 mb-1.5 uppercase" for="select-teclado">10. Teclado Gamer / Oficina</label>
                            <select id="select-teclado" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                        <div>
                            <label class="block text-[11px] font-mono font-bold text-blue-400 mb-1.5 uppercase" for="select-mouse">11. Mouse & Mousepad</label>
                            <select id="select-mouse" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                    </div>

                    <!-- FILA 6: MONITOR + SOFTWARE & SISTEMA OPERATIVO -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6 pb-4 border-b border-slate-800/60">
                        <div>
                            <label class="block text-[11px] font-mono font-bold text-purple-400 mb-1.5 uppercase" for="select-monitor">12. Monitor</label>
                            <select id="select-monitor" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                        <div>
                            <label class="block text-[11px] font-mono font-bold text-pink-400 mb-1.5 uppercase" for="select-software">13. Sistema Operativo & Software</label>
                            <select id="select-software" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                    </div>

                    <!-- SLIDER INTERACTIVO DE PRESUPUESTO ($0 A $250,000 MXN) -->
                    <div class="p-4 sm:p-5 bg-slate-900/80 border border-slate-800 rounded-2xl flex flex-col gap-3">
                        <div class="flex justify-between items-center text-xs">
                            <span class="font-mono text-slate-400 uppercase font-bold">Simular Presupuesto Disponible:</span>
                            <span id="cotizador-slider-val" class="font-mono font-black text-cyan-400 text-sm">$7,500 MXN</span>
                        </div>
                        <input type="range" id="cotizador-slider" min="0" max="250000" step="500" value="7500" oninput="onCotizadorSliderInput(this.value)" class="w-full accent-cyan-400 cursor-pointer" />
                        <div class="flex justify-between text-[10px] font-mono text-slate-500">
                            <span>$0 MXN</span>
                            <span>$50k MXN</span>
                            <span>$125k MXN</span>
                            <span>$250k MXN</span>
                        </div>

                        <!-- PANEL DE COSTO TOTAL / ALERTA EN ROJO -->
                        <div id="panel-presupuesto-box" class="mt-2 p-4 rounded-xl border bg-slate-950 flex flex-col sm:flex-row justify-between items-center gap-4 transition-all">
                            <div>
                                <span class="text-[10px] font-mono text-slate-400 uppercase block">Costo de Configuración Actual:</span>
                                <div class="text-2xl sm:text-3xl font-black font-mono tracking-tight" id="cotizador-total-txt">$7,500.00 MXN</div>
                            </div>
                            <div class="flex gap-2.5 w-full sm:w-auto">
                                <button type="button" onclick="ejecutarPagoSeguroCotizador()" class="flex-1 sm:flex-none bg-amber-500 hover:bg-amber-400 text-slate-950 font-black px-4 py-2.5 rounded-xl text-xs uppercase tracking-wider transition active:scale-95 flex items-center justify-center gap-1.5 shadow-md">
                                    <i class="fa-solid fa-cart-shopping"></i> Comprar
                                </button>
                                <button type="button" onclick="enviarPresupuestoWhatsAppCotizador()" class="flex-1 sm:flex-none bg-emerald-600 hover:bg-emerald-500 text-white font-black px-4 py-2.5 rounded-xl text-xs uppercase tracking-wider transition active:scale-95 flex items-center justify-center gap-1.5 shadow-md">
                                    <i class="fa-brands fa-whatsapp"></i> WhatsApp
                                </button>
                            </div>
                        </div>

                        <!-- ALERTA DINÁMICA DE PRESUPUESTO INSUFICIENTE -->
                        <div id="alert-presupuesto-insuficiente" class="hidden p-3 rounded-xl bg-red-950/40 border border-red-500/40 text-red-300 text-xs font-medium">
                            <i class="fa-solid fa-triangle-exclamation mr-1.5 text-red-400"></i> Presupuesto insuficiente para un ensamble completo. Ajusta el slider a mínimo ~$6,500 MXN o cotiza refacciones individuales en la pirámide izquierda.
                        </div>
                    </div>

                </form>
            </div>

        </div>
    </div>
</section>
"""

JS_LOGICA_COTIZADOR_DEFINITIVO = """
// ========================================================================
// CONFIGURADOR MODULAR (6 PARES + PIRÁMIDE CON PRECIOS + SLIDER 0-250K)
// ========================================================================
const HARDWARE_CATALOG = {
    "5": {
        gabinete: [{ text: "Gabinete Micro-ATX Slim con Fuente 400W", price: 950 }],
        psu: [{ text: "Fuente Genérica 450W Certificada", price: 650 }],
        cpu: [
            { text: "Intel Core i3-14100 (4C/8T hasta 4.7GHz)", price: 3200 },
            { text: "AMD Ryzen 3 4100 / Ryzen 5 4600G (6C/12T)", price: 2900 }
        ],
        cooling: [{ text: "Disipador Stock de Fábrica (Silencioso)", price: 0 }],
        mobo: [{ text: "Tarjeta Madre H610M / A520M Austera", price: 1600 }],
        gpu: [{ text: "Gráficos Integrados Intel UHD / AMD Radeon Vega", price: 0 }],
        ram: [{ text: "8GB RAM DDR4 3200MHz Kingston Fury", price: 550 }, { text: "16GB RAM DDR4 (2x8GB) Dual Channel", price: 950 }],
        ssd: [{ text: "SSD 500GB NVMe M.2 Kingston NV2 (3500 MB/s)", price: 850 }],
        teclado: [{ text: "Teclado Multimedia USB Oficina", price: 250 }],
        mouse: [{ text: "Mouse Óptico Ergonómico 1200 DPI", price: 150 }],
        monitor: [{ text: "Sin Monitor (Solo Torre)", price: 0 }, { text: "Monitor 22\\" Full HD 75Hz", price: 1800 }],
        software: [
            { text: "Sin Sistema Operativo (Equipo sin SO)", price: 0 },
            { text: "Linux Ubuntu LTS 64-bit (Instalación Libre)", price: 0 },
            { text: "Windows 11 Home 64-bit Licencia Oficial", price: 2200 },
            { text: "Windows 11 Pro 64-bit Licencia Oficial", price: 3100 },
            { text: "Windows 11 Pro + Licencia Microsoft Office 2026", price: 4600 }
        ]
    },
    "4": {
        gabinete: [{ text: "Gabinete Mid-Tower Mesh con 3 Ventiladores ARGB", price: 1800 }],
        psu: [{ text: "Fuente Corsair CV550 550W 80+ Bronze", price: 1400 }],
        cpu: [
            { text: "Intel Core i5-14400F (10C/16T hasta 4.7GHz)", price: 5800 },
            { text: "AMD Ryzen 5 7600X AM5 (6C/12T hasta 5.3GHz)", price: 6200 }
        ],
        cooling: [{ text: "Disipador de Torre Cooler Master Hyper 212", price: 800 }],
        mobo: [{ text: "Tarjeta Madre B760M DDR5 / B650M AM5", price: 3400 }],
        gpu: [{ text: "Tarjeta Nvidia RTX 4060 8GB GDDR6", price: 8500 }, { text: "Tarjeta AMD Radeon RX 7600 8GB GDDR6", price: 6800 }],
        ram: [{ text: "16GB RAM DDR5 5600MHz (2x8GB) Corsair", price: 1800 }],
        ssd: [{ text: "SSD 1TB NVMe PCIe 4.0 WD Black SN770", price: 1800 }],
        teclado: [{ text: "Teclado Mecánico RGB Switches Red", price: 950 }],
        mouse: [{ text: "Mouse Gamer 6400 DPI Óptico", price: 450 }],
        monitor: [{ text: "Sin Monitor", price: 0 }, { text: "Monitor 24\\" IPS 144Hz 1ms FreeSync", price: 3500 }],
        software: [
            { text: "Sin Sistema Operativo (Equipo sin SO)", price: 0 },
            { text: "Linux Ubuntu LTS 64-bit", price: 0 },
            { text: "Windows 11 Home 64-bit Licencia Oficial", price: 2200 },
            { text: "Windows 11 Pro 64-bit Licencia Oficial", price: 3100 },
            { text: "Windows 11 Pro + Licencia Microsoft Office 2026", price: 4600 }
        ]
    },
    "3": {
        gabinete: [{ text: "Gabinete NZXT H5 Flow / Corsair 4000D Airflow", price: 2400 }],
        psu: [{ text: "Fuente Corsair RM750e 750W 80+ Gold ATX 3.0", price: 2400 }],
        cpu: [
            { text: "Intel Core i7-14700K (20C/28T hasta 5.6GHz)", price: 12000 },
            { text: "AMD Ryzen 7 7800X3D (8C/16T con 96MB 3D V-Cache)", price: 12000 }
        ],
        cooling: [{ text: "Enfriamiento Líquido AIO 240mm ARGB", price: 2200 }],
        mobo: [{ text: "Tarjeta Madre ASUS TUF Z790 / B650-Plus WiFi", price: 5800 }],
        gpu: [{ text: "Tarjeta Nvidia RTX 4070 Super 12GB GDDR6X", price: 21000 }, { text: "Tarjeta AMD Radeon RX 7800 XT 16GB Nitro+", price: 17000 }],
        ram: [{ text: "32GB RAM DDR5 6000MHz (2x16GB) Corsair Vengeance", price: 3800 }],
        ssd: [{ text: "SSD 1TB Samsung 990 PRO PCIe 4.0 (7450 MB/s)", price: 2800 }],
        teclado: [{ text: "Teclado Mecánico TKL RGB Corsair K70", price: 2200 }],
        mouse: [{ text: "Mouse Inalámbrico Logitech G Pro Ultraligero", price: 2200 }],
        monitor: [{ text: "Sin Monitor", price: 0 }, { text: "Monitor 27\\" QHD 2K 165Hz IPS", price: 6500 }],
        software: [
            { text: "Sin Sistema Operativo (Equipo sin SO)", price: 0 },
            { text: "Linux Ubuntu LTS 64-bit", price: 0 },
            { text: "Windows 11 Pro 64-bit Licencia Oficial", price: 3100 },
            { text: "Windows 11 Pro + Licencia Microsoft Office 2026", price: 4600 }
        ]
    },
    "2": {
        gabinete: [{ text: "Gabinete Lian Li O11 Dynamic EVO / Corsair 5000D", price: 4200 }],
        psu: [{ text: "Fuente Corsair RM1000x 1000W 80+ Gold ATX 3.0", price: 4200 }],
        cpu: [
            { text: "Intel Core i9-14900K / Core Ultra 7 265K (IA Ready)", price: 17500 },
            { text: "AMD Ryzen 9 7950X / Ryzen 9 9900X AM5", price: 16500 }
        ],
        cooling: [{ text: "Enfriamiento Líquido AIO 360mm con Pantalla LCD", price: 4500 }],
        mobo: [{ text: "Tarjeta Madre ROG Strix Z790 / X670E Aorus Master", price: 12000 }],
        gpu: [{ text: "Tarjeta Nvidia RTX 4080 Super 16GB GDDR6X", price: 35000 }, { text: "Tarjeta Nvidia RTX 5080 16GB GDDR7 (Blackwell)", price: 38000 }],
        ram: [{ text: "64GB RAM DDR5 6400MHz (2x32GB) Trident Z5", price: 7500 }],
        ssd: [{ text: "SSD 2TB Samsung 990 PRO PCIe 4.0 + HDD 2TB", price: 6500 }],
        teclado: [{ text: "Teclado Mecánico Custom Gasket Mount QMK/VIA", price: 3500 }],
        mouse: [{ text: "Mouse Logitech G502 X Plus Wireless Lightspeed", price: 2800 }],
        monitor: [{ text: "Sin Monitor", price: 0 }, { text: "Monitor 27\\" OLED 240Hz 0.03ms QHD", price: 18000 }],
        software: [
            { text: "Sin Sistema Operativo (Equipo sin SO)", price: 0 },
            { text: "Windows 11 Pro 64-bit Licencia Oficial", price: 3100 },
            { text: "Windows 11 Pro Workstation + Licencia Office 2026", price: 4600 }
        ]
    },
    "1": {
        gabinete: [{ text: "Gabinete HYTE Y70 Touch con Pantalla Táctil IPS 14\\"", price: 8500 }],
        psu: [{ text: "Fuente Seasonic Prime TX-1300 Titanium ATX 3.1", price: 9500 }],
        cpu: [
            { text: "Intel Core Ultra 9 285K (Arrow Lake Flagship IA NPU)", price: 18500 },
            { text: "AMD Ryzen 9 9950X (16C/32T 5.7GHz Zen 5 Flagship)", price: 18500 }
        ],
        cooling: [{ text: "Enfriamiento Líquido ROG Ryujin III 360 con LCD 3.5\\"", price: 6000 }],
        mobo: [{ text: "Tarjeta Madre ROG Maximus Z890 Extreme / X870E Taichi", price: 18000 }],
        gpu: [{ text: "Tarjeta Nvidia RTX 5090 32GB GDDR7 (Topping Extreme 2026)", price: 65000 }],
        ram: [{ text: "128GB RAM DDR5 8000MHz+ XMP/EXPO (4x32GB)", price: 14000 }],
        ssd: [{ text: "SSD 4TB Crucial T700 PCIe 5.0 Extreme (12,400 MB/s)", price: 14500 }],
        teclado: [{ text: "Teclado Razer Huntsman V3 Pro Rapid Trigger", price: 4800 }],
        mouse: [{ text: "Mouse Logitech G Pro X Superlight 2 Wireless 32K", price: 3200 }],
        monitor: [{ text: "Sin Monitor", price: 0 }, { text: "Monitor 32\\" 4K Mini-LED 144Hz HDR 1400", price: 28000 }],
        software: [
            { text: "Windows 11 Pro Workstation Licencia Oficial", price: 3500 },
            { text: "Windows 11 Pro + Licencia Permanente Office 2026", price: 4600 }
        ]
    }
};

const COMPONENT_MAP = {
    'select-ram': 'pyr-price-ram',
    'select-mouse': 'pyr-price-mouse',
    'select-psu': 'pyr-price-psu',
    'select-monitor': 'pyr-price-monitor',
    'select-teclado': 'pyr-price-teclado',
    'select-gabinete': 'pyr-price-gabinete',
    'select-cpu': 'pyr-price-cpu',
    'select-ssd': 'pyr-price-ssd',
    'select-gpu': 'pyr-price-gpu',
    'select-mobo': 'pyr-price-mobo',
    'select-cooling': 'pyr-price-cooling',
    'select-software': 'pyr-price-software'
};

function actualizarPrefiltroNivel() {
    const selectNivel = document.getElementById('select-nivel-filtro');
    if (!selectNivel) return;
    const lvl = selectNivel.value;
    const cfg = HARDWARE_CATALOG[lvl] || HARDWARE_CATALOG["5"];

    function poblarSelect(elemId, items) {
        const sel = document.getElementById(elemId);
        if (!sel) return;
        sel.innerHTML = '';
        items.forEach(it => {
            const opt = document.createElement('option');
            opt.value = it.price;
            opt.text = `${it.text} (+$${it.price.toLocaleString('es-MX')} MXN)`;
            sel.appendChild(opt);
        });
    }

    poblarSelect('select-gabinete', cfg.gabinete);
    poblarSelect('select-psu', cfg.psu);
    poblarSelect('select-cpu', cfg.cpu);
    poblarSelect('select-cooling', cfg.cooling);
    poblarSelect('select-mobo', cfg.mobo);
    poblarSelect('select-gpu', cfg.gpu);
    poblarSelect('select-ram', cfg.ram);
    poblarSelect('select-ssd', cfg.ssd);
    poblarSelect('select-teclado', cfg.teclado);
    poblarSelect('select-mouse', cfg.mouse);
    poblarSelect('select-monitor', cfg.monitor);
    poblarSelect('select-software', cfg.software);

    recalcularCotizador();
}

function recalcularCotizador() {
    let total = 0;
    
    for (const [selectId, pyrPriceId] of Object.entries(COMPONENT_MAP)) {
        const sel = document.getElementById(selectId);
        const pyrEl = document.getElementById(pyrPriceId);
        const price = sel ? (parseFloat(sel.value) || 0) : 0;
        total += price;
        if (pyrEl) {
            pyrEl.innerText = price === 0 ? '$0 MXN' : `$${price.toLocaleString('es-MX')} MXN`;
        }
    }

    const txtTotal = document.getElementById('cotizador-total-txt');
    const slider = document.getElementById('cotizador-slider');
    const sliderVal = document.getElementById('cotizador-slider-val');
    const panelBox = document.getElementById('panel-presupuesto-box');
    const alertBox = document.getElementById('alert-presupuesto-insuficiente');
    const statusBadge = document.getElementById('status-hardware-badge');

    if (txtTotal) txtTotal.innerText = `$${total.toLocaleString('es-MX', { minimumFractionDigits: 2 })} MXN`;
    if (slider) slider.value = Math.min(250000, total);
    if (sliderVal) sliderVal.innerText = `$${Math.round(total).toLocaleString('es-MX')} MXN`;

    // Validación de presupuesto crítico (< $6,500 MXN)
    if (total < 6500) {
        if (panelBox) {
            panelBox.className = "mt-2 p-4 rounded-xl border border-red-500 bg-red-950/20 text-red-400 flex flex-col sm:flex-row justify-between items-center gap-4 transition-all";
        }
        if (alertBox) alertBox.classList.remove('hidden');
    } else {
        if (panelBox) {
            panelBox.className = "mt-2 p-4 rounded-xl border border-slate-800 bg-slate-950 text-white flex flex-col sm:flex-row justify-between items-center gap-4 transition-all";
        }
        if (alertBox) alertBox.classList.add('hidden');
    }

    // Semáforo de "Computadora Completa"
    const hasCore = (parseFloat(document.getElementById('select-cpu')?.value) || 0) > 0 &&
                    (parseFloat(document.getElementById('select-mobo')?.value) || 0) > 0 &&
                    (parseFloat(document.getElementById('select-ram')?.value) || 0) > 0 &&
                    (parseFloat(document.getElementById('select-ssd')?.value) || 0) > 0 &&
                    (parseFloat(document.getElementById('select-psu')?.value) || 0) > 0;

    if (statusBadge) {
        if (hasCore) {
            statusBadge.className = "p-3 rounded-xl border border-emerald-500/40 bg-emerald-950/30 text-emerald-300 text-xs font-bold transition flex items-start gap-2.5";
            statusBadge.innerHTML = `<i class="fa-solid fa-circle-check text-base text-emerald-400 shrink-0 mt-0.5"></i>
                <div>
                    <span class="block font-black uppercase text-white">✅ COMPUTADORA COMPLETA Y FUNCIONAL</span>
                    <span class="text-[11px] font-normal text-slate-300">Tu ensamble cuenta con el hardware básico necesario para encender y operar. ¿Deseas agregar tarjeta de video dedicada o software adicional?</span>
                </div>`;
        } else {
            statusBadge.className = "p-3 rounded-xl border border-amber-500/40 bg-amber-950/30 text-amber-300 text-xs font-bold transition flex items-start gap-2.5";
            statusBadge.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-base text-amber-400 shrink-0 mt-0.5"></i>
                <div>
                    <span class="block font-black uppercase text-amber-200">⚠️ Ensamble Parcial / Incompleto</span>
                    <span class="text-[11px] font-normal text-slate-300">Selecciona componentes clave (CPU, Placa, RAM, SSD, Fuente) para completar una estación de trabajo funcional.</span>
                </div>`;
        }
    }
}

function onCotizadorSliderInput(val) {
    const sliderVal = document.getElementById('cotizador-slider-val');
    if (sliderVal) sliderVal.innerText = `$${parseFloat(val).toLocaleString('es-MX')} MXN`;
    
    const num = parseFloat(val);
    const selLvl = document.getElementById('select-nivel-filtro');
    if (selLvl) {
        let nuevoLvl = "5";
        if (num >= 130000) nuevoLvl = "1";
        else if (num >= 65000) nuevoLvl = "2";
        else if (num >= 30000) nuevoLvl = "3";
        else if (num >= 14000) nuevoLvl = "4";
        
        if (selLvl.value !== nuevoLvl) {
            selLvl.value = nuevoLvl;
            actualizarPrefiltroNivel();
        }
    }
}

function focusComponent(selectId) {
    const sel = document.getElementById(selectId);
    if (sel) {
        sel.scrollIntoView({ behavior: 'smooth', block: 'center' });
        sel.classList.add('ring-2', 'ring-cyan-400');
        setTimeout(() => sel.classList.remove('ring-2', 'ring-cyan-400'), 1500);
    }
}

window.abrirCotizadorConNivel = function(lvl) {
    const selLvl = document.getElementById('select-nivel-filtro');
    if (selLvl) {
        selLvl.value = lvl.toString();
        actualizarPrefiltroNivel();
    }
    const cotSec = document.getElementById('cotizador');
    if (cotSec) {
        cotSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
};

window.ejecutarPagoSeguroCotizador = function() {
    const lvlText = document.getElementById('select-nivel-filtro')?.selectedOptions[0]?.text || 'Ensamble a Medida';
    const total = document.getElementById('cotizador-total-txt')?.innerText || '$0.00 MXN';
    
    try {
        let cart = JSON.parse(localStorage.getItem('ecosystem_global_cart') || '[]');
        cart.push({
            sku: 'PC-CUSTOM-' + Date.now().toString().slice(-4),
            nombre: `Ensamble Personalizado (${lvlText.split('—')[0].trim()})`,
            precio: parseFloat(total.replace(/[^0-9.]/g, '')) || 7500,
            imagen: 'https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp',
            quantity: 1
        });
        localStorage.setItem('ecosystem_global_cart', JSON.stringify(cart));
        window.dispatchEvent(new Event('storage'));
        window.location.href = 'checkout.html';
    } catch(e) {
        window.location.href = 'checkout.html';
    }
};

window.enviarPresupuestoWhatsAppCotizador = function() {
    const getSel = id => document.getElementById(id)?.selectedOptions[0]?.text || 'N/A';
    const lvl = getSel('select-nivel-filtro');
    const cpu = getSel('select-cpu');
    const gpu = getSel('select-gpu');
    const ram = getSel('select-ram');
    const ssd = getSel('select-ssd');
    const software = getSel('select-software');
    const total = document.getElementById('cotizador-total-txt')?.innerText || '$0.00 MXN';

    const msg = `Hola PC Custom Lab, coticé el siguiente ensamble en su configurador:%0A- Nivel: ${lvl}%0A- CPU: ${cpu}%0A- GPU: ${gpu}%0A- RAM: ${ram}%0A- Almacenamiento: ${ssd}%0A- Sistema Operativo: ${software}%0A- Total Estimado: ${total}`;
    window.open(`https://wa.me/523337271440?text=${msg}`, '_blank');
};
"""

def update_pc_custom_lab():
    print("=" * 75)
    print("APLICANDO COTIZADOR PIRAMIDAL INTERACTIVO EN PC CUSTOM LAB")
    print("=" * 75)

    if not os.path.exists(PC_INDEX_PATH):
        print(f"[Error] No se encontró el archivo {PC_INDEX_PATH}")
        return

    with open(PC_INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Reemplazar la sección #cotizador
    content = re.sub(r'<section[^>]*id=["\']cotizador["\'][\s\S]*?<\/section>', COTIZADOR_SECTION_HTML, content, flags=re.IGNORECASE)

    # 2. Inyectar o actualizar lógica JavaScript
    if "HARDWARE_CATALOG" not in content:
        content = content.replace("</script>", f"{JS_LOGICA_COTIZADOR_DEFINITIVO}\n</script>")
    else:
        content = re.sub(r'\/\/ =+\s*CONFIGURADOR MODULAR[\s\S]*?enviarPresupuestoWhatsAppCotizador[\s\S]*?};', JS_LOGICA_COTIZADOR_DEFINITIVO, content)

    with open(PC_INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("✓ pc-custom-lab/index.html actualizado.")

def deploy_to_git():
    print("\n" + "=" * 75)
    print("SINCRONIZACIÓN CON GITHUB PAGES (-C GC.AUTO=0)")
    print("=" * 75)
    pc_dir = os.path.join(BASE_DIR, "pc-custom-lab")
    subprocess.run(["git", "add", "-A"], cwd=pc_dir, check=True)
    subprocess.run(["git", "commit", "-m", "feat(cotizador): piramide de componentes, selector de software y alerta de presupuesto", "--allow-empty"], cwd=pc_dir, capture_output=True)
    res_pc = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=pc_dir, capture_output=True, text=True)
    print(f"🟢 pc-custom-lab -> Push: {'OK' if res_pc.returncode == 0 else res_pc.stderr.strip()}")

    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(pc-custom-lab): modulo de cotizador interactivo con piramide y validacion", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
    res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
    print(f"🟢 Monorepositorio Raíz -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    update_pc_custom_lab()
    deploy_to_git()
