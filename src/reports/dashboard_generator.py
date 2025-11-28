"""
Generador de dashboard HTML interactivo - TORO · Resumen de Cuentas
Autor: Sistema TORO
"""
import pandas as pd
import json
from datetime import datetime
from typing import Dict

class DashboardGenerator:
    """
    Genera dashboard HTML interactivo con Chart.js.
    """

    def __init__(self, df: pd.DataFrame, metricas: Dict):
        """
        Args:
            df: DataFrame con movimientos categorizados (con columnas Tipo_Movimiento, Categoria_Final)
            metricas: Diccionario con métricas calculadas
        """
        self.df = df
        self.metricas = metricas

        # Filtrar sin clasificar
        self.df_sin_clasificar = df[df['Categoria_Principal'] == 'Sin Clasificar'].copy()

    def generar_html(self, ruta_salida: str):
        """
        Genera el archivo HTML del dashboard.

        Args:
            ruta_salida: Ruta donde guardar el HTML
        """
        print(f"\nGenerando dashboard HTML...")

        html = self._crear_html()

        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"OK Dashboard generado: {ruta_salida}")

    def _crear_html(self) -> str:
        """
        Crea el HTML completo del dashboard.

        Returns:
            String con el HTML
        """
        # Calcular datos REALES desde el DataFrame categorizado
        ingresos_por_categoria = self._calcular_ingresos_por_categoria()
        egresos_por_categoria = self._calcular_egresos_por_categoria()
        kpis = self._calcular_kpis_adicionales()
        resumen_categorias = self._calcular_resumen_categorias()
        alertas = self._generar_alertas()

        # Preparar datos para gráficos
        datos_ingresos = self._preparar_datos_torta(ingresos_por_categoria)
        datos_egresos = self._preparar_datos_torta(egresos_por_categoria)
        datos_flujo = self._preparar_datos_flujo(self.metricas['flujo_diario'])

        # Color del balance
        balance_color = '#28a745' if self.metricas['balance'] >= 0 else '#dc3545'

        # Fecha de generación
        fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M")

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SANARTE - Dashboard Financiero</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .content {{
            padding: 30px;
        }}

        .cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 4px solid;
        }}

        .card.ingresos {{
            border-color: #28a745;
        }}

        .card.egresos {{
            border-color: #dc3545;
        }}

        .card.variacion {{
            border-color: {balance_color};
        }}

        .card.clasificados {{
            border-color: #007bff;
        }}

        .card.saldo-inicial {{
            border-color: #6f42c1;
        }}

        .card.saldo-final {{
            border-color: #17a2b8;
        }}

        .card.debin {{
            border-color: #28a745;
        }}

        .card.prestadores {{
            border-color: #e83e8c;
        }}

        .card.mayor-egreso {{
            border-color: #dc3545;
        }}

        .card.mayor-ingreso {{
            border-color: #20c997;
        }}

        .card-title {{
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 10px;
            font-weight: 600;
        }}

        .card-value {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .card.ingresos .card-value {{
            color: #28a745;
        }}

        .card.egresos .card-value {{
            color: #dc3545;
        }}

        .card.variacion .card-value {{
            color: {balance_color};
        }}

        .card.clasificados .card-value {{
            color: #007bff;
        }}

        .card.saldo-inicial .card-value {{
            color: #6f42c1;
        }}

        .card.saldo-final .card-value {{
            color: #17a2b8;
        }}

        .card.debin .card-value {{
            color: #28a745;
        }}

        .card.prestadores .card-value {{
            color: #e83e8c;
        }}

        .card.mayor-egreso .card-value {{
            color: #dc3545;
        }}

        .card.mayor-ingreso .card-value {{
            color: #20c997;
        }}

        .card-subtitle {{
            font-size: 0.85em;
            color: #999;
        }}

        .charts {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}

        .chart-container {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .chart-title {{
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 20px;
            color: #333;
        }}

        .chart-full {{
            grid-column: 1 / -1;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}

        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}

        th {{
            background-color: #f8f9fa;
            font-weight: 600;
            color: #333;
        }}

        tr:hover {{
            background-color: #f8f9fa;
        }}

        .alert {{
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
            color: #856404;
        }}

        .alert-danger {{
            background-color: #f8d7da;
            border-color: #dc3545;
            color: #721c24;
        }}

        .alert-info {{
            background-color: #d1ecf1;
            border-color: #17a2b8;
            color: #0c5460;
        }}

        .alert-success {{
            background-color: #d4edda;
            border-color: #28a745;
            color: #155724;
        }}

        .summary-table {{
            width: 100%;
            margin-top: 15px;
        }}

        .summary-table th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: right;
        }}

        .summary-table th:first-child {{
            text-align: left;
        }}

        .summary-table td {{
            padding: 10px;
            text-align: right;
            border-bottom: 1px solid #e0e0e0;
        }}

        .summary-table td:first-child {{
            text-align: left;
            font-weight: 600;
        }}

        .summary-table .neto-positivo {{
            color: #28a745;
            font-weight: 600;
        }}

        .summary-table .neto-negativo {{
            color: #dc3545;
            font-weight: 600;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            .charts {{
                grid-template-columns: 1fr;
            }}

            .cards {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>SANARTE - Dashboard Financiero</h1>
            <p>Generado el {fecha_generacion}</p>
        </div>

        <div class="content">
            <!-- Alertas Inteligentes -->
            {alertas}

            <!-- Cards de métricas principales -->
            <div class="cards">
                <div class="card saldo-inicial">
                    <div class="card-title">Saldo Inicial</div>
                    <div class="card-value">{'No disponible' if pd.isna(self.metricas['saldo_inicial']) else f"${self.metricas['saldo_inicial']:,.2f}"}</div>
                </div>

                <div class="card ingresos">
                    <div class="card-title">Total Ingresos</div>
                    <div class="card-value">${self.metricas['total_ingresos']:,.2f}</div>
                </div>

                <div class="card egresos">
                    <div class="card-title">Total Egresos</div>
                    <div class="card-value">${self.metricas['total_egresos']:,.2f}</div>
                </div>

                <div class="card saldo-final">
                    <div class="card-title">Saldo Final</div>
                    <div class="card-value">{'No disponible' if pd.isna(self.metricas['saldo_final']) else f"${self.metricas['saldo_final']:,.2f}"}</div>
                </div>

                <div class="card variacion">
                    <div class="card-title">Variación del Mes</div>
                    <div class="card-value">${self.metricas['variacion']:,.2f}</div>
                </div>

                <div class="card clasificados">
                    <div class="card-title">Movimientos Clasificados</div>
                    <div class="card-value">{self.metricas['porcentaje_clasificado']:.1f}%</div>
                    <div class="card-subtitle">{self.metricas['movimientos_clasificados']} de {self.metricas['total_movimientos']}</div>
                </div>

                <div class="card debin">
                    <div class="card-title">💳 Ingresos DEBIN</div>
                    <div class="card-value">${kpis['ingresos_debin_monto']:,.2f}</div>
                    <div class="card-subtitle">{kpis['ingresos_debin_cant']} transacciones</div>
                </div>

                <div class="card prestadores">
                    <div class="card-title">👥 Prestadores Activos</div>
                    <div class="card-value">{kpis['prestadores_activos']}</div>
                    <div class="card-subtitle">Total pagado: ${kpis['prestadores_total']:,.0f}</div>
                </div>

                <div class="card mayor-egreso">
                    <div class="card-title">💰 Mayor Categoría Egreso</div>
                    <div class="card-value">${kpis['mayor_cat_egreso_monto']:,.0f}</div>
                    <div class="card-subtitle">{kpis['mayor_cat_egreso_nombre'][:30]} ({kpis['mayor_cat_egreso_pct']:.1f}%)</div>
                </div>

                <div class="card mayor-ingreso">
                    <div class="card-title">📊 Mayor Categoría Ingreso</div>
                    <div class="card-value">${kpis['mayor_cat_ingreso_monto']:,.0f}</div>
                    <div class="card-subtitle">{kpis['mayor_cat_ingreso_nombre'][:30]} ({kpis['mayor_cat_ingreso_pct']:.1f}%)</div>
                </div>
            </div>

            <!-- Gráficos -->
            <div class="charts">
                <!-- Gráfico de Ingresos -->
                <div class="chart-container">
                    <div class="chart-title">Ingresos por Categoría</div>
                    <canvas id="chartIngresos"></canvas>
                </div>

                <!-- Gráfico de Egresos -->
                <div class="chart-container">
                    <div class="chart-title">Top 10 Egresos por Categoría</div>
                    <canvas id="chartEgresos"></canvas>
                </div>

                <!-- Gráfico de Flujo de Caja -->
                <div class="chart-container chart-full">
                    <div class="chart-title">Flujo de Caja Diario</div>
                    <canvas id="chartFlujo"></canvas>
                </div>
            </div>

            <!-- Tabla Resumen por Categoría Principal -->
            <div class="chart-container chart-full">
                <div class="chart-title">📊 Resumen por Categoría Principal</div>
                <table class="summary-table">
                    <thead>
                        <tr>
                            <th>Categoría</th>
                            <th>Transacciones</th>
                            <th>Ingresos</th>
                            <th>Egresos</th>
                            <th>Neto</th>
                        </tr>
                    </thead>
                    <tbody id="summaryTableBody">
                        <!-- Generado dinámicamente por JavaScript -->
                    </tbody>
                </table>
            </div>

            <!-- Tabla de Top Prestadores -->
            {self._generar_tabla_prestadores()}

            <!-- Tabla de Movimientos Sin Clasificar -->
            {self._generar_tabla_sin_clasificar()}
        </div>

        <div class="footer">
            &copy; 2025 SANARTE - Sistema de Control Financiero | Generado automáticamente
        </div>
    </div>

    <script>
        // Datos para gráficos
        const datosIngresos = {datos_ingresos};
        const datosEgresos = {datos_egresos};
        const datosFlujo = {datos_flujo};
        const resumenCategorias = {resumen_categorias};

        // Llenar tabla de resumen por categoría principal
        const summaryTableBody = document.getElementById('summaryTableBody');
        resumenCategorias.forEach(cat => {{
            const row = document.createElement('tr');
            const netoClass = cat.neto >= 0 ? 'neto-positivo' : 'neto-negativo';
            row.innerHTML = `
                <td>${{cat.categoria}}</td>
                <td>${{cat.transacciones.toLocaleString('es-AR')}}</td>
                <td>$${{cat.ingresos.toLocaleString('es-AR', {{minimumFractionDigits: 0, maximumFractionDigits: 0}})}}</td>
                <td>$${{cat.egresos.toLocaleString('es-AR', {{minimumFractionDigits: 0, maximumFractionDigits: 0}})}}</td>
                <td class="${{netoClass}}">$${{cat.neto.toLocaleString('es-AR', {{minimumFractionDigits: 0, maximumFractionDigits: 0}})}}</td>
            `;
            summaryTableBody.appendChild(row);
        }});

        // Gráfico de Ingresos (Torta)
        new Chart(document.getElementById('chartIngresos'), {{
            type: 'pie',
            data: {{
                labels: datosIngresos.labels,
                datasets: [{{
                    data: datosIngresos.values,
                    backgroundColor: [
                        '#28a745',
                        '#20c997',
                        '#17a2b8',
                        '#6610f2',
                        '#e83e8c'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                let label = context.label || '';
                                if (label) {{
                                    label += ': ';
                                }}
                                label += '$' + context.parsed.toLocaleString('es-AR', {{minimumFractionDigits: 2}});
                                return label;
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Gráfico de Egresos (Torta - Top 10)
        new Chart(document.getElementById('chartEgresos'), {{
            type: 'pie',
            data: {{
                labels: datosEgresos.labels,
                datasets: [{{
                    data: datosEgresos.values,
                    backgroundColor: [
                        '#dc3545', // Rojo
                        '#fd7e14', // Naranja
                        '#ff6b6b', // Rojo claro
                        '#e83e8c', // Rosa
                        '#9b59b6', // Púrpura
                        '#ffc107', // Amarillo
                        '#f39c12', // Naranja oscuro
                        '#17a2b8', // Azul
                        '#3498db', // Azul claro
                        '#6c757d'  // Gris
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                let label = context.label || '';
                                if (label) {{
                                    label += ': ';
                                }}
                                label += '$' + context.parsed.toLocaleString('es-AR', {{minimumFractionDigits: 2}});
                                return label;
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Gráfico de Flujo de Caja (Líneas)
        new Chart(document.getElementById('chartFlujo'), {{
            type: 'line',
            data: {{
                labels: datosFlujo.labels,
                datasets: [
                    {{
                        label: 'Ingresos',
                        data: datosFlujo.ingresos,
                        borderColor: '#28a745',
                        backgroundColor: 'rgba(40, 167, 69, 0.1)',
                        tension: 0.4,
                        fill: true
                    }},
                    {{
                        label: 'Egresos',
                        data: datosFlujo.egresos,
                        borderColor: '#dc3545',
                        backgroundColor: 'rgba(220, 53, 69, 0.1)',
                        tension: 0.4,
                        fill: true
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'top'
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                let label = context.dataset.label || '';
                                if (label) {{
                                    label += ': ';
                                }}
                                label += '$' + context.parsed.y.toLocaleString('es-AR', {{minimumFractionDigits: 2}});
                                return label;
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value.toLocaleString('es-AR');
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

        return html

    def _calcular_ingresos_por_categoria(self) -> Dict[str, float]:
        """
        Calcula ingresos REALES por Categoria_Final desde el DataFrame.

        Returns:
            Diccionario {categoria_final: monto}
        """
        df_ingresos = self.df[self.df['Tipo_Movimiento'] == 'Ingreso'].copy()

        if len(df_ingresos) == 0:
            return {}

        # Agrupar por Categoria_Final y sumar Crédito
        ingresos_por_cat = df_ingresos.groupby('Categoria_Final')['Crédito'].sum()

        # Ordenar de mayor a menor
        ingresos_por_cat = ingresos_por_cat.sort_values(ascending=False)

        return ingresos_por_cat.to_dict()

    def _calcular_egresos_por_categoria(self) -> Dict[str, float]:
        """
        Calcula Top 10 egresos por Categoria_Final desde el DataFrame.

        Returns:
            Diccionario {categoria_final: monto} - Solo Top 10
        """
        df_egresos = self.df[self.df['Tipo_Movimiento'] == 'Egreso'].copy()

        if len(df_egresos) == 0:
            return {}

        # Agrupar por Categoria_Final y sumar Débito
        egresos_por_cat = df_egresos.groupby('Categoria_Final')['Débito'].sum()

        # Ordenar de mayor a menor y tomar Top 10
        egresos_por_cat = egresos_por_cat.sort_values(ascending=False).head(10)

        return egresos_por_cat.to_dict()

    def _generar_alertas(self) -> str:
        """
        Genera alertas inteligentes HTML basadas en los datos.

        Returns:
            String HTML con alertas
        """
        alertas_html = []

        # Alerta 1: Clasificación completa
        pct_clasificado = self.metricas['porcentaje_clasificado']
        if pct_clasificado == 100:
            alertas_html.append(
                '<div class="alert alert-success">'
                f'<strong>✅ Sistema funcionando:</strong> {self.metricas["movimientos_clasificados"]} transacciones clasificadas (100%)'
                '</div>'
            )
        elif pct_clasificado >= 95:
            alertas_html.append(
                '<div class="alert alert-info">'
                f'<strong>📊 Buena clasificación:</strong> {self.metricas["movimientos_clasificados"]} de {self.metricas["total_movimientos"]} clasificadas ({pct_clasificado:.1f}%)'
                '</div>'
            )

        # Alerta 2: Sueldos altos
        df_sueldos = self.df[self.df['Categoria_Final'].str.contains('Sueldos', case=False, na=False)]
        if len(df_sueldos) > 0:
            total_sueldos = df_sueldos['Débito'].sum()
            pct_sueldos = (total_sueldos / self.metricas['total_egresos'] * 100) if self.metricas['total_egresos'] > 0 else 0
            if pct_sueldos > 20:
                alertas_html.append(
                    '<div class="alert alert-warning">'
                    f'<strong>⚠️ Sueldos altos:</strong> Representan {pct_sueldos:.1f}% de egresos totales (${total_sueldos:,.0f})'
                    '</div>'
                )

        # Alerta 3: Red prestacional
        df_prestadores = self.df[self.df['Categoria_Principal'] == 'Prestadores']
        if len(df_prestadores) > 0:
            n_prestadores = df_prestadores['Persona_Nombre'].nunique()
            total_prestadores = df_prestadores['Débito'].sum()
            alertas_html.append(
                '<div class="alert alert-info">'
                f'<strong>📊 Red prestacional:</strong> {n_prestadores} prestadores activos este mes (${total_prestadores:,.0f} total)'
                '</div>'
            )

        # Alerta 4: Ingresos DEBIN
        if 'Es_DEBIN' in self.df.columns:
            df_debin = self.df[(self.df['Tipo_Movimiento'] == 'Ingreso') & (self.df['Es_DEBIN'] == True)]
            if len(df_debin) > 0:
                total_debin = df_debin['Crédito'].sum()
                promedio_debin = df_debin['Crédito'].mean()
                alertas_html.append(
                    '<div class="alert alert-info">'
                    f'<strong>💳 Ingresos por DEBIN:</strong> {len(df_debin)} transacciones por ${total_debin:,.0f} (promedio ${promedio_debin:,.0f})'
                    '</div>'
                )

        # Alerta 5: Egresos superan ingresos (ya existente)
        if self.metricas['alerta_egresos_mayores']:
            alertas_html.append(
                '<div class="alert alert-danger">'
                '<strong>⚠️ ALERTA:</strong> Los egresos superan a los ingresos en este período.'
                '</div>'
            )

        # Alerta 6: Diferencia en validación (ya existente)
        if not self.metricas['validacion_saldos_ok']:
            alertas_html.append(
                '<div class="alert alert-warning">'
                f'<strong>⚠️ ADVERTENCIA:</strong> Diferencia en validación de saldos: ${self.metricas["diferencia_validacion"]:,.2f}. '
                'El saldo final no coincide con la fórmula esperada.'
                '</div>'
            )

        return '\n'.join(alertas_html)

    def _calcular_kpis_adicionales(self) -> Dict:
        """
        Calcula KPIs adicionales para el dashboard.

        Returns:
            Diccionario con KPIs: ingresos_debin, prestadores_activos, mayor_cat_egreso, mayor_cat_ingreso
        """
        kpis = {}

        # Ingresos DEBIN
        df_debin = self.df[(self.df['Tipo_Movimiento'] == 'Ingreso') & (self.df['Es_DEBIN'] == True)]
        kpis['ingresos_debin_monto'] = df_debin['Crédito'].sum()
        kpis['ingresos_debin_cant'] = len(df_debin)

        # Prestadores Activos
        df_prestadores = self.df[self.df['Categoria_Principal'] == 'Prestadores']
        kpis['prestadores_activos'] = df_prestadores['Persona_Nombre'].nunique()
        kpis['prestadores_total'] = df_prestadores['Débito'].sum()

        # Mayor categoría de egreso
        egresos_por_cat = self.df[self.df['Tipo_Movimiento'] == 'Egreso'].groupby('Categoria_Final')['Débito'].sum()
        if len(egresos_por_cat) > 0:
            mayor_egreso = egresos_por_cat.idxmax()
            kpis['mayor_cat_egreso_nombre'] = mayor_egreso
            kpis['mayor_cat_egreso_monto'] = egresos_por_cat[mayor_egreso]
            kpis['mayor_cat_egreso_pct'] = (egresos_por_cat[mayor_egreso] / self.metricas['total_egresos'] * 100) if self.metricas['total_egresos'] > 0 else 0
        else:
            kpis['mayor_cat_egreso_nombre'] = 'N/A'
            kpis['mayor_cat_egreso_monto'] = 0
            kpis['mayor_cat_egreso_pct'] = 0

        # Mayor categoría de ingreso
        ingresos_por_cat = self.df[self.df['Tipo_Movimiento'] == 'Ingreso'].groupby('Categoria_Final')['Crédito'].sum()
        if len(ingresos_por_cat) > 0:
            mayor_ingreso = ingresos_por_cat.idxmax()
            kpis['mayor_cat_ingreso_nombre'] = mayor_ingreso
            kpis['mayor_cat_ingreso_monto'] = ingresos_por_cat[mayor_ingreso]
            kpis['mayor_cat_ingreso_pct'] = (ingresos_por_cat[mayor_ingreso] / self.metricas['total_ingresos'] * 100) if self.metricas['total_ingresos'] > 0 else 0
        else:
            kpis['mayor_cat_ingreso_nombre'] = 'N/A'
            kpis['mayor_cat_ingreso_monto'] = 0
            kpis['mayor_cat_ingreso_pct'] = 0

        return kpis

    def _calcular_resumen_categorias(self) -> str:
        """
        Calcula resumen por Categoria_Principal para tabla.

        Returns:
            String JSON con datos de la tabla
        """
        # Agrupar por Categoria_Principal
        resumen = []

        for cat_principal in self.df['Categoria_Principal'].unique():
            if cat_principal == 'Sin Clasificar':
                continue

            df_cat = self.df[self.df['Categoria_Principal'] == cat_principal]

            transacciones = len(df_cat)
            ingresos = df_cat[df_cat['Tipo_Movimiento'] == 'Ingreso']['Crédito'].sum()
            egresos = df_cat[df_cat['Tipo_Movimiento'] == 'Egreso']['Débito'].sum()
            neto = ingresos - egresos

            resumen.append({
                'categoria': cat_principal,
                'transacciones': transacciones,
                'ingresos': ingresos,
                'egresos': egresos,
                'neto': neto
            })

        # Ordenar por egresos descendente
        resumen.sort(key=lambda x: x['egresos'], reverse=True)

        return json.dumps(resumen)

    def _preparar_datos_torta(self, datos: Dict) -> str:
        """
        Prepara datos para gráfico de torta.

        Args:
            datos: Diccionario {categoria: monto}

        Returns:
            String JSON con labels y values
        """
        if not datos:
            return json.dumps({'labels': [], 'values': []})

        labels = list(datos.keys())
        values = list(datos.values())

        return json.dumps({
            'labels': labels,
            'values': values
        })

    def _preparar_datos_flujo(self, df_flujo: pd.DataFrame) -> str:
        """
        Prepara datos para gráfico de flujo de caja.

        Args:
            df_flujo: DataFrame con flujo diario

        Returns:
            String JSON con labels, ingresos y egresos
        """
        if len(df_flujo) == 0:
            return json.dumps({'labels': [], 'ingresos': [], 'egresos': []})

        labels = [str(fecha) for fecha in df_flujo['fecha']]
        ingresos = df_flujo['ingresos'].tolist()
        egresos = df_flujo['egresos'].tolist()

        return json.dumps({
            'labels': labels,
            'ingresos': ingresos,
            'egresos': egresos
        })

    def _generar_tabla_prestadores(self) -> str:
        """
        Genera HTML de la tabla de top prestadores.

        Returns:
            String HTML con la tabla
        """
        if len(self.metricas['top_prestadores']) == 0:
            return ""

        html = """
        <div class="chart-container">
            <div class="chart-title">Top Prestadores</div>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Nombre</th>
                        <th>Monto Total</th>
                    </tr>
                </thead>
                <tbody>
        """

        for i, prestador in enumerate(self.metricas['top_prestadores'], 1):
            html += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{prestador['nombre']}</td>
                        <td>${prestador['monto']:,.2f}</td>
                    </tr>
            """

        html += """
                </tbody>
            </table>
        </div>
        """

        return html

    def _generar_tabla_sin_clasificar(self) -> str:
        """
        Genera HTML de la tabla de movimientos sin clasificar.

        Returns:
            String HTML con la tabla
        """
        if len(self.df_sin_clasificar) == 0:
            return """
        <div class="alert">
            <strong>Excelente!</strong> No hay movimientos sin clasificar.
        </div>
            """

        html = f"""
        <div class="chart-container">
            <div class="chart-title">Movimientos Sin Clasificar ({len(self.df_sin_clasificar)})</div>
            <table>
                <thead>
                    <tr>
                        <th>Fecha</th>
                        <th>Concepto</th>
                        <th>Débito</th>
                        <th>Crédito</th>
                    </tr>
                </thead>
                <tbody>
        """

        # Mostrar máximo 20 movimientos
        for _, row in self.df_sin_clasificar.head(20).iterrows():
            html += f"""
                    <tr>
                        <td>{row['Fecha']}</td>
                        <td>{row['Concepto']}</td>
                        <td>${row['Débito']:,.2f}</td>
                        <td>${row['Crédito']:,.2f}</td>
                    </tr>
            """

        if len(self.df_sin_clasificar) > 20:
            html += f"""
                    <tr>
                        <td colspan="4" style="text-align: center; color: #999;">
                            ... y {len(self.df_sin_clasificar) - 20} más
                        </td>
                    </tr>
            """

        html += """
                </tbody>
            </table>
        </div>
        """

        return html
