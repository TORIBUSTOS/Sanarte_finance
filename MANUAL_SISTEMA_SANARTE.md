# MANUAL TÉCNICO COMPLETO
# SISTEMA SANARTE - CONTROL FINANCIERO

**Versión:** 1.3
**Fecha:** Noviembre 2025
**Autor:** Sistema SANARTE

---

## TABLA DE CONTENIDOS

1. [Descripción General](#1-descripción-general)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Requisitos e Instalación](#3-requisitos-e-instalación)
4. [Flujo Principal de Ejecución](#4-flujo-principal-de-ejecución)
5. [Estructura de Archivos](#5-estructura-de-archivos)
6. [Módulos y Funciones Detalladas](#6-módulos-y-funciones-detalladas)
7. [Guía de Uso](#7-guía-de-uso)
8. [Solución de Problemas](#8-solución-de-problemas)
9. [Notas Técnicas Importantes](#9-notas-técnicas-importantes)

---

## 1. DESCRIPCIÓN GENERAL

### 1.1 ¿Qué problema resuelve?

El sistema SANARTE resuelve el problema de **análisis financiero manual** de extractos bancarios para empresas que:

- Reciben extractos de múltiples bancos en formatos diferentes
- Necesitan categorizar miles de transacciones mensualmente
- Requieren reportes ejecutivos y análisis de flujo de caja
- Deben identificar prestadores, ingresos por pacientes, gastos operativos, etc.

**Sin SANARTE:**
- ❌ Análisis manual en Excel (horas/días de trabajo)
- ❌ Errores humanos en clasificación
- ❌ Formatos inconsistentes entre bancos
- ❌ Difícil seguimiento de prestadores y categorías

**Con SANARTE:**
- ✅ Procesamiento automático en minutos
- ✅ 99%+ de clasificación automática
- ✅ Formato unificado multi-banco
- ✅ Reportes ejecutivos y dashboards instantáneos

### 1.2 ¿Cómo funciona?

El sistema opera en **4 bloques secuenciales**:

```
┌─────────────────┐
│  BLOQUE 1       │  Lee extractos bancarios (.xlsx)
│  CONSOLIDADOR   │  → Detecta banco automáticamente
│                 │  → Normaliza formato
└────────┬────────┘
         │ movimientos_consolidados_2025_XX.xlsx
         ↓
┌─────────────────┐
│  BLOQUE 2       │  Clasifica cada movimiento
│  CATEGORIZADOR  │  → Sistema de cascada 2 niveles
│                 │  → Extrae metadata (DEBIN, nombres, etc.)
└────────┬────────┘
         │ movimientos_categorizados_2025_XX.xlsx
         ↓
┌─────────────────┐
│  BLOQUE 3       │  Genera análisis financiero
│  REPORTES       │  → Calcula métricas (saldos, totales)
│                 │  → Dashboard HTML + Reporte Excel
└────────┬────────┘
         │ dashboard_2025_XX.html
         │ reporte_ejecutivo_2025_XX.xlsx
         ↓
┌─────────────────┐
│  BLOQUE 4       │  Menú interactivo (INICIAR.bat)
│  ORQUESTADOR    │  → Permite ejecutar bloques individualmente
│                 │  → Selección de archivos
└─────────────────┘
```

### 1.3 Tecnologías Utilizadas

- **Python 3.8+**
- **Pandas 2.0+** - Manipulación de datos
- **OpenPyXL 3.1+** - Lectura/escritura de Excel
- **Batch Scripts** - Automatización en Windows

---

## 2. ARQUITECTURA DEL SISTEMA

### 2.1 Diagrama de Componentes

```
sanarte_financiero/
│
├── input/                    # Extractos bancarios originales (.xlsx)
│   └── Movimientos_*.xlsx
│
├── output/                   # Archivos generados
│   ├── movimientos_consolidados_2025_XX.xlsx
│   ├── movimientos_categorizados_2025_XX.xlsx
│   ├── dashboard_2025_XX.html
│   └── reporte_ejecutivo_2025_XX.xlsx
│
├── src/                      # Código fuente
│   ├── main.py              # Punto de entrada principal
│   │
│   ├── readers/             # Lectores por banco
│   │   ├── supervielle_reader.py
│   │   └── galicia_reader.py
│   │
│   ├── processors/          # Procesamiento y clasificación
│   │   ├── normalizer.py
│   │   ├── consolidator.py
│   │   ├── categorizer.py
│   │   ├── clasificador_cascada.py
│   │   └── metadata_extractor.py
│   │
│   ├── reports/             # Generación de reportes
│   │   ├── analyzer.py
│   │   ├── dashboard_generator.py
│   │   └── excel_exporter.py
│   │
│   └── utils/
│       └── cli_corrector.py
│
├── menu_principal.py         # Menú interactivo
├── INICIAR.bat              # Launcher para Windows
└── requirements.txt         # Dependencias Python
```

### 2.2 Flujo de Datos

```
[Excel Banco]
    ↓ (SupervielleReader/GaliciaReader)
[DataFrame Raw]
    ↓ (Normalizer)
[DataFrame Normalizado: Fecha, Concepto, Débito, Crédito, Saldo]
    ↓ (Consolidator)
[movimientos_consolidados.xlsx]
    ↓ (Categorizer + ClasificadorCascada)
[DataFrame + Tipo_Movimiento, Categoria_Principal, Categoria_Final]
    ↓ (ExcelExporter)
[movimientos_categorizados.xlsx]
    ↓ (Analyzer)
[Métricas: Saldos, Ingresos, Egresos, Top Prestadores]
    ↓ (DashboardGenerator + ExcelExporter)
[dashboard.html + reporte_ejecutivo.xlsx]
```

---

## 3. REQUISITOS E INSTALACIÓN

### 3.1 Requisitos del Sistema

**Software:**
- Windows 10/11 (o Linux/Mac con adaptaciones)
- Python 3.8 o superior
- 2 GB RAM mínimo
- 100 MB espacio en disco

**Conocimientos:**
- Básico: Ejecutar archivos .bat, copiar archivos a carpetas
- Avanzado: Python, pandas (solo para desarrollo)

### 3.2 Instalación

#### Paso 1: Instalar Python

```powershell
# Descargar desde https://www.python.org/downloads/
# Durante instalación: ✓ Marcar "Add Python to PATH"
```

#### Paso 2: Descargar el proyecto

```powershell
git clone https://github.com/TORIBUSTOS/Sanarte_finance.git
cd Sanarte_finance
```

#### Paso 3: Instalar dependencias

```powershell
pip install -r requirements.txt
```

**Archivo requirements.txt:**
```
pandas>=2.0.0
openpyxl>=3.1.0
```

#### Paso 4: Verificar instalación

```powershell
python src/main.py --help
```

Si muestra la ayuda, ¡instalación exitosa! ✅

---

## 4. FLUJO PRINCIPAL DE EJECUCIÓN

### 4.1 Ejecución Completa (Recomendada)

**Opción A: Menú Interactivo**

```powershell
.\INICIAR.bat
```

1. Seleccionar opción **1** (Proceso Completo)
2. Elegir número del archivo a procesar
3. Esperar a que termine (1-5 minutos)
4. Revisar reportes en carpeta `output/`

**Opción B: Línea de Comandos**

```powershell
# Paso 1: Consolidar
python src/main.py --consolidar --archivo Movimientos_Supervielle_2025_11.xlsx

# Paso 2: Categorizar
python src/main.py --categorizar --sin-revision

# Paso 3: Reportes
python src/main.py --reportes --sin-abrir
```

### 4.2 Ejecución Individual de Bloques

**Solo Consolidar:**
```powershell
python src/main.py --consolidar --archivo MI_ARCHIVO.xlsx
```

**Solo Categorizar:**
```powershell
python src/main.py --categorizar --sin-revision
```

**Solo Reportes:**
```powershell
python src/main.py --reportes --sin-abrir
```

### 4.3 Parámetros Disponibles

| Parámetro | Descripción | Obligatorio |
|-----------|-------------|-------------|
| `--consolidar` | Ejecuta bloque 1 (consolidación) | - |
| `--categorizar` | Ejecuta bloque 2 (categorización) | - |
| `--reportes` | Ejecuta bloque 3 (reportes) | - |
| `--archivo NOMBRE` | Archivo específico a procesar | ✅ Con --consolidar |
| `--sin-revision` | Omite revisión manual en categorización | - |
| `--sin-abrir` | No abre dashboard automáticamente | - |
| `--input RUTA` | Carpeta de entrada (default: ./input) | - |
| `--output RUTA` | Carpeta de salida (default: ./output) | - |

---

## 5. ESTRUCTURA DE ARCHIVOS

### 5.1 Archivos de Entrada

**Ubicación:** `input/`

**Formato esperado (Supervielle):**
```
| Fecha      | Concepto                  | Detalle              | Débito  | Crédito | Saldo      |
|------------|---------------------------|----------------------|---------|---------|------------|
| 01/11/2025 | Compra Visa Débito        | FARMACIA LIDER S     | 650.00  | 0.00    | 1234567.89 |
| 02/11/2025 | Crédito por Transferencia | PACIENTE JUAN PEREZ  | 0.00    | 5000.00 | 1239567.89 |
```

**Formato esperado (Galicia):**
Similar estructura, con detección automática.

### 5.2 Archivos de Salida

**Ubicación:** `output/`

#### movimientos_consolidados_2025_XX.xlsx
- **Contenido:** Movimientos normalizados de todos los bancos
- **Columnas:** Fecha, Concepto, Detalle, Débito, Crédito, Saldo, Banco
- **Uso:** Input para categorización

#### movimientos_categorizados_2025_XX.xlsx
- **Contenido:** Movimientos con clasificación automática
- **Columnas adicionales:**
  - `Tipo_Movimiento`: Ingreso / Egreso / Neutro
  - `Categoria_Principal`: Impuestos, Ingresos, Gastos Operativos, etc.
  - `Categoria_Final`: Subcategoría refinada (ej: "Impuestos - IVA")
  - `Persona_Nombre`: Nombre extraído del detalle (si aplica)
  - `Documento`: DNI/CUIT extraído (si aplica)
  - `Es_DEBIN`: True/False
  - `DEBIN_ID`: ID del DEBIN (si aplica)

#### dashboard_2025_XX.html
- **Contenido:** Dashboard interactivo con gráficos
- **Secciones:**
  - Resumen ejecutivo
  - Gráfico de ingresos vs egresos
  - Top 10 egresos por categoría
  - Top 10 prestadores
  - Timeline de movimientos

#### reporte_ejecutivo_2025_XX.xlsx
- **Contenido:** Reporte Excel con 5 hojas
- **Hojas:**
  1. **Resumen:** Métricas principales
  2. **Ingresos:** Desglose completo de ingresos
  3. **Egresos:** Desglose completo de egresos
  4. **Top Egresos:** Los 10 mayores egresos
  5. **Sin Clasificar:** Movimientos que requieren revisión manual

---

## 6. MÓDULOS Y FUNCIONES DETALLADAS

### 6.1 BLOQUE 1: CONSOLIDADOR

#### src/readers/supervielle_reader.py

**Clase:** `SupervielleReader`

**Funciones principales:**

##### `detectar_formato(df: pd.DataFrame) -> bool`
- **Propósito:** Detecta si el Excel es de Banco Supervielle
- **Lógica:** Busca columnas "Fecha", "Concepto", "Débito", "Crédito"
- **Returns:** True si es Supervielle, False si no

##### `leer(ruta_archivo: str) -> pd.DataFrame`
- **Propósito:** Lee el archivo Excel de Supervielle y lo convierte a DataFrame
- **Pasos:**
  1. Lee Excel con `pd.read_excel()`
  2. Busca la fila donde empieza la tabla (primera fila con "Fecha")
  3. Usa esa fila como headers
  4. Lee datos desde la siguiente fila
  5. Limpia valores nulos
- **Returns:** DataFrame con columnas normalizadas

**Ejemplo de uso:**
```python
reader = SupervielleReader()
df = reader.leer("input/Movimientos_Supervielle_2025_11.xlsx")
# df contiene: Fecha, Concepto, Detalle, Débito, Crédito, Saldo
```

#### src/readers/galicia_reader.py

**Clase:** `GaliciaReader`

Similar a SupervielleReader, pero adaptado al formato de Banco Galicia.

#### src/processors/normalizer.py

**Clase:** `Normalizer`

##### `normalizar(df: pd.DataFrame) -> pd.DataFrame`
- **Propósito:** Normaliza formatos de fechas, números, y limpia datos
- **Operaciones:**
  1. Convierte fechas a formato estándar (YYYY-MM-DD)
  2. Convierte débito/crédito a float
  3. Rellena NaN con 0.0
  4. Limpia espacios en strings
- **Returns:** DataFrame normalizado

#### src/processors/consolidator.py

**Clase:** `Consolidator`

##### `consolidar(dataframes: List[pd.DataFrame]) -> pd.DataFrame`
- **Propósito:** Combina DataFrames de múltiples bancos
- **Lógica:**
  1. Concatena todos los DataFrames
  2. Elimina duplicados
  3. Ordena por fecha
- **Returns:** DataFrame consolidado único

##### `exportar(df: pd.DataFrame) -> str`
- **Propósito:** Exporta a Excel en carpeta output/
- **Nombre archivo:** `movimientos_consolidados_YYYY_MM.xlsx`
- **Returns:** Ruta del archivo generado

---

### 6.2 BLOQUE 2: CATEGORIZADOR

#### src/processors/clasificador_cascada.py

**Clase:** `ClasificadorCascada`

Este es el **corazón del sistema de clasificación**. Usa un sistema de **cascada de 2 niveles**:

**Nivel 1:** Clasificación por "Concepto"
**Nivel 2:** Refinamiento por "Detalle"

##### `__init__()`
- **Propósito:** Inicializa reglas de clasificación
- **Estructura de reglas:**

```python
self.reglas_concepto = {
    # Nivel 1: Patrones en el campo "Concepto"
    'impuesto': 'Impuestos',
    'percepción': 'Impuestos',
    'débitos y créditos': 'Impuestos',
    'compra': 'Gastos Operativos',
    'transferencia': 'Ingresos',
    'debin': 'Ingresos',
    # ... 37 reglas totales
}

self.reglas_refinamiento = {
    # Nivel 2: Patrones en el campo "Detalle" para refinar categorías
    'Impuestos': {
        'afip': 'Impuestos - AFIP',
        'iva': 'Impuestos - IVA',
        'rg 5617': 'Impuestos - Percepciones',
        # ... 24 patrones de refinamiento
    },
    'Ingresos': {
        'debin': 'Ingresos - DEBIN Afiliados',
        'transferencia': 'Ingresos - Transferencias',
        # ...
    }
}
```

##### `clasificar_movimiento(concepto, detalle, debito, credito) -> Tuple`
- **Propósito:** Clasifica un movimiento individual
- **Algoritmo:**

```python
# 1. Determinar Tipo_Movimiento
UMBRAL_MINIMO = 0.01  # Importante: evita valores microscópicos (5e-324)

if credito >= UMBRAL_MINIMO:
    tipo_movimiento = "Ingreso"
elif debito >= UMBRAL_MINIMO:
    tipo_movimiento = "Egreso"
else:
    tipo_movimiento = "Neutro"

# 2. Buscar coincidencia en reglas_concepto
concepto_lower = concepto.lower()
for patron, categoria in reglas_concepto.items():
    if patron in concepto_lower:
        categoria_base = categoria
        break

# 3. Intentar refinar con reglas_refinamiento
if categoria_base in reglas_refinamiento:
    detalle_upper = detalle.upper()
    for patron, categoria_final in reglas_refinamiento[categoria_base].items():
        if patron in detalle_upper:
            return (tipo_movimiento, categoria_base, categoria_final, 100)

# 4. Si no se pudo refinar, devolver categoría base
return (tipo_movimiento, categoria_base, categoria_base, 100)
```

- **Returns:** `(tipo_movimiento, categoria_principal, categoria_final, confianza)`
  - `tipo_movimiento`: "Ingreso" | "Egreso" | "Neutro"
  - `categoria_principal`: "Impuestos", "Ingresos", etc.
  - `categoria_final`: "Impuestos - IVA", "Ingresos - DEBIN", etc.
  - `confianza`: 0 (sin clasificar) o 100 (clasificado)

**Ejemplo:**
```python
clasificador = ClasificadorCascada()

# Movimiento: Débito de $500 por "Impuesto Débitos y Créditos/DB"
tipo, cat_principal, cat_final, conf = clasificador.clasificar_movimiento(
    concepto="Impuesto Débitos y Créditos/DB",
    detalle="",
    debito=500.0,
    credito=0.0
)
# Resultado:
# tipo = "Egreso" (porque debito > 0.01)
# cat_principal = "Impuestos" (porque "débitos y créditos" en concepto)
# cat_final = "Impuestos - Débitos y Créditos"
# conf = 100
```

#### src/processors/metadata_extractor.py

**Clase:** `MetadataExtractor`

##### `extraer_metadata(concepto, detalle) -> dict`
- **Propósito:** Extrae información adicional de los movimientos
- **Extrae:**
  - `persona_nombre`: Nombres propios (ej: "JUAN PEREZ")
  - `documento`: DNI/CUIT (patrones numéricos)
  - `es_debin`: True si es un DEBIN
  - `debin_id`: ID del DEBIN (si aplica)

**Ejemplo:**
```python
extractor = MetadataExtractor()
metadata = extractor.extraer_metadata(
    concepto="Débito DEBIN",
    detalle="TOSIN SONIA BEATRIZ DNI 12345678 ID:ABC123"
)
# Resultado:
# {
#     'persona_nombre': 'TOSIN SONIA BEATRIZ',
#     'documento': '12345678',
#     'es_debin': True,
#     'debin_id': 'ABC123'
# }
```

#### src/processors/categorizer.py

**Clase:** `Categorizer`

##### `categorizar(df: pd.DataFrame) -> pd.DataFrame`
- **Propósito:** Orquesta la categorización de todo el DataFrame
- **Algoritmo:**

```python
# 1. Crear columnas nuevas
df['Tipo_Movimiento'] = None
df['Categoria_Principal'] = None
df['Categoria_Final'] = None
df['Persona_Nombre'] = None
df['Documento'] = None
df['Es_DEBIN'] = False
df['DEBIN_ID'] = None

# 2. Iterar por cada fila
for idx, row in df.iterrows():
    # 2.1 Clasificar
    tipo, cat_p, cat_f, conf = clasificador.clasificar_movimiento(
        row['Concepto'], row['Detalle'], row['Débito'], row['Crédito']
    )

    # 2.2 Extraer metadata
    metadata = extractor.extraer_metadata(row['Concepto'], row['Detalle'])

    # 2.3 Asignar a DataFrame
    df.at[idx, 'Tipo_Movimiento'] = tipo
    df.at[idx, 'Categoria_Principal'] = cat_p
    df.at[idx, 'Categoria_Final'] = cat_f
    df.at[idx, 'Persona_Nombre'] = metadata['persona_nombre']
    # ... etc

# 3. Retornar DataFrame enriquecido
return df
```

##### `exportar_categorizados(df, ruta_salida)`
- **Propósito:** Exporta a Excel con nombre `movimientos_categorizados_YYYY_MM.xlsx`
- **Formato:** Hoja única "Movimientos Categorizados"

---

### 6.3 BLOQUE 3: REPORTES

#### src/reports/analyzer.py

**Clase:** `Analyzer`

Esta clase calcula **todas las métricas financieras**.

##### `__init__(df: pd.DataFrame)`
- **Propósito:** Inicializa con DataFrame categorizado
- **Importante:** Filtra movimientos inválidos (Fecha = NaT) automáticamente

```python
# Filtrar movimientos sin fecha válida
df_limpio = df[df['Fecha'].notna()].copy()
```

##### `calcular_metricas() -> dict`
- **Propósito:** Calcula todas las métricas del sistema
- **Métricas calculadas:**

```python
metricas = {
    'saldo_inicial': float,
    'saldo_final': float,
    'total_ingresos': float,
    'total_egresos': float,
    'total_ingresos_clasificados': float,
    'total_egresos_clasificados': float,
    'total_ingresos_sin_clasificar': float,
    'total_egresos_sin_clasificar': float,
    'variacion': float,
    'diferencia_validacion': float,
    'total_movimientos': int,
    'movimientos_clasificados': int,
    'movimientos_sin_clasificar': int,
    'porcentaje_clasificados': float,
    'desglose_ingresos': dict,    # {categoria: monto}
    'desglose_egresos': dict,     # {categoria: monto}
    'top_prestadores': list,      # [(nombre, monto), ...]
}
```

##### `_calcular_saldos() -> Tuple[float, float]`
- **Propósito:** Calcula saldo inicial y final
- **Lógica crítica:**

```python
# Ordenar por fecha
df_ordenado = df.sort_values('Fecha')

# Saldo final: último movimiento (DESPUÉS del último movimiento)
saldo_final = df_ordenado.iloc[-1]['Saldo']

# Saldo inicial: ANTES del primer movimiento
# El saldo en Excel es DESPUÉS del movimiento
# Fórmula: Saldo_Antes = Saldo_Después - Crédito + Débito
primer_movimiento = df_ordenado.iloc[0]
saldo_despues_primer_mov = primer_movimiento['Saldo']
credito_primer_mov = primer_movimiento['Crédito'] if pd.notna(...) else 0
debito_primer_mov = primer_movimiento['Débito'] if pd.notna(...) else 0

saldo_inicial = saldo_despues_primer_mov - credito_primer_mov + debito_primer_mov

return saldo_inicial, saldo_final
```

**Ejemplo:**
```
Primer movimiento: 01/11/2025
  Débito: $1,650.00
  Crédito: $0.00
  Saldo (DESPUÉS): $607.82

Cálculo saldo inicial:
  Saldo_Inicial = 607.82 - 0.00 + 1650.00 = 2,257.82

Interpretación: Antes del movimiento, tenía $2,257.82
                Después de débito de $1,650, quedó $607.82
```

##### `_calcular_ingresos() -> float`
- **Propósito:** Suma todos los movimientos con Tipo_Movimiento = "Ingreso"
- **Fórmula:** `SUM(Crédito WHERE Tipo_Movimiento = 'Ingreso')`

##### `_calcular_egresos() -> float`
- **Propósito:** Suma todos los movimientos con Tipo_Movimiento = "Egreso"
- **Fórmula:** `SUM(Débito WHERE Tipo_Movimiento = 'Egreso')`

##### `_desglosar_por_categoria(df, tipo) -> dict`
- **Propósito:** Agrupa movimientos por categoria y suma montos
- **Returns:** `{categoria: monto}` ordenado descendente

#### src/reports/dashboard_generator.py

**Clase:** `DashboardGenerator`

##### `__init__(df, metricas)`
- **Propósito:** Inicializa con DataFrame y métricas calculadas

##### `generar(ruta_salida) -> str`
- **Propósito:** Genera dashboard HTML interactivo
- **Componentes:**
  1. **Header:** Logo y título
  2. **Resumen ejecutivo:** Cards con métricas principales
  3. **Gráfico de barras:** Ingresos vs Egresos
  4. **Gráfico de dona:** Distribución de egresos
  5. **Tabla:** Top 10 prestadores
  6. **Timeline:** Últimos 20 movimientos

- **Tecnología:** HTML + CSS inline (no requiere JavaScript)
- **Responsive:** Se adapta a móvil/tablet/desktop

#### src/reports/excel_exporter.py

**Clase:** `ExcelExporter`

##### `generar_reporte_ejecutivo(df, metricas, ruta_salida)`
- **Propósito:** Genera archivo Excel con 5 hojas
- **Estructura:**

**Hoja 1: Resumen**
```
+----------------------------------+------------------+
| Concepto                         | Valor            |
+----------------------------------+------------------+
| SANARTE - RESUMEN EJECUTIVO      |                  |
| SALDOS BANCARIOS                 |                  |
| Saldo Inicial                    | $2,257.82        |
| Total Ingresos                   | $22,827,126.31   |
| Total Egresos                    | $19,612,632.86   |
| Saldo Final                      | $1,336,671.62    |
| ...                              | ...              |
+----------------------------------+------------------+
```

**Hoja 2: Ingresos**
- Tabla con todos los movimientos donde Tipo_Movimiento = "Ingreso"
- Columnas: Fecha, Concepto, Detalle, Monto, Categoría

**Hoja 3: Egresos**
- Tabla con todos los movimientos donde Tipo_Movimiento = "Egreso"
- Columnas: Fecha, Concepto, Detalle, Monto, Categoría

**Hoja 4: Top Egresos**
- Los 10 mayores egresos individuales
- Ordenado descendente por monto

**Hoja 5: Sin Clasificar**
- Movimientos con Categoria_Principal = "Sin Clasificar"
- Requieren revisión manual

---

### 6.4 BLOQUE 4: ORQUESTADOR

#### menu_principal.py

**Función:** `seleccionar_archivo_input() -> str`
- **Propósito:** Muestra archivos .xlsx en ./input y permite seleccionar uno
- **Interfaz:**

```
================================================================================
ARCHIVOS DISPONIBLES EN './input':
================================================================================

  1. Movimientos_Supervielle_2025_11_18_.xlsx (34.5 KB)
  2. Ejemplo_Galicia_2025_10.xlsx (5.8 KB)

  0. Cancelar

Selecciona el número del archivo a procesar: _
```

- **Validación:**
  - Verifica que input sea número
  - Verifica que esté en rango válido
  - Maneja Ctrl+C (cancela operación)

- **Returns:** Nombre del archivo (ej: "Movimientos_Supervielle_2025_11_18_.xlsx") o None

**Función:** `proceso_completo()`
- **Propósito:** Ejecuta los 3 bloques secuencialmente
- **Flujo:**

```python
# 1. Seleccionar archivo
archivo = seleccionar_archivo_input()
if archivo is None:
    return

# 2. Consolidar
df, archivo_consolidado = consolidar_bancos(archivo_especifico=archivo)

# 3. Categorizar
df, archivo_categorizado = categorizar_movimientos(
    ruta_archivo_consolidado=archivo_consolidado
)

# 4. Reportes
generar_reportes(ruta_archivo_categorizado=archivo_categorizado)

# 5. Mostrar resumen
print("Proceso completado exitosamente")
```

**Función:** `solo_consolidar()`, `solo_categorizar()`, `solo_reportes()`
- **Propósito:** Ejecuta bloques individuales
- Similar a proceso_completo() pero ejecuta solo un paso

#### src/main.py

**Función:** `main()`
- **Propósito:** Parser de argumentos de línea de comandos
- **Parser:** Usa `argparse` para manejar flags

```python
parser = argparse.ArgumentParser(
    description="Sistema SANARTE - Control Financiero"
)

parser.add_argument('--consolidar', action='store_true')
parser.add_argument('--categorizar', action='store_true')
parser.add_argument('--reportes', action='store_true')
parser.add_argument('--archivo', type=str, default=None)
parser.add_argument('--sin-revision', action='store_true')
parser.add_argument('--sin-abrir', action='store_true')
parser.add_argument('--input', type=str, default='./input')
parser.add_argument('--output', type=str, default='./output')

args = parser.parse_args()

# Ejecutar según flags
if args.consolidar:
    consolidar_bancos(
        ruta_input=args.input,
        ruta_output=args.output,
        archivo_especifico=args.archivo  # OBLIGATORIO
    )

if args.categorizar:
    categorizar_movimientos(
        ruta_archivo_consolidado=args.archivo,
        ruta_output=args.output,
        revisar_manual=not args.sin_revision
    )

if args.reportes:
    generar_reportes(
        ruta_archivo_categorizado=args.archivo,
        ruta_output=args.output,
        abrir_dashboard=not args.sin_abrir
    )
```

---

## 7. GUÍA DE USO

### 7.1 Uso Básico (Usuarios No Técnicos)

#### Paso 1: Preparar archivo

1. Descargar extracto bancario en Excel
2. Copiar a carpeta `input/`
3. Verificar que sea formato `.xlsx` (no `.xls`)

#### Paso 2: Ejecutar sistema

1. Hacer doble clic en `INICIAR.bat`
2. Elegir opción **1** (Proceso Completo)
3. Seleccionar número del archivo
4. Esperar (1-5 minutos según tamaño)

#### Paso 3: Revisar resultados

Abrir carpeta `output/`:
- **dashboard_2025_11.html** → Abrir en navegador
- **reporte_ejecutivo_2025_11.xlsx** → Abrir en Excel

### 7.2 Uso Avanzado (Línea de Comandos)

#### Procesar archivo específico

```powershell
# Consolidar un archivo
python src/main.py --consolidar --archivo Movimientos_Supervielle_2025_11.xlsx

# Categorizar (usa el consolidado más reciente)
python src/main.py --categorizar --sin-revision

# Generar reportes
python src/main.py --reportes --sin-abrir
```

#### Cambiar carpetas de entrada/salida

```powershell
python src/main.py --consolidar \
    --archivo MI_ARCHIVO.xlsx \
    --input C:\MisExtracts \
    --output C:\MisReportes
```

#### Automatización con scripts

```batch
@echo off
REM Procesar automáticamente archivo de hoy
set FECHA=%date:~-4,4%_%date:~-7,2%_%date:~-10,2%
set ARCHIVO=Movimientos_Supervielle_%FECHA%.xlsx

python src/main.py --consolidar --archivo %ARCHIVO%
python src/main.py --categorizar --sin-revision
python src/main.py --reportes --sin-abrir

echo Proceso completado: %FECHA%
```

### 7.3 Revisión Manual de Clasificación

Si NO usas `--sin-revision`, el sistema abre una CLI interactiva para corregir movimientos sin clasificar:

```
================================================================================
MOVIMIENTOS SIN CLASIFICAR (3 encontrados)
================================================================================

Movimiento 1/3:
  Fecha: 2025-11-15
  Concepto: PAGO VARIOS
  Detalle: REF: 12345
  Débito: $5,000.00

Categoría sugerida: Egresos - Transferencias Varias

¿Es correcta? (S/N/E para editar): s
```

---

## 8. SOLUCIÓN DE PROBLEMAS

### 8.1 Errores Comunes

#### Error: "No se reconoce como nombre de un cmdlet"

**Causa:** PowerShell no encuentra el archivo
**Solución:**
```powershell
# Usar .\ antes del nombre
.\INICIAR.bat
```

#### Error: "Permission denied" al escribir Excel

**Causa:** El archivo está abierto en Excel
**Solución:**
1. Cerrar Excel
2. Volver a ejecutar el comando

#### Error: "Debes especificar un archivo con --archivo"

**Causa:** Usaste `--consolidar` sin `--archivo`
**Solución:**
```powershell
# Agregar --archivo
python src/main.py --consolidar --archivo MI_ARCHIVO.xlsx
```

#### Advertencia: "La columna 'Saldo' existe pero no tiene valores"

**Causa:** Hay movimientos con Saldo = NaN
**Solución:** El sistema automáticamente filtra estos movimientos. Revisar si el archivo de entrada está corrupto.

#### Bug: Todos los movimientos marcados como "Ingreso"

**Causa:** Valores microscópicos (5e-324) en columna Crédito
**Solución:** Ya corregido en versión actual con umbral de 0.01. Actualizar código:
```powershell
git pull origin claude/resolve-analyzer-merge-conflict-01ArCAYCdBKWKAzQZGstJ6ur
```

### 8.2 Verificación de Integridad

#### Verificar clasificación correcta

```powershell
python -c "import pandas as pd; df = pd.read_excel('output/movimientos_categorizados_2025_11.xlsx', sheet_name='Movimientos Categorizados'); print(df['Tipo_Movimiento'].value_counts())"
```

**Output esperado:**
```
Egreso     ~298
Ingreso    ~41
Neutro     ~1
```

#### Verificar saldos

```powershell
python -c "import pandas as pd; df = pd.read_excel('output/reporte_ejecutivo_2025_11.xlsx', sheet_name='Resumen'); print(df[['Concepto', 'Valor']].head(10))"
```

**Verificar que:**
- Saldo Inicial ≠ NaN
- Saldo Final ≠ NaN
- Saldo Final ≈ Saldo Inicial + Ingresos - Egresos (puede haber pequeña diferencia por transacciones fuera del extracto)

---

## 9. NOTAS TÉCNICAS IMPORTANTES

### 9.1 Umbral Mínimo en Tipo_Movimiento

**Problema histórico:** Celdas vacías en Excel se leían como `5e-324` (número microscópico).

**Solución implementada:**
```python
UMBRAL_MINIMO = 0.01  # 1 centavo

if credito >= UMBRAL_MINIMO:
    tipo_movimiento = "Ingreso"
elif debito >= UMBRAL_MINIMO:
    tipo_movimiento = "Egreso"
else:
    tipo_movimiento = "Neutro"
```

**Implicación:** Movimientos con débito/crédito < $0.01 se marcan como "Neutro".

### 9.2 Cálculo de Saldo Inicial

**Concepto clave:** El saldo en el extracto bancario es **DESPUÉS** de aplicar el movimiento.

```
Ejemplo:
  Saldo antes del mov: $10,000
  Débito: $2,000
  Saldo en Excel: $8,000  ← Este es el que aparece

Para calcular saldo inicial:
  Saldo_Inicial = Saldo_Excel - Crédito + Débito
  Saldo_Inicial = 8,000 - 0 + 2,000 = 10,000
```

### 9.3 Archivo Específico Obligatorio

**Decisión de diseño:** No se permite consolidar múltiples archivos juntos.

**Razón:** Mezclar archivos de diferentes períodos rompe los cálculos de saldo:
```
Archivo A (Octubre):
  Saldo inicial: $5,000
  Saldo final: $10,000

Archivo B (Noviembre):
  Saldo inicial: $10,000
  Saldo final: $15,000

Si se consolidan juntos:
  Saldo inicial: $5,000 (de A)
  Saldo final: $15,000 (de B)
  ✅ Parece correcto

PERO: Los movimientos intermedios rompen la secuencia cronológica
y pueden causar errores en análisis de flujo de caja.
```

**Solución:** Procesar un archivo a la vez con `--archivo NOMBRE.xlsx` obligatorio.

### 9.4 Filtrado de Movimientos Inválidos

El `Analyzer` automáticamente filtra movimientos con:
- `Fecha = NaT` (Not a Time)
- Filas totalmente vacías
- Filas de suma/totales que el reader captura por error

```python
# En Analyzer.__init__()
df_limpio = df[df['Fecha'].notna()].copy()
```

### 9.5 Categorías Soportadas

**Categorías Principales (Nivel 1):**
1. Impuestos
2. Ingresos
3. Gastos Operativos
4. Prestadores
5. Comisiones Bancarias
6. Servicios
7. Egresos
8. Sin Clasificar

**Subcategorías (Nivel 2 - ejemplos):**
- Impuestos → Impuestos - AFIP, Impuestos - IVA, Impuestos - Percepciones
- Ingresos → Ingresos - DEBIN, Ingresos - Transferencias, Ingresos - Cheques
- Prestadores → Prestadores - Profesionales, Prestadores - Farmacias

### 9.6 Estructura de Commits

El proyecto usa mensajes de commit descriptivos:

```
Formato:
  <Acción> <descripción breve>

  PROBLEMA/MOTIVACIÓN:
  <Explicación del por qué>

  SOLUCIÓN:
  <Qué se hizo>

  RESULTADOS:
  <Verificación de que funciona>
```

**Ejemplo:**
```
Corregir bug crítico: usar umbral mínimo para Tipo_Movimiento

BUG IDENTIFICADO:
Las celdas "vacías" del Excel se leían como 5e-324...

SOLUCIÓN:
Usar umbral de 0.01 (1 centavo) en lugar de > 0...

RESULTADO:
Ahora clasifica correctamente movimientos...
```

### 9.7 Extensibilidad

Para **agregar un nuevo banco**:

1. Crear `src/readers/NUEVO_BANCO_reader.py`:
```python
class NuevoBancoReader:
    def detectar_formato(self, df):
        # Lógica para detectar formato
        return True/False

    def leer(self, ruta_archivo):
        # Leer Excel y normalizar
        return df
```

2. Registrar en `src/main.py` → `detectar_banco()`:
```python
# Probar Nuevo Banco
nuevo_banco = NuevoBancoReader()
if nuevo_banco.detectar_formato(df):
    return "NuevoBanco", nuevo_banco
```

Para **agregar nueva categoría**:

Editar `src/processors/clasificador_cascada.py`:
```python
self.reglas_concepto = {
    # ... reglas existentes
    'nueva_palabra_clave': 'Nueva Categoría',
}

self.reglas_refinamiento = {
    'Nueva Categoría': {
        'patron1': 'Nueva Categoría - Subcategoria 1',
        'patron2': 'Nueva Categoría - Subcategoria 2',
    }
}
```

---

## APÉNDICES

### A. Glosario de Términos

| Término | Definición |
|---------|------------|
| **Consolidar** | Unificar extractos de diferentes bancos en un formato estándar |
| **Categorizar** | Clasificar movimientos en categorías (Impuestos, Ingresos, etc.) |
| **DataFrame** | Estructura de datos tabular de pandas (como Excel en Python) |
| **DEBIN** | Débito Inmediato - Sistema de cobro electrónico argentino |
| **Egreso** | Salida de dinero (débito) |
| **Ingreso** | Entrada de dinero (crédito) |
| **Neutro** | Movimiento con débito y crédito = 0 (ej: comisión bonificada) |
| **Normalizar** | Convertir datos a formato estándar |
| **Saldo** | Balance de cuenta bancaria |

### B. Estructura de Datos

#### DataFrame Consolidado

```python
{
    'Fecha': datetime,          # 2025-11-15
    'Concepto': str,            # "Compra Visa Débito"
    'Detalle': str,             # "FARMACIA LIDER S"
    'Débito': float,            # 650.00
    'Crédito': float,           # 0.00
    'Saldo': float,             # 1234567.89
    'Banco': str                # "Supervielle"
}
```

#### DataFrame Categorizado

```python
{
    # ... columnas anteriores +
    'Tipo_Movimiento': str,     # "Egreso"
    'Categoria_Principal': str,  # "Gastos Operativos"
    'Categoria_Final': str,     # "Gastos Operativos - Compras Varias"
    'Persona_Nombre': str,      # "FARMACIA LIDER S" (o None)
    'Documento': str,           # "12345678" (o None)
    'Es_DEBIN': bool,           # False
    'DEBIN_ID': str             # None
}
```

#### Métricas (dict)

```python
{
    'saldo_inicial': 2257.82,
    'saldo_final': 1336671.62,
    'total_ingresos': 22827126.31,
    'total_egresos': 19612632.86,
    'variacion': 3214493.45,
    'total_movimientos': 340,
    'movimientos_clasificados': 339,
    'porcentaje_clasificados': 99.7,
    'desglose_ingresos': {
        'Ingresos - Transferencias': 9685214.71,
        'Ingresos - DEBIN Afiliados': 5023685.00,
        # ...
    },
    'desglose_egresos': {
        'Egresos - Transferencias Varias': 8239556.00,
        'Gastos Operativos - Sueldos': 2400000.00,
        # ...
    },
    'top_prestadores': [
        ('TOSIN SONIA BEATRIZ', 600000.00),
        ('TOSIN MARCO ANTONIO', 600000.00),
        # ...
    ]
}
```

### C. Patrones de Clasificación

#### Impuestos
- débitos y créditos
- percepción
- rg 5617
- afip
- iva
- iibb
- sellos

#### Ingresos
- transferencia
- debin
- cheque
- obra social
- osde
- swiss medical

#### Gastos Operativos
- compra
- pago
- mercadolibre
- mercado libre
- sueldo
- viático

#### Prestadores
- profesional
- farmacia
- dr.
- dra.
- lic.

#### Comisiones Bancarias
- comisión
- mantenimiento
- interés
- mora

#### Servicios
- luz
- gas
- agua
- internet
- telefon
- cable

### D. Referencias

**Documentación de dependencias:**
- Pandas: https://pandas.pydata.org/docs/
- OpenPyXL: https://openpyxl.readthedocs.io/

**Python:**
- Guía oficial: https://docs.python.org/3/
- Tutorial argparse: https://docs.python.org/3/library/argparse.html

**Git:**
- Repositorio: https://github.com/TORIBUSTOS/Sanarte_finance
- Branch actual: `claude/resolve-analyzer-merge-conflict-01ArCAYCdBKWKAzQZGstJ6ur`

---

## CONTACTO Y SOPORTE

Para reportar bugs o solicitar nuevas funcionalidades, crear un issue en:
https://github.com/TORIBUSTOS/Sanarte_finance/issues

---

**FIN DEL MANUAL**

---

*Versión del manual: 1.3*
*Última actualización: 18 de Noviembre, 2025*
*Sistema SANARTE - Control Financiero*
