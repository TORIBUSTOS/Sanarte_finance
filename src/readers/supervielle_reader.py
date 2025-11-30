"""
Lector de archivos Excel del Banco Supervielle - TORO · Resumen de Cuentas
Autor: Sistema TORO
"""
import pandas as pd
from typing import Optional

class SupervielleReader:
    """
    Lector especializado para extractos del Banco Supervielle.
    El formato de Supervielle ya es ideal, solo requiere validación.
    """

    COLUMNAS_ESPERADAS = ['Fecha', 'Concepto', 'Detalle', 'Débito', 'Crédito', 'Saldo']

    def __init__(self):
        self.nombre_banco = "Supervielle"

    def detectar_formato(self, df: pd.DataFrame) -> bool:
        """
        Detecta si el DataFrame corresponde a un extracto de Supervielle.

        Args:
            df: DataFrame a analizar

        Returns:
            True si es formato Supervielle, False en caso contrario
        """
        columnas_df = df.columns.tolist()

        # Verifica que tenga exactamente 6 columnas
        if len(columnas_df) != 6:
            return False

        # Verifica que las columnas clave existan (con tolerancia a encoding)
        tiene_fecha = 'Fecha' in columnas_df
        tiene_concepto = 'Concepto' in columnas_df
        tiene_detalle = 'Detalle' in columnas_df

        # Busca columnas de montos con encoding posiblemente corrupto
        tiene_debito = any('bito' in col for col in columnas_df)
        tiene_credito = any('dito' in col for col in columnas_df)
        tiene_saldo = 'Saldo' in columnas_df

        return tiene_fecha and tiene_concepto and tiene_detalle and tiene_debito and tiene_credito and tiene_saldo

    def leer(self, ruta_archivo: str) -> pd.DataFrame:
        """
        Lee un archivo Excel de Supervielle y retorna un DataFrame normalizado.

        Args:
            ruta_archivo: Ruta al archivo Excel

        Returns:
            DataFrame con las columnas normalizadas

        Raises:
            ValueError: Si el archivo no tiene el formato esperado
        """
        try:
            # Leer Excel
            df = pd.read_excel(ruta_archivo)

            # Validar formato
            if not self.detectar_formato(df):
                raise ValueError(f"El archivo no tiene el formato de {self.nombre_banco}")

            # Normalizar nombres de columnas (por si hay problemas de encoding)
            columnas_normalizadas = []
            for col in df.columns:
                if 'Fecha' in col:
                    columnas_normalizadas.append('Fecha')
                elif 'Concepto' in col:
                    columnas_normalizadas.append('Concepto')
                elif 'Detalle' in col:
                    columnas_normalizadas.append('Detalle')
                elif 'bito' in col and 'Cr' not in col:
                    columnas_normalizadas.append('Débito')
                elif 'dito' in col and 'Cr' in col:
                    columnas_normalizadas.append('Crédito')
                elif 'Saldo' in col:
                    columnas_normalizadas.append('Saldo')
                else:
                    columnas_normalizadas.append(col)

            df.columns = columnas_normalizadas

            # Añadir columna de origen
            df['Banco'] = self.nombre_banco

            print(f"OK Leidos {len(df)} movimientos de {self.nombre_banco}")

            return df

        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")
        except Exception as e:
            raise Exception(f"Error al leer archivo de {self.nombre_banco}: {str(e)}")
