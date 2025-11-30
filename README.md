# 🐂 TORO · Resumen de Cuentas

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)
![Tests](https://img.shields.io/badge/tests-26%20passed-success.svg)
![Coverage](https://img.shields.io/badge/coverage-90%25%20core-brightgreen.svg)
![Status](https://img.shields.io/badge/status-production-success.svg)

Sistema profesional de análisis y control financiero con procesamiento automatizado de extractos bancarios multi-banco.

**Versión:** 2.0.0 - Release de Producción
**Sistema:** TORO (anteriormente SANARTE)
**Autor:** Sistema TORO
**Fecha:** Noviembre 2025

---

## ✨ Novedades en v2.0.0

### 🚀 Motor ClasificadorCascada v2.0
- Sistema de clasificación de 2 niveles (Concepto + Detalle)
- 37 reglas de nivel 1 + 24 patrones de refinamiento
- Cobertura del 99%+ de movimientos comunes
- Sistema de reglas externas en JSON (preparado para expansión)

### 🎨 Dashboard TORO
- Rediseño visual completo con paleta verde petróleo (#059669)
- Branding unificado "TORO · Resumen de Cuentas"
- Gráficos interactivos con Chart.js
- Responsive design mobile/desktop

### ⚙️ Arquitectura Mejorada
- **Configuración centralizada** (`src/config.py`)
- **Lógica pura testeable** (separada de CLI)
- **Suite de tests completa** (26 tests, 90% coverage en módulos core)
- **Sin rutas hardcodeadas** - portable entre sistemas

### 📦 Empaquetado Profesional
- Ejecutable standalone con PyInstaller
- Paquete distribuible listo para producción
- No requiere Python instalado
- INICIAR_TORO.bat para usuarios

---

## 🏗️ COMPONENTES DEL SISTEMA

### 1. Consolidador Multi-Banco ✓
- Detección automática por estructura de columnas
- Soporte Galicia y Supervielle
- Normalización de fechas y números
- Exportación consolidada a Excel

### 2. Categorizador Cascada v2.0 ✓
- Motor de 2 niveles (Concepto → Detalle)
- Categorización automática >95%
- Extracción de metadata (DEBIN, nombres, CUIT)
- CLI de corrección manual para casos especiales

### 3. Reportes y Analytics ✓
- Dashboard HTML interactivo con diseño TORO
- Análisis financiero completo (ingresos, egresos, flujo)
- Reporte Excel ejecutivo (5 hojas)
- Top prestadores y alertas automáticas
- Gráficos de flujo de caja diario

### 4. Orquestador CLI ✓
- Menú interactivo con rich
- Flujo completo automatizado
- Ejecución modular de componentes
- Configuración centralizada

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

2. **Verás un menú con 9 opciones:**
   - Opción 1: Ejecuta todo el proceso completo automáticamente
   - Opción 2: Consolidar TODOS los archivos de la carpeta input
   - Opción 3: **NUEVO** - Consolidar con SELECCIÓN de archivos específicos
   - Opción 4: Categorizar movimientos (usa automáticamente el archivo de la sesión)
   - Opción 5: Generar reportes y dashboard (usa automáticamente el archivo de la sesión)
   - Opción 6: Ver configuración
   - Opción 7: Ver información del sistema
   - Opción 8: **NUEVO** - Limpiar sesión de trabajo
   - Opción 0: Salir

3. **Selecciona la opción deseada** ingresando el número y presionando ENTER

4. **El sistema te guiará paso a paso** con mensajes claros

### Opción 2: Uso Manual con Comandos (avanzado)

Si prefieres usar comandos directos, continúa con la sección "Uso Mensual - Paso a Paso" más abajo.

---

## Sistema de Sesión de Trabajo (NUEVO)

El sistema ahora **recuerda** qué archivos estás procesando durante toda la sesión, permitiéndote trabajar con un flujo más natural **sin tener que borrar archivos** entre procesos.

### ¿Cómo funciona?

**Antes:** Tenías que borrar archivos de `input/` para procesar diferentes meses por separado.

**Ahora:** El sistema mantiene una **sesión de trabajo** que recuerda:
- Qué archivos consolidaste
- Qué archivo se generó al consolidar
- Qué archivo se generó al categorizar

### Flujo de Trabajo con Sesión

```
1. Opción 2 o 3: CONSOLIDAR
   ↓
   [SESION] Archivo listo para CATEGORIZAR

2. Opción 4: CATEGORIZAR
   ↓ (usa automáticamente el archivo consolidado)
   [SESION] Archivo listo para REPORTES

3. Opción 5: REPORTES
   ↓ (usa automáticamente el archivo categorizado)
   ✓ Dashboard y reportes generados
```

### Ventajas

- **No borras archivos**: Puedes tener extractos de varios meses en `input/`
- **Flujo natural**: Consolidar → Categorizar → Reportes sin especificar archivos
- **Visualización clara**: El banner muestra qué archivos estás procesando
- **Control total**: Opción 8 para limpiar sesión y empezar de nuevo

### Ejemplo de Uso

**Escenario:** Tienes extractos de octubre y noviembre. Quieres procesar noviembre solamente.

```
Paso 1: Opción 3 (Consolidar con selección)
  → Selecciono archivos de noviembre
  → [SESION] Archivo listo para CATEGORIZAR

Paso 2: Opción 4 (Categorizar)
  → Sistema usa automáticamente el archivo consolidado de noviembre
  → [SESION] Archivo listo para REPORTES

Paso 3: Opción 5 (Reportes)
  → Sistema usa automáticamente el archivo categorizado de noviembre
  → Dashboard de noviembre generado

Paso 4 (OPCIONAL): Opción 8 (Limpiar sesión)
  → Ahora puedo procesar octubre desde cero
```

### Banner con Información de Sesión

Cuando tienes una sesión activa, el banner te muestra:

```
================================================================================
Fecha y hora: 15/11/2025 14:30:00
================================================================================

[SESION ACTIVA]
  Archivos input: Extracto_Galicia_noviembre.xlsx, Extracto_Supervielle_noviembre.xlsx
  Consolidado: movimientos_consolidados_2025_11.xlsx
  Categorizado: movimientos_categorizados_2025_11.xlsx
================================================================================
```

---

## Selección de Archivos Específicos (NUEVO)

### ¿Cuándo usar esta opción?

- Cuando tienes varios archivos en la carpeta `input/` pero **solo quieres procesar algunos**
- Cuando quieres procesar archivos de diferentes meses por separado
- Cuando quieres excluir temporalmente ciertos archivos sin borrarlos

### Cómo usar la Opción 3: Consolidar con Selección

1. **Coloca todos tus archivos** en la carpeta `input/` (no importa cuántos sean)

2. **Ejecuta INICIAR.bat** y selecciona la **opción 3**

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
