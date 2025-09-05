import math
import numpy as np
from ..base_movimiento import Movimiento

class MovimientoCircularUniformementeVariado(Movimiento):
    """
    Clase para calcular y simular Movimiento Circular Uniformemente Variado (MCUV).
    """

    def __init__(self, radio: float, posicion_angular_inicial: float = 0.0,
                 velocidad_angular_inicial: float = 0.0, aceleracion_angular_inicial: float = 0.0):
        """
        Inicializa el objeto MovimientoCircularUniformementeVariado con las condiciones iniciales.

        Args:
            radio (float): Radio de la trayectoria circular (m).
            posicion_angular_inicial (float): Posición angular inicial (radianes).
            velocidad_angular_inicial (float): Velocidad angular inicial (rad/s).
            aceleracion_angular_inicial (float): Aceleración angular inicial (rad/s^2).
        
        Raises:
            ValueError: Si el radio es menor o igual a cero.
        """
        if radio <= 0:
            raise ValueError("El radio debe ser un valor positivo.")

        self.radio = radio
        self.posicion_angular_inicial = posicion_angular_inicial
        self.velocidad_angular_inicial = velocidad_angular_inicial
        self.aceleracion_angular_inicial = aceleracion_angular_inicial

    def posicion_angular(self, tiempo: float) -> float:
        """
        Calcula la posición angular en MCUV.
        Ecuación: theta = theta0 + omega0 * t + 0.5 * alpha * t^2

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float: Posición angular final (radianes).
        
        Raises:
            ValueError: Si el tiempo es negativo.
        """
        if tiempo < 0:
            raise ValueError("El tiempo no puede ser negativo.")
        return (self.posicion_angular_inicial +
                self.velocidad_angular_inicial * tiempo +
                0.5 * self.aceleracion_angular_inicial * (tiempo ** 2))

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
        omega = self.velocidad_angular_inicial + self.aceleracion_angular_inicial * tiempo
        theta = self.posicion_angular(tiempo)
        vx = -omega * self.radio * math.sin(theta)
        vy = omega * self.radio * math.cos(theta)
        return np.array([vx, vy])

    def aceleracion(self, tiempo: float) -> np.ndarray:
        """
        Calcula la aceleración (ax, ay) del objeto en un tiempo dado.
        Considera la aceleración tangencial y centrípeta.

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            np.ndarray: Vector de aceleración [ax, ay] (m/s^2).
        """
        if tiempo < 0:
            raise ValueError("El tiempo no puede ser negativo.")
        
        omega = self.velocidad_angular_inicial + self.aceleracion_angular_inicial * tiempo
        alpha = self.aceleracion_angular_inicial
        theta = self.posicion_angular(tiempo)

        # Aceleración tangencial
        at_x = -alpha * self.radio * math.sin(theta)
        at_y = alpha * self.radio * math.cos(theta)

        # Aceleración centrípeta
        ac_x = - (omega ** 2) * self.radio * math.cos(theta)
        ac_y = - (omega ** 2) * self.radio * math.sin(theta)

        ax = at_x + ac_x
        ay = at_y + ac_y
        return np.array([ax, ay])

    def velocidad_angular(self, tiempo: float) -> float:
        """
        Calcula la velocidad angular en MCUV.
        Ecuación: omega = omega0 + alpha * t

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float: Velocidad angular final (rad/s).
        
        Raises:
            ValueError: Si el tiempo es negativo.
        """
        if tiempo < 0:
            raise ValueError("El tiempo no puede ser negativo.")
        return self.velocidad_angular_inicial + self.aceleracion_angular_inicial * tiempo

    def aceleracion_angular_constante(self) -> float:
        """
        Retorna la aceleración angular constante en MCUV.
        """
        return self.aceleracion_angular_inicial
