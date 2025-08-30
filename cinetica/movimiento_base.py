"""
Módulo para definir la clase base abstracta para los movimientos cinemáticos.
"""

from abc import ABC, abstractmethod

class MovimientoBase(ABC):
    """
    Clase base abstracta para todos los tipos de movimiento cinemático.
    Define una interfaz común para calcular posición, velocidad y aceleración.
    """

    @abstractmethod
    def posicion(self, tiempo: float):
        """
        Calcula la posición del objeto en un tiempo dado.
        Debe ser implementado por las subclases.

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float or tuple: La posición del objeto. El tipo de retorno puede variar
                            (float para 1D, tuple para 2D/3D).
        """
        pass

    @abstractmethod
    def velocidad(self, tiempo: float):
        """
        Calcula la velocidad del objeto en un tiempo dado.
        Debe ser implementado por las subclases.

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float or tuple: La velocidad del objeto. El tipo de retorno puede variar
                            (float para 1D, tuple para 2D/3D).
        """
        pass

    @abstractmethod
    def aceleracion(self, tiempo: float):
        """
        Calcula la aceleración del objeto en un tiempo dado.
        Debe ser implementado por las subclases.

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float or tuple: La aceleración del objeto. El tipo de retorno puede variar
                            (float para 1D, tuple para 2D/3D).
        """
        pass
