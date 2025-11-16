"""
Generador de dashboard HTML interactivo
Autor: Sistema SANARTE
"""
import pandas as pd
import json
from datetime import datetime
from typing import Dict

class DashboardGenerator:
    """
    Genera dashboard HTML interactivo con Chart.js.
    """

    def __init__(self, metricas: Dict, df_sin_clasificar: pd.DataFrame):
        """
        Args:
            metricas: Diccionario con métricas calculadas
            df_sin_clasificar: DataFrame con movimientos sin clasificar
        """
        self.metricas = metricas
        self.df_sin_clasificar = df_sin_clasificar

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
        # Preparar datos para gráficos
        datos_ingresos = self._preparar_datos_torta(self.metricas['ingresos_por_subcategoria'])
        datos_egresos = self._preparar_datos_torta(self.metricas['egresos_por_subcategoria'])
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
            <!-- Alertas -->
            {'<div class="alert alert-danger"><strong>ALERTA:</strong> Los egresos superan a los ingresos en este período.</div>' if self.metricas['alerta_egresos_mayores'] else ''}
            {'<div class="alert"><strong>ADVERTENCIA:</strong> Diferencia en validación de saldos: $' + f"{self.metricas['diferencia_validacion']:,.2f}" + '. El saldo final no coincide con la fórmula esperada.</div>' if not self.metricas['validacion_saldos_ok'] else ''}

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
                    <div class="chart-title">Egresos por Categoría</div>
                    <canvas id="chartEgresos"></canvas>
                </div>

                <!-- Gráfico de Flujo de Caja -->
                <div class="chart-container chart-full">
                    <div class="chart-title">Flujo de Caja Diario</div>
                    <canvas id="chartFlujo"></canvas>
                </div>
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

        // Gráfico de Egresos (Torta)
        new Chart(document.getElementById('chartEgresos'), {{
            type: 'pie',
            data: {{
                labels: datosEgresos.labels,
                datasets: [{{
                    data: datosEgresos.values,
                    backgroundColor: [
                        '#dc3545',
                        '#fd7e14',
                        '#ffc107',
                        '#e83e8c',
                        '#6f42c1',
                        '#6c757d'
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
