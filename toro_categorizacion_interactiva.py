"""
Módulo de categorización interactiva para movimientos bancarios
Integrado con toro_categorias para gestión unificada de categorías y reglas
"""
import pandas as pd
from typing import Optional, Tuple
from toro_categorias import cargar_categorias, crear_regla_desde_movimiento


def mostrar_movimiento(movimiento: pd.Series, numero: int, total: int):
    """
    Muestra la información de un movimiento en pantalla.

    Args:
        movimiento: Serie de pandas con datos del movimiento
        numero: Número del movimiento actual
        total: Total de movimientos sin clasificar
    """
    print("\n" + "="*80)
    print(f"Movimiento #{numero} de {total} sin clasificar")
    print("="*80)

    print(f"\nFecha:    {movimiento.get('Fecha', 'N/A')}")
    print(f"Banco:    {movimiento.get('Banco', 'N/A')}")
    print(f"Concepto: {movimiento.get('Concepto', 'N/A')}")

    if pd.notna(movimiento.get('Detalle')) and str(movimiento.get('Detalle')) != 'None':
        detalle = str(movimiento['Detalle'])
        print(f"Detalle:  {detalle[:80]}")
        if len(detalle) > 80:
            print(f"          {detalle[80:160]}")

    # Mostrar monto con formato
    debito = movimiento.get('Débito', 0) or movimiento.get('Debito', 0) or 0
    credito = movimiento.get('Crédito', 0) or movimiento.get('Credito', 0) or 0

    if debito > 0:
        print(f"Monto:    ${debito:,.2f} (DEBITO)")
    elif credito > 0:
        print(f"Monto:    ${credito:,.2f} (CREDITO)")

    # Metadata adicional si está disponible
    if pd.notna(movimiento.get('Persona_Nombre')):
        print(f"Persona:  {movimiento['Persona_Nombre']}")

    if movimiento.get('Es_DEBIN', False):
        print(f"DEBIN:    SI")
        if pd.notna(movimiento.get('DEBIN_ID')):
            print(f"ID DEBIN: {movimiento['DEBIN_ID']}")


def mostrar_categorias_disponibles(categorias: list) -> dict:
    """
    Muestra las categorías disponibles y retorna un mapeo número -> categoría.

    Args:
        categorias: Lista de dicts con 'id' y 'nombre'

    Returns:
        Dict mapeando número -> dict de categoría
    """
    print(f"\n{'='*80}")
    print("CATEGORIAS DISPONIBLES:")
    print(f"{'='*80}\n")

    opciones = {}
    for idx, cat in enumerate(categorias, start=1):
        print(f"  [{idx}] {cat['nombre']} ({cat['id']})")
        opciones[idx] = cat

    print(f"\n  [0] Omitir este movimiento")
    print(f"  [S] Salir de la revision")

    return opciones


def solicitar_categoria(opciones: dict) -> Optional[str]:
    """
    Solicita al usuario que seleccione una categoría.

    Args:
        opciones: Dict con mapeo número -> categoría

    Returns:
        ID de categoría seleccionada, '0' para omitir, 'S' para salir, o None si error
    """
    while True:
        try:
            respuesta = input("\nSelecciona una opcion: ").strip().upper()

            if respuesta == 'S':
                return 'S'
            elif respuesta == '0':
                return '0'
            else:
                try:
                    num = int(respuesta)
                    if num in opciones:
                        return opciones[num]['id']
                    else:
                        print(f"❌ Opción inválida: {num}")
                except ValueError:
                    print(f"❌ Por favor ingresa un número válido")
        except KeyboardInterrupt:
            print("\n\n⚠ Revisión cancelada por el usuario.")
            return 'S'


def solicitar_crear_regla() -> bool:
    """
    Pregunta si se debe crear una regla automática.

    Returns:
        True si se debe crear la regla, False en caso contrario
    """
    while True:
        try:
            respuesta = input("\n¿Crear regla automática para futuros movimientos similares? (S/N): ").strip().upper()
            if respuesta in ['S', 'SI', 'Y', 'YES']:
                return True
            elif respuesta in ['N', 'NO']:
                return False
            else:
                print("Por favor responde S (Sí) o N (No)")
        except KeyboardInterrupt:
            return False


def asignar_categoria_interactiva(movimiento: pd.Series, numero: int, total: int) -> Tuple[Optional[str], bool]:
    """
    Permite al usuario asignar interactivamente una categoría a un movimiento.

    Args:
        movimiento: Serie de pandas con datos del movimiento
        numero: Número del movimiento actual (para mostrar progreso)
        total: Total de movimientos a procesar

    Returns:
        Tupla (categoria_id, crear_regla):
            - categoria_id: ID de la categoría seleccionada, '0' para omitir, 'S' para salir
            - crear_regla: True si se debe crear regla automática
    """
    # Mostrar movimiento
    mostrar_movimiento(movimiento, numero, total)

    # Cargar categorías disponibles
    categorias = cargar_categorias()
    if not categorias:
        print("\n⚠ No hay categorías configuradas. Usa la opción 7 del menú principal para agregar categorías.")
        return None, False

    # Mostrar categorías y obtener mapeo
    opciones = mostrar_categorias_disponibles(categorias)

    # Solicitar selección
    categoria_id = solicitar_categoria(opciones)

    # Procesar respuesta
    if categoria_id == 'S':
        return 'S', False
    elif categoria_id == '0':
        print("⚠ Movimiento omitido.")
        return '0', False
    elif categoria_id:
        # Preguntar si crear regla
        crear_regla = solicitar_crear_regla()

        # Mostrar confirmación
        cat_info = next((c for c in categorias if c['id'] == categoria_id), None)
        if cat_info:
            print(f"\n✅ Categoría asignada: {cat_info['nombre']} ({categoria_id})")
            if crear_regla:
                print("   📝 Se creará regla automática")

        return categoria_id, crear_regla

    return None, False


def procesar_movimientos_sin_clasificar(df_sin_clasificar: pd.DataFrame,
                                       df_completo: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa interactivamente todos los movimientos sin clasificar.

    Args:
        df_sin_clasificar: DataFrame con movimientos sin clasificar
        df_completo: DataFrame completo con todos los movimientos

    Returns:
        DataFrame completo con las categorizaciones aplicadas
    """
    if len(df_sin_clasificar) == 0:
        print("\n✅ No hay movimientos sin clasificar. Todos fueron categorizados automáticamente!")
        return df_completo

    print(f"\n{'='*80}")
    print(f"REVISIÓN MANUAL DE MOVIMIENTOS SIN CLASIFICAR")
    print(f"{'='*80}")
    print(f"\nTotal de movimientos a revisar: {len(df_sin_clasificar)}")
    print(f"\nInstrucciones:")
    print(f"  • Revisa cada movimiento cuidadosamente")
    print(f"  • Selecciona la categoría correcta")
    print(f"  • Decide si quieres crear una regla automática")
    print(f"  • Puedes omitir movimientos y salir en cualquier momento")

    input("\nPresiona ENTER para comenzar...")

    df_resultado = df_completo.copy()
    contador = 0
    corregidos = 0
    reglas_creadas = 0

    for idx, movimiento in df_sin_clasificar.iterrows():
        contador += 1

        # Asignar categoría interactivamente
        categoria_id, crear_regla = asignar_categoria_interactiva(movimiento, contador, len(df_sin_clasificar))

        # Procesar resultado
        if categoria_id == 'S':
            print("\n⚠ Saliendo de la revisión...")
            break
        elif categoria_id == '0':
            continue
        elif categoria_id:
            # Aplicar categoría al DataFrame
            # Determinar columnas (pueden variar entre Categoria_Principal o Categoría)
            col_categoria = 'Categoria_Principal' if 'Categoria_Principal' in df_resultado.columns else 'Categoría'

            df_resultado.loc[idx, col_categoria] = categoria_id

            # Marcar como manual si existe la columna
            if 'Clasificacion_Manual' in df_resultado.columns:
                df_resultado.loc[idx, 'Clasificacion_Manual'] = True

            corregidos += 1

            # Crear regla si se solicitó
            if crear_regla:
                # Convertir Serie a dict para crear_regla_desde_movimiento
                mov_dict = movimiento.to_dict()
                crear_regla_desde_movimiento(mov_dict, categoria_id)
                reglas_creadas += 1

    # Resumen
    print(f"\n{'='*80}")
    print(f"RESUMEN DE REVISIÓN")
    print(f"{'='*80}")
    print(f"Movimientos revisados:     {contador}/{len(df_sin_clasificar)}")
    print(f"Movimientos categorizados: {corregidos}")
    print(f"Movimientos omitidos:      {contador - corregidos}")
    print(f"Reglas creadas:            {reglas_creadas}")

    return df_resultado
