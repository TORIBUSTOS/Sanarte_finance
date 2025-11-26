# GUÍA: Compilar SANARTE para Windows

Esta guía explica cómo generar un ejecutable `.exe` para Windows que otros puedan usar sin instalar Python.

---

## OPCIÓN 1: Compilar en Windows (Recomendado)

### Requisitos
- Windows 10/11 (64-bit)
- Python 3.8+ instalado

### Pasos

```powershell
# 1. Instalar dependencias
pip install -r requirements.txt
pip install pyinstaller

# 2. Generar ejecutable
python build_exe.py

# 3. Crear paquete de distribución
python preparar_paquete.py
```

### Resultado
- Ejecutable: `dist/SANARTE.exe` (~150-200 MB)
- Paquete completo: `paquete_distribucion/SANARTE_v1.3.zip`

---

## OPCIÓN 2: Cross-compilar desde Linux (Experimental)

⚠️ **NOTA:** PyInstaller no soporta oficialmente cross-compilation. El método más confiable es compilar en Windows.

### Alternativa con Wine (Avanzado)

```bash
# 1. Instalar Wine y dependencias
sudo apt-get install wine wine64 python3-wine

# 2. Descargar Python para Windows con Wine
# Instrucciones en: https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Win-from-Lin

# 3. Compilar con PyInstaller en Wine
wine python build_exe.py
```

### Alternativa con Máquina Virtual
1. Crear VM con Windows 10/11
2. Clonar repositorio en VM
3. Seguir pasos de "OPCIÓN 1"

---

## OPCIÓN 3: Compilar en Linux (Para Linux)

Ya compilado! Si ejecutaste `python build_exe.py` en Linux, el ejecutable generado funciona en Linux.

```bash
# 1. Instalar dependencias
pip install -r requirements.txt
pip install pyinstaller

# 2. Generar ejecutable
python build_exe.py

# 3. Crear paquete
python preparar_paquete.py

# 4. Ejecutar
./dist/SANARTE
```

### Resultado
- Ejecutable: `dist/SANARTE` (7 MB)
- Paquete: `paquete_distribucion/SANARTE_v1.3.zip`

---

## Estructura de Archivos del Proyecto

```
Sanarte_finance/
├── build_exe.py              ← Script para generar ejecutable
├── preparar_paquete.py       ← Script para crear paquete completo
├── sanarte.spec              ← Config de PyInstaller (alternativa)
├── menu_principal.py         ← Punto de entrada principal
├── requirements.txt          ← Dependencias Python
├── src/                      ← Código fuente
│   ├── main.py
│   ├── processors/
│   ├── readers/
│   ├── reports/
│   └── utils/
├── input/                    ← Carpeta para archivos Excel
├── output/                   ← Carpeta para reportes
├── data/                     ← Archivos de configuración/ejemplos
└── dist/                     ← Ejecutable generado
    └── SANARTE(.exe)
```

---

## Scripts Disponibles

### `build_exe.py`
Genera el ejecutable usando PyInstaller.

```bash
python build_exe.py
```

**Qué hace:**
- Limpia builds anteriores
- Configura PyInstaller con dependencias necesarias
- Genera ejecutable de un solo archivo
- Muestra tamaño y ubicación del resultado

### `preparar_paquete.py`
Crea paquete completo para distribución.

```bash
python preparar_paquete.py
```

**Qué hace:**
- Crea estructura de carpetas
- Copia ejecutable y documentación
- Incluye carpetas input/output
- Genera archivo ZIP para compartir
- Crea INICIO_RAPIDO.txt para usuarios

### `sanarte.spec` (Alternativa)
Archivo de configuración de PyInstaller.

```bash
pyinstaller sanarte.spec
```

Usa este método si prefieres más control sobre la configuración.

---

## Personalización

### Cambiar versión

Editar en `build_exe.py`:
```python
VERSION = "1.4"  # Cambiar aquí
```

Y en `preparar_paquete.py`:
```python
VERSION = "1.4"  # Cambiar aquí también
```

### Agregar ícono personalizado

1. Crear o conseguir archivo `.ico` (Windows) o `.png` (Linux/Mac)
2. Nombrar como `sanarte_icon.ico`
3. Colocar en raíz del proyecto
4. Ejecutar `python build_exe.py` (detecta el ícono automáticamente)

### Incluir archivos adicionales

Editar `build_exe.py`:
```python
comando.extend(['--add-data', 'archivo_extra.txt:./'])
```

---

## Solución de Problemas

### Error: "pandas not found"
```bash
pip install pandas openpyxl rich
```

### Error: "PyInstaller not found"
```bash
pip install pyinstaller
```

### Ejecutable muy grande (>500 MB)
Esto es normal. Incluye Python completo + bibliotecas.

Para reducir tamaño:
- Remover imports no usados del código
- Usar `--exclude-module` para módulos innecesarios

### Windows SmartScreen bloquea ejecutable
Normal con ejecutables sin firma digital.

**Solución para usuarios:**
1. Clic en "Más información"
2. Clic en "Ejecutar de todas formas"

**Solución permanente (opcional):**
- Comprar certificado de firma de código (~$200/año)
- Usar `signtool.exe` para firmar el `.exe`

### Antivirus marca como virus
Falso positivo común con PyInstaller.

**Solución:**
1. Subir a VirusTotal para verificar
2. Reportar falso positivo al antivirus
3. Agregar excepción temporal

---

## Distribución del Paquete

### Método 1: ZIP (Simple)
```bash
python preparar_paquete.py
# Enviar: paquete_distribucion/SANARTE_v1.3.zip
```

### Método 2: Instalador (Profesional)
Requiere [Inno Setup](https://jrsoftware.org/isdl.php) (Windows)

Ver `INSTRUCCIONES_DISTRIBUCION.md` para detalles.

### Método 3: Repositorio
```bash
# En GitHub Releases
git tag v1.3
git push origin v1.3
# Subir SANARTE_v1.3.zip como release asset
```

---

## Compatibilidad

| Sistema Operativo | Compilar en | Ejecutar en |
|-------------------|-------------|-------------|
| **Windows** | Windows | Windows 10/11 (64-bit) |
| **Linux** | Linux | Ubuntu/Debian/Fedora (64-bit) |
| **macOS** | macOS | macOS 10.13+ (64-bit) |

⚠️ **IMPORTANTE:** Debes compilar en el mismo SO donde se ejecutará.

---

## Recursos Adicionales

- [PyInstaller Docs](https://pyinstaller.org/)
- [PyInstaller GitHub](https://github.com/pyinstaller/pyinstaller)
- [Inno Setup](https://jrsoftware.org/isinfo.php) (para instaladores Windows)
- [NSIS](https://nsis.sourceforge.io/) (alternativa a Inno Setup)

---

## Licencia y Distribución

Este proyecto está bajo licencia [especificar licencia].

Para distribuir:
- ✅ Incluir archivo LEEME.txt con instrucciones
- ✅ Mantener créditos originales
- ✅ No modificar ejecutable sin permiso
- ✅ Reportar bugs y sugerencias

---

## Contacto

GitHub: https://github.com/TORIBUSTOS/Sanarte_finance

---

**Última actualización:** 2025-11-26
