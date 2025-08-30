import math
from ..graficos.graficador import plot_mcu
from ..exceptions import InvalidPhysicsParameterError, NegativeTimeError
from ..movimiento_base import MovimientoBase

class MovimientoCircularUniforme(MovimientoBase):
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
            InvalidPhysicsParameterError: Si el radio es menor o igual a cero.
        """
        if radio <= 0:
            raise InvalidPhysicsParameterError("El radio debe ser un valor positivo.")

        self.radio = radio
        self.posicion_angular_inicial = posicion_angular_inicial
        self.velocidad_angular_inicial = velocidad_angular_inicial

    def posicion(self, tiempo: float) -> float:
        """
        Calcula la posición angular en MCU.
        Ecuación: theta = theta0 + omega * t

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float: Posición angular final (radianes).
        
        Raises:
            NegativeTimeError: Si el tiempo es negativo.
        """
        if tiempo < 0:
            raise NegativeTimeError("El tiempo no puede ser negativo.")
        return self.posicion_angular_inicial + self.velocidad_angular_inicial * tiempo

    def velocidad(self, tiempo: float) -> float:
        """
        Calcula la velocidad angular en MCU (es constante).
        Ecuación: omega = omega0

        Args:
            tiempo (float): Tiempo transcurrido (s). (Ignorado en MCU ya que la velocidad angular es constante)

        Returns:
            float: Velocidad angular (rad/s).
        """
        return self.velocidad_angular_inicial

    def velocidad_tangencial(self) -> float:
        """
        Calcula la velocidad tangencial en MCU.
        Ecuación: v = omega * R

        Returns:
            float: Velocidad tangencial (m/s).
        """
        return self.velocidad_angular() * self.radio

    def aceleracion_centripeta(self) -> float:
        """
        Calcula la aceleración centrípeta en MCU.
        Ecuación: ac = omega^2 * R = v^2 / R

        Returns:
            float: Aceleración centrípeta (m/s^2).
        """
        return (self.velocidad_angular(tiempo=0) ** 2) * self.radio # Aceleración centrípeta es constante

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

    def graficar(self, t_max: float, num_points: int = 100):
        """
        Genera y muestra gráficos de posición angular vs. tiempo, velocidad angular vs. tiempo
        y aceleración centrípeta vs. tiempo para MCU. También grafica la trayectoria circular.

        Args:
            t_max (float): Tiempo máximo para la simulación (s).
            num_points (int): Número de puntos a generar para el gráfico.
        
        Raises:
            InvalidPhysicsParameterError: Si el tiempo máximo es menor o igual a cero.
        """
        if t_max <= 0:
            raise InvalidPhysicsParameterError("El tiempo máximo debe ser positivo para generar el gráfico.")
        plot_mcu(self, t_max, num_points)
