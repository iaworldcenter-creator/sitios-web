@echo off
title Abrir VíaMX Local
echo ==============================================================================
echo                 ESCUDERÍA ANTIGRAVITY 2.0 - INICIADOR LOCAL VIA MX
echo ==============================================================================
echo.
echo Intentando iniciar servidor local de alta velocidad (Python)...
echo.

:: Buscar si python está disponible en la ASUS Frankenstein
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] Python detectado. Iniciando servidor en http://localhost:8080...
    echo.
    echo [GATEWAY] Lanzando enrutador dinámico en puerto 8082...
    start /b python pipeline_viamx_2026.py
    echo [AGENTE] Lanzando monitor verificador de enlaces (Ollama)...
    start /b python agent_checker_ollama.py
    echo.
    echo Manten esta ventana abierta mientras navegas. Para cerrar el servidor, presiona CTRL+C.
    echo.
    
    :: Abrir el navegador por defecto
    start http://localhost:8080/index.html
    
    :: Iniciar servidor HTTP ligero
    python -m http.server 8080
) else (
    echo [ADVERTENCIA] Python no esta instalado en este sistema.
    echo Abriendo index.html directamente en el navegador por defecto (Protocolo de Archivo)...
    echo.
    start "" "index.html"
)
