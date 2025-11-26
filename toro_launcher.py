"""
Launcher para TORO - Maneja problemas de stdin con PyInstaller
Este archivo soluciona el problema de "lost sys.stdin" en ejecutables
"""
import sys
import os

# Fijar sys.stdin, sys.stdout y sys.stderr para PyInstaller
if getattr(sys, 'frozen', False):
    # Estamos en un ejecutable de PyInstaller
    import io

    # Si stdin no está disponible, crear uno dummy
    if sys.stdin is None or not hasattr(sys.stdin, 'read'):
        sys.stdin = io.StringIO()

    # Asegurar que stdout y stderr también estén disponibles
    if sys.stdout is None:
        sys.stdout = io.StringIO()
    if sys.stderr is None:
        sys.stderr = io.StringIO()

# Ahora importar y ejecutar el programa principal
if __name__ == "__main__":
    # Importar el menú principal
    import menu_principal

    # Ejecutar el programa
    try:
        menu_principal.main()
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
        sys.exit(1)
