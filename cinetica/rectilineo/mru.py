import math
from ..graficos.graficador import plot_mru
from ..exceptions import NegativeTimeError, InvalidPhysicsParameterError
from ..movimiento_base import MovimientoBase

class MovimientoRectilineoUniforme(MovimientoBase):
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
        
        Raises:
            NegativeTimeError: Si el tiempo es negativo.
        """
        if tiempo < 0:
            raise NegativeTimeError("El tiempo no puede ser negativo.")
        return self.posicion_inicial + self.velocidad_inicial * tiempo

    def velocidad(self, tiempo: float) -> float:
        """
        Calcula la velocidad en MRU (es constante).
        Ecuación: v = v0

        Args:
            tiempo (float): Tiempo transcurrido (s). (Ignorado en MRU ya que la velocidad es constante)

        Returns:
            float: Velocidad (m/s).
        """
        return self.velocidad_inicial

    def aceleracion(self, tiempo: float) -> float:
        """
        Calcula la aceleración en MRU (es cero).
        Ecuación: a = 0

        Args:
            tiempo (float): Tiempo transcurrido (s). (Ignorado en MRU ya que la aceleración es cero)

        Returns:
            float: Aceleración (m/s^2).
        """
        return 0.0

    def graficar(self, t_max: float, num_points: int = 100):
        """
        Genera y muestra gráficos de posición vs. tiempo y velocidad vs. tiempo para MRU.

        Args:
            t_max (float): Tiempo máximo para la simulación (s).
            num_points (int): Número de puntos a generar para el gráfico.
        
        Raises:
            InvalidPhysicsParameterError: Si el tiempo máximo es menor o igual a cero.
        """
        if t_max <= 0:
            raise InvalidPhysicsParameterError("El tiempo máximo debe ser positivo para generar el gráfico.")
        plot_mru(self, t_max, num_points)
