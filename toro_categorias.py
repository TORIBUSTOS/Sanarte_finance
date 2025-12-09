import json
from pathlib import Path

# Directorio base: carpeta donde está este archivo
BASE_DIR = Path(__file__).resolve().parent

# Carpeta y archivos de configuración
CONFIG_DIR = BASE_DIR / "config"
CATEGORIES_FILE = CONFIG_DIR / "categorias.json"
REGLAS_FILE = CONFIG_DIR / "reglas_categorias.json"


# ============================
# GESTIÓN DE CATEGORÍAS
# ============================

def cargar_categorias():
    """Lee el archivo de categorías y devuelve una lista de dicts."""
    if not CATEGORIES_FILE.exists():
        return []

    with open(CATEGORIES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("categorias", [])


def guardar_categorias(categorias):
    """Guarda la lista de categorías en el archivo JSON."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CATEGORIES_FILE, "w", encoding="utf-8") as f:
        json.dump({"categorias": categorias}, f, indent=2, ensure_ascii=False)


def listar_categorias():
    """Imprime por consola la lista de categorías configuradas."""
    categorias = cargar_categorias()
    if not categorias:
        print("\nNo hay categorías configuradas.")
        return

    print("\nCategorías actuales:")
    for idx, cat in enumerate(categorias, start=1):
        print(f"{idx}. {cat['id']} - {cat['nombre']}")


def agregar_categoria():
    """Pide datos por consola y agrega una nueva categoría."""
    categorias = cargar_categorias()

    nuevo_id = input("\nID interno de la categoría (ej: HONORARIOS): ").strip().upper()
    if not nuevo_id:
        print("El ID de la categoría no puede estar vacío.")
        return

    # Validar que no exista el ID
    for cat in categorias:
        if cat["id"] == nuevo_id:
            print("⚠ Ya existe una categoría con ese ID.")
            return

    nombre_visible = input("Nombre para mostrar (ej: Honorarios profesionales): ").strip()
    if not nombre_visible:
        print("El nombre visible no puede estar vacío.")
        return

    categorias.append({"id": nuevo_id, "nombre": nombre_visible})
    guardar_categorias(categorias)
    print("✅ Categoría agregada correctamente.")


def editar_categoria():
    """Permite cambiar el nombre visible de una categoría."""
    categorias = cargar_categorias()
    if not categorias:
        print("\nNo hay categorías para editar.")
        return

    listar_categorias()
    try:
        pos = int(input("\nNúmero de categoría a editar: "))
        cat = categorias[pos - 1]
    except (ValueError, IndexError):
        print("Selección inválida.")
        return

    print(f"Editando: {cat['id']} - {cat['nombre']}")
    nuevo_nombre = input("Nuevo nombre (enter para dejar igual): ").strip()

    if nuevo_nombre:
        cat["nombre"] = nuevo_nombre
        guardar_categorias(categorias)
        print("✅ Categoría actualizada.")
    else:
        print("No se hicieron cambios.")


def borrar_categoria():
    """Permite eliminar una categoría del catálogo."""
    categorias = cargar_categorias()
    if not categorias:
        print("\nNo hay categorías para borrar.")
        return

    listar_categorias()
    try:
        pos = int(input("\nNúmero de categoría a borrar: "))
        cat = categorias[pos - 1]
    except (ValueError, IndexError):
        print("Selección inválida.")
        return

    # Evitar borrar la categoría por defecto si se usa como fallback
    if cat["id"] == "SIN_CATEGORIA":
        print("⚠ No se recomienda borrar la categoría SIN_CATEGORIA.")
        return

    confirm = input(f"¿Seguro que querés borrar '{cat['nombre']}'? (s/n): ").strip().lower()
    if confirm == "s":
        categorias.pop(pos - 1)
        guardar_categorias(categorias)
        print("✅ Categoría borrada.")
    else:
        print("Operación cancelada.")


def menu_categorias():
    """
    Menú interactivo para gestionar categorías.

    Esta función será llamada desde el menú principal (opción 7).
    """
    while True:
        print("\n=== Gestión de categorías ===")
        print("1. Listar categorías")
        print("2. Agregar categoría")
        print("3. Editar categoría")
        print("4. Borrar categoría")
        print("0. Volver")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            listar_categorias()
        elif opcion == "2":
            agregar_categoria()
        elif opcion == "3":
            editar_categoria()
        elif opcion == "4":
            borrar_categoria()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


# ============================
# GESTIÓN DE REGLAS
# ============================

def cargar_reglas():
    """Lee el archivo de reglas de categorización."""
    if not REGLAS_FILE.exists():
        return []

    with open(REGLAS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("reglas", [])


def guardar_reglas(reglas):
    """Guarda la lista de reglas en el archivo JSON."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(REGLAS_FILE, "w", encoding="utf-8") as f:
        json.dump({"reglas": reglas}, f, indent=2, ensure_ascii=False)


def clasificar_movimiento(movimiento: dict) -> str:
    """
    Devuelve el ID de categoría para un movimiento según las reglas definidas.

    movimiento debería ser un dict con campos como:
    {
        "alias": "...",
        "cbu": "...",
        "titular": "...",
        "nombre": "...",
        "concepto": "...",
        "documento": "...",
        ...
    }
    """
    reglas = cargar_reglas()

    for regla in reglas:
        criterio = regla["criterio"]      # ej: "cbu", "nombre", "documento", "concepto"
        valor_busqueda = regla["valor"]
        categoria_id = regla["categoria_id"]

        valor_mov = movimiento.get(criterio)
        if valor_mov is None:
            continue

        # Comparación case-insensitive
        if str(valor_mov).upper() == str(valor_busqueda).upper():
            return categoria_id

    # Categoría por defecto si ninguna regla matchea
    return "SIN_CATEGORIA"


def agregar_regla(criterio: str, valor: str, categoria_id: str):
    """
    Agrega una regla simple al archivo de reglas.

    criterio: campo a matchear (ej: 'cbu', 'nombre', 'documento', 'concepto')
    valor: valor exacto a comparar
    categoria_id: ID de la categoría (ej: 'HONORARIOS_ABOGADO')
    """
    reglas = cargar_reglas()

    # Evitar duplicados exactos
    for r in reglas:
        if (
            r.get("criterio") == criterio
            and str(r.get("valor")).upper() == str(valor).upper()
            and r.get("categoria_id") == categoria_id
        ):
            print("⚠ Ya existe una regla igual, no se agrega otra.")
            return

    nueva_regla = {
        "criterio": criterio,
        "valor": valor,
        "categoria_id": categoria_id,
    }
    reglas.append(nueva_regla)
    guardar_reglas(reglas)
    print(f"✅ Regla agregada: si {criterio} = '{valor}' → {categoria_id}")


def crear_regla_desde_movimiento(movimiento: dict, categoria_id: str):
    """
    Crea una regla tomando datos del movimiento.

    Prioridad:
    - Si tiene CBU, usar CBU.
    - Si no, usar NOMBRE / TITULAR.
    - Si no, usar DOCUMENTO.
    - Si no, usar CONCEPTO.
    """
    # 1) Intentar usar CBU
    cbu = movimiento.get("cbu") or movimiento.get("CBU")
    if cbu:
        agregar_regla("cbu", str(cbu), categoria_id)
        return

    # 2) Intentar usar nombre / titular
    nombre = (
        movimiento.get("nombre")
        or movimiento.get("NOMBRE")
        or movimiento.get("titular")
        or movimiento.get("TITULAR")
    )
    if nombre:
        agregar_regla("nombre", str(nombre), categoria_id)
        return

    # 3) Intentar usar documento
    documento = (
        movimiento.get("documento")
        or movimiento.get("DOCUMENTO")
    )
    if documento:
        agregar_regla("documento", str(documento), categoria_id)
        return

    # 4) Intentar usar concepto
    concepto = (
        movimiento.get("concepto")
        or movimiento.get("CONCEPTO")
    )
    if concepto:
        agregar_regla("concepto", str(concepto), categoria_id)
        return

    print("⚠ No se pudo crear una regla automática: faltan datos (CBU/NOMBRE/DOCUMENTO/CONCEPTO).")
