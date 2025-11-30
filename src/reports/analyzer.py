"""
Analizador financiero de movimientos categorizados - TORO · Resumen de Cuentas
Autor: Sistema TORO
"""
from datetime import datetime
from typing import Dict, List, Tuple

import pandas as pd

class Analyzer:
    """
    Analiza movimientos categorizados y genera métricas financieras.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Args:
            df: DataFrame con movimientos categorizados
        """
        # Filtrar movimientos inválidos (sin fecha o con fecha NaT)
        df_limpio = df[df['Fecha'].notna()].copy()

        # Advertir si se filtraron movimientos
        if len(df_limpio) < len(df):
            filas_filtradas = len(df) - len(df_limpio)
            print(f"  Advertencia: Se filtraron {filas_filtradas} movimiento(s) sin fecha válida")

        self.df = df_limpio
        self.metricas = {}

    def calcular_metricas(self) -> Dict:
        """
        Calcula todas las métricas financieras.

        Returns:
            Diccionario con todas las métricas
        """
        print("\nCalculando métricas financieras...")

        # Filtrar movimientos clasificados vs sin clasificar
        df_clasificados = self.df[self.df['Categoria_Principal'] != 'Sin Clasificar']
        df_sin_clasificar = self.df[self.df['Categoria_Principal'] == 'Sin Clasificar']

        # Calcular saldos inicial y final
        saldo_inicial, saldo_final = self._calcular_saldos()

        # Calcular totales (TODOS los movimientos)
        total_ingresos = self._calcular_ingresos()
        total_egresos = self._calcular_egresos()
        variacion = total_ingresos - total_egresos
        balance = total_ingresos - total_egresos  # Mantener por compatibilidad

        # Calcular montos de movimientos sin clasificar
        ingresos_sin_clasificar = df_sin_clasificar['Crédito'].sum()
        egresos_sin_clasificar = df_sin_clasificar['Débito'].sum()

        # Calcular montos solo de clasificados
        ingresos_clasificados = df_clasificados[df_clasificados['Tipo_Movimiento'] == 'Ingreso']['Crédito'].sum()
        egresos_clasificados = df_clasificados[df_clasificados['Tipo_Movimiento'] == 'Egreso']['Débito'].sum()

        # Validación de coherencia
        validacion_ok, diferencia = self._validar_coherencia_saldos(
            saldo_inicial, saldo_final, total_ingresos, total_egresos
        )

        # Porcentaje clasificado
        total_movimientos = len(self.df)
        movimientos_clasificados = len(df_clasificados)
        porcentaje_clasificado = (movimientos_clasificados / total_movimientos * 100) if total_movimientos > 0 else 0

        # Desglose por subcategoría
        ingresos_por_sub = self._desglose_ingresos()
        egresos_por_sub = self._desglose_egresos()

        # Top prestadores
        top_prestadores = self._top_prestadores(10)

        # Flujo diario
        flujo_diario = self._flujo_diario()

        # Detectar alerta
        alerta = total_egresos > total_ingresos

        # Guardar métricas
        self.metricas = {
            'saldo_inicial': saldo_inicial,
            'saldo_final': saldo_final,
            'total_ingresos': total_ingresos,
            'total_egresos': total_egresos,
            'variacion': variacion,
            'balance': balance,  # Mantener por compatibilidad
            'ingresos_clasificados': ingresos_clasificados,
            'egresos_clasificados': egresos_clasificados,
            'ingresos_sin_clasificar': ingresos_sin_clasificar,
            'egresos_sin_clasificar': egresos_sin_clasificar,
            'total_movimientos': total_movimientos,
            'movimientos_clasificados': movimientos_clasificados,
            'movimientos_sin_clasificar': len(df_sin_clasificar),
            'porcentaje_clasificado': porcentaje_clasificado,
            'ingresos_por_subcategoria': ingresos_por_sub,
            'egresos_por_subcategoria': egresos_por_sub,
            'top_prestadores': top_prestadores,
            'flujo_diario': flujo_diario,
            'alerta_egresos_mayores': alerta,
            'validacion_saldos_ok': validacion_ok,
            'diferencia_validacion': diferencia
        }

        # Mostrar resumen
        self._mostrar_resumen()

        return self.metricas

    def _calcular_saldos(self) -> Tuple[float, float]:
        """
        Calcula el saldo inicial y final del período.

        Saldo Inicial = saldo ANTES del primer movimiento
        Saldo Final = saldo del movimiento más reciente (última fecha)

        Returns:
            Tupla (saldo_inicial, saldo_final)
        """
        if len(self.df) == 0:
            return 0.0, 0.0

        # Verificar si existe la columna Saldo y tiene valores
        if 'Saldo' not in self.df.columns:
            print("  ADVERTENCIA: El archivo no tiene columna 'Saldo'. No se puede calcular saldo inicial/final.")
            return float('nan'), float('nan')

        # Ordenar por fecha
        df_ordenado = self.df.sort_values('Fecha')

        # Saldo final: último movimiento (DESPUÉS del último movimiento)
        saldo_final = df_ordenado.iloc[-1]['Saldo']

        # Saldo inicial: ANTES del primer movimiento
        # El saldo que aparece en el Excel es DESPUÉS del movimiento
        # Entonces: Saldo_Antes = Saldo_Después - Crédito + Débito
        primer_movimiento = df_ordenado.iloc[0]
        saldo_despues_primer_mov = primer_movimiento['Saldo']
        credito_primer_mov = primer_movimiento['Crédito'] if pd.notna(primer_movimiento['Crédito']) else 0
        debito_primer_mov = primer_movimiento['Débito'] if pd.notna(primer_movimiento['Débito']) else 0

        saldo_inicial = saldo_despues_primer_mov - credito_primer_mov + debito_primer_mov

        # Verificar si son NaN
        if pd.isna(saldo_inicial) or pd.isna(saldo_final):
            print("  ADVERTENCIA: La columna 'Saldo' existe pero no tiene valores. No se puede calcular saldo inicial/final.")
            return float('nan'), float('nan')

        return saldo_inicial, saldo_final

    def _validar_coherencia_saldos(self, saldo_inicial: float, saldo_final: float,
                                   ingresos: float, egresos: float) -> Tuple[bool, float]:
        """
        Valida la coherencia entre saldos y movimientos.

        Fórmula esperada: Saldo Final = Saldo Inicial + Ingresos - Egresos

        Args:
            saldo_inicial: Saldo al inicio del período
            saldo_final: Saldo al final del período
            ingresos: Total de ingresos
            egresos: Total de egresos

        Returns:
            Tupla (validacion_ok, diferencia)
        """
        saldo_calculado = saldo_inicial + ingresos - egresos
        diferencia = abs(saldo_final - saldo_calculado)

        # Tolerancia de 1 peso por redondeos
        validacion_ok = diferencia < 1.0

        return validacion_ok, diferencia

    def _calcular_ingresos(self) -> float:
        """
        Calcula el total de ingresos (TODOS los créditos).

        Returns:
            Total de ingresos
        """
        # Sumar TODOS los créditos (clasificados y sin clasificar)
        return self.df['Crédito'].sum()

    def _calcular_egresos(self) -> float:
        """
        Calcula el total de egresos (TODOS los débitos).

        Returns:
            Total de egresos
        """
        # Sumar TODOS los débitos (clasificados y sin clasificar)
        return self.df['Débito'].sum()

    def _desglose_ingresos(self) -> Dict[str, float]:
        """
        Desglose de ingresos por categoría final.

        Returns:
            Diccionario {categoria_final: monto}
        """
        df_ingresos = self.df[self.df['Tipo_Movimiento'] == 'Ingreso']
        desglose = df_ingresos.groupby('Categoria_Final')['Crédito'].sum().to_dict()
        return desglose

    def _desglose_egresos(self) -> Dict[str, float]:
        """
        Desglose de egresos por categoría final.

        Returns:
            Diccionario {categoria_final: monto}
        """
        df_egresos = self.df[self.df['Tipo_Movimiento'] == 'Egreso']
        desglose = df_egresos.groupby('Categoria_Final')['Débito'].sum().to_dict()
        return desglose

    def _top_prestadores(self, n: int = 10) -> List[Dict]:
        """
        Top N prestadores por monto.

        Args:
            n: Número de prestadores a retornar

        Returns:
            Lista de diccionarios con nombre y monto
        """
        df_prestadores = self.df[self.df['Categoria_Principal'] == 'Prestadores']

        if len(df_prestadores) == 0:
            return []

        # Agrupar por nombre de persona
        top = df_prestadores.groupby('Persona_Nombre')['Débito'].sum().sort_values(ascending=False).head(n)

        resultado = []
        for nombre, monto in top.items():
            if pd.notna(nombre) and nombre != 'None':
                resultado.append({
                    'nombre': nombre,
                    'monto': monto
                })

        return resultado

    def _flujo_diario(self) -> pd.DataFrame:
        """
        Calcula el flujo de caja diario.

        Returns:
            DataFrame con columnas: fecha, ingresos, egresos
        """
        # Extraer solo la fecha (sin hora)
        self.df['Fecha_Solo'] = pd.to_datetime(self.df['Fecha']).dt.date

        # Filtrar solo clasificados
        df_clasificados = self.df[self.df['Categoria_Principal'] != 'Sin Clasificar'].copy()

        # Calcular ingresos por fecha
        ingresos_diarios = df_clasificados[df_clasificados['Tipo_Movimiento'] == 'Ingreso'].groupby('Fecha_Solo')['Crédito'].sum()

        # Calcular egresos por fecha
        egresos_diarios = df_clasificados[df_clasificados['Tipo_Movimiento'] == 'Egreso'].groupby('Fecha_Solo')['Débito'].sum()

        # Obtener todas las fechas únicas
        todas_fechas = sorted(df_clasificados['Fecha_Solo'].unique())

        # Crear DataFrame con todas las fechas
        flujo = pd.DataFrame({'fecha': todas_fechas})

        # Mapear ingresos y egresos
        flujo['ingresos'] = flujo['fecha'].map(ingresos_diarios).fillna(0)
        flujo['egresos'] = flujo['fecha'].map(egresos_diarios).fillna(0)

        # Ordenar por fecha
        flujo = flujo.sort_values('fecha')

        return flujo

    def _mostrar_resumen(self):
        """
        Muestra un resumen de las métricas calculadas.
        """
        print("\nRESUMEN FINANCIERO:")
        print("="*80)

        # Mostrar saldo inicial (puede ser NaN)
        if pd.isna(self.metricas['saldo_inicial']):
            print(f"Saldo Inicial:   No disponible (archivo sin columna Saldo)")
        else:
            print(f"Saldo Inicial:   ${self.metricas['saldo_inicial']:,.2f}")

        print(f"Total Ingresos:  ${self.metricas['total_ingresos']:,.2f}")
        if self.metricas['ingresos_sin_clasificar'] > 0:
            print(f"  - Clasificados:    ${self.metricas['ingresos_clasificados']:,.2f}")
            print(f"  - Sin clasificar:  ${self.metricas['ingresos_sin_clasificar']:,.2f}")

        print(f"Total Egresos:   ${self.metricas['total_egresos']:,.2f}")
        if self.metricas['egresos_sin_clasificar'] > 0:
            print(f"  - Clasificados:    ${self.metricas['egresos_clasificados']:,.2f}")
            print(f"  - Sin clasificar:  ${self.metricas['egresos_sin_clasificar']:,.2f}")

        # Mostrar saldo final (puede ser NaN)
        if pd.isna(self.metricas['saldo_final']):
            print(f"Saldo Final:     No disponible (archivo sin columna Saldo)")
        else:
            print(f"Saldo Final:     ${self.metricas['saldo_final']:,.2f}")

        print(f"Variación:       ${self.metricas['variacion']:,.2f}")

        # Validación de coherencia
        if not self.metricas['validacion_saldos_ok']:
            print(f"\nADVERTENCIA: Diferencia en validación de saldos: ${self.metricas['diferencia_validacion']:,.2f}")
            print("El saldo final no coincide con: Saldo Inicial + Ingresos - Egresos")

        if self.metricas['alerta_egresos_mayores']:
            print("\nALERTA: Los egresos superan a los ingresos!")

        print(f"\nMovimientos clasificados: {self.metricas['movimientos_clasificados']}/{self.metricas['total_movimientos']} ({self.metricas['porcentaje_clasificado']:.1f}%)")

        print(f"\nDesglose Ingresos:")
        for sub, monto in self.metricas['ingresos_por_subcategoria'].items():
            porcentaje = (monto / self.metricas['total_ingresos'] * 100) if self.metricas['total_ingresos'] > 0 else 0
            print(f"  - {sub}: ${monto:,.2f} ({porcentaje:.1f}%)")

        print(f"\nDesglose Egresos:")
        for sub, monto in self.metricas['egresos_por_subcategoria'].items():
            porcentaje = (monto / self.metricas['total_egresos'] * 100) if self.metricas['total_egresos'] > 0 else 0
            print(f"  - {sub}: ${monto:,.2f} ({porcentaje:.1f}%)")

        if len(self.metricas['top_prestadores']) > 0:
            print(f"\nTop {len(self.metricas['top_prestadores'])} Prestadores:")
            for i, prestador in enumerate(self.metricas['top_prestadores'], 1):
                print(f"  {i}. {prestador['nombre']}: ${prestador['monto']:,.2f}")

    def obtener_metricas(self) -> Dict:
        """
        Retorna las métricas calculadas.

        Returns:
            Diccionario con métricas
        """
        if not self.metricas:
            self.calcular_metricas()

        return self.metricas

    def obtener_sin_clasificar(self) -> pd.DataFrame:
        """
        Retorna los movimientos sin clasificar.

        Returns:
            DataFrame con movimientos sin clasificar
        """
        return self.df[self.df['Categoria_Principal'] == 'Sin Clasificar'].copy()
