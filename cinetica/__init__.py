"""
Cinetica - Una librería para cálculos de cinemática
"""

__version__ = "0.19.0"  # Versión actualizada por la nueva funcionalidad

from .units import ureg, Q_
from .logger import setup_logger, get_logger

from .cinematica import (
    circular,
    espacial,
    oscilatorio,
    parabolico,
    rectilineo,
    relativo,
)
from . import graficos
from . import dinamica

# Configurar logger raíz por defecto
logger = setup_logger('cinetica')

__all__ = [
    "circular",
    "espacial",
    "oscilatorio",
    "parabolico",
    "rectilineo",
    "relativo",
    "graficos",
    "dinamica",
    "setup_logger",
    "get_logger",
    "logger",
    "__version__",
]
