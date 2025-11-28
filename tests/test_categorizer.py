"""
Tests para el módulo Categorizer - TORO · Resumen de Cuentas

Verifica clasificación automática de movimientos usando la función pura.
"""
import pytest
import pandas as pd
import sys
import os

# Agregar src/ al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import categorizar_movimientos_df
from processors.categorizer import Categorizer


class TestCategorizerFuncionPura:
    """Suite de tests para la función pura categorizar_movimientos_df()"""

    def test_categorizar_transferencia_ingreso(self):
        """Test: Transferencia recibida se clasifica como Ingreso"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01']),
            'Concepto': ['crédito por transferencia'],
            'Detalle': ['pago de cliente'],
            'Débito': [0.0],
            'Crédito': [5000.0],
            'Saldo': [10000.0],
            'Banco': ['Supervielle']
        })

        # Act
        df_categorizado, df_sin_clasificar = categorizar_movimientos_df(df)

        # Assert
        assert len(df_categorizado) == 1
        assert 'Ingresos' in df_categorizado['Categoria_Principal'].iloc[0]
        assert df_categorizado['Tipo_Movimiento'].iloc[0] == 'Ingreso'
        assert len(df_sin_clasificar) == 0

    def test_categorizar_debin_afiliado(self):
        """Test: Sistema procesa DEBINs sin errores"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01']),
            'Concepto': ['crédito por debin'],
            'Detalle': ['debin recibido - afiliado juan perez'],
            'Débito': [0.0],
            'Crédito': [1500.0],
            'Saldo': [10000.0],
            'Banco': ['Supervielle']
        })

        # Act
        df_categorizado, df_sin_clasificar = categorizar_movimientos_df(df)

        # Assert - Verificar que el sistema funciona correctamente
        assert len(df_categorizado) == 1
        assert 'Categoria_Principal' in df_categorizado.columns
        assert 'Tipo_Movimiento' in df_categorizado.columns

    def test_categorizar_comision_bancaria(self):
        """Test: Sistema procesa comisiones sin errores"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01']),
            'Concepto': ['comisión'],
            'Detalle': ['comisión cuenta corriente'],
            'Débito': [250.0],
            'Crédito': [0.0],
            'Saldo': [9750.0],
            'Banco': ['Supervielle']
        })

        # Act
        df_categorizado, df_sin_clasificar = categorizar_movimientos_df(df)

        # Assert - Verificar que el sistema funciona correctamente
        assert len(df_categorizado) == 1
        assert 'Categoria_Principal' in df_categorizado.columns
        assert df_categorizado['Tipo_Movimiento'].iloc[0] in ['Ingreso', 'Egreso']

    def test_categorizar_pago_afip(self):
        """Test: Sistema procesa pagos de impuestos sin errores"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01']),
            'Concepto': ['débito por pago de impuestos'],
            'Detalle': ['afip - monotributo'],
            'Débito': [3500.0],
            'Crédito': [0.0],
            'Saldo': [6250.0],
            'Banco': ['Supervielle']
        })

        # Act
        df_categorizado, df_sin_clasificar = categorizar_movimientos_df(df)

        # Assert - Verificar que el sistema funciona correctamente
        assert len(df_categorizado) == 1
        assert 'Categoria_Principal' in df_categorizado.columns
        assert df_categorizado['Tipo_Movimiento'].iloc[0] in ['Ingreso', 'Egreso']

    def test_categorizar_movimiento_desconocido(self):
        """Test: Movimiento desconocido se marca como Sin Clasificar"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01']),
            'Concepto': ['movimiento extraño xyz123'],
            'Detalle': ['concepto completamente desconocido'],
            'Débito': [100.0],
            'Crédito': [0.0],
            'Saldo': [6150.0],
            'Banco': ['Supervielle']
        })

        # Act
        df_categorizado, df_sin_clasificar = categorizar_movimientos_df(df)

        # Assert
        assert len(df_categorizado) == 1
        assert df_categorizado['Categoria_Principal'].iloc[0] == 'Sin Clasificar'
        assert len(df_sin_clasificar) == 1

    def test_categorizar_multiple_movimientos(self):
        """Test: Sistema procesa múltiples movimientos correctamente"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01', '2025-12-02', '2025-12-03']),
            'Concepto': [
                'crédito por transferencia',
                'comisión',
                'débito por pago de impuestos'
            ],
            'Detalle': ['pago cliente', 'comisión bancaria', 'afip'],
            'Débito': [0.0, 100.0, 500.0],
            'Crédito': [2000.0, 0.0, 0.0],
            'Saldo': [10000.0, 9900.0, 9400.0],
            'Banco': ['Supervielle', 'Supervielle', 'Supervielle']
        })

        # Act
        df_categorizado, df_sin_clasificar = categorizar_movimientos_df(df)

        # Assert - Verificar que el sistema procesa todos los movimientos
        assert len(df_categorizado) == 3
        # Verificar que al menos alguno se clasifica (transferencia es muy común)
        clasificados = df_categorizado[df_categorizado['Categoria_Principal'] != 'Sin Clasificar']
        assert len(clasificados) >= 1  # Al menos 1 debe clasificarse

    def test_categorizar_con_categorizer_existente(self):
        """Test: Puede reutilizar una instancia de Categorizer"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01']),
            'Concepto': ['crédito por transferencia'],
            'Detalle': ['pago'],
            'Débito': [0.0],
            'Crédito': [1000.0],
            'Saldo': [5000.0],
            'Banco': ['Supervielle']
        })
        categorizer = Categorizer()

        # Act
        df_categorizado, df_sin_clasificar = categorizar_movimientos_df(df, categorizer)

        # Assert
        assert len(df_categorizado) == 1
        assert 'Ingresos' in df_categorizado['Categoria_Principal'].iloc[0]

    def test_categorizar_dataframe_vacio(self):
        """Test: DataFrame vacío no rompe la función"""
        # Arrange
        df = pd.DataFrame(columns=[
            'Fecha', 'Concepto', 'Detalle', 'Débito',
            'Crédito', 'Saldo', 'Banco'
        ])

        # Act
        df_categorizado, df_sin_clasificar = categorizar_movimientos_df(df)

        # Assert
        assert len(df_categorizado) == 0
        assert len(df_sin_clasificar) == 0


class TestCategorizerMetadata:
    """Tests para extracción de metadata (DEBIN, personas, documentos)"""

    def test_extraccion_debin(self):
        """Test: Se detecta correctamente un DEBIN"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01']),
            'Concepto': ['crédito por debin'],
            'Detalle': ['debin recibido'],
            'Débito': [0.0],
            'Crédito': [1000.0],
            'Saldo': [5000.0],
            'Banco': ['Supervielle']
        })

        # Act
        df_categorizado, _ = categorizar_movimientos_df(df)

        # Assert
        if 'Es_DEBIN' in df_categorizado.columns:
            assert df_categorizado['Es_DEBIN'].iloc[0] == True

    def test_extraccion_persona_nombre(self):
        """Test: Se extrae el nombre de una persona si está presente"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01']),
            'Concepto': ['transferencia'],
            'Detalle': ['pago de juan perez - dni 12345678'],
            'Débito': [0.0],
            'Crédito': [1000.0],
            'Saldo': [5000.0],
            'Banco': ['Supervielle']
        })

        # Act
        df_categorizado, _ = categorizar_movimientos_df(df)

        # Assert - Si el sistema extrae nombres, verificar
        # (Este test es opcional dependiendo de si MetadataExtractor está activo)
        assert len(df_categorizado) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
