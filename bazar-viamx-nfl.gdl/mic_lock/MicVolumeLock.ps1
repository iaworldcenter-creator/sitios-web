# MicVolumeLock.ps1
# Monitor y Bloqueo de Volumen de Microfono
# Disenado por Antigravity para Windows

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if ([string]::IsNullOrEmpty($scriptDir)) { $scriptDir = "." }
$env:TEMP = $scriptDir
$env:TMP = $scriptDir
$configFile = Join-Path $scriptDir "config.json"
$logFile = Join-Path $scriptDir "activity.log"

# Asegurar existencia del archivo de configuracion inicial
if (-not (Test-Path $configFile)) {
    @{
        TargetVolume = 1.0
        Enabled = $true
    } | ConvertTo-Json | Out-File $configFile -Encoding utf8
}

# Cargar configuracion o usar valores por defecto
function Get-TargetVolume {
    if (Test-Path $configFile) {
        try {
            $config = Get-Content $configFile -Raw | ConvertFrom-Json
            if ($config.TargetVolume -ne $null) {
                $vol = [float]$config.TargetVolume
                if ($vol -lt 0) { $vol = 0.0 }
                if ($vol -gt 1.0) { $vol = 1.0 }
                return $vol
            }
        } catch {}
    }
    return 1.0 # 100% por defecto
}

# Obtener si el servicio esta activo o pausado
function Get-EnabledState {
    if (Test-Path $configFile) {
        try {
            $config = Get-Content $configFile -Raw | ConvertFrom-Json
            if ($config.Enabled -ne $null) {
                return [bool]$config.Enabled
            }
        } catch {}
    }
    return $true
}

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
    public static bool SetMicrophoneVolume(float volume) {
        try {
            if (volume < 0 || volume > 1) return false;
            var enumerator = new MMDeviceEnumeratorComObject() as IMMDeviceEnumerator;
            if (enumerator == null) return false;
            IMMDevice dev = null;
            int hr = enumerator.GetDefaultAudioEndpoint(1, 1, out dev);
            if (hr != 0 || dev == null) return false;
            
            IAudioEndpointVolume epv = null;
            var epvid = typeof(IAudioEndpointVolume).GUID;
            hr = dev.Activate(ref epvid, 23, 0, out epv);
            if (hr != 0 || epv == null) return false;
            
            epv.SetMasterVolumeLevelScalar(volume, Guid.Empty);
            return true;
        } catch {
            return false;
        }
    }
    
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

# Compilar codigo de audio en la sesion
try {
    Add-Type -TypeDefinition $AudioCode -Language CSharp
} catch {
    # Si ya se cargo en esta misma sesion de PowerShell, ignorar el error de tipo duplicado
}

Write-Host "=========================================================="
Write-Host "  SERVICIO DE BLOQUEO DE VOLUMEN DE MICROFONO ACTIVADO  "
Write-Host "=========================================================="
Write-Host "Configuracion: $configFile"
Write-Host "Registro de actividad: $logFile"

# Registrar inicio
$startMsg = @{
    Time = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    Type = "Sistema"
    Message = "Servicio de monitoreo iniciado. Nivel objetivo: $((Get-TargetVolume)*100)%."
}
Add-Content -Path $logFile -Value (ConvertTo-Json -Compress $startMsg)

# Bucle principal de monitoreo
$lastUsbAudioCount = @(Get-CimInstance -ClassName Win32_PnPEntity | Where-Object { $_.Service -eq 'usbaudio' } -ErrorAction SilentlyContinue).Count
$wasDisconnected = $false

while ($true) {
    if (Get-EnabledState) {
        $targetVolume = Get-TargetVolume
        $currentVolume = [AudioController]::GetMicrophoneVolume()
        
        # 1. Detectar reconexión por cambio en cantidad de dispositivos USB Audio
        $currentUsbAudioCount = @(Get-CimInstance -ClassName Win32_PnPEntity | Where-Object { $_.Service -eq 'usbaudio' } -ErrorAction SilentlyContinue).Count
        $triggerRestart = $false
        
        if ($currentUsbAudioCount -gt $lastUsbAudioCount) {
            Write-Host "$(Get-Date -Format 'HH:mm:ss') - Se detectó la reconexión física de un dispositivo de audio USB."
            $triggerRestart = $true
        }
        $lastUsbAudioCount = $currentUsbAudioCount
        
        # 2. Detectar reconexión por restablecimiento del micrófono predeterminado de Windows
        if ($currentVolume -lt 0) {
            if (-not $wasDisconnected) {
                $wasDisconnected = $true
                Write-Host "$(Get-Date -Format 'HH:mm:ss') - Micrófono predeterminado desconectado de Windows."
                $logMsg = @{
                    Time = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
                    Type = "Desconexion"
                    Message = "El micrófono se ha desconectado o no está disponible en Windows."
                }
                Add-Content -Path $logFile -Value (ConvertTo-Json -Compress $logMsg)
            }
        } else {
            if ($wasDisconnected) {
                Write-Host "$(Get-Date -Format 'HH:mm:ss') - Micrófono predeterminado de Windows restablecido."
                $triggerRestart = $true
                $wasDisconnected = $false
            }
        }
        
        # 3. Si se detectó reconexión, enviar comando de reinicio al motor de Voicemeeter
        if ($triggerRestart) {
            $logMsg = @{
                Time = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
                Type = "Reconexion"
                Message = "Dispositivo de audio reconectado. Reiniciando motor de audio de Voicemeeter."
            }
            Add-Content -Path $logFile -Value (ConvertTo-Json -Compress $logMsg)
            
            $vmPaths = @(
                "C:\Program Files (x86)\VB\Voicemeeter\voicemeeterpro_x64.exe",
                "C:\Program Files (x86)\VB\Voicemeeter\voicemeeterpro.exe",
                "C:\Program Files (x86)\VB\Voicemeeter\voicemeeter_x64.exe",
                "C:\Program Files (x86)\VB\Voicemeeter\voicemeeter.exe"
            )
            foreach ($vmPath in $vmPaths) {
                if (Test-Path $vmPath) {
                    try {
                        Start-Process -FilePath $vmPath -ArgumentList "-R" -ErrorAction SilentlyContinue
                        Write-Host "  -> Enviado reinicio de motor a: $vmPath"
                        break
                    } catch {}
                }
            }
        }
        
        # 4. Asegurar volumen del micrófono si está conectado
        if ($currentVolume -ge 0) {
            # Margen de tolerancia de 1%
            $difference = [Math]::Abs($currentVolume - $targetVolume)
            if ($difference -gt 0.01) {
                $pctCurrent = [Math]::Round($currentVolume * 100)
                $pctTarget = [Math]::Round($targetVolume * 100)
                Write-Host "$(Get-Date -Format 'HH:mm:ss') - Volumen en: $pctCurrent%. Corrigiendo a $pctTarget%..."
                $success = [AudioController]::SetMicrophoneVolume($targetVolume)
                if ($success) {
                    $logMsg = @{
                        Time = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
                        Type = "Restauracion"
                        Message = "Volumen detectado en ${pctCurrent}%. Restablecido a ${pctTarget}%."
                    }
                    Add-Content -Path $logFile -Value (ConvertTo-Json -Compress $logMsg)
                }
            }
        }
        
        # Mantener el log bajo control (maximo 100KB)
        if ((Test-Path $logFile) -and (Get-Item $logFile).Length -gt 100KB) {
            $lines = Get-Content $logFile -Tail 50
            $lines | Out-File $logFile -Encoding utf8
        }
    }
    Start-Sleep -Seconds 2
}
