# Status.ps1
# Diagnostico de Estado de Bloqueo de Volumen de Microfono
# Disenado por Antigravity para Windows

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if ([string]::IsNullOrEmpty($scriptDir)) { $scriptDir = "." }
$env:TEMP = $scriptDir
$env:TMP = $scriptDir
$configFile = Join-Path $scriptDir "config.json"
$logFile = Join-Path $scriptDir "activity.log"

Write-Host "=========================================================="
Write-Host " ESTADO DEL BLOQUEO DE VOLUMEN DE MICROFONO"
Write-Host "=========================================================="

# 1. Verificar si el proceso esta corriendo
$running = $false
try {
    $processes = Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe' AND CommandLine LIKE '%MicVolumeLock.ps1%'" -ErrorAction SilentlyContinue
    if ($processes) {
        $running = $true
        Write-Host "Estado del Servicio:  [ACTIVO] (Ejecutandose en segundo plano)" -ForegroundColor Green
        foreach ($proc in $processes) {
            Write-Host "  -> PID del Proceso:  $($proc.ProcessId)"
            Write-Host "  -> Hora de inicio:   $($proc.CreationDate)"
        }
    } else {
        Write-Host "Estado del Servicio:  [INACTIVO] (No se esta ejecutando)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Estado del Servicio:  Indeterminado (Error al consultar procesos)" -ForegroundColor Red
}

# 2. Cargar configuracion y volumen actual
$targetPct = "100%"
if (Test-Path $configFile) {
    try {
        $config = Get-Content $configFile -Raw | ConvertFrom-Json
        if ($config.TargetVolume -ne $null) {
            $targetPct = "$([Math]::Round($config.TargetVolume * 100))%"
        }
    } catch {}
}

# Obtener volumen en tiempo real usando el codigo de audio nativo
$AudioCode = '
using System;
using System.Runtime.InteropServices;

[Guid("5CDF2C82-841E-4546-9722-0CF74078229A"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioEndpointVolume {
    int f1(); int f2(); int f3(); int f4();
    int SetMasterVolumeLevelScalar(float fLevel, Guid pguidEventContext);
    int f6();
    int GetMasterVolumeLevelScalar(out float pfLevel);
    int f8(); int f9(); int f10(); int f11();
    int SetMute([MarshalAs(UnmanagedType.Bool)] bool bMute, Guid pguidEventContext);
    int GetMute(out bool pbMute);
}

[Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDevice {
    int Activate(ref Guid id, int clsCtx, int activationParams, out IAudioEndpointVolume aev);
}

[Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDeviceEnumerator {
    int f1();
    int GetDefaultAudioEndpoint(int dataFlow, int role, out IMMDevice endpoint);
}

[ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")]
class MMDeviceEnumeratorComObject { }

public class AudioController {
    public static float GetMicrophoneVolume() {
        try {
            var enumerator = new MMDeviceEnumeratorComObject() as IMMDeviceEnumerator;
            if (enumerator == null) return -1f;
            IMMDevice dev = null;
            int hr = enumerator.GetDefaultAudioEndpoint(1, 1, out dev);
            if (hr != 0 || dev == null) return -1f;
            
            IAudioEndpointVolume epv = null;
            var epvid = typeof(IAudioEndpointVolume).GUID;
            hr = dev.Activate(ref epvid, 23, 0, out epv);
            if (hr != 0 || epv == null) return -1f;
            
            float volume = 0f;
            hr = epv.GetMasterVolumeLevelScalar(out volume);
            if (hr != 0) return -1f;
            return volume;
        } catch {
            return -1f;
        }
    }
}
'

try {
    Add-Type -TypeDefinition $AudioCode -Language CSharp -ErrorAction SilentlyContinue
} catch {}

$currentVol = [AudioController]::GetMicrophoneVolume()
if ($currentVol -ge 0) {
    $currentPct = "$([Math]::Round($currentVol * 100))%"
    $color = if ($currentVol -lt 0.95) { "Yellow" } else { "Green" }
    Write-Host "Volumen Objetivo:     $targetPct"
    Write-Host "Volumen Actual Mic:   $currentPct" -ForegroundColor $color
} else {
    Write-Host "Volumen Objetivo:     $targetPct"
    Write-Host "Volumen Actual Mic:   Error al leer (Microfono desconectado?)" -ForegroundColor Red
}

# 3. Mostrar ultimas actividades
Write-Host ""
Write-Host "Ultimos eventos en el registro:"
if (Test-Path $logFile) {
    $logs = Get-Content $logFile -Tail 5
    if ($logs) {
        foreach ($line in $logs) {
            try {
                $entry = $line | ConvertFrom-Json
                Write-Host "[$($entry.Time)] [$($entry.Type)] $($entry.Message)"
            } catch {
                Write-Host $line
            }
        }
    } else {
        Write-Host "  -> Registro vacio."
    }
} else {
    Write-Host "  -> No hay archivo de registro aun."
}
Write-Host "=========================================================="
