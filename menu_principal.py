"""
SANARTE - Sistema de Control Financiero
Menú Principal CLI Interactivo - Bloque 4

Autor: Sistema SANARTE
Versión: 1.3 - Bloque 4: Orquestador Completo
"""
import os
import sys
from datetime import datetime

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Cambiar al directorio del script para rutas relativas
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from main import consolidar_bancos, categorizar_movimientos, generar_reportes
from glob import glob


def seleccionar_archivo_input():
    """
    Muestra archivos disponibles en input/ y permite al usuario seleccionar uno.

    Returns:
        str: Nombre del archivo seleccionado o None si no hay archivos o se cancela
    """
    archivos = glob(os.path.join('./input', '*.xlsx'))

    if not archivos:
        print("\n[ERROR] No hay archivos Excel (.xlsx) en la carpeta './input'")
        print("Por favor, coloca los extractos bancarios en esa carpeta.")
        return None

    print("\n" + "=" * 80)
    print("ARCHIVOS DISPONIBLES EN './input':")
    print("=" * 80 + "\n")

    for i, archivo in enumerate(archivos, 1):
        nombre = os.path.basename(archivo)
        tamaño = os.path.getsize(archivo) / 1024  # KB
        print(f"  {i}. {nombre} ({tamaño:.1f} KB)")

    print(f"\n  0. Cancelar")
    print()

    while True:
        try:
            opcion = input("Selecciona el número del archivo a procesar: ").strip()

            if opcion == '0':
                print("\nOperación cancelada.")
                return None

            idx = int(opcion) - 1
            if 0 <= idx < len(archivos):
                archivo_seleccionado = os.path.basename(archivos[idx])
                print(f"\n[OK] Archivo seleccionado: {archivo_seleccionado}")
                return archivo_seleccionado
            else:
                print(f"[ERROR] Opción inválida. Selecciona un número entre 1 y {len(archivos)}")

        except ValueError:
            print("[ERROR] Por favor ingresa un número válido.")
        except KeyboardInterrupt:
            print("\n\nOperación cancelada.")
            return None


def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_banner():
    """Muestra el banner principal del sistema."""
    print("\n" + "=" * 80)
    print("#" * 80)
    print("#" + " " * 78 + "#")
    print("#" + " " * 20 + "SANARTE - CONTROL FINANCIERO" + " " * 30 + "#")
    print("#" + " " * 25 + "Sistema Integrado v1.3" + " " * 32 + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80)
    print("=" * 80)
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"Fecha y hora: {fecha_hora}")
    print("=" * 80 + "\n")


def mostrar_menu_principal():
    """Muestra el menú principal."""
    print("\n+-------------------------------------------------------------+")
    print("|                     MENU PRINCIPAL                          |")
    print("+-------------------------------------------------------------+")
    print("|                                                             |")
    print("|  1. PROCESO COMPLETO (Consolidar -> Categorizar -> Reportes)|")
    print("|                                                             |")
    print("|  2. Solo CONSOLIDAR extractos bancarios                     |")
    print("|  3. Solo CATEGORIZAR movimientos                            |")
    print("|  4. Solo generar REPORTES y Dashboard                       |")
    print("|                                                             |")
    print("|  5. Configuracion de rutas                                  |")
    print("|  6. Informacion del sistema                                 |")
    print("|                                                             |")
    print("|  0. SALIR                                                   |")
    print("|                                                             |")
    print("+-------------------------------------------------------------+\n")


def proceso_completo():
    """Ejecuta el proceso completo: consolidar -> categorizar -> reportes."""
    print("\n" + "=" * 80)
    print(">> INICIANDO PROCESO COMPLETO")
    print("=" * 80)
    print("\nEste proceso ejecutará los 3 bloques en secuencia:")
    print("  1. Consolidar extractos bancarios")
    print("  2. Categorizar movimientos")
    print("  3. Generar reportes y dashboard")
    print()

    respuesta = input("¿Deseas continuar? (S/N): ").strip().upper()
    if respuesta not in ['S', 'SI', 'Y', 'YES']:
        print("\nProceso cancelado.")
        return

    # Seleccionar archivo de input
    archivo_input = seleccionar_archivo_input()
    if archivo_input is None:
        input("\nPresiona ENTER para continuar...")
        return

    # PASO 1: Consolidar
    print("\n" + "=" * 80)
    print("PASO 1/3: CONSOLIDANDO EXTRACTOS BANCARIOS")
    print("=" * 80 + "\n")

    resultado = consolidar_bancos(archivo_especifico=archivo_input)
    if resultado is None:
        print("\n[ERROR] Error en consolidacion. Proceso detenido.")
        input("\nPresiona ENTER para continuar...")
        return

    df_consolidado, archivo_consolidado = resultado

    input("\n[OK] Consolidación completada. Presiona ENTER para continuar...")

    # PASO 2: Categorizar
    print("\n" + "=" * 80)
    print("PASO 2/3: CATEGORIZANDO MOVIMIENTOS")
    print("=" * 80 + "\n")

    resultado = categorizar_movimientos(
        ruta_archivo_consolidado=archivo_consolidado,
        revisar_manual=True
    )

    if resultado is None:
        print("\n[ERROR] Error en categorización. Proceso detenido.")
        input("\nPresiona ENTER para continuar...")
        return

    df_categorizado, archivo_categorizado = resultado

    input("\n[OK] Categorización completada. Presiona ENTER para continuar...")

    # PASO 3: Reportes
    print("\n" + "=" * 80)
    print("PASO 3/3: GENERANDO REPORTES Y DASHBOARD")
    print("=" * 80 + "\n")

    resultado = generar_reportes(
        ruta_archivo_categorizado=archivo_categorizado,
        abrir_dashboard=True
    )

    if resultado is None:
        print("\n[ERROR] Error en generación de reportes.")
        input("\nPresiona ENTER para continuar...")
        return

    # Proceso completo exitoso
    print("\n" + "=" * 80)
    print("[OK] PROCESO COMPLETO FINALIZADO EXITOSAMENTE")
    print("=" * 80)
    print("\n>> Archivos generados en la carpeta 'output/':")
    print(f"  - {os.path.basename(archivo_consolidado)}")
    print(f"  - {os.path.basename(archivo_categorizado)}")
    print(f"  - reporte_ejecutivo_*.xlsx")
    print(f"  - dashboard_*.html")

    input("\nPresiona ENTER para volver al menú principal...")


def solo_consolidar():
    """Ejecuta solo el bloque 1: consolidar."""
    print("\n" + "=" * 80)
    print(">> BLOQUE 1: CONSOLIDAR EXTRACTOS BANCARIOS")
    print("=" * 80 + "\n")

    # Seleccionar archivo de input
    archivo_input = seleccionar_archivo_input()
    if archivo_input is None:
        input("\nPresiona ENTER para volver al menú principal...")
        return

    consolidar_bancos(archivo_especifico=archivo_input)

    input("\nPresiona ENTER para volver al menú principal...")


def solo_categorizar():
    """Ejecuta solo el bloque 2: categorizar."""
    print("\n" + "=" * 80)
    print(">>  BLOQUE 2: CATEGORIZAR MOVIMIENTOS")
    print("=" * 80 + "\n")

    categorizar_movimientos()

    input("\nPresiona ENTER para volver al menú principal...")


def solo_reportes():
    """Ejecuta solo el bloque 3: reportes."""
    print("\n" + "=" * 80)
    print(">> BLOQUE 3: GENERAR REPORTES Y DASHBOARD")
    print("=" * 80 + "\n")

    generar_reportes()

    input("\nPresiona ENTER para volver al menú principal...")


def configuracion():
    """Muestra y permite cambiar la configuración."""
    print("\n" + "=" * 80)
    print(">>  CONFIGURACIÓN DEL SISTEMA")
    print("=" * 80 + "\n")

    print("Configuración actual:")
    print(f"  - Carpeta de entrada:  ./input")
    print(f"  - Carpeta de salida:   ./output")
    print()
    print("Nota: El sistema ahora requiere seleccionar UN archivo específico para procesar.")
    print("Esto previene errores al mezclar archivos de diferentes períodos/cuentas.")
    print()
    print("Para cambiar las rutas, usa los parámetros --input y --output")
    print("al ejecutar directamente main.py con argumentos.")
    print()
    print("Ejemplo:")
    print("  python src/main.py --consolidar --archivo MI_ARCHIVO.xlsx --input ./mis_extractos")

    input("\nPresiona ENTER para volver al menú principal...")


def informacion_sistema():
    """Muestra información sobre el sistema."""
    print("\n" + "=" * 80)
    print(">>  INFORMACIÓN DEL SISTEMA")
    print("=" * 80 + "\n")

    print("SANARTE - Sistema de Control Financiero")
    print("Versión: 1.3")
    print("Autor: Sistema SANARTE")
    print("Fecha: Noviembre 2025")
    print()
    print("BLOQUES IMPLEMENTADOS:")
    print()
    print("  [OK] Bloque 1: Consolidador Multi-Banco")
    print("    - Detección automática de banco")
    print("    - Soporte Supervielle y Galicia")
    print("    - Normalización y exportación")
    print()
    print("  [OK] Bloque 2: Categorizador Inteligente")
    print("    - 24 reglas de clasificación")
    print("    - 80%+ categorización automática")
    print("    - Sistema de aprendizaje")
    print("    - Corrección manual interactiva")
    print()
    print("  [OK] Bloque 3: Reportes y Dashboard")
    print("    - Análisis financiero completo")
    print("    - Dashboard HTML interactivo")
    print("    - Reporte Excel ejecutivo")
    print("    - Top prestadores y métricas")
    print()
    print("  [OK] Bloque 4: Orquestador CLI (este menú)")
    print("    - Menú interactivo")
    print("    - Proceso completo automatizado")
    print("    - Ejecución individual de bloques")
    print()
    print("CATEGORÍAS SOPORTADAS:")
    print()
    print("  Ingresos:")
    print("    - Afiliados DEBIN")
    print("    - Pacientes Transferencia")
    print("    - Otros Ingresos")
    print()
    print("  Egresos:")
    print("    - Prestadores")
    print("    - Sueldos")
    print("    - Impuestos")
    print("    - Comisiones Bancarias")
    print("    - Servicios")
    print("    - Gastos Operativos")

    input("\nPresiona ENTER para volver al menú principal...")


def main():
    """Función principal del menú CLI."""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        mostrar_menu_principal()

        try:
            opcion = input("Selecciona una opción: ").strip()

            if opcion == '0':
                print("\n" + "=" * 80)
                print("¡Gracias por usar SANARTE Control Financiero!")
                print("=" * 80 + "\n")
                sys.exit(0)

            elif opcion == '1':
                proceso_completo()

            elif opcion == '2':
                solo_consolidar()

            elif opcion == '3':
                solo_categorizar()

            elif opcion == '4':
                solo_reportes()

            elif opcion == '5':
                configuracion()

            elif opcion == '6':
                informacion_sistema()

            else:
                print("\n[ERROR] Opción inválida. Por favor selecciona una opción del menú.")
                input("\nPresiona ENTER para continuar...")

        except KeyboardInterrupt:
            print("\n\n" + "=" * 80)
            print("¡Gracias por usar SANARTE Control Financiero!")
            print("=" * 80 + "\n")
            sys.exit(0)

        except Exception as e:
            print(f"\n[ERROR] Error inesperado: {e}")
            input("\nPresiona ENTER para continuar...")


if __name__ == "__main__":
    main()
