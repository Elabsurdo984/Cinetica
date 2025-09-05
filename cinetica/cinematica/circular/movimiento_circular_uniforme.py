import math
import numpy as np
from ..base_movimiento import Movimiento
# from ..graficos.graficador import plot_mcu # This will be handled by a separate Graficador class

class MovimientoCircularUniforme(Movimiento):
    """
    Clase para calcular y simular Movimiento Circular Uniforme (MCU).
    """

    def __init__(self, radio: float, posicion_angular_inicial: float = 0.0, velocidad_angular_inicial: float = 0.0):
        """
        Inicializa el objeto MovimientoCircularUniforme con las condiciones iniciales.

        Args:
            radio (float): Radio de la trayectoria circular (m).
            posicion_angular_inicial (float): Posición angular inicial (radianes).
            velocidad_angular_inicial (float): Velocidad angular inicial (rad/s).
        
        Raises:
            ValueError: Si el radio es menor o igual a cero.
        """
        if radio <= 0:
            raise ValueError("El radio debe ser un valor positivo.")

        self.radio = radio
        self.posicion_angular_inicial = posicion_angular_inicial
        self.velocidad_angular_inicial = velocidad_angular_inicial

    def posicion_angular(self, tiempo: float) -> float:
        """
        Calcula la posición angular en MCU.
        Ecuación: theta = theta0 + omega * t

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float: Posición angular final (radianes).
        
        Raises:
            ValueError: Si el tiempo es negativo.
        """
        if tiempo < 0:
            raise ValueError("El tiempo no puede ser negativo.")
        return self.posicion_angular_inicial + self.velocidad_angular_inicial * tiempo

    def posicion(self, tiempo: float) -> np.ndarray:
        """
        Calcula la posición (x, y) del objeto en un tiempo dado.

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            np.ndarray: Vector de posición [x, y] (m).
        """
        if tiempo < 0:
            raise ValueError("El tiempo no puede ser negativo.")
        theta = self.posicion_angular(tiempo)
        x = self.radio * math.cos(theta)
        y = self.radio * math.sin(theta)
        return np.array([x, y])

    def velocidad(self, tiempo: float) -> np.ndarray:
        """
        Calcula la velocidad (vx, vy) del objeto en un tiempo dado.

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            np.ndarray: Vector de velocidad [vx, vy] (m/s).
        """
        if tiempo < 0:
            raise ValueError("El tiempo no puede ser negativo.")
        omega = self.velocidad_angular_inicial
        theta = self.posicion_angular(tiempo)
        vx = -omega * self.radio * math.sin(theta)
        vy = omega * self.radio * math.cos(theta)
        return np.array([vx, vy])

    def aceleracion(self, tiempo: float) -> np.ndarray:
        """
        Calcula la aceleración (ax, ay) del objeto en un tiempo dado (aceleración centrípeta).

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            np.ndarray: Vector de aceleración [ax, ay] (m/s^2).
        """
        if tiempo < 0:
            raise ValueError("El tiempo no puede ser negativo.")
        omega = self.velocidad_angular_inicial
        theta = self.posicion_angular(tiempo)
        ac = (omega ** 2) * self.radio
        ax = -ac * math.cos(theta)
        ay = -ac * math.sin(theta)
        return np.array([ax, ay])

    def velocidad_angular_constante(self) -> float:
        """
        Retorna la velocidad angular constante en MCU.
        """
        return self.velocidad_angular_inicial

    def aceleracion_centripeta_constante(self) -> float:
        """
        Retorna la magnitud de la aceleración centrípeta constante en MCU.
        """
        return (self.velocidad_angular_inicial ** 2) * self.radio

    def periodo(self) -> float:
        """
        Calcula el período en MCU.
        Ecuación: T = 2 * pi / omega

        Returns:
            float: Período (s).
        
        Notes:
            Retorna `math.inf` si la velocidad angular inicial es cero.
        """
        if self.velocidad_angular_inicial == 0:
            return math.inf  # Período infinito si la velocidad angular es cero
        return (2 * math.pi) / self.velocidad_angular_inicial

    def frecuencia(self) -> float:
        """
        Calcula la frecuencia en MCU.
        Ecuación: f = 1 / T = omega / (2 * pi)

        Returns:
            float: Frecuencia (Hz).
        
        Notes:
            Retorna `0.0` si la velocidad angular inicial es cero.
        """
        if self.velocidad_angular_inicial == 0:
            return 0.0  # Frecuencia cero si la velocidad angular es cero
        return self.velocidad_angular_inicial / (2 * math.pi)
