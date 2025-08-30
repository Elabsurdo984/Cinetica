import math
from typing import Union
from ..graficos.graficador import plot_mcu
from ..exceptions import InvalidPhysicsParameterError, NegativeTimeError
from ..movimiento_base import MovimientoBase
from ..units import ureg, Q_

class MovimientoCircularUniforme(MovimientoBase):
    """
    Clase para calcular y simular Movimiento Circular Uniforme (MCU).
    """

    def __init__(self, radio: Q_, posicion_angular_inicial: Q_ = 0.0 * ureg.radian, velocidad_angular_inicial: Q_ = 0.0 * ureg.radian / ureg.second):
        """
        Inicializa el objeto MovimientoCircularUniforme con las condiciones iniciales.

        Args:
            radio (Q_): Radio de la trayectoria circular (ej. `5 * ureg.meter`).
            posicion_angular_inicial (Q_): Posición angular inicial (ej. `0.0 * ureg.radian`).
            velocidad_angular_inicial (Q_): Velocidad angular inicial (ej. `2 * ureg.radian / ureg.second`).
        
        Raises:
            InvalidPhysicsParameterError: Si el radio es menor o igual a cero o las unidades son incorrectas.
        """
        if not isinstance(radio, Q_) or not radio.check('[length]'):
            raise InvalidPhysicsParameterError("El radio debe ser una cantidad de longitud.")
        if radio.magnitude <= 0:
            raise InvalidPhysicsParameterError("El radio debe ser un valor positivo.")
        if not isinstance(posicion_angular_inicial, Q_) or not posicion_angular_inicial.check('[angle]'):
            raise InvalidPhysicsParameterError("La posición angular inicial debe ser una cantidad de ángulo.")
        if not isinstance(velocidad_angular_inicial, Q_) or not velocidad_angular_inicial.check('[angle] / [time]'):
            raise InvalidPhysicsParameterError("La velocidad angular inicial debe ser una cantidad de velocidad angular.")

        self.radio = radio
        self.posicion_angular_inicial = posicion_angular_inicial
        self.velocidad_angular_inicial = velocidad_angular_inicial

    def posicion(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la posición angular en MCU.
        Ecuación: theta = theta0 + omega * t

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`).

        Returns:
            Q_: Posición angular final (cantidad de ángulo).
        
        Raises:
            NegativeTimeError: Si el tiempo es negativo.
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        if tiempo.magnitude < 0:
            raise NegativeTimeError("El tiempo no puede ser negativo.")
        return self.posicion_angular_inicial + self.velocidad_angular_inicial * tiempo

    def velocidad(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la velocidad angular en MCU (es constante).
        Ecuación: omega = omega0

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`). (Ignorado en MCU ya que la velocidad angular es constante)

        Returns:
            Q_: Velocidad angular (cantidad de velocidad angular).
        
        Raises:
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        return self.velocidad_angular_inicial

    def aceleracion(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la aceleración angular en MCU (es cero).
        Ecuación: alpha = 0

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`). (Ignorado en MCU ya que la aceleración angular es cero)

        Returns:
            Q_: Aceleración angular (cantidad de aceleración angular).
        
        Raises:
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        return 0.0 * ureg.radian / ureg.second**2

    def velocidad_tangencial(self) -> Q_:
        """
        Calcula la velocidad tangencial en MCU.
        Ecuación: v = omega * R

        Returns:
            Q_: Velocidad tangencial (cantidad de velocidad).
        """
        return self.velocidad_angular(tiempo=0 * ureg.second) * self.radio

    def aceleracion_centripeta(self) -> Q_:
        """
        Calcula la aceleración centrípeta en MCU.
        Ecuación: ac = omega^2 * R = v^2 / R

        Returns:
            Q_: Aceleración centrípeta (cantidad de aceleración).
        """
        return (self.velocidad_angular(tiempo=0 * ureg.second) ** 2) * self.radio # Aceleración centrípeta es constante

    def periodo(self) -> Q_:
        """
        Calcula el período en MCU.
        Ecuación: T = 2 * pi / omega

        Returns:
            Q_: Período (cantidad de tiempo).
        
        Notes:
            Retorna `math.inf * ureg.second` si la velocidad angular inicial es cero.
        """
        if self.velocidad_angular_inicial.magnitude == 0:
            return math.inf * ureg.second  # Período infinito si la velocidad angular es cero
        return (2 * math.pi * ureg.radian) / self.velocidad_angular_inicial

    def frecuencia(self) -> Q_:
        """
        Calcula la frecuencia en MCU.
        Ecuación: f = 1 / T = omega / (2 * pi)

        Returns:
            Q_: Frecuencia (cantidad de frecuencia).
        
        Notes:
            Retorna `0.0 * ureg.hertz` si la velocidad angular inicial es cero.
        """
        if self.velocidad_angular_inicial.magnitude == 0:
            return 0.0 * ureg.hertz  # Frecuencia cero si la velocidad angular es cero
        return self.velocidad_angular_inicial / (2 * math.pi * ureg.radian)

    def graficar(self, t_max: Union[float, Q_], num_points: int = 100):
        """
        Genera y muestra gráficos de posición angular vs. tiempo, velocidad angular vs. tiempo
        y aceleración centrípeta vs. tiempo para MCU. También grafica la trayectoria circular.

        Args:
            t_max (Union[float, Q_]): Tiempo máximo para la simulación (s o cantidad de tiempo).
            num_points (int): Número de puntos a generar para el gráfico.
        
        Raises:
            InvalidPhysicsParameterError: Si el tiempo máximo es menor o igual a cero o no es una cantidad de tiempo.
        """
        if isinstance(t_max, Q_):
            if not t_max.check('[time]'):
                raise InvalidPhysicsParameterError("El tiempo máximo debe ser una cantidad de tiempo.")
            if t_max.magnitude <= 0:
                raise InvalidPhysicsParameterError("El tiempo máximo debe ser positivo para generar el gráfico.")
            plot_mcu(self, t_max.to(ureg.second).magnitude, num_points)
        elif isinstance(t_max, (int, float)):
            if t_max <= 0:
                raise InvalidPhysicsParameterError("El tiempo máximo debe ser positivo para generar el gráfico.")
            plot_mcu(self, t_max, num_points)
        else:
            raise InvalidPhysicsParameterError("El tiempo máximo debe ser un número o una cantidad de tiempo.")
