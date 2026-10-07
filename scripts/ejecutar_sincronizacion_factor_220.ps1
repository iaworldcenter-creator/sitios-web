# ==============================================================================
# EJECUTAR_SINCRONIZACION_FACTOR_220.PS1
# Unificación y despliegue comercial con Factor 2.20 en los 8 repositorios
# ==============================================================================

Add-Type -AssemblyName System.Web.Extensions
$ser = New-Object System.Web.Script.Serialization.JavaScriptSerializer
$ser.MaxJsonLength = [int]::MaxValue

$baseDir = "D:\Proyectos\sitios web"
$ctCsvPath = Join-Path $baseDir "pc-custom-lab\data\catalogo_maestro_ct.csv"

Write-Output "=================================================================="
Write-Output "FASE 1: CARGA DE SSOT Y CÁLCULO DEL FACTOR 2.20"
Write-Output "=================================================================="

if (-not (Test-Path $ctCsvPath)) {
    Write-Error "No se encontro catalogo_maestro_ct.csv en $ctCsvPath"
    exit 1
}

$ctRows = Import-Csv $ctCsvPath
Write-Output "Filas cargadas de CT CSV: $($ctRows.Count)"

# Construir diccionario de precios factor 2.20
$priceMap = @{}
$nameMap = @{}

foreach ($r in $ctRows) {
    $sku = $r.sku.Trim()
    $costo = [double]$r.costo_base_mxn
    if ($costo -le 0) { $costo = 100.0 } # seguro

    $pLista = [math]::Round($costo * 2.20, 2)
    $pVenta = [math]::Round($costo * 1.65, 2)
    $pMayoreo = [math]::Round($costo * 1.485, 2)

    $info = @{
        sku = $sku
        costo = $costo
        p_lista = $pLista
        p_venta = $pVenta
        p_mayoreo = $pMayoreo
        usd = if ($r.precio_usd) { [double]$r.precio_usd } else { [math]::Round($pVenta / 19.5, 2) }
        nombre = $r.nombre
        categoria = $r.categoria_clasificada
        linea = $r.linea_origen
        img = $r.img
    }

    $priceMap[$sku] = $info
    $priceMap["A-$sku"] = $info
    $nameMap[$sku] = $r.nombre
}

Write-Output "Mapa de precios indexado: $($priceMap.Count) variantes de SKU (con y sin prefijo A-)."

# Actualizar catalogo_maestro_ct.csv
foreach ($r in $ctRows) {
    $sku = $r.sku.Trim()
    if ($priceMap.ContainsKey($sku)) {
        $p = $priceMap[$sku]
        $r.precio_original = $p.p_lista.ToString("F2")
        $r.precio_mxn = $p.p_venta.ToString("F2")
        $r.precio = $p.p_venta.ToString("F2")
        $r.precio_mayoreo = $p.p_mayoreo.ToString("F2")
        $r.precio_mayoreo_10pzs = $p.p_mayoreo.ToString("F2")
        $r.descuento_porcentaje = "25"
        $r.descuento_pct = "25"
    }
}
$ctRows | Export-Csv -Path $ctCsvPath -NoTypeInformation -Encoding UTF8
Write-Output "[OK] catalogo_maestro_ct.csv actualizado con factor 2.20."

# ------------------------------------------------------------------------------
# FASE 2: ACTUALIZAR catalogo_maestro_compact.json E inventario_maestro_buscador.json
# ------------------------------------------------------------------------------
Write-Output "`n=================================================================="
Write-Output "FASE 2: REGENERACION DE CATALOGO COMPACTO Y BUSCADOR"
Write-Output "=================================================================="

$compactMasterPath = Join-Path $baseDir "pc-custom-lab\data\catalogo_maestro_compact.json"
$searchMasterPath = Join-Path $baseDir "pc-custom-lab\data\inventario_maestro_buscador.json"

$compactRaw = [System.IO.File]::ReadAllText($compactMasterPath, [System.Text.Encoding]::UTF8)
$compactItems = $ser.DeserializeObject($compactRaw)
Write-Output "Items en catalogo_maestro_compact: $($compactItems.Length)"

$updatedCompactCount = 0
for ($i = 0; $i -lt $compactItems.Length; $i++) {
    $it = $compactItems[$i]
    $s = $it["s"]
    if (-not $s) { $s = $it["sku"] }
    if ($s) {
        $raw = $s.Replace("A-", "")
        if ($priceMap.ContainsKey($raw)) {
            $p = $priceMap[$raw]
            $it["o"] = $p.p_lista
            $it["p"] = $p.p_venta
            $it["y"] = $p.p_mayoreo
            $it["descuento_pct"] = 25
            $updatedCompactCount++
        }
    }
}
Write-Output "Items actualizados en catalogo compacto: $updatedCompactCount"
$compactJsonNew = $ser.Serialize($compactItems)
[System.IO.File]::WriteAllText($compactMasterPath, $compactJsonNew, [System.Text.Encoding]::UTF8)
Write-Output "[OK] catalogo_maestro_compact.json guardado en pc-custom-lab ($([math]::Round($compactJsonNew.Length/1MB, 2)) MB)."

# Actualizar buscador
$searchRaw = [System.IO.File]::ReadAllText($searchMasterPath, [System.Text.Encoding]::UTF8)
$searchItems = $ser.DeserializeObject($searchRaw)
Write-Output "Items en inventario_maestro_buscador: $($searchItems.Length)"

$updatedSearchCount = 0
for ($i = 0; $i -lt $searchItems.Length; $i++) {
    $it = $searchItems[$i]
    $s = $it["sku"]
    if (-not $s) { $s = $it["id"] }
    if ($s) {
        $raw = $s.Replace("A-", "")
        if ($priceMap.ContainsKey($raw)) {
            $p = $priceMap[$raw]
            $it["o"] = $p.p_lista
            $it["p"] = $p.p_venta
            $updatedSearchCount++
        }
    }
}
Write-Output "Items actualizados en buscador: $updatedSearchCount"
$searchJsonNew = $ser.Serialize($searchItems)
[System.IO.File]::WriteAllText($searchMasterPath, $searchJsonNew, [System.Text.Encoding]::UTF8)
Write-Output "[OK] inventario_maestro_buscador.json guardado en pc-custom-lab ($([math]::Round($searchJsonNew.Length/1MB, 2)) MB)."

# ------------------------------------------------------------------------------
# FASE 3: REGENERAR js/ct-catalog-data.js Y data/departments/*.json
# ------------------------------------------------------------------------------
Write-Output "`n=================================================================="
Write-Output "FASE 3: ACTUALIZAR ct-catalog-data.js Y CHUNKING DE DEPARTAMENTOS"
Write-Output "=================================================================="

$catalogJsPath = Join-Path $baseDir "pc-custom-lab\js\ct-catalog-data.js"
$jsLines = [System.IO.File]::ReadAllLines($catalogJsPath, [System.Text.Encoding]::UTF8)

# Extraer departamentos
$deptLine = $jsLines | Where-Object { $_ -match "window\.PC_DEPARTAMENTOS =" } | Select-Object -First 1
$deptJson = $deptLine.Substring("window.PC_DEPARTAMENTOS = ".Length)
if ($deptJson.EndsWith(";")) { $deptJson = $deptJson.Substring(0, $deptJson.Length - 1) }
$deptsList = $ser.DeserializeObject($deptJson)
Write-Output "Departamentos detectados: $($deptsList.Length)"

# Extraer todos los productos de CT_CATALOG_DATA
$catDataLine = $jsLines | Where-Object { $_ -match "window\.CT_CATALOG_DATA =" } | Select-Object -First 1
$catDataJson = $catDataLine.Substring("window.CT_CATALOG_DATA = ".Length)
if ($catDataJson.EndsWith(";")) { $catDataJson = $catDataJson.Substring(0, $catDataJson.Length - 1) }
$catalogDataItems = $ser.DeserializeObject($catDataJson)
Write-Output "Productos en CT_CATALOG_DATA: $($catalogDataItems.Length)"

for ($i = 0; $i -lt $catalogDataItems.Length; $i++) {
    $it = $catalogDataItems[$i]
    $s = $it["s"]
    if ($s) {
        $raw = $s.Replace("A-", "")
        if ($priceMap.ContainsKey($raw)) {
            $p = $priceMap[$raw]
            $it["o"] = $p.p_lista
            $it["p"] = $p.p_venta
            $it["y"] = $p.p_mayoreo
        }
    }
}

# Tomar primeros 50 para INITIAL
$initialItems = $catalogDataItems[0..[Math]::Min(49, $catalogDataItems.Length - 1)]

# Reconstruir ct-catalog-data.js
$newJsContent = @"
// METADATOS OFICIALES DE DEPARTAMENTOS VECTEC (67 DEPARTAMENTOS)
window.PC_DEPARTAMENTOS = $($ser.Serialize($deptsList));

// SLICE INICIAL INSTANTANEO
window.CT_CATALOG_DATA_INITIAL = $($ser.Serialize($initialItems));

// CATALOGO COMPLETO COMPACTADO
window.CT_CATALOG_DATA = $($ser.Serialize($catalogDataItems));
"@

[System.IO.File]::WriteAllText($catalogJsPath, $newJsContent, [System.Text.Encoding]::UTF8)
Write-Output "[OK] pc-custom-lab/js/ct-catalog-data.js reescrito ($([math]::Round($newJsContent.Length/1MB, 2)) MB)."

# Particionar departamentos
$deptDir = Join-Path $baseDir "pc-custom-lab\data\departments"
if (-not (Test-Path $deptDir)) { New-Item -ItemType Directory -Path $deptDir -Force }

# Limpiar archivos json anteriores
Get-ChildItem -Path $deptDir -Filter "*.json" | Remove-Item -Force

$deptMap = @{}
foreach ($d in $deptsList) { $deptMap[$d["id"]] = [System.Collections.ArrayList]::new() }

foreach ($item in $catalogDataItems) {
    $cat = $item["c"]
    if (-not $cat) { $cat = "accesorios_perifericos" }
    if ($deptMap.ContainsKey($cat)) {
        [void]$deptMap[$cat].Add($item)
    } else {
        [void]$deptMap["accesorios_perifericos"].Add($item)
    }
}

$MAX_CHUNK_BYTES = 320 * 1024
$manifest = @{
    generatedAt = (Get-Date).ToString("o")
    totalProducts = $catalogDataItems.Length
    departmentsCount = $deptsList.Length
    departments = @{}
}

$totalDeptFiles = 0
foreach ($d in $deptsList) {
    $dId = $d["id"]
    $itemsInDept = $deptMap[$dId]
    $deptInfo = @{
        id = $dId
        name = $d["name"]
        icon = $d["icon"]
        order = $d["order"]
        count = $itemsInDept.Count
        files = @()
    }

    if ($itemsInDept.Count -eq 0) {
        $manifest["departments"][$dId] = $deptInfo
        continue
    }

    $fullJson = $ser.Serialize($itemsInDept)
    $fullBytes = [System.Text.Encoding]::UTF8.GetByteCount($fullJson)

    if ($fullBytes -le $MAX_CHUNK_BYTES) {
        $filename = "$dId.json"
        $filePath = Join-Path $deptDir $filename
        [System.IO.File]::WriteAllText($filePath, $fullJson, [System.Text.Encoding]::UTF8)
        $deptInfo["files"] += "data/departments/$filename"
        $totalDeptFiles++
    } else {
        $currentChunk = [System.Collections.ArrayList]::new()
        $currentBytes = 2
        $partIndex = 1

        for ($j = 0; $j -lt $itemsInDept.Count; $j++) {
            $itemStr = $ser.Serialize($itemsInDept[$j])
            $itemBytes = [System.Text.Encoding]::UTF8.GetByteCount($itemStr) + 1

            if (($currentBytes + $itemBytes -gt $MAX_CHUNK_BYTES) -and ($currentChunk.Count -gt 0)) {
                $filename = "${dId}_part_${partIndex}.json"
                $filePath = Join-Path $deptDir $filename
                [System.IO.File]::WriteAllText($filePath, $ser.Serialize($currentChunk), [System.Text.Encoding]::UTF8)
                $deptInfo["files"] += "data/departments/$filename"
                $totalDeptFiles++
                $partIndex++
                $currentChunk = [System.Collections.ArrayList]::new()
                $currentBytes = 2
            }

            [void]$currentChunk.Add($itemsInDept[$j])
            $currentBytes += $itemBytes
        }

        if ($currentChunk.Count -gt 0) {
            $filename = "${dId}_part_${partIndex}.json"
            $filePath = Join-Path $deptDir $filename
            [System.IO.File]::WriteAllText($filePath, $ser.Serialize($currentChunk), [System.Text.Encoding]::UTF8)
            $deptInfo["files"] += "data/departments/$filename"
            $totalDeptFiles++
        }
    }
    $manifest["departments"][$dId] = $deptInfo
}

$manifestPath = Join-Path $baseDir "pc-custom-lab\data\departments_manifest.json"
[System.IO.File]::WriteAllText($manifestPath, $ser.Serialize($manifest), [System.Text.Encoding]::UTF8)
Write-Output "[OK] Particionado completado: $totalDeptFiles archivos JSON creados en data/departments/."

# ------------------------------------------------------------------------------
# FASE 4: ACTUALIZAR ofertas-y-liquidaciones/catalog.csv
# ------------------------------------------------------------------------------
Write-Output "`n=================================================================="
Write-Output "FASE 4: RECÁLCULO DE OFERTAS-Y-LIQUIDACIONES (CERO PÉRDIDAS)"
Write-Output "=================================================================="

$ofertasCsvPath = Join-Path $baseDir "ofertas-y-liquidaciones\catalog.csv"
$ofertasRows = Import-Csv $ofertasCsvPath

$updatedOfertas = 0
foreach ($of in $ofertasRows) {
    $name = $of.nombre
    $match = $null
    if ($name -match "(i\d-\d{4,5}[A-Z]*|Ryzen \d \d{4,5}[A-Z]*|RTX \d{4}[A-Z\s]*|RX \d{4}[A-Z\s]*|Arc A\d{3})") {
        $term = $matches[1].Trim()
        $candidates = $ctRows | Where-Object { $_.nombre -match [regex]::Escape($term) }
        if ($candidates) { $match = $candidates[0] }
    }

    if ($match) {
        $sku = $match.sku.Trim()
        if ($priceMap.ContainsKey($sku)) {
            $p = $priceMap[$sku]
            $of.precio_original = $p.p_lista.ToString("F2")
            # En liquidacion outlet: 25% OFF regular o 30% OFF si es Refurb, siempre dejando >=20% neto
            if ($name -match "Refurb|Outlet") {
                $pOutlet = [math]::Round($p.costo * 1.54, 2) # 30% OFF sobre precio lista 2.20
                $of.precio = $pOutlet.ToString("F2")
                $of.descuento = "30% OFF"
            } else {
                $of.precio = $p.p_venta.ToString("F2") # 25% OFF sobre lista 2.20
                $of.descuento = "25% OFF"
            }
            $updatedOfertas++
        }
    }
}
$ofertasRows | Export-Csv -Path $ofertasCsvPath -NoTypeInformation -Encoding UTF8
Write-Output "[OK] ofertas-y-liquidaciones/catalog.csv actualizado con Factor 2.20 ($updatedOfertas SKUs reajustados sin pérdidas)."

# ------------------------------------------------------------------------------
# FASE 5: DISTRIBUCIÓN EN LAS 8 TIENDAS Y LA RAÍZ
# ------------------------------------------------------------------------------
Write-Output "`n=================================================================="
Write-Output "FASE 5: DISTRIBUCIÓN FÍSICA EN LOS 8 REPOSITORIOS Y RAÍZ"
Write-Output "=================================================================="

$targetStores = @(
    "pc-custom-lab",
    "VECTEC",
    "bazar-viamx-nfl.gdl",
    "cigarros-bazar",
    "dulces-bazar",
    "kiosco-digital",
    "mi-puesto-bazar",
    "ofertas-y-liquidaciones"
)

# Copiar a la raiz data/
$rootDataDir = Join-Path $baseDir "data"
if (-not (Test-Path $rootDataDir)) { New-Item -ItemType Directory -Path $rootDataDir -Force }
Copy-Item -Path $compactMasterPath -Destination (Join-Path $rootDataDir "catalogo_maestro_compact.json") -Force
Copy-Item -Path $searchMasterPath -Destination (Join-Path $rootDataDir "inventario_maestro_buscador.json") -Force
Copy-Item -Path $manifestPath -Destination (Join-Path $rootDataDir "departments_manifest.json") -Force

# Copiar carpetas departments/ a la raiz data/
$rootDeptDir = Join-Path $rootDataDir "departments"
if (-not (Test-Path $rootDeptDir)) { New-Item -ItemType Directory -Path $rootDeptDir -Force }
Copy-Item -Path "$deptDir\*" -Destination $rootDeptDir -Force

foreach ($st in $targetStores) {
    $stData = Join-Path $baseDir "$st\data"
    if (-not (Test-Path $stData)) { New-Item -ItemType Directory -Path $stData -Force }

    # 1. Copiar compact y search
    Copy-Item -Path $compactMasterPath -Destination (Join-Path $stData "catalogo_maestro_compact.json") -Force
    Copy-Item -Path $searchMasterPath -Destination (Join-Path $stData "inventario_maestro_buscador.json") -Force
    Copy-Item -Path $manifestPath -Destination (Join-Path $stData "departments_manifest.json") -Force

    # 2. Copiar departments si aplica
    $stDeptDir = Join-Path $stData "departments"
    if (-not (Test-Path $stDeptDir)) { New-Item -ItemType Directory -Path $stDeptDir -Force }
    Copy-Item -Path "$deptDir\*" -Destination $stDeptDir -Force

    # 3. Sincronizar aparador_200.json
    $aparadorPath = Join-Path $stData "catalogo_aparador_200.json"
    if (Test-Path $aparadorPath) {
        $apRaw = [System.IO.File]::ReadAllText($aparadorPath, [System.Text.Encoding]::UTF8)
        $apItems = $ser.DeserializeObject($apRaw)
        $apCambios = 0
        for ($k = 0; $k -lt $apItems.Length; $k++) {
            $it = $apItems[$k]
            $s = $it["sku"]
            if (-not $s) { $s = $it["s"] }
            if ($s) {
                $raw = $s.Replace("A-", "")
                if ($priceMap.ContainsKey($raw)) {
                    $p = $priceMap[$raw]
                    $it["precio"] = $p.p_venta
                    $it["p"] = $p.p_venta
                    $it["precio_original"] = $p.p_lista
                    $it["o"] = $p.p_lista
                    $it["precio_mayoreo"] = $p.p_mayoreo
                    $it["y"] = $p.p_mayoreo
                    $it["descuento_pct"] = 25
                    $apCambios++
                }
            }
        }
        [System.IO.File]::WriteAllText($aparadorPath, $ser.Serialize($apItems), [System.Text.Encoding]::UTF8)
        Write-Output "   -> $st : catalogo_aparador_200.json sincronizado ($apCambios productos ajustados)."
    }

    # 4. En VECTEC sincronizar js
    if ($st -eq "VECTEC") {
        $vectecJs = Join-Path $baseDir "VECTEC\js"
        if (-not (Test-Path $vectecJs)) { New-Item -ItemType Directory -Path $vectecJs -Force }
        Copy-Item -Path $catalogJsPath -Destination (Join-Path $vectecJs "ct-catalog-data.js") -Force
        Copy-Item -Path (Join-Path $baseDir "pc-custom-lab\js\ct-search-engine.js") -Destination (Join-Path $vectecJs "ct-search-engine.js") -Force -ErrorAction SilentlyContinue
    }
}
Write-Output "[OK] Archivos replicados en las 8 tiendas y la raiz con total paridad."