"""
CLI para corrección manual de categorías
Autor: Sistema SANARTE
"""
import pandas as pd
from typing import Dict, List

class CLICorrector:
    """
    Interfaz de línea de comandos para revisar y corregir movimientos sin clasificar.
    """

    def __init__(self, categorias: Dict[str, List[str]]):
        """
        Args:
            categorias: Diccionario {categoria: [subcategorias]}
        """
        self.categorias = categorias
        self.crear_menu_opciones()

    def crear_menu_opciones(self):
        """
        Crea el menú de opciones de categorías disponibles.
        """
        self.opciones = []
        contador = 1

        for categoria, subcategorias in self.categorias.items():
            for subcategoria in subcategorias:
                self.opciones.append({
                    'numero': contador,
                    'categoria': categoria,
                    'subcategoria': subcategoria
                })
                contador += 1

    def mostrar_movimiento(self, movimiento: pd.Series, numero: int, total: int):
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

        print(f"\nFecha:    {movimiento['Fecha']}")
        print(f"Banco:    {movimiento['Banco']}")
        print(f"Concepto: {movimiento['Concepto']}")

        if pd.notna(movimiento['Detalle']) and str(movimiento['Detalle']) != 'None':
            print(f"Detalle:  {movimiento['Detalle'][:80]}")
            if len(str(movimiento['Detalle'])) > 80:
                print(f"          {movimiento['Detalle'][80:][:80]}")

        # Mostrar monto con formato
        if movimiento['Débito'] > 0:
            monto_str = f"${movimiento['Débito']:,.2f} (DEBITO)"
            print(f"Monto:    {monto_str}")
        else:
            monto_str = f"${movimiento['Crédito']:,.2f} (CREDITO)"
            print(f"Monto:    {monto_str}")

        # Metadata si está disponible
        if pd.notna(movimiento.get('Persona_Nombre')):
            print(f"Persona:  {movimiento['Persona_Nombre']}")

        if movimiento.get('Es_DEBIN', False):
            print(f"DEBIN:    SI")
            if pd.notna(movimiento.get('DEBIN_ID')):
                print(f"ID DEBIN: {movimiento['DEBIN_ID']}")

    def mostrar_opciones(self):
        """
        Muestra el menú de categorías disponibles.
        """
        print(f"\n{'='*80}")
        print("CATEGORIAS DISPONIBLES:")
        print(f"{'='*80}")

        ultima_categoria = None

        for opcion in self.opciones:
            # Mostrar header de categoría si cambió
            if opcion['categoria'] != ultima_categoria:
                print(f"\n{opcion['categoria']}:")
                ultima_categoria = opcion['categoria']

            print(f"  [{opcion['numero']}] {opcion['subcategoria']}")

        print(f"\n  [0] Omitir este movimiento")
        print(f"  [S] Salir de la revision")

    def solicitar_opcion(self) -> str:
        """
        Solicita al usuario que seleccione una opción.

        Returns:
            Opción seleccionada (como string)
        """
        while True:
            try:
                respuesta = input("\nSelecciona una opcion: ").strip().upper()
                return respuesta
            except KeyboardInterrupt:
                print("\n\nRevision cancelada por el usuario.")
                return 'S'
            except:
                print("Opcion invalida. Intenta nuevamente.")

    def solicitar_aprender(self) -> bool:
        """
        Pregunta si se debe recordar la regla.

        Returns:
            True si se debe aprender, False en caso contrario
        """
        while True:
            try:
                respuesta = input("\nRecordar esta regla para futuros movimientos? (S/N): ").strip().upper()
                if respuesta in ['S', 'SI', 'Y', 'YES']:
                    return True
                elif respuesta in ['N', 'NO']:
                    return False
                else:
                    print("Por favor responde S (Si) o N (No)")
            except KeyboardInterrupt:
                return False

    def procesar_sin_clasificar(self, df_sin_clasificar: pd.DataFrame,
                                df_completo: pd.DataFrame,
                                categorizer) -> pd.DataFrame:
        """
        Procesa interactivamente los movimientos sin clasificar.

        Args:
            df_sin_clasificar: DataFrame con movimientos sin clasificar
            df_completo: DataFrame completo con todos los movimientos
            categorizer: Instancia del Categorizer para aplicar correcciones

        Returns:
            DataFrame completo con correcciones aplicadas
        """
        if len(df_sin_clasificar) == 0:
            print("\nNo hay movimientos sin clasificar. Todos fueron categorizados automaticamente!")
            return df_completo

        print(f"\n{'='*80}")
        print(f"REVISION MANUAL DE MOVIMIENTOS SIN CLASIFICAR")
        print(f"{'='*80}")
        print(f"\nTotal de movimientos a revisar: {len(df_sin_clasificar)}")
        print(f"\nInstrucciones:")
        print(f"  - Revisa cada movimiento cuidadosamente")
        print(f"  - Selecciona la categoria correcta")
        print(f"  - Decide si quieres recordar la regla")
        print(f"  - Puedes omitir movimientos y salir en cualquier momento")

        input("\nPresiona ENTER para comenzar...")

        df_resultado = df_completo.copy()
        contador = 0
        corregidos = 0

        for idx, movimiento in df_sin_clasificar.iterrows():
            contador += 1

            # Mostrar movimiento
            self.mostrar_movimiento(movimiento, contador, len(df_sin_clasificar))

            # Mostrar opciones
            self.mostrar_opciones()

            # Solicitar opción
            opcion = self.solicitar_opcion()

            # Procesar opción
            if opcion == 'S':
                print("\nSaliendo de la revision...")
                break
            elif opcion == '0':
                print("Movimiento omitido.")
                continue
            else:
                try:
                    num_opcion = int(opcion)

                    # Buscar la opción seleccionada
                    opcion_elegida = None
                    for op in self.opciones:
                        if op['numero'] == num_opcion:
                            opcion_elegida = op
                            break

                    if opcion_elegida:
                        # Preguntar si aprender
                        aprender = self.solicitar_aprender()

                        # Aplicar corrección
                        df_resultado = categorizer.aplicar_correccion(
                            df=df_resultado,
                            idx=idx,
                            categoria=opcion_elegida['categoria'],
                            subcategoria=opcion_elegida['subcategoria'],
                            aprender=aprender
                        )

                        corregidos += 1
                        print(f"\nOK Movimiento clasificado como: {opcion_elegida['categoria']} > {opcion_elegida['subcategoria']}")

                        if aprender:
                            print("   Regla guardada para futuros movimientos.")

                    else:
                        print(f"Opcion invalida: {num_opcion}")

                except ValueError:
                    print(f"Opcion invalida: {opcion}")

        # Resumen
        print(f"\n{'='*80}")
        print(f"RESUMEN DE REVISION")
        print(f"{'='*80}")
        print(f"Movimientos revisados: {contador}/{len(df_sin_clasificar)}")
        print(f"Movimientos corregidos: {corregidos}")
        print(f"Movimientos omitidos: {contador - corregidos}")

        if corregidos > 0:
            # Guardar reglas aprendidas
            categorizer.guardar_reglas_aprendidas()

        return df_resultado
