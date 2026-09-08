@echo off
setlocal
chcp 65001 >nul
title VECTEC - Actualizador de Inventario y Sincronizacion de Datos
color 0b

echo ===============================================================================
echo          VECTEC - SISTEMA CENTRAL DE SINCRONIZACION DE INVENTARIO
echo ===============================================================================
echo [*] Verificando entorno de ejecucion Python...
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXEC=%~dp0.venv\Scripts\python.exe"
    echo [+] Utilizando entorno virtual local (.venv con soporte WebP)
) else (
    set "PYTHON_EXEC=python"
    echo [!] Utilizando Python del sistema
)

echo [*] Procesando catalogos multi-proveedor (CT Internacional Clave A + Intcomex Clave B)...
echo [*] Optimizando costos de adquisicion, imagenes reales y cascada de datos...
echo:

%PYTHON_EXEC% "%~dp0scripts\sincronizar_fuente_datos.py"

if errorlevel 1 goto error_handler

echo:
echo ===============================================================================
echo [EXITO] Sincronizacion multi-proveedor VECTEC completada correctamente.
echo ===============================================================================
goto end_script

:error_handler
echo:
echo ===============================================================================
echo [ERROR] Ocurrio un problema durante la sincronizacion.
echo ===============================================================================

:end_script
echo:
pause
endlocal
