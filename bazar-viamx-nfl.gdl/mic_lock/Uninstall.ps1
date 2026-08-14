# Uninstall.ps1
# Desinstalador de Bloqueo de Volumen de Microfono
# Disenado por Antigravity para Windows

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if ([string]::IsNullOrEmpty($scriptDir)) { $scriptDir = "." }
$startupFolder = [System.Environment]::GetFolderPath("Startup")
$startupLnkPath = Join-Path $startupFolder "StartMicVolumeLock.lnk"
$startupVbsPath = Join-Path $startupFolder "StartMicVolumeLock.vbs"
$logFile = Join-Path $scriptDir "activity.log"

Write-Host "=========================================================="
Write-Host "     DESINSTALANDO BLOQUEO DE VOLUMEN DE MICROFONO"
Write-Host "=========================================================="

# 1. Detener procesos activos
Write-Host "[1/3] Deteniendo el servicio monitor en segundo plano..."
try {
    $processes = Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe' AND CommandLine LIKE '%MicVolumeLock.ps1%'" -ErrorAction SilentlyContinue
    if ($processes) {
        foreach ($proc in $processes) {
            $proc | Invoke-CimMethod -MethodName Terminate | Out-Null
            Write-Host "  -> Proceso detenido. PID: $($proc.ProcessId)"
        }
    } else {
        Write-Host "  -> No hay procesos del monitor activos en segundo plano."
    }
} catch {
    Write-Host "  -> Advertencia: No se pudieron comprobar procesos mediante WMI, intentando fallback de detencion..."
}

# 2. Eliminar el cargador de inicio de Windows
Write-Host "[2/3] Eliminando el inicio automatico con Windows..."
if (Test-Path $startupLnkPath) {
    Remove-Item $startupLnkPath -Force
    Write-Host "  -> Acceso directo de inicio eliminado: $startupLnkPath"
}
if (Test-Path $startupVbsPath) {
    Remove-Item $startupVbsPath -Force
}
Write-Host "  -> Cargadores automaticos limpios."

# 3. Restaurar atenuacion de audio de Windows a su valor predeterminado
Write-Host "[3/3] Restaurando preferencias de audio predeterminadas de Windows..."
$registryPath = "HKCU:\Software\Microsoft\Multimedia\Audio"
if (Test-Path $registryPath) {
    # 1 = Reducir el volumen de otros sonidos un 80% (Predeterminado de Windows)
    Set-ItemProperty -Path $registryPath -Name "UserDuckingPreference" -Value 1 -Type DWord
    Write-Host '  -> Preferencia de sonido de comunicaciones restaurada a por defecto (80%).'
}

# 4. Opcional: Eliminar archivos de registro y configuracion
$configFile = Join-Path $scriptDir "config.json"
if (Test-Path $configFile) {
    Remove-Item $configFile -Force
}
if (Test-Path $logFile) {
    Remove-Item $logFile -Force
}

Write-Host "=========================================================="
Write-Host " DESINSTALACION COMPLETADA CON EXITO"
Write-Host " El servicio de bloqueo de microfono se ha removido."
Write-Host "=========================================================="
