@echo off
REM Script para preparar paquete de distribución SANARTE
REM Ejecutar después de generar el .exe con PyInstaller

echo ================================================================================
echo PREPARANDO PAQUETE DE DISTRIBUCIÓN SANARTE v1.3
echo ================================================================================
echo.

REM Verificar que existe el ejecutable
if not exist "dist\SANARTE.exe" (
    echo [ERROR] No se encontró dist\SANARTE.exe
    echo.
    echo Primero debes generar el ejecutable con:
    echo   python build_exe.py
    echo.
    pause
    exit /b 1
)

REM Crear carpeta de distribución
set DIST_DIR=SANARTE_v1.3_Distribucion
echo Creando carpeta de distribución: %DIST_DIR%
if exist %DIST_DIR% rmdir /s /q %DIST_DIR%
mkdir %DIST_DIR%

REM Copiar ejecutable
echo Copiando SANARTE.exe...
copy "dist\SANARTE.exe" "%DIST_DIR%\" >nul

REM Crear carpetas input y output
echo Creando carpetas input y output...
mkdir "%DIST_DIR%\input"
mkdir "%DIST_DIR%\output"

REM Copiar archivo LEEME
echo Copiando instrucciones de uso...
copy "LEEME_USUARIOS.txt" "%DIST_DIR%\LEEME.txt" >nul

REM Crear archivo de ejemplo en input
echo Creando archivo de ejemplo...
(
echo Este es un ejemplo de cómo debe verse tu extracto bancario.
echo.
echo Pasos:
echo 1. Elimina este archivo
echo 2. Copia aquí tu extracto bancario en formato .xlsx
echo 3. Ejecuta SANARTE.exe
) > "%DIST_DIR%\input\COLOCA_TU_EXTRACTO_AQUI.txt"

REM Crear ZIP
echo.
echo Comprimiendo a ZIP...
powershell Compress-Archive -Path "%DIST_DIR%" -DestinationPath "%DIST_DIR%.zip" -Force

echo.
echo ================================================================================
echo PAQUETE DE DISTRIBUCIÓN CREADO EXITOSAMENTE
echo ================================================================================
echo.
echo Carpeta: %DIST_DIR%
echo ZIP:     %DIST_DIR%.zip
echo Tamaño:
for %%A in ("%DIST_DIR%.zip") do echo   %%~zA bytes
echo.
echo Para distribuir:
echo   1. Envía el archivo %DIST_DIR%.zip por email/Drive
echo   2. O copia la carpeta %DIST_DIR% a un pendrive
echo.
echo Instrucciones para usuarios incluidas en LEEME.txt
echo.
pause
