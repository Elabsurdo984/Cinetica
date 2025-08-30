import math
from ..graficos.graficador import plot_parabolico
from ..exceptions import InvalidPhysicsParameterError, NegativeTimeError
from ..movimiento_base import MovimientoBase

class MovimientoParabolicoBase(MovimientoBase):
    """
    Clase base para simular trayectorias en Movimiento Parabólico.
    Se asume que el lanzamiento se realiza desde el origen (0,0) y la gravedad actúa hacia abajo.
    """

    def __init__(self, velocidad_inicial: float, angulo_grados: float, gravedad: float = 9.81):
        """
        Inicializa el objeto MovimientoParabolicoBase con las condiciones iniciales.

        Args:
            velocidad_inicial (float): Magnitud de la velocidad inicial (m/s).
            angulo_grados (float): Ángulo de lanzamiento con respecto a la horizontal (grados).
            gravedad (float): Aceleración debido a la gravedad (m/s^2).
        
        Raises:
            InvalidPhysicsParameterError: Si la velocidad inicial es negativa, el ángulo no está entre 0 y 90 grados, o la gravedad es menor o igual a cero.
        """
        if velocidad_inicial < 0:
            raise InvalidPhysicsParameterError("La velocidad inicial no puede ser negativa.")
        if not (0 <= angulo_grados <= 90):
            raise InvalidPhysicsParameterError("El ángulo de lanzamiento debe estar entre 0 y 90 grados.")
        if gravedad <= 0:
            raise InvalidPhysicsParameterError("La gravedad debe ser un valor positivo.")

        self.velocidad_inicial = velocidad_inicial
        self.angulo_radianes = math.radians(angulo_grados)
        self.gravedad = gravedad

        self.velocidad_inicial_x = self.velocidad_inicial * math.cos(self.angulo_radianes)
        self.velocidad_inicial_y = self.velocidad_inicial * math.sin(self.angulo_radianes)

    def posicion(self, tiempo: float) -> tuple[float, float]:
        """
        Calcula la posición (x, y) del proyectil en un tiempo dado.

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            tuple: Una tupla (x, y) con las coordenadas de la posición (m).
        
        Raises:
            NegativeTimeError: Si el tiempo es negativo.
        """
        if tiempo < 0:
            raise NegativeTimeError("El tiempo no puede ser negativo.")

        posicion_x = self.velocidad_inicial_x * tiempo
        posicion_y = (self.velocidad_inicial_y * tiempo) - (0.5 * self.gravedad * (tiempo ** 2))
        return (posicion_x, posicion_y)

    def velocidad(self, tiempo: float) -> tuple[float, float]:
        """
        Calcula la velocidad (vx, vy) del proyectil en un tiempo dado.

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            tuple: Una tupla (vx, vy) con las componentes de la velocidad (m/s).
        
        Raises:
            NegativeTimeError: Si el tiempo es negativo.
        """
        if tiempo < 0:
            raise NegativeTimeError("El tiempo no puede ser negativo.")

        velocidad_x = self.velocidad_inicial_x
        velocidad_y = self.velocidad_inicial_y - (self.gravedad * tiempo)
        return (velocidad_x, velocidad_y)

    def aceleracion(self, tiempo: float) -> tuple[float, float]:
        """
        Calcula la aceleración (ax, ay) del proyectil en un tiempo dado.

        Args:
            tiempo (float): Tiempo transcurrido (s). (Ignorado en movimiento parabólico ya que la aceleración es constante)

        Returns:
            tuple: Una tupla (ax, ay) con las componentes de la aceleración (m/s^2).
        """
        return (0.0, -self.gravedad) # Aceleración en x es 0, en y es -gravedad

    def graficar(self, t_max: float, num_points: int = 100):
        """
        Genera y muestra el gráfico de la trayectoria (y vs. x) para Movimiento Parabólico.

        Args:
            t_max (float): Tiempo máximo para la simulación (s).
            num_points (int): Número de puntos a generar para el gráfico.
        
        Raises:
            InvalidPhysicsParameterError: Si el tiempo máximo es menor o igual a cero.
        """
        if t_max <= 0:
            raise InvalidPhysicsParameterError("El tiempo máximo debe ser positivo para generar el gráfico.")
        plot_parabolico(self, t_max, num_points)
