"""
TORO - Sistema de Resumen de Cuenta
Menú Principal CLI Interactivo - Bloque 4

Autor: Sistema TORO
Versión: 1.3 - Bloque 4: Orquestador Completo
"""
import os
import sys
from datetime import datetime

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Cambiar al directorio del script para rutas relativas
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from main import consolidar_bancos, categorizar_movimientos, generar_reportes
from glob import glob

# Rich imports para interfaz mejorada
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.prompt import Prompt, Confirm

console = Console()


def seleccionar_archivo_input():
    """
    Muestra archivos disponibles en input/ y permite al usuario seleccionar uno.

    Returns:
        str: Nombre del archivo seleccionado o None si no hay archivos o se cancela
    """
    archivos = glob(os.path.join('./input', '*.xlsx'))

    if not archivos:
        console.print("\n[bold red]❌ ERROR:[/bold red] No hay archivos Excel (.xlsx) en la carpeta './input'")
        console.print("[yellow]Por favor, coloca los extractos bancarios en esa carpeta.[/yellow]")
        return None

    # Crear tabla con rich
    tabla = Table(title="📁 Archivos Disponibles", box=box.ROUNDED, title_style="bold cyan")
    tabla.add_column("#", style="cyan", justify="center", width=5)
    tabla.add_column("Nombre del Archivo", style="white")
    tabla.add_column("Tamaño", justify="right", style="green")

    for i, archivo in enumerate(archivos, 1):
        nombre = os.path.basename(archivo)
        tamaño = os.path.getsize(archivo) / 1024  # KB
        tabla.add_row(str(i), nombre, f"{tamaño:.1f} KB")

    tabla.add_row("0", "[italic]Cancelar[/italic]", "", style="dim")

    console.print()
    console.print(tabla)
    console.print()

    while True:
        try:
            opcion = Prompt.ask(
                "[bold cyan]Selecciona el número del archivo[/bold cyan]",
                default="1"
            ).strip()

            if opcion == '0':
                console.print("[yellow]Operación cancelada.[/yellow]")
                return None

            idx = int(opcion) - 1
            if 0 <= idx < len(archivos):
                archivo_seleccionado = os.path.basename(archivos[idx])
                console.print(f"\n[bold green]✅ Archivo seleccionado:[/bold green] {archivo_seleccionado}")
                return archivo_seleccionado
            else:
                console.print(f"[bold red]❌ Opción inválida.[/bold red] Selecciona un número entre 1 y {len(archivos)}")

        except ValueError:
            console.print("[bold red]❌ Por favor ingresa un número válido.[/bold red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Operación cancelada.[/yellow]")
            return None


def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_banner():
    """Muestra el banner principal del sistema."""
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # ASCII art del toro (versión compacta)
    toro_art = """
                          .:*%*-.
                         .*@+.      .::.
                         *@%.        .#*.
                         #@@+.        .%#.
                         =@@@%=:....   :%@:
                         .=%@@@@@%%%##%%@@%.
                           .*%@@@@@@@@@@@@@@%%##:
                        ..*@@@@@@@@@@@@@@@@@@@@@#+.
                      .-#@@@@@@@@@@@@@@@@@@@@@@@@+.
             ..         .-%@@@@@@@@@@@@@@@@%%#%%@@%.
             .:.       .+@@@@@@@@@@@@@@@%+:.    ..
              +-.     .-%@@@@@@@@@@@@@@:-%@*..
              .*=.    .*@@@@@@@@@@@@@@=*@@@@@@%*:.
               .+@-. .@@@@@@@@@@@@@@@@@@@@@@@@@%#+=:
                 :##-.%@@@@@@@@@@@@@@@@@@@@@@@@%%*+
                  .=%%@@@@@@@@@@@@@@@@@@@@@@@@@%%#
                    .=%@@@@@@@@@@@@@@@@@@@@@@@@@%
                      .-*%@@@@@@@@@@@@@@@@@@@@%*:.
                          .:=*%%%%%%%%%%*=.
"""

    banner_text = Text()
    banner_text.append(toro_art, style="bold cyan")
    banner_text.append("\n")
    banner_text.append("                    🏦 TORO ", style="bold cyan")
    banner_text.append("- Resumen de Cuenta\n", style="bold white")
    banner_text.append("                    💰 Sistema Integrado v1.3\n", style="bold green")
    banner_text.append(f"                    📅 {fecha_hora}", style="dim")

    panel = Panel(
        banner_text,
        box=box.DOUBLE,
        border_style="cyan",
        padding=(1, 2)
    )

    console.print()
    console.print(panel)


def mostrar_menu_principal():
    """Muestra el menú principal."""
    menu = Table(show_header=False, box=box.ROUNDED, border_style="cyan", padding=(0, 2))
    menu.add_column("Opción", style="bold cyan", width=8)
    menu.add_column("Descripción", style="white")

    menu.add_row("1", "🔄 PROCESO COMPLETO (Consolidar → Categorizar → Reportes)")
    menu.add_row("", "")
    menu.add_row("2", "📥 Solo CONSOLIDAR extractos bancarios")
    menu.add_row("3", "🏷️  Solo CATEGORIZAR movimientos")
    menu.add_row("4", "📊 Solo generar REPORTES y Dashboard")
    menu.add_row("", "")
    menu.add_row("5", "⚙️  Configuración de rutas")
    menu.add_row("6", "ℹ️  Información del sistema")
    menu.add_row("", "")
    menu.add_row("0", "🚪 SALIR", style="dim")

    panel = Panel(
        menu,
        title="[bold white]MENÚ PRINCIPAL[/bold white]",
        border_style="cyan",
        box=box.DOUBLE
    )

    console.print()
    console.print(panel)
    console.print()


def proceso_completo():
    """Ejecuta el proceso completo: consolidar -> categorizar -> reportes."""
    console.print()
    console.print(Panel(
        "[bold white]Este proceso ejecutará los 3 bloques en secuencia:[/bold white]\n\n"
        "  [cyan]1.[/cyan] Consolidar extractos bancarios\n"
        "  [cyan]2.[/cyan] Categorizar movimientos\n"
        "  [cyan]3.[/cyan] Generar reportes y dashboard",
        title="[bold green]🔄 INICIANDO PROCESO COMPLETO[/bold green]",
        border_style="green",
        box=box.ROUNDED
    ))
    console.print()

    # Seleccionar archivo de input
    archivo_input = seleccionar_archivo_input()
    if archivo_input is None:
        Prompt.ask("\n[dim]Presiona ENTER para continuar[/dim]")
        return

    # PASO 1: Consolidar
    console.print()
    console.print(Panel(
        "[bold cyan]PASO 1/3: CONSOLIDANDO EXTRACTOS BANCARIOS[/bold cyan]",
        border_style="cyan",
        box=box.HEAVY
    ))

    resultado = consolidar_bancos(archivo_especifico=archivo_input)
    if resultado is None:
        console.print("\n[bold red]❌ Error en consolidación. Proceso detenido.[/bold red]")
        Prompt.ask("\n[dim]Presiona ENTER para continuar[/dim]")
        return

    df_consolidado, archivo_consolidado = resultado

    console.print("\n[bold green]✅ Consolidación completada.[/bold green]")
    Prompt.ask("[dim]Presiona ENTER para continuar[/dim]")

    # PASO 2: Categorizar
    console.print()
    console.print(Panel(
        "[bold cyan]PASO 2/3: CATEGORIZANDO MOVIMIENTOS[/bold cyan]",
        border_style="cyan",
        box=box.HEAVY
    ))

    resultado = categorizar_movimientos(
        ruta_archivo_consolidado=archivo_consolidado,
        revisar_manual=True
    )

    if resultado is None:
        console.print("\n[bold red]❌ Error en categorización. Proceso detenido.[/bold red]")
        Prompt.ask("\n[dim]Presiona ENTER para continuar[/dim]")
        return

    df_categorizado, archivo_categorizado = resultado

    console.print("\n[bold green]✅ Categorización completada.[/bold green]")
    Prompt.ask("[dim]Presiona ENTER para continuar[/dim]")

    # PASO 3: Reportes
    console.print()
    console.print(Panel(
        "[bold cyan]PASO 3/3: GENERANDO REPORTES Y DASHBOARD[/bold cyan]",
        border_style="cyan",
        box=box.HEAVY
    ))

    resultado = generar_reportes(
        ruta_archivo_categorizado=archivo_categorizado,
        abrir_dashboard=True
    )

    if resultado is None:
        console.print("\n[bold red]❌ Error en generación de reportes.[/bold red]")
        Prompt.ask("\n[dim]Presiona ENTER para continuar[/dim]")
        return

    # Proceso completo exitoso
    console.print()
    console.print(Panel(
        f"[bold white]Archivos generados en la carpeta 'output/':[/bold white]\n\n"
        f"  [green]✓[/green] {os.path.basename(archivo_consolidado)}\n"
        f"  [green]✓[/green] {os.path.basename(archivo_categorizado)}\n"
        f"  [green]✓[/green] reporte_ejecutivo_*.xlsx\n"
        f"  [green]✓[/green] dashboard_*.html",
        title="[bold green]✅ PROCESO COMPLETO FINALIZADO EXITOSAMENTE[/bold green]",
        border_style="green",
        box=box.DOUBLE
    ))

    Prompt.ask("\n[dim]Presiona ENTER para volver al menú principal[/dim]")


def solo_consolidar():
    """Ejecuta solo el bloque 1: consolidar."""
    console.print()
    console.print(Panel(
        "[bold cyan]BLOQUE 1: CONSOLIDAR EXTRACTOS BANCARIOS[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED
    ))

    # Seleccionar archivo de input
    archivo_input = seleccionar_archivo_input()
    if archivo_input is None:
        Prompt.ask("\n[dim]Presiona ENTER para volver al menú principal[/dim]")
        return

    consolidar_bancos(archivo_especifico=archivo_input)

    Prompt.ask("\n[dim]Presiona ENTER para volver al menú principal[/dim]")


def solo_categorizar():
    """Ejecuta solo el bloque 2: categorizar."""
    console.print()
    console.print(Panel(
        "[bold cyan]BLOQUE 2: CATEGORIZAR MOVIMIENTOS[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED
    ))

    categorizar_movimientos()

    Prompt.ask("\n[dim]Presiona ENTER para volver al menú principal[/dim]")


def solo_reportes():
    """Ejecuta solo el bloque 3: reportes."""
    console.print()
    console.print(Panel(
        "[bold cyan]BLOQUE 3: GENERAR REPORTES Y DASHBOARD[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED
    ))

    generar_reportes()

    Prompt.ask("\n[dim]Presiona ENTER para volver al menú principal[/dim]")


def configuracion():
    """Muestra y permite cambiar la configuración."""
    console.print()
    console.print(Panel(
        "[bold white]Configuración actual:[/bold white]\n\n"
        "  [cyan]•[/cyan] Carpeta de entrada:  [green]./input[/green]\n"
        "  [cyan]•[/cyan] Carpeta de salida:   [green]./output[/green]\n\n"
        "[yellow]Nota:[/yellow] El sistema requiere seleccionar UN archivo específico.\n"
        "Esto previene errores al mezclar archivos de diferentes períodos.\n\n"
        "[dim]Para cambiar rutas, usa --input y --output:[/dim]\n"
        "[dim]python src/main.py --consolidar --archivo MI_ARCHIVO.xlsx --input ./mis_extractos[/dim]",
        title="[bold cyan]⚙️  CONFIGURACIÓN DEL SISTEMA[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED
    ))

    Prompt.ask("\n[dim]Presiona ENTER para volver al menú principal[/dim]")


def informacion_sistema():
    """Muestra información sobre el sistema."""
    console.print()

    # Info básica
    info_texto = Text()
    info_texto.append("TORO - Sistema de Resumen de Cuenta\n", style="bold white")
    info_texto.append("Versión: ", style="dim")
    info_texto.append("1.3\n", style="bold green")
    info_texto.append("Autor: ", style="dim")
    info_texto.append("Sistema TORO\n", style="cyan")
    info_texto.append("Fecha: ", style="dim")
    info_texto.append("Noviembre 2025", style="white")

    console.print(Panel(info_texto, title="[bold cyan]ℹ️  INFORMACIÓN DEL SISTEMA[/bold cyan]", border_style="cyan", box=box.ROUNDED))

    # Bloques implementados
    console.print()
    tabla_bloques = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    tabla_bloques.add_column("", style="green", width=4)
    tabla_bloques.add_column("Bloque", style="bold white")
    tabla_bloques.add_column("Características", style="dim")

    tabla_bloques.add_row("✓", "Bloque 1: Consolidador Multi-Banco", "Detección automática • Supervielle y Galicia")
    tabla_bloques.add_row("✓", "Bloque 2: Categorizador Inteligente", "37 reglas • 99%+ clasificación automática")
    tabla_bloques.add_row("✓", "Bloque 3: Reportes y Dashboard", "Dashboard HTML • Reporte Excel ejecutivo")
    tabla_bloques.add_row("✓", "Bloque 4: Orquestador CLI", "Menú interactivo • Proceso automatizado")

    console.print(Panel(tabla_bloques, title="[bold white]BLOQUES IMPLEMENTADOS[/bold white]", border_style="green", box=box.ROUNDED))

    # Categorías
    console.print()
    categorias_texto = (
        "[bold white]Ingresos:[/bold white]\n"
        "  [cyan]•[/cyan] Afiliados DEBIN\n"
        "  [cyan]•[/cyan] Transferencias\n"
        "  [cyan]•[/cyan] Cheques y Obras Sociales\n\n"
        "[bold white]Egresos:[/bold white]\n"
        "  [cyan]•[/cyan] Prestadores\n"
        "  [cyan]•[/cyan] Sueldos\n"
        "  [cyan]•[/cyan] Impuestos (AFIP, IVA, Percepciones)\n"
        "  [cyan]•[/cyan] Comisiones Bancarias\n"
        "  [cyan]•[/cyan] Servicios (Luz, Gas, Internet)\n"
        "  [cyan]•[/cyan] Gastos Operativos"
    )

    console.print(Panel(categorias_texto, title="[bold white]CATEGORÍAS SOPORTADAS[/bold white]", border_style="yellow", box=box.ROUNDED))

    Prompt.ask("\n[dim]Presiona ENTER para volver al menú principal[/dim]")


def main():
    """Función principal del menú CLI."""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        mostrar_menu_principal()

        try:
            opcion = Prompt.ask(
                "[bold cyan]Selecciona una opción[/bold cyan]",
                choices=['0', '1', '2', '3', '4', '5', '6'],
                default='1'
            ).strip()

            if opcion == '0':
                console.print()
                console.print(Panel(
                    "[bold white]¡Gracias por usar TORO - Resumen de Cuenta![/bold white]\n"
                    "[dim]Sistema v1.3 - Noviembre 2025[/dim]",
                    title="[bold green]👋 HASTA PRONTO[/bold green]",
                    border_style="green",
                    box=box.DOUBLE
                ))
                console.print()
                sys.exit(0)

            elif opcion == '1':
                proceso_completo()

            elif opcion == '2':
                solo_consolidar()

            elif opcion == '3':
                solo_categorizar()

            elif opcion == '4':
                solo_reportes()

            elif opcion == '5':
                configuracion()

            elif opcion == '6':
                informacion_sistema()

            else:
                console.print("\n[bold red]❌ ERROR:[/bold red] Opción inválida. Por favor selecciona una opción del menú.")
                Prompt.ask("\n[dim]Presiona ENTER para continuar[/dim]")

        except KeyboardInterrupt:
            console.print()
            console.print(Panel(
                "[bold white]¡Gracias por usar TORO - Resumen de Cuenta![/bold white]\n"
                "[dim]Sistema v1.3 - Noviembre 2025[/dim]",
                title="[bold yellow]👋 HASTA PRONTO[/bold yellow]",
                border_style="yellow",
                box=box.DOUBLE
            ))
            console.print()
            sys.exit(0)

        except Exception as e:
            console.print(f"\n[bold red]❌ ERROR INESPERADO:[/bold red] {e}")
            Prompt.ask("\n[dim]Presiona ENTER para continuar[/dim]")


if __name__ == "__main__":
    main()
