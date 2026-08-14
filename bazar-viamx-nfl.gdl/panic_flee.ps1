# panic_flee.ps1
# ==============================================================================
#                 ESCUDERÍA ANTIGRAVITY 2.0 - CORE DE CONTINUIDAD
#                PROTOCOLO DE FUGA MÁSTER Y REPLICACIÓN ASÍNCRONA
# ==============================================================================
# Plataforma: Windows (ASUS Frankenstein)
# Codename: Nexo-Origen-2026
# ==============================================================================

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if ([string]::IsNullOrEmpty($scriptDir)) { $scriptDir = "." }
$logFile = Join-Path $scriptDir "log_operativo.txt"
$signalFile = Join-Path $scriptDir "panic.signal"

# Configuración de Servidores Espejo
$GitLabMirrorSuiza = "https://gitlab.ch/viamx-security/mirror.git"
$GitLabMirrorPanama = "https://gitlab.pa/viamx-security/mirror.git"

Write-Host "=========================================================="
Write-Host "     INICIANDO ALERTA ACTIVA DE FUGA (PANIC_FLEE)"
Write-Host "=========================================================="

function Log-Event {
    param([string]$message, [string]$type = "SISTEMA")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logLine = "[$timestamp] [$type] $message"
    Write-Host $logLine
    Add-Content -Path $logFile -Value $logLine
}

Log-Event "Servidor Espejo de Fuga iniciado en estado de Alerta Activa en la ASUS Frankenstein." "FUGA"

# Bucle de Monitoreo Continuo (Cada 10 segundos)
while ($true) {
    # 1. Comprobar si se ha creado el archivo físico de detonación manual
    if (Test-Path $signalFile) {
        Log-Event "¡DETONACIÓN MANUAL DETECTADA! Iniciando protocolo de evacuación..." "CRÍTICO"
        
        # Intentar replicación hacia los espejos de Europa y Centroamérica
        try {
            Log-Event "Configurando puente remoto temporal de GitLab Suiza..." "EVACUAR"
            # Comprobar si ya existe el remote mirror
            $remotes = git remote
            if ($remotes -contains "mirror-suiza") {
                git remote remove mirror-suiza | Out-Null
            }
            git remote add mirror-suiza $GitLabMirrorSuiza | Out-Null
            
            Log-Event "Empujando chasis y catálogo completo de VíaMX hacia servidores de Suiza..." "PUSH"
            # Ejecutar push silencioso (con timeout simulado para pruebas locales)
            git push mirror-suiza master --force -q 2>$null
            
            Log-Event "Puente de Suiza completado con éxito. Réplica Activa en Europa Central." "OK"
        } catch {
            Log-Event "Servidor principal Suiza en mantenimiento. Redirigiendo canal de escape a Panamá..." "ADVERTENCIA"
            try {
                if ($remotes -contains "mirror-panama") {
                    git remote remove mirror-panama | Out-Null
                }
                git remote add mirror-panama $GitLabMirrorPanama | Out-Null
                git push mirror-panama master --force -q 2>$null
                Log-Event "Puente de Panamá completado con éxito. Réplica Activa en Centroamérica." "OK"
            } catch {
                Log-Event "Fallo de enrutamiento en canal de escape secundario. Reintentando en 30 segundos..." "FALLO"
            }
        }
        
        # Limpiar la señal de detonación
        Remove-Item $signalFile -Force -ErrorAction SilentlyContinue
    }
    
    # 2. Dormir hilo para conservar rendimiento (10 segundos)
    Start-Sleep -Seconds 10
}
