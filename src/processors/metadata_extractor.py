"""
Extractor de metadata de movimientos bancarios
Autor: Sistema SANARTE
"""
import re
from typing import Optional, Dict

class MetadataExtractor:
    """
    Extrae información relevante de los detalles de movimientos:
    - Nombres de personas
    - Documentos (CUIT/CUIL/DNI)
    - IDs de DEBIN
    """

    def __init__(self):
        # Patrones regex para detección
        self.patron_documento = re.compile(r'(?:DOCUMENTO|CUIT|CUIL):\s*(\d{8,11})', re.IGNORECASE)
        self.patron_debin = re.compile(r'ID_DEBIN:\s*(\d+)', re.IGNORECASE)
        self.patron_tipo_debin = re.compile(r'TIPO_DEBIN:\s*(\d+)', re.IGNORECASE)

        # Patrón para nombres (palabras capitalizadas seguidas)
        # Busca 2-4 palabras capitalizadas consecutivas (ej: HECTOR GASTON OLMEDO)
        self.patron_nombre = re.compile(r'\b([A-Z][A-Z\s]{2,50})\b')

    def extraer_documento(self, texto: str) -> Optional[str]:
        """
        Extrae número de documento (CUIT/CUIL/DNI) del texto.

        Args:
            texto: Texto donde buscar

        Returns:
            Número de documento o None
        """
        if not texto or pd.isna(texto):
            return None

        match = self.patron_documento.search(str(texto))
        if match:
            return match.group(1)

        return None

    def extraer_debin_id(self, texto: str) -> Optional[str]:
        """
        Extrae ID de DEBIN del texto.

        Args:
            texto: Texto donde buscar

        Returns:
            ID de DEBIN o None
        """
        if not texto or pd.isna(texto):
            return None

        match = self.patron_debin.search(str(texto))
        if match:
            return match.group(1)

        return None

    def es_debin(self, concepto: str, detalle: str) -> bool:
        """
        Determina si un movimiento es un DEBIN.

        Args:
            concepto: Concepto del movimiento
            detalle: Detalle del movimiento

        Returns:
            True si es DEBIN, False en caso contrario
        """
        texto_completo = f"{concepto or ''} {detalle or ''}".lower()

        # Buscar indicadores de DEBIN
        indicadores = ['debin', 'tipo_debin', 'id_debin']

        return any(ind in texto_completo for ind in indicadores)

    def extraer_nombre(self, texto: str) -> Optional[str]:
        """
        Extrae nombre de persona del texto.
        Busca palabras en mayúsculas que probablemente sean un nombre.

        Args:
            texto: Texto donde buscar

        Returns:
            Nombre extraído o None
        """
        if not texto or pd.isna(texto):
            return None

        texto_str = str(texto)

        # Buscar patrones específicos como "NOMBRE APELLIDO DOCUMENTO:"
        # Extraer lo que está antes de DOCUMENTO/CUIT/CUIL
        match_antes_doc = re.search(r'([A-Z\s]{5,50})\s+(?:DOCUMENTO|CUIT|CUIL):', texto_str)
        if match_antes_doc:
            nombre = match_antes_doc.group(1).strip()
            # Limpiar espacios múltiples
            nombre = re.sub(r'\s+', ' ', nombre)
            if len(nombre) > 5:  # Al menos 5 caracteres para ser un nombre válido
                return nombre

        # Buscar nombres en general (2-4 palabras capitalizadas)
        matches = self.patron_nombre.findall(texto_str)
        if matches:
            for match in matches:
                # Filtrar palabras comunes que no son nombres
                palabras_excluir = {'TRANSFERENCIA', 'CREDITO', 'DEBITO', 'DOCUMENTO', 'CUIT',
                                   'CUIL', 'BANCO', 'SANARTE', 'SRL', 'SA', 'PROCESAMIENTO',
                                   'NOMINA', 'PAGO', 'COMPRA', 'SERVICIO'}

                palabras = match.split()
                if len(palabras) >= 2 and not any(p in palabras_excluir for p in palabras):
                    nombre = ' '.join(palabras)
                    if len(nombre) > 5:
                        return nombre

        return None

    def extraer_metadata(self, concepto: str, detalle: str) -> Dict[str, any]:
        """
        Extrae toda la metadata relevante de un movimiento.

        Args:
            concepto: Concepto del movimiento
            detalle: Detalle del movimiento

        Returns:
            Diccionario con metadata extraída
        """
        texto_completo = f"{concepto or ''} {detalle or ''}"

        metadata = {
            'persona_nombre': self.extraer_nombre(detalle),
            'documento': self.extraer_documento(detalle),
            'es_debin': self.es_debin(concepto, detalle),
            'debin_id': self.extraer_debin_id(detalle)
        }

        return metadata


# Importar pandas para validaciones
import pandas as pd
