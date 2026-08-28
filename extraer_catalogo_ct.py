import os
import pandas as pd
import json
import re

FILE_LISTA = r"D:\Descargas\lista3\TOL 082426\1308 LISTA DE PRECIOS DE CT TOL 082426.xlsx"
FILE_CONFIG = r"D:\Descargas\lista3\TOL 082426\1308 CONFIGURACIONES TOL 082426.xlsx"
GALLERY_DIR = r"E:\sitios web\pc-custom-lab\assets\gallery"

print("=" * 80)
print("EXTRACTOR MAESTRO DE INVENTARIO CT INTERNACIONAL Y CONFIGURACIONES")
print("=" * 80)

# Cargar catálogo de imágenes locales
gallery_images = []
if os.path.exists(GALLERY_DIR):
    gallery_images = [f for f in os.listdir(GALLERY_DIR) if f.endswith('.webp') or f.endswith('.png') or f.endswith('.jpg')]

print(f"Total imágenes locales en galería PC Custom Lab: {len(gallery_images)}")

# TIPO DE CAMBIO USD -> MXN (CT suele listar en USD antes de IVA o en MXN según hoja)
TIPO_CAMBIO = 19.50
MARGEN_UTILIDAD = 1.18 # 18% margen

xls = pd.ExcelFile(FILE_LISTA)
print(f"Hojas encontradas en Lista de Precios ({len(xls.sheet_names)}):", xls.sheet_names)

all_clean_products = []
img_idx = 0

for sheet in xls.sheet_names:
    if sheet in ['LISTA DE PRECIOS', 'INDICE', 'DIRECTORIO', 'DIRECTORIO DE COORDINADORES']:
        continue
    
    try:
        df = pd.read_excel(xls, sheet)
    except Exception as e:
        print(f"Error leyendo hoja {sheet}: {e}")
        continue
        
    print(f"Procesando hoja [{sheet}] con {df.shape[0]} filas y {df.shape[1]} columnas...")

    # Recorrer filas buscando claves de producto
    for r in range(len(df)):
        row = df.iloc[r]
        for c in range(df.shape[1]):
            val = str(df.iloc[r, c]).strip()
            # Patrón de clave CT (3-6 letras mayúsculas seguidas de números/letras)
            if len(val) >= 5 and len(val) <= 18 and val[:3].isalpha() and val[3:].isalnum() and val.upper() != 'NAN' and not val.startswith('HTTP'):
                row_vals = row.values
                desc = ""
                price = 0.0
                brand = ""
                
                for item in row_vals:
                    if isinstance(item, str) and len(item) > 12 and not item.startswith('http') and not item == val:
                        if len(item) > len(desc):
                            desc = item.strip()
                    elif isinstance(item, (int, float)) and not pd.isna(item):
                        if 0.5 < float(item) < 1000000:
                            price = float(item)
                            
                if desc and price > 0:
                    # Extraer marca tentativa de los primeros términos de la descripción o clave
                    desc_words = desc.split()
                    brand = desc_words[0] if desc_words else "GENERIC"
                    if len(desc_words) > 1 and desc_words[0].upper() in ["PROCESADOR", "TARJETA", "MEMORIA", "DISCO", "GABINETE", "FUENTE", "MONITOR", "TECLADO", "MOUSE"]:
                        brand = desc_words[1]

                    # Determinar si el precio está en USD o MXN
                    precio_mxn = price * TIPO_CAMBIO * MARGEN_UTILIDAD if price < 2500 and "MXN" not in sheet.upper() else price * MARGEN_UTILIDAD
                    precio_original = precio_mxn * 1.25

                    # Asignar imagen
                    img_file = gallery_images[img_idx % len(gallery_images)] if gallery_images else "assets/img/fachada-oficial.webp"
                    img_url = f"https://iaworldcenter-creator.github.io/pc-custom-lab/assets/gallery/{img_file}"
                    img_idx += 1

                    all_clean_products.append({
                        "sku": val,
                        "nombre": desc[:120],
                        "descripcion_completa": desc,
                        "categoria_ct": sheet,
                        "marca": brand.upper().replace(",", "").replace(".", ""),
                        "costo_base": round(price, 2),
                        "precio_mxn": round(precio_mxn, 2),
                        "precio_original": round(precio_original, 2),
                        "img": img_url
                    })

df_clean = pd.DataFrame(all_clean_products).drop_duplicates(subset=['sku'])
print(f"\n✅ Total productos limpios y únicos extraídos: {len(df_clean)}")
print("\nDesglose por Categoría:")
print(df_clean['categoria_ct'].value_counts())

# Guardar CSV y JSON en pc-custom-lab y en catálogo general
os.makedirs(r"E:\sitios web\pc-custom-lab\data", exist_ok=True)
os.makedirs(r"C:\Users\nflgd\OneDrive\Documentos\ChatGPT\sitios web\pc-custom-lab\data", exist_ok=True)

csv_path = r"E:\sitios web\pc-custom-lab\data\catalogo_maestro_ct.csv"
json_path = r"E:\sitios web\pc-custom-lab\data\catalogo_maestro_ct.json"

df_clean.to_csv(csv_path, index=False, encoding='utf-8')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(df_clean.to_dict(orient='records'), f, ensure_ascii=False, indent=2)

print(f"\n📁 Guardado exitosamente:")
print(f" -> {csv_path}")
print(f" -> {json_path}")
