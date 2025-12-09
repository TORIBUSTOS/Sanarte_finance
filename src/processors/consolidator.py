"""
Consolidador de movimientos multi-banco - TORO · Resumen de Cuentas
Autor: Sistema TORO
"""
import os
import shutil
from datetime import datetime
from typing import List, Tuple

import pandas as pd

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

    def exportar(self, df: pd.DataFrame, nombre_archivo: str = None, archivo_original: str = None) -> Tuple[str, str]:
        """
        Exporta el DataFrame consolidado a Excel en una carpeta organizada por mes/año.

        Args:
            df: DataFrame consolidado
            nombre_archivo: Nombre del archivo (opcional, por defecto usa fecha del período de datos)
            archivo_original: Ruta del archivo original a copiar/mover (opcional)

        Returns:
            Tupla (ruta_archivo_generado, ruta_carpeta_mes)
        """
        # Extraer año y mes de la fecha más reciente en los datos
        if len(df) > 0 and 'Fecha' in df.columns:
            # Obtener la fecha más reciente (primera fila ya que está ordenada desc)
            fecha_datos = pd.to_datetime(df['Fecha'].iloc[0])
            anio = fecha_datos.year
            mes = fecha_datos.month
        else:
            # Fallback: usar fecha actual
            fecha_actual = datetime.now()
            anio = fecha_actual.year
            mes = fecha_actual.month

        # Crear nombre de carpeta: octubre_25, noviembre_25, etc.
        meses = {
            1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
            5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
            9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
        }
        nombre_mes = meses[mes]
        nombre_carpeta = f"{nombre_mes}_{str(anio)[-2:]}"

        # Crear la carpeta si no existe
        carpeta_mes = os.path.join(self.ruta_output, nombre_carpeta)
        if not os.path.exists(carpeta_mes):
            os.makedirs(carpeta_mes)
            print(f"\nCarpeta creada: {carpeta_mes}")

        # Copiar archivo original a la carpeta si se proporciona
        if archivo_original and os.path.exists(archivo_original):
            nombre_original = os.path.basename(archivo_original)
            destino_original = os.path.join(carpeta_mes, nombre_original)
            if not os.path.exists(destino_original):
                shutil.copy2(archivo_original, destino_original)
                print(f"OK Archivo original copiado a: {destino_original}")
            else:
                print(f"OK Archivo original ya existe en: {destino_original}")
        else:
            if archivo_original:
                print(f"ADVERTENCIA: No se encontro el archivo original: {archivo_original}")
            else:
                print(f"ADVERTENCIA: No se proporciono archivo original para copiar")

        # Generar nombre de archivo si no se especifica
        if nombre_archivo is None:
            nombre_archivo = f"movimientos_consolidados_{anio}_{mes:02d}.xlsx"

        ruta_completa = os.path.join(carpeta_mes, nombre_archivo)

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
        print(f"Carpeta del período: {carpeta_mes}")

        return ruta_completa, carpeta_mes
