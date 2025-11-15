"""
Script para crear archivos Excel de ejemplo para probar el sistema
"""
import pandas as pd
from datetime import datetime, timedelta
import random

# Crear ejemplo de Supervielle (formato ideal)
print("Creando archivo de ejemplo: Supervielle...")

fechas_supervielle = [datetime(2025, 10, 31) - timedelta(days=i) for i in range(15)]

conceptos_supervielle = [
    "Impuesto Débitos y Créditos/CR",
    "Descuento por Promociones",
    "Crédito por Transferencia",
    "Débito por Pago Sueldos",
    "Transferencia por CBU",
    "Credito DEBIN",
    "Comisión Mantenimiento",
    "Crédito por Transferencia"
]

detalles_supervielle = [
    None,
    None,
    "HECTOR GASTON OLMEDO DOCUMENTO: 20336991898",
    "PROCESAMIENTO NOMINA SANARTE",
    "CLINICA ROMAGOSA CUIT: 30712345678",
    "TIPO_DEBIN: 05 ID_DEBIN: 12345 SANARTE SRL",
    None,
    "MARIA GONZALEZ DOCUMENTO: 27123456789"
]

data_supervielle = []
saldo = 1500000.0

for i in range(15):
    es_credito = random.choice([True, False])
    monto = round(random.uniform(5000, 150000), 2)

    if es_credito:
        debito = 0.0
        credito = monto
        saldo += monto
    else:
        debito = monto
        credito = 0.0
        saldo -= monto

    data_supervielle.append({
        'Fecha': fechas_supervielle[i],
        'Concepto': random.choice(conceptos_supervielle),
        'Detalle': random.choice(detalles_supervielle),
        'Débito': debito,
        'Crédito': credito,
        'Saldo': round(saldo, 2)
    })

df_supervielle = pd.DataFrame(data_supervielle)

# Guardar Supervielle
ruta_supervielle = "./input/Ejemplo_Supervielle_2025_10.xlsx"
df_supervielle.to_excel(ruta_supervielle, index=False)
print(f"  OK Creado: {ruta_supervielle} ({len(df_supervielle)} movimientos)")

# Crear ejemplo de Galicia (formato sucio con 16 columnas)
print("\nCreando archivo de ejemplo: Galicia...")

fechas_galicia = [datetime(2025, 10, 31) - timedelta(days=i*2) for i in range(8)]

data_galicia = []
saldo_galicia = 500000.0

for i in range(8):
    es_credito = random.choice([True, False])
    monto = round(random.uniform(10000, 80000), 2)

    if es_credito:
        debitos = 0.0
        creditos = monto
        saldo_galicia += monto
    else:
        debitos = monto
        creditos = 0.0
        saldo_galicia -= monto

    data_galicia.append({
        'Fecha': fechas_galicia[i],
        'Descripción': random.choice(['Percep. Iva', 'Iva', 'Comision Servicio De Cuenta', 'Transferencia Recibida', 'Pago Electronico']),
        'Origen': None,
        'Débitos': debitos,
        'Créditos': creditos,
        'Grupo de Conceptos': random.choice(['000901 - Impuestos', '000808 - Comisiones', '001234 - Transferencias']),
        'Concepto': random.choice(['907172 - PERCEP. IVA', '907171 - IVA', '907394 - COMISION SERVICIO DE CUENTA']),
        'Número de Terminal': None,
        'Observaciones Cliente': None,
        'Número de Comprobante': None,
        'Leyendas Adicionales 1': 'Octubre 2025' if i % 2 == 0 else None,
        'Leyendas Adicionales 2': None,
        'Leyendas Adicionales 3': None,
        'Leyendas Adicionales 4': None,
        'Tipo de Movimiento': 'Imputado',
        'Saldo': round(saldo_galicia, 2)
    })

df_galicia = pd.DataFrame(data_galicia)

# Guardar Galicia
ruta_galicia = "./input/Ejemplo_Galicia_2025_10.xlsx"
df_galicia.to_excel(ruta_galicia, index=False)
print(f"  OK Creado: {ruta_galicia} ({len(df_galicia)} movimientos)")

print(f"\nOK Archivos de ejemplo creados exitosamente en la carpeta input/")
