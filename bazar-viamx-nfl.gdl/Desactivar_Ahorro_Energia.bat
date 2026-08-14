@echo off
chcp 65001 > nul
echo ==========================================================
echo   DESACTIVANDO AHORRO DE ENERGÍA DE USB Y AUDIO
echo ==========================================================
echo.

:: Verificar si se ejecuta como Administrador
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Ejecutando con privilegios de Administrador.
    echo Ejecutando script de remediación...
    powershell -ExecutionPolicy Bypass -File "%~dp0mic_lock\disable_power_mgmt.ps1"
    echo.
    echo Remediación completada.
    pause
) else (
    echo [INFO] Solicitando elevación de Administrador...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
)
