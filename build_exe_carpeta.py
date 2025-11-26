"""
Script de build alternativo para SANARTE - Modo carpeta (más estable)
Genera una carpeta con el ejecutable y dependencias (sin problemas de stdin)
Ejecutar: python build_exe_carpeta.py
"""
import os
import subprocess
import shutil

# Configuración
APP_NAME = "SANARTE"
VERSION = "1.3"
ICON = "sanarte_icon.ico"

# Limpiar builds anteriores
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

print("="*80)
print(f"GENERANDO EJECUTABLE {APP_NAME} v{VERSION} (MODO CARPETA)")
print("="*80)
print("\nEste método genera una carpeta con el .exe y sus dependencias.")
print("Es más estable y evita problemas con entrada de teclado.\n")

# Comando PyInstaller - MODO CARPETA (--onedir)
separador = ':' if os.name != 'nt' else ';'

comando = [
    'pyinstaller',
    '--name', APP_NAME,
    '--onedir',                     # ⭐ CARPETA (en lugar de archivo único)
    '--console',                    # Con consola
    '--add-data', f'src{separador}src',
    '--hidden-import', 'pandas',
    '--hidden-import', 'openpyxl',
    '--hidden-import', 'datetime',
    '--hidden-import', 'rich',
    '--hidden-import', 'rich.console',
    '--hidden-import', 'rich.prompt',
    '--hidden-import', 'rich.table',
    '--hidden-import', 'rich.panel',
    '--collect-all', 'openpyxl',
    '--collect-all', 'rich',
    '--noconfirm',
    'menu_principal.py'
]

# Agregar icono si existe
if os.path.exists(ICON):
    comando.extend(['--icon', ICON])

print("Ejecutando PyInstaller...")
print(f"Comando: {' '.join(comando)}")
print()

resultado = subprocess.run(comando)

if resultado.returncode == 0:
    print("\n" + "="*80)
    print("✅ EJECUTABLE GENERADO EXITOSAMENTE (MODO CARPETA)")
    print("="*80)

    # Calcular tamaño de la carpeta
    carpeta_dist = f'dist/{APP_NAME}'
    tamanio_total = 0
    if os.path.exists(carpeta_dist):
        for root, dirs, files in os.walk(carpeta_dist):
            for file in files:
                tamanio_total += os.path.getsize(os.path.join(root, file))

        print(f"\nUbicación: {carpeta_dist}/")
        print(f"Tamaño total: {tamanio_total / (1024*1024):.1f} MB")
        print(f"Ejecutable principal: {carpeta_dist}/{APP_NAME}{'.exe' if os.name == 'nt' else ''}")

        print("\n📦 PARA DISTRIBUIR:")
        print(f"  1. Comprimir toda la carpeta: {carpeta_dist}/")
        print(f"  2. El usuario debe extraer y ejecutar {APP_NAME}.exe")
        print(f"  3. ⚠️ IMPORTANTE: Distribuir TODA LA CARPETA, no solo el .exe")

        print("\n💡 VENTAJAS de este método:")
        print("  ✅ Más estable (no hay problemas con stdin)")
        print("  ✅ Inicia más rápido")
        print("  ✅ Más fácil de depurar")

        print("\n⚠️  DESVENTAJA:")
        print("  • Hay que compartir toda la carpeta (no un solo archivo)")

else:
    print("\n❌ ERROR al generar ejecutable")
    print(f"Código de salida: {resultado.returncode}")
