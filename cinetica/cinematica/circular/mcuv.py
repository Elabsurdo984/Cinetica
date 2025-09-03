import math

class MovimientoCircularUniformementeVariado:
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

    def aceleracion_angular(self) -> float:
        """
        Calcula la aceleración angular en MCUV (es constante).
        Ecuación: alpha = alpha0

        Returns:
            float: Aceleración angular (rad/s^2).
        """
        return self.aceleracion_angular_inicial

    def velocidad_tangencial(self, tiempo: float) -> float:
        """
        Calcula la velocidad tangencial en MCUV.
        Ecuación: v = omega * R

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float: Velocidad tangencial (m/s).
        """
        return self.velocidad_angular(tiempo) * self.radio

    def aceleracion_tangencial(self) -> float:
        """
        Calcula la aceleración tangencial en MCUV.
        Ecuación: at = alpha * R

        Returns:
            float: Aceleración tangencial (m/s^2).
        """
        return self.aceleracion_angular_inicial * self.radio

    def aceleracion_centripeta(self, tiempo: float) -> float:
        """
        Calcula la aceleración centrípeta en MCUV.
        Ecuación: ac = omega^2 * R

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float: Aceleración centrípeta (m/s^2).
        """
        return (self.velocidad_angular(tiempo) ** 2) * self.radio

    def aceleracion_total(self, tiempo: float) -> float:
        """
        Calcula la magnitud de la aceleración total en MCUV.
        Ecuación: a_total = sqrt(at^2 + ac^2)

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float: Magnitud de la aceleración total (m/s^2).
        """
        at = self.aceleracion_tangencial()
        ac = self.aceleracion_centripeta(tiempo)
        return math.sqrt(at**2 + ac**2)
