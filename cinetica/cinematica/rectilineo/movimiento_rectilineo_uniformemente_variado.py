import math
from ..base_movimiento import Movimiento
# from ..graficos.graficador import plot_mruv # This will be handled by a separate Graficador class

class MovimientoRectilineoUniformementeVariado(Movimiento):
    """
    Clase para calcular posición, velocidad y aceleración en Movimiento Rectilíneo Uniformemente Variado (MRUV).
    """

    def __init__(self, posicion_inicial: float = 0.0, velocidad_inicial: float = 0.0, aceleracion_inicial: float = 0.0):
        """
        Inicializa el objeto MovimientoRectilineoUniformementeVariado con condiciones iniciales.

        Args:
            posicion_inicial (float): Posición inicial del objeto (m).
            velocidad_inicial (float): Velocidad inicial del objeto (m/s).
            aceleracion_inicial (float): Aceleración inicial del objeto (m/s^2).
        """
        self.posicion_inicial = posicion_inicial
        self.velocidad_inicial = velocidad_inicial
        self.aceleracion_inicial = aceleracion_inicial

    def posicion(self, tiempo: float) -> float:
        """
        Calcula la posición en MRUV.
        Ecuación: x = x0 + v0 * t + 0.5 * a * t^2

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float: Posición final (m).
        """
        return (
            self.posicion_inicial +
            self.velocidad_inicial * tiempo +
            0.5 * self.aceleracion_inicial * tiempo**2
        )

    def velocidad(self, tiempo: float) -> float:
        """
        Calcula la velocidad en MRUV.
        Ecuación: v = v0 + a * t

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float: Velocidad (m/s).
        """
        return self.velocidad_inicial + self.aceleracion_inicial * tiempo

    def velocidad_sin_tiempo(self, posicion: float) -> float:
        """
        Calcula la velocidad usando la ecuación v^2 = v0^2 + 2*a*Δx.
        Esta ecuación es útil cuando no se conoce el tiempo.

        Args:
            posicion (float): Posición final (m).

        Returns:
            float: Velocidad (m/s).
        """
        delta_x = posicion - self.posicion_inicial
        v_squared = self.velocidad_inicial**2 + 2 * self.aceleracion_inicial * delta_x
        if v_squared < 0:
            raise ValueError("No se puede calcular la velocidad real para esta posición (velocidad al cuadrado negativa).")
        return math.sqrt(v_squared) * (1 if self.velocidad_inicial + self.aceleracion_inicial * (posicion - self.posicion_inicial) >= 0 else -1)

    def posicion(self, tiempo: float) -> float:
        """
        Calcula la posición en MRUV.
        Ecuación: x = x0 + v0 * t + 0.5 * a * t^2

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float: Posición final (m).
        
        Raises:
            ValueError: Si el tiempo es negativo.
        """
        if tiempo < 0:
            raise ValueError("El tiempo no puede ser negativo.")
        return self.posicion_inicial + self.velocidad_inicial * tiempo + 0.5 * self.aceleracion_inicial * (tiempo ** 2)

    def velocidad(self, tiempo: float) -> float:
        """
        Calcula la velocidad en MRUV.
        Ecuación: v = v0 + a * t

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float: Velocidad final (m/s).
        
        Raises:
            ValueError: Si el tiempo es negativo.
        """
        if tiempo < 0:
            raise ValueError("El tiempo no puede ser negativo.")
        return self.velocidad_inicial + self.aceleracion_inicial * tiempo

    def aceleracion(self, tiempo: float = None) -> float:
        """
        Calcula la aceleración en MRUV (es constante).
        Ecuación: a = a0

        Args:
            tiempo (float, optional): Tiempo transcurrido (s). No afecta al resultado.

        Returns:
            float: Aceleración (m/s^2).
        """
        return self.aceleracion_inicial
