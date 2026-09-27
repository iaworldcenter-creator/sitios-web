# -*- coding: utf-8 -*-
import json
import re

# Load all products from catalogo_maestro_compact.json or inventario_maestro_buscador.json
with open("data/inventario_maestro_buscador.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

print(f"Loaded {len(catalog)} products for simulation test.")

from clasificador_semantico_vectec import clasificar_producto_semantico

# Let's inspect current vs proposed rules
# We can test the current clasificar_producto_semantico directly first
from collections import Counter
curr_depts = Counter()
for it in catalog:
    sku = it.get("sku") or it.get("s")
    name = it.get("nombre") or it.get("n")
    brand = it.get("marca") or it.get("m")
    desc = it.get("d_desc") or it.get("desc") or ""
    cat = clasificar_producto_semantico(sku, name, brand=brand, desc=desc)
    curr_depts[cat] += 1

print("\nCurrent classification counts for key departments:")
for d in ["procesadores", "tarjetas_madre", "fuentes_energia", "enfriamiento", "monitores_pantallas", "memorias_ram_pc", "sistemas_operativos", "candados_seguridad_laptop"]:
    print(f"  {d}: {curr_depts[d]}")
