"""
Parche para entrada de usuario compatible con PyInstaller
Este módulo reemplaza rich.Prompt con input() nativo cuando sea necesario
"""
import sys

def safe_input(prompt_text, default=None):
    """
    Input seguro que funciona tanto en modo normal como en ejecutable PyInstaller.

    Args:
        prompt_text: Texto del prompt
        default: Valor por defecto

    Returns:
        str: Input del usuario
    """
    try:
        # Intentar usar rich.Prompt primero
        from rich.console import Console
        from rich.prompt import Prompt

        console = Console()

        # Si estamos en PyInstaller y hay problemas con stdin, usar input() nativo
        if getattr(sys, 'frozen', False):
            # Estamos en ejecutable PyInstaller
            if default:
                print(f"{prompt_text} [{default}]: ", end="", flush=True)
            else:
                print(f"{prompt_text}: ", end="", flush=True)

            respuesta = input().strip()
            return respuesta if respuesta else (default or "")
        else:
            # Modo normal, usar rich.Prompt
            return Prompt.ask(prompt_text, default=default)

    except Exception:
        # Fallback a input() nativo si rich falla
        if default:
            print(f"{prompt_text} [{default}]: ", end="", flush=True)
        else:
            print(f"{prompt_text}: ", end="", flush=True)

        respuesta = input().strip()
        return respuesta if respuesta else (default or "")


def safe_confirm(prompt_text, default=True):
    """
    Confirmación segura que funciona en ejecutables PyInstaller.

    Args:
        prompt_text: Texto del prompt
        default: Valor por defecto (True/False)

    Returns:
        bool: True si confirma, False si no
    """
    try:
        from rich.prompt import Confirm

        if getattr(sys, 'frozen', False):
            # Estamos en ejecutable
            default_text = "S/n" if default else "s/N"
            print(f"{prompt_text} ({default_text}): ", end="", flush=True)
            respuesta = input().strip().lower()

            if not respuesta:
                return default
            return respuesta in ['s', 'si', 'sí', 'y', 'yes']
        else:
            return Confirm.ask(prompt_text, default=default)

    except Exception:
        default_text = "S/n" if default else "s/N"
        print(f"{prompt_text} ({default_text}): ", end="", flush=True)
        respuesta = input().strip().lower()

        if not respuesta:
            return default
        return respuesta in ['s', 'si', 'sí', 'y', 'yes']
