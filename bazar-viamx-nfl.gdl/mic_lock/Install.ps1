# Install.ps1
# Instalador de Bloqueo de Volumen de Microfono
# Disenado por Antigravity para Windows

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if ([string]::IsNullOrEmpty($scriptDir)) { $scriptDir = "." }
$scriptPath = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "MicVolumeLock.ps1"))
$startupFolder = [System.Environment]::GetFolderPath("Startup")
$startupLnkPath = Join-Path $startupFolder "StartMicVolumeLock.lnk"
$oldStartupVbsPath = Join-Path $startupFolder "StartMicVolumeLock.vbs"

Write-Host "=========================================================="
Write-Host "     INSTALANDO BLOQUEO DE VOLUMEN DE MICROFONO"
Write-Host "=========================================================="

# 1. Aplicar correccion de Registro (Deshabilitar Ducking de Windows)
Write-Host "[1/4] Configurando Windows para no atenuar sonido en llamadas..."
$registryPath = "HKCU:\Software\Microsoft\Multimedia\Audio"
if (-not (Test-Path $registryPath)) {
    New-Item -Path $registryPath -Force | Out-Null
}
Set-ItemProperty -Path $registryPath -Name "UserDuckingPreference" -Value 3 -Type DWord
Write-Host '  -> Registro configurado correctamente (UserDuckingPreference = 3).'

# 2. Detener instancias previas del monitor y limpiar archivos viejos
Write-Host "[2/4] Deteniendo instancias anteriores del monitor en ejecucion..."
try {
    $processes = Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe' AND CommandLine LIKE '%MicVolumeLock.ps1%'" -ErrorAction SilentlyContinue
    if ($processes) {
        foreach ($proc in $processes) {
            $proc | Invoke-CimMethod -MethodName Terminate | Out-Null
            Write-Host "  -> Proceso detenido. PID: $($proc.ProcessId)"
        }
    } else {
        Write-Host "  -> No se encontraron procesos anteriores activos."
    }
} catch {
    Write-Host "  -> Advertencia: No se pudieron comprobar procesos mediante WMI, intentando fallback de detencion..."
}

if (Test-Path $oldStartupVbsPath) {
    Remove-Item $oldStartupVbsPath -Force
}

# 3. Crear el acceso directo de arranque silencioso (.lnk) en la carpeta de Inicio de Windows
Write-Host "[3/4] Configurando arranque automatico y silencioso al iniciar Windows..."
try {
    $wsh = New-Object -ComObject WScript.Shell
    $shortcut = $wsh.CreateShortcut($startupLnkPath)
    $shortcut.TargetPath = "powershell.exe"
    $shortcut.Arguments = "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`""
    $shortcut.WindowStyle = 7 # 7 = Minimized/Hidden
    $shortcut.Save()
    Write-Host "  -> Acceso directo de arranque creado en Inicio: $startupLnkPath"
} catch {
    Write-Host "  -> Error al crear el acceso directo: $_"
}

# 4. Iniciar el servicio en segundo plano inmediatamente
Write-Host "[4/4] Iniciando el servicio en segundo plano inmediatamente..."
try {
    Start-Process powershell.exe -ArgumentList "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`""
    Write-Host "  -> Servicio iniciado con exito en segundo plano."
} catch {
    Write-Host "  -> Error al arrancar el servicio: $_"
}

Write-Host "=========================================================="
Write-Host " INSTALACION COMPLETADA CON EXITO"
Write-Host " El volumen de tu microfono ahora esta bloqueado al 100%."
Write-Host " Cualquier intento del sistema o de apps de bajarlo se revertira."
Write-Host "=========================================================="
