@echo off
REM Launcher para SANARTE.exe que asegura stdin disponible
REM Este archivo soluciona el problema "lost sys.stdin"

cd /d "%~dp0"

echo.
echo ================================================================================
echo   SANARTE - Sistema de Control Financiero
echo   Iniciando...
echo ================================================================================
echo.

REM Verificar si existe el ejecutable
if not exist "SANARTE.exe" (
    echo [ERROR] No se encuentra SANARTE.exe en esta carpeta.
    echo Por favor, asegurate de que SANARTE.exe este en la misma carpeta que este archivo.
    pause
    exit /b 1
)

REM Ejecutar SANARTE.exe con stdin disponible
"%~dp0SANARTE.exe"

REM Si hay error, mostrar mensaje
if errorlevel 1 (
    echo.
    echo [ERROR] El programa termino con un error.
    echo.
    pause
)

exit /b 0
