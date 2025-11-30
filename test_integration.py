"""
Test de Integración End-to-End - TORO
Verifica el flujo completo: Importar → Categorizar → Analizar → Dashboard
"""
import sys
import os
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_flujo_completo():
    """Ejecuta flujo completo con archivo de ejemplo."""
    print("=" * 60)
    print("TEST DE INTEGRACIÓN END-TO-END - TORO")
    print("=" * 60)

    # 1. Importar configuración
    print("\n[1/5] Inicializando configuración...")
    from config import get_config
    cfg = get_config()
    cfg.paths.crear_directorios()
    print("✓ Configuración inicializada")

    # 2. Leer archivo de ejemplo
    print("\n[2/5] Leyendo archivo de ejemplo Galicia...")
    from readers.galicia_reader import GaliciaReader
    reader = GaliciaReader()
    archivo_ejemplo = Path("input/Ejemplo_Galicia_2025_10.xlsx")

    if not archivo_ejemplo.exists():
        print(f"✗ ERROR: No se encontró {archivo_ejemplo}")
        return False

    df = reader.leer(str(archivo_ejemplo))
    print(f"✓ Archivo leído: {len(df)} movimientos")

    # 3. Categorizar con ClasificadorCascada v2.0
    print("\n[3/5] Categorizando con motor ClasificadorCascada v2.0...")
    from processors.categorizer import Categorizer
    categorizer = Categorizer()
    df_categorizado = categorizer.categorizar_dataframe(df)
    clasificados = len(df_categorizado[df_categorizado['Categoria_Principal'] != 'Sin Clasificar'])
    print(f"✓ Categorización completada: {clasificados}/{len(df)} clasificados")

    # 4. Analizar métricas
    print("\n[4/5] Analizando métricas financieras...")
    from reports.analyzer import Analyzer
    analyzer = Analyzer(df_categorizado)
    metricas = analyzer.calcular_metricas()
    print(f"✓ Métricas calculadas:")
    print(f"  - Total Ingresos: ${metricas['total_ingresos']:,.2f}")
    print(f"  - Total Egresos: ${metricas['total_egresos']:,.2f}")
    print(f"  - Variación: ${metricas['variacion']:,.2f}")
    print(f"  - % Clasificado: {metricas['porcentaje_clasificado']:.1f}%")

    # 5. Generar dashboard HTML
    print("\n[5/5] Generando dashboard HTML con diseño TORO...")
    from reports.dashboard_generator import DashboardGenerator
    dashboard = DashboardGenerator(df_categorizado, metricas)
    ruta_dashboard = "output/dashboard_test_integration.html"
    dashboard.generar_html(ruta_dashboard)

    # Verificar que el archivo se generó
    if Path(ruta_dashboard).exists():
        size_kb = Path(ruta_dashboard).stat().st_size / 1024
        print(f"✓ Dashboard generado: {ruta_dashboard} ({size_kb:.1f} KB)")

        # Verificar que contiene branding TORO
        with open(ruta_dashboard, 'r', encoding='utf-8') as f:
            contenido = f.read()
            if "TORO · Resumen de Cuentas" in contenido:
                print("✓ Branding TORO verificado en dashboard")
            if "#059669" in contenido:
                print("✓ Paleta de colores TORO verificada")
    else:
        print(f"✗ ERROR: Dashboard no generado en {ruta_dashboard}")
        return False

    print("\n" + "=" * 60)
    print("✓ TEST DE INTEGRACIÓN EXITOSO")
    print("=" * 60)
    return True

if __name__ == "__main__":
    try:
        exito = test_flujo_completo()
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"\n✗ ERROR EN TEST DE INTEGRACIÓN: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
