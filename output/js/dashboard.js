/* ===================================
   SANARTE Dashboard - JavaScript
   =================================== */

// Datos para gráficos
const datosIngresos = {
    "labels": ["Afiliados DEBIN", "Otros Ingresos", "Pacientes Transferencia"],
    "values": [5291443.8100000005, 55683.53, 0.0]
};

const datosEgresos = {
    "labels": ["Comisiones Bancarias", "Gastos Operativos", "Impuestos", "Prestadores", "Servicios", "Sueldos"],
    "values": [330101.89, 1581480.67, 500006.05, 6356029.0, 492236.4, 0.0]
};

const datosFlujo = {
    "labels": ["2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04", "2025-10-05", "2025-10-06", "2025-10-07", "2025-10-08", "2025-10-09", "2025-10-10", "2025-10-11", "2025-10-12", "2025-10-13", "2025-10-14", "2025-10-15", "2025-10-16", "2025-10-17", "2025-10-18", "2025-10-19", "2025-10-20", "2025-10-21", "2025-10-22", "2025-10-23", "2025-10-24", "2025-10-25", "2025-10-26", "2025-10-27", "2025-10-28", "2025-10-29", "2025-10-30", "2025-10-31"],
    "ingresos": [75000.0, 0.0, 175000.0, 0.0, 0.0, 0.0, 0.0, 135000.0, 132469.0, 346998.0, 0.0, 0.0, 39892.0, 1171867.0, 53245.0, 160177.0, 3522.75, 0.0, 0.0, 846092.51, 313409.14, 0.0, 672000.0, 495000.0, 0.0, 0.0, 164000.0, 0.0, 230000.0, 267500.0, 65954.94],
    "egresos": [220937.69999999998, 308395.99, 242600.8, 83754.79, 41366.72, 11265.470000000001, 29840.73, 657425.47, 1359217.8099999998, 181624.03, 48216.32, 61068.770000000004, 17632.86, 206805.53999999998, 1719071.15, 3764.5699999999997, 154991.22, 5522.94, 163660.26, 688669.78, 232417.92, 317103.28, 20668.559999999998, 2078435.55, 65135.04, 10319.789999999999, 85549.01000000001, 32278.01, 86983.64, 125037.58, 92.71000000000001]
};

/**
 * Función reutilizable para crear gráficos de torta (pie chart)
 * @param {string} canvasId - ID del elemento canvas
 * @param {Array} labels - Etiquetas de las categorías
 * @param {Array} values - Valores numéricos
 * @param {Array} colors - Colores para cada sección (opcional)
 * @returns {Chart} - Instancia del gráfico creado
 */
function crearPieChart(canvasId, labels, values, colors = null) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`No se encontró el canvas con id: ${canvasId}`);
        return null;
    }

    // Colores por defecto si no se proporcionan
    const defaultColors = [
        '#28a745', '#20c997', '#17a2b8', '#6610f2', '#e83e8c',
        '#dc3545', '#fd7e14', '#ffc107', '#6f42c1', '#6c757d'
    ];

    return new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors || defaultColors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += '$' + context.parsed.toLocaleString('es-AR', {minimumFractionDigits: 2});
                            return label;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Función para crear gráfico de flujo de caja (líneas)
 * @param {string} canvasId - ID del elemento canvas
 * @param {Array} labels - Etiquetas del eje X (fechas)
 * @param {Array} ingresos - Valores de ingresos
 * @param {Array} egresos - Valores de egresos
 * @returns {Chart} - Instancia del gráfico creado
 */
function crearFlujoCajaChart(canvasId, labels, ingresos, egresos) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`No se encontró el canvas con id: ${canvasId}`);
        return null;
    }

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Ingresos',
                    data: ingresos,
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Egresos',
                    data: egresos,
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += '$' + context.parsed.y.toLocaleString('es-AR', {minimumFractionDigits: 2});
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString('es-AR');
                        }
                    }
                }
            }
        }
    });
}

// Inicialización de gráficos cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    // Gráfico de Ingresos por Categoría
    const coloresIngresos = ['#28a745', '#20c997', '#17a2b8', '#6610f2', '#e83e8c'];
    crearPieChart('chartIngresos', datosIngresos.labels, datosIngresos.values, coloresIngresos);

    // Gráfico de Egresos por Categoría
    const coloresEgresos = ['#dc3545', '#fd7e14', '#ffc107', '#e83e8c', '#6f42c1', '#6c757d'];
    crearPieChart('chartEgresos', datosEgresos.labels, datosEgresos.values, coloresEgresos);

    // Gráfico de Flujo de Caja Diario
    crearFlujoCajaChart('chartFlujo', datosFlujo.labels, datosFlujo.ingresos, datosFlujo.egresos);
});
