"""
Consolidador de movimientos multi-banco - TORO · Resumen de Cuentas
Autor: Sistema TORO
"""
import pandas as pd
from datetime import datetime
import os
from typing import List

class Consolidator:
    """
    Consolida DataFrames de múltiples bancos en un único archivo unificado.
    - Une movimientos de todos los bancos
    - Ordena cronológicamente
    - Exporta a Excel
    """

    def __init__(self, ruta_output: str = None):
        # Usar configuración centralizada si no se especifica ruta
        if ruta_output is None:
            from config import get_config
            config = get_config()
            ruta_output = config.paths.output_dir

        self.ruta_output = ruta_output

        # Crear carpeta output si no existe
        if not os.path.exists(self.ruta_output):
            os.makedirs(self.ruta_output)

    def consolidar(self, dataframes: List[pd.DataFrame]) -> pd.DataFrame:
        """
        Consolida múltiples DataFrames en uno solo.

        Args:
            dataframes: Lista de DataFrames normalizados

        Returns:
            DataFrame consolidado y ordenado cronológicamente
        """
        if not dataframes:
            raise ValueError("No hay DataFrames para consolidar")

        print(f"\nConsolidando movimientos de {len(dataframes)} banco(s)...")

        # Unir todos los DataFrames
        df_consolidado = pd.concat(dataframes, ignore_index=True)

        # Ordenar cronológicamente (más reciente primero)
        df_consolidado = df_consolidado.sort_values('Fecha', ascending=False)

        # Resetear índice
        df_consolidado = df_consolidado.reset_index(drop=True)

        # Estadísticas por banco
        print(f"\nEstadísticas:")
        print(f"  Total movimientos consolidados: {len(df_consolidado)}")
        print(f"\n  Desglose por banco:")
        for banco, count in df_consolidado['Banco'].value_counts().items():
            porcentaje = (count / len(df_consolidado)) * 100
            print(f"    - {banco}: {count} movimientos ({porcentaje:.1f}%)")

        return df_consolidado

    def exportar(self, df: pd.DataFrame, nombre_archivo: str = None) -> str:
        """
        Exporta el DataFrame consolidado a Excel.

        Args:
            df: DataFrame consolidado
            nombre_archivo: Nombre del archivo (opcional, por defecto usa fecha actual)

        Returns:
            Ruta del archivo generado
        """
        if nombre_archivo is None:
            # Generar nombre con fecha actual: movimientos_consolidados_YYYY_MM.xlsx
            fecha_actual = datetime.now()
            nombre_archivo = f"movimientos_consolidados_{fecha_actual.year}_{fecha_actual.month:02d}.xlsx"

        ruta_completa = os.path.join(self.ruta_output, nombre_archivo)

        print(f"\nExportando a: {ruta_completa}")

        # Crear una copia para exportar con formato argentino de números
        df_export = df.copy()

        # Exportar a Excel
        with pd.ExcelWriter(ruta_completa, engine='openpyxl') as writer:
            df_export.to_excel(writer, sheet_name='Movimientos', index=False)

            # Obtener la hoja para aplicar formato
            worksheet = writer.sheets['Movimientos']

            # Ajustar anchos de columna
            anchos = {
                'A': 20,  # Fecha
                'B': 35,  # Concepto
                'C': 50,  # Detalle
                'D': 15,  # Débito
                'E': 15,  # Crédito
                'F': 15,  # Saldo
                'G': 12,  # Banco
            }

            for col, ancho in anchos.items():
                worksheet.column_dimensions[col].width = ancho

            # Formato de números con coma decimal (estilo argentino)
            from openpyxl.styles import numbers

            # Aplicar formato numérico a columnas de montos (D, E, F)
            for row in range(2, len(df_export) + 2):  # Empezar desde fila 2 (después del header)
                for col in ['D', 'E', 'F']:
                    cell = worksheet[f'{col}{row}']
                    # Formato: #,##0.00 (separador de miles y 2 decimales)
                    cell.number_format = '#,##0.00'

        print(f"OK Archivo exportado exitosamente ({len(df)} movimientos)")

        return ruta_completa
