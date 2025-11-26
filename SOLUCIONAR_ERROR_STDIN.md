# 🔧 SOLUCIÓN: Error "lost sys.stdin" en SANARTE.exe

Este error ocurre cuando PyInstaller compila en modo `--onefile` y la librería `rich.Prompt` intenta leer del teclado. Es un problema conocido de compatibilidad.

---

## ✅ SOLUCIÓN RECOMENDADA: Compilar en Modo Carpeta

El modo carpeta (`--onedir`) es **más estable** y **no tiene problemas con stdin**.

### 📋 **Pasos en Windows (PowerShell):**

```powershell
# 1. Navegar a la carpeta del proyecto
cd C:\Users\mauri\OneDrive\Escritorio\CLAUDE\sanarte_financiero

# 2. Traer últimas actualizaciones de GitHub
git pull origin claude/package-system-executable-01TwMLej6hryb631LkpsKvpA

# 3. Generar ejecutable en MODO CARPETA (sin problemas de stdin)
python build_exe_carpeta.py

# 4. Crear paquete de distribución
python preparar_paquete.py
```

---

## 📦 **Resultado**

Después de ejecutar `build_exe_carpeta.py`:

```
📁 dist/SANARTE/
   ├── SANARTE.exe          ← Ejecutable principal
   ├── python313.dll
   ├── base_library.zip
   └── [otras dependencias...]
```

**Diferencias con el método anterior:**

| Característica | Archivo Único (--onefile) | Carpeta (--onedir) |
|----------------|---------------------------|---------------------|
| **Archivos** | 1 solo .exe | Carpeta con varios archivos |
| **Tamaño** | 33 MB | ~80-100 MB total |
| **Velocidad** | Más lento (descomprime al iniciar) | ⚡ Más rápido |
| **Estabilidad stdin** | ❌ Problemas | ✅ Sin problemas |
| **Distribución** | Más fácil (1 archivo) | Hay que comprimir carpeta |

---

## 🎯 **Cómo Distribuir el Modo Carpeta**

### Opción A: Comprimir manualmente

```powershell
# En PowerShell, navega a dist/
cd dist

# Comprime la carpeta SANARTE
Compress-Archive -Path SANARTE -DestinationPath SANARTE_v1.3.zip
```

### Opción B: Usar el script preparar_paquete.py

El script `preparar_paquete.py` detecta automáticamente si usaste modo carpeta y ajusta el paquete.

```powershell
python preparar_paquete.py
```

---

## 👥 **Instrucciones para Usuarios Finales**

Cuando reciban `SANARTE_v1.3.zip`:

```
1. Extraer el ZIP
2. Entrar a la carpeta SANARTE_v1.3/
3. Doble clic en SANARTE.exe
4. ✅ Listo! (sin errores de stdin)
```

⚠️ **IMPORTANTE:** El usuario debe mantener todos los archivos de la carpeta juntos. No puede mover solo el .exe.

---

## 🔀 **Alternativa: Archivo .bat de Inicio**

Si prefieres seguir usando el ejecutable de archivo único, usa el launcher .bat:

```powershell
# 1. Traer el archivo .bat actualizado
git pull origin claude/package-system-executable-01TwMLej6hryb631LkpsKvpA

# 2. Distribuir junto con SANARTE.exe:
dist/
├── SANARTE.exe
└── INICIAR_SANARTE.bat    ← Usar este para ejecutar
```

**Instrucciones para usuarios:**
- Doble clic en `INICIAR_SANARTE.bat` en lugar de `SANARTE.exe`

---

## 📊 **Comparación de Soluciones**

| Solución | Ventajas | Desventajas |
|----------|----------|-------------|
| **Modo Carpeta** | ✅ Sin problemas stdin<br>✅ Más rápido<br>✅ Más estable | ⚠️ Más archivos (carpeta completa) |
| **Archivo .bat** | ✅ Solo 2 archivos | ⚠️ Puede no funcionar en todos los casos |
| **Archivo único** | ✅ 1 solo .exe | ❌ Problemas con stdin |

---

## 🛠️ **Comandos Completos (Copia y Pega)**

```powershell
# SOLUCIÓN COMPLETA - Ejecuta estos comandos en orden:

cd C:\Users\mauri\OneDrive\Escritorio\CLAUDE\sanarte_financiero
git pull origin claude/package-system-executable-01TwMLej6hryb631LkpsKvpA
python build_exe_carpeta.py
python preparar_paquete.py
explorer paquete_distribucion
```

---

## ❓ **FAQ - Preguntas Frecuentes**

### ¿Por qué ocurre este error?
PyInstaller empaqueta todo en un archivo temporal que se descomprime al ejecutar, perdiendo control de `sys.stdin` que necesita `rich.Prompt`.

### ¿El modo carpeta es mejor?
Sí, para este tipo de aplicaciones. Es más rápido, más estable y sin problemas de I/O.

### ¿Puedo volver al archivo único?
Sí, pero tendrías que modificar el código de `menu_principal.py` para usar `input()` nativo en lugar de `rich.Prompt`.

### ¿Cuánto pesa el modo carpeta?
La carpeta completa pesa ~80-100 MB, pero comprimida en ZIP queda en ~35-40 MB.

---

## 📞 **Soporte**

Si sigues teniendo problemas:
1. Verifica que usaste `build_exe_carpeta.py` (no `build_exe.py`)
2. Asegúrate de distribuir TODA la carpeta (no solo el .exe)
3. Revisa que no haya antivirus bloqueando archivos

---

**Última actualización:** 2025-11-26
