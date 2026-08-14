# disable_power_mgmt.ps1
# Script de remediación de ahorro de energía para USB y Audio
# Diseñado por Antigravity para Windows (Requiere privilegios de Administrador)

$logFile = "d:\Downloads\Proyecto Web\mic_lock\activity.log"
$timeStr = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log ($message, $type="Remediacion") {
    $logMsg = @{
        Time = $timeStr
        Type = $type
        Message = $message
    }
    Add-Content -Path $logFile -Value (ConvertTo-Json -Compress $logMsg)
    Write-Host "$timeStr [$type] $message"
}

Write-Log "Iniciando remediación de energía de dispositivos..."

# 1. Configurar powercfg para deshabilitar la suspensión selectiva de USB
try {
    # Obtener el esquema de energía actual
    $activeScheme = (powercfg /getactivescheme).Split(' ')[3]
    
    powercfg /setacvalueindex $activeScheme sub_usb subusb 0
    powercfg /setdcvalueindex $activeScheme sub_usb subusb 0
    powercfg /setactive $activeScheme
    Write-Log "Suspensión selectiva de USB desactivada en el plan de energía ($activeScheme) para AC y DC."
} catch {
    Write-Log "Error al configurar powercfg: $_" "Error"
}

# 2. Deshabilitar ahorro de energía en WMI (MSPower_DeviceEnable) para concentradores USB, controladoras y audio
try {
    $devices = Get-CimInstance -ClassName MSPower_DeviceEnable -Namespace root\wmi
    $count = 0
    
    foreach ($d in $devices) {
        # Filtrar dispositivos críticos: USB hubs, controladoras PCI y dispositivos de Audio
        if ($d.InstanceName -like "*USB*" -or $d.InstanceName -like "*PCI\VEN_*" -or $d.InstanceName -like "*HDAUDIO*") {
            if ($d.Enable -eq $true) {
                $d.Enable = $false
                Set-CimInstance -InputObject $d
                Write-Log "Deshabilitado 'Permitir al equipo apagar este dispositivo para ahorrar energía' para: $($d.InstanceName)"
                $count++
            }
        }
    }
    
    Write-Log "Se deshabilitó el ahorro de energía en $count dispositivos críticos."
} catch {
    Write-Log "Error al configurar WMI MSPower_DeviceEnable: $_" "Error"
}

Write-Log "Remediación de energía de dispositivos completada con éxito."
