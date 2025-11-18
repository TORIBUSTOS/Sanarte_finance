"""
Categorizador de movimientos bancarios
Autor: Sistema SANARTE
Versión: 2.0 - Sistema de Cascada de 2 Niveles
"""
import pandas as pd
from .clasificador_cascada import ClasificadorCascada
from .metadata_extractor import MetadataExtractor

class Categorizer:
    """
    Categoriza movimientos bancarios automáticamente usando estrategia de cascada:
    - Nivel 1: Clasificación BASE por "Concepto" (siempre disponible)
    - Nivel 2: Refinamiento por "Detalle" (cuando disponible)

    Objetivo: 99%+ de clasificación automática
    """

    def __init__(self):
        """Inicializa el categorizador con el clasificador en cascada."""
        self.clasificador = ClasificadorCascada()
        self.extractor = MetadataExtractor()

        # Mostrar estadísticas del clasificador
        stats = self.clasificador.obtener_estadisticas()
        print(f"\nClasificador Cascada v2.0 inicializado:")
        print(f"  - Reglas de Concepto (Nivel 1): {stats['reglas_concepto']}")
        print(f"  - Categorías Refinables (Nivel 2): {stats['categorias_refinables']}")
        print(f"  - Patrones de Refinamiento: {stats['patrones_refinamiento']}")
        print(f"  - Cobertura Estimada: {stats['cobertura_estimada']}")

    def categorizar_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Categoriza todos los movimientos de un DataFrame usando sistema de cascada.

        Añade las siguientes columnas NUEVAS:
        - Tipo_Movimiento: "Ingreso" o "Egreso"
        - Categoria_Principal: Texto antes del " - " (ej: "Servicios")
        - Categoria_Final: Categoría completa refinada (ej: "Servicios - Agua")

        También mantiene columnas de metadata:
        - Persona_Nombre
        - Documento
        - Es_DEBIN
        - DEBIN_ID

        Args:
            df: DataFrame con movimientos consolidados

        Returns:
            DataFrame con columnas de categorización añadidas
        """
        print(f"\nCategorizando {len(df)} movimientos...")
        print("Estrategia: Cascada de 2 Niveles (Concepto + Detalle)")

        df = df.copy()

        # Inicializar columnas NUEVAS
        df['Tipo_Movimiento'] = None
        df['Categoria_Principal'] = None
        df['Categoria_Final'] = None

        # Inicializar columnas de metadata
        df['Persona_Nombre'] = None
        df['Documento'] = None
        df['Es_DEBIN'] = False
        df['DEBIN_ID'] = None

        total = len(df)
        clasificados_nivel1 = 0
        clasificados_nivel2 = 0
        sin_clasificar = 0

        # Procesar cada movimiento
        for idx, row in df.iterrows():
            # Clasificar usando cascada
            tipo_mov, cat_principal, cat_final, confianza = self.clasificador.clasificar_movimiento(
                concepto=row['Concepto'],
                detalle=row['Detalle'],
                debito=row['Débito'],
                credito=row['Crédito']
            )

            # Extraer metadata
            metadata = self.extractor.extraer_metadata(
                concepto=row['Concepto'],
                detalle=row['Detalle']
            )

            # Asignar categorías
            df.at[idx, 'Tipo_Movimiento'] = tipo_mov
            df.at[idx, 'Categoria_Principal'] = cat_principal
            df.at[idx, 'Categoria_Final'] = cat_final

            # Asignar metadata
            df.at[idx, 'Persona_Nombre'] = metadata['persona_nombre']
            df.at[idx, 'Documento'] = metadata['documento']
            df.at[idx, 'Es_DEBIN'] = metadata['es_debin']
            df.at[idx, 'DEBIN_ID'] = metadata['debin_id']

            # Contadores para estadísticas
            if confianza == 0:
                sin_clasificar += 1
            else:
                clasificados_nivel1 += 1
                # Detectar si hubo refinamiento (Nivel 2 aplicado)
                if cat_principal != cat_final and " - " in cat_final:
                    clasificados_nivel2 += 1

        # Estadísticas detalladas
        clasificados_total = clasificados_nivel1
        porcentaje_clasificados = (clasificados_total / total) * 100 if total > 0 else 0
        porcentaje_refinados = (clasificados_nivel2 / clasificados_total * 100) if clasificados_total > 0 else 0

        print(f"\n{'='*80}")
        print("ESTADÍSTICAS DE CLASIFICACIÓN")
        print(f"{'='*80}")
        print(f"Total movimientos:              {total}")
        print(f"Clasificados automáticamente:   {clasificados_total} ({porcentaje_clasificados:.1f}%)")
        print(f"  - Solo Nivel 1 (Concepto):    {clasificados_nivel1 - clasificados_nivel2}")
        print(f"  - Refinados Nivel 2 (Detalle): {clasificados_nivel2} ({porcentaje_refinados:.1f}% de clasificados)")
        print(f"Sin clasificar:                 {sin_clasificar} ({100-porcentaje_clasificados:.1f}%)")

        # Desglose por categoría principal
        if clasificados_total > 0:
            print(f"\nDESGLOSE POR CATEGORÍA PRINCIPAL:")
            print("-" * 80)
            categorias_principales = df[df['Categoria_Principal'] != 'Sin Clasificar']['Categoria_Principal'].value_counts()
            for cat, count in categorias_principales.items():
                porcentaje = (count / total) * 100
                print(f"  {cat:30s} {count:4d} movimientos ({porcentaje:5.1f}%)")

        return df

    def exportar_categorizados(self, df: pd.DataFrame, ruta_salida: str):
        """
        Exporta DataFrame categorizado a Excel con las nuevas columnas.

        Args:
            df: DataFrame con categorías
            ruta_salida: Ruta del archivo de salida
        """
        print(f"\nExportando movimientos categorizados...")

        # Reordenar columnas para mejor visualización
        columnas_ordenadas = [
            'Fecha', 'Concepto', 'Detalle',
            'Débito', 'Crédito', 'Saldo',
            'Banco',
            'Tipo_Movimiento', 'Categoria_Principal', 'Categoria_Final',
            'Persona_Nombre', 'Documento', 'Es_DEBIN', 'DEBIN_ID'
        ]

        df_export = df[columnas_ordenadas].copy()

        # Exportar a Excel
        with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
            df_export.to_excel(writer, sheet_name='Movimientos Categorizados', index=False)

            # Aplicar formato
            worksheet = writer.sheets['Movimientos Categorizados']

            # Anchos de columna
            anchos = {
                'A': 20,  # Fecha
                'B': 35,  # Concepto
                'C': 50,  # Detalle
                'D': 15,  # Débito
                'E': 15,  # Crédito
                'F': 15,  # Saldo
                'G': 12,  # Banco
                'H': 12,  # Tipo_Movimiento
                'I': 25,  # Categoria_Principal
                'J': 40,  # Categoria_Final
                'K': 30,  # Persona_Nombre
                'L': 15,  # Documento
                'M': 10,  # Es_DEBIN
                'N': 15,  # DEBIN_ID
            }

            for col, ancho in anchos.items():
                worksheet.column_dimensions[col].width = ancho

            # Formato numérico
            for row in range(2, len(df_export) + 2):
                for col in ['D', 'E', 'F']:
                    cell = worksheet[f'{col}{row}']
                    cell.number_format = '#,##0.00'

        print(f"OK Archivo exportado: {ruta_salida}")
        print(f"Columnas generadas:")
        print(f"  - Tipo_Movimiento")
        print(f"  - Categoria_Principal")
        print(f"  - Categoria_Final")

    def obtener_sin_clasificar(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Retorna solo los movimientos sin clasificar.

        Args:
            df: DataFrame categorizado

        Returns:
            DataFrame con movimientos sin clasificar
        """
        return df[df['Categoria_Principal'] == 'Sin Clasificar'].copy()

    def aplicar_correccion(self, df: pd.DataFrame, idx: int,
                          categoria_final: str, tipo_movimiento: str = None,
                          aprender: bool = True) -> pd.DataFrame:
        """
        Aplica una corrección manual a un movimiento.

        Args:
            df: DataFrame categorizado
            idx: Índice del movimiento a corregir
            categoria_final: Nueva categoría completa (ej: "Servicios - Agua")
            tipo_movimiento: "Ingreso" o "Egreso" (opcional, se infiere si no se provee)
            aprender: Si True, guarda la regla para aprendizaje futuro

        Returns:
            DataFrame con la corrección aplicada
        """
        df = df.copy()

        # Extraer categoria_principal de categoria_final
        if " - " in categoria_final:
            categoria_principal = categoria_final.split(" - ")[0]
        else:
            categoria_principal = categoria_final

        # Inferir tipo_movimiento si no se provee
        if tipo_movimiento is None:
            # Inferir basado en Débito/Crédito
            credito = df.at[idx, 'Crédito']
            tipo_movimiento = "Ingreso" if credito > 0 else "Egreso"

        # Aplicar corrección
        df.at[idx, 'Tipo_Movimiento'] = tipo_movimiento
        df.at[idx, 'Categoria_Principal'] = categoria_principal
        df.at[idx, 'Categoria_Final'] = categoria_final

        # Nota: El sistema de aprendizaje automático requeriría reimplementación
        # en el nuevo ClasificadorCascada para agregar reglas dinámicamente.
        # Por ahora, solo aplicamos la corrección manual.
        if aprender:
            print(f"  NOTA: La corrección se aplicó pero el aprendizaje automático requiere")
            print(f"        agregar la regla manualmente en clasificador_cascada.py")

        return df

    def guardar_reglas_aprendidas(self):
        """
        Guarda las reglas aprendidas.

        NOTA: Con el nuevo sistema ClasificadorCascada, las reglas se definen
        directamente en el código fuente (clasificador_cascada.py) en lugar de
        en un archivo JSON externo. Para agregar nuevas reglas permanentemente,
        deben añadirse manualmente en ese archivo.
        """
        print("NOTA: El nuevo sistema de clasificación usa reglas hardcoded.")
        print("      Para agregar reglas permanentes, editar clasificador_cascada.py")
