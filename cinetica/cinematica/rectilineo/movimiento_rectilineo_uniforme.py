"""
Módulo que implementa el Movimiento Rectilíneo Uniforme (MRU)
"""

from ..base_movimiento import Movimiento

class MovimientoRectilineoUniforme(Movimiento):
    """
    Clase para calcular posición y velocidad en Movimiento Rectilíneo Uniforme (MRU).
    """

    def __init__(self, posicion_inicial: float = 0.0, velocidad_inicial: float = 0.0):
        """
        Inicializa el objeto MovimientoRectilineoUniforme con condiciones iniciales.

        Args:
            posicion_inicial (float): Posición inicial del objeto (m).
            velocidad_inicial (float): Velocidad inicial del objeto (m/s).
        """
        self.posicion_inicial = posicion_inicial
        self.velocidad_inicial = velocidad_inicial

    def posicion(self, tiempo: float) -> float:
        """
        Calcula la posición en MRU.
        Ecuación: x = x0 + v * t

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float: Posición final (m).
        """
        return self.posicion_inicial + self.velocidad_inicial * tiempo

    def velocidad(self, tiempo: float = None) -> float:
        """
        Obtiene la velocidad en MRU.
        En MRU la velocidad es constante.

        Args:
            tiempo (float, optional): Tiempo transcurrido (s). No afecta al resultado.

        Returns:
            float: Velocidad (m/s).
        """
        return self.velocidad_inicial

    def aceleracion(self, tiempo: float = None) -> float:
        """
        Obtiene la aceleración en MRU.
        En MRU la aceleración es siempre 0.

        Args:
            tiempo (float, optional): Tiempo transcurrido (s). No afecta al resultado.

        Returns:
            float: Aceleración (m/s²).
        """
        return 0.0
