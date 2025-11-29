"""
Script para preparar paquete de distribución de TORO
Crea una carpeta lista para compartir con todo lo necesario
"""
import os
import shutil
import zipfile
from datetime import datetime

# Configuración
VERSION = "2.0.0"
NOMBRE_PAQUETE = f"TORO_v{VERSION}"
CARPETA_DIST = "paquete_distribucion"

print("="*80)
print(f"🐂 PREPARANDO PAQUETE DE DISTRIBUCIÓN - TORO v{VERSION}")
print("="*80)

# 1. Limpiar carpeta de distribución anterior
if os.path.exists(CARPETA_DIST):
    print(f"\n🗑️  Limpiando carpeta anterior: {CARPETA_DIST}/")
    shutil.rmtree(CARPETA_DIST)

# 2. Crear estructura de carpetas
print(f"\n📁 Creando estructura de carpetas...")
os.makedirs(CARPETA_DIST, exist_ok=True)
os.makedirs(os.path.join(CARPETA_DIST, NOMBRE_PAQUETE), exist_ok=True)
os.makedirs(os.path.join(CARPETA_DIST, NOMBRE_PAQUETE, 'input'), exist_ok=True)
os.makedirs(os.path.join(CARPETA_DIST, NOMBRE_PAQUETE, 'output'), exist_ok=True)
os.makedirs(os.path.join(CARPETA_DIST, NOMBRE_PAQUETE, 'manuales'), exist_ok=True)

# 3. Copiar ejecutable
print(f"\n📦 Copiando ejecutable...")

# Modo carpeta: dist/TORO/ (carpeta completa)
if os.path.exists('dist/TORO') and os.path.isdir('dist/TORO'):
    carpeta_destino = os.path.join(CARPETA_DIST, NOMBRE_PAQUETE, 'TORO')
    shutil.copytree('dist/TORO', carpeta_destino)
    print(f"   ✅ Copiada carpeta: dist/TORO/ → TORO/")
# Modo archivo único: dist/TORO.exe o dist/TORO
else:
    ejecutable_origen = 'dist/TORO'
    if os.name == 'nt':  # Windows
        ejecutable_origen = 'dist/TORO.exe'

    if os.path.exists(ejecutable_origen):
        ejecutable_destino = os.path.join(CARPETA_DIST, NOMBRE_PAQUETE, os.path.basename(ejecutable_origen))
        shutil.copy2(ejecutable_origen, ejecutable_destino)
        print(f"   ✅ Copiado: {ejecutable_origen}")
    else:
        print(f"   ⚠️  ADVERTENCIA: No se encontró {ejecutable_origen}")
        print("   Primero ejecuta: python build_exe_carpeta.py o python build_exe.py")

# 3b. Copiar launcher .bat (si existe)
if os.path.exists('INICIAR_TORO.bat'):
    shutil.copy2('INICIAR_TORO.bat', os.path.join(CARPETA_DIST, NOMBRE_PAQUETE, 'INICIAR_TORO.bat'))
    print(f"   ✅ Copiado: INICIAR_TORO.bat")

# 4. Copiar documentación a carpeta manuales/
print(f"\n📄 Copiando documentación a manuales/...")
archivos_doc = [
    ('LEEME_USUARIOS.txt', 'LEEME.txt'),
    ('MANUAL_SISTEMA_SANARTE.md', 'MANUAL.md'),
    ('README.md', 'README.md'),
]

for origen, destino in archivos_doc:
    if os.path.exists(origen):
        shutil.copy2(origen, os.path.join(CARPETA_DIST, NOMBRE_PAQUETE, 'manuales', destino))
        print(f"   ✅ Copiado: {origen} → manuales/{destino}")

# 5. Copiar archivos de ejemplo (si existen)
if os.path.exists('data'):
    print(f"\n📊 Copiando archivos de ejemplo...")
    carpeta_ejemplos = os.path.join(CARPETA_DIST, NOMBRE_PAQUETE, 'ejemplos')
    shutil.copytree('data', carpeta_ejemplos, ignore=shutil.ignore_patterns('*.pyc', '__pycache__'))
    print(f"   ✅ Copiada carpeta: data/ → ejemplos/")

# 6. Crear archivo de instrucciones rápidas
print(f"\n📝 Creando INICIO_RAPIDO.txt...")
inicio_rapido = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      TORO - Sistema de Control Financiero                     ║
║                              Versión {VERSION} - {datetime.now().year}                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

🚀 INICIO RÁPIDO (3 pasos):

1️⃣  Copiar tu extracto bancario Excel (.xlsx) a la carpeta "input/"

2️⃣  Doble clic en el ejecutable TORO{'  (o ./TORO en Linux)' if os.name != 'nt' else '.exe'}

3️⃣  Seguir las instrucciones del menú:
    → Opción 1: Procesar archivo
    → Los reportes aparecerán en la carpeta "output/"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📂 ESTRUCTURA DE CARPETAS:

    TORO_v{VERSION}/
    ├── INICIAR_TORO.bat      ← Ejecutar este archivo
    ├── TORO/                 ← Carpeta con ejecutable
    ├── input/                ← Poner aquí los archivos Excel
    ├── output/               ← Aquí aparecen los reportes
    ├── ejemplos/             ← Archivos de ejemplo (opcional)
    └── manuales/             ← Documentación
        ├── INICIO_RAPIDO.txt ← Este archivo
        ├── LEEME.txt         ← Instrucciones completas
        └── MANUAL.md         ← Manual técnico completo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ BANCOS SOPORTADOS:
   • Banco Galicia
   • Banco Supervielle
   • (Más bancos próximamente...)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ PROBLEMAS COMUNES:

{"Windows protegió tu PC (SmartScreen):" if os.name == 'nt' else ""}
{"   → Clic en 'Más información'" if os.name == 'nt' else ""}
{"   → Clic en 'Ejecutar de todas formas'" if os.name == 'nt' else ""}
{"" if os.name == 'nt' else "Permiso denegado en Linux:"}
{"" if os.name == 'nt' else "   → chmod +x TORO"}

No hay archivos en input/:
   → Verifica que el archivo sea .xlsx (no .xls)
   → Revisa que esté en la carpeta correcta

El programa no abre:
   → Verifica tener permisos de ejecución
   → Consulta manuales/LEEME.txt para más detalles

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📧 SOPORTE Y CONTACTO:

Para reportar problemas o sugerencias:
   GitHub: https://github.com/TORIBUSTOS/Sanarte_finance

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                              ¡Gracias por usar TORO! 🐂
"""

with open(os.path.join(CARPETA_DIST, NOMBRE_PAQUETE, 'manuales', 'INICIO_RAPIDO.txt'), 'w', encoding='utf-8') as f:
    f.write(inicio_rapido)
print("   ✅ Creado: manuales/INICIO_RAPIDO.txt")

# 7. Crear archivo ZIP
print(f"\n📦 Comprimiendo paquete...")
nombre_zip = f"{CARPETA_DIST}/{NOMBRE_PAQUETE}.zip"

with zipfile.ZipFile(nombre_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(os.path.join(CARPETA_DIST, NOMBRE_PAQUETE)):
        for file in files:
            ruta_completa = os.path.join(root, file)
            ruta_relativa = os.path.relpath(ruta_completa, CARPETA_DIST)
            zipf.write(ruta_completa, ruta_relativa)

tamanio_zip = os.path.getsize(nombre_zip) / (1024 * 1024)
print(f"   ✅ Creado: {nombre_zip} ({tamanio_zip:.1f} MB)")

# 8. Resumen final
print("\n" + "="*80)
print("✅ PAQUETE DE DISTRIBUCIÓN LISTO")
print("="*80)
print(f"\n📦 Paquete creado en: {CARPETA_DIST}/")
print(f"   • Carpeta: {NOMBRE_PAQUETE}/")
print(f"   • ZIP: {NOMBRE_PAQUETE}.zip ({tamanio_zip:.1f} MB)")

print(f"\n📤 PARA COMPARTIR:")
print(f"   1. Envía el archivo: {nombre_zip}")
print(f"   2. O comparte la carpeta: {CARPETA_DIST}/{NOMBRE_PAQUETE}/")
print(f"   3. Los usuarios solo necesitan extraer y ejecutar")

print(f"\n💡 NOTA:")
print(f"   • No requiere Python instalado")
print(f"   • Funciona en {'Windows 10/11' if os.name == 'nt' else 'Linux'} de 64 bits")
print(f"   • Todos los archivos necesarios están incluidos")

print("\n" + "="*80)
