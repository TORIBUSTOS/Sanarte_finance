"""
SANARTE - Sistema de Control Financiero
Menú Principal CLI Interactivo - Bloque 4

Autor: Sistema SANARTE
Versión: 1.3 - Bloque 4: Orquestador Completo
"""
import os
import sys
from glob import glob
from datetime import datetime

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Cambiar al directorio del script para rutas relativas
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from main import consolidar_bancos, categorizar_movimientos, generar_reportes

# Variable global para mantener el contexto de la sesión de trabajo
sesion_trabajo = {
    'archivo_consolidado': None,
    'archivo_categorizado': None,
    'archivos_input_usados': []
}


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
    print("=" * 80)

    # Mostrar estado de la sesión de trabajo
    if sesion_trabajo['archivo_consolidado'] or sesion_trabajo['archivo_categorizado']:
        print("\n[SESION ACTIVA]")
        if sesion_trabajo['archivos_input_usados']:
            print(f"  Archivos input: {', '.join(sesion_trabajo['archivos_input_usados'])}")
        if sesion_trabajo['archivo_consolidado']:
            print(f"  Consolidado: {os.path.basename(sesion_trabajo['archivo_consolidado'])}")
        if sesion_trabajo['archivo_categorizado']:
            print(f"  Categorizado: {os.path.basename(sesion_trabajo['archivo_categorizado'])}")
        print("=" * 80)
    print()


def mostrar_menu_principal():
    """Muestra el menú principal."""
    print("\n+-------------------------------------------------------------+")
    print("|                     MENU PRINCIPAL                          |")
    print("+-------------------------------------------------------------+")
    print("|                                                             |")
    print("|  1. PROCESO COMPLETO (Consolidar -> Categorizar -> Reportes)|")
    print("|                                                             |")
    print("|  2. CONSOLIDAR extractos bancarios (todos los archivos)     |")
    print("|  3. CONSOLIDAR con SELECCIÓN de archivos específicos        |")
    print("|  4. CATEGORIZAR movimientos                                 |")
    print("|  5. Generar REPORTES y Dashboard                            |")
    print("|                                                             |")
    print("|  6. Configuracion de rutas                                  |")
    print("|  7. Informacion del sistema                                 |")
    print("|  8. Limpiar SESION de trabajo                               |")
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

    # PASO 1: Consolidar
    print("\n" + "=" * 80)
    print("PASO 1/3: CONSOLIDANDO EXTRACTOS BANCARIOS")
    print("=" * 80 + "\n")

    resultado = consolidar_bancos()
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

    resultado = consolidar_bancos()

    if resultado is not None:
        df_consolidado, archivo_consolidado = resultado
        # Guardar en la sesión
        sesion_trabajo['archivo_consolidado'] = archivo_consolidado
        sesion_trabajo['archivo_categorizado'] = None  # Resetear categorizado
        sesion_trabajo['archivos_input_usados'] = ['Todos los archivos de ./input']

        print("\n" + "=" * 80)
        print("[SESION ACTUALIZADA]")
        print(f"Archivo listo para CATEGORIZAR (Opcion 4)")
        print("=" * 80)

    input("\nPresiona ENTER para volver al menú principal...")


def solo_categorizar():
    """Ejecuta solo el bloque 2: categorizar."""
    print("\n" + "=" * 80)
    print(">>  BLOQUE 2: CATEGORIZAR MOVIMIENTOS")
    print("=" * 80 + "\n")

    # Usar archivo de la sesión si existe
    archivo_a_usar = sesion_trabajo.get('archivo_consolidado')

    if archivo_a_usar:
        print(f"[SESION] Usando archivo consolidado: {os.path.basename(archivo_a_usar)}\n")

    resultado = categorizar_movimientos(ruta_archivo_consolidado=archivo_a_usar)

    if resultado is not None:
        df_categorizado, archivo_categorizado = resultado
        # Guardar en la sesión
        sesion_trabajo['archivo_categorizado'] = archivo_categorizado

        print("\n" + "=" * 80)
        print("[SESION ACTUALIZADA]")
        print(f"Archivo listo para generar REPORTES (Opcion 5)")
        print("=" * 80)

    input("\nPresiona ENTER para volver al menú principal...")


def solo_reportes():
    """Ejecuta solo el bloque 3: reportes."""
    print("\n" + "=" * 80)
    print(">> BLOQUE 3: GENERAR REPORTES Y DASHBOARD")
    print("=" * 80 + "\n")

    # Usar archivo de la sesión si existe
    archivo_a_usar = sesion_trabajo.get('archivo_categorizado')

    if archivo_a_usar:
        print(f"[SESION] Usando archivo categorizado: {os.path.basename(archivo_a_usar)}\n")

    generar_reportes(ruta_archivo_categorizado=archivo_a_usar)

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
    print("Nota: Para cambiar las rutas, usa los parámetros --input y --output")
    print("al ejecutar directamente main.py con argumentos.")
    print()
    print("Ejemplo:")
    print("  python src/main.py --consolidar --input ./mis_extractos --output ./resultados")

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


def seleccionar_archivos_excel():
    """
    Muestra los archivos Excel disponibles y permite seleccionar cuáles procesar.

    Returns:
        Lista de nombres de archivos seleccionados o None si se cancela
    """
    ruta_input = "./input"

    # Buscar archivos Excel
    archivos_completos = glob(os.path.join(ruta_input, "*.xlsx"))

    if not archivos_completos:
        print(f"\n[ERROR] No se encontraron archivos Excel (.xlsx) en '{ruta_input}'")
        print(f"Por favor, coloca los extractos bancarios en esa carpeta.")
        return None

    # Obtener solo los nombres de archivo (sin ruta)
    archivos = [os.path.basename(f) for f in archivos_completos]

    print("\n" + "=" * 80)
    print("ARCHIVOS EXCEL DISPONIBLES EN ./input/")
    print("=" * 80 + "\n")

    # Mostrar lista numerada
    for i, archivo in enumerate(archivos, 1):
        print(f"  {i}. {archivo}")

    print("\n" + "-" * 80)
    print("INSTRUCCIONES:")
    print("  - Para seleccionar archivos, ingresa los números separados por comas")
    print("  - Ejemplos: '1' para el primero, '1,3' para el 1 y 3, '1,2,3' para todos")
    print("  - Presiona ENTER sin ingresar nada para CANCELAR")
    print("-" * 80 + "\n")

    seleccion = input("Ingresa tu selección: ").strip()

    if not seleccion:
        print("\n[INFO] Selección cancelada.")
        return None

    try:
        # Parsear la selección
        indices = [int(x.strip()) for x in seleccion.split(',')]

        # Validar que los índices estén en rango
        archivos_seleccionados = []
        for idx in indices:
            if 1 <= idx <= len(archivos):
                archivos_seleccionados.append(archivos[idx - 1])
            else:
                print(f"\n[ADVERTENCIA] Número {idx} fuera de rango. Ignorando...")

        if not archivos_seleccionados:
            print("\n[ERROR] No se seleccionó ningún archivo válido.")
            return None

        # Mostrar confirmación
        print("\n" + "=" * 80)
        print("ARCHIVOS SELECCIONADOS:")
        print("=" * 80)
        for archivo in archivos_seleccionados:
            print(f"  - {archivo}")
        print()

        confirmacion = input("¿Confirmar selección? (S/N): ").strip().upper()
        if confirmacion not in ['S', 'SI', 'Y', 'YES']:
            print("\n[INFO] Selección cancelada.")
            return None

        return archivos_seleccionados

    except ValueError:
        print("\n[ERROR] Formato inválido. Debes ingresar números separados por comas.")
        return None


def limpiar_sesion():
    """Limpia la sesión de trabajo actual."""
    print("\n" + "=" * 80)
    print(">> LIMPIAR SESION DE TRABAJO")
    print("=" * 80 + "\n")

    if not sesion_trabajo['archivo_consolidado'] and not sesion_trabajo['archivo_categorizado']:
        print("[INFO] No hay sesión activa. Nada que limpiar.")
        input("\nPresiona ENTER para volver al menú principal...")
        return

    print("Sesión actual:")
    if sesion_trabajo['archivos_input_usados']:
        print(f"  Archivos input: {', '.join(sesion_trabajo['archivos_input_usados'])}")
    if sesion_trabajo['archivo_consolidado']:
        print(f"  Consolidado: {os.path.basename(sesion_trabajo['archivo_consolidado'])}")
    if sesion_trabajo['archivo_categorizado']:
        print(f"  Categorizado: {os.path.basename(sesion_trabajo['archivo_categorizado'])}")

    print("\nEsto permitirá iniciar un nuevo proceso desde cero.")
    confirmacion = input("\n¿Deseas limpiar la sesión? (S/N): ").strip().upper()

    if confirmacion in ['S', 'SI', 'Y', 'YES']:
        sesion_trabajo['archivo_consolidado'] = None
        sesion_trabajo['archivo_categorizado'] = None
        sesion_trabajo['archivos_input_usados'] = []

        print("\n[OK] Sesión limpiada. Puedes iniciar un nuevo proceso.")
    else:
        print("\n[INFO] Sesión no modificada.")

    input("\nPresiona ENTER para volver al menú principal...")


def consolidar_con_seleccion():
    """Ejecuta consolidación con selección manual de archivos."""
    print("\n" + "=" * 80)
    print(">> CONSOLIDAR CON SELECCIÓN DE ARCHIVOS")
    print("=" * 80)

    # Seleccionar archivos
    archivos_seleccionados = seleccionar_archivos_excel()

    if archivos_seleccionados is None:
        input("\nPresiona ENTER para volver al menú principal...")
        return

    # Ejecutar consolidación con archivos seleccionados
    print("\n" + "=" * 80)
    print("PROCESANDO ARCHIVOS SELECCIONADOS")
    print("=" * 80 + "\n")

    resultado = consolidar_bancos(archivos_seleccionados=archivos_seleccionados)

    if resultado is not None:
        df_consolidado, archivo_consolidado = resultado
        # Guardar en la sesión
        sesion_trabajo['archivo_consolidado'] = archivo_consolidado
        sesion_trabajo['archivo_categorizado'] = None  # Resetear categorizado
        sesion_trabajo['archivos_input_usados'] = archivos_seleccionados

        print("\n" + "=" * 80)
        print("[SESION ACTUALIZADA]")
        print(f"Archivo listo para CATEGORIZAR (Opcion 4)")
        print("=" * 80)

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
                consolidar_con_seleccion()

            elif opcion == '4':
                solo_categorizar()

            elif opcion == '5':
                solo_reportes()

            elif opcion == '6':
                configuracion()

            elif opcion == '7':
                informacion_sistema()

            elif opcion == '8':
                limpiar_sesion()

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
