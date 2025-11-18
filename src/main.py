"""
Sistema de Control Financiero SANARTE
Script principal - Bloques 1 y 2

Autor: Sistema SANARTE
Versión: 1.1 - Bloques 1 y 2
"""
import os
import sys
import argparse
from glob import glob
from datetime import datetime

# Importar módulos propios
from readers.supervielle_reader import SupervielleReader
from readers.galicia_reader import GaliciaReader
from processors.normalizer import Normalizer
from processors.consolidator import Consolidator
from processors.categorizer import Categorizer
from utils.cli_corrector import CLICorrector
from reports.analyzer import Analyzer
from reports.dashboard_generator import DashboardGenerator
from reports.excel_exporter import ExcelExporter


def detectar_banco(ruta_archivo: str):
    """
    Detecta automáticamente qué banco corresponde a un archivo Excel.

    Args:
        ruta_archivo: Ruta al archivo Excel

    Returns:
        Tupla (nombre_banco, reader_instance) o (None, None) si no se detecta
    """
    import pandas as pd

    try:
        df = pd.read_excel(ruta_archivo)

        # Probar Supervielle
        supervielle = SupervielleReader()
        if supervielle.detectar_formato(df):
            return "Supervielle", supervielle

        # Probar Galicia
        galicia = GaliciaReader()
        if galicia.detectar_formato(df):
            return "Galicia", galicia

        return None, None

    except Exception as e:
        print(f"Error al detectar formato de {ruta_archivo}: {e}")
        return None, None


def consolidar_bancos(ruta_input: str = "./input", ruta_output: str = "./output"):
    """
    Proceso completo de consolidación de extractos bancarios.

    Args:
        ruta_input: Carpeta donde están los archivos Excel
        ruta_output: Carpeta donde se guardarán los resultados
    """
    print("="*80)
    print("SANARTE - Sistema de Control Financiero")
    print("Bloque 1: Consolidador Multi-Banco")
    print("="*80)

    # Validar que exista carpeta input
    if not os.path.exists(ruta_input):
        print(f"\nError: No existe la carpeta '{ruta_input}'")
        print(f"Por favor, crea la carpeta y coloca allí los archivos Excel de los bancos.")
        return

    # Buscar archivos Excel en la carpeta input
    archivos_excel = glob(os.path.join(ruta_input, "*.xlsx"))

    if not archivos_excel:
        print(f"\nNo se encontraron archivos Excel (.xlsx) en '{ruta_input}'")
        print(f"Por favor, coloca los extractos bancarios en esa carpeta.")
        return

    print(f"\nEncontrados {len(archivos_excel)} archivo(s) Excel:")
    for archivo in archivos_excel:
        print(f"  - {os.path.basename(archivo)}")

    # Procesar cada archivo
    dataframes_normalizados = []

    print(f"\n{'='*80}")
    print("PROCESANDO ARCHIVOS")
    print(f"{'='*80}")

    for archivo in archivos_excel:
        print(f"\nArchivo: {os.path.basename(archivo)}")
        print("-" * 80)

        # Detectar banco automáticamente
        banco, reader = detectar_banco(archivo)

        if banco is None:
            print(f"  Advertencia: No se pudo detectar el formato del banco")
            print(f"  Omitiendo este archivo...")
            continue

        print(f"  Banco detectado: {banco}")

        try:
            # Leer archivo con el reader correspondiente
            df = reader.leer(archivo)

            # Normalizar
            normalizer = Normalizer()
            df_normalizado = normalizer.normalizar(df)

            dataframes_normalizados.append(df_normalizado)

        except Exception as e:
            print(f"  Error al procesar: {e}")
            continue

    # Consolidar todos los DataFrames
    if not dataframes_normalizados:
        print("\nNo se pudo procesar ningún archivo. Verifica los formatos.")
        return

    consolidator = Consolidator(ruta_output=ruta_output)
    df_consolidado = consolidator.consolidar(dataframes_normalizados)

    # Exportar
    archivo_salida = consolidator.exportar(df_consolidado)

    print(f"\n{'='*80}")
    print("PROCESO COMPLETADO")
    print(f"{'='*80}")
    print(f"\nArchivo generado: {archivo_salida}")
    print(f"\nPuedes abrir el archivo para verificar los {len(df_consolidado)} movimientos consolidados.")

    return df_consolidado, archivo_salida


def categorizar_movimientos(ruta_archivo_consolidado: str = None,
                            ruta_output: str = "./output",
                            revisar_manual: bool = True):
    """
    Categoriza movimientos consolidados.

    Args:
        ruta_archivo_consolidado: Ruta al archivo consolidado (si None, busca el más reciente)
        ruta_output: Carpeta de salida
        revisar_manual: Si True, abre CLI para corrección de movimientos sin clasificar
    """
    import pandas as pd

    print("="*80)
    print("SANARTE - Sistema de Control Financiero")
    print("Bloque 2: Categorizador Inteligente")
    print("="*80)

    # Si no se especifica archivo, buscar el más reciente
    if ruta_archivo_consolidado is None:
        archivos_consolidados = glob(os.path.join(ruta_output, "movimientos_consolidados_*.xlsx"))

        if not archivos_consolidados:
            print("\nError: No se encontraron archivos consolidados.")
            print("Por favor ejecuta primero: python main.py --consolidar")
            return

        # Tomar el más reciente
        ruta_archivo_consolidado = max(archivos_consolidados, key=os.path.getmtime)

    print(f"\nArchivo a categorizar: {os.path.basename(ruta_archivo_consolidado)}")

    # Leer archivo consolidado
    try:
        df = pd.read_excel(ruta_archivo_consolidado, sheet_name='Movimientos')
        print(f"OK Leidos {len(df)} movimientos")
    except Exception as e:
        print(f"Error al leer archivo: {e}")
        return

    # Crear categorizador
    categorizer = Categorizer()

    # Categorizar
    df_categorizado = categorizer.categorizar_dataframe(df)

    # Obtener movimientos sin clasificar
    df_sin_clasificar = categorizer.obtener_sin_clasificar(df_categorizado)

    # Revisión manual si hay movimientos sin clasificar y se solicita
    if len(df_sin_clasificar) > 0 and revisar_manual:
        print(f"\n{'='*80}")
        print(f"Hay {len(df_sin_clasificar)} movimientos sin clasificar.")
        print(f"{'='*80}")

        respuesta = input("\nDeseas revisar y corregir manualmente estos movimientos? (S/N): ").strip().upper()

        if respuesta in ['S', 'SI', 'Y', 'YES']:
            # Obtener categorías del clasificador
            categorias = categorizer.clasificador.obtener_categorias()

            # Crear CLI corrector
            cli = CLICorrector(categorias)

            # Procesar
            df_categorizado = cli.procesar_sin_clasificar(
                df_sin_clasificar=df_sin_clasificar,
                df_completo=df_categorizado,
                categorizer=categorizer
            )

    # Generar nombre de archivo de salida
    fecha_actual = datetime.now()
    nombre_salida = f"movimientos_categorizados_{fecha_actual.year}_{fecha_actual.month:02d}.xlsx"
    ruta_salida = os.path.join(ruta_output, nombre_salida)

    # Exportar
    categorizer.exportar_categorizados(df_categorizado, ruta_salida)

    print(f"\n{'='*80}")
    print("PROCESO COMPLETADO")
    print(f"{'='*80}")
    print(f"\nArchivo generado: {ruta_salida}")

    # Estadísticas finales
    total_clasificados = len(df_categorizado[df_categorizado['Categoria'] != 'Sin Clasificar'])
    porcentaje = (total_clasificados / len(df_categorizado)) * 100

    print(f"\nEstadisticas finales:")
    print(f"  Total movimientos: {len(df_categorizado)}")
    print(f"  Clasificados: {total_clasificados} ({porcentaje:.1f}%)")
    print(f"  Sin clasificar: {len(df_categorizado) - total_clasificados} ({100-porcentaje:.1f}%)")

    return df_categorizado, ruta_salida


def generar_reportes(ruta_archivo_categorizado: str = None,
                     ruta_output: str = "./output",
                     abrir_dashboard: bool = True):
    """
    Genera reportes y dashboard desde movimientos categorizados.

    Args:
        ruta_archivo_categorizado: Ruta al archivo categorizado (si None, busca el más reciente)
        ruta_output: Carpeta de salida
        abrir_dashboard: Si True, intenta abrir el dashboard en el navegador
    """
    import pandas as pd
    import webbrowser

    print("="*80)
    print("SANARTE - Sistema de Control Financiero")
    print("Bloque 3: Reportes y Dashboard")
    print("="*80)

    # Si no se especifica archivo, buscar el más reciente
    if ruta_archivo_categorizado is None:
        archivos_categorizados = glob(os.path.join(ruta_output, "movimientos_categorizados_*.xlsx"))

        if not archivos_categorizados:
            print("\nError: No se encontraron archivos categorizados.")
            print("Por favor ejecuta primero: python main.py --categorizar")
            return

        # Tomar el más reciente
        ruta_archivo_categorizado = max(archivos_categorizados, key=os.path.getmtime)

    print(f"\nArchivo a analizar: {os.path.basename(ruta_archivo_categorizado)}")

    # Leer archivo categorizado
    try:
        df = pd.read_excel(ruta_archivo_categorizado, sheet_name='Movimientos Categorizados')
        print(f"OK Leidos {len(df)} movimientos")
    except Exception as e:
        print(f"Error al leer archivo: {e}")
        return

    # Crear analizador
    analyzer = Analyzer(df)

    # Calcular métricas
    metricas = analyzer.calcular_metricas()

    # Obtener movimientos sin clasificar
    df_sin_clasificar = analyzer.obtener_sin_clasificar()

    # Generar dashboard HTML
    fecha_actual = datetime.now()
    nombre_dashboard = f"dashboard_{fecha_actual.year}_{fecha_actual.month:02d}.html"
    ruta_dashboard = os.path.join(ruta_output, nombre_dashboard)

    dashboard_gen = DashboardGenerator(metricas, df_sin_clasificar)
    dashboard_gen.generar_html(ruta_dashboard)

    # Generar reporte ejecutivo Excel
    nombre_reporte = f"reporte_ejecutivo_{fecha_actual.year}_{fecha_actual.month:02d}.xlsx"
    ruta_reporte = os.path.join(ruta_output, nombre_reporte)

    excel_exp = ExcelExporter(df, metricas)
    excel_exp.exportar(ruta_reporte)

    print(f"\n{'='*80}")
    print("PROCESO COMPLETADO")
    print(f"{'='*80}")
    print(f"\nArchivos generados:")
    print(f"  - Dashboard HTML: {ruta_dashboard}")
    print(f"  - Reporte Excel:  {ruta_reporte}")

    # Abrir dashboard en navegador si se solicita
    if abrir_dashboard:
        print(f"\nAbriendo dashboard en el navegador...")
        try:
            webbrowser.open('file://' + os.path.abspath(ruta_dashboard))
        except:
            print("No se pudo abrir el navegador automaticamente.")
            print(f"Abre manualmente: {ruta_dashboard}")

    return ruta_dashboard, ruta_reporte


def main():
    """
    Punto de entrada principal del sistema.
    """
    parser = argparse.ArgumentParser(
        description="Sistema SANARTE - Control Financiero",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  Consolidar extractos bancarios:
    python main.py --consolidar

  Especificar carpetas personalizadas:
    python main.py --consolidar --input ./mis_extractos --output ./resultados

Para más información, consulta el README.md
        """
    )

    parser.add_argument(
        '--consolidar',
        action='store_true',
        help='Consolidar extractos bancarios de la carpeta input/'
    )

    parser.add_argument(
        '--categorizar',
        action='store_true',
        help='Categorizar movimientos consolidados'
    )

    parser.add_argument(
        '--reportes',
        action='store_true',
        help='Generar reportes y dashboard desde movimientos categorizados'
    )

    parser.add_argument(
        '--archivo',
        type=str,
        default=None,
        help='Archivo a procesar (default: el más reciente)'
    )

    parser.add_argument(
        '--sin-revision',
        action='store_true',
        help='No abrir CLI de revisión manual (solo para --categorizar)'
    )

    parser.add_argument(
        '--sin-abrir',
        action='store_true',
        help='No abrir dashboard en navegador (solo para --reportes)'
    )

    parser.add_argument(
        '--input',
        type=str,
        default='./input',
        help='Carpeta con archivos Excel de entrada (default: ./input)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='./output',
        help='Carpeta para archivos de salida (default: ./output)'
    )

    args = parser.parse_args()

    # Si se invoca sin argumentos, mostrar ayuda
    if len(sys.argv) == 1:
        parser.print_help()
        return

    # Ejecutar consolidación
    if args.consolidar:
        consolidar_bancos(ruta_input=args.input, ruta_output=args.output)

    # Ejecutar categorización
    if args.categorizar:
        categorizar_movimientos(
            ruta_archivo_consolidado=args.archivo,
            ruta_output=args.output,
            revisar_manual=not args.sin_revision
        )

    # Generar reportes
    if args.reportes:
        generar_reportes(
            ruta_archivo_categorizado=args.archivo,
            ruta_output=args.output,
            abrir_dashboard=not args.sin_abrir
        )


if __name__ == "__main__":
    main()
