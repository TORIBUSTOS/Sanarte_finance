"""
Cargador de reglas externas desde JSON
Sistema TORO · Resumen de Cuentas
Versión: 2.0

Este módulo permite cargar reglas de clasificación desde archivos JSON externos,
facilitando la configuración sin modificar código fuente.
"""
import json
import os
from typing import Dict, List, Tuple


class ReglasLoader:
    """
    Carga reglas de clasificación desde archivos JSON.

    Soporta:
    - Reglas de Nivel 1 (Concepto) desde data/reglas_concepto.json
    - Reglas de Nivel 2 (Refinamiento) desde data/reglas_refinamiento.json
    """

    def __init__(self, ruta_base: str = "./data"):
        """
        Inicializa el cargador de reglas.

        Args:
            ruta_base: Ruta base donde están los archivos JSON
        """
        self.ruta_base = ruta_base
        self.ruta_concepto = os.path.join(ruta_base, "reglas_concepto.json")
        self.ruta_refinamiento = os.path.join(ruta_base, "reglas_refinamiento.json")

    def cargar_reglas_concepto(self) -> Dict[str, str]:
        """
        Carga reglas de Nivel 1 (Concepto) desde JSON.

        Returns:
            Dict[patron_lowercase, categoria_completa]
            Ejemplo: {"crédito por transferencia": "Ingresos - Transferencias"}

        Raises:
            FileNotFoundError: Si no existe el archivo JSON
            json.JSONDecodeError: Si el JSON es inválido
        """
        if not os.path.exists(self.ruta_concepto):
            raise FileNotFoundError(
                f"No se encontró archivo de reglas de concepto: {self.ruta_concepto}"
            )

        with open(self.ruta_concepto, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Convertir lista de reglas a diccionario
        reglas_dict = {}
        reglas_activas = 0

        for regla in data.get('reglas', []):
            if not regla.get('activo', True):
                continue  # Saltar reglas desactivadas

            patron = regla['patron'].lower().strip()
            categoria = regla['categoria']

            # Guardar en diccionario
            reglas_dict[patron] = categoria
            reglas_activas += 1

        print(f"✓ Cargadas {reglas_activas} reglas de concepto (Nivel 1) desde JSON")
        print(f"  Archivo: {os.path.basename(self.ruta_concepto)}")
        print(f"  Versión: {data.get('version', 'N/A')}")

        return reglas_dict

    def cargar_reglas_refinamiento(self) -> Dict[str, Dict]:
        """
        Carga reglas de Nivel 2 (Refinamiento) desde JSON.

        Returns:
            Dict con estructura:
            {
                'categoria_base': {
                    'patrones': [(lista_palabras, categoria_refinada), ...],
                    'default': 'Categoria Default'
                }
            }

        Raises:
            FileNotFoundError: Si no existe el archivo JSON
            json.JSONDecodeError: Si el JSON es inválido
        """
        if not os.path.exists(self.ruta_refinamiento):
            raise FileNotFoundError(
                f"No se encontró archivo de reglas de refinamiento: {self.ruta_refinamiento}"
            )

        with open(self.ruta_refinamiento, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Convertir estructura JSON a formato del clasificador
        reglas_dict = {}
        total_categorias = 0
        total_patrones = 0

        for categoria_base, config in data.get('reglas_refinamiento', {}).items():
            patrones_lista = []

            for patron in config.get('patrones', []):
                if not patron.get('activo', True):
                    continue  # Saltar patrones desactivados

                palabras_clave = patron['palabras_clave']
                categoria_refinada = patron['categoria_refinada']

                # Convertir a tupla (lista_palabras, categoria)
                patrones_lista.append((palabras_clave, categoria_refinada))
                total_patrones += 1

            # Guardar configuración de esta categoría
            reglas_dict[categoria_base] = {
                'patrones': patrones_lista,
                'default': config.get('categoria_default', categoria_base)
            }
            total_categorias += 1

        print(f"✓ Cargadas reglas de refinamiento (Nivel 2) desde JSON")
        print(f"  Archivo: {os.path.basename(self.ruta_refinamiento)}")
        print(f"  Versión: {data.get('version', 'N/A')}")
        print(f"  Categorías refinables: {total_categorias}")
        print(f"  Patrones de refinamiento: {total_patrones}")

        return reglas_dict

    def validar_archivos(self) -> Tuple[bool, List[str]]:
        """
        Valida que los archivos JSON existan y sean válidos.

        Returns:
            Tupla (valido, lista_errores)
        """
        errores = []

        # Validar archivo de concepto
        if not os.path.exists(self.ruta_concepto):
            errores.append(f"Falta archivo: {self.ruta_concepto}")
        else:
            try:
                with open(self.ruta_concepto, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'reglas' not in data:
                        errores.append(f"Archivo {self.ruta_concepto} no tiene campo 'reglas'")
            except json.JSONDecodeError as e:
                errores.append(f"JSON inválido en {self.ruta_concepto}: {e}")

        # Validar archivo de refinamiento
        if not os.path.exists(self.ruta_refinamiento):
            errores.append(f"Falta archivo: {self.ruta_refinamiento}")
        else:
            try:
                with open(self.ruta_refinamiento, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'reglas_refinamiento' not in data:
                        errores.append(
                            f"Archivo {self.ruta_refinamiento} no tiene campo 'reglas_refinamiento'"
                        )
            except json.JSONDecodeError as e:
                errores.append(f"JSON inválido en {self.ruta_refinamiento}: {e}")

        valido = len(errores) == 0
        return valido, errores


# Función de conveniencia para uso directo
def cargar_reglas_desde_json(ruta_base: str = "./data") -> Tuple[Dict, Dict]:
    """
    Carga todas las reglas desde archivos JSON.

    Args:
        ruta_base: Ruta base donde están los JSON

    Returns:
        Tupla (reglas_concepto, reglas_refinamiento)

    Raises:
        FileNotFoundError: Si faltan archivos
        json.JSONDecodeError: Si hay errores en JSON
    """
    loader = ReglasLoader(ruta_base)

    # Validar primero
    valido, errores = loader.validar_archivos()
    if not valido:
        raise FileNotFoundError(
            f"Errores al cargar reglas:\n" + "\n".join(f"  - {e}" for e in errores)
        )

    # Cargar reglas
    reglas_concepto = loader.cargar_reglas_concepto()
    reglas_refinamiento = loader.cargar_reglas_refinamiento()

    return reglas_concepto, reglas_refinamiento
