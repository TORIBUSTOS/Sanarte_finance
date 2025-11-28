"""
Tests para el módulo Analyzer - TORO · Resumen de Cuentas

Verifica cálculos de análisis financiero:
- Ingresos totales
- Egresos totales
- Saldo/Balance
- Estadísticas por categoría
"""
import pytest
import pandas as pd
import sys
import os

# Agregar src/ al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from reports.analyzer import Analyzer


class TestAnalyzer:
    """Suite de tests para Analyzer"""

    def test_calcular_ingresos_totales(self):
        """Test: Suma correcta de ingresos"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01', '2025-12-02']),
            'Concepto': ['transferencia', 'transferencia'],
            'Detalle': ['pago 1', 'pago 2'],
            'Débito': [0.0, 0.0],
            'Crédito': [1000.0, 2500.0],
            'Saldo': [5000.0, 7500.0],
            'Banco': ['Supervielle', 'Supervielle'],
            'Tipo_Movimiento': ['Ingreso', 'Ingreso'],
            'Categoria_Principal': ['Ingresos - Transferencias', 'Ingresos - Transferencias'],
            'Categoria_Final': ['Ingresos - Transferencias', 'Ingresos - Transferencias']
        })
        analyzer = Analyzer(df)

        # Act
        metricas = analyzer.calcular_metricas()

        # Assert
        assert metricas['total_ingresos'] == 3500.0

    def test_calcular_egresos_totales(self):
        """Test: Suma correcta de egresos"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01', '2025-12-02']),
            'Concepto': ['comisión', 'impuesto'],
            'Detalle': ['comisión bancaria', 'afip'],
            'Débito': [250.0, 500.0],
            'Crédito': [0.0, 0.0],
            'Saldo': [4750.0, 4250.0],
            'Banco': ['Supervielle', 'Supervielle'],
            'Tipo_Movimiento': ['Egreso', 'Egreso'],
            'Categoria_Principal': ['Egresos - Comisiones', 'Egresos - Impuestos'],
            'Categoria_Final': ['Egresos - Comisiones', 'Egresos - Impuestos']
        })
        analyzer = Analyzer(df)

        # Act
        metricas = analyzer.calcular_metricas()

        # Assert
        assert metricas['total_egresos'] == 750.0

    def test_calcular_saldo_balance(self):
        """Test: Saldo = Ingresos - Egresos"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01', '2025-12-02', '2025-12-03']),
            'Concepto': ['transferencia', 'comisión', 'transferencia'],
            'Detalle': ['ingreso 1', 'comisión', 'ingreso 2'],
            'Débito': [0.0, 200.0, 0.0],
            'Crédito': [1000.0, 0.0, 1500.0],
            'Saldo': [5000.0, 4800.0, 6300.0],
            'Banco': ['Supervielle', 'Supervielle', 'Supervielle'],
            'Tipo_Movimiento': ['Ingreso', 'Egreso', 'Ingreso'],
            'Categoria_Principal': [
                'Ingresos - Transferencias',
                'Egresos - Comisiones',
                'Ingresos - Transferencias'
            ],
            'Categoria_Final': [
                'Ingresos - Transferencias',
                'Egresos - Comisiones',
                'Ingresos - Transferencias'
            ]
        })
        analyzer = Analyzer(df)

        # Act
        metricas = analyzer.calcular_metricas()

        # Assert
        assert metricas['total_ingresos'] == 2500.0
        assert metricas['total_egresos'] == 200.0
        assert metricas['variacion'] == 2300.0
        assert metricas['balance'] == 2300.0  # Compatibilidad

    def test_porcentaje_clasificados(self):
        """Test: Porcentaje de movimientos clasificados se calcula correctamente"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01', '2025-12-02', '2025-12-03', '2025-12-04']),
            'Concepto': ['transferencia', 'comisión', 'xxx', 'yyy'],
            'Detalle': ['pago', 'comisión', 'desconocido', 'otro'],
            'Débito': [0.0, 100.0, 50.0, 25.0],
            'Crédito': [1000.0, 0.0, 0.0, 0.0],
            'Saldo': [5000.0, 4900.0, 4850.0, 4825.0],
            'Banco': ['Supervielle'] * 4,
            'Tipo_Movimiento': ['Ingreso', 'Egreso', 'Egreso', 'Egreso'],
            'Categoria_Principal': [
                'Ingresos - Transferencias',
                'Egresos - Comisiones',
                'Sin Clasificar',
                'Sin Clasificar'
            ],
            'Categoria_Final': [
                'Ingresos - Transferencias',
                'Egresos - Comisiones',
                'Sin Clasificar',
                'Sin Clasificar'
            ]
        })
        analyzer = Analyzer(df)

        # Act
        metricas = analyzer.calcular_metricas()

        # Assert
        assert metricas['total_movimientos'] == 4
        assert metricas['movimientos_clasificados'] == 2
        assert metricas['movimientos_sin_clasificar'] == 2
        assert metricas['porcentaje_clasificado'] == 50.0

    def test_desglose_ingresos_por_subcategoria(self):
        """Test: Desglose de ingresos por subcategoría"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01', '2025-12-02', '2025-12-03']),
            'Concepto': ['transferencia', 'debin', 'cheque'],
            'Detalle': ['pago 1', 'debin afiliado', 'cheque recibido'],
            'Débito': [0.0, 0.0, 0.0],
            'Crédito': [1000.0, 500.0, 750.0],
            'Saldo': [5000.0, 5500.0, 6250.0],
            'Banco': ['Supervielle'] * 3,
            'Tipo_Movimiento': ['Ingreso'] * 3,
            'Categoria_Principal': [
                'Ingresos - Transferencias',
                'Ingresos - Afiliados DEBIN',
                'Ingresos - Cheques'
            ],
            'Categoria_Final': [
                'Ingresos - Transferencias',
                'Ingresos - Afiliados DEBIN',
                'Ingresos - Cheques'
            ]
        })
        analyzer = Analyzer(df)

        # Act
        metricas = analyzer.calcular_metricas()

        # Assert
        assert 'ingresos_por_subcategoria' in metricas
        ingresos_sub = metricas['ingresos_por_subcategoria']
        assert len(ingresos_sub) >= 2  # Al menos 2 subcategorías diferentes

    def test_desglose_egresos_por_subcategoria(self):
        """Test: Desglose de egresos por subcategoría"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01', '2025-12-02']),
            'Concepto': ['comisión', 'impuesto'],
            'Detalle': ['comisión bancaria', 'afip'],
            'Débito': [100.0, 500.0],
            'Crédito': [0.0, 0.0],
            'Saldo': [4900.0, 4400.0],
            'Banco': ['Supervielle'] * 2,
            'Tipo_Movimiento': ['Egreso'] * 2,
            'Categoria_Principal': [
                'Egresos - Comisiones',
                'Egresos - Impuestos'
            ],
            'Categoria_Final': [
                'Egresos - Comisiones',
                'Egresos - Impuestos'
            ]
        })
        analyzer = Analyzer(df)

        # Act
        metricas = analyzer.calcular_metricas()

        # Assert
        assert 'egresos_por_subcategoria' in metricas
        egresos_sub = metricas['egresos_por_subcategoria']
        assert len(egresos_sub) >= 2  # Al menos 2 subcategorías diferentes

    def test_movimientos_sin_clasificar_separados(self):
        """Test: Movimientos sin clasificar se contabilizan aparte"""
        # Arrange
        df = pd.DataFrame({
            'Fecha': pd.to_datetime(['2025-12-01', '2025-12-02']),
            'Concepto': ['transferencia', 'xxx'],
            'Detalle': ['pago conocido', 'concepto desconocido'],
            'Débito': [0.0, 100.0],
            'Crédito': [1000.0, 0.0],
            'Saldo': [5000.0, 4900.0],
            'Banco': ['Supervielle'] * 2,
            'Tipo_Movimiento': ['Ingreso', 'Egreso'],
            'Categoria_Principal': [
                'Ingresos - Transferencias',
                'Sin Clasificar'
            ],
            'Categoria_Final': [
                'Ingresos - Transferencias',
                'Sin Clasificar'
            ]
        })
        analyzer = Analyzer(df)

        # Act
        metricas = analyzer.calcular_metricas()

        # Assert
        assert metricas['ingresos_clasificados'] == 1000.0
        assert metricas['egresos_sin_clasificar'] == 100.0
        assert metricas['ingresos_sin_clasificar'] == 0.0

    def test_dataframe_vacio_no_rompe(self):
        """Test: DataFrame vacío no genera error"""
        # Arrange
        df = pd.DataFrame(columns=[
            'Fecha', 'Concepto', 'Detalle', 'Débito', 'Crédito',
            'Saldo', 'Banco', 'Tipo_Movimiento', 'Categoria_Principal', 'Categoria_Final'
        ])

        # Act & Assert - No debe lanzar excepción
        analyzer = Analyzer(df)
        metricas = analyzer.calcular_metricas()

        assert metricas['total_ingresos'] == 0.0
        assert metricas['total_egresos'] == 0.0
        assert metricas['total_movimientos'] == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
