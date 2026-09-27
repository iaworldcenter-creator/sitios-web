# -*- coding: utf-8 -*-
import os
import json
import glob

DEPT_DIR = "data/departments"

anomalies = []

files = glob.glob(os.path.join(DEPT_DIR, "*.json"))
print(f"Total department files found: {len(files)}")

for fpath in sorted(files):
    dept_name = os.path.basename(fpath).replace(".json", "")
    with open(fpath, "r", encoding="utf-8") as f:
        try:
            items = json.load(f)
        except Exception as e:
            print(f"Error loading {fpath}: {e}")
            continue
    
    count = len(items)
    
    # Check for suspicious items in each department
    suspicious = []
    for it in items:
        sku = (it.get("sku") or it.get("s") or "").upper()
        raw_sku = sku.replace("A-", "").replace("B-", "")
        name = (it.get("nombre") or it.get("n") or "").upper()
        
        # 1. In procesadores: should not have motherboards or cooling or cases
        if "procesadores" in dept_name:
            if raw_sku.startswith("MBD") or "TARJETA MADRE" in name or "MOTHERBOARD" in name:
                suspicious.append((sku, name[:60], "Motherboard in CPUs"))
            if raw_sku.startswith("MON") or "MONITOR" in name:
                suspicious.append((sku, name[:60], "Monitor in CPUs"))
        
        # 2. In tarjetas_madre: should not have CPUs
        if "tarjetas_madre" in dept_name:
            if raw_sku.startswith(("CPUINT", "CPUAMD")) or name.startswith("PROCESADOR "):
                suspicious.append((sku, name[:60], "CPU in Motherboards"))
            if "MONITOR" in name and not "SOPORTE" in name:
                suspicious.append((sku, name[:60], "Monitor in Motherboards"))
        
        # 3. In fuentes_energia: should not have monitors or RAM or motherboards
        if "fuentes_energia" in dept_name:
            if "MONITOR" in name:
                suspicious.append((sku, name[:60], "Monitor in Power Supplies"))
            if raw_sku.startswith("MEM") or "MEMORIA RAM" in name:
                suspicious.append((sku, name[:60], "RAM in Power Supplies"))
            if raw_sku.startswith("MBD"):
                suspicious.append((sku, name[:60], "Motherboard in Power Supplies"))
            if "GABINETE CON FUENTE" in name or (name.startswith("GABINETE ") and "CON FUENTE" in name):
                suspicious.append((sku, name[:60], "Case in Power Supplies"))
        
        # 4. In monitores_pantallas: should not have power supplies or RAM or CPUs
        if "monitores_pantallas" in dept_name:
            if raw_sku.startswith("FUE") or "FUENTE DE PODER" in name:
                suspicious.append((sku, name[:60], "Power Supply in Monitors"))
            if raw_sku.startswith("MEM") or "MEMORIA RAM" in name:
                suspicious.append((sku, name[:60], "RAM in Monitors"))
            if raw_sku.startswith(("CPUINT", "CPUAMD")):
                suspicious.append((sku, name[:60], "CPU in Monitors"))
        
        # 5. In memorias_ram: should not have monitors, power supplies, or CPUs
        if "memorias_ram" in dept_name:
            if raw_sku.startswith("MON") or "MONITOR " in name:
                suspicious.append((sku, name[:60], "Monitor in RAM"))
            if raw_sku.startswith("FUE") or "FUENTE DE PODER" in name:
                suspicious.append((sku, name[:60], "Power Supply in RAM"))
            if raw_sku.startswith(("CPUINT", "CPUAMD")):
                suspicious.append((sku, name[:60], "CPU in RAM"))
            if raw_sku.startswith("MSD") or "MICROSD" in name:
                suspicious.append((sku, name[:60], "MicroSD in RAM PC"))
        
        # 6. In sistemas_operativos: should NOT have CPUs or motherboards or RAM
        if "sistemas_operativos" in dept_name:
            if raw_sku.startswith(("CPUINT", "CPUAMD")) or name.startswith("PROCESADOR ") or "RYZEN " in name or "CORE I" in name:
                suspicious.append((sku, name[:60], "CPU in Operating Systems"))
            if raw_sku.startswith("MBD") or "TARJETA MADRE" in name:
                suspicious.append((sku, name[:60], "Motherboard in Operating Systems"))
            if raw_sku.startswith("MEM") or "MEMORIA RAM" in name:
                suspicious.append((sku, name[:60], "RAM in Operating Systems"))

        # 7. In candados_seguridad_laptop: should NOT have monitors
        if "candados_seguridad_laptop" in dept_name:
            if raw_sku.startswith("MON") or name.startswith("MONITOR ") or "PANTALLA " in name:
                suspicious.append((sku, name[:60], "Monitor in Candados"))

        # 8. In enfriamiento: should NOT have power supplies or CPUs
        if "enfriamiento" in dept_name:
            if raw_sku.startswith("FUE") or name.startswith("FUENTE DE PODER") or "FUENTE DE PODER " in name:
                suspicious.append((sku, name[:60], "Power Supply in Enfriamiento"))
            if raw_sku.startswith(("CPUINT", "CPUAMD")) and not ("DISIPADOR" in name or "COOLER" in name):
                suspicious.append((sku, name[:60], "CPU in Enfriamiento"))

        # 9. In gabinetes: should NOT have standalone power supplies or motherboards
        if "gabinetes" in dept_name:
            if raw_sku.startswith("FUE") and not "GABINETE" in name:
                suspicious.append((sku, name[:60], "Power Supply in Gabinetes"))
            if raw_sku.startswith("MBD"):
                suspicious.append((sku, name[:60], "Motherboard in Gabinetes"))

        # 10. In tarjetas_video: should NOT have CPUs or motherboards
        if "tarjetas_video" in dept_name:
            if raw_sku.startswith(("CPUINT", "CPUAMD")) or name.startswith("PROCESADOR "):
                suspicious.append((sku, name[:60], "CPU in Tarjetas de Video"))
            if raw_sku.startswith("MBD"):
                suspicious.append((sku, name[:60], "Motherboard in Tarjetas de Video"))
                
    if suspicious:
        print(f"\n[ANOMALY] {dept_name} (Total: {count} items) -> {len(suspicious)} suspicious items:")
        for s in suspicious[:10]:
            print(f"   {s[0]} | {s[2]} | {s[1]}")
        anomalies.append((dept_name, len(suspicious)))
    else:
        print(f"[OK] {dept_name}: {count} items")

print("\n" + "=" * 80)
print(f"Total departments with anomalies: {len(anomalies)}")
for a in anomalies:
    print(f" - {a[0]}: {a[1]} anomalies")
print("=" * 80)
