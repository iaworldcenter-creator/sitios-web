import os
import re
import subprocess

BASE_DIR = r"E:\sitios web"
PC_INDEX_PATH = os.path.join(BASE_DIR, "pc-custom-lab", "index.html")

NIVELES_SECTION_HTML = """<!-- NIVELES DE EQUIPOS (SINCRONIZADOS DE i3 A ULTRA 9) -->
<section class="py-20 bg-slate-950 border-t border-slate-900 relative overflow-hidden" id="niveles">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 relative z-10">
        <div class="text-center mb-16">
            <span class="px-4 py-1.5 rounded-full bg-teal-500/10 border border-teal-500/30 text-teal-400 font-mono text-xs uppercase tracking-widest inline-block mb-4">Laboratorio de Ensamblaje</span>
            <h2 class="text-3xl sm:text-5xl font-black text-white tracking-tight mb-4">Nuestros Niveles de Ensamble</h2>
            <p class="text-slate-400 text-sm sm:text-base max-w-2xl mx-auto">Desde estaciones básicas de trabajo y oficina hasta servidores dedicados a Inteligencia Artificial.</p>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            
            <div class="lg:col-span-6 relative rounded-3xl overflow-hidden border border-teal-500/30 shadow-2xl shadow-teal-950/20 bg-slate-900/40 p-1 flex items-center justify-center min-h-[300px] sm:min-h-[450px]">
                <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/20 to-slate-950/40 z-10"></div>
                <div class="w-full h-full object-cover rounded-2xl absolute inset-0 overflow-hidden" id="video-container-1">
                    <img src="assets/img/Female_technician_assembling_gam_202608041518_thumb.webp?v=1.1.0" alt="Ensamble de Computadora" class="w-full h-full object-cover" loading="lazy" width="300" height="168" />
                </div>
                <div class="absolute bottom-6 left-6 right-6 bg-slate-950/80 backdrop-blur-md border border-teal-500/30 p-4 rounded-xl flex items-center gap-3 z-20">
                    <div class="w-2.5 h-2.5 rounded-full bg-teal-400 animate-ping shrink-0"></div>
                    <span class="text-[11px] text-teal-300 font-mono uppercase tracking-wider">Ensamble de Precisión: Control de Calidad en Pedro Moreno 501 A</span>
                </div>
            </div>

            <div class="lg:col-span-6 flex flex-col gap-3.5">
                <!-- Nivel 5 -->
                <button type="button" onclick="abrirCotizadorConNivel(5)" class="w-full text-left bg-slate-900/50 hover:bg-slate-900 border border-slate-800 hover:border-amber-500/60 transition duration-200 p-4 rounded-2xl group flex items-start gap-4 cursor-pointer">
                    <div class="w-9 h-9 rounded-xl bg-slate-800 group-hover:bg-amber-500 group-hover:text-slate-950 flex items-center justify-center text-slate-400 border border-slate-700 transition shrink-0 font-mono font-black text-sm">5</div>
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <h4 class="font-bold text-white text-sm group-hover:text-amber-400 transition">PC Básica Hogar &amp; Oficina</h4>
                            <span class="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-400 font-mono">Nivel 5</span>
                        </div>
                        <p class="text-xs text-slate-400 leading-relaxed">Intel Core i3 / AMD Ryzen 3, 8GB/16GB RAM, SSD NVMe, Gabinete Slim con Fuente económica. Ideal para trabajo y oficina.</p>
                    </div>
                </button>

                <!-- Nivel 4 -->
                <button type="button" onclick="abrirCotizadorConNivel(4)" class="w-full text-left bg-slate-900/50 hover:bg-slate-900 border border-slate-800 hover:border-blue-500/60 transition duration-200 p-4 rounded-2xl group flex items-start gap-4 cursor-pointer">
                    <div class="w-9 h-9 rounded-xl bg-slate-800 group-hover:bg-blue-500 group-hover:text-white flex items-center justify-center text-slate-400 border border-slate-700 transition shrink-0 font-mono font-black text-sm">4</div>
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <h4 class="font-bold text-white text-sm group-hover:text-blue-400 transition">PC Completa Gama Media / Estudiantes</h4>
                            <span class="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-400 font-mono">Nivel 4</span>
                        </div>
                        <p class="text-xs text-slate-400 leading-relaxed">Intel Core i5 / AMD Ryzen 5, 16GB RAM, SSD 1TB, GPU dedicada 8GB. Excelente multitarea y productividad ágil.</p>
                    </div>
                </button>

                <!-- Nivel 3 -->
                <button type="button" onclick="abrirCotizadorConNivel(3)" class="w-full text-left bg-slate-900/50 hover:bg-slate-900 border border-slate-800 hover:border-purple-500/60 transition duration-200 p-4 rounded-2xl group flex items-start gap-4 cursor-pointer">
                    <div class="w-9 h-9 rounded-xl bg-slate-800 group-hover:bg-purple-500 group-hover:text-white flex items-center justify-center text-slate-400 border border-slate-700 transition shrink-0 font-mono font-black text-sm">3</div>
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <h4 class="font-bold text-white text-sm group-hover:text-purple-400 transition">Gama Alta / Render &amp; Oficina Pro</h4>
                            <span class="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-400 font-mono">Nivel 3</span>
                        </div>
                        <p class="text-xs text-slate-400 leading-relaxed">Intel Core i7 / AMD Ryzen 7, 32GB RAM DDR5, AIO 240mm, GPU RTX 4070 / RX 7800 XT. Creadores y modelado 3D.</p>
                    </div>
                </button>

                <!-- Nivel 2 -->
                <button type="button" onclick="abrirCotizadorConNivel(2)" class="w-full text-left bg-slate-900/50 hover:bg-slate-900 border border-slate-800 hover:border-cyan-500/60 transition duration-200 p-4 rounded-2xl group flex items-start gap-4 cursor-pointer">
                    <div class="w-9 h-9 rounded-xl bg-slate-800 group-hover:bg-cyan-500 group-hover:text-slate-950 flex items-center justify-center text-slate-400 border border-slate-700 transition shrink-0 font-mono font-black text-sm">2</div>
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <h4 class="font-bold text-white text-sm group-hover:text-cyan-400 transition">Categoría Entusiasta / IA &amp; Streaming</h4>
                            <span class="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-400 font-mono">Nivel 2</span>
                        </div>
                        <p class="text-xs text-slate-400 leading-relaxed">Intel Core i9 / Core Ultra 7 / AMD Ryzen 9, 64GB RAM DDR5, SSD 2TB PCIe 4.0, RTX 4080 Super / RTX 5080.</p>
                    </div>
                </button>

                <!-- Nivel 1 -->
                <button type="button" onclick="abrirCotizadorConNivel(1)" class="w-full text-left bg-slate-900/50 hover:bg-slate-900 border border-teal-500/30 hover:border-teal-400 transition duration-200 p-4 rounded-2xl group flex items-start gap-4 cursor-pointer">
                    <div class="w-9 h-9 rounded-xl bg-teal-500/20 group-hover:bg-teal-400 group-hover:text-slate-950 flex items-center justify-center text-teal-400 border border-teal-500/40 transition shrink-0 font-mono font-black text-sm">1</div>
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <h4 class="font-bold text-teal-300 text-sm group-hover:text-teal-200 transition">Topping Extreme / Flagship 2026</h4>
                            <span class="px-2 py-0.5 rounded bg-teal-500/20 text-[10px] text-teal-300 font-mono">Nivel 1</span>
                        </div>
                        <p class="text-xs text-slate-300 leading-relaxed font-mono">Intel Core Ultra 9 285K / AMD Ryzen 9 9950X, 128GB RAM DDR5 8000MHz, SSD 4TB PCIe 5.0, RTX 5090 32GB GDDR7.</p>
                    </div>
                </button>
            </div>

        </div>
    </div>
</section>
"""

COTIZADOR_HTML = """<!-- COTIZADOR MATRIZ INTERACTIVO: PIRÁMIDE VISUAL + MATRIZ DE PARES + SLIDER -->
<section class="py-20 bg-slate-900/90 border-y border-slate-800" id="cotizador">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div class="text-center mb-12">
            <span class="px-3.5 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 font-mono text-xs uppercase tracking-widest inline-block mb-3">
                Configurador Modular Interactivo 2026
            </span>
            <h2 class="text-3xl sm:text-4xl font-black text-white">Configura tu Equipo Paso a Paso</h2>
            <p class="text-slate-400 text-sm mt-2 max-w-2xl mx-auto">Selecciona tu nivel base, personaliza tus piezas o haz clic en cualquier componente para explorar opciones en la boutique.</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            
            <!-- COLUMNA IZQUIERDA: PIRÁMIDE VISUAL CON PRECIOS Y ENLACES DIRECTOS A BOUTIQUE -->
            <div class="lg:col-span-5 bg-slate-950 border border-slate-800 rounded-3xl p-5 sm:p-6 shadow-2xl flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
                        <h3 class="text-xs font-mono font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-2">
                            <i class="fa-solid fa-layer-group"></i> Resumen de Ensamble
                        </h3>
                        <span class="text-[10px] font-mono text-slate-500"><i class="fa-solid fa-arrow-up-right-from-square"></i> Clic: Ver en Boutique</span>
                    </div>

                    <!-- LISTA ESCALONADA PIRAMIDAL CON PRECIOS A LA DERECHA -->
                    <div class="flex flex-col gap-1.5" id="pyramid-list">
                        <button type="button" onclick="goToBoutiqueCategory('ram')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-memory text-[11px] text-cyan-400"></i> 1. Memoria RAM</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-ram">$0 MXN</span>
                        </button>
                        <button type="button" onclick="goToBoutiqueCategory('perifericos')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-computer-mouse text-[11px] text-blue-400"></i> 2. Mouse & Mousepad</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-mouse">$0 MXN</span>
                        </button>
                        <button type="button" onclick="goToBoutiqueCategory('fuentes')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-plug text-[11px] text-emerald-400"></i> 3. Fuente de Poder</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-psu">$0 MXN</span>
                        </button>
                        <button type="button" onclick="goToBoutiqueCategory('monitores')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-tv text-[11px] text-purple-400"></i> 4. Monitor</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-monitor">$0 MXN</span>
                        </button>
                        <button type="button" onclick="goToBoutiqueCategory('perifericos')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-keyboard text-[11px] text-emerald-400"></i> 5. Teclado Gamer / Oficina</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-teclado">$0 MXN</span>
                        </button>
                        <button type="button" onclick="goToBoutiqueCategory('gabinetes')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-box text-[11px] text-blue-400"></i> 6. Gabinete (Chasis)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-gabinete">$0 MXN</span>
                        </button>
                        <button type="button" onclick="goToBoutiqueCategory('procesadores')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-microchip text-[11px] text-pink-400"></i> 7. Procesador (Intel / AMD)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-cpu">$0 MXN</span>
                        </button>
                        <button type="button" onclick="goToBoutiqueCategory('almacenamiento')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-hard-drive text-[11px] text-amber-400"></i> 8. Almacenamiento (SSD / HDD)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-ssd">$0 MXN</span>
                        </button>
                        <button type="button" onclick="goToBoutiqueCategory('gpu')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-vr-cardboard text-[11px] text-indigo-400"></i> 9. Tarjeta de Video (GPU)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-gpu">$0 MXN</span>
                        </button>
                        <button type="button" onclick="goToBoutiqueCategory('motherboards')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-chess-board text-[11px] text-purple-400"></i> 10. Tarjeta Madre (Motherboard)</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-mobo">$0 MXN</span>
                        </button>
                        <button type="button" onclick="goToBoutiqueCategory('enfriamiento')" class="w-full flex justify-between items-center bg-slate-900/60 hover:bg-cyan-950/40 border border-slate-800/80 hover:border-cyan-500/50 rounded-lg px-3 py-1.5 transition text-left group">
                            <span class="text-xs font-semibold text-slate-300 group-hover:text-cyan-300 flex items-center gap-2"><i class="fa-solid fa-fan text-[11px] text-teal-400"></i> 11. Sistema de Enfriamiento</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-cooling">$0 MXN</span>
                        </button>
                        <div class="w-full flex justify-between items-center bg-slate-900/60 border border-slate-800/80 rounded-lg px-3 py-1.5 text-left">
                            <span class="text-xs font-semibold text-slate-300 flex items-center gap-2"><i class="fa-brands fa-windows text-[11px] text-pink-400"></i> 12. Sistema Operativo &amp; Software</span>
                            <span class="text-xs font-mono font-bold text-amber-400" id="pyr-price-software">$0 MXN</span>
                        </div>
                    </div>
                </div>

                <!-- SEMÁFORO DE VALIDACIÓN DE HARDWARE FUNCIONAL -->
                <div class="mt-5 pt-4 border-t border-slate-800 flex flex-col gap-2">
                    <div id="status-hardware-badge" class="p-3 rounded-xl border text-xs font-bold transition flex items-start gap-2.5"></div>
                </div>
            </div>

            <!-- COLUMNA DERECHA: MATRIZ DE 13 CAMPOS + SLIDER REACTIVO -->
            <div class="lg:col-span-7 bg-slate-950 border border-slate-800 rounded-3xl p-5 sm:p-7 shadow-2xl">
                <form id="form-cotizador" onchange="recalcularCotizador()">
                    
                    <!-- 1. SELECTOR MAESTRO DE NIVEL -->
                    <div class="mb-5 pb-4 border-b border-slate-800">
                        <label class="block text-xs font-mono font-bold text-amber-400 mb-1.5 uppercase tracking-wider" for="select-nivel-filtro">
                            1. Selecciona el Nivel Base de Ensamble
                        </label>
                        <select id="select-nivel-filtro" onchange="actualizarPrefiltroNivel()" class="w-full bg-slate-900 border border-amber-500/50 text-amber-200 rounded-xl p-2.5 text-xs sm:text-sm font-bold focus:border-amber-400 focus:outline-none transition cursor-pointer">
                            <option value="5" selected>Nivel 5 — Entrada / Hogar / Oficina (Core i3 / Ryzen 3)</option>
                            <option value="4">Nivel 4 — Gama Media / Estudiantes (Core i5 / Ryzen 5)</option>
                            <option value="3">Nivel 3 — Gama Alta / Render / Oficina Pro (Core i7 / Ryzen 7)</option>
                            <option value="2">Nivel 2 — Categoría Entusiasta / IA (Core i9 / Ultra 7 / Ryzen 9)</option>
                            <option value="1">Nivel 1 — TOPPING EXTREME 2026 (Core Ultra 9 / Ryzen 9 9950X / RTX 5090)</option>
                        </select>
                    </div>

                    <!-- FILA 1: GABINETE + FUENTE -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5 mb-3.5 pb-3.5 border-b border-slate-800/60">
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label class="text-[11px] font-mono font-bold text-blue-400 uppercase" for="select-gabinete">2. Gabinete (Chasis)</label>
                                <button type="button" onclick="goToBoutiqueCategory('gabinetes')" class="text-[9px] font-mono text-slate-500 hover:text-cyan-400">Ver modelos &rarr;</button>
                            </div>
                            <select id="select-gabinete" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label class="text-[11px] font-mono font-bold text-emerald-400 uppercase" for="select-psu">3. Fuente de Poder (PSU)</label>
                                <button type="button" onclick="goToBoutiqueCategory('fuentes')" class="text-[9px] font-mono text-slate-500 hover:text-cyan-400">Ver modelos &rarr;</button>
                            </div>
                            <select id="select-psu" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                    </div>

                    <!-- FILA 2: PROCESADOR + ENFRIAMIENTO -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5 mb-3.5 pb-3.5 border-b border-slate-800/60">
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label class="text-[11px] font-mono font-bold text-pink-400 uppercase" for="select-cpu">4. Procesador (Intel / AMD)</label>
                                <button type="button" onclick="goToBoutiqueCategory('procesadores')" class="text-[9px] font-mono text-slate-500 hover:text-cyan-400">Ver modelos &rarr;</button>
                            </div>
                            <select id="select-cpu" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label class="text-[11px] font-mono font-bold text-teal-400 uppercase" for="select-cooling">5. Sistema de Enfriamiento</label>
                                <button type="button" onclick="goToBoutiqueCategory('enfriamiento')" class="text-[9px] font-mono text-slate-500 hover:text-cyan-400">Ver modelos &rarr;</button>
                            </div>
                            <select id="select-cooling" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                    </div>

                    <!-- FILA 3: TARJETA MADRE + TARJETA DE VIDEO -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5 mb-3.5 pb-3.5 border-b border-slate-800/60">
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label class="text-[11px] font-mono font-bold text-purple-400 uppercase" for="select-mobo">6. Tarjeta Madre</label>
                                <button type="button" onclick="goToBoutiqueCategory('motherboards')" class="text-[9px] font-mono text-slate-500 hover:text-cyan-400">Ver modelos &rarr;</button>
                            </div>
                            <select id="select-mobo" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label class="text-[11px] font-mono font-bold text-indigo-400 uppercase" for="select-gpu">7. Tarjeta de Video (GPU)</label>
                                <button type="button" onclick="goToBoutiqueCategory('gpu')" class="text-[9px] font-mono text-slate-500 hover:text-cyan-400">Ver modelos &rarr;</button>
                            </div>
                            <select id="select-gpu" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                    </div>

                    <!-- FILA 4: MEMORIA RAM + ALMACENAMIENTO -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5 mb-3.5 pb-3.5 border-b border-slate-800/60">
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label class="text-[11px] font-mono font-bold text-cyan-400 uppercase" for="select-ram">8. Memoria RAM</label>
                                <button type="button" onclick="goToBoutiqueCategory('ram')" class="text-[9px] font-mono text-slate-500 hover:text-cyan-400">Ver modelos &rarr;</button>
                            </div>
                            <select id="select-ram" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label class="text-[11px] font-mono font-bold text-amber-400 uppercase" for="select-ssd">9. Almacenamiento (SSD / HDD)</label>
                                <button type="button" onclick="goToBoutiqueCategory('almacenamiento')" class="text-[9px] font-mono text-slate-500 hover:text-cyan-400">Ver modelos &rarr;</button>
                            </div>
                            <select id="select-ssd" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                    </div>

                    <!-- FILA 5: TECLADO + MOUSE -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5 mb-3.5 pb-3.5 border-b border-slate-800/60">
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label class="text-[11px] font-mono font-bold text-emerald-400 uppercase" for="select-teclado">10. Teclado Gamer / Oficina</label>
                                <button type="button" onclick="goToBoutiqueCategory('perifericos')" class="text-[9px] font-mono text-slate-500 hover:text-cyan-400">Ver modelos &rarr;</button>
                            </div>
                            <select id="select-teclado" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label class="text-[11px] font-mono font-bold text-blue-400 uppercase" for="select-mouse">11. Mouse & Mousepad</label>
                                <button type="button" onclick="goToBoutiqueCategory('perifericos')" class="text-[9px] font-mono text-slate-500 hover:text-cyan-400">Ver modelos &rarr;</button>
                            </div>
                            <select id="select-mouse" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                    </div>

                    <!-- FILA 6: MONITOR + SISTEMA OPERATIVO & SOFTWARE -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5 mb-5 pb-3.5 border-b border-slate-800/60">
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label class="text-[11px] font-mono font-bold text-purple-400 uppercase" for="select-monitor">12. Monitor</label>
                                <button type="button" onclick="goToBoutiqueCategory('monitores')" class="text-[9px] font-mono text-slate-500 hover:text-cyan-400">Ver modelos &rarr;</button>
                            </div>
                            <select id="select-monitor" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                        <div>
                            <label class="block text-[11px] font-mono font-bold text-pink-400 mb-1 uppercase" for="select-software">13. Sistema Operativo &amp; Software</label>
                            <select id="select-software" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"></select>
                        </div>
                    </div>

                    <!-- SLIDER INTERACTIVO DE PRESUPUESTO ($0 A $250,000 MXN) -->
                    <div class="p-4 bg-slate-900/80 border border-slate-800 rounded-2xl flex flex-col gap-3">
                        <div class="flex justify-between items-center text-xs">
                            <span class="font-mono text-slate-400 uppercase font-bold">Simular Presupuesto Disponible:</span>
                            <span id="cotizador-slider-val" class="font-mono font-black text-cyan-400 text-sm">$8,200 MXN</span>
                        </div>
                        <input type="range" id="cotizador-slider" min="0" max="250000" step="500" value="8200" oninput="onCotizadorSliderInput(this.value)" class="w-full accent-cyan-400 cursor-pointer" />
                        <div class="flex justify-between text-[10px] font-mono text-slate-500">
                            <span>$0 MXN</span>
                            <span>$50k MXN</span>
                            <span>$125k MXN</span>
                            <span>$250k MXN</span>
                        </div>

                        <!-- PANEL DE COSTO TOTAL / ACCIONES -->
                        <div id="panel-presupuesto-box" class="mt-1 p-3.5 rounded-xl border bg-slate-950 flex flex-col sm:flex-row justify-between items-center gap-3 transition-all">
                            <div>
                                <span class="text-[10px] font-mono text-slate-400 uppercase block">Costo de Configuración Actual:</span>
                                <div class="text-2xl font-black font-mono tracking-tight text-amber-400" id="cotizador-total-txt">$8,200.00 MXN</div>
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
                            <i class="fa-solid fa-triangle-exclamation mr-1.5 text-red-400"></i> Presupuesto insuficiente para un ensamble completo funcional. Ajusta el slider a mínimo ~$6,500 MXN o cotiza refacciones individuales en la pirámide izquierda.
                        </div>
                    </div>

                </form>
            </div>

        </div>
    </div>
</section>
"""

JS_LOGICA_ACTUALIZADA = """
// ========================================================================
// CONFIGURADOR MODULAR Y ENLACES DIRECTOS A LA BOUTIQUE
// ========================================================================
const HARDWARE_CATALOG = {
    "5": {
        gabinete: [{ text: "Gabinete Micro-ATX Slim con Fuente 400W incluida", price: 500 }],
        psu: [{ text: "Fuente Genérica 450W Certificada", price: 350 }],
        cpu: [
            { text: "Intel Core i3-14100 (4C/8T hasta 4.7GHz)", price: 3200 },
            { text: "AMD Ryzen 3 4100 / Ryzen 5 4600G (6C/12T)", price: 2500 }
        ],
        cooling: [{ text: "Disipador Stock Silencioso de Fábrica", price: 0 }],
        mobo: [{ text: "Tarjeta Madre H610M / A520M Austera", price: 1400 }],
        gpu: [{ text: "Gráficos Integrados Intel UHD / AMD Radeon", price: 0 }],
        ram: [{ text: "8GB RAM DDR4 3200MHz Kingston Fury", price: 450 }, { text: "16GB RAM DDR4 (2x8GB) Dual Channel", price: 850 }],
        ssd: [{ text: "SSD 256GB NVMe M.2 de Alta Velocidad", price: 450 }, { text: "SSD 500GB NVMe M.2 Kingston NV2", price: 750 }],
        teclado: [{ text: "Teclado Multimedia USB Oficina", price: 150 }],
        mouse: [{ text: "Mouse Óptico Ergonómico 1200 DPI", price: 100 }],
        monitor: [{ text: "Sin Monitor (Solo Torre)", price: 0 }, { text: "Monitor 22\" Full HD 75Hz", price: 1600 }],
        software: [
            { text: "Windows 11 Home 64-bit Licencia Oficial", price: 2200 },
            { text: "Windows 11 Pro 64-bit Licencia Oficial", price: 2900 },
            { text: "Windows 11 Pro + Suite Office 2026", price: 4200 },
            { text: "Linux Ubuntu LTS 64-bit (Instalación Libre)", price: 0 },
            { text: "Sin Sistema Operativo (Equipo sin SO)", price: 0 }
        ]
    },
    "4": {
        gabinete: [{ text: "Gabinete Mid-Tower Mesh con Fuente 500W", price: 950 }],
        psu: [{ text: "Fuente Corsair CV550 550W 80+ Bronze", price: 1200 }],
        cpu: [
            { text: "Intel Core i5-14400F (10C/16T hasta 4.7GHz)", price: 4800 },
            { text: "AMD Ryzen 5 7600X AM5 (6C/12T hasta 5.3GHz)", price: 5200 }
        ],
        cooling: [{ text: "Disipador de Torre Cooler Master Hyper 212", price: 650 }],
        mobo: [{ text: "Tarjeta Madre B760M DDR5 / B650M AM5", price: 2800 }],
        gpu: [{ text: "Tarjeta Nvidia RTX 4060 8GB GDDR6", price: 7500 }, { text: "Tarjeta AMD Radeon RX 7600 8GB GDDR6", price: 6200 }],
        ram: [{ text: "16GB RAM DDR5 5600MHz (2x8GB) Corsair", price: 1400 }],
        ssd: [{ text: "SSD 1TB NVMe PCIe 4.0 WD Black SN770", price: 1400 }],
        teclado: [{ text: "Teclado Ergonómico Retroiluminado", price: 450 }],
        mouse: [{ text: "Mouse Gamer Óptico 3200 DPI", price: 300 }],
        monitor: [{ text: "Monitor 24\" IPS 144Hz 1ms FreeSync", price: 2900 }, { text: "Sin Monitor", price: 0 }],
        software: [
            { text: "Windows 11 Pro 64-bit Licencia Oficial", price: 2900 },
            { text: "Windows 11 Home 64-bit Licencia Oficial", price: 2200 },
            { text: "Windows 11 Pro + Suite Office 2026", price: 4200 },
            { text: "Linux Ubuntu LTS 64-bit", price: 0 },
            { text: "Sin Sistema Operativo (Equipo sin SO)", price: 0 }
        ]
    },
    "3": {
        gabinete: [{ text: "Gabinete NZXT H5 Flow / Corsair 4000D Airflow", price: 1800 }],
        psu: [{ text: "Fuente Corsair RM750e 750W 80+ Gold ATX 3.0", price: 2200 }],
        cpu: [
            { text: "Intel Core i7-14700K (20C/28T hasta 5.6GHz)", price: 9500 },
            { text: "AMD Ryzen 7 7800X3D (8C/16T con 96MB 3D V-Cache)", price: 9800 }
        ],
        cooling: [{ text: "Enfriamiento Líquido AIO 240mm ARGB", price: 1800 }],
        mobo: [{ text: "Tarjeta Madre ASUS TUF Z790 / B650-Plus WiFi", price: 4500 }],
        gpu: [{ text: "Tarjeta Nvidia RTX 4070 Super 12GB GDDR6X", price: 16500 }, { text: "Tarjeta AMD Radeon RX 7800 XT 16GB Nitro+", price: 14000 }],
        ram: [{ text: "32GB RAM DDR5 6000MHz (2x16GB) Corsair", price: 2800 }],
        ssd: [{ text: "SSD 1TB Samsung 990 PRO PCIe 4.0 (7450 MB/s)", price: 2400 }],
        teclado: [{ text: "Teclado Mecánico TKL RGB Corsair K70", price: 1600 }],
        mouse: [{ text: "Mouse Inalámbrico Logitech G Pro Ultraligero", price: 1400 }],
        monitor: [{ text: "Monitor 27\" QHD 2K 165Hz IPS", price: 5200 }, { text: "Sin Monitor", price: 0 }],
        software: [
            { text: "Windows 11 Pro 64-bit Licencia Oficial", price: 2900 },
            { text: "Windows 11 Pro + Suite Office 2026", price: 4200 },
            { text: "Linux Ubuntu LTS 64-bit", price: 0 },
            { text: "Sin Sistema Operativo (Equipo sin SO)", price: 0 }
        ]
    },
    "2": {
        gabinete: [{ text: "Gabinete Lian Li O11 Dynamic EVO / Corsair 5000D", price: 3800 }],
        psu: [{ text: "Fuente Corsair RM1000x 1000W 80+ Gold ATX 3.0", price: 3800 }],
        cpu: [
            { text: "Intel Core i9-14900K / Core Ultra 7 265K (IA Ready)", price: 15000 },
            { text: "AMD Ryzen 9 9900X / Ryzen 9 7950X AM5", price: 14500 }
        ],
        cooling: [{ text: "Enfriamiento Líquido AIO 360mm con Pantalla LCD", price: 3800 }],
        mobo: [{ text: "Tarjeta Madre ROG Strix Z790 / X670E Aorus Master", price: 9500 }],
        gpu: [{ text: "Tarjeta Nvidia RTX 4080 Super 16GB GDDR6X", price: 28000 }, { text: "Tarjeta Nvidia RTX 5080 16GB GDDR7 (Blackwell)", price: 32000 }],
        ram: [{ text: "64GB RAM DDR5 6400MHz (2x32GB) Trident Z5", price: 5800 }],
        ssd: [{ text: "SSD 2TB Samsung 990 PRO PCIe 4.0 + HDD 2TB", price: 4800 }],
        teclado: [{ text: "Teclado Mecánico Custom Gasket Mount QMK/VIA", price: 2800 }],
        mouse: [{ text: "Mouse Logitech G502 X Plus Wireless Lightspeed", price: 2200 }],
        monitor: [{ text: "Monitor 27\" OLED 240Hz 0.03ms QHD", price: 14000 }, { text: "Sin Monitor", price: 0 }],
        software: [
            { text: "Windows 11 Pro Workstation + Suite Office 2026", price: 4600 },
            { text: "Windows 11 Pro 64-bit Licencia Oficial", price: 2900 },
            { text: "Sin Sistema Operativo (Equipo sin SO)", price: 0 }
        ]
    },
    "1": {
        gabinete: [{ text: "Gabinete HYTE Y70 Touch con Pantalla Táctil IPS 14\"", price: 7500 }],
        psu: [{ text: "Fuente Seasonic Prime TX-1300 Titanium ATX 3.1", price: 8500 }],
        cpu: [
            { text: "Intel Core Ultra 9 285K (Arrow Lake Flagship IA NPU)", price: 18500 },
            { text: "AMD Ryzen 9 9950X (16C/32T 5.7GHz Zen 5 Flagship)", price: 18500 }
        ],
        cooling: [{ text: "Enfriamiento Líquido ROG Ryujin III 360 con LCD 3.5\"", price: 5800 }],
        mobo: [{ text: "Tarjeta Madre ROG Maximus Z890 Extreme / X870E Taichi", price: 16000 }],
        gpu: [{ text: "Tarjeta Nvidia RTX 5090 32GB GDDR7 (Topping Extreme 2026)", price: 55000 }],
        ram: [{ text: "128GB RAM DDR5 8000MHz+ XMP/EXPO (4x32GB)", price: 12000 }],
        ssd: [{ text: "SSD 4TB Crucial T700 PCIe 5.0 Extreme (12,400 MB/s)", price: 12500 }],
        teclado: [{ text: "Teclado Razer Huntsman V3 Pro Rapid Trigger", price: 4200 }],
        mouse: [{ text: "Mouse Logitech G Pro X Superlight 2 Wireless 32K", price: 2800 }],
        monitor: [{ text: "Monitor 32\" 4K Mini-LED 144Hz HDR 1400", price: 22000 }, { text: "Sin Monitor", price: 0 }],
        software: [
            { text: "Windows 11 Pro Workstation + Licencia Permanente Office 2026", price: 4600 },
            { text: "Windows 11 Pro 64-bit Licencia Oficial", price: 2900 }
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

const BOUTIQUE_PAGE_MAP = {
    'gpu': 1,
    'motherboards': 2,
    'ram': 3,
    'procesadores': 4,
    'almacenamiento': 5,
    'gabinetes': 6,
    'fuentes': 7,
    'enfriamiento': 8,
    'monitores': 9,
    'perifericos': 10
};

window.goToBoutiqueCategory = function(cat) {
    const pageNum = BOUTIQUE_PAGE_MAP[cat] || 1;
    if (typeof changePage === 'function') {
        const btns = document.querySelectorAll('.pagination-btn');
        if (btns.length >= pageNum) {
            changePage(pageNum, btns[pageNum - 1]);
        }
    }
    const catSec = document.getElementById("productos");
    if (catSec) {
        catSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
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

    // Alerta de presupuesto crítico (< $6,500 MXN)
    if (total < 6500) {
        if (panelBox) {
            panelBox.className = "mt-1 p-3.5 rounded-xl border border-red-500 bg-red-950/20 text-red-400 flex flex-col sm:flex-row justify-between items-center gap-3 transition-all";
        }
        if (alertBox) alertBox.classList.remove('hidden');
    } else {
        if (panelBox) {
            panelBox.className = "mt-1 p-3.5 rounded-xl border border-slate-800 bg-slate-950 text-white flex flex-col sm:flex-row justify-between items-center gap-3 transition-all";
        }
        if (alertBox) alertBox.classList.add('hidden');
    }

    // Semáforo de "Computadora Completa y Funcional"
    const hasCoreHardware = (parseFloat(document.getElementById('select-cpu')?.value) || 0) > 0 &&
                            (parseFloat(document.getElementById('select-mobo')?.value) || 0) > 0 &&
                            (parseFloat(document.getElementById('select-ram')?.value) || 0) > 0 &&
                            (parseFloat(document.getElementById('select-ssd')?.value) || 0) > 0 &&
                            (parseFloat(document.getElementById('select-psu')?.value) || 0) > 0 &&
                            (parseFloat(document.getElementById('select-gabinete')?.value) || 0) > 0;

    const soSelectText = document.getElementById('select-software')?.selectedOptions[0]?.text || '';
    const hasOS = !soSelectText.toLowerCase().includes('sin sistema');

    if (statusBadge) {
        if (hasCoreHardware && hasOS) {
            statusBadge.className = "p-3 rounded-xl border border-emerald-500/40 bg-emerald-950/30 text-emerald-300 text-xs font-bold transition flex items-start gap-2.5";
            statusBadge.innerHTML = `<i class="fa-solid fa-circle-check text-base text-emerald-400 shrink-0 mt-0.5"></i>
                <div>
                    <span class="block font-black uppercase text-white">✅ COMPUTADORA COMPLETA Y FUNCIONAL</span>
                    <span class="text-[11px] font-normal text-slate-300">Tu ensamble cuenta con todos los componentes esenciales y sistema operativo para encender y operar. ¿Deseas agregar tarjeta de video dedicada o accesorios?</span>
                </div>`;
        } else if (hasCoreHardware && !hasOS) {
            statusBadge.className = "p-3 rounded-xl border border-amber-500/40 bg-amber-950/30 text-amber-300 text-xs font-bold transition flex items-start gap-2.5";
            statusBadge.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-base text-amber-400 shrink-0 mt-0.5"></i>
                <div>
                    <span class="block font-black uppercase text-amber-200">⚠️ Falta Sistema Operativo</span>
                    <span class="text-[11px] font-normal text-slate-300">El hardware está completo, pero se seleccionó "Sin Sistema Operativo". Selecciona Windows o Linux para entrega lista para usar.</span>
                </div>`;
        } else {
            statusBadge.className = "p-3 rounded-xl border border-red-500/40 bg-red-950/30 text-red-300 text-xs font-bold transition flex items-start gap-2.5";
            statusBadge.innerHTML = `<i class="fa-solid fa-circle-xmark text-base text-red-400 shrink-0 mt-0.5"></i>
                <div>
                    <span class="block font-black uppercase text-red-200">❌ Ensamble Incompleto</span>
                    <span class="text-[11px] font-normal text-slate-300">Faltan piezas indispensables para que la computadora encienda. Asegúrate de incluir Procesador, Tarjeta Madre, RAM, Almacenamiento, Fuente y Gabinete.</span>
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
            precio: parseFloat(total.replace(/[^0-9.]/g, '')) || 8200,
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

def update_entire_pc_custom_lab():
    print("=" * 75)
    print("REESTRUCTURANDO SECCIONES NIVELES Y COTIZADOR EN PC CUSTOM LAB")
    print("=" * 75)

    if not os.path.exists(PC_INDEX_PATH):
        print(f"[Error] No se encontró {PC_INDEX_PATH}")
        return

    with open(PC_INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Reemplazar la sección #niveles
    content = re.sub(r'<section[^>]*id=["\']niveles["\'][\s\S]*?<\/section>', NIVELES_SECTION_HTML, content, flags=re.IGNORECASE)

    # 2. Reemplazar la sección #cotizador
    content = re.sub(r'<section[^>]*id=["\']cotizador["\'][\s\S]*?<\/section>', COTIZADOR_HTML, content, flags=re.IGNORECASE)

    # 3. Inyectar o actualizar lógica JavaScript
    if "HARDWARE_CATALOG" not in content:
        content = content.replace("</script>", f"{JS_LOGICA_ACTUALIZADA}\n</script>")
    else:
        content = re.sub(r'\/\/ =+\s*CONFIGURADOR MODULAR[\s\S]*?enviarPresupuestoWhatsAppCotizador[\s\S]*?};', JS_LOGICA_ACTUALIZADA, content)

    with open(PC_INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("✓ pc-custom-lab/index.html actualizado y compilado.")

def deploy():
    print("\n" + "=" * 75)
    print("SUBIENDO CAMBIOS A GITHUB PAGES (-C GC.AUTO=0)")
    print("=" * 75)
    pc_dir = os.path.join(BASE_DIR, "pc-custom-lab")
    subprocess.run(["git", "add", "-A"], cwd=pc_dir, check=True)
    subprocess.run(["git", "commit", "-m", "feat(cotizador): sincronizacion de niveles i3 a ultra9, enlaces a boutique y validacion SO", "--allow-empty"], cwd=pc_dir, capture_output=True)
    res_pc = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=pc_dir, capture_output=True, text=True)
    print(f"🟢 pc-custom-lab -> Push: {'OK' if res_pc.returncode == 0 else res_pc.stderr.strip()}")

    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat(pc-custom-lab): actualizacion integral de niveles, cotizador piramidal y navegacion cruzada", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
    res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
    print(f"🟢 Monorepositorio Raíz -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    update_entire_pc_custom_lab()
    deploy()
