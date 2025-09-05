"""
Módulo para el Movimiento Armónico Complejo (MAC).

Este módulo define clases y funciones para simular y analizar el movimiento
armónico complejo, que es la superposición de varios movimientos armónicos simples.
"""

import numpy as np
from ..base_movimiento import Movimiento

class MovimientoArmonicoComplejo(Movimiento):
    """
    Representa un Movimiento Armónico Complejo (MAC) como la superposición
    de múltiples Movimientos Armónicos Simples (MAS).
    """
    def __init__(self, mas_components):
        """
        Inicializa un objeto de Movimiento Armónico Complejo.

        Args:
            mas_components (list): Una lista de diccionarios, donde cada diccionario
                                   representa un MAS con las siguientes claves:
                                   - 'amplitud' (float): Amplitud del MAS.
                                   - 'frecuencia_angular' (float): Frecuencia angular (omega) del MAS.
                                   - 'fase_inicial' (float): Fase inicial (phi) del MAS en radianes.
        """
        if not isinstance(mas_components, list) or not mas_components:
            raise ValueError("mas_components debe ser una lista no vacía de diccionarios.")
        
        for comp in mas_components:
            if not all(k in comp for k in ['amplitud', 'frecuencia_angular', 'fase_inicial']):
                raise ValueError("Cada componente MAS debe tener 'amplitud', 'frecuencia_angular' y 'fase_inicial'.")
            if not all(isinstance(comp[k], (int, float)) for k in ['amplitud', 'frecuencia_angular', 'fase_inicial']):
                raise ValueError("Los valores de amplitud, frecuencia_angular y fase_inicial deben ser numéricos.")

        self.mas_components = mas_components

    def posicion(self, tiempo):
        """
        Calcula la posición del objeto en un tiempo dado para el MAC.

        Args:
            tiempo (float or np.ndarray): El tiempo o array de tiempos en segundos.

        Returns:
            float or np.ndarray: La posición total en el tiempo especificado.
        """
        posiciones = np.zeros_like(np.array(tiempo, dtype=float))
        for comp in self.mas_components:
            A = comp['amplitud']
            omega = comp['frecuencia_angular']
            phi = comp['fase_inicial']
            posiciones += A * np.cos(omega * tiempo + phi)
        posicion_total = 0.0
        for comp in self.mas_components:
            A = comp['amplitud']
            omega = comp['frecuencia_angular']
            phi = comp['fase_inicial']
            posicion_total += A * np.cos(omega * tiempo + phi)
        return posicion_total

    def velocidad(self, tiempo: float) -> float:
        """
        Calcula la velocidad del objeto en un tiempo dado para el MAC.

        Args:
            tiempo (float): El tiempo en segundos.

        Returns:
            float: La velocidad total en el tiempo especificado.
        """
        velocidad_total = 0.0
        for comp in self.mas_components:
            A = comp['amplitud']
            omega = comp['frecuencia_angular']
            phi = comp['fase_inicial']
            velocidad_total += -A * omega * np.sin(omega * tiempo + phi)
        return velocidad_total

    def aceleracion(self, tiempo: float) -> float:
        """
        Calcula la aceleración del objeto en un tiempo dado para el MAC.

        Args:
            tiempo (float): El tiempo en segundos.

        Returns:
            float: La aceleración total en el tiempo especificado.
        """
        aceleracion_total = 0.0
        for comp in self.mas_components:
            A = comp['amplitud']
            omega = comp['frecuencia_angular']
            phi = comp['fase_inicial']
            aceleracion_total += -A * (omega**2) * np.cos(omega * tiempo + phi)
        return aceleracion_total
