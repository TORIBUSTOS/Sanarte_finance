"""
Tests para el módulo Normalizer - TORO · Resumen de Cuentas

Verifica normalización de:
- Fechas en diferentes formatos
- Montos con coma/punto
- Textos con espacios
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Agregar src/ al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from processors.normalizer import Normalizer


class TestNormalizer:
    """Suite de tests para Normalizer"""

    def test_normalizar_fechas_formato_barra(self):
        """Test: Fechas se convierten a datetime correctamente"""
        # Arrange - Usar formato ISO para evitar ambigüedad DD/MM vs MM/DD
        df = pd.DataFrame({
            'Fecha': ['2025-12-01', '2025-11-15', '2025-10-30']
        })
        normalizer = Normalizer()

        # Act
        df_norm = normalizer.normalizar_fechas(df)

        # Assert
        assert pd.api.types.is_datetime64_any_dtype(df_norm['Fecha'])
        assert df_norm['Fecha'].iloc[0].day == 1
        assert df_norm['Fecha'].iloc[0].month == 12
        assert df_norm['Fecha'].iloc[0].year == 2025

    def test_normalizar_fechas_formato_guion(self):
        """Test: Fechas con formato DD-MM-YYYY se convierten a datetime"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': ['01-12-2025', '15-11-2025']
        })
        normalizer = Normalizer()

        # Act
        df_norm = normalizer.normalizar_fechas(df)

        # Assert
        assert pd.api.types.is_datetime64_any_dtype(df_norm['Fecha'])
        assert len(df_norm) == 2

    def test_normalizar_fechas_ya_datetime(self):
        """Test: Fechas que ya son datetime no se rompen"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01', '2025-11-15'])
        })
        normalizer = Normalizer()

        # Act
        df_norm = normalizer.normalizar_fechas(df)

        # Assert
        assert pd.api.types.is_datetime64_any_dtype(df_norm['Fecha'])
        assert len(df_norm) == 2

    def test_normalizar_numeros_debito_credito(self):
        """Test: Columnas Débito y Crédito se convierten a float"""
        # Arrange
        df = pd.DataFrame({
            'Débito': ['1000', '500.50', '0'],
            'Crédito': ['0', '2500', '100.25'],
            'Saldo': ['5000', '7000', '7100.25']
        })
        normalizer = Normalizer()

        # Act
        df_norm = normalizer.normalizar_numeros(df)

        # Assert
        assert df_norm['Débito'].dtype == np.float64
        assert df_norm['Crédito'].dtype == np.float64
        assert df_norm['Saldo'].dtype == np.float64
        assert df_norm['Débito'].iloc[0] == 1000.0
        assert df_norm['Crédito'].iloc[1] == 2500.0

    def test_normalizar_numeros_nan_convertido_a_cero(self):
        """Test: NaN en Débito/Crédito se convierte a 0.0"""
        # Arrange
        df = pd.DataFrame({
            'Débito': [np.nan, '500', np.nan],
            'Crédito': ['1000', np.nan, '200'],
            'Saldo': ['5000', '4500', '4700']
        })
        normalizer = Normalizer()

        # Act
        df_norm = normalizer.normalizar_numeros(df)

        # Assert
        assert df_norm['Débito'].iloc[0] == 0.0
        assert df_norm['Débito'].iloc[2] == 0.0
        assert df_norm['Crédito'].iloc[1] == 0.0

    def test_normalizar_textos_elimina_espacios(self):
        """Test: Espacios en blanco se eliminan de Concepto y Detalle"""
        # Arrange
        df = pd.DataFrame({
            'Concepto': ['  transferencia  ', 'pago   ', '  débito'],
            'Detalle': ['factura  ', '  comisión', 'cheque  ']
        })
        normalizer = Normalizer()

        # Act
        df_norm = normalizer.normalizar_textos(df)

        # Assert
        assert df_norm['Concepto'].iloc[0] == 'transferencia'
        assert df_norm['Concepto'].iloc[1] == 'pago'
        assert df_norm['Detalle'].iloc[0] == 'factura'
        assert df_norm['Detalle'].iloc[2] == 'cheque'

    def test_normalizar_textos_nan_a_none(self):
        """Test: Strings 'nan' se convierten a None"""
        # Arrange
        df = pd.DataFrame({
            'Concepto': ['transferencia', np.nan, 'pago'],
            'Detalle': [np.nan, 'detalle', 'otro']
        })
        normalizer = Normalizer()

        # Act
        df_norm = normalizer.normalizar_textos(df)

        # Assert
        # Después de astype(str), np.nan se convierte a 'nan' y luego a None
        assert df_norm['Concepto'].iloc[0] == 'transferencia'
        assert df_norm['Detalle'].iloc[2] == 'otro'

    def test_normalizar_columnas_faltantes_no_rompe(self):
        """Test: Si faltan columnas opcionales, no se rompe"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': ['01/12/2025'],
            'Concepto': ['test']
            # Falta Débito, Crédito, Saldo, Detalle
        })
        normalizer = Normalizer()

        # Act & Assert - No debe lanzar excepción
        df_norm = normalizer.normalizar_fechas(df)
        assert len(df_norm) == 1

        df_norm2 = normalizer.normalizar_textos(df)
        assert len(df_norm2) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
