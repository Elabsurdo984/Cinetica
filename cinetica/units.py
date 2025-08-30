"""
Módulo para la gestión centralizada de unidades con Pint.
"""

import pint

# Crear un registro de unidades global para la librería
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity # Alias para facilitar la creación de cantidades
