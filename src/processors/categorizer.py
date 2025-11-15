"""
Categorizador de movimientos bancarios
Autor: Sistema SANARTE
"""
import pandas as pd
from .clasificador import Clasificador
from .metadata_extractor import MetadataExtractor

class Categorizer:
    """
    Categoriza movimientos bancarios automáticamente.
    Integra clasificación por reglas y extracción de metadata.
    """

    def __init__(self, umbral_confianza: int = 70, ruta_reglas: str = "./data/reglas.json"):
        """
        Args:
            umbral_confianza: Confianza mínima para clasificación automática (default: 70%)
            ruta_reglas: Ruta al archivo de reglas JSON
        """
        self.umbral_confianza = umbral_confianza
        self.clasificador = Clasificador(ruta_reglas=ruta_reglas)
        self.extractor = MetadataExtractor()

    def categorizar_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Categoriza todos los movimientos de un DataFrame.

        Añade las siguientes columnas:
        - Categoria
        - Subcategoria
        - Confianza_%
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

        df = df.copy()

        # Inicializar columnas nuevas
        df['Categoria'] = None
        df['Subcategoria'] = None
        df['Confianza_%'] = 0
        df['Persona_Nombre'] = None
        df['Documento'] = None
        df['Es_DEBIN'] = False
        df['DEBIN_ID'] = None

        total = len(df)
        clasificados_auto = 0
        sin_clasificar = 0

        # Procesar cada movimiento
        for idx, row in df.iterrows():
            # Clasificar
            categoria, subcategoria, confianza = self.clasificador.clasificar_movimiento(
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

            # Si la confianza es suficiente, asignar categoría
            if confianza >= self.umbral_confianza:
                df.at[idx, 'Categoria'] = categoria
                df.at[idx, 'Subcategoria'] = subcategoria
                df.at[idx, 'Confianza_%'] = confianza
                clasificados_auto += 1
            else:
                # Marcar como sin clasificar
                df.at[idx, 'Categoria'] = 'Sin Clasificar'
                df.at[idx, 'Subcategoria'] = 'Requiere Revision'
                df.at[idx, 'Confianza_%'] = confianza
                sin_clasificar += 1

            # Asignar metadata
            df.at[idx, 'Persona_Nombre'] = metadata['persona_nombre']
            df.at[idx, 'Documento'] = metadata['documento']
            df.at[idx, 'Es_DEBIN'] = metadata['es_debin']
            df.at[idx, 'DEBIN_ID'] = metadata['debin_id']

        # Estadísticas
        porcentaje_auto = (clasificados_auto / total) * 100 if total > 0 else 0

        print(f"\nEstadisticas de clasificacion:")
        print(f"  Total movimientos: {total}")
        print(f"  Clasificados automaticamente: {clasificados_auto} ({porcentaje_auto:.1f}%)")
        print(f"  Sin clasificar: {sin_clasificar} ({100-porcentaje_auto:.1f}%)")

        # Desglose por categoría
        if clasificados_auto > 0:
            print(f"\n  Desglose por categoria:")
            categorias_count = df[df['Categoria'] != 'Sin Clasificar']['Categoria'].value_counts()
            for cat, count in categorias_count.items():
                porcentaje = (count / total) * 100
                print(f"    - {cat}: {count} ({porcentaje:.1f}%)")

        return df

    def exportar_categorizados(self, df: pd.DataFrame, ruta_salida: str):
        """
        Exporta DataFrame categorizado a Excel.

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
            'Categoria', 'Subcategoria', 'Confianza_%',
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
                'H': 18,  # Categoria
                'I': 25,  # Subcategoria
                'J': 12,  # Confianza_%
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

    def obtener_sin_clasificar(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Retorna solo los movimientos sin clasificar.

        Args:
            df: DataFrame categorizado

        Returns:
            DataFrame con movimientos sin clasificar
        """
        return df[df['Categoria'] == 'Sin Clasificar'].copy()

    def aplicar_correccion(self, df: pd.DataFrame, idx: int,
                          categoria: str, subcategoria: str,
                          aprender: bool = True) -> pd.DataFrame:
        """
        Aplica una corrección manual a un movimiento.

        Args:
            df: DataFrame categorizado
            idx: Índice del movimiento a corregir
            categoria: Nueva categoría
            subcategoria: Nueva subcategoría
            aprender: Si True, guarda la regla para aprendizaje futuro

        Returns:
            DataFrame con la corrección aplicada
        """
        df = df.copy()

        # Aplicar corrección
        df.at[idx, 'Categoria'] = categoria
        df.at[idx, 'Subcategoria'] = subcategoria
        df.at[idx, 'Confianza_%'] = 100  # Corrección manual = 100% confianza

        # Aprender regla si se solicita
        if aprender:
            concepto = df.at[idx, 'Concepto']
            detalle = df.at[idx, 'Detalle']

            # Extraer primeras 3 palabras del concepto para la regla
            palabras_concepto = str(concepto).lower().split()[:3]
            patron = ' '.join(palabras_concepto)

            # Agregar regla
            self.clasificador.agregar_regla(
                patron=patron,
                campo='concepto',
                categoria=categoria,
                subcategoria=subcategoria,
                confianza=80  # Confianza inicial para reglas aprendidas
            )

        return df

    def guardar_reglas_aprendidas(self):
        """
        Guarda las reglas aprendidas en el archivo JSON.
        """
        self.clasificador.guardar_reglas()
