import os
import subprocess
import json
import urllib.parse

BASE_DIR = r"E:\sitios web"
APP_URL = "https://iaworldcenter-creator.github.io/sitios-web/app.html"

print("=" * 80)
print("INTEGRANDO BOTÓN 'MI CUENTA / DOMICILIO & CASHBACK' Y MODAL EN TODO EL ECOSISTEMA")
print("=" * 80)

# Barra de navegación cruzada
NAV_BAR_HTML = """
<nav class="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1 w-full lg:w-auto text-[11px] font-bold text-slate-300 shrink-0">
    <a href="https://iaworldcenter-creator.github.io/sitios-web/" class="px-2.5 py-1 rounded-lg bg-amber-500/15 border border-amber-500/40 text-amber-400 hover:bg-amber-500 hover:text-slate-950 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-house text-[10px]"></i> Matriz</a>
    <a href="https://iaworldcenter-creator.github.io/pc-custom-lab/" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 hover:text-cyan-400 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-microchip text-[10px] text-cyan-400"></i> PC Custom</a>
    <a href="https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 hover:text-cyan-300 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-gem text-[10px] text-cyan-300"></i> Vía MX</a>
    <a href="https://iaworldcenter-creator.github.io/cigarros-bazar/" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 hover:text-amber-400 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-smoking text-[10px] text-amber-400"></i> Cigarros</a>
    <a href="https://iaworldcenter-creator.github.io/dulces-bazar/" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 hover:text-pink-400 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-candy-cane text-[10px] text-pink-400"></i> Dulces</a>
    <a href="https://iaworldcenter-creator.github.io/kiosco-digital/" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 hover:text-indigo-400 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-newspaper text-[10px] text-indigo-400"></i> Kiosco</a>
    <a href="https://iaworldcenter-creator.github.io/mi-puesto-bazar/" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 hover:text-emerald-400 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-store text-[10px] text-emerald-400"></i> Mi Puesto</a>
    <a href="https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/" class="px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 hover:text-red-400 transition flex items-center gap-1 shrink-0"><i class="fa-solid fa-tags text-[10px] text-red-400"></i> Liquidaciones</a>
</nav>
"""

# Módulo Persuasivo del Código QR
QR_CARD_HTML = f"""
<div class="mt-4 p-4 bg-slate-950 border-2 border-cyan-400 rounded-3xl shadow-[0_0_25px_rgba(6,182,212,0.25)] text-center space-y-3">
    <div class="flex items-center justify-center gap-2">
        <i class="fa-solid fa-mobile-screen text-cyan-400 text-lg"></i>
        <span class="text-xs font-mono font-black text-white uppercase tracking-wider">App Móvil Pedidos Rápidos</span>
    </div>
    <div class="w-44 h-44 mx-auto bg-white p-2.5 rounded-2xl shadow-xl flex items-center justify-center">
        <img 
            src="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(APP_URL)}&margin=1" 
            alt="Código QR App BAZAR NFL" 
            class="w-full h-full object-contain rounded-lg"
            onerror="this.onerror=null; this.src='https://quickchart.io/qr?text={urllib.parse.quote(APP_URL)}&size=300';"
        />
    </div>
    <div class="space-y-1">
        <strong class="text-xs text-amber-400 block font-bold uppercase">Entrega Directa a tu Domicilio</strong>
        <p class="text-[11px] text-slate-300 leading-snug">Utiliza nuestra App oficial para que tus compras lleguen volando a la puerta de tu casa o taller.</p>
    </div>
    <div class="flex flex-col gap-2 pt-1">
        <a href="{APP_URL}" target="_blank" class="flex items-center justify-center gap-3 bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-emerald-400 py-2.5 px-3 rounded-xl text-left transition shadow group">
            <i class="fa-brands fa-google-play text-xl text-emerald-400 group-hover:scale-110 transition"></i>
            <div>
                <span class="text-[8px] font-mono text-slate-400 block uppercase leading-none">Disponible vía Web / PWA</span>
                <strong class="text-xs text-white block leading-none font-bold">Instalar en Android</strong>
            </div>
        </a>
        <a href="{APP_URL}" target="_blank" class="flex items-center justify-center gap-3 bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-cyan-400 py-2.5 px-3 rounded-xl text-left transition shadow group">
            <i class="fa-brands fa-apple text-2xl text-white group-hover:scale-110 transition"></i>
            <div>
                <span class="text-[8px] font-mono text-slate-400 block uppercase leading-none">Compatible con iPhone</span>
                <strong class="text-xs text-white block leading-none font-bold">Instalar en iOS / Apple</strong>
            </div>
        </a>
    </div>
</div>
"""

# Ventana Modal de Registro de Domicilio & Activación de Cashback
ACCOUNT_MODAL_HTML = """
<!-- MODAL FLOTANTE: MI CUENTA / DOMICILIO & CASHBACK -->
<div id="accountModal" class="fixed inset-0 z-[300] hidden">
    <div class="absolute inset-0 bg-slate-950/80 backdrop-blur-sm" onclick="toggleAccountModal()"></div>
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[95%] max-w-lg bg-slate-900 border-2 border-cyan-400 rounded-3xl shadow-2xl p-5 sm:p-6 z-10 max-h-[90vh] overflow-y-auto no-scrollbar space-y-4">
        
        <div class="flex justify-between items-start border-b border-slate-800 pb-3">
            <div>
                <span class="text-[10px] font-mono text-amber-400 uppercase font-bold tracking-widest block">Beneficio Exclusivo</span>
                <h3 class="font-black text-white text-base sm:text-lg flex items-center gap-2">
                    <i class="fa-solid fa-address-card text-cyan-400"></i> Mi Cuenta & Domicilio de Entrega
                </h3>
            </div>
            <button onclick="toggleAccountModal()" class="text-slate-400 hover:text-white p-1 text-lg cursor-pointer">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>

        <!-- Banner Explicativo de Cashback -->
        <div class="p-3 bg-gradient-to-r from-emerald-950/60 to-slate-950 border border-emerald-500/40 rounded-2xl space-y-1">
            <div class="flex items-center gap-2 text-emerald-400 text-xs font-bold font-mono">
                <i class="fa-solid fa-coins text-sm"></i>
                <span>5% DE CASHBACK EN CADA PEDIDO</span>
            </div>
            <p class="text-[11px] text-slate-300 leading-tight">
                <strong>Importante:</strong> Llena todos tus datos completos (Nombre, WhatsApp, Correo y Domicilio) para activar tu <strong>5% de Cashback acumulable</strong> y habilitar entregas directas con Uber Flash.
            </p>
        </div>

        <!-- Formulario de Cuenta y Dirección -->
        <div class="space-y-3 text-xs">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                <div>
                    <label class="text-[10px] font-mono text-slate-400 font-bold block mb-1">Nombre Completo / Taller:</label>
                    <input type="text" id="accName" placeholder="Ej. Juan Pérez / Taller Silva" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white outline-none focus:border-cyan-400 font-medium" />
                </div>
                <div>
                    <label class="text-[10px] font-mono text-slate-400 font-bold block mb-1">WhatsApp de Contacto:</label>
                    <input type="tel" id="accPhone" placeholder="Ej. 33 3727 1440" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white outline-none focus:border-cyan-400 font-medium font-mono" />
                </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                <div class="sm:col-span-2">
                    <label class="text-[10px] font-mono text-slate-400 font-bold block mb-1">Correo Electrónico:</label>
                    <input type="email" id="accEmail" placeholder="tu_correo@ejemplo.com" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white outline-none focus:border-cyan-400 font-medium" />
                </div>
                <div>
                    <label class="text-[10px] font-mono text-slate-400 font-bold block mb-1">Código Postal:</label>
                    <input type="text" id="accCP" placeholder="Ej. 44100" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white outline-none focus:border-cyan-400 font-mono font-bold" />
                </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                <div class="sm:col-span-2">
                    <label class="text-[10px] font-mono text-slate-400 font-bold block mb-1">Calle / Avenida:</label>
                    <input type="text" id="accCalle" placeholder="Ej. Av. Juárez, Hidalgo..." class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white outline-none focus:border-cyan-400 font-medium" />
                </div>
                <div>
                    <label class="text-[10px] font-mono text-slate-400 font-bold block mb-1">Núm. Ext / Int:</label>
                    <input type="text" id="accNum" placeholder="Ej. #501 int A" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white outline-none focus:border-cyan-400 font-medium" />
                </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                <div>
                    <label class="text-[10px] font-mono text-slate-400 font-bold block mb-1">Colonia / Barrio:</label>
                    <input type="text" id="accColonia" placeholder="Ej. Americana, Centro, Vallarta..." class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white outline-none focus:border-cyan-400 font-medium" />
                </div>
                <div>
                    <label class="text-[10px] font-mono text-slate-400 font-bold block mb-1">Municipio / Zona:</label>
                    <select id="accMunicipio" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white outline-none focus:border-cyan-400 font-medium">
                        <option value="">-- Selecciona Municipio --</option>
                        <option value="guadalajara">Guadalajara (Centro / Alrededores)</option>
                        <option value="zapopan">Zapopan (Minerva / Providencia / Poniente)</option>
                        <option value="tlaquepaque">Tlaquepaque (Centro / Alamo)</option>
                        <option value="tonala">Tonalá (Oriente / Periférico)</option>
                        <option value="tlajomulco">Tlajomulco de Zúñiga (Zona Sur / Payuca)</option>
                        <option value="elsalto">El Salto / Aeropuerto</option>
                    </select>
                </div>
            </div>

            <div>
                <label class="text-[10px] font-mono text-slate-400 font-bold block mb-1">Referencias de Entrega (Opcional):</label>
                <input type="text" id="accRef" placeholder="Ej. Portón blanco, entre calle Galeana y Colón" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white outline-none focus:border-cyan-400 font-medium" />
            </div>

            <!-- Caja de Estado / Alerta -->
            <div id="accAlertBox" class="hidden p-3 rounded-xl text-xs font-mono leading-tight"></div>
        </div>

        <div class="pt-2 border-t border-slate-800 flex flex-col sm:flex-row gap-2">
            <button onclick="saveUserProfile()" class="flex-1 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-black py-3 rounded-xl text-xs uppercase tracking-wider transition active:scale-95 shadow-lg flex items-center justify-center gap-2 cursor-pointer">
                <i class="fa-solid fa-floppy-disk text-sm"></i> <span>Guardar Domicilio & Activar Cashback</span>
            </button>
        </div>

    </div>
</div>
"""

# JavaScript Universal para manejo de Cuenta y Cashback
ACCOUNT_JS = """
function getSavedProfile() {
    try {
        const raw = localStorage.getItem('bazar_user_profile');
        return raw ? JSON.parse(raw) : null;
    } catch(e) { return null; }
}

function updateAccountBadgeUI() {
    const profile = getSavedProfile();
    const btn = document.getElementById("header-account-btn");
    if (!btn) return;

    if (profile && profile.isComplete) {
        btn.innerHTML = `
            <div class="flex items-center gap-2 bg-emerald-950/60 border border-emerald-500/50 px-3 py-1.5 rounded-xl text-emerald-300 text-xs font-mono font-bold shadow-md hover:bg-emerald-900/60 transition">
                <i class="fa-solid fa-circle-check text-emerald-400 text-sm"></i>
                <div class="flex flex-col text-left">
                    <span class="text-[9px] text-emerald-400 leading-none uppercase">5% Cashback Activo</span>
                    <span class="text-white text-[11px] leading-tight truncate max-w-[120px] sm:max-w-[180px]">${profile.name || 'Mi Cuenta'}</span>
                </div>
            </div>
        `;
    } else {
        btn.innerHTML = `
            <div class="flex items-center gap-2 bg-slate-800/90 hover:bg-slate-700 border border-cyan-500/40 px-3 py-1.5 rounded-xl text-white text-xs font-mono font-bold shadow-md transition">
                <i class="fa-solid fa-user-plus text-cyan-400 text-sm"></i>
                <div class="flex flex-col text-left">
                    <span class="text-[9px] text-amber-400 leading-none uppercase">5% Cashback</span>
                    <span class="text-slate-200 text-[11px] leading-tight">Registra tu Domicilio</span>
                </div>
            </div>
        `;
    }
}

function toggleAccountModal() {
    const modal = document.getElementById("accountModal");
    if (!modal) return;
    modal.classList.toggle("hidden");

    if (!modal.classList.contains("hidden")) {
        loadProfileIntoModal();
    }
}

function loadProfileIntoModal() {
    const p = getSavedProfile() || {};
    document.getElementById("accName").value = p.name || '';
    document.getElementById("accPhone").value = p.phone || '';
    document.getElementById("accEmail").value = p.email || '';
    document.getElementById("accCP").value = p.cp || '';
    document.getElementById("accCalle").value = p.calle || '';
    document.getElementById("accNum").value = p.num || '';
    document.getElementById("accColonia").value = p.colonia || '';
    document.getElementById("accMunicipio").value = p.municipio || '';
    document.getElementById("accRef").value = p.ref || '';

    const alertBox = document.getElementById("accAlertBox");
    if (p.isComplete) {
        alertBox.className = "p-3 rounded-xl text-xs font-mono leading-tight bg-emerald-950/60 border border-emerald-500/50 text-emerald-300 block";
        alertBox.innerHTML = '🎉 <strong>¡Felicidades!</strong> Tu perfil está completo y tienes <strong>5% de Cashback activo</strong> en todas tus compras.';
    } else {
        alertBox.className = "hidden";
    }
}

function saveUserProfile() {
    const name = document.getElementById("accName").value.trim();
    const phone = document.getElementById("accPhone").value.trim();
    const email = document.getElementById("accEmail").value.trim();
    const cp = document.getElementById("accCP").value.trim();
    const calle = document.getElementById("accCalle").value.trim();
    const num = document.getElementById("accNum").value.trim();
    const colonia = document.getElementById("accColonia").value.trim();
    const municipio = document.getElementById("accMunicipio").value;
    const ref = document.getElementById("accRef").value.trim();
    const alertBox = document.getElementById("accAlertBox");

    if (!name || !phone || !email || !cp || !calle || !num || !colonia || !municipio) {
        alertBox.className = "p-3 rounded-xl text-xs font-mono leading-tight bg-amber-950/70 border border-amber-500/60 text-amber-300 block";
        alertBox.innerHTML = '⚠️ <strong>Perfil Incompleto:</strong> Para acumular tu 5% de Cashback y habilitar envíos Uber Flash, es obligatorio llenar todos los campos de contacto y domicilio.';
        return;
    }

    let rate = 35;
    let dist = "1.8 km (Guadalajara Centro)";
    if (municipio === "zapopan") { rate = 52; dist = "4.8 km (Zapopan)"; }
    else if (municipio === "tlaquepaque") { rate = 48; dist = "4.5 km (Tlaquepaque)"; }
    else if (municipio === "tonala") { rate = 70; dist = "9.2 km (Tonalá)"; }
    else if (municipio === "tlajomulco") { rate = 125; dist = "18.5 km (Tlajomulco Sur/Payuca)"; }
    else if (municipio === "elsalto") { rate = 135; dist = "21.0 km (El Salto)"; }

    const profile = {
        name, phone, email, cp, calle, num, colonia, municipio, ref,
        rate, dist, isComplete: true, updatedAt: new Date().toISOString()
    };

    localStorage.setItem('bazar_user_profile', JSON.stringify(profile));
    updateAccountBadgeUI();

    alertBox.className = "p-3 rounded-xl text-xs font-mono leading-tight bg-emerald-950/60 border border-emerald-500/50 text-emerald-300 block";
    alertBox.innerHTML = '🎉 <strong>¡Domicilio Guardado Exitosamente!</strong> Tu 5% de Cashback está activo. El costo estimado de flete Uber Flash a tu zona es de <strong>$' + rate.toFixed(2) + ' MXN</strong>.';

    setTimeout(() => {
        toggleAccountModal();
    }, 1200);
}
"""

# Configuración de las 7 Boutiques
boutiques_data = {
    "pc-custom-lab": {
        "folder_pattern": "pc-custom-lab",
        "title": "PC Custom Lab | Hardware, GPUs & Ensambles IA 2026",
        "name": "PC CUSTOM LAB",
        "tag": "TECNOLOGÍA & GAMING",
        "subtitle": "Pedro Moreno 501 A • Hardware de Alto Rendimiento, GPUs & Ensambles IA",
        "color": "text-cyan-400",
        "categories": [
            {"name": "Tarjetas de Video RTX & Radeon", "icon": "fa-microchip"},
            {"name": "Procesadores Intel & AMD Ryzen", "icon": "fa-bolt"},
            {"name": "Tarjetas Madre LGA1700 & AM5", "icon": "fa-server"},
            {"name": "Memorias RAM DDR5 & DDR4", "icon": "fa-memory"},
            {"name": "Discos SSD M.2 NVMe PCIe 4.0", "icon": "fa-hard-drive"},
            {"name": "Gabinetes & Fuentes Modulares", "icon": "fa-cube"}
        ],
        "products": [
            {"sku": "PC-001", "nombre": "Gabinete Micro-ATX con Fuente 500W Incluida", "marca": "Acteck", "precio": 1250.00, "original": 1550.00, "desc": "Chasis esbelto con fuente certificada y USB 3.0 frontal.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/gabinete_negro.webp", "tokens": ["gabinete", "fuente", "pc", "chasis"]},
            {"sku": "PC-002", "nombre": "Tarjeta Madre ASUS Prime B760M-A WiFi DDR5", "marca": "ASUS", "precio": 3400.00, "original": 3950.00, "desc": "Soporte Intel 12va/13va/14va Gen y dual M.2 PCIe 4.0.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/motherboard_asus.webp", "tokens": ["tarjeta madre", "motherboard", "asus", "placa"]},
            {"sku": "PC-003", "nombre": "Procesador Intel Core i5-14400F 10C/16T con Disipador", "marca": "Intel", "precio": 4350.00, "original": 4990.00, "desc": "10 núcleos híbridos de alto rendimiento con disipador silencioso.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/cpu_intel_ultra.webp", "tokens": ["procesador", "cpu", "intel", "i5"]},
            {"sku": "PC-004", "nombre": "Memoria RAM Kingston FURY Beast 16GB DDR5 5600MHz", "marca": "Kingston", "precio": 1250.00, "original": 1500.00, "desc": "Módulo DDR5 de alta velocidad con disipador de aluminio negro.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/ram_caja.webp", "tokens": ["ram", "kingston", "fury", "ddr5", "memoria"]},
            {"sku": "PC-005", "nombre": "Disco Sólido SSD Kingston NV2 1TB NVMe PCIe 4.0", "marca": "Kingston", "precio": 1350.00, "original": 1650.00, "desc": "3,500 MB/s de lectura secuencial para carga instantánea.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/disco_solido_m2.webp", "tokens": ["ssd", "kingston", "nvme", "disco", "m2"]},
            {"sku": "PC-006", "nombre": "Tarjeta Gráfica NVIDIA RTX 4070 Ti Super 16GB", "marca": "NVIDIA", "precio": 17800.00, "original": 21500.00, "desc": "DLSS 3, Ray Tracing y 16GB GDDR6X para gaming 4K.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/gpu_nvidia.webp", "tokens": ["gpu", "nvidia", "rtx", "4070", "grafica"]}
        ]
    },
    "bazar-viamx-nfl.gdl": {
        "folder_pattern": "bazar-viamx",
        "title": "Vía MX Boutique | Curaduría Departamental 2026",
        "name": "VÍA MX BOUTIQUE",
        "tag": "DEPARTAMENTAL & B2B",
        "subtitle": "Pedro Moreno 501 A • 30 Departamentos, Electrónica, Hogar & B2B",
        "color": "text-cyan-300",
        "categories": [
            {"name": "Pantallas Smart TV & Audio HD", "icon": "fa-tv"},
            {"name": "Refrigeradores & Línea Blanca", "icon": "fa-snowflake"},
            {"name": "Laptops & Computación Slim", "icon": "fa-laptop"},
            {"name": "Telefonía 5G & Celulares", "icon": "fa-mobile-screen"},
            {"name": "Electrodomésticos & Cocina", "icon": "fa-kitchen-set"},
            {"name": "Ropa NFL & Moda Internacional", "icon": "fa-shirt"}
        ],
        "products": [
            {"sku": "VMX-001", "nombre": "Pantalla Smart TV 55 Pulgadas 4K UHD HDR10+ WiFi", "marca": "Samsung", "precio": 7999.00, "original": 11499.00, "desc": "Panel LED 4K ultra nítido con asistente de voz.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_curvo_negro.webp", "tokens": ["pantalla", "smart tv", "samsung", "4k"]},
            {"sku": "VMX-002", "nombre": "Refrigerador Inverter No Frost 14 Pies Cúbicos Acero", "marca": "LG", "precio": 11899.00, "original": 15999.00, "desc": "Doble puerta con compresor Digital Inverter y despachador.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_warehouse_thumb.webp", "tokens": ["refrigerador", "lg", "linea blanca", "inverter"]},
            {"sku": "VMX-003", "nombre": "Freidora de Aire Digital 6.5 Litros con 12 Programas", "marca": "Tefal", "precio": 1499.00, "original": 2199.00, "desc": "Canastilla antiadherente libre de BPA con calor envolvente 360.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp", "tokens": ["freidora", "aire", "airfryer", "tefal"]},
            {"sku": "VMX-004", "nombre": "Laptop Ultra Slim 15.6 Pulgadas Core i7 16GB RAM 512GB", "marca": "Lenovo", "precio": 14500.00, "original": 18900.00, "desc": "Chasis de aluminio ligero, teclado iluminado y lector de huella.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_mantenimiento_thumb.webp", "tokens": ["laptop", "lenovo", "core i7", "computadora"]},
            {"sku": "VMX-005", "nombre": "Smartphone 5G Desbloqueado 256GB / 8GB RAM 108MP", "marca": "Motorola", "precio": 4899.00, "original": 6499.00, "desc": "Pantalla AMOLED 120Hz con batería de 5000mAh.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/perifericos_combo_1.webp", "tokens": ["celular", "telefono", "smartphone", "motorola"]}
        ]
    },
    "cigarros-bazar": {
        "folder_pattern": "cigarros-bazar",
        "title": "Cigarros Bazar | Puros Habanos & Tabacos Selectos 2026",
        "name": "CIGARROS BAZAR",
        "tag": "TABACOS & HABANOS",
        "subtitle": "Pedro Moreno 501 A • Cigarros Premium, Puros Habanos & Accesorios",
        "color": "text-amber-400",
        "categories": [
            {"name": "Cigarros Nacionales & Importación", "icon": "fa-smoking"},
            {"name": "Puros Habanos Cubanos Hechos a Mano", "icon": "fa-gem"},
            {"name": "Tabaco para Liar & Filtros Especiales", "icon": "fa-leaf"},
            {"name": "Encendedores Recargables & Antorchas", "icon": "fa-fire"}
        ],
        "products": [
            {"sku": "CIG-001", "nombre": "Cigarros Marlboro Gold Original (Cajetilla 20)", "marca": "Marlboro", "precio": 82.00, "original": 95.00, "desc": "Sabor suave y filtro blanco balanceado.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", "tokens": ["cigarros", "marlboro", "gold", "tabaco"]},
            {"sku": "CIG-002", "nombre": "Cigarros Benson & Hedges Black Switch (Cajetilla 20)", "marca": "Benson & Hedges", "precio": 88.00, "original": 105.00, "desc": "Cápsula de sabor mentolado premium.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", "tokens": ["cigarros", "benson", "hedges", "mentolados"]},
            {"sku": "CIG-003", "nombre": "Puro Habanos Cohiba Siglo VI Tubo Individual", "marca": "Cohiba", "precio": 850.00, "original": 1100.00, "desc": "Puro cubano hecho a mano con notas amaderadas.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", "tokens": ["puro", "cohiba", "siglo vi", "habano"]},
            {"sku": "CIG-005", "nombre": "Encendedor de Colección Vintage a Gas Recargable", "marca": "Clipper Pro", "precio": 195.00, "original": 260.00, "desc": "Cuerpo metálico cepillado con piedra intercambiable.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", "tokens": ["encendedor", "clipper", "fuego", "gas"]}
        ]
    },
    "dulces-bazar": {
        "folder_pattern": "dulces-bazar",
        "title": "Dulces Bazar | Confitería Mexicana & Mayoreo 2026",
        "name": "DULCES BAZAR",
        "tag": "CONFITERÍA & BOTANAS",
        "subtitle": "Pedro Moreno 501 A • Paletas, Chocolates Finos, Mazapanes & Botanas",
        "color": "text-pink-400",
        "categories": [
            {"name": "Paletas & Malvaviscos Tradicionales", "icon": "fa-candy-cane"},
            {"name": "Mazapanes & Dulces de Cacahuate", "icon": "fa-cookie"},
            {"name": "Caramelos Macizos con Chile & Ácidos", "icon": "fa-pepper-hot"}
        ],
        "products": [
            {"sku": "DUL-001", "nombre": "Paleta Payaso Ricolino (Caja con 15 piezas)", "marca": "Ricolino", "precio": 245.00, "original": 290.00, "desc": "Malvavisco cubierto de chocolate con gomitas de colores.", "img": "assets/img/mascota_tigre_thumb.webp", "tokens": ["paleta", "payaso", "ricolino", "dulces"]},
            {"sku": "DUL-002", "nombre": "Mazapán De La Rosa Gigante (Caja con 20 piezas)", "marca": "De La Rosa", "precio": 160.00, "original": 195.00, "desc": "El dulce tradicional mexicano de cacahuate tostado.", "img": "assets/img/mascota_tigre_thumb.webp", "tokens": ["mazapan", "de la rosa", "cacahuate"]},
            {"sku": "DUL-003", "nombre": "Rocaleta Sonrics con Centro de Goma (Bolsa 30)", "marca": "Sonrics", "precio": 185.00, "original": 230.00, "desc": "Caramelo con 4 capas de chile ácido.", "img": "assets/img/mascota_tigre_thumb.webp", "tokens": ["rocaleta", "sonrics", "chile", "paleta"]},
            {"sku": "DUL-004", "nombre": "Chocolates Finos Surtidos Artesanales Caja Regalo", "marca": "Turín", "precio": 220.00, "original": 280.00, "desc": "Bombones semiamargos rellenos de licor.", "img": "assets/img/mascota_tigre_thumb.webp", "tokens": ["chocolate", "turin", "bombones"]}
        ]
    },
    "kiosco-digital": {
        "folder_pattern": "kiosco-digital",
        "title": "Kiosco Digital | Revistas, Prensa & Suscripciones 2026",
        "name": "KIOSCO DIGITAL",
        "tag": "LECTURA & CULTURA",
        "subtitle": "Pedro Moreno 501 A • Suscripciones Digitales, Revistas HD & Prensa",
        "color": "text-indigo-400",
        "categories": [
            {"name": "Revistas de Ciencia, Naturaleza & Espacio", "icon": "fa-atom"},
            {"name": "Divulgación Científica & Curiosidades", "icon": "fa-brain"},
            {"name": "Prensa Matutina & Periódicos de GDL", "icon": "fa-newspaper"}
        ],
        "products": [
            {"sku": "KIO-001", "nombre": "Suscripción Digital Anual Revista National Geographic", "marca": "RBA", "precio": 599.00, "original": 850.00, "desc": "12 ediciones digitales en alta definición.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_plano_blanco.webp", "tokens": ["revista", "national geographic", "natgeo", "digital"]},
            {"sku": "KIO-002", "nombre": "Suscripción Digital Revista Muy Interesante (1 Año)", "marca": "Zinet", "precio": 450.00, "original": 620.00, "desc": "Acceso total a reportajes de ciencia e innovación.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_plano_blanco.webp", "tokens": ["revista", "muy interesante", "ciencia"]},
            {"sku": "KIO-003", "nombre": "Suscripción Revista Conozca Más Digital Colección", "marca": "Editorial Televisa", "precio": 380.00, "original": 490.00, "desc": "Enciclopedia de curiosidades científicas.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_plano_blanco.webp", "tokens": ["revista", "conozca mas", "cultura"]}
        ]
    },
    "mi-puesto-bazar": {
        "folder_pattern": "mi-puesto-bazar",
        "title": "Mi Puesto Bazar | Novedades, Gadgets & Conveniencia 2026",
        "name": "MI PUESTO BAZAR",
        "tag": "NOVEDADES & GADGETS",
        "subtitle": "Pedro Moreno 501 A • Lentes Inteligentes, Consolas Retro & Cables",
        "color": "text-emerald-400",
        "categories": [
            {"name": "Lentes Inteligentes Bluetooth & Audio", "icon": "fa-glasses"},
            {"name": "Consolas Retro Portátiles & Arcade", "icon": "fa-gamepad"},
            {"name": "Cables USB-C, Cargadores & Hubs", "icon": "fa-plug"}
        ],
        "products": [
            {"sku": "PUE-001", "nombre": "Lentes Inteligentes Bluetooth con Audio y Micrófono", "marca": "SmartVision", "precio": 680.00, "original": 950.00, "desc": "Llamadas y música con protección UV.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_gamer_thumb.webp", "tokens": ["lentes", "inteligentes", "bluetooth", "audio"]},
            {"sku": "PUE-002", "nombre": "Consola Retro Portátil con 500 Juegos Clásicos", "marca": "Sup Game", "precio": 290.00, "original": 390.00, "desc": "Batería recargable y salida para TV.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_gemini_thumb.webp", "tokens": ["consola", "retro", "videojuegos", "juegos"]},
            {"sku": "PUE-003", "nombre": "Cable de Carga Rápida USB-C a USB-C de 65W Reforzado", "marca": "Baseus", "precio": 120.00, "original": 180.00, "desc": "Cable trenzado de nailon para celulares y laptops.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/fuente_modular.webp", "tokens": ["cable", "cargador", "usb c", "carga rapida"]}
        ]
    },
    "ofertas-y-liquidaciones": {
        "folder_pattern": "ofertas-y-liquidaciones",
        "title": "Ofertas & Liquidaciones | Outlet Directo B2B 2026",
        "name": "OFERTAS & LIQUIDACIONES",
        "tag": "OUTLET & REMATES",
        "subtitle": "Pedro Moreno 501 A • Remates de Bodega, Excedentes & Lotes con 50% Dto",
        "color": "text-red-400",
        "categories": [
            {"name": "Lotes de Remate Electrónica & B2B", "icon": "fa-layer-group"},
            {"name": "Monitores & Pantallas de Exhibición", "icon": "fa-display"},
            {"name": "Herramientas al Costo en Maletín", "icon": "fa-toolbox"}
        ],
        "products": [
            {"sku": "OFE-001", "nombre": "Lote de Remate Electrónica y Accesorios Varios Grado A", "marca": "Sony / Varios", "precio": 2490.00, "original": 3800.00, "desc": "Paquete surtido de oportunidad comercial.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/software_estante_madera.webp", "tokens": ["lote", "remate", "liquidacion", "oferta"]},
            {"sku": "OFE-002", "nombre": "Monitor Curvo 24 Pulgadas 144Hz Full HD Exhibición", "marca": "AOC", "precio": 2100.00, "original": 3200.00, "desc": "Equipo de vitrina 10/10 con cables.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_curvo_negro.webp", "tokens": ["monitor", "curvo", "aoc", "144hz"]},
            {"sku": "OFE-003", "nombre": "Kit de Herramientas Mecánicas 168 Piezas en Maletín", "marca": "Stanley", "precio": 899.00, "original": 1299.00, "desc": "Matraca y dados milimétricos al costo.", "img": "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/software_estante_muro.webp", "tokens": ["herramientas", "stanley", "maletin"]}
        ]
    }
}

def generate_boutique_html(data):
    js_products = json.dumps(data["products"], ensure_ascii=False)
    js_categories = json.dumps(data["categories"], ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{data["title"]}</title>
    <meta name="description" content="{data["subtitle"]}" />
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />

    <style>
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
        .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
        .cart-pop {{ animation: popBadge 0.25s ease-in-out; }}
        @keyframes popBadge {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.35); }} 100% {{ transform: scale(1); }} }}
    </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen flex flex-col justify-between overflow-x-hidden selection:bg-cyan-500 selection:text-slate-950">

    <header class="bg-slate-900/95 backdrop-blur border-b border-slate-800 sticky top-0 z-50 shadow-2xl">
        <div class="max-w-[99%] 2xl:max-w-[1850px] mx-auto px-4 py-2 flex flex-wrap items-center justify-between gap-2 text-xs border-b border-slate-800/80">
            <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded bg-amber-500/10 border border-amber-500/30 text-amber-400 font-mono font-bold text-[10px] uppercase">
                    Envío Exprés El Mismo Día
                </span>
                <span class="text-slate-300 hidden xl:inline text-[11px] font-semibold">Guadalajara Centro • Carrito Unificado</span>
            </div>

            {NAV_BAR_HTML}

            <div class="flex items-center gap-3 font-bold text-[11px]">
                <a href="https://gemini.google.com" target="_blank" class="text-slate-300 hover:text-cyan-400 transition flex items-center gap-1">
                    <i class="fa-solid fa-wand-magic-sparkles text-cyan-400"></i> Gemini AI
                </a>
                <span class="text-slate-700">|</span>
                <a href="https://antigravity.google/download" target="_blank" class="text-slate-300 hover:text-amber-400 transition flex items-center gap-1">
                    <i class="fa-solid fa-download text-amber-400"></i> Anti-Gravity
                </a>
            </div>
        </div>

        <!-- Nivel 2: Marca + Botón "Mi Cuenta / Cashback" + Buscador + Carrito -->
        <div class="max-w-[99%] 2xl:max-w-[1850px] mx-auto px-4 py-3 flex flex-col md:flex-row items-center justify-between gap-3">
            
            <div class="flex items-center justify-between w-full md:w-auto gap-3">
                <div class="flex items-center gap-3 cursor-pointer shrink-0" onclick="document.getElementById('pie-de-pagina').scrollIntoView({{ behavior: 'smooth' }});">
                    <div class="relative w-12 h-12 flex items-center justify-center">
                        <img src="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" alt="Logo Tigre {data["name"]}" class="w-12 h-12 rounded-full object-cover border-2 border-amber-400 shadow-[0_0_15px_rgba(251,191,36,0.5)]" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';" />
                    </div>
                    <div class="flex flex-col">
                        <span class="font-black text-xl sm:text-2xl text-white tracking-wider uppercase leading-none">{data["name"]}</span>
                        <span class="text-[10px] sm:text-[11px] font-mono {data["color"]} uppercase tracking-tight mt-1 flex items-center gap-1">
                            <i class="fa-solid fa-location-dot text-amber-400"></i> Pedro Moreno 501 A
                        </span>
                    </div>
                </div>

                <!-- Botón Compacto de Mi Cuenta / Cashback -->
                <button id="header-account-btn" onclick="toggleAccountModal()" class="cursor-pointer active:scale-95 transition shrink-0"></button>
            </div>

            <!-- Buscador Search-First -->
            <div class="flex-1 max-w-2xl w-full relative">
                <div class="flex items-center bg-white rounded-full border-2 border-cyan-400 shadow-[0_0_22px_rgba(6,182,212,0.4)] px-4 py-1.5 gap-2">
                    <i class="fa-solid fa-magnifying-glass text-slate-400 text-sm"></i>
                    <input type="text" id="boutiqueSearchInput" autocomplete="off" spellcheck="false" placeholder="Busca en {data['name']} (ej. por producto, SKU, síntoma o marca)..." class="flex-1 bg-transparent border-0 outline-none text-slate-950 font-bold text-sm placeholder-slate-400" oninput="onBoutiqueSearch(event)" />
                    <button onclick="clearBoutiqueSearch()" id="clear-search-btn" class="hidden text-slate-400 hover:text-slate-600 text-xs px-2 font-bold cursor-pointer"><i class="fa-solid fa-xmark"></i></button>
                    <button onclick="executeBoutiqueSearch()" class="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black px-6 py-2 rounded-full text-xs uppercase tracking-wider transition active:scale-95 shrink-0 shadow cursor-pointer">BUSCAR</button>
                </div>
                <div id="boutique-autocomplete-box" class="hidden absolute top-full left-0 right-0 mt-2 bg-slate-900 border-2 border-cyan-500/60 rounded-2xl shadow-2xl z-50 p-2.5 flex flex-col gap-2 max-h-96 overflow-y-auto no-scrollbar"></div>
            </div>

            <button onclick="toggleCartDrawer()" class="flex items-center gap-3 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white px-4 py-2.5 rounded-xl transition cursor-pointer active:scale-95 shadow shrink-0 group">
                <div class="relative">
                    <i class="fa-solid fa-cart-shopping text-cyan-400 text-base group-hover:scale-110 transition"></i>
                    <span id="boutique-cart-badge" class="absolute -top-2.5 -right-2.5 bg-amber-500 text-slate-950 font-mono font-black text-[10px] rounded-full w-5 h-5 flex items-center justify-center shadow">0</span>
                </div>
                <div class="flex flex-col text-left">
                    <span class="text-[10px] font-mono text-slate-400 uppercase leading-none">Canasta Global</span>
                    <span id="boutique-cart-total" class="text-xs font-mono font-bold text-amber-400">$0.00 MXN</span>
                </div>
            </button>
        </div>
    </header>

    <main class="w-full max-w-[99%] 2xl:max-w-[1850px] mx-auto px-2 sm:px-4 py-6 flex-1">
        
        <div class="flex flex-col lg:flex-row gap-8 items-start justify-center">
            
            <aside class="w-full lg:w-[340px] xl:w-[370px] shrink-0 bg-slate-900/90 rounded-3xl p-5 shadow-2xl relative" id="boutique-sidebar-root">
                <div class="flex items-center justify-between border-b border-slate-800 pb-3.5 mb-3.5">
                    <h3 class="font-mono text-sm font-black text-white uppercase tracking-wider flex items-center gap-2 truncate">
                        <i class="fa-solid fa-layer-group text-amber-400"></i> Departamentos
                    </h3>
                </div>
                <div class="mb-3.5">
                    <span class="text-[10px] font-mono text-cyan-400 font-bold bg-cyan-950/40 border border-cyan-500/30 px-3 py-1 rounded-xl block text-center uppercase tracking-widest">
                        Compras Rápidas
                    </span>
                </div>

                <nav class="flex flex-col gap-2" id="sidebar-categories-list"></nav>

                <!-- CÓDIGO QR PERSUASIVO -->
                {QR_CARD_HTML}

                <div class="mt-5 pt-5 border-t border-slate-800 flex flex-col gap-3">
                    <div class="bg-gradient-to-b from-slate-950 to-slate-900 border border-cyan-500/40 rounded-2xl p-4 flex flex-col gap-2 shadow-lg">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-wand-magic-sparkles text-cyan-400 text-sm"></i>
                            <span class="text-[10px] font-mono font-bold uppercase text-cyan-300">Creado por Google Gemini</span>
                        </div>
                        <p class="text-[11px] text-slate-300 leading-snug">Concebido y programado con la Inteligencia Artificial de Google Gemini.</p>
                        <a href="https://gemini.google.com" target="_blank" class="w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black py-2 rounded-xl text-xs text-center uppercase tracking-wider transition active:scale-95 shadow">Suscribirse a Gemini</a>
                    </div>
                    <div class="bg-gradient-to-b from-slate-950 to-slate-900 border border-amber-500/40 rounded-2xl p-4 flex flex-col gap-2 shadow-lg">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-robot text-amber-400 text-sm"></i>
                            <span class="text-[10px] font-mono font-bold uppercase text-amber-300">Desarrollado por Anti-Gravity</span>
                        </div>
                        <p class="text-[11px] text-slate-300 leading-snug">Desarrollado, optimizado y desplegado por Anti-Gravity Copilot.</p>
                        <a href="https://antigravity.google/download" target="_blank" class="w-full bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black py-2 rounded-xl text-xs text-center uppercase tracking-wider transition active:scale-95 shadow">Bajar Anti-Gravity Gratis</a>
                    </div>
                </div>
            </aside>

            <!-- ESCAPARATE CON 2 PRODUCTOS EN MÓVIL + FLECHAS -->
            <section class="flex-1 w-full flex flex-col gap-4 min-w-0">
                <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                    <span class="text-xs font-mono text-cyan-400 font-bold uppercase tracking-wider" id="results-count-txt">
                        Catálogo de Entrega Inmediata
                    </span>
                    <span class="text-xs font-mono text-slate-400">Pedro Moreno 501 A</span>
                </div>

                <div class="relative">
                    <button onclick="scrollCarousel('products-grid-container', -1)" class="lg:hidden absolute -left-2 top-1/2 -translate-y-1/2 z-20 w-8 h-8 rounded-full bg-slate-900 border border-cyan-400 text-cyan-300 flex items-center justify-center shadow-lg active:scale-90">
                        <i class="fa-solid fa-chevron-left text-xs"></i>
                    </button>

                    <div id="products-grid-container" class="flex flex-row overflow-x-auto flex-nowrap lg:grid lg:grid-cols-5 lg:overflow-visible gap-3 pb-3 lg:pb-0 no-scrollbar snap-x snap-mandatory scroll-smooth px-1">
                    </div>

                    <button onclick="scrollCarousel('products-grid-container', 1)" class="lg:hidden absolute -right-2 top-1/2 -translate-y-1/2 z-20 w-8 h-8 rounded-full bg-slate-900 border border-cyan-400 text-cyan-300 flex items-center justify-center shadow-lg active:scale-90">
                        <i class="fa-solid fa-chevron-right text-xs"></i>
                    </button>
                </div>
            </section>

        </div>
    </main>

    {ACCOUNT_MODAL_HTML}

    <footer class="bg-slate-950 border-t border-slate-900 pt-16 pb-8 text-slate-400 text-xs" id="pie-de-pagina">
        <div class="max-w-[99%] 2xl:max-w-[1850px] mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 pb-12 border-b border-slate-800/80">
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2"><i class="fa-solid fa-location-dot text-amber-400"></i> Contacto Local</h4>
                    <p class="flex items-start gap-2 text-slate-300"><i class="fa-solid fa-map-pin text-slate-500 mt-0.5 shrink-0"></i><span>Pedro Moreno 501 A, Guadalajara Centro, Jalisco (CP 44100)</span></p>
                    <p class="flex items-center gap-2"><i class="fa-solid fa-phone text-cyan-400 shrink-0"></i><span>Teléfono: <a href="tel:3336136348" class="text-slate-200 hover:text-cyan-400 font-mono">(33) 3613 6348</a></span></p>
                    <p class="flex items-center gap-2"><i class="fa-brands fa-whatsapp text-emerald-400 shrink-0 text-sm"></i><span>WhatsApp: <a href="https://wa.me/523337271440" target="_blank" class="text-slate-200 hover:text-emerald-400 font-mono">+52 33 3727 1440</a></span></p>
                </div>
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2"><i class="fa-solid fa-shield-halved text-cyan-400"></i> Políticas de Compra</h4>
                    <p class="text-[11px] text-slate-400">Devoluciones en tienda dentro de las 48 horas con empaque íntegro. Soporte técnico local y reemplazo inmediato.</p>
                </div>
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2"><i class="fa-solid fa-coins text-emerald-400"></i> Ahorro y Cashback</h4>
                    <p class="text-slate-300 font-bold">5% de Cashback acumulable con tu cuenta registrada.</p>
                </div>
            </div>
            <div class="pt-8 text-center text-slate-500 text-[11px]">
                <p>&copy; 2026 {data["name"]} & Ecosistema Comercial Pedro Moreno 501 A. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>

    <script>
    const boutiqueProducts = {js_products};
    const boutiqueCategories = {js_categories};

    {ACCOUNT_JS}

    function scrollCarousel(id, direction) {{
        const el = document.getElementById(id);
        if (el) {{
            const amount = el.clientWidth * 0.85;
            el.scrollBy({{ left: direction * amount, behavior: 'smooth' }});
        }}
    }}

    function renderBoutiqueSidebar() {{
        const container = document.getElementById("sidebar-categories-list");
        if (!container) return;
        container.innerHTML = boutiqueCategories.map(c => `
            <button onclick="filterCategory('${{c.name}}')" class="w-full text-left p-3.5 rounded-2xl bg-slate-950/70 hover:bg-slate-800/90 shadow-md flex justify-between items-center transition group cursor-pointer">
                <div class="flex items-center gap-3.5 min-w-0">
                    <div class="w-8 h-8 rounded-xl bg-slate-900 flex items-center justify-center {data["color"]} shrink-0 shadow"><i class="fa-solid ${{c.icon}} text-sm"></i></div>
                    <strong class="text-white text-xs block group-hover:text-cyan-300 truncate font-bold">${{c.name}}</strong>
                </div>
                <i class="fa-solid fa-chevron-right text-[10px] text-slate-600 group-hover:{data["color"]} transition group-hover:translate-x-0.5 shrink-0 ml-2"></i>
            </button>
        `).join('');
    }}

    function renderBoutiqueGrid(items = boutiqueProducts) {{
        const container = document.getElementById("products-grid-container");
        const countTxt = document.getElementById("results-count-txt");
        if (countTxt) countTxt.innerText = `Mostrando ${{items.length}} artículos de entrega inmediata`;
        if (!container) return;

        container.innerHTML = items.map(p => {{
            const discountPct = p.original ? Math.round((1 - (p.precio / p.original)) * 100) : 0;
            return `
                <div class="w-[calc(50%-6px)] min-w-[155px] max-w-[210px] lg:w-auto lg:max-w-none shrink-0 snap-start bg-slate-950/90 hover:bg-slate-950 rounded-2xl p-3 flex flex-col justify-between transition group shadow-xl hover:shadow-[0_8px_30px_rgba(6,182,212,0.2)]">
                    <div>
                        <div class="w-full h-32 sm:h-40 overflow-hidden rounded-xl bg-slate-900 flex items-center justify-center p-2 relative mb-2 shadow-inner">
                            <img src="${{p.img}}" alt="${{p.nombre}}" class="w-full h-full object-contain group-hover:scale-105 transition duration-300" onerror="this.onerror=null; this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';" />
                            ${{discountPct > 0 ? `<span class="absolute top-1 left-1 bg-red-600 text-white text-[8px] font-mono font-black px-1.5 py-0.2 rounded shadow">-${{discountPct}}%</span>` : `<span class="absolute top-1 left-1 bg-amber-500/20 text-amber-300 text-[8px] font-mono font-black px-1.5 py-0.2 rounded">Directo</span>`}}
                        </div>
                        <span class="text-[8px] font-mono text-cyan-400 font-bold block truncate">${{p.marca}} &bull; ${{p.sku}}</span>
                        <h4 class="text-xs font-bold text-white mb-1 line-clamp-2 leading-snug group-hover:text-cyan-300 transition" title="${{p.nombre}}">${{p.nombre}}</h4>
                    </div>

                    <div>
                        <div class="pt-2 border-t border-slate-900 mb-2 flex flex-col">
                            ${{p.original ? `<span class="text-[9px] font-mono text-red-400 line-through">$${{p.original.toLocaleString('es-MX', {{ minimumFractionDigits: 2 }})}}</span>` : ''}}
                            <span class="text-sm sm:text-base font-black font-mono text-amber-400">$${{p.precio.toLocaleString('es-MX', {{ minimumFractionDigits: 2 }})}} <span class="text-[9px] text-amber-300/80 font-normal">MXN</span></span>
                        </div>

                        <div class="grid grid-cols-2 gap-1">
                            <button onclick="addToCartDirect('${{p.sku}}', 1)" class="bg-slate-900 hover:bg-slate-800 text-cyan-300 font-bold py-1.5 px-1 rounded-lg text-[10px] flex items-center justify-center gap-1 transition active:scale-95 shadow border border-cyan-500/30" title="Carrito">
                                <i class="fa-solid fa-cart-plus text-[10px]"></i> <span class="hidden sm:inline">Carrito</span>
                            </button>
                            <button onclick="buyNowDirect('${{p.sku}}')" class="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black py-1.5 px-1 rounded-lg text-[10px] flex items-center justify-center gap-1 transition active:scale-95 shadow" title="Comprar">
                                <i class="fa-solid fa-bolt text-[10px]"></i> <span class="hidden sm:inline">Comprar</span>
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }}).join('');
    }}

    function filterCategory(catName) {{
        const filtered = boutiqueProducts.filter(p => p.nombre.toLowerCase().includes(catName.toLowerCase()) || p.desc.toLowerCase().includes(catName.toLowerCase()));
        renderBoutiqueGrid(filtered.length > 0 ? filtered : boutiqueProducts);
    }}

    function onBoutiqueSearch(e) {{
        const q = e.target.value.toLowerCase().trim();
        const clearBtn = document.getElementById("clear-search-btn");
        if (clearBtn) clearBtn.classList.toggle("hidden", q.length === 0);
        const filtered = boutiqueProducts.filter(p => {{
            const searchStr = `${{p.sku}} ${{p.nombre}} ${{p.marca}} ${{p.desc}} ${{ (p.tokens || []).join(' ') }}`.toLowerCase();
            return searchStr.includes(q);
        }});
        renderBoutiqueAutocomplete(q, filtered);
        renderBoutiqueGrid(q ? filtered : boutiqueProducts);
    }}

    function renderBoutiqueAutocomplete(val, matches) {{
        const box = document.getElementById("boutique-autocomplete-box");
        if (!val || val.length < 1) {{ box.classList.add("hidden"); return; }}
        if (matches.length === 0) {{
            box.innerHTML = `<div class="p-3 text-center text-slate-400 text-xs">No hay coincidencias para "${{val}}"</div>`;
            box.classList.remove("hidden");
            return;
        }}
        box.innerHTML = matches.slice(0, 5).map(item => `
            <div class="bg-slate-950 rounded-xl p-2.5 flex items-center justify-between gap-2 border border-slate-800">
                <div class="min-w-0 flex-1">
                    <h5 class="text-xs font-bold text-white truncate">${{item.nombre}}</h5>
                    <span class="text-amber-400 font-mono font-bold text-xs">$${{item.precio.toFixed(2)}} MXN</span>
                </div>
                <button onclick="addToCartDirect('${{item.sku}}', 1)" class="bg-slate-800 text-cyan-300 p-1.5 rounded-lg text-xs border border-cyan-500/30"><i class="fa-solid fa-cart-plus"></i></button>
            </div>
        `).join('');
        box.classList.remove("hidden");
    }}

    function clearBoutiqueSearch() {{
        document.getElementById("boutiqueSearchInput").value = '';
        document.getElementById("clear-search-btn").classList.add("hidden");
        document.getElementById("boutique-autocomplete-box").classList.add("hidden");
        renderBoutiqueGrid(boutiqueProducts);
    }}

    function executeBoutiqueSearch() {{
        document.getElementById("boutique-autocomplete-box").classList.add("hidden");
    }}

    function addToCartDirect(sku, qty = 1) {{
        const item = boutiqueProducts.find(p => p.sku === sku);
        if (!item) return;
        let cartStorage = [];
        try {{
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cartStorage = JSON.parse(raw);
        }} catch(e) {{}}
        const exist = cartStorage.find(i => i.sku === sku);
        if (exist) {{ exist.quantity = (parseInt(exist.quantity) || 1) + qty; }}
        else {{ cartStorage.push({{ ...item, quantity: qty }}); }}
        localStorage.setItem('ecosystem_global_cart', JSON.stringify(cartStorage));
        syncBoutiqueCart();
        const badge = document.getElementById("boutique-cart-badge");
        if (badge) {{ badge.classList.remove("cart-pop"); void badge.offsetWidth; badge.classList.add("cart-pop"); }}
    }}

    function buyNowDirect(sku) {{
        addToCartDirect(sku, 1);
        window.location.href = "https://iaworldcenter-creator.github.io/pc-custom-lab/checkout.html";
    }}

    function syncBoutiqueCart() {{
        let cartStorage = [];
        try {{
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cartStorage = JSON.parse(raw);
        }} catch(e) {{}}
        const totalCount = cartStorage.reduce((sum, i) => sum + (parseInt(i.quantity) || 0), 0);
        const totalMoney = cartStorage.reduce((sum, i) => sum + ((parseFloat(i.precio) || 0) * (parseInt(i.quantity) || 0)), 0);
        const badge = document.getElementById("boutique-cart-badge");
        const totalTxt = document.getElementById("boutique-cart-total");
        if (badge) badge.innerText = totalCount;
        if (totalTxt) totalTxt.innerText = `$${{totalMoney.toLocaleString('es-MX', {{ minimumFractionDigits: 2 }})}} MXN`;
    }}

    function toggleCartDrawer() {{
        window.location.href = "https://iaworldcenter-creator.github.io/pc-custom-lab/checkout.html";
    }}

    document.addEventListener("DOMContentLoaded", () => {{
        updateAccountBadgeUI();
        renderBoutiqueSidebar();
        renderBoutiqueGrid();
        syncBoutiqueCart();
    }});
    window.addEventListener("storage", () => {{
        updateAccountBadgeUI();
        syncBoutiqueCart();
    }});
    </script>
</body>
</html>
"""

# 1. Actualizar las 7 Boutiques
all_dirs = os.listdir(BASE_DIR)
for key, b_info in boutiques_data.items():
    for d in all_dirs:
        if b_info["folder_pattern"].lower() in d.lower() and os.path.isdir(os.path.join(BASE_DIR, d)):
            target_path = os.path.join(BASE_DIR, d, "index.html")
            html_content = generate_boutique_html(b_info)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"✓ Boutique {d} actualizada con Botón Mi Cuenta y Modal de Cashback.")

            sub_repo = os.path.join(BASE_DIR, d)
            if os.path.exists(os.path.join(sub_repo, ".git")):
                subprocess.run(["git", "add", "-A"], cwd=sub_repo, check=True)
                subprocess.run(["git", "commit", "-m", "feat(account): modal de domicilio y cashback 5% en cabecera", "--allow-empty"], cwd=sub_repo, capture_output=True)
                res = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sub_repo, capture_output=True, text=True)
                print(f"   🟢 Submódulo {d} -> Push: {'OK' if res.returncode == 0 else res.stderr.strip()}")
            break

# 2. Reconstruir Portal Matriz
PORTAL_MATRIZ_HTML = f"""<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>BAZAR NFL.GDL | Ecosistema Comercial Pedro Moreno 501 A</title>
    <meta name="description" content="Hub central BAZAR NFL.GDL: 7 boutiques en Pedro Moreno 501 A, Guadalajara Centro. Registro de cuenta, 5% Cashback y Carrito Unificado." />
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />

    <style>
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
        .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
        .cart-pop {{ animation: popBadge 0.25s ease-in-out; }}
        @keyframes popBadge {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.35); }} 100% {{ transform: scale(1); }} }}
    </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen flex flex-col justify-between overflow-x-hidden selection:bg-cyan-500 selection:text-slate-950">

    <header class="bg-slate-900/95 backdrop-blur border-b border-slate-800 sticky top-0 z-50 shadow-2xl">
        <div class="max-w-[99%] 2xl:max-w-[1850px] mx-auto px-4 py-2 flex flex-wrap items-center justify-between gap-2 text-xs border-b border-slate-800/80">
            <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded bg-amber-500/10 border border-amber-500/30 text-amber-400 font-mono font-bold text-[10px] uppercase">
                    Envío Exprés El Mismo Día
                </span>
                <span class="text-slate-300 hidden xl:inline text-[11px] font-semibold">Guadalajara Centro • Carrito Unificado</span>
            </div>

            {NAV_BAR_HTML}

            <div class="flex items-center gap-3 font-bold text-[11px]">
                <a href="https://gemini.google.com" target="_blank" class="text-slate-300 hover:text-cyan-400 transition flex items-center gap-1">
                    <i class="fa-solid fa-wand-magic-sparkles text-cyan-400"></i> Gemini AI
                </a>
                <span class="text-slate-700">|</span>
                <a href="https://antigravity.google/download" target="_blank" class="text-slate-300 hover:text-amber-400 transition flex items-center gap-1">
                    <i class="fa-solid fa-download text-amber-400"></i> Anti-Gravity
                </a>
            </div>
        </div>

        <div class="max-w-[99%] 2xl:max-w-[1850px] mx-auto px-4 py-3 flex flex-col md:flex-row items-center justify-between gap-3">
            <div class="flex items-center justify-between w-full md:w-auto gap-3">
                <div class="flex items-center gap-3 cursor-pointer shrink-0" onclick="document.getElementById('pie-de-pagina').scrollIntoView({{ behavior: 'smooth' }});">
                    <div class="relative w-12 h-12 flex items-center justify-center">
                        <img src="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" alt="Logo Tigre BAZAR NFL.GDL" class="w-12 h-12 rounded-full object-cover border-2 border-amber-400 shadow-[0_0_15px_rgba(251,191,36,0.5)]" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';" />
                    </div>
                    <div class="flex flex-col">
                        <span class="font-black text-xl sm:text-2xl text-white tracking-wider uppercase leading-none">BAZAR NFL.GDL</span>
                        <span class="text-[10px] sm:text-[11px] font-mono text-cyan-400 uppercase tracking-tight mt-1 flex items-center gap-1">
                            <i class="fa-solid fa-location-dot text-amber-400"></i> Pedro Moreno 501 A
                        </span>
                    </div>
                </div>

                <!-- Botón de Mi Cuenta & 5% Cashback -->
                <button id="header-account-btn" onclick="toggleAccountModal()" class="cursor-pointer active:scale-95 transition shrink-0"></button>
            </div>

            <div class="flex-1 max-w-2xl w-full relative">
                <div class="flex items-center bg-white rounded-full border-2 border-cyan-400 shadow-[0_0_22px_rgba(6,182,212,0.4)] px-4 py-1.5 gap-2">
                    <i class="fa-solid fa-magnifying-glass text-slate-400 text-sm"></i>
                    <input type="text" id="masterSearchInput" autocomplete="off" spellcheck="false" placeholder="Busca, encuentra y compra rápido (ej. RAM Kingston, Marlboro, Paletas, Cohiba, Lentes)..." class="flex-1 bg-transparent border-0 outline-none text-slate-950 font-bold text-sm placeholder-slate-400" oninput="onMasterSearch(event)" />
                    <button onclick="clearMasterSearch()" id="clear-search-btn" class="hidden text-slate-400 hover:text-slate-600 text-xs px-2 font-bold cursor-pointer"><i class="fa-solid fa-xmark"></i></button>
                    <button onclick="executeMasterSearch()" class="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black px-6 py-2 rounded-full text-xs uppercase tracking-wider transition active:scale-95 shrink-0 shadow cursor-pointer">BUSCAR</button>
                </div>
                <div id="master-autocomplete-box" class="hidden absolute top-full left-0 right-0 mt-2 bg-slate-900 border-2 border-cyan-500/60 rounded-2xl shadow-2xl z-50 p-2.5 flex flex-col gap-2 max-h-96 overflow-y-auto no-scrollbar"></div>
            </div>

            <button onclick="toggleCartDrawer()" class="flex items-center gap-3 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white px-4 py-2.5 rounded-xl transition cursor-pointer active:scale-95 shadow shrink-0 group">
                <div class="relative">
                    <i class="fa-solid fa-cart-shopping text-cyan-400 text-base group-hover:scale-110 transition"></i>
                    <span id="portal-cart-badge" class="absolute -top-2.5 -right-2.5 bg-amber-500 text-slate-950 font-mono font-black text-[10px] rounded-full w-5 h-5 flex items-center justify-center shadow">0</span>
                </div>
                <div class="flex flex-col text-left">
                    <span class="text-[10px] font-mono text-slate-400 uppercase leading-none">Canasta Global</span>
                    <span id="portal-cart-total" class="text-xs font-mono font-bold text-amber-400">$0.00 MXN</span>
                </div>
            </button>
        </div>
    </header>

    <main class="w-full max-w-[99%] 2xl:max-w-[1850px] mx-auto px-2 sm:px-4 py-6 flex-1">
        <div class="flex flex-col lg:flex-row gap-8 items-start justify-center">
            
            <aside class="w-full lg:w-[340px] xl:w-[370px] shrink-0 bg-slate-900/90 rounded-3xl p-5 shadow-2xl relative" id="portal-sidebar-root">
                <div class="flex items-center justify-between border-b border-slate-800 pb-3.5 mb-3.5">
                    <h3 class="font-mono text-sm font-black text-white uppercase tracking-wider flex items-center gap-2 truncate">
                        <i class="fa-solid fa-layer-group text-amber-400"></i> Nuestras 7 Boutiques
                    </h3>
                </div>
                <div class="mb-3.5">
                    <span class="text-[10px] font-mono text-cyan-400 font-bold bg-cyan-950/40 border border-cyan-500/30 px-3 py-1 rounded-xl block text-center uppercase tracking-widest">
                        Compras Rápidas
                    </span>
                </div>

                <nav class="flex flex-col gap-2" id="sidebar-boutiques-list"></nav>

                {QR_CARD_HTML}

                <div class="mt-5 pt-5 border-t border-slate-800 flex flex-col gap-3">
                    <div class="bg-gradient-to-b from-slate-950 to-slate-900 border border-cyan-500/40 rounded-2xl p-4 flex flex-col gap-2 shadow-lg">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-wand-magic-sparkles text-cyan-400 text-sm"></i>
                            <span class="text-[10px] font-mono font-bold uppercase text-cyan-300">Creado por Google Gemini</span>
                        </div>
                        <p class="text-[11px] text-slate-300 leading-snug">Concebido y programado con la Inteligencia Artificial de Google Gemini.</p>
                        <a href="https://gemini.google.com" target="_blank" class="w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black py-2 rounded-xl text-xs text-center uppercase tracking-wider transition active:scale-95 shadow">Suscribirse a Gemini</a>
                    </div>
                    <div class="bg-gradient-to-b from-slate-950 to-slate-900 border border-amber-500/40 rounded-2xl p-4 flex flex-col gap-2 shadow-lg">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-robot text-amber-400 text-sm"></i>
                            <span class="text-[10px] font-mono font-bold uppercase text-amber-300">Desarrollado por Anti-Gravity</span>
                        </div>
                        <p class="text-[11px] text-slate-300 leading-snug">Desarrollado, compilado y desplegado por Anti-Gravity Copilot.</p>
                        <a href="https://antigravity.google/download" target="_blank" class="w-full bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black py-2 rounded-xl text-xs text-center uppercase tracking-wider transition active:scale-95 shadow">Bajar Anti-Gravity Gratis</a>
                    </div>
                </div>
            </aside>

            <!-- ESCAPARATE DE 7 SECCIONES CON CARRUSEL DE 2 PRODUCTOS EN MÓVIL + FLECHAS -->
            <section class="flex-1 w-full flex flex-col gap-8 min-w-0" id="showcase-container"></section>
        </div>
    </main>

    {ACCOUNT_MODAL_HTML}

    <footer class="bg-slate-950 border-t border-slate-900 pt-16 pb-8 text-slate-400 text-xs" id="pie-de-pagina">
        <div class="max-w-[99%] 2xl:max-w-[1850px] mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 pb-12 border-b border-slate-800/80">
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2"><i class="fa-solid fa-location-dot text-amber-400"></i> Contacto Local</h4>
                    <p class="flex items-start gap-2 text-slate-300"><i class="fa-solid fa-map-pin text-slate-500 mt-0.5 shrink-0"></i><span>Pedro Moreno 501 A, Guadalajara Centro, Jalisco (CP 44100)</span></p>
                    <p class="flex items-center gap-2"><i class="fa-solid fa-phone text-cyan-400 shrink-0"></i><span>Teléfono: <a href="tel:3336136348" class="text-slate-200 hover:text-cyan-400 font-mono">(33) 3613 6348</a></span></p>
                    <p class="flex items-center gap-2"><i class="fa-brands fa-whatsapp text-emerald-400 shrink-0 text-sm"></i><span>WhatsApp: <a href="https://wa.me/523337271440" target="_blank" class="text-slate-200 hover:text-emerald-400 font-mono">+52 33 3727 1440</a></span></p>
                </div>
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2"><i class="fa-solid fa-shield-halved text-cyan-400"></i> Políticas de Compra</h4>
                    <p class="text-[11px] text-slate-400">Devoluciones en tienda dentro de las 48 horas con empaque íntegro. Soporte técnico local y reemplazo inmediato.</p>
                </div>
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2"><i class="fa-solid fa-coins text-emerald-400"></i> Ahorro y Cashback</h4>
                    <p class="text-slate-300 font-bold">5% de Cashback en cada compra de forma directa.</p>
                </div>
            </div>
            <div class="pt-8 text-center text-slate-500 text-[11px]">
                <p>&copy; 2026 BAZAR NFL.GDL & Ecosistema Comercial Pedro Moreno 501 A. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>

    <script>
    const boutiquesConfig = [
        {{ id: "pc-custom", name: "PC Custom Lab", tag: "TECNOLOGÍA", icon: "fa-microchip", color: "text-cyan-400", desc: "Hardware esencial, GPUs NVIDIA RTX y procesadores.", url: "https://iaworldcenter-creator.github.io/pc-custom-lab/" }},
        {{ id: "viamx", name: "Vía MX Boutique", tag: "DEPARTAMENTAL", icon: "fa-gem", color: "text-cyan-300", desc: "Pantallas 4K, refrigeradores, laptops slim y electrónica.", url: "https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/" }},
        {{ id: "cigarros", name: "Cigarros Bazar", tag: "TABACOS", icon: "fa-smoking", color: "text-amber-400", desc: "Cigarros premium, puros habanos y encendedores selectos.", url: "https://iaworldcenter-creator.github.io/cigarros-bazar/" }},
        {{ id: "dulces", name: "Dulces Bazar", tag: "DULCERÍA", icon: "fa-candy-cane", color: "text-pink-400", desc: "Paletas payaso, mazapanes y confitería mexicana.", url: "https://iaworldcenter-creator.github.io/dulces-bazar/" }},
        {{ id: "kiosco", name: "Kiosco Digital", tag: "LECTURA", icon: "fa-newspaper", color: "text-indigo-400", desc: "Suscripciones digitales anuales a revistas y prensa.", url: "https://iaworldcenter-creator.github.io/kiosco-digital/" }},
        {{ id: "puesto", name: "Mi Puesto Bazar", tag: "NOVEDADES", icon: "fa-store", color: "text-emerald-400", desc: "Lentes con audio, consolas retro y cables de carga.", url: "https://iaworldcenter-creator.github.io/mi-puesto-bazar/" }},
        {{ id: "ofertas", name: "Ofertas & Liquidaciones", tag: "OUTLET B2B", icon: "fa-tags", color: "text-red-400", desc: "Excedentes de inventario y remates con hasta 50% de dto.", url: "https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/" }}
    ];

    const masterItems = [
        {{ sku: "PC-001", boutiqueId: "pc-custom", nombre: "Gabinete Micro-ATX con Fuente 500W Incluida", marca: "Acteck", precio: 1250.00, original: 1550.00, desc: "Chasis esbelto con fuente certificada y USB 3.0.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/gabinete_negro.webp", tokens: ["gabinete", "fuente", "pc"] }},
        {{ sku: "PC-002", boutiqueId: "pc-custom", nombre: "Tarjeta Madre ASUS Prime B760M-A WiFi DDR5", marca: "ASUS", precio: 3400.00, original: 3950.00, desc: "Soporte Intel 12va/13va/14va Gen y dual M.2.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/motherboard_asus.webp", tokens: ["tarjeta madre", "asus", "placa"] }},
        {{ sku: "PC-003", boutiqueId: "pc-custom", nombre: "Procesador Intel Core i5-14400F 10C/16T Disipador", marca: "Intel", precio: 4350.00, original: 4990.00, desc: "10 núcleos híbridos de alto desempeño.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/cpu_intel_ultra.webp", tokens: ["procesador", "cpu", "intel"] }},
        {{ sku: "PC-004", boutiqueId: "pc-custom", nombre: "Memoria RAM Kingston FURY Beast 16GB DDR5", marca: "Kingston", precio: 1250.00, original: 1500.00, desc: "Disipador de aluminio negro de bajo perfil.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/ram_caja.webp", tokens: ["ram", "kingston", "fury"] }},
        {{ sku: "PC-005", boutiqueId: "pc-custom", nombre: "Disco Sólido SSD Kingston NV2 1TB NVMe PCIe 4.0", marca: "Kingston", precio: 1350.00, original: 1650.00, desc: "3,500 MB/s lectura ultra rápida.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/disco_solido_m2.webp", tokens: ["ssd", "kingston", "nvme"] }},
        
        {{ sku: "VMX-001", boutiqueId: "viamx", nombre: "Pantalla Smart TV 55 Pulgadas 4K UHD HDR10+", marca: "Samsung", precio: 7999.00, original: 11499.00, desc: "Panel LED 4K con asistente de voz y HDMI 2.1.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_curvo_negro.webp", tokens: ["pantalla", "smart tv", "samsung"] }},
        {{ sku: "VMX-002", boutiqueId: "viamx", nombre: "Refrigerador Inverter No Frost 14 Pies Cúbicos", marca: "LG", precio: 11899.00, original: 15999.00, desc: "Doble puerta con compresor Inverter bajo consumo.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_warehouse_thumb.webp", tokens: ["refrigerador", "lg", "linea blanca"] }},
        {{ sku: "VMX-003", boutiqueId: "viamx", nombre: "Freidora de Aire Digital 6.5L con 12 Programas", marca: "Tefal", precio: 1499.00, original: 2199.00, desc: "Canastilla antiadherente con calor envolvente 360.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp", tokens: ["freidora", "aire", "airfryer"] }},

        {{ sku: "CIG-001", boutiqueId: "cigarros", nombre: "Cigarros Marlboro Gold Original (Cajetilla 20)", marca: "Marlboro", precio: 82.00, original: 95.00, desc: "Sabor suave y filtro blanco balanceado.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["cigarros", "marlboro", "gold"] }},
        {{ sku: "CIG-003", boutiqueId: "cigarros", nombre: "Puro Habanos Cohiba Siglo VI Tubo Individual", marca: "Cohiba", precio: 850.00, original: 1100.00, desc: "Puro cubano hecho a mano con notas amaderadas.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["puro", "cohiba", "siglo vi"] }},

        {{ sku: "DUL-001", boutiqueId: "dulces", nombre: "Paleta Payaso Ricolino (Caja 15 piezas)", marca: "Ricolino", precio: 245.00, original: 290.00, desc: "Malvavisco con chocolate y gomitas.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp", tokens: ["paleta", "payaso", "ricolino"] }},
        {{ sku: "DUL-002", boutiqueId: "dulces", nombre: "Mazapán De La Rosa Gigante (Caja 20 piezas)", marca: "De La Rosa", precio: 160.00, original: 195.00, desc: "Dulce tradicional de cacahuate tostado.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp", tokens: ["mazapan", "de la rosa"] }}
    ];

    {ACCOUNT_JS}

    function scrollCarousel(id, direction) {{
        const el = document.getElementById(id);
        if (el) {{
            const amount = el.clientWidth * 0.85;
            el.scrollBy({{ left: direction * amount, behavior: 'smooth' }});
        }}
    }}

    function renderSidebarBoutiques() {{
        const container = document.getElementById("sidebar-boutiques-list");
        if (!container) return;
        container.innerHTML = boutiquesConfig.map(b => `
            <button onclick="window.location.href='${{b.url}}'" class="w-full text-left p-3.5 rounded-2xl bg-slate-950/70 hover:bg-slate-800/90 shadow-md flex justify-between items-center transition group cursor-pointer">
                <div class="flex items-center gap-3.5 min-w-0">
                    <div class="w-8 h-8 rounded-xl bg-slate-900 flex items-center justify-center ${{b.color}} shrink-0 shadow"><i class="fa-solid ${{b.icon}} text-sm"></i></div>
                    <div class="min-w-0">
                        <strong class="text-white text-xs block group-hover:text-cyan-300 truncate font-bold">${{b.name}}</strong>
                        <span class="text-[10px] text-slate-400 block truncate font-medium">${{b.desc}}</span>
                    </div>
                </div>
                <i class="fa-solid fa-chevron-right text-[10px] text-slate-600 group-hover:${{b.color}} transition group-hover:translate-x-0.5 shrink-0 ml-2"></i>
            </button>
        `).join('');
    }}

    function renderShowcase() {{
        const container = document.getElementById("showcase-container");
        if (!container) return;

        container.innerHTML = boutiquesConfig.map(b => {{
            const products = masterItems.filter(p => p.boutiqueId === b.id);
            if (products.length === 0) return '';
            const carouselId = `carousel-${{b.id}}`;

            return `
                <div class="bg-slate-900/50 rounded-3xl p-5 shadow-2xl space-y-4">
                    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-slate-800/80 pb-3">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-xl bg-slate-950 flex items-center justify-center ${{b.color}} shadow"><i class="fa-solid ${{b.icon}} text-lg"></i></div>
                            <div>
                                <div class="flex items-center gap-2"><h3 class="text-base font-black text-white">${{b.name}}</h3><span class="text-[9px] font-mono font-bold uppercase px-2 py-0.5 rounded bg-slate-950 text-slate-300">${{b.tag}}</span></div>
                                <p class="text-xs text-slate-400 font-medium">${{b.desc}}</p>
                            </div>
                        </div>
                        <a href="${{b.url}}" class="text-xs font-mono font-bold text-cyan-400 hover:text-cyan-300 transition flex items-center gap-1.5 shrink-0 bg-slate-950 px-3.5 py-1.5 rounded-xl shadow">
                            <span>Ver todo en boutique</span> <i class="fa-solid fa-arrow-right text-[10px]"></i>
                        </a>
                    </div>

                    <div class="relative">
                        <button onclick="scrollCarousel('${{carouselId}}', -1)" class="lg:hidden absolute -left-2 top-1/2 -translate-y-1/2 z-20 w-8 h-8 rounded-full bg-slate-900 border border-cyan-400 text-cyan-300 flex items-center justify-center shadow-lg active:scale-90">
                            <i class="fa-solid fa-chevron-left text-xs"></i>
                        </button>

                        <div id="${{carouselId}}" class="flex flex-row overflow-x-auto flex-nowrap lg:grid lg:grid-cols-5 lg:overflow-visible gap-3 pb-3 lg:pb-0 no-scrollbar snap-x snap-mandatory scroll-smooth px-1">
                            ${{products.map(p => {{
                                const discountPct = p.original ? Math.round((1 - (p.precio / p.original)) * 100) : 0;
                                return `
                                    <div class="w-[calc(50%-6px)] min-w-[155px] max-w-[210px] lg:w-auto lg:max-w-none shrink-0 snap-start bg-slate-950/90 hover:bg-slate-950 rounded-2xl p-3 flex flex-col justify-between transition group shadow-xl hover:shadow-[0_8px_30px_rgba(6,182,212,0.2)]">
                                        <div>
                                            <div class="w-full h-32 sm:h-40 overflow-hidden rounded-xl bg-slate-900 flex items-center justify-center p-2 relative mb-2 shadow-inner">
                                                <img src="${{p.img}}" alt="${{p.nombre}}" class="w-full h-full object-contain group-hover:scale-105 transition duration-300" onerror="this.onerror=null; this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';" />
                                                ${{discountPct > 0 ? `<span class="absolute top-1 left-1 bg-red-600 text-white text-[8px] font-mono font-black px-1.5 py-0.2 rounded shadow">-${{discountPct}}%</span>` : `<span class="absolute top-1 left-1 bg-amber-500/20 text-amber-300 text-[8px] font-mono font-black px-1.5 py-0.2 rounded">Directo</span>`}}
                                            </div>
                                            <span class="text-[8px] font-mono text-cyan-400 font-bold block truncate">${{p.marca}} &bull; ${{p.sku}}</span>
                                            <h4 class="text-xs font-bold text-white mb-1 line-clamp-2 leading-snug group-hover:text-cyan-300 transition" title="${{p.nombre}}">${{p.nombre}}</h4>
                                        </div>

                                        <div>
                                            <div class="pt-2 border-t border-slate-900 mb-2 flex flex-col">
                                                ${{p.original ? `<span class="text-[9px] font-mono text-red-400 line-through">$${{p.original.toLocaleString('es-MX', {{ minimumFractionDigits: 2 }})}}</span>` : ''}}
                                                <span class="text-sm sm:text-base font-black font-mono text-amber-400">$${{p.precio.toLocaleString('es-MX', {{ minimumFractionDigits: 2 }})}} <span class="text-[9px] text-amber-300/80 font-normal">MXN</span></span>
                                            </div>

                                            <div class="grid grid-cols-2 gap-1">
                                                <button onclick="addToCartDirect('${{p.sku}}', 1)" class="bg-slate-900 hover:bg-slate-800 text-cyan-300 font-bold py-1.5 px-1 rounded-lg text-[10px] flex items-center justify-center gap-1 transition active:scale-95 shadow border border-cyan-500/30" title="Carrito">
                                                    <i class="fa-solid fa-cart-plus text-[10px]"></i> <span class="hidden sm:inline">Carrito</span>
                                                </button>
                                                <button onclick="buyNowDirect('${{p.sku}}')" class="bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black py-1.5 px-1 rounded-lg text-[10px] flex items-center justify-center gap-1 transition active:scale-95 shadow" title="Comprar">
                                                    <i class="fa-solid fa-bolt text-[10px]"></i> <span class="hidden sm:inline">Comprar</span>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                `;
                            }}).join('')}}
                        </div>

                        <button onclick="scrollCarousel('${{carouselId}}', 1)" class="lg:hidden absolute -right-2 top-1/2 -translate-y-1/2 z-20 w-8 h-8 rounded-full bg-slate-900 border border-cyan-400 text-cyan-300 flex items-center justify-center shadow-lg active:scale-90">
                            <i class="fa-solid fa-chevron-right text-xs"></i>
                        </button>
                    </div>
                </div>
            `;
        }}).join('');
    }}

    function searchMultiToken(query) {{
        if (!query || !query.trim()) return [];
        const q = query.toLowerCase().trim();
        const tokens = q.split(/\s+/).filter(t => t.length > 0);
        return masterItems.filter(item => {{
            const fullSearch = `${{item.sku}} ${{item.nombre}} ${{item.marca}} ${{item.desc}} ${{ (item.tokens || []).join(' ') }}`.toLowerCase();
            return tokens.every(token => fullSearch.includes(token));
        }});
    }}

    function onMasterSearch(e) {{
        const val = e.target.value;
        const clearBtn = document.getElementById("clear-search-btn");
        if (clearBtn) clearBtn.classList.toggle("hidden", val.length === 0);
        renderMasterAutocomplete(val);
    }}

    function renderMasterAutocomplete(val) {{
        const box = document.getElementById("master-autocomplete-box");
        if (!val || val.trim().length < 1) {{ box.classList.add("hidden"); return; }}
        const matches = searchMultiToken(val).slice(0, 6);
        if (matches.length === 0) {{
            box.innerHTML = `<div class="p-3 text-center text-slate-400 text-xs">No hay coincidencias para "${{val}}"</div>`;
            box.classList.remove("hidden");
            return;
        }}
        box.innerHTML = matches.map(item => `
            <div class="bg-slate-950 rounded-xl p-2.5 flex items-center justify-between gap-2 border border-slate-800">
                <div class="min-w-0 flex-1">
                    <span class="text-[9px] font-mono text-cyan-400 font-bold block">${{item.sku}} &bull; ${{item.marca}}</span>
                    <h5 class="text-xs font-bold text-white truncate">${{item.nombre}}</h5>
                    <span class="text-amber-400 font-mono font-bold text-xs">$${{item.precio.toFixed(2)}} MXN</span>
                </div>
                <div class="flex items-center gap-1.5 shrink-0">
                    <button onclick="addToCartDirect('${{item.sku}}', 1)" class="bg-slate-800 text-cyan-300 px-2.5 py-1 rounded-lg text-[10px] border border-cyan-500/30"><i class="fa-solid fa-cart-plus"></i></button>
                    <button onclick="buyNowDirect('${{item.sku}}')" class="bg-gradient-to-r from-amber-400 to-amber-500 text-slate-950 font-black px-3 py-1 rounded-lg text-[10px]">Comprar</button>
                </div>
            </div>
        `).join('');
        box.classList.remove("hidden");
    }}

    function clearMasterSearch() {{
        document.getElementById("masterSearchInput").value = '';
        document.getElementById("clear-search-btn").classList.add("hidden");
        document.getElementById("master-autocomplete-box").classList.add("hidden");
    }}

    function executeMasterSearch() {{
        document.getElementById("master-autocomplete-box").classList.add("hidden");
    }}

    function addToCartDirect(sku, qty = 1) {{
        const item = masterItems.find(p => p.sku === sku);
        if (!item) return;
        let cartStorage = [];
        try {{
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cartStorage = JSON.parse(raw);
        }} catch(e) {{}}
        const exist = cartStorage.find(i => i.sku === sku);
        if (exist) {{ exist.quantity = (parseInt(exist.quantity) || 1) + qty; }}
        else {{ cartStorage.push({{ ...item, quantity: qty }}); }}
        localStorage.setItem('ecosystem_global_cart', JSON.stringify(cartStorage));
        syncCartState();
        const badge = document.getElementById("portal-cart-badge");
        if (badge) {{ badge.classList.remove("cart-pop"); void badge.offsetWidth; badge.classList.add("cart-pop"); }}
    }}

    function buyNowDirect(sku) {{
        addToCartDirect(sku, 1);
        window.location.href = "https://iaworldcenter-creator.github.io/pc-custom-lab/checkout.html";
    }}

    function syncCartState() {{
        let cartStorage = [];
        try {{
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cartStorage = JSON.parse(raw);
        }} catch(e) {{}}
        const totalCount = cartStorage.reduce((sum, i) => sum + (parseInt(i.quantity) || 0), 0);
        const totalMoney = cartStorage.reduce((sum, i) => sum + ((parseFloat(i.precio) || 0) * (parseInt(i.quantity) || 0)), 0);
        const badge = document.getElementById("portal-cart-badge");
        const totalTxt = document.getElementById("portal-cart-total");
        if (badge) badge.innerText = totalCount;
        if (totalTxt) totalTxt.innerText = `$${{totalMoney.toLocaleString('es-MX', {{ minimumFractionDigits: 2 }})}} MXN`;
    }}

    function toggleCartDrawer() {{
        window.location.href = "https://iaworldcenter-creator.github.io/pc-custom-lab/checkout.html";
    }}

    document.addEventListener("DOMContentLoaded", () => {{
        updateAccountBadgeUI();
        renderSidebarBoutiques();
        renderShowcase();
        syncCartState();
    }});
    window.addEventListener("storage", () => {{
        updateAccountBadgeUI();
        syncCartState();
    }});
    </script>
</body>
</html>
"""

for p in [os.path.join(BASE_DIR, "index.html"), os.path.join(BASE_DIR, "sitios-web", "index.html")]:
    if os.path.exists(os.path.dirname(p)):
        with open(p, "w", encoding="utf-8") as f:
            f.write(PORTAL_MATRIZ_HTML)
        print(f"✓ Portal Matriz actualizado con Botón Mi Cuenta y Modal Cashback: {p}")

# 3. Actualizar App Móvil (app.html)
APP_HTML_CODE = f"""<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>BAZAR NFL App | Portal B2B & Cashback Pedro Moreno 501 A</title>
    
    <link rel="manifest" href="./manifest.json" />
    <meta name="theme-color" content="#0f172a" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    <link rel="apple-touch-icon" href="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" />

    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />

    <style>
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
        .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
        .cart-pop {{ animation: popBadge 0.25s ease-in-out; }}
        @keyframes popBadge {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.35); }} 100% {{ transform: scale(1); }} }}
    </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen flex flex-col justify-between selection:bg-cyan-500 selection:text-slate-950 pb-20 select-none">

    <!-- CABECERA MÓVIL CON MI CUENTA -->
    <header class="bg-slate-900/95 backdrop-blur border-b border-slate-800 sticky top-0 z-50 px-3 py-2.5 shadow-xl">
        <div class="max-w-md mx-auto flex items-center justify-between gap-2">
            <div class="flex items-center gap-2">
                <img src="https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp" alt="Logo Tigre App" class="w-9 h-9 rounded-full object-cover border border-amber-400" />
                <div>
                    <span class="font-black text-sm text-white block leading-none">BAZAR NFL</span>
                    <span class="text-[9px] font-mono text-cyan-400 block leading-tight">Pedro Moreno 501 A</span>
                </div>
            </div>

            <!-- Botón Mi Cuenta -->
            <button id="header-account-btn" onclick="toggleAccountModal()" class="cursor-pointer active:scale-95 transition"></button>

            <!-- Botón Canasta -->
            <button onclick="toggleCartModal()" class="relative bg-slate-800 border border-slate-700 p-2 rounded-xl text-cyan-400 active:scale-90 transition shadow">
                <i class="fa-solid fa-cart-shopping text-sm"></i>
                <span id="app-cart-badge" class="absolute -top-1.5 -right-1.5 bg-amber-500 text-slate-950 font-mono font-black text-[9px] rounded-full w-4 h-4 flex items-center justify-center shadow">0</span>
            </button>
        </div>
    </header>

    <main class="max-w-md mx-auto w-full px-3 py-3 space-y-3.5 flex-1">
        
        <!-- SÚPER-BUSCADOR -->
        <div class="relative">
            <div class="flex items-center bg-white rounded-2xl px-3.5 py-2 gap-2 shadow-lg border-2 border-cyan-400">
                <i class="fa-solid fa-magnifying-glass text-slate-400 text-sm"></i>
                <input type="text" id="mobileSearchInput" autocomplete="off" placeholder="Busca pieza, SKU o falla (ej. RAM, 4070, paleta)..." class="flex-1 bg-transparent border-0 outline-none text-slate-950 font-bold text-xs placeholder-slate-400" oninput="onMobileSearch(event)" />
                <button onclick="clearMobileSearch()" id="clear-search-btn" class="hidden text-slate-400 hover:text-slate-600 text-xs px-1 font-bold"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div id="mobile-autocomplete-box" class="hidden absolute top-full left-0 right-0 mt-2 bg-slate-900 border-2 border-cyan-500/60 rounded-2xl shadow-2xl z-40 p-2.5 flex flex-col gap-2 max-h-80 overflow-y-auto no-scrollbar"></div>
        </div>

        <!-- 7 BOUTIQUES -->
        <div class="space-y-2">
            <div class="flex justify-between items-center px-1">
                <span class="text-xs font-mono font-bold text-white uppercase flex items-center gap-1.5">
                    <i class="fa-solid fa-layer-group text-amber-400"></i> Nuestras 7 Boutiques
                </span>
                <span class="text-[9px] font-mono text-cyan-400 font-bold">Toca para ver top 3</span>
            </div>
            <div class="grid grid-cols-1 gap-2" id="boutiques-accordion-list"></div>
        </div>

        <!-- CARRUSEL 2 PRODUCTOS CON FLECHAS -->
        <div class="space-y-2 pt-1">
            <div class="flex justify-between items-center px-1">
                <span class="text-xs font-mono font-bold text-slate-400 uppercase">Catálogo de Entrega Inmediata</span>
                <span class="text-[10px] font-mono text-cyan-400 font-bold">Desliza a los lados &rarr;</span>
            </div>

            <div class="relative">
                <button onclick="scrollCarousel('mobile-product-carousel', -1)" class="absolute -left-2 top-1/2 -translate-y-1/2 z-20 w-7 h-7 rounded-full bg-slate-900/95 border border-cyan-400 text-cyan-300 flex items-center justify-center shadow-lg active:scale-90">
                    <i class="fa-solid fa-chevron-left text-[10px]"></i>
                </button>
                
                <div id="mobile-product-carousel" class="flex flex-row overflow-x-auto flex-nowrap gap-2.5 pb-2 no-scrollbar snap-x snap-mandatory scroll-smooth px-1">
                </div>

                <button onclick="scrollCarousel('mobile-product-carousel', 1)" class="absolute -right-2 top-1/2 -translate-y-1/2 z-20 w-7 h-7 rounded-full bg-slate-900/95 border border-cyan-400 text-cyan-300 flex items-center justify-center shadow-lg active:scale-90">
                    <i class="fa-solid fa-chevron-right text-[10px]"></i>
                </button>
            </div>
        </div>

    </main>

    <!-- BARRA INFERIOR -->
    <nav class="fixed bottom-0 left-0 right-0 bg-slate-900/98 backdrop-blur border-t border-slate-800 px-6 py-2.5 z-40">
        <div class="max-w-md mx-auto flex items-center justify-between text-xs font-bold">
            <a href="https://iaworldcenter-creator.github.io/sitios-web/" class="flex flex-col items-center gap-1 text-slate-400 hover:text-amber-400 transition">
                <i class="fa-solid fa-house text-base"></i><span class="text-[9px] font-mono">Matriz</span>
            </a>
            <button onclick="toggleAccountModal()" class="flex flex-col items-center gap-1 text-emerald-400">
                <i class="fa-solid fa-user-check text-base"></i><span class="text-[9px] font-mono">Mi Cuenta</span>
            </button>
            <a href="https://wa.me/523337271440" target="_blank" class="flex flex-col items-center gap-1 text-cyan-400">
                <i class="fa-brands fa-whatsapp text-base"></i><span class="text-[9px] font-mono">Atención</span>
            </a>
            <button onclick="toggleCartModal()" class="flex flex-col items-center gap-1 text-amber-400">
                <i class="fa-solid fa-bag-shopping text-base"></i><span class="text-[9px] font-mono">Mi Pedido</span>
            </button>
        </div>
    </nav>

    {ACCOUNT_MODAL_HTML}

    <!-- MODAL DE CHECKOUT -->
    <div id="appCartModal" class="fixed inset-0 z-50 hidden">
        <div class="absolute inset-0 bg-slate-950/80 backdrop-blur-sm" onclick="toggleCartModal()"></div>
        <div class="absolute bottom-0 left-0 right-0 max-w-md mx-auto bg-slate-900 border-t-2 border-emerald-400 rounded-t-3xl p-5 shadow-2xl flex flex-col justify-between max-h-[90vh] z-10">
            <div>
                <div class="flex justify-between items-center border-b border-slate-800 pb-3 mb-3">
                    <h3 class="font-black text-white text-sm flex items-center gap-2">
                        <i class="fa-solid fa-receipt text-cyan-400"></i> Despacho con Pago Previo SPEI
                    </h3>
                    <button onclick="toggleCartModal()" class="text-slate-400 hover:text-white p-1"><i class="fa-solid fa-xmark text-lg"></i></button>
                </div>
                <div id="modal-cart-items" class="flex flex-col gap-2 overflow-y-auto max-h-[25vh] pr-1 no-scrollbar"></div>
                <div class="mt-3 p-3 bg-slate-950 rounded-2xl border border-emerald-500/40 flex items-center justify-between">
                    <div>
                        <span class="text-[9px] font-mono text-emerald-400 uppercase font-bold block">PIN de Entrega Uber:</span>
                        <span id="delivery-pin-display" class="text-xl font-mono font-black text-white tracking-widest">----</span>
                    </div>
                    <span class="text-[9px] text-slate-400 max-w-[150px] text-right">Díctalo al chofer para recibir el paquete.</span>
                </div>
                <div class="mt-3 p-3 bg-slate-950 rounded-2xl border border-slate-800 space-y-1 text-xs font-mono">
                    <div class="flex justify-between items-center"><span class="text-slate-400 text-[10px]">Banco:</span><strong class="text-white text-[11px]">BBVA México / STP</strong></div>
                    <div class="flex justify-between items-center"><span class="text-slate-400 text-[10px]">CLABE:</span><span class="text-cyan-300 font-bold text-[11px]">0123 2001 5824 9382 10</span></div>
                </div>
            </div>
            <div class="border-t border-slate-800 pt-3 space-y-2 mt-3">
                <div class="flex justify-between text-xs font-mono"><span class="text-slate-400">Subtotal:</span><span id="modal-subtotal-txt" class="text-white font-bold">$0.00 MXN</span></div>
                <div class="flex justify-between text-xs font-mono"><span class="text-slate-400">Flete Cotizado:</span><span id="modal-shipping-txt" class="text-amber-400 font-bold">$35.00 MXN</span></div>
                <div class="flex justify-between text-sm font-mono pt-1 border-t border-slate-800"><strong class="text-white">Total SPEI:</strong><strong id="modal-total-txt" class="text-emerald-400 font-black text-base">$0.00 MXN</strong></div>
                <button onclick="sendOrderViaWhatsApp()" class="w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 text-slate-950 font-black py-3 rounded-2xl text-xs uppercase tracking-wider transition active:scale-95 shadow-lg flex items-center justify-center gap-2 cursor-pointer">
                    <i class="fa-brands fa-whatsapp text-sm text-slate-950"></i> Mandar Comprobante SPEI & Despachar
                </button>
            </div>
        </div>
    </div>

    <script>
    const boutiquesConfig = [
        {{ id: "pc-custom", name: "PC Custom Lab", tag: "HARDWARE & PC", icon: "fa-microchip", color: "text-cyan-400", url: "https://iaworldcenter-creator.github.io/pc-custom-lab/" }},
        {{ id: "viamx", name: "Vía MX Boutique", tag: "DEPARTAMENTAL", icon: "fa-gem", color: "text-cyan-300", url: "https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/" }},
        {{ id: "cigarros", name: "Cigarros Bazar", tag: "TABACOS & PUROS", icon: "fa-smoking", color: "text-amber-400", url: "https://iaworldcenter-creator.github.io/cigarros-bazar/" }},
        {{ id: "dulces", name: "Dulces Bazar", tag: "DULCERÍA & BOTANAS", icon: "fa-candy-cane", color: "text-pink-400", url: "https://iaworldcenter-creator.github.io/dulces-bazar/" }},
        {{ id: "kiosco", name: "Kiosco Digital", tag: "REVISTAS & PRENSA", icon: "fa-newspaper", color: "text-indigo-400", url: "https://iaworldcenter-creator.github.io/kiosco-digital/" }},
        {{ id: "puesto", name: "Mi Puesto Bazar", tag: "NOVEDADES & GADGETS", icon: "fa-store", color: "text-emerald-400", url: "https://iaworldcenter-creator.github.io/mi-puesto-bazar/" }},
        {{ id: "ofertas", name: "Ofertas & Liquidaciones", tag: "OUTLET DIRECTO B2B", icon: "fa-tags", color: "text-red-400", url: "https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/" }}
    ];

    const appProducts = [
        {{ sku: "PC-001", boutiqueId: "pc-custom", nombre: "Gabinete Micro-ATX con Fuente 500W", marca: "Acteck", precio: 1250.00, original: 1550.00, desc: "Fuente certificada, USB 3.0 para taller.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/gabinete_negro.webp", tokens: ["gabinete", "fuente", "pc"] }},
        {{ sku: "PC-002", boutiqueId: "pc-custom", nombre: "Tarjeta Madre ASUS Prime B760M-A WiFi DDR5", marca: "ASUS", precio: 3400.00, original: 3950.00, desc: "Soporte Intel 12va/13va/14va Gen, dual M.2.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/motherboard_asus.webp", tokens: ["tarjeta madre", "asus", "placa"] }},
        {{ sku: "PC-004", boutiqueId: "pc-custom", nombre: "RAM Kingston FURY Beast 16GB DDR5 5600MHz", marca: "Kingston", precio: 1250.00, original: 1500.00, desc: "Disipador de aluminio de bajo perfil.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/ram_caja.webp", tokens: ["ram", "kingston", "fury", "ddr5"] }},
        {{ sku: "PC-005", boutiqueId: "pc-custom", nombre: "SSD Kingston NV2 1TB NVMe PCIe 4.0", marca: "Kingston", precio: 1350.00, original: 1650.00, desc: "3,500 MB/s lectura ultra rápida.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/disco_solido_m2.webp", tokens: ["ssd", "kingston", "nvme", "disco"] }},
        {{ sku: "VMX-001", boutiqueId: "viamx", nombre: "Pantalla Smart TV 55 Pulgadas 4K UHD", marca: "Samsung", precio: 7999.00, original: 11499.00, desc: "Panel LED 4K con asistente de voz.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_curvo_negro.webp", tokens: ["pantalla", "smart tv", "samsung"] }},
        {{ sku: "CIG-001", boutiqueId: "cigarros", nombre: "Cigarros Marlboro Gold Original (20)", marca: "Marlboro", precio: 82.00, original: 95.00, desc: "Sabor suave de importación.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["cigarros", "marlboro"] }},
        {{ sku: "DUL-001", boutiqueId: "dulces", nombre: "Paleta Payaso Ricolino (Caja 15 piezas)", marca: "Ricolino", precio: 245.00, original: 290.00, desc: "Malvavisco con chocolate y gomitas.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp", tokens: ["paleta", "dulces"] }},
        {{ sku: "PUE-001", boutiqueId: "puesto", nombre: "Lentes Inteligentes Bluetooth con Audio", marca: "SmartVision", precio: 680.00, original: 950.00, desc: "Llamadas y música con protección UV.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_gamer_thumb.webp", tokens: ["lentes", "bluetooth"] }}
    ];

    let generatedPIN = "";
    let activeBoutiqueId = null;

    {ACCOUNT_JS}

    function scrollCarousel(id, direction) {{
        const el = document.getElementById(id);
        if (el) {{
            const amount = el.clientWidth * 0.85;
            el.scrollBy({{ left: direction * amount, behavior: 'smooth' }});
        }}
    }}

    function renderMobileList(items = appProducts) {{
        const container = document.getElementById("mobile-product-carousel");
        if (!container) return;

        container.innerHTML = items.map(p => {{
            const discountPct = p.original ? Math.round((1 - (p.precio / p.original)) * 100) : 0;
            return `
                <div class="w-[calc(50%-5px)] min-w-[155px] max-w-[185px] shrink-0 snap-start bg-slate-900 border border-slate-800 rounded-2xl p-2.5 flex flex-col justify-between shadow-md">
                    <div>
                        <div class="w-full h-32 overflow-hidden rounded-xl bg-slate-950 flex items-center justify-center p-1.5 relative mb-2 shadow-inner">
                            <img src="${{p.img}}" alt="${{p.nombre}}" class="w-full h-full object-contain" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';" />
                            ${{discountPct > 0 ? `<span class="absolute top-1 left-1 bg-red-600 text-white text-[8px] font-mono font-bold px-1.5 py-0.2 rounded">-${{discountPct}}%</span>` : ''}}
                        </div>
                        <span class="text-[8px] font-mono text-cyan-400 font-bold block truncate">${{p.marca}} &bull; ${{p.sku}}</span>
                        <h4 class="text-xs font-bold text-white line-clamp-2 leading-snug mt-0.5" title="${{p.nombre}}">${{p.nombre}}</h4>
                    </div>

                    <div class="pt-1.5 border-t border-slate-800/80 mt-1.5 space-y-1.5">
                        <div class="flex flex-col">
                            ${{p.original ? `<span class="text-[9px] font-mono text-red-400 line-through">$${{p.original.toFixed(2)}}</span>` : ''}}
                            <span class="text-amber-400 font-mono font-black text-xs">$${{p.precio.toFixed(2)}}</span>
                        </div>
                        <div class="grid grid-cols-2 gap-1">
                            <button onclick="addToCartApp('${{p.sku}}')" class="bg-slate-800 text-cyan-300 p-1.5 rounded-lg text-[10px] flex items-center justify-center shadow border border-cyan-500/30 active:scale-90" title="Agregar">
                                <i class="fa-solid fa-cart-plus"></i>
                            </button>
                            <button onclick="buyNowApp('${{p.sku}}')" class="bg-gradient-to-r from-amber-400 to-amber-500 text-slate-950 font-black p-1.5 rounded-lg text-[10px] flex items-center justify-center shadow active:scale-90">
                                Comprar
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }}).join('');
    }}

    function renderBoutiquesAccordions() {{
        const container = document.getElementById("boutiques-accordion-list");
        if (!container) return;

        container.innerHTML = boutiquesConfig.map(b => {{
            const top3 = appProducts.filter(p => p.boutiqueId === b.id).slice(0, 3);
            const isOpen = activeBoutiqueId === b.id;

            return `
                <div class="bg-slate-900 border ${{isOpen ? 'border-cyan-400' : 'border-slate-800'}} rounded-2xl overflow-hidden shadow-md">
                    <button onclick="toggleBoutique('${{b.id}}')" class="w-full text-left p-3 flex items-center justify-between gap-3 bg-slate-950/60 hover:bg-slate-800/80 transition cursor-pointer">
                        <div class="flex items-center gap-2.5 min-w-0">
                            <div class="w-8 h-8 rounded-xl bg-slate-900 flex items-center justify-center ${{b.color}} shrink-0 shadow"><i class="fa-solid ${{b.icon}} text-sm"></i></div>
                            <div class="min-w-0">
                                <strong class="text-xs font-bold text-white block truncate">${{b.name}}</strong>
                                <span class="text-[9px] font-mono text-slate-400 block truncate">${{b.tag}}</span>
                            </div>
                        </div>
                        <div class="flex items-center gap-2 shrink-0">
                            <span class="text-[9px] font-mono font-bold text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded-lg border border-cyan-500/30">Top 3</span>
                            <i class="fa-solid fa-chevron-${{isOpen ? 'up' : 'down'}} text-slate-500 text-xs"></i>
                        </div>
                    </button>

                    ${{isOpen ? `
                        <div class="p-3 bg-slate-950 border-t border-slate-800/80 space-y-2">
                            ${{top3.map(p => `
                                <div class="bg-slate-900 rounded-xl p-2 flex items-center justify-between gap-2 border border-slate-800">
                                    <img src="${{p.img}}" alt="${{p.nombre}}" class="w-10 h-10 object-contain rounded bg-slate-950 p-0.5 shrink-0" onerror="this.src='https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp';" />
                                    <div class="min-w-0 flex-1">
                                        <h5 class="text-xs font-bold text-white line-clamp-1">${{p.nombre}}</h5>
                                        <span class="text-amber-400 font-mono font-black text-xs">$${{p.precio.toFixed(2)}}</span>
                                    </div>
                                    <button onclick="addToCartApp('${{p.sku}}')" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 p-2 rounded-lg text-xs border border-cyan-500/30"><i class="fa-solid fa-cart-plus"></i></button>
                                </div>
                            `).join('')}}
                            <div class="pt-1 text-center">
                                <a href="${{b.url}}" class="text-[11px] font-mono font-bold text-cyan-400 hover:underline">Ir a boutique completa &rarr;</a>
                            </div>
                        </div>
                    ` : ''}}
                </div>
            `;
        }}).join('');
    }}

    function toggleBoutique(id) {{
        activeBoutiqueId = activeBoutiqueId === id ? null : id;
        renderBoutiquesAccordions();
    }}

    function onMobileSearch(e) {{
        const q = e.target.value.toLowerCase().trim();
        const box = document.getElementById("mobile-autocomplete-box");
        const clearBtn = document.getElementById("clear-search-btn");
        if (clearBtn) clearBtn.classList.toggle("hidden", q.length === 0);

        if (!q) {{ box.classList.add("hidden"); return; }}
        const matches = appProducts.filter(p => `${{p.sku}} ${{p.nombre}} ${{p.desc}} ${{(p.tokens||[]).join(' ')}}`.toLowerCase().includes(q));

        if (matches.length === 0) {{
            const best = appProducts.slice(0, 3);
            box.innerHTML = `
                <div class="p-2 space-y-1.5 text-xs text-center">
                    <span class="text-white font-bold block">No hay coincidencias para "${{q}}"</span>
                    <span class="text-[10px] text-amber-400 font-mono block">Te recomendamos los más pedidos:</span>
                    ${{best.map(i => `
                        <div class="bg-slate-950 p-2 rounded-xl flex justify-between items-center text-left">
                            <span class="truncate max-w-[180px] text-white font-bold">${{i.nombre}}</span>
                            <button onclick="addToCartApp('${{i.sku}}')" class="bg-emerald-600 text-slate-950 font-black px-2 py-0.5 rounded text-[10px]">+1 Clic</button>
                        </div>
                    `).join('')}}
                </div>
            `;
            box.classList.remove("hidden");
            return;
        }}

        box.innerHTML = matches.slice(0, 5).map(item => `
            <div class="bg-slate-950 rounded-xl p-2 flex items-center justify-between gap-2 border border-slate-800">
                <div class="min-w-0 flex-1">
                    <h5 class="text-xs font-bold text-white truncate">${{item.nombre}}</h5>
                    <span class="text-amber-400 font-mono font-bold text-xs">$${{item.precio.toFixed(2)}}</span>
                </div>
                <button onclick="addToCartApp('${{item.sku}}')" class="bg-slate-800 text-cyan-300 p-1.5 rounded-lg text-xs border border-cyan-500/30"><i class="fa-solid fa-cart-plus"></i></button>
            </div>
        `).join('');
        box.classList.remove("hidden");
    }}

    function clearMobileSearch() {{
        document.getElementById("mobileSearchInput").value = '';
        document.getElementById("clear-search-btn").classList.add("hidden");
        document.getElementById("mobile-autocomplete-box").classList.add("hidden");
    }}

    function generatePIN() {{
        generatedPIN = Math.floor(1000 + Math.random() * 9000).toString();
        const el = document.getElementById("delivery-pin-display");
        if (el) el.innerText = generatedPIN;
    }}

    function addToCartApp(sku) {{
        const item = appProducts.find(p => p.sku === sku);
        if (!item) return;
        let cart = [];
        try {{
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cart = JSON.parse(raw);
        }} catch(e) {{}}
        const exist = cart.find(i => i.sku === sku);
        if (exist) {{ exist.quantity = (parseInt(exist.quantity) || 1) + 1; }}
        else {{ cart.push({{ ...item, quantity: 1 }}); }}
        localStorage.setItem('ecosystem_global_cart', JSON.stringify(cart));
        syncAppCart();
        const badge = document.getElementById("app-cart-badge");
        if (badge) {{ badge.classList.remove("cart-pop"); void badge.offsetWidth; badge.classList.add("cart-pop"); }}
    }}

    function buyNowApp(sku) {{
        addToCartApp(sku);
        toggleCartModal();
    }}

    function syncAppCart() {{
        let cart = [];
        try {{
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cart = JSON.parse(raw);
        }} catch(e) {{}}
        const count = cart.reduce((sum, i) => sum + (parseInt(i.quantity) || 0), 0);
        const subtotal = cart.reduce((sum, i) => sum + ((parseFloat(i.precio) || 0) * (parseInt(i.quantity) || 0)), 0);
        
        const profile = getSavedProfile();
        const shippingRate = profile && profile.rate ? profile.rate : 35;
        const isFree = subtotal >= 1500 || count >= 10;
        const shippingFinal = isFree ? 0 : (subtotal > 0 ? shippingRate : 0);
        const total = subtotal + shippingFinal;

        document.getElementById("app-cart-badge").innerText = count;
        document.getElementById("modal-subtotal-txt").innerText = `$${{subtotal.toFixed(2)}} MXN`;
        document.getElementById("modal-shipping-txt").innerText = isFree ? "GRATIS ($0.00)" : `$${{shippingFinal.toFixed(2)}} MXN`;
        document.getElementById("modal-total-txt").innerText = `$${{total.toFixed(2)}} MXN`;

        const container = document.getElementById("modal-cart-items");
        if (!container) return;
        if (cart.length === 0) {{
            container.innerHTML = '<div class="text-center py-6 text-slate-500 text-xs">Sin artículos en la orden.</div>';
            return;
        }}
        container.innerHTML = cart.map(i => `
            <div class="bg-slate-950 p-2 rounded-xl border border-slate-800 flex justify-between items-center text-xs">
                <span class="text-white truncate max-w-[180px]">${{i.nombre}} (x${{i.quantity}})</span>
                <span class="text-amber-400 font-mono font-bold">$${{(parseFloat(i.precio)*parseInt(i.quantity)).toFixed(2)}}</span>
            </div>
        `).join('');
    }}

    function toggleCartModal() {{
        generatePIN();
        document.getElementById("appCartModal").classList.toggle("hidden");
        syncAppCart();
    }}

    function sendOrderViaWhatsApp() {{
        let cart = [];
        try {{
            const raw = localStorage.getItem('ecosystem_global_cart');
            if (raw) cart = JSON.parse(raw);
        }} catch(e) {{}}
        if (cart.length === 0) {{ alert('Agrega al menos un artículo a tu orden.'); return; }}

        const profile = getSavedProfile();
        if (!profile || !profile.isComplete) {{
            alert('Por favor registra primero tu domicilio en "Mi Cuenta" para activar tu 5% de Cashback y habilitar entrega Uber Flash.');
            toggleAccountModal();
            return;
        }}

        const subtotal = cart.reduce((sum, i) => sum + ((parseFloat(i.precio) || 0) * (parseInt(i.quantity) || 0)), 0);
        const shipping = subtotal >= 1500 ? 0 : profile.rate;
        const total = subtotal + shipping;

        let msg = `🛵 *ORDEN DESPACHO UBER FLASH - BAZAR NFL*%0A`;
        msg += `👤 *Cliente:* ${{profile.name}} (${{profile.phone}})%0A`;
        msg += `📍 *Origen:* Pedro Moreno 501 A, GDL Centro%0A`;
        msg += `🏠 *Destino:* ${{profile.calle}} #${{profile.num}}, Col. ${{profile.colonia}}, CP ${{profile.cp}}, ${{profile.municipio.toUpperCase()}}%0A`;
        if (profile.ref) msg += `📌 *Ref:* ${{profile.ref}}%0A`;
        msg += `🔐 *PIN Uber:* ${{generatedPIN}}%0A`;
        msg += `🎁 *Cashback Activo:* 5%%0A%0A`;
        msg += `📦 *PRODUCTOS:*%0A`;
        cart.forEach(i => {{
            msg += `• *${{i.quantity}}x* ${{i.nombre}} ($${{(parseFloat(i.precio)*parseInt(i.quantity)).toFixed(2)}})%0A`;
        }});
        msg += `%0A💵 *Subtotal:* $${{subtotal.toFixed(2)}} MXN`;
        msg += `%0A🛵 *Flete Uber Flash:* ${{shipping === 0 ? 'GRATIS' : '$' + shipping.toFixed(2) + ' MXN'}}`;
        msg += `%0A💰 *TOTAL SPEI:* $${{total.toFixed(2)}} MXN%0A%0A`;
        msg += `_Adjunto comprobante de pago bancario para enviar la moto._`;

        window.open(`https://wa.me/523337271440?text=${{msg}}`, '_blank');
    }}

    document.addEventListener("DOMContentLoaded", () => {{
        updateAccountBadgeUI();
        renderMobileList();
        renderBoutiquesAccordions();
        syncAppCart();
    }});
    </script>
</body>
</html>
"""

for p in [os.path.join(BASE_DIR, "app.html"), os.path.join(BASE_DIR, "sitios-web", "app.html")]:
    if os.path.exists(os.path.dirname(p)):
        with open(p, "w", encoding="utf-8") as f:
            f.write(APP_HTML_CODE)
        print(f"✓ App móvil actualizada con Botón Mi Cuenta y Modal Cashback: {p}")

# Desplegar cambios a GitHub Pages
print("\n=== DESPLEGANDO CAMBIOS A GITHUB PAGES ===")
sitios_repo = os.path.join(BASE_DIR, "sitios-web")
if os.path.exists(os.path.join(sitios_repo, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=sitios_repo, check=True)
    subprocess.run(["git", "commit", "-m", "feat(account): modal universal de cuenta, domicilio y cashback 5%", "--allow-empty"], cwd=sitios_repo, capture_output=True)
    res_sub = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sitios_repo, capture_output=True, text=True)
    print(f"🟢 Submódulo sitios-web -> Push: {'OK' if res_sub.returncode == 0 else res_sub.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(ecosistema): cabecera limpia con boton Mi Cuenta, modal de domicilio y cashback 5%", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
