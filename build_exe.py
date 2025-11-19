"""
Script de build para generar ejecutable SANARTE.exe
Ejecutar: python build_exe.py
"""
import os
import subprocess
import shutil

# Configuración
APP_NAME = "SANARTE"
VERSION = "1.3"
ICON = "sanarte_icon.ico"  # Opcional: agregar icono personalizado

# Limpiar builds anteriores
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

print("="*80)
print(f"GENERANDO EJECUTABLE {APP_NAME} v{VERSION}")
print("="*80)

# Comando PyInstaller
comando = [
    'pyinstaller',
    '--name', APP_NAME,
    '--onefile',                    # Un solo .exe
    '--windowed',                   # Sin consola negra (opcional)
    '--add-data', 'src;src',        # Incluir carpeta src
    '--hidden-import', 'pandas',
    '--hidden-import', 'openpyxl',
    '--hidden-import', 'datetime',
    '--collect-all', 'openpyxl',
    '--noconfirm',                  # Sobrescribir sin preguntar
]

# Agregar icono si existe
if os.path.exists(ICON):
    comando.extend(['--icon', ICON])

# Archivo principal
comando.append('menu_principal.py')

print("\nEjecutando PyInstaller...")
print(f"Comando: {' '.join(comando)}")
print()

resultado = subprocess.run(comando)

if resultado.returncode == 0:
    print("\n" + "="*80)
    print("✅ EJECUTABLE GENERADO EXITOSAMENTE")
    print("="*80)
    print(f"\nUbicación: dist/{APP_NAME}.exe")
    print(f"Tamaño: {os.path.getsize(f'dist/{APP_NAME}.exe') / (1024*1024):.1f} MB")
    print("\nPara distribuir:")
    print(f"  1. Copiar dist/{APP_NAME}.exe")
    print("  2. Copiar carpetas 'input/' y 'output/' junto al .exe")
    print("  3. Listo para usar en cualquier PC Windows")
else:
    print("\n❌ ERROR al generar ejecutable")
    print(f"Código de salida: {resultado.returncode}")
