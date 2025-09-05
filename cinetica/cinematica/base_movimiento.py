from abc import ABC, abstractmethod
import numpy as np

class Movimiento(ABC):
    """
    Clase base abstracta para diferentes tipos de movimiento.
    Define una interfaz común para la posición, velocidad y aceleración.
    """

    @abstractmethod
    def posicion(self, tiempo: float):
        """
        Calcula la posición del objeto en un tiempo dado.
        Debe ser implementado por las subclases.
        """
        pass

    @abstractmethod
    def velocidad(self, tiempo: float):
        """
        Calcula la velocidad del objeto en un tiempo dado.
        Debe ser implementado por las subclases.
        """
        pass

    @abstractmethod
    def aceleracion(self, tiempo: float):
        """
        Calcula la aceleración del objeto en un tiempo dado.
        Debe ser implementado por las subclases.
        """
        pass
