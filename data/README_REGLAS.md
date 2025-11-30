# 📚 Guía de Reglas de Clasificación - TORO

Sistema de reglas externas para el motor de clasificación **ClasificadorCascada v2.0**.

---

## 📂 Archivos de Reglas

### 1. `reglas_concepto.json` - Nivel 1 (Base)

**Propósito:** Clasificación inicial basada en el campo **"Concepto"** del movimiento bancario.

**Estructura de una regla:**

```json
{
  "id": "ING-001",
  "patron": "crédito por transferencia",
  "tipo_match": "exacto",
  "categoria": "Ingresos - Transferencias",
  "prioridad": 1,
  "activo": true,
  "notas": "Transferencias recibidas"
}
```

**Campos:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | string | Identificador único (formato: `TIPO-NNN`) |
| `patron` | string | Texto a buscar en el campo "Concepto" (en minúsculas) |
| `tipo_match` | string | Tipo de coincidencia: `"exacto"`, `"contiene"`, `"comienza"`, `"termina"` |
| `categoria` | string | Categoría completa (formato: `"Grupo - Subgrupo"`) |
| `prioridad` | int | 1=alta, 2=media, 3=baja (evalúa primero las de mayor prioridad) |
| `activo` | bool | `true` para usar la regla, `false` para desactivarla |
| `notas` | string | Comentario descriptivo |

**Convenciones de ID:**
- `ING-XXX`: Ingresos
- `EGR-XXX`: Egresos
- `IMP-XXX`: Impuestos
- `SRV-XXX`: Servicios
- `GAS-XXX`: Gastos Operativos
- `COM-XXX`: Comisiones Bancarias

---

### 2. `reglas_refinamiento.json` - Nivel 2 (Refinamiento)

**Propósito:** Refinar categorías genéricas del Nivel 1 usando el campo **"Detalle"**.

**Estructura:**

```json
{
  "reglas_refinamiento": {
    "Gastos Operativos - Compras": {
      "descripcion": "Refina compras genéricas según el detalle",
      "patrones": [
        {
          "id": "REF-GAS-001",
          "palabras_clave": ["aguas cordobesas", "aguascordobesas"],
          "categoria_refinada": "Servicios - Agua",
          "activo": true,
          "notas": "Servicio de agua potable"
        }
      ],
      "categoria_default": "Gastos Operativos - Compras Varias"
    }
  }
}
```

**Campos:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| Clave raíz | string | Categoría base a refinar (del Nivel 1) |
| `descripcion` | string | Descripción de qué refina esta categoría |
| `patrones` | array | Lista de patrones de refinamiento |
| `categoria_default` | string | Categoría si no coincide ningún patrón |

**Estructura de un patrón:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | string | Identificador único (formato: `REF-XXX-NNN`) |
| `palabras_clave` | array | Lista de strings a buscar en "Detalle" |
| `categoria_refinada` | string | Categoría refinada si coincide |
| `activo` | bool | `true` para usar, `false` para desactivar |
| `notas` | string | Comentario descriptivo |

---

## 🔧 Cómo Funciona el Sistema

### Flujo de Clasificación (Cascada de 2 Niveles):

```
1. NIVEL 1 - Concepto
   ├─ Leer campo "Concepto" del movimiento
   ├─ Buscar en reglas_concepto.json
   ├─ Aplicar regla que coincida (según tipo_match y prioridad)
   └─ Resultado: Categoría BASE (ej: "Gastos Operativos - Compras")

2. NIVEL 2 - Refinamiento (opcional)
   ├─ ¿La categoría base es refinable?
   │  └─ Buscar en reglas_refinamiento.json
   ├─ Si SÍ: Leer campo "Detalle" del movimiento
   │  ├─ Buscar coincidencias en palabras_clave
   │  └─ Aplicar categoria_refinada si coincide
   ├─ Si NO: Mantener categoría base
   └─ Resultado: Categoría FINAL (ej: "Servicios - Agua")
```

---

## 📝 Ejemplos Prácticos

### Ejemplo 1: Clasificación Simple (Solo Nivel 1)

**Movimiento:**
- Concepto: `"IMPUESTO DÉBITOS Y CRÉDITOS/DB"`
- Detalle: `""`

**Proceso:**
1. Nivel 1: Coincide con patrón `"impuesto débitos y créditos/db"`
2. Categoría BASE: `"Impuestos - Débitos y Créditos"`
3. Nivel 2: No refinable
4. **Resultado:** `"Impuestos - Débitos y Créditos"`

---

### Ejemplo 2: Clasificación con Refinamiento (Nivel 1 + 2)

**Movimiento:**
- Concepto: `"COMPRA VISA DÉBITO"`
- Detalle: `"EPEC CÓRDOBA - PAGO SERVICIO ELÉCTRICO"`

**Proceso:**
1. Nivel 1: Coincide con patrón `"compra visa débito"`
2. Categoría BASE: `"Gastos Operativos - Compras"`
3. Nivel 2: Categoría refinable → Buscar en Detalle
   - Coincide palabra clave: `"epec"`
4. Categoría REFINADA: `"Servicios - Electricidad"`
5. **Resultado:** `"Servicios - Electricidad"`

---

## ➕ Cómo Agregar Nuevas Reglas

### Agregar regla de Nivel 1 (Concepto):

1. Abrir `data/reglas_concepto.json`
2. Agregar al array `"reglas"`:

```json
{
  "id": "ING-050",
  "patron": "nuevo tipo de ingreso",
  "tipo_match": "contiene",
  "categoria": "Ingresos - Nuevos",
  "prioridad": 2,
  "activo": true,
  "notas": "Descripción del nuevo tipo"
}
```

3. Guardar archivo
4. Reiniciar el sistema TORO

---

### Agregar patrón de refinamiento (Nivel 2):

1. Abrir `data/reglas_refinamiento.json`
2. Buscar la categoría base a refinar
3. Agregar al array `"patrones"`:

```json
{
  "id": "REF-GAS-999",
  "palabras_clave": ["nuevo servicio", "servicio xyz"],
  "categoria_refinada": "Servicios - Nuevo",
  "activo": true,
  "notas": "Nuevo servicio agregado"
}
```

4. Guardar archivo
5. Reiniciar el sistema TORO

---

## ⚙️ Uso Programático

### Cargar reglas desde código:

```python
from processors.reglas_loader import cargar_reglas_desde_json

# Cargar todas las reglas
reglas_concepto, reglas_refinamiento = cargar_reglas_desde_json()

# Usar en ClasificadorCascada
clasificador = ClasificadorCascada()
clasificador.reglas_concepto = reglas_concepto
clasificador.reglas_refinamiento = reglas_refinamiento
```

---

## 🔍 Validación

Para verificar que los archivos JSON son válidos:

```python
from processors.reglas_loader import ReglasLoader

loader = ReglasLoader()
valido, errores = loader.validar_archivos()

if not valido:
    for error in errores:
        print(f"ERROR: {error}")
```

---

## 📌 Notas Importantes

1. **Case-insensitive:** Todos los patrones se buscan sin distinguir mayúsculas/minúsculas
2. **Prioridad:** Las reglas con prioridad=1 se evalúan antes que las de prioridad=2
3. **Activo/Inactivo:** Usa `"activo": false` para desactivar temporalmente una regla sin borrarla
4. **IDs únicos:** Cada regla debe tener un ID único para trazabilidad
5. **Backup:** Haz backup de estos archivos antes de modificaciones masivas

---

## 🐂 Sistema TORO · Resumen de Cuentas

Versión de reglas: **2.0**
Motor: **ClasificadorCascada**
Fecha: **2025-11-27**
