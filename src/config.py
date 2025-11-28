"""
Configuración Centralizada - TORO · Resumen de Cuentas
======================================================

Gestión unificada de rutas, configuraciones y constantes del sistema.

Sistema: TORO (anteriormente SANARTE)
Versión: 1.2
"""
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PathsConfig:
    """
    Configuración de rutas del sistema.

    Attributes:
        input_dir: Directorio de archivos de entrada (extractos bancarios)
        output_dir: Directorio de salida (consolidados, categorizados, reportes)
        data_dir: Directorio de datos del sistema (reglas, configuraciones)
    """
    input_dir: str = "./input"
    output_dir: str = "./output"
    data_dir: str = "./data"

    def __post_init__(self):
        """Convierte rutas a Path para mejor manejo."""
        self.input_path = Path(self.input_dir)
        self.output_path = Path(self.output_dir)
        self.data_path = Path(self.data_dir)

    def crear_directorios(self):
        """Crea los directorios si no existen."""
        self.input_path.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.data_path.mkdir(parents=True, exist_ok=True)


@dataclass
class ClasificadorConfig:
    """
    Configuración del motor de clasificación.

    Attributes:
        reglas_concepto_file: Archivo JSON con reglas de nivel 1 (concepto)
        reglas_refinamiento_file: Archivo JSON con reglas de nivel 2 (detalle)
        usar_reglas_externas: Si True, cargar reglas desde JSON (futuro)
    """
    reglas_concepto_file: str = "reglas_concepto.json"
    reglas_refinamiento_file: str = "reglas_refinamiento.json"
    usar_reglas_externas: bool = False  # Futuro: migración a JSON

    def get_reglas_concepto_path(self, data_dir: str = "./data") -> Path:
        """Retorna Path completo al archivo de reglas de concepto."""
        return Path(data_dir) / self.reglas_concepto_file

    def get_reglas_refinamiento_path(self, data_dir: str = "./data") -> Path:
        """Retorna Path completo al archivo de reglas de refinamiento."""
        return Path(data_dir) / self.reglas_refinamiento_file


@dataclass
class SystemConfig:
    """
    Configuración general del sistema.

    Attributes:
        app_name: Nombre de la aplicación
        version: Versión del sistema
        autor: Autor del sistema
    """
    app_name: str = "TORO · Resumen de Cuentas"
    version: str = "1.2"
    autor: str = "Sistema TORO"


class AppConfig:
    """
    Configuración unificada de la aplicación TORO.

    Provee acceso centralizado a todas las configuraciones del sistema.

    Uso:
        from src.config import AppConfig

        config = AppConfig()
        input_dir = config.paths.input_dir
        output_dir = config.paths.output_dir
    """

    def __init__(self):
        self.paths = PathsConfig()
        self.clasificador = ClasificadorConfig()
        self.system = SystemConfig()

    def inicializar_entorno(self):
        """
        Inicializa el entorno de trabajo.
        Crea directorios necesarios si no existen.
        """
        self.paths.crear_directorios()
        print(f"✓ Entorno inicializado: {self.system.app_name} v{self.system.version}")
        print(f"  - Input: {self.paths.input_dir}")
        print(f"  - Output: {self.paths.output_dir}")
        print(f"  - Data: {self.paths.data_dir}")


# Instancia global de configuración (singleton pattern)
_app_config = None


def get_config() -> AppConfig:
    """
    Obtiene la instancia única de configuración de la aplicación.

    Returns:
        AppConfig: Instancia singleton de configuración

    Uso:
        from src.config import get_config

        config = get_config()
        print(config.paths.input_dir)
    """
    global _app_config
    if _app_config is None:
        _app_config = AppConfig()
    return _app_config
