@echo off
REM Launcher para TORO.exe que asegura stdin disponible
REM Este archivo soluciona el problema "lost sys.stdin"

cd /d "%~dp0"

echo.
echo ================================================================================
echo   TORO - Sistema de Control Financiero
echo   Iniciando...
echo ================================================================================
echo.

REM Verificar si existe el ejecutable
if not exist "TORO.exe" (
    echo [ERROR] No se encuentra TORO.exe en esta carpeta.
    echo Por favor, asegurate de que TORO.exe este en la misma carpeta que este archivo.
    pause
    exit /b 1
)

REM Ejecutar TORO.exe con stdin disponible
"%~dp0TORO.exe"

REM Si hay error, mostrar mensaje
if errorlevel 1 (
    echo.
    echo [ERROR] El programa termino con un error.
    echo.
    pause
)

exit /b 0
