import os
import subprocess
import json
import urllib.parse

BASE_DIR = r"E:\sitios web"
APP_URL = "https://iaworldcenter-creator.github.io/sitios-web/app.html"

print("=" * 80)
print("INTEGRANDO LAS 7 BOUTIQUES COMPLETAS CON 5 PRODUCTOS CADA UNA EN EL PORTAL MATRIZ")
print("=" * 80)

# Barra de navegación universal
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

# Tarjeta persuasiva de código QR
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

# Modal de Cuenta y Domicilio para 5% Cashback
ACCOUNT_MODAL_HTML = """
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

        <div class="p-3 bg-gradient-to-r from-emerald-950/60 to-slate-950 border border-emerald-500/40 rounded-2xl space-y-1">
            <div class="flex items-center gap-2 text-emerald-400 text-xs font-bold font-mono">
                <i class="fa-solid fa-coins text-sm"></i>
                <span>5% DE CASHBACK EN CADA PEDIDO</span>
            </div>
            <p class="text-[11px] text-slate-300 leading-tight">
                <strong>Importante:</strong> Llena tus datos completos para activar tu <strong>5% de Cashback acumulable</strong> y habilitar entregas con Uber Flash.
            </p>
        </div>

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
                    <input type="text" id="accColonia" placeholder="Ej. Centro, Americana..." class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white outline-none focus:border-cyan-400 font-medium" />
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
                <label class="text-[10px] font-mono text-slate-400 font-bold block mb-1">Referencias de Entrega:</label>
                <input type="text" id="accRef" placeholder="Ej. Fachada gris, portón blanco" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white outline-none focus:border-cyan-400 font-medium" />
            </div>

            <div id="accAlertBox" class="hidden p-3 rounded-xl text-xs font-mono leading-tight"></div>
        </div>

        <div class="pt-2 border-t border-slate-800">
            <button onclick="saveUserProfile()" class="w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 text-slate-950 font-black py-3 rounded-xl text-xs uppercase tracking-wider transition active:scale-95 shadow-lg flex items-center justify-center gap-2 cursor-pointer">
                <i class="fa-solid fa-floppy-disk text-sm"></i> <span>Guardar Domicilio & Activar Cashback</span>
            </button>
        </div>

    </div>
</div>
"""

# JavaScript de gestión de cuenta
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
    if (!modal.classList.contains("hidden")) { loadProfileIntoModal(); }
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
        alertBox.innerHTML = '🎉 <strong>¡Felicidades!</strong> Tu perfil está completo y tienes <strong>5% de Cashback activo</strong>.';
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

    const profile = { name, phone, email, cp, calle, num, colonia, municipio, ref, rate, dist, isComplete: true, updatedAt: new Date().toISOString() };
    localStorage.setItem('bazar_user_profile', JSON.stringify(profile));
    updateAccountBadgeUI();

    alertBox.className = "p-3 rounded-xl text-xs font-mono leading-tight bg-emerald-950/60 border border-emerald-500/50 text-emerald-300 block";
    alertBox.innerHTML = '🎉 <strong>¡Domicilio Guardado!</strong> 5% de Cashback activo. Flete estimado: <strong>$' + rate.toFixed(2) + ' MXN</strong>.';
    setTimeout(() => { toggleAccountModal(); }, 1200);
}
"""

# Portal Matriz con 7 Boutiques x 5 Productos (35 productos en total)
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

            <!-- ESCAPARATE DE LAS 7 BOUTIQUES COMPLETAS -->
            <section class="flex-1 w-full flex flex-col gap-8 min-w-0" id="showcase-container"></section>
        </div>
    </main>

    {ACCOUNT_MODAL_HTML}

    <footer class="bg-slate-950 border-t border-slate-900 pt-16 pb-8 text-slate-400 text-xs" id="pie-de-pagina">
        <div class="max-w-[99%] 2xl:max-w-[1850px] mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 pb-12 border-b border-slate-800/80">
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2"><i class="fa-solid fa-location-dot text-amber-400"></i> Contacto y Redes Oficiales</h4>
                    <p class="flex items-start gap-2 text-slate-300"><i class="fa-solid fa-map-pin text-slate-500 mt-0.5 shrink-0"></i><span>Pedro Moreno 501 A, Guadalajara Centro, Jalisco (CP 44100)</span></p>
                    <p class="flex items-center gap-2"><i class="fa-solid fa-phone text-cyan-400 shrink-0"></i><span>Teléfono: <a href="tel:3336136348" class="text-slate-200 hover:text-cyan-400 font-mono">(33) 3613 6348</a></span></p>
                    <p class="flex items-center gap-2"><i class="fa-brands fa-whatsapp text-emerald-400 shrink-0 text-sm"></i><span>WhatsApp: <a href="https://wa.me/523337271440" target="_blank" class="text-slate-200 hover:text-emerald-400 font-mono">+52 33 3727 1440</a></span></p>
                    <div class="flex flex-col gap-1.5 pt-2 border-t border-slate-900 text-[11px] text-slate-400">
                        <a href="https://www.facebook.com/profile.php?id=61593020515115" target="_blank" rel="noopener" class="hover:text-blue-400 transition flex items-center gap-2"><i class="fa-brands fa-facebook text-blue-500 w-4 text-center"></i> Facebook: BAZAR NFL.GDL</a>
                        <a href="https://www.instagram.com/pccustomlab/" target="_blank" rel="noopener" class="hover:text-pink-400 transition flex items-center gap-2"><i class="fa-brands fa-instagram text-pink-500 w-4 text-center"></i> Instagram: @pccustomlab</a>
                        <a href="https://www.youtube.com/@IAWorldCenter" target="_blank" rel="noopener" class="hover:text-red-400 transition flex items-center gap-2"><i class="fa-brands fa-youtube text-red-500 w-4 text-center"></i> YouTube: IA World Center</a>
                        <a href="https://t.me/pc_custom_lab" target="_blank" rel="noopener" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-brands fa-telegram text-cyan-400 w-4 text-center"></i> Telegram: pc_custom_lab</a>
                        <a href="mailto:iaworldcenter@gmail.com" class="hover:text-amber-400 transition flex items-center gap-2"><i class="fa-solid fa-envelope text-amber-400 w-4 text-center"></i> Correo: iaworldcenter@gmail.com</a>
                    </div>
                </div>
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2"><i class="fa-solid fa-shield-halved text-cyan-400"></i> Políticas de Compra</h4>
                    <p class="text-[11px] text-slate-400 leading-relaxed">Devoluciones en tienda dentro de las 48 horas con empaque íntegro. Soporte técnico local y reemplazo inmediato.</p>
                </div>
                <div class="flex flex-col gap-3">
                    <h4 class="text-sm font-black text-white uppercase tracking-wider mb-1 flex items-center gap-2"><i class="fa-solid fa-coins text-emerald-400"></i> Ahorro y Cashback</h4>
                    <p class="text-slate-300 font-bold">5% de Cashback acumulable con tu cuenta registrada.</p>
                </div>
            </div>
            <div class="pt-8 text-center text-slate-500 text-[11px]">
                <p>&copy; 2026 BAZAR NFL.GDL & Ecosistema Comercial Pedro Moreno 501 A. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>

    <script>
    // 1. CONFIGURACIÓN DE LAS 7 BOUTIQUES OFICIALES
    const boutiquesConfig = [
        {{ id: "pc-custom", name: "PC Custom Lab", tag: "TECNOLOGÍA & PC", icon: "fa-microchip", color: "text-cyan-400", desc: "Hardware esencial, GPUs NVIDIA RTX, procesadores y ensamble.", url: "https://iaworldcenter-creator.github.io/pc-custom-lab/" }},
        {{ id: "viamx", name: "Vía MX Boutique", tag: "DEPARTAMENTAL & B2B", icon: "fa-gem", color: "text-cyan-300", desc: "Pantallas 4K, refrigeradores, laptops slim y electrónica del hogar.", url: "https://iaworldcenter-creator.github.io/bazar-viamx-NFL.GDL/" }},
        {{ id: "cigarros", name: "Cigarros Bazar", tag: "TABACOS & HABANOS", icon: "fa-smoking", color: "text-amber-400", desc: "Cigarros premium, puros habanos cubanos y encendedores selectos.", url: "https://iaworldcenter-creator.github.io/cigarros-bazar/" }},
        {{ id: "dulces", name: "Dulces Bazar", tag: "DULCERÍA & BOTANAS", icon: "fa-candy-cane", color: "text-pink-400", desc: "Paletas payaso, mazapanes de la rosa y confitería mexicana.", url: "https://iaworldcenter-creator.github.io/dulces-bazar/" }},
        {{ id: "kiosco", name: "Kiosco Digital", tag: "REVISTAS & PRENSA", icon: "fa-newspaper", color: "text-indigo-400", desc: "Suscripciones digitales anuales a revistas y periódicos en HD.", url: "https://iaworldcenter-creator.github.io/kiosco-digital/" }},
        {{ id: "puesto", name: "Mi Puesto Bazar", tag: "NOVEDADES & GADGETS", icon: "fa-store", color: "text-emerald-400", desc: "Lentes inteligentes, consolas retro y cables reforzados.", url: "https://iaworldcenter-creator.github.io/mi-puesto-bazar/" }},
        {{ id: "ofertas", name: "Ofertas & Liquidaciones", tag: "OUTLET DIRECTO B2B", icon: "fa-tags", color: "text-red-400", desc: "Excedentes de inventario y remates de lote con 50% de dto.", url: "https://iaworldcenter-creator.github.io/ofertas-y-liquidaciones-/" }}
    ];

    // 2. CATÁLOGO COMPLETO DE 35 PRODUCTOS (5 POR BOUTIQUE)
    const masterItems = [
        // Boutique 1: PC Custom Lab
        {{ sku: "PC-001", boutiqueId: "pc-custom", nombre: "Gabinete Micro-ATX con Fuente 500W Incluida", marca: "Acteck", precio: 1250.00, original: 1550.00, desc: "Chasis esbelto con fuente certificada y puertos USB 3.0 frontales.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/gabinete_negro.webp", tokens: ["gabinete", "fuente", "pc", "chasis"] }},
        {{ sku: "PC-002", boutiqueId: "pc-custom", nombre: "Tarjeta Madre ASUS Prime B760M-A WiFi DDR5", marca: "ASUS", precio: 3400.00, original: 3950.00, desc: "Placa base con soporte Intel Core 12va/13va/14va Gen y dual M.2 PCIe 4.0.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/motherboard_asus.webp", tokens: ["tarjeta madre", "motherboard", "asus", "placa"] }},
        {{ sku: "PC-003", boutiqueId: "pc-custom", nombre: "Procesador Intel Core i5-14400F 10C/16T con Disipador", marca: "Intel", precio: 4350.00, original: 4990.00, desc: "10 núcleos híbridos de alto rendimiento con disipador silencioso de fábrica.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/cpu_intel_ultra.webp", tokens: ["procesador", "cpu", "intel", "i5"] }},
        {{ sku: "PC-004", boutiqueId: "pc-custom", nombre: "Memoria RAM Kingston FURY Beast 16GB DDR5 5600MHz", marca: "Kingston", precio: 1250.00, original: 1500.00, desc: "Módulo DDR5 de alta velocidad con disipador térmico de aluminio negro.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/ram_caja.webp", tokens: ["ram", "kingston", "fury", "ddr5", "memoria"] }},
        {{ sku: "PC-005", boutiqueId: "pc-custom", nombre: "Disco Sólido SSD Kingston NV2 1TB NVMe PCIe 4.0", marca: "Kingston", precio: 1350.00, original: 1650.00, desc: "3,500 MB/s de lectura secuencial para carga instantánea del sistema.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/disco_solido_m2.webp", tokens: ["ssd", "kingston", "nvme", "disco", "m2"] }},
        
        // Boutique 2: Vía MX Boutique
        {{ sku: "VMX-001", boutiqueId: "viamx", nombre: "Pantalla Smart TV 55 Pulgadas 4K UHD HDR10+ WiFi", marca: "Samsung", precio: 7999.00, original: 11499.00, desc: "Panel LED 4K ultra nítido con asistente de voz y 4 puertos HDMI 2.1.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_curvo_negro.webp", tokens: ["pantalla", "smart tv", "samsung", "4k"] }},
        {{ sku: "VMX-002", boutiqueId: "viamx", nombre: "Refrigerador Inverter No Frost 14 Pies Cúbicos Acero", marca: "LG", precio: 11899.00, original: 15999.00, desc: "Doble puerta con compresor Digital Inverter de bajo consumo y despachador.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_warehouse_thumb.webp", tokens: ["refrigerador", "lg", "linea blanca", "inverter"] }},
        {{ sku: "VMX-003", boutiqueId: "viamx", nombre: "Freidora de Aire Digital 6.5 Litros con 12 Programas", marca: "Tefal", precio: 1499.00, original: 2199.00, desc: "Canastilla antiadherente libre de BPA con calor envolvente 360 grados.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_ia_human_thumb.webp", tokens: ["freidora", "aire", "airfryer", "tefal"] }},
        {{ sku: "VMX-004", boutiqueId: "viamx", nombre: "Laptop Ultra Slim 15.6 Pulgadas Core i7 16GB RAM 512GB", marca: "Lenovo", precio: 14500.00, original: 18900.00, desc: "Chasis de aluminio ligero, teclado iluminado y lector de huella.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_mantenimiento_thumb.webp", tokens: ["laptop", "lenovo", "core i7", "computadora"] }},
        {{ sku: "VMX-005", boutiqueId: "viamx", nombre: "Smartphone 5G Desbloqueado 256GB / 8GB RAM 108MP", marca: "Motorola", precio: 4899.00, original: 6499.00, desc: "Pantalla AMOLED 120Hz con batería de 5000mAh y carga turbo rápida.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/perifericos_combo_1.webp", tokens: ["celular", "telefono", "smartphone", "motorola"] }},

        // Boutique 3: Cigarros Bazar
        {{ sku: "CIG-001", boutiqueId: "cigarros", nombre: "Cigarros Marlboro Gold Original (Cajetilla 20)", marca: "Marlboro", precio: 82.00, original: 95.00, desc: "Sabor suave y filtro blanco balanceado de importación nacional.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["cigarros", "marlboro", "gold", "tabaco"] }},
        {{ sku: "CIG-002", boutiqueId: "cigarros", nombre: "Cigarros Benson & Hedges Black Switch (Cajetilla 20)", marca: "Benson & Hedges", precio: 88.00, original: 105.00, desc: "Cápsula de sabor mentolado premium con tabaco curado de alta calidad.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["cigarros", "benson", "hedges", "mentolados"] }},
        {{ sku: "CIG-003", boutiqueId: "cigarros", nombre: "Puro Habanos Cohiba Siglo VI Tubo Individual", marca: "Cohiba", precio: 850.00, original: 1100.00, desc: "Puro cubano hecho a mano con notas amaderadas y especiadas.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["puro", "cohiba", "siglo vi", "habano"] }},
        {{ sku: "CIG-004", boutiqueId: "cigarros", nombre: "Puro Romeo y Julieta Churchill en Tubo Aluminio", marca: "Romeo y Julieta", precio: 620.00, original: 790.00, desc: "Vitola clásica Churchill de fortaleza media con tiro excelente.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["puro", "romeo y julieta", "churchill"] }},
        {{ sku: "CIG-005", boutiqueId: "cigarros", nombre: "Encendedor de Colección Vintage a Gas Recargable", marca: "Clipper Pro", precio: 195.00, original: 260.00, desc: "Cuerpo metálico cepillado con piedra intercambiable y válvula.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_corporativo_thumb.webp", tokens: ["encendedor", "clipper", "fuego", "gas"] }},

        // Boutique 4: Dulces Bazar
        {{ sku: "DUL-001", boutiqueId: "dulces", nombre: "Paleta Payaso Ricolino (Caja con 15 piezas)", marca: "Ricolino", precio: 245.00, original: 290.00, desc: "Malvavisco cubierto de chocolate con gomitas de colores tradicionales.", img: "assets/img/mascota_tigre_thumb.webp", tokens: ["paleta", "payaso", "ricolino", "dulces"] }},
        {{ sku: "DUL-002", boutiqueId: "dulces", nombre: "Mazapán De La Rosa Gigante (Caja con 20 piezas)", marca: "De La Rosa", precio: 160.00, original: 195.00, desc: "El dulce tradicional mexicano de cacahuate tostado seleccionado.", img: "assets/img/mascota_tigre_thumb.webp", tokens: ["mazapan", "de la rosa", "cacahuate"] }},
        {{ sku: "DUL-003", boutiqueId: "dulces", nombre: "Rocaleta Sonrics con Centro de Goma (Bolsa 30)", marca: "Sonrics", precio: 185.00, original: 230.00, desc: "Caramelo con 4 capas de chile ácido y centro de chicle masticable.", img: "assets/img/mascota_tigre_thumb.webp", tokens: ["rocaleta", "sonrics", "chile", "paleta"] }},
        {{ sku: "DUL-004", boutiqueId: "dulces", nombre: "Chocolates Finos Surtidos Artesanales Caja Regalo", marca: "Turín", precio: 220.00, original: 280.00, desc: "Bombones semiamargos rellenos de licor y crema de avellana.", img: "assets/img/mascota_tigre_thumb.webp", tokens: ["chocolate", "turin", "bombones"] }},
        {{ sku: "DUL-005", boutiqueId: "dulces", nombre: "Cacahuates Japoneses con Ajo y Chile (Bolsa 1 Kg)", marca: "Nipon", precio: 95.00, original: 130.00, desc: "Botana crujiente horneada ideal para reuniones y eventos.", img: "assets/img/mascota_tigre_thumb.webp", tokens: ["cacahuates", "botana", "snacks", "nipon"] }},

        // Boutique 5: Kiosco Digital
        {{ sku: "KIO-001", boutiqueId: "kiosco", nombre: "Suscripción Digital Anual Revista National Geographic", marca: "RBA", precio: 599.00, original: 850.00, desc: "12 ediciones digitales en alta definición + acceso al archivo fotográfico.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_plano_blanco.webp", tokens: ["revista", "national geographic", "natgeo", "digital"] }},
        {{ sku: "KIO-002", boutiqueId: "kiosco", nombre: "Suscripción Digital Revista Muy Interesante (1 Año)", marca: "Zinet", precio: 450.00, original: 620.00, desc: "Acceso total multidispositivo a reportajes de ciencia, historia e innovación.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_plano_blanco.webp", tokens: ["revista", "muy interesante", "ciencia"] }},
        {{ sku: "KIO-003", boutiqueId: "kiosco", nombre: "Suscripción Revista Conozca Más Digital Colección", marca: "Editorial Televisa", precio: 380.00, original: 490.00, desc: "Enciclopedia de curiosidades científicas, enigmas y avances médicos.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_plano_blanco.webp", tokens: ["revista", "conozca mas", "cultura"] }},
        {{ sku: "KIO-004", boutiqueId: "kiosco", nombre: "Paquete Digital Cómics Clásicos Restaurados (PDF HD)", marca: "Panini / Marvel", precio: 290.00, original: 420.00, desc: "Tomos históricos de superhéroes digitalizados en máxima resolución.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_plano_blanco.webp", tokens: ["comics", "marvel", "panini"] }},
        {{ sku: "KIO-005", boutiqueId: "kiosco", nombre: "Pase Mensual Prensa Digital y Periódicos de Guadalajara", marca: "El Informador", precio: 180.00, original: 240.00, desc: "Edición matutina completa disponible en tu celular desde las 6:00 AM.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_plano_blanco.webp", tokens: ["periodico", "noticias", "guadalajara"] }},

        // Boutique 6: Mi Puesto Bazar
        {{ sku: "PUE-001", boutiqueId: "puesto", nombre: "Lentes Inteligentes Bluetooth con Audio y Micrófono", marca: "SmartVision", precio: 680.00, original: 950.00, desc: "Contesta llamadas, sube/baja volumen y escucha música con protección UV.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_gamer_thumb.webp", tokens: ["lentes", "inteligentes", "bluetooth", "audio"] }},
        {{ sku: "PUE-002", boutiqueId: "puesto", nombre: "Consola Retro Portátil con 500 Juegos Clásicos", marca: "Sup Game", precio: 290.00, original: 390.00, desc: "Batería recargable y salida para conectar a la televisión con cable AV.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/tigre_gemini_thumb.webp", tokens: ["consola", "retro", "videojuegos", "juegos"] }},
        {{ sku: "PUE-003", boutiqueId: "puesto", nombre: "Cable de Carga Rápida USB-C a USB-C de 65W Reforzado", marca: "Baseus", precio: 120.00, original: 180.00, desc: "Cable trenzado de nailon de 2 metros compatible con celulares y laptops.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/fuente_modular.webp", tokens: ["cable", "cargador", "usb c", "carga rapida"] }},
        {{ sku: "PUE-004", boutiqueId: "puesto", nombre: "Batería Portátil Power Bank 10,000mAh con Display", marca: "Adata", precio: 340.00, original: 450.00, desc: "Carga hasta dos dispositivos con indicador LED de porcentaje exacto.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/perifericos_combo_1.webp", tokens: ["bateria", "power bank", "cargador portatil"] }},
        {{ sku: "PUE-005", boutiqueId: "puesto", nombre: "Smartwatch Deportivo con Monitor de Ritmo y Pasos", marca: "FitBand Pro", precio: 450.00, original: 650.00, desc: "Notificaciones de WhatsApp, llamadas y resistencia al agua IP67.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/Female_technician_assembling_gam_202608041518_thumb.webp", tokens: ["reloj", "smartwatch", "fitness", "deportivo"] }},

        // Boutique 7: Ofertas & Liquidaciones
        {{ sku: "OFE-001", boutiqueId: "ofertas", nombre: "Lote de Remate Electrónica y Accesorios Varios Grado A", marca: "Sony / Varios", precio: 2490.00, original: 3800.00, desc: "Paquete surtido de oportunidad comercial con garantía y respaldo.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/software_estante_madera.webp", tokens: ["lote", "remate", "liquidacion", "oferta"] }},
        {{ sku: "OFE-002", boutiqueId: "ofertas", nombre: "Monitor Curvo 24 Pulgadas 144Hz Full HD de Exhibición", marca: "AOC", precio: 2100.00, original: 3200.00, desc: "Equipo de vitrina estética 10/10 con caja original y cables.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/monitor_curvo_negro.webp", tokens: ["monitor", "curvo", "aoc", "144hz"] }},
        {{ sku: "OFE-003", boutiqueId: "ofertas", nombre: "Kit de Herramientas Mecánicas 168 Piezas en Maletín", marca: "Stanley", precio: 899.00, original: 1299.00, desc: "Últimas piezas de importación con matraca y dados milimétricos.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/catalog/software_estante_muro.webp", tokens: ["herramientas", "stanley", "maletin"] }},
        {{ sku: "OFE-004", boutiqueId: "ofertas", nombre: "Bocina Bluetooth Portátil contra Agua 20W Excedente", marca: "JBL", precio: 750.00, original: 1100.00, desc: "Sonido de alta fidelidad con batería de 12 horas de duración.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/slider_warehouse_thumb.webp", tokens: ["bocina", "jbl", "bluetooth", "audio"] }},
        {{ sku: "OFE-005", boutiqueId: "ofertas", nombre: "Caja Sorpresa de Novedades y Gadgets Mixtos (10 Piezas)", marca: "Bazar NFL.GDL", precio: 999.00, original: 1800.00, desc: "Artículos variados de conveniencia con valor superior garantizado.", img: "https://iaworldcenter-creator.github.io/pc-custom-lab/assets/img/mascota_tigre.webp", tokens: ["caja sorpresa", "mistery box", "novedades"] }}
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
                            <span>Ver todo en boutique (${{products.length}})</span> <i class="fa-solid fa-arrow-right text-[10px]"></i>
                        </a>
                    </div>

                    <!-- CARRUSEL DE 2 PRODUCTOS EN MÓVIL Y 5 EN DESKTOP CON FLECHAS -->
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

# Guardar en la raíz y submódulo
for p in [os.path.join(BASE_DIR, "index.html"), os.path.join(BASE_DIR, "sitios-web", "index.html")]:
    if os.path.exists(os.path.dirname(p)):
        with open(p, "w", encoding="utf-8") as f:
            f.write(PORTAL_MATRIZ_HTML)
        print(f"✓ Portal Matriz actualizado con las 7 Boutiques y 35 productos en: {p}")

# Desplegar todo a GitHub Pages
print("\n=== DESPLEGANDO A GITHUB PAGES ===")
sitios_repo = os.path.join(BASE_DIR, "sitios-web")
if os.path.exists(os.path.join(sitios_repo, ".git")):
    subprocess.run(["git", "add", "-A"], cwd=sitios_repo, check=True)
    subprocess.run(["git", "commit", "-m", "feat(showcase): 7 boutiques completas con 5 productos cada una (35 items)", "--allow-empty"], cwd=sitios_repo, capture_output=True)
    res_sub = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=sitios_repo, capture_output=True, text=True)
    print(f"🟢 Submódulo sitios-web -> Push: {'OK' if res_sub.returncode == 0 else res_sub.stderr.strip()}")

subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
subprocess.run(["git", "commit", "-m", "feat(ecosistema): 7 boutiques y 35 productos desplegados en monorepositorio", "--allow-empty"], cwd=BASE_DIR, capture_output=True)
res_root = subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
print(f"🟢 Monorepositorio Central -> Push: {'OK' if res_root.returncode == 0 else res_root.stderr.strip()}")
