# GUÍA: DISTRIBUIR SANARTE COMO EJECUTABLE

Esta guía explica cómo convertir SANARTE a un ejecutable (.exe) para distribuir a usuarios sin conocimientos técnicos.

---

## MÉTODO 1: EJECUTABLE SIMPLE (RECOMENDADO)

### Paso 1: Generar el .exe

En tu PC de desarrollo:

```powershell
# Instalar PyInstaller (solo la primera vez)
pip install pyinstaller

# Generar ejecutable
python build_exe.py
```

**Resultado:** Archivo `dist/SANARTE.exe` (~100-200 MB)

### Paso 2: Preparar carpeta de distribución

Crear carpeta con esta estructura:

```
SANARTE_v1.3/
├── SANARTE.exe          ← Ejecutable generado
├── input/               ← Carpeta vacía (para archivos Excel)
├── output/              ← Carpeta vacía (para reportes)
└── LEEME.txt           ← Instrucciones de uso
```

### Paso 3: Distribuir

**Opción A: Comprimir en ZIP**
```powershell
Compress-Archive -Path SANARTE_v1.3 -DestinationPath SANARTE_v1.3.zip
```

Enviar `SANARTE_v1.3.zip` por email/Drive/etc.

**Opción B: Pendrive**
Copiar carpeta `SANARTE_v1.3` directamente

---

## MÉTODO 2: INSTALADOR PROFESIONAL (AVANZADO)

### Requisitos adicionales:
- Inno Setup (descarga: https://jrsoftware.org/isdl.php)

### Paso 1: Generar .exe con PyInstaller

```powershell
pyinstaller sanarte.spec
```

### Paso 2: Crear script de instalación

Archivo `sanarte_installer.iss`:

```iss
[Setup]
AppName=SANARTE Control Financiero
AppVersion=1.3
DefaultDirName={autopf}\SANARTE
DefaultGroupName=SANARTE
OutputDir=installers
OutputBaseFilename=SANARTE_Setup_v1.3
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\SANARTE.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "input\*"; DestDir: "{app}\input"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "output\*"; DestDir: "{app}\output"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\SANARTE"; Filename: "{app}\SANARTE.exe"
Name: "{autodesktop}\SANARTE"; Filename: "{app}\SANARTE.exe"

[Run]
Filename: "{app}\SANARTE.exe"; Description: "Ejecutar SANARTE"; Flags: postinstall nowait skipifsilent
```

### Paso 3: Compilar instalador

1. Abrir Inno Setup
2. Abrir `sanarte_installer.iss`
3. Build → Compile
4. Resultado: `installers/SANARTE_Setup_v1.3.exe`

---

## INSTRUCCIONES PARA USUARIOS FINALES

### Método Simple (ZIP):

1. Extraer `SANARTE_v1.3.zip`
2. Entrar a carpeta `SANARTE_v1.3`
3. Doble clic en `SANARTE.exe`
4. Listo!

### Método Instalador:

1. Ejecutar `SANARTE_Setup_v1.3.exe`
2. Siguiente → Siguiente → Instalar
3. Buscar icono "SANARTE" en escritorio o menú inicio
4. Listo!

---

## USO DEL PROGRAMA

1. Copiar extracto bancario (.xlsx) a carpeta `input/`
2. Ejecutar `SANARTE.exe`
3. Elegir opción 1
4. Seleccionar archivo
5. Esperar proceso (1-5 min)
6. Revisar reportes en carpeta `output/`

---

## SOLUCIÓN DE PROBLEMAS

### "Windows protegió tu PC"
**Causa:** Windows SmartScreen bloquea ejecutables desconocidos

**Solución:**
1. Clic en "Más información"
2. Clic en "Ejecutar de todas formas"

### "El antivirus bloqueó SANARTE.exe"
**Causa:** Falso positivo común en ejecutables Python

**Solución:**
1. Agregar excepción en antivirus
2. O usar método ZIP en lugar de instalador

### "No se puede escribir en output/"
**Causa:** Permisos de carpeta

**Solución:**
1. Clic derecho en carpeta SANARTE
2. Propiedades → Seguridad
3. Dar permisos de escritura

---

## NOTAS TÉCNICAS

### Tamaño del ejecutable
- **Un archivo:** ~150-200 MB (incluye Python + pandas + openpyxl)
- **Con carpeta:** ~100 MB exe + ~50 MB dependencias

### Compatibilidad
- ✅ Windows 10/11 (64-bit)
- ✅ No requiere Python instalado
- ✅ No requiere instalación de dependencias
- ⚠️ Solo Windows (para Mac/Linux usar método original Python)

### Actualizar versión
1. Modificar código en PC desarrollo
2. Regenerar .exe con `python build_exe.py`
3. Redistribuir nueva versión

---

## ALTERNATIVAS

### Si PyInstaller no funciona:

**cx_Freeze:**
```powershell
pip install cx_Freeze
cxfreeze menu_principal.py --target-dir dist
```

**Nuitka (más rápido):**
```powershell
pip install nuitka
python -m nuitka --onefile --windows-disable-console menu_principal.py
```

---

## CONTACTO

Para soporte técnico o reportar problemas:
- GitHub Issues: https://github.com/TORIBUSTOS/Sanarte_finance/issues
- Email: [tu email aquí]
