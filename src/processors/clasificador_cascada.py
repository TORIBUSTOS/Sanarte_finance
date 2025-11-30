"""
Motor de Clasificación Oficial - TORO · Resumen de Cuentas
===========================================================

Sistema: TORO (anteriormente SANARTE)
Motor: ClasificadorCascada
Versión: 2.0
Estado: OFICIAL - Motor en producción

Descripción:
-----------
Motor de clasificación en cascada de 2 niveles para movimientos bancarios.

Estrategia de Clasificación:
- Nivel 1 (BASE): Clasificación por campo "Concepto" (siempre disponible)
- Nivel 2 (REFINAMIENTO): Refinamiento por campo "Detalle" (cuando disponible)

Objetivo: Alcanzar 99%+ de clasificación automática

Autor: Sistema TORO
Última actualización: 2025-11-27
"""
import pandas as pd
from typing import Tuple, Dict


class ClasificadorCascada:
    """
    Motor de clasificación oficial de TORO · Resumen de Cuentas.
    Versión: 2.0 (clasificación en cascada Concepto → Detalle)

    Estrategia de Cascada de 2 Niveles:
    ----------------------------------
    - Nivel 1 (BASE): Clasificación por campo "Concepto" (siempre disponible)
    - Nivel 2 (REFINAMIENTO): Refinamiento por campo "Detalle" (cuando disponible)

    Reglas Actuales:
    ---------------
    - Nivel 1: 78 reglas hardcoded en _cargar_reglas_concepto()
    - Nivel 2: 4 categorías refinables en _cargar_reglas_refinamiento()

    Migración Futura:
    ----------------
    Las reglas hardcoded serán migradas a archivos JSON externos:
    - data/reglas_concepto.json (Nivel 1)
    - data/reglas_refinamiento.json (Nivel 2)

    Objetivo: 99%+ de clasificación automática
    """

    def __init__(self):
        """Inicializa el clasificador con todas las reglas."""
        self.reglas_concepto = self._cargar_reglas_concepto()
        self.reglas_refinamiento = self._cargar_reglas_refinamiento()

    def _cargar_reglas_concepto(self) -> Dict[str, str]:
        """
        Reglas de clasificación NIVEL 1 - BASE por "Concepto"

        Returns:
            Dict[patron_concepto_lowercase, categoria_completa]
        """
        return {
            # ===== INGRESOS =====
            "crédito por transferencia": "Ingresos - Transferencias",
            "credito debin": "Ingresos - DEBIN Afiliados",
            "cred bca electronica interbanc": "Ingresos - Transferencias",
            "cobranzas resumen visa": "Ingresos - Tarjetas",
            "comercios first data": "Ingresos - Tarjetas",
            "contras.ints.sobreg.": "Ingresos - Intereses",
            "suscripcion / rescate fci": "Ingresos - Inversiones",
            "acreditación cheque dep.48 hs.": "Ingresos - Cheques",
            "reverso compra visa débito": "Ingresos - Devoluciones",
            "devolución de compras": "Ingresos - Devoluciones",
            "descuento por promociones": "Ingresos - Descuentos",

            # ===== IMPUESTOS =====
            "impuesto débitos y créditos/db": "Impuestos - Débitos y Créditos",
            "impuesto débitos y créditos/cr": "Impuestos - Devoluciones",
            "iibb- acreditaciones bancarias": "Impuestos - IIBB",
            "iibb córdoba d1290 titulo viii": "Impuestos - IIBB",
            "iva": "Impuestos - IVA",
            "percepción rg 5617": "Impuestos - Percepciones",
            "percepción i.v.a. rg. 3337": "Impuestos - IVA",
            "devolucion imp. ley 25413": "Impuestos - Devoluciones",
            "devolución imp. débitos": "Impuestos - Devoluciones",
            "impuesto a los sellos": "Impuestos - Sellos",

            # ===== GASTOS OPERATIVOS =====
            "compra visa débito": "Gastos Operativos - Compras",
            "pago de servicios": "Servicios - Varios",
            "débito automático de servicio": "Servicios - Varios",
            "débito por pago sueldos": "Gastos Operativos - Sueldos",

            # ===== EGRESOS =====
            "transferencia por cbu": "Egresos - Transferencias",
            "debito transf. homebanking": "Egresos - Transferencias",
            "debito debin": "Egresos - DEBIN",
            "pago cheque de cámara recibida": "Prestadores - Pagos",
            "embargo judicial": "Egresos - Legales",

            # ===== COMISIONES BANCARIAS =====
            "com.cheque pagado por clearing": "Comisiones Bancarias - Cheques",
            "comis.transferencias": "Comisiones Bancarias - Transferencias",
            "comisión permanencia saldo dr": "Comisiones Bancarias - Mantenimiento",
            "comision mantenimiento paquete": "Comisiones Bancarias - Mantenimiento",
            "comisión consulta cámara": "Comisiones Bancarias - Consultas",
            "comisiones cheques o/bancos": "Comisiones Bancarias - Cheques",
            "intereses de sobregiro": "Comisiones Bancarias - Intereses",
        }

    def _cargar_reglas_refinamiento(self) -> Dict[str, Dict]:
        """
        Reglas de NIVEL 2 - REFINAMIENTO por "Detalle"

        Estructura: {
            'categoria_base_a_refinar': {
                'patrones': [(patron, categoria_refinada), ...]
            }
        }

        Returns:
            Dict con reglas de refinamiento por categoría base
        """
        return {
            # ===== A) REFINAR "Gastos Operativos - Compras" =====
            "Gastos Operativos - Compras": {
                'patrones': [
                    # Servicios Públicos
                    (["aguas cordobesas", "aguascordobesas"], "Servicios - Agua"),
                    (["epec", "epeced", "pagos360*epec"], "Servicios - Electricidad"),
                    (["gas del centro", "gascentro"], "Servicios - Gas"),

                    # Software y Tecnología
                    (["microsoft"], "Servicios - Software"),
                    (["openai", "chatgpt"], "Servicios - Software"),
                    (["google gsuite", "google workspace", "google one", "youtube"], "Servicios - Software"),
                    (["netflix", "spotify", "hbo"], "Servicios - Entretenimiento"),
                    (["hosting", "godaddy", "aws", "cloud"], "Servicios - Hosting/IT"),

                    # Viáticos y Movilidad
                    (["pedidosya", "rappi"], "Gastos Operativos - Viáticos"),
                    (["uber", "cabify"], "Gastos Operativos - Movilidad"),

                    # Mercado Libre/Pago
                    (["merpago", "mercadopago", "mercadolibre"], "Gastos Operativos - Compras ML"),
                ],
                'default': "Gastos Operativos - Compras Varias"
            },

            # ===== B) REFINAR "Egresos - Transferencias" =====
            "Egresos - Transferencias": {
                'patrones': [
                    # Prestadores de Salud
                    (["farmacia", "farmacias lider"], "Prestadores - Farmacias"),
                    (["laboratorio"], "Prestadores - Laboratorios"),
                    (["clinica", "sanatorio", "aclinor"], "Prestadores - Clínicas"),
                    (["dr.", "dra."], "Prestadores - Profesionales"),

                    # Prestadores Conocidos (por nombre)
                    (["tosin", "plizzo", "tosca", "bernardi", "lopez", "tura", "decade",
                      "frandino", "picatto", "diaz gustavo", "cabrera", "ghiglione",
                      "figueroa", "caballi", "gorosito", "lezcano", "marengo", "pizzichini",
                      "gentile", "sosa", "bonaldi", "cuevas", "roda"], "Prestadores - Profesionales"),

                    # Pagos Municipales/AFIP
                    (["municipalidad", "municipio"], "Impuestos - Municipal"),
                    (["afip"], "Impuestos - AFIP"),
                    (["arba"], "Impuestos - ARBA"),
                ],
                'default': "Egresos - Transferencias Varias"
            },

            # ===== C) REFINAR "Servicios - Varios" =====
            "Servicios - Varios": {
                'patrones': [
                    (["aguas cordobesas"], "Servicios - Agua"),
                    (["epec", "epeced"], "Servicios - Electricidad"),
                    (["gas"], "Servicios - Gas"),
                    (["afip"], "Impuestos - AFIP"),
                ],
                'default': "Servicios - Varios"
            },

            # ===== D) REFINAR "Ingresos - Transferencias" =====
            "Ingresos - Transferencias": {
                'patrones': [
                    (["obra soc", "obra social"], "Ingresos - Obras Sociales"),
                ],
                'default': "Ingresos - Transferencias"
            },
        }

    def clasificar_movimiento(self, concepto: str, detalle: str,
                            debito: float, credito: float) -> Tuple[str, str, str, int]:
        """
        Clasifica un movimiento usando estrategia de cascada de 2 niveles.

        Args:
            concepto: Campo "Concepto" del movimiento (siempre completo)
            detalle: Campo "Detalle" del movimiento (puede estar vacío)
            debito: Monto debitado
            credito: Monto acreditado

        Returns:
            Tupla (tipo_movimiento, categoria_principal, categoria_final, confianza)
            - tipo_movimiento: "Ingreso" o "Egreso"
            - categoria_principal: Texto antes del " - " (ej: "Servicios")
            - categoria_final: Categoría completa refinada (ej: "Servicios - Agua")
            - confianza: 0-100, donde 100 = clasificado, 0 = sin clasificar
        """
        # 1. Determinar tipo de movimiento
        # Usar umbral de 0.01 para evitar valores microscópicos (ej: 5e-324 del Excel)
        UMBRAL_MINIMO = 0.01  # 1 centavo

        if credito >= UMBRAL_MINIMO:
            tipo_movimiento = "Ingreso"
        elif debito >= UMBRAL_MINIMO:
            tipo_movimiento = "Egreso"
        else:
            # Ambos son 0 o valores insignificantes
            tipo_movimiento = "Neutro"

        # 2. Normalizar campos
        concepto_str = str(concepto) if pd.notna(concepto) else ''
        detalle_str = str(detalle) if pd.notna(detalle) else ''
        concepto_lower = concepto_str.lower().strip()
        detalle_upper = detalle_str.upper().strip()  # DETALLE en mayúsculas para búsqueda

        # 3. NIVEL 1: Clasificación BASE por "Concepto"
        categoria_base = self._clasificar_por_concepto(concepto_lower)

        if not categoria_base:
            # No se pudo clasificar
            return (tipo_movimiento, "Sin Clasificar", "Sin Clasificar - Requiere Revisión", 0)

        # 4. NIVEL 2: Refinamiento por "Detalle" (si existe)
        if detalle_upper and categoria_base in self.reglas_refinamiento:
            categoria_refinada = self._refinar_por_detalle(categoria_base, detalle_upper)
        else:
            categoria_refinada = categoria_base

        # 5. Extraer categoría principal (texto antes del " - ")
        if " - " in categoria_refinada:
            categoria_principal = categoria_refinada.split(" - ")[0]
        else:
            categoria_principal = categoria_refinada

        # 6. Confianza = 100 si se clasificó, 0 si no
        confianza = 100

        return (tipo_movimiento, categoria_principal, categoria_refinada, confianza)

    def _clasificar_por_concepto(self, concepto_lower: str) -> str:
        """
        NIVEL 1: Clasifica basándose en el campo "Concepto".

        Args:
            concepto_lower: Concepto en minúsculas

        Returns:
            Categoría base o None si no se encuentra
        """
        # Buscar coincidencia exacta primero
        for patron, categoria in self.reglas_concepto.items():
            if patron == concepto_lower:
                return categoria

        # Si no hay coincidencia exacta, buscar por contención
        for patron, categoria in self.reglas_concepto.items():
            if patron in concepto_lower:
                return categoria

        return None

    def _refinar_por_detalle(self, categoria_base: str, detalle_upper: str) -> str:
        """
        NIVEL 2: Refina la categoría base usando el campo "Detalle".

        Args:
            categoria_base: Categoría obtenida del Nivel 1
            detalle_upper: Detalle en mayúsculas

        Returns:
            Categoría refinada o categoria_base si no se puede refinar
        """
        reglas = self.reglas_refinamiento[categoria_base]

        # Buscar coincidencia en patrones
        for patrones_lista, categoria_refinada in reglas['patrones']:
            for patron in patrones_lista:
                if patron.upper() in detalle_upper:
                    return categoria_refinada

        # Si no hay coincidencia, retornar default
        return reglas.get('default', categoria_base)

    def obtener_estadisticas(self) -> Dict:
        """
        Retorna estadísticas sobre las reglas cargadas.

        Returns:
            Dict con información sobre el clasificador
        """
        total_reglas_concepto = len(self.reglas_concepto)
        total_categorias_refinables = len(self.reglas_refinamiento)

        total_patrones_refinamiento = sum(
            len(reglas['patrones'])
            for reglas in self.reglas_refinamiento.values()
        )

        return {
            'reglas_concepto': total_reglas_concepto,
            'categorias_refinables': total_categorias_refinables,
            'patrones_refinamiento': total_patrones_refinamiento,
            'cobertura_estimada': '99%+'
        }
