"""
Normalizador de datos financieros
Autor: Sistema SANARTE
"""
import pandas as pd
from datetime import datetime

class Normalizer:
    """
    Normaliza DataFrames de diferentes bancos a un formato estándar unificado.
    - Formato de fechas: YYYY-MM-DD HH:MM:SS
    - Formato numérico: Decimal con coma (estándar argentino)
    """

    def __init__(self):
        pass

    def normalizar_fechas(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normaliza la columna Fecha al formato estándar.

        Args:
            df: DataFrame con columna 'Fecha'

        Returns:
            DataFrame con fechas normalizadas
        """
        df = df.copy()

        # Convertir a datetime si no lo es
        if not pd.api.types.is_datetime64_any_dtype(df['Fecha']):
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

        # Formato estándar: YYYY-MM-DD HH:MM:SS
        # Pandas ya maneja esto internamente como datetime64

        return df

    def normalizar_numeros(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normaliza columnas numéricas (Débito, Crédito, Saldo).

        Args:
            df: DataFrame con columnas numéricas

        Returns:
            DataFrame con números normalizados
        """
        df = df.copy()

        # Convertir a float64 si no lo son
        for col in ['Débito', 'Crédito', 'Saldo']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

                # Reemplazar NaN por 0 en Débito y Crédito
                if col in ['Débito', 'Crédito']:
                    df[col] = df[col].fillna(0.0)

        return df

    def normalizar_textos(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normaliza columnas de texto (Concepto, Detalle).

        Args:
            df: DataFrame con columnas de texto

        Returns:
            DataFrame con textos normalizados
        """
        df = df.copy()

        # Limpiar espacios en blanco
        for col in ['Concepto', 'Detalle']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                # Convertir 'nan' string a None
                df.loc[df[col] == 'nan', col] = None

        return df

    def normalizar(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica todas las normalizaciones al DataFrame.

        Args:
            df: DataFrame a normalizar

        Returns:
            DataFrame completamente normalizado
        """
        print(f"  Normalizando {len(df)} movimientos...")

        df = self.normalizar_fechas(df)
        df = self.normalizar_numeros(df)
        df = self.normalizar_textos(df)

        # Ordenar columnas en orden estándar
        columnas_ordenadas = ['Fecha', 'Concepto', 'Detalle', 'Débito', 'Crédito', 'Saldo', 'Banco']
        df = df[columnas_ordenadas]

        print(f"  OK Normalizacion completada")

        return df
