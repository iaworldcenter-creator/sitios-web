@echo off
setlocal
chcp 65001 >nul
title VECTEC - Terminal Mostrador POS (Pedro Moreno 501 A)
color 0b

echo ===============================================================================
echo          VECTEC - TERMINAL DE PUNTO DE VENTA / MODO MOSTRADOR
echo          Local Fisico: Pedro Moreno 501 A, Guadalajara Centro
echo ===============================================================================
echo:
echo [*] Iniciando estacion de mostrador en modo aplicacion dedicada (Edge POS)...
echo [*] Modo Kiosco / App Nativa: sin barras de navegacion, maximizado y a pantalla completa.
echo:

:: Buscar ejecutable de Microsoft Edge
set "EDGE_CMD=msedge.exe"
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    set "EDGE_CMD=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
) else if exist "C:\Program Files\Microsoft\Edge\Application\msedge.exe" (
    set "EDGE_CMD=C:\Program Files\Microsoft\Edge\Application\msedge.exe"
)

:: Lanzar Microsoft Edge en modo aplicacion dedicada a pantalla completa
start "" "%EDGE_CMD%" --app="file:///D:/Proyectos/sitios web/VECTEC/mostrador.html" --start-fullscreen

echo [OK] Estacion de mostrador iniciada con exito.
timeout /t 2 >nul
exit
