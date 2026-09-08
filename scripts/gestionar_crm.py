#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/gestionar_crm.py
GESTOR COMERCIAL Y CRM PARTICIONADO EN LOTES DE 10,000 CARACTERES
Ecosistema VECTEC / 8 Boutiques Oficiales

Formato de Registro:
ID | Fecha | Nombre | Teléfono | Correo | Giro Estimado | Total MXN | Canal/Tienda | Dirección

Regla de Particionado:
Cada archivo en crm_clientes/ (lote_01.txt, lote_02.txt, etc.) tiene un límite estricto
de 10,000 caracteres. Al alcanzar dicho umbral, se cierra y se continúa en el siguiente lote.
"""

import os
import sys
import json
import csv
from datetime import datetime

MAX_CHARS_POR_LOTE = 10000

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
CRM_DIR = os.path.join(BASE_DIR, "crm_clientes")
CRM_JSON = os.path.join(DATA_DIR, "clientes_registrados_crm.json")

os.makedirs(CRM_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

def estimar_giro_comercial(cliente):
    nombre = (cliente.get("nombre") or "").lower()
    email = (cliente.get("email") or "").lower()
    total = float(cliente.get("total_mxn") or cliente.get("total") or 0)
    
    if "cctv" in nombre or "seguridad" in nombre or "alarmas" in nombre:
        return "Instalador CCTV / Seguridad Privada"
    elif "ciber" in nombre or "cafe" in nombre or "papeleria" in nombre:
        return "Cibercafé / Papelería Local"
    elif "compu" in nombre or "pc" in nombre or "tech" in nombre or "sistemas" in nombre:
        return "Taller de Ensamble y Reparación PC"
    elif "despacho" in nombre or "abogad" in nombre or "notaria" in nombre or "consultor" in nombre:
        return "Servicios Profesionales / Corporativo"
    elif total >= 15000:
        return "Distribuidor / Mayorista TI"
    elif total >= 5000:
        return "Gamer Entusiasta / Creador de Contenido"
    else:
        return "Consumidor Final / Retail"

def formatear_registro(idx, c):
    cid = f"CLI-{idx:05d}"
    fecha = c.get("fecha") or c.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M")
    nombre = c.get("nombre") or "Cliente Mostrador"
    tel = c.get("telefono") or c.get("phone") or "3328652309"
    email = c.get("email") or "contacto@vectec.mx"
    giro = c.get("giro_estimado") or estimar_giro_comercial(c)
    total = float(c.get("total_mxn") or c.get("total") or 0)
    tienda = c.get("tienda") or c.get("store") or "VECTEC Pedro Moreno 501 A"
    dir_txt = c.get("direccion") or c.get("address") or "Pedro Moreno 501 A, Centro, GDL"

    linea = (
        f"[{cid}] | Fecha: {fecha} | Nombre: {nombre} | Tel: {tel} | "
        f"Correo: {email} | Giro: {giro} | Total: ${total:,.2f} MXN | "
        f"Tienda: {tienda} | Domicilio: {dir_txt}\n"
    )
    return linea

def cargar_clientes_existentes():
    clientes = []
    if os.path.exists(CRM_JSON):
        try:
            with open(CRM_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    clientes.extend(data)
        except Exception as e:
            print(f"Advertencia al leer {CRM_JSON}: {e}")
    
    # Si hay pocos, generar clientes de ejemplo representativos del ecosistema
    if len(clientes) < 50:
        tiendas_ejemplo = [
            ("PC Custom Lab", 6450.00, "Ing. Alejandro Morales", "3312457890", "amorales@cybertech.mx", "Taller de Ensamble y Reparación PC"),
            ("Bazar Vía MX NFL", 3200.50, "Lic. Roberto Garza", "3324568901", "rgarza@notaria45.com", "Servicios Profesionales / Corporativo"),
            ("Mi Puesto Bazar", 850.00, "María Elena Ríos", "3335679012", "m.rios@gmail.com", "Consumidor Final / Retail"),
            ("Ofertas & Liquidaciones", 12890.00, "Carlos Mendoza", "3346780123", "carlos@redescctv.com", "Instalador CCTV / Seguridad Privada"),
            ("Kiosco Digital", 4500.00, "Fernanda Salcido", "3357891234", "fsalcido@cibernet.com", "Cibercafé / Papelería Local"),
            ("Dulces Bazar", 750.00, "Daniel Ortíz", "3368902345", "dany.ortiz@hotmail.com", "Consumidor Final / Retail"),
            ("Cigarros Bazar", 1250.00, "Jorge Valenzuela", "3379013456", "jorge_val@yahoo.com", "Consumidor Final / Retail"),
            ("Matriz Central", 18500.00, "Sistemas Computacionales GDL", "3380124567", "compras@sistemasgdl.mx", "Distribuidor / Mayorista TI")
        ]
        base_len = len(clientes)
        for i in range(1, 65):
            t_info = tiendas_ejemplo[i % len(tiendas_ejemplo)]
            clientes.append({
                "id": f"CLI-{base_len + i:05d}",
                "fecha": f"2026-09-{(i % 7) + 1:02d} 14:{i%60:02d}",
                "nombre": f"{t_info[2]} #{i}",
                "telefono": t_info[3],
                "email": t_info[4],
                "giro_estimado": t_info[5],
                "total_mxn": t_info[1] + (i * 25.50),
                "tienda": t_info[0],
                "direccion": f"Av. Vallarta #{1000 + i*15}, Col. Americana, Guadalajara, Jal."
            })
        
        # Guardar en json
        with open(CRM_JSON, "w", encoding="utf-8") as f:
            json.dump(clientes, f, indent=2, ensure_ascii=False)

    return clientes

def particionar_crm_en_lotes(clientes=None):
    if clientes is None:
        clientes = cargar_clientes_existentes()

    lote_num = 1
    archivo_actual = os.path.join(CRM_DIR, f"lote_{lote_num:02d}.txt")
    contenido_lote = (
        f"===============================================================================\n"
        f" VECTEC CRM COMERCIAL - LOTE {lote_num:02d} (MAX 10,000 CARACTERES)\n"
        f" Fecha de corte: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"===============================================================================\n\n"
    )

    lotes_generados = []
    
    for idx, c in enumerate(clientes, 1):
        linea = formatear_registro(idx, c)
        
        # Si agregar la siguiente línea excede los 10,000 caracteres, cerrar lote
        if len(contenido_lote) + len(linea) > MAX_CHARS_POR_LOTE:
            with open(archivo_actual, "w", encoding="utf-8") as out:
                out.write(contenido_lote)
            lotes_generados.append((archivo_actual, len(contenido_lote)))
            
            lote_num += 1
            archivo_actual = os.path.join(CRM_DIR, f"lote_{lote_num:02d}.txt")
            contenido_lote = (
                f"===============================================================================\n"
                f" VECTEC CRM COMERCIAL - LOTE {lote_num:02d} (MAX 10,000 CARACTERES)\n"
                f" Fecha de corte: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"===============================================================================\n\n"
            )
        
        contenido_lote += linea

    # Guardar último lote
    if contenido_lote:
        with open(archivo_actual, "w", encoding="utf-8") as out:
            out.write(contenido_lote)
        lotes_generados.append((archivo_actual, len(contenido_lote)))

    print(f"\n[CRM] Particionado completado exitosamente: {len(lotes_generados)} lotes generados.")
    for ruta, tam in lotes_generados:
        print(f"  -> {os.path.basename(ruta)}: {tam:,} caracteres (Límite: {MAX_CHARS_POR_LOTE:,})")
    
    return lotes_generados

def registrar_nuevo_pedido(cliente_dict):
    clientes = cargar_clientes_existentes()
    cliente_dict["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    cliente_dict["id"] = f"CLI-{len(clientes)+1:05d}"
    clientes.append(cliente_dict)
    
    with open(CRM_JSON, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=2, ensure_ascii=False)
    
    particionar_crm_en_lotes(clientes)
    return cliente_dict["id"]

if __name__ == "__main__":
    print("Iniciando particionado de CRM en lotes de 10,000 caracteres...")
    particionar_crm_en_lotes()
