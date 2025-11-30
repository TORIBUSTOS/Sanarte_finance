"""
Lector de archivos Excel del Banco Galicia - TORO · Resumen de Cuentas
Autor: Sistema TORO
"""
import pandas as pd
from typing import Optional

class GaliciaReader:
    """
    Lector especializado para extractos del Banco Galicia.
    Limpia las 10 columnas basura y normaliza al formato estándar.
    """

    # Columnas útiles del extracto de Galicia
    COLUMNAS_UTILES = ['Fecha', 'Descripción', 'Débitos', 'Créditos',
                       'Grupo de Conceptos', 'Concepto', 'Saldo']

    # Columnas basura que se eliminarán
    COLUMNAS_BASURA = ['Origen', 'Número de Terminal', 'Observaciones Cliente',
                       'Número de Comprobante', 'Leyendas Adicionales 1',
                       'Leyendas Adicionales 2', 'Leyendas Adicionales 3',
                       'Leyendas Adicionales 4', 'Tipo de Movimiento']

    def __init__(self):
        self.nombre_banco = "Galicia"

    def detectar_formato(self, df: pd.DataFrame) -> bool:
        """
        Detecta si el DataFrame corresponde a un extracto de Galicia.

        Args:
            df: DataFrame a analizar

        Returns:
            True si es formato Galicia, False en caso contrario
        """
        columnas_df = df.columns.tolist()

        # Galicia tiene 16 columnas
        if len(columnas_df) < 10:
            return False

        # Verifica columnas características de Galicia
        tiene_descripcion = any('Descripci' in col for col in columnas_df)
        tiene_grupo_conceptos = any('Grupo de Conceptos' in col for col in columnas_df)
        tiene_debitos = any('bitos' in col and 'Cr' not in col for col in columnas_df)

        return tiene_descripcion and tiene_grupo_conceptos and tiene_debitos

    def leer(self, ruta_archivo: str) -> pd.DataFrame:
        """
        Lee un archivo Excel de Galicia y lo transforma al formato estándar.

        Transformaciones:
        - Descripción -> Concepto
        - Grupo de Conceptos + Concepto -> Detalle
        - Débitos -> Débito
        - Créditos -> Crédito
        - Elimina 10 columnas basura

        Args:
            ruta_archivo: Ruta al archivo Excel

        Returns:
            DataFrame con formato normalizado (igual a Supervielle)

        Raises:
            ValueError: Si el archivo no tiene el formato esperado
        """
        try:
            # Leer Excel
            df = pd.read_excel(ruta_archivo)

            # Validar formato
            if not self.detectar_formato(df):
                raise ValueError(f"El archivo no tiene el formato de {self.nombre_banco}")

            # Crear DataFrame normalizado
            df_normalizado = pd.DataFrame()

            # Mapear columnas
            df_normalizado['Fecha'] = df['Fecha']

            # Descripción -> Concepto
            col_descripcion = [col for col in df.columns if 'Descripci' in col][0]
            df_normalizado['Concepto'] = df[col_descripcion]

            # Combinar Grupo de Conceptos + Concepto -> Detalle
            grupo = df['Grupo de Conceptos'].fillna('')
            concepto = df['Concepto'].fillna('')
            df_normalizado['Detalle'] = (grupo + ' | ' + concepto).str.strip(' | ')
            # Si queda vacío, usar NaN
            df_normalizado.loc[df_normalizado['Detalle'] == '', 'Detalle'] = None

            # Débitos -> Débito (convertir 0 a NaN para consistencia)
            col_debitos = [col for col in df.columns if 'bitos' in col and 'Cr' not in col][0]
            df_normalizado['Débito'] = df[col_debitos]
            df_normalizado.loc[df_normalizado['Débito'] == 0, 'Débito'] = 0.0

            # Créditos -> Crédito
            col_creditos = [col for col in df.columns if 'ditos' in col and 'Cr' in col][0]
            df_normalizado['Crédito'] = df[col_creditos]
            df_normalizado.loc[df_normalizado['Crédito'] == 0, 'Crédito'] = 0.0

            # Saldo
            df_normalizado['Saldo'] = df['Saldo']

            # Añadir columna de origen
            df_normalizado['Banco'] = self.nombre_banco

            print(f"OK Leidos {len(df_normalizado)} movimientos de {self.nombre_banco}")
            print(f"  (eliminadas {len(df.columns) - len(self.COLUMNAS_UTILES)} columnas basura)")

            return df_normalizado

        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")
        except Exception as e:
            raise Exception(f"Error al leer archivo de {self.nombre_banco}: {str(e)}")
