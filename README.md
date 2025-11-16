# SANARTE - Sistema de Control Financiero

![Version](https://img.shields.io/badge/version-1.3-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)
![Made with](https://img.shields.io/badge/made%20with-Python-1f425f.svg)

Sistema automatizado para procesamiento de extractos bancarios de múltiples bancos.

**Version:** 1.3 - Bloques 1, 2, 3 y 4 (Consolidador + Categorizador + Reportes + Orquestador CLI)
**Autor:** Sistema SANARTE
**Fecha:** Noviembre 2025

---

## BLOQUES IMPLEMENTADOS

### BLOQUE 1: Consolidador Multi-Banco ✓

1. **Detección automática de banco** por estructura de columnas
2. **Lector Supervielle**: Lectura directa del formato ideal
3. **Lector Galicia**: Limpieza de columnas basura y normalización
4. **Normalizador**: Unificación de formatos de fecha y números
5. **Consolidador**: Une movimientos de múltiples bancos y exporta a Excel

### BLOQUE 2: Categorizador Inteligente ✓

1. **Motor de clasificación** con 24 reglas predefinidas
2. **Categorización automática** de 80%+ de movimientos
3. **Extractor de metadata**: Nombres, CUIT, DEBIN
4. **Sistema de aprendizaje** que mejora con el uso
5. **CLI de corrección manual** para movimientos sin clasificar
6. **Exportación categorizada** a Excel con 14 columnas

### BLOQUE 3: Reportes y Dashboard ✓

1. **Analizador financiero** con métricas clave (ingresos, egresos, saldos inicial/final)
2. **Dashboard HTML interactivo** con Chart.js (gráficos de torta y línea)
3. **Reporte Excel ejecutivo** con 5 hojas formateadas profesionalmente
4. **Saldos inicial/final** en hojas de Ingresos y Egresos
5. **Top 10 prestadores** con montos totales
6. **Flujo de caja diario** visualizado
7. **Alertas automáticas** si egresos > ingresos

### BLOQUE 4: Orquestador CLI ✓

1. **Menú principal interactivo** con interfaz amigable
2. **Proceso completo automatizado** (consolidar → categorizar → reportes)
3. **Ejecución individual de bloques** bajo demanda
4. **Información del sistema** y configuración
5. **Archivo de inicio rápido** (INICIAR.bat para Windows)
6. **Navegación intuitiva** con confirmaciones y mensajes claros

---

## Instalación

### Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto** en tu computadora

2. **Abrir una terminal/consola** en la carpeta del proyecto:
   ```
   cd sanarte_financiero
   ```

3. **Instalar dependencias**:
   ```
   pip install -r requirements.txt
   ```

   Esto instalará:
   - pandas (procesamiento de datos)
   - openpyxl (lectura/escritura de Excel)

---

## Inicio Rápido con Menú Interactivo (RECOMENDADO)

### Opción 1: Usar el Menú Principal (más fácil)

1. **Doble click en el archivo `INICIAR.bat`** (Windows)

   O desde la terminal:
   ```bash
   python menu_principal.py
   ```

2. **Verás un menú con 8 opciones:**
   - Opción 1: Ejecuta todo el proceso completo automáticamente
   - Opción 2: Consolidar TODOS los archivos de la carpeta input
   - Opción 3: Categorizar movimientos
   - Opción 4: Generar reportes y dashboard
   - Opción 7: **NUEVO** - Consolidar con SELECCIÓN de archivos específicos
   - Opción 5: Ver configuración
   - Opción 6: Ver información del sistema
   - Opción 0: Salir

3. **Selecciona la opción deseada** ingresando el número y presionando ENTER

4. **El sistema te guiará paso a paso** con mensajes claros

### Opción 2: Uso Manual con Comandos (avanzado)

Si prefieres usar comandos directos, continúa con la sección "Uso Mensual - Paso a Paso" más abajo.

---

## Selección de Archivos Específicos (NUEVO)

### ¿Cuándo usar esta opción?

- Cuando tienes varios archivos en la carpeta `input/` pero **solo quieres procesar algunos**
- Cuando quieres procesar archivos de diferentes meses por separado
- Cuando quieres excluir temporalmente ciertos archivos sin borrarlos

### Cómo usar la Opción 7: Consolidar con Selección

1. **Coloca todos tus archivos** en la carpeta `input/` (no importa cuántos sean)

2. **Ejecuta INICIAR.bat** y selecciona la **opción 7**

3. **El sistema mostrará** una lista numerada de todos los archivos:
   ```
   ARCHIVOS EXCEL DISPONIBLES EN ./input/
   ================================================================================

     1. Extracto_Galicia_octubre.xlsx
     2. Extracto_Supervielle_octubre.xlsx
     3. Extracto_Galicia_noviembre.xlsx
     4. Extracto_Supervielle_noviembre.xlsx
   ```

4. **Ingresa los números** de los archivos que quieres procesar:
   - Para un solo archivo: `1`
   - Para varios archivos: `1,2` o `1,3,4`
   - Para todos: `1,2,3,4`

5. **Confirma tu selección** y el sistema procesará solo esos archivos

### Ejemplo de Uso

**Escenario:** Tienes extractos de octubre y noviembre, pero solo quieres procesar noviembre.

```
Ingresa tu selección: 3,4

ARCHIVOS SELECCIONADOS:
================================================================================
  - Extracto_Galicia_noviembre.xlsx
  - Extracto_Supervielle_noviembre.xlsx

¿Confirmar selección? (S/N): S

→ El sistema procesará SOLO los archivos de noviembre
```

---

## Uso Mensual - Paso a Paso

### Paso 1: Descargar extractos del homebanking

1. Ingresa al homebanking de **Banco Supervielle**
   - Descarga el extracto mensual en formato Excel (.xlsx)
   - Guárdalo en tu computadora

2. Ingresa al homebanking de **Banco Galicia**
   - Descarga el extracto mensual en formato Excel (.xlsx)
   - Guárdalo en tu computadora

### Paso 2: Colocar archivos en la carpeta input

1. Navega a la carpeta del proyecto: `sanarte_financiero/input/`
2. Copia los archivos Excel descargados en esta carpeta
3. Los nombres de archivo pueden ser cualquiera (el sistema detecta automáticamente el banco)

Ejemplo:
```
sanarte_financiero/
└── input/
    ├── Movimientos_Supervielle_octubre_2025.xlsx
    └── Extracto_Galicia_octubre_2025.xlsx
```

### Paso 3: Ejecutar consolidación

1. Abre una terminal/consola en la carpeta del proyecto
2. Ejecuta el comando:
   ```
   python src/main.py --consolidar
   ```

3. El sistema procesará automáticamente:
   - Detectará el banco de cada archivo
   - Leerá y normalizará los movimientos
   - Consolidará todo en un único archivo

El archivo consolidado se generará en:
```
sanarte_financiero/output/movimientos_consolidados_YYYY_MM.xlsx
```

### Paso 4: Categorizar movimientos

1. Ejecuta el comando de categorización:
   ```
   python src/main.py --categorizar
   ```

2. El sistema:
   - Cargará el archivo consolidado más reciente
   - Categorizará automáticamente 80%+ de los movimientos
   - Mostrará estadísticas de clasificación
   - Preguntará si quieres revisar manualmente los movimientos sin clasificar

3. Si eliges revisar manualmente:
   - El sistema mostrará cada movimiento sin clasificar
   - Podrás seleccionar la categoría correcta
   - Decidir si quieres que el sistema "aprenda" la regla
   - Omitir movimientos o salir en cualquier momento

El archivo categorizado se generará en:
```
sanarte_financiero/output/movimientos_categorizados_YYYY_MM.xlsx
```

### Paso 5: Generar reportes y dashboard

1. Ejecuta el comando de reportes:
   ```
   python src/main.py --reportes
   ```

2. El sistema:
   - Cargará el archivo categorizado más reciente
   - Calculará métricas financieras (ingresos, egresos, balance)
   - Generará dashboard HTML interactivo
   - Creará reporte Excel ejecutivo con 5 hojas
   - Abrirá automáticamente el dashboard en tu navegador

Los archivos generados serán:
```
sanarte_financiero/output/dashboard_YYYY_MM.html
sanarte_financiero/output/reporte_ejecutivo_YYYY_MM.xlsx
```

### Paso 6: Revisar dashboard y reportes

**Dashboard HTML:**
- Abre automáticamente en tu navegador
- Visualiza cards con métricas principales
- Gráficos de torta para ingresos y egresos por categoría
- Gráfico de línea con flujo de caja diario
- Tabla de top prestadores
- Tabla de movimientos sin clasificar

**Reporte Excel:**
- Hoja "Resumen": Métricas principales y desgloses
- Hoja "Ingresos": Todos los ingresos detallados
- Hoja "Egresos": Todos los egresos detallados
- Hoja "Prestadores": Top prestadores con totales
- Hoja "Sin Clasificar": Movimientos pendientes de revisión

---

## Estructura de los Archivos Generados

### Archivo Consolidado

El Excel `movimientos_consolidados_YYYY_MM.xlsx` tiene 7 columnas:

| Columna   | Descripción                                    | Ejemplo                          |
|-----------|------------------------------------------------|----------------------------------|
| Fecha     | Fecha y hora del movimiento                    | 2025-10-31 16:23:45              |
| Concepto  | Tipo de operación                              | Crédito por Transferencia        |
| Detalle   | Información adicional del movimiento           | HECTOR OLMEDO DOCUMENTO: 2033... |
| Débito    | Monto debitado (salida de dinero)              | 150000.00                        |
| Crédito   | Monto acreditado (entrada de dinero)           | 96229.00                         |
| Saldo     | Saldo de la cuenta después del movimiento      | 1450670.50                       |
| Banco     | Banco de origen (Supervielle o Galicia)        | Supervielle                      |

### Archivo Categorizado (NUEVO)

El Excel `movimientos_categorizados_YYYY_MM.xlsx` tiene 14 columnas:

| Columna          | Descripción                                    | Ejemplo                          |
|------------------|------------------------------------------------|----------------------------------|
| *Columnas base*  | Las mismas 7 del consolidado                   | -                                |
| **Categoria**    | Categoría principal (Ingresos/Egresos)         | Egresos                          |
| **Subcategoria** | Subcategoría específica                        | Prestadores                      |
| **Confianza_%**  | Nivel de confianza de la clasificación (0-100) | 95                               |
| **Persona_Nombre** | Nombre extraído del detalle                  | HECTOR GASTON OLMEDO             |
| **Documento**    | CUIT/CUIL/DNI extraído                         | 20336991898                      |
| **Es_DEBIN**     | Indica si es un DEBIN (True/False)             | True                             |
| **DEBIN_ID**     | ID del DEBIN si aplica                         | 12345                            |

---

## Bancos Soportados

### Banco Supervielle

**Formato esperado:**
- 6 columnas: Fecha, Concepto, Detalle, Débito, Crédito, Saldo
- Formato limpio y estructurado
- No requiere limpieza adicional

### Banco Galicia

**Formato esperado:**
- 16 columnas (solo 6 útiles)
- El sistema elimina automáticamente las 10 columnas basura:
  - Origen
  - Número de Terminal
  - Observaciones Cliente
  - Número de Comprobante
  - Leyendas Adicionales 1-4
  - Tipo de Movimiento

**Mapeo realizado:**
- Descripción → Concepto
- Grupo de Conceptos + Concepto → Detalle
- Débitos → Débito
- Créditos → Crédito

---

## Categorías Disponibles

El sistema clasifica automáticamente movimientos en las siguientes categorías:

### INGRESOS
- **Afiliados DEBIN**: Cobros por DEBIN de afiliados
- **Pacientes Transferencia**: Transferencias de pacientes
- **Otros Ingresos**: Descuentos, promociones, otros

### EGRESOS
- **Prestadores**: Pagos a médicos y clínicas (> $10,000)
- **Sueldos**: Pago de nómina (> $1,000,000)
- **Impuestos**: IVA, IIBB, Percepciones, Débitos y Créditos
- **Comisiones Bancarias**: Mantenimiento, IVA operaciones
- **Servicios**: EPEC, Claro, Cablevisión, etc.
- **Gastos Operativos**: Compras, PedidosYa, Visa Débito

---

## Ejemplos de Uso

### Consolidar extractos
```bash
python src/main.py --consolidar
```

### Categorizar movimientos (con revisión manual)
```bash
python src/main.py --categorizar
```

### Categorizar sin revisión manual
```bash
python src/main.py --categorizar --sin-revision
```

### Generar reportes y dashboard
```bash
python src/main.py --reportes
```

### Generar reportes sin abrir navegador
```bash
python src/main.py --reportes --sin-abrir
```

### Proceso completo (consolidar + categorizar + reportes)
```bash
python src/main.py --consolidar
python src/main.py --categorizar
python src/main.py --reportes
```

### Uso con carpetas personalizadas
```bash
python src/main.py --consolidar --input ./mis_extractos --output ./resultados
python src/main.py --categorizar --output ./resultados
python src/main.py --reportes --output ./resultados
```

### Ver ayuda
```bash
python src/main.py --help
```

---

## Troubleshooting

### Error: "No existe la carpeta './input'"
**Solución:** Crea la carpeta `input` en la raíz del proyecto antes de ejecutar.

### Error: "No se encontraron archivos Excel"
**Solución:** Verifica que los archivos en `/input` tengan extensión `.xlsx` (no `.xls` o `.csv`).

### Error: "No se pudo detectar el formato del banco"
**Solución:** Verifica que los archivos descargados tengan el formato correcto de Supervielle o Galicia. Si usas otro banco, contacta al administrador del sistema.

### Los números no se ven bien en Excel
**Solución:** El archivo ya tiene formato aplicado. Si ves puntos en lugar de comas, verifica la configuración regional de Excel (debe estar en español/Argentina).

---

## Sistema de Aprendizaje

El categorizador incluye un sistema de aprendizaje automático:

1. **Reglas Predefinidas**: 24 reglas iniciales en `data/reglas.json`
2. **Aprendizaje Continuo**: Cuando corriges manualmente una categoría y eliges "Recordar regla", el sistema:
   - Extrae un patrón del concepto del movimiento
   - Guarda la nueva regla en `reglas.json`
   - Incrementa la confianza cada vez que confirmas la misma regla
3. **Mejora Progresiva**: Con el tiempo, el % de clasificación automática aumentará

---

## Métricas del Dashboard

El dashboard HTML muestra:

### Cards Superiores
- **Total Ingresos**: Suma de todos los créditos clasificados como Ingresos
- **Total Egresos**: Suma de todos los débitos clasificados como Egresos
- **Balance**: Diferencia entre ingresos y egresos (verde si positivo, rojo si negativo)
- **% Clasificados**: Porcentaje de movimientos categorizados automáticamente

### Gráficos Interactivos
- **Torta de Ingresos**: Distribución por subcategoría (Afiliados DEBIN, Pacientes, Otros)
- **Torta de Egresos**: Distribución por subcategoría (Prestadores, Sueldos, Impuestos, etc.)
- **Línea de Flujo**: Evolución diaria de ingresos vs egresos

### Tablas
- **Top Prestadores**: Los 10 prestadores con mayores pagos acumulados
- **Sin Clasificar**: Movimientos que requieren revisión manual (si existen)

---

## Todos los Bloques Completados ✓

Todos los 4 bloques han sido implementados exitosamente:
- ✓ Bloque 1: Consolidador Multi-Banco
- ✓ Bloque 2: Categorizador Inteligente
- ✓ Bloque 3: Reportes y Dashboard
- ✓ Bloque 4: Orquestador CLI

### Posibles Mejoras Futuras

- Soporte para más bancos (ICBC, Macro, etc.)
- Exportación a PDF de reportes
- Gráficos de tendencia mes a mes
- Predicciones basadas en históricos
- API REST para integraciones

---

## Soporte

Para reportar problemas o solicitar mejoras, contacta al equipo de desarrollo de SANARTE.

---

## Changelog

### v1.3 - Bloque 4: Orquestador CLI (Noviembre 2025)
- **Bloque 4:** Menú Principal Interactivo
  - Menú CLI con interfaz amigable y navegación intuitiva
  - Opción de proceso completo automatizado (3 bloques en secuencia)
  - Ejecución individual de cada bloque bajo demanda
  - Pantalla de información del sistema y configuración
  - Archivo de inicio rápido INICIAR.bat para Windows
  - Confirmaciones y mensajes claros en cada paso
  - Compatibilidad total con Windows (sin emojis problemáticos)
- **Mejoras en Bloque 3:**
  - Agregados saldos inicial/final en hojas Ingresos y Egresos
  - Desglose por subcategoría con porcentajes
  - Mejor separación visual entre resumen y detalle

### v1.2 - Bloques 1, 2 y 3 (Noviembre 2025)
- **Bloque 3:** Reportes y Dashboard
  - Analizador financiero con métricas clave
  - Dashboard HTML interactivo con Chart.js
  - Gráficos de torta (ingresos y egresos por categoría)
  - Gráfico de línea (flujo de caja diario)
  - Reporte Excel ejecutivo con 5 hojas formateadas
  - Top 10 prestadores automático
  - Alertas visuales (egresos > ingresos)
  - Apertura automática en navegador

### v1.1 - Bloques 1 y 2 (Noviembre 2025)
- **Bloque 2:** Categorizador Inteligente
  - Motor de clasificación con 24 reglas predefinidas
  - Categorización automática 80%+ de movimientos
  - Extractor de metadata (nombres, CUIT, DEBIN)
  - Sistema de aprendizaje de reglas
  - CLI para corrección manual interactiva
  - Exportación con 14 columnas (7 base + 7 categorización)

### v1.0 - Bloque 1 (Noviembre 2025)
- Implementación inicial del consolidador multi-banco
- Soporte para Banco Supervielle y Banco Galicia
- Detección automática de formato
- Normalización y exportación a Excel
