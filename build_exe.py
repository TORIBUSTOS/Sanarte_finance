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
# Determinar separador según OS (: en Linux/Mac, ; en Windows)
separador = ':' if os.name != 'nt' else ';'

comando = [
    'pyinstaller',
    '--name', APP_NAME,
    '--onefile',                    # Un solo .exe
    '--console',                    # Con consola (cambiado de --windowed)
    '--add-data', f'src{separador}src',  # Incluir carpeta src
    '--hidden-import', 'pandas',
    '--hidden-import', 'openpyxl',
    '--hidden-import', 'datetime',
    '--hidden-import', 'rich',
    '--collect-all', 'openpyxl',
    '--collect-all', 'rich',
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

    # Nombre del ejecutable depende del SO
    exe_ext = '.exe' if os.name == 'nt' else ''
    exe_path = f'dist/{APP_NAME}{exe_ext}'

    if os.path.exists(exe_path):
        print(f"\nUbicación: {exe_path}")
        print(f"Tamaño: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
    else:
        print(f"\nUbicación: dist/{APP_NAME}")
        print(f"Tamaño: {os.path.getsize(f'dist/{APP_NAME}') / (1024*1024):.1f} MB")

    print("\nPara distribuir:")
    print(f"  1. Copiar el ejecutable desde dist/")
    print("  2. Copiar carpetas 'input/' y 'output/' junto al ejecutable")
    print("  3. Listo para usar en cualquier PC")
else:
    print("\n❌ ERROR al generar ejecutable")
    print(f"Código de salida: {resultado.returncode}")
