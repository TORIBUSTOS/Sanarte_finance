"""
Motor de clasificación de movimientos bancarios
Autor: Sistema SANARTE
"""
import json
import os
from typing import Optional, Tuple, Dict, List
import pandas as pd

class Clasificador:
    """
    Clasifica movimientos bancarios según reglas predefinidas y aprendidas.
    """

    def __init__(self, ruta_reglas: str = "./data/reglas.json"):
        self.ruta_reglas = ruta_reglas
        self.reglas = []
        self.categorias = {}
        self.cargar_reglas()

    def cargar_reglas(self):
        """
        Carga reglas desde el archivo JSON.
        """
        try:
            if not os.path.exists(self.ruta_reglas):
                print(f"Advertencia: No se encontro archivo de reglas en {self.ruta_reglas}")
                self.reglas = []
                self.categorias = {}
                return

            with open(self.ruta_reglas, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.reglas = data.get('reglas', [])
            self.categorias = data.get('categorias', {})

            print(f"OK Cargadas {len(self.reglas)} reglas de clasificacion")

        except Exception as e:
            print(f"Error al cargar reglas: {e}")
            self.reglas = []
            self.categorias = {}

    def guardar_reglas(self):
        """
        Guarda las reglas actuales en el archivo JSON.
        """
        try:
            data = {
                "version": "1.0",
                "fecha_actualizacion": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "categorias": self.categorias,
                "reglas": self.reglas
            }

            with open(self.ruta_reglas, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"OK Reglas guardadas en {self.ruta_reglas}")

        except Exception as e:
            print(f"Error al guardar reglas: {e}")

    def clasificar_movimiento(self, concepto: str, detalle: str,
                             debito: float, credito: float) -> Tuple[str, str, int]:
        """
        Clasifica un movimiento individual según las reglas.

        Args:
            concepto: Concepto del movimiento
            detalle: Detalle del movimiento
            debito: Monto debitado
            credito: Monto acreditado

        Returns:
            Tupla (categoria, subcategoria, confianza)
            Si no se puede clasificar: (None, None, 0)
        """
        # Convertir a string y manejar NaN
        concepto_str = str(concepto) if pd.notna(concepto) else ''
        detalle_str = str(detalle) if pd.notna(detalle) else ''

        concepto_lower = concepto_str.lower()
        detalle_lower = detalle_str.lower()
        monto = debito if debito > 0 else credito

        mejor_match = None
        mejor_confianza = 0

        # Evaluar cada regla
        for regla in self.reglas:
            patron = regla['patron'].lower()
            campo = regla['campo']
            confianza_base = regla.get('confianza', 50)

            # Seleccionar el campo a evaluar
            if campo == 'concepto':
                texto = concepto_lower
            elif campo == 'detalle':
                texto = detalle_lower
            else:
                texto = f"{concepto_lower} {detalle_lower}"

            # Verificar si el patrón coincide
            if patron in texto:
                # Verificar condición de monto mínimo si existe
                monto_minimo = regla.get('monto_minimo', 0)
                if monto >= monto_minimo:
                    # Este patrón coincide
                    if confianza_base > mejor_confianza:
                        mejor_confianza = confianza_base
                        mejor_match = {
                            'categoria': regla['categoria'],
                            'subcategoria': regla['subcategoria'],
                            'confianza': confianza_base
                        }

        if mejor_match:
            return (mejor_match['categoria'],
                   mejor_match['subcategoria'],
                   mejor_match['confianza'])

        # No se encontró clasificación
        return (None, None, 0)

    def agregar_regla(self, patron: str, campo: str, categoria: str,
                     subcategoria: str, confianza: int = 70):
        """
        Agrega una nueva regla al sistema de aprendizaje.

        Args:
            patron: Texto a buscar (se convertirá a minúsculas)
            campo: Campo donde buscar ('concepto', 'detalle', 'ambos')
            categoria: Categoría principal
            subcategoria: Subcategoría
            confianza: Nivel de confianza (0-100)
        """
        # Verificar si ya existe una regla similar
        patron_lower = patron.lower()

        for regla in self.reglas:
            if regla['patron'].lower() == patron_lower and regla['campo'] == campo:
                # Actualizar confianza si ya existe
                regla['confianza'] = min(100, regla['confianza'] + 5)
                regla['categoria'] = categoria
                regla['subcategoria'] = subcategoria
                print(f"  Regla actualizada: '{patron}' (confianza: {regla['confianza']}%)")
                return

        # Agregar nueva regla
        nueva_regla = {
            "patron": patron_lower,
            "campo": campo,
            "categoria": categoria,
            "subcategoria": subcategoria,
            "confianza": confianza,
            "descripcion": f"Aprendida: {patron}"
        }

        self.reglas.append(nueva_regla)
        print(f"  Nueva regla agregada: '{patron}' -> {categoria}/{subcategoria}")

    def obtener_categorias(self) -> Dict[str, List[str]]:
        """
        Retorna el diccionario de categorías disponibles.

        Returns:
            Diccionario {categoria: [subcategorias]}
        """
        resultado = {}
        for cat, data in self.categorias.items():
            resultado[cat] = data.get('subcategorias', [])

        return resultado
