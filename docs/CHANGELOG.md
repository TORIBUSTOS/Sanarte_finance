# Changelog

Todos los cambios importantes de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

---

## [2.0.0] - 2025-11-29

### 🚀 Release de Producción

Versión 2.0.0 marca un hito importante en el proyecto con mejoras sustanciales en calidad de código, arquitectura y experiencia de usuario.

### ✨ Agregado

#### Motor de Clasificación v2.0
- **ClasificadorCascada v2.0**: Sistema de clasificación de 2 niveles (Concepto + Detalle)
- 37 reglas de nivel 1 para categorización inicial
- 24 patrones de refinamiento para categorización detallada
- Cobertura del 99%+ de movimientos bancarios comunes
- Sistema de reglas externas en formato JSON (preparado para futuras expansiones)
- Documentación completa del motor de clasificación

#### Arquitectura y Testing
- **Configuración centralizada** en `src/config.py` (PathsConfig, ClasificadorConfig, SystemConfig)
- **Suite de tests completa** con pytest (26 tests)
- Cobertura de código del 90% en módulos core
- Tests unitarios para Normalizer, Categorizer, Analyzer
- Función pura `categorizar_movimientos_df()` testeable sin efectos secundarios
- Sistema de tests automatizados en CI/CD ready

#### Dashboard y Diseño
- **Rediseño visual completo** del dashboard HTML
- Branding unificado "TORO · Resumen de Cuentas"
- Nueva paleta de colores verde petróleo (#059669, #047857, #0ea5e9, #10b981)
- Gradientes modernos en header y body
- 10 cards actualizadas con colores TORO
- Gráficos Chart.js con colores TORO (ingresos, egresos, flujo)
- Diseño responsive mobile/desktop

#### Desarrollo y Documentación
- `requirements-dev.txt` para dependencias de desarrollo
- Test de integración end-to-end (`test_integration.py`)
- Documentación actualizada en README.md
- CHANGELOG.md para versionado semántico
- Badges de versión, tests y coverage en README
- Actualización de TORO.spec para excluir tests del paquete

### 🔧 Cambiado

- **Rebranding completo**: SANARTE → TORO en todo el sistema
- Versión actualizada de 1.3 a 2.0.0 en:
  - `src/config.py`
  - `preparar_paquete.py`
  - README.md y documentación
- Rutas hardcodeadas eliminadas, ahora usa config centralizada
- Lógica de negocio separada de CLI para mejor testabilidad
- Motor de clasificación mejorado de 24 reglas a 61 (37+24)
- Estructura de carpetas reorganizada (manuales/ separado)

### 🐛 Corregido

- **Bug crítico**: JSON serialization error en `dashboard_generator.py`
  - Problema: `int64` y `float64` de pandas no serializaban a JSON
  - Solución: Conversión explícita a tipos nativos Python (`int()`, `float()`)
  - Archivo: `src/reports/dashboard_generator.py:846-849`
- Importaciones mejoradas en módulos
- Manejo de errores en consolidador y categorizador
- Docstrings actualizadas y completas

### 📦 Empaquetado

- TORO.spec actualizado con excludes para tests
- preparar_paquete.py versión 2.0.0
- INICIAR_TORO.bat mejorado
- Paquete distribuible optimizado

### 🧪 Testing

```
============================= test session starts ==============================
platform linux -- Python 3.11.14, pytest-9.0.1
collected 26 items

tests/test_analyzer.py ........              [ 30%]
tests/test_categorizer.py ..........          [ 69%]
tests/test_normalizer.py ........             [100%]

============================== 26 passed in 1.39s ===============================

Coverage:
- clasificador_cascada.py: 90%
- analyzer.py: 81%
- normalizer.py: 76%
- categorizer.py: 66%
```

### 📈 Métricas de Calidad

- **Tests**: 26/26 passing (100%)
- **Coverage (core)**: 90% en módulos críticos
- **Clasificación**: >95% de movimientos categorizados automáticamente
- **Líneas de código**: ~1400 (sin contar tests)
- **Documentación**: 100% de módulos documentados

---

## [1.3] - 2025-11-26

### Agregado
- Sistema de empaquetado con PyInstaller
- Rebranding inicial SANARTE → TORO
- Scripts de preparación de paquete distribuible
- Soluciones documentadas para error stdin en ejecutables
- INICIAR_TORO.bat para Windows

### Cambiado
- Estructura reorganizada con carpeta manuales/
- Documentación mejorada

---

## [1.2] - 2025-11 (anterior)

### Agregado
- Motor de clasificación con 24 reglas
- Dashboard HTML interactivo
- Reporte Excel con 5 hojas
- CLI interactivo con menú principal
- Soporte multi-banco (Galicia, Supervielle)

### Características
- Consolidación de extractos bancarios
- Categorización automática
- Análisis financiero
- Generación de reportes

---

## Formato de Versiones

- **MAJOR** (2.x.x): Cambios incompatibles en API/arquitectura
- **MINOR** (x.2.x): Nuevas funcionalidades compatibles
- **PATCH** (x.x.2): Correcciones de bugs

---

## Enlaces

- [Repositorio](https://github.com/TORIBUSTOS/Sanarte_finance)
- [Issues](https://github.com/TORIBUSTOS/Sanarte_finance/issues)
- [Documentación](README.md)
