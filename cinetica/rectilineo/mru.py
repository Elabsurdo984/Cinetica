import math
from typing import Union
from ..graficos.graficador import plot_mru
from ..exceptions import NegativeTimeError, InvalidPhysicsParameterError
from ..movimiento_base import MovimientoBase
from ..units import ureg, Q_

class MovimientoRectilineoUniforme(MovimientoBase):
    """
    Clase para calcular posición y velocidad en Movimiento Rectilíneo Uniforme (MRU).
    """

    def __init__(self, posicion_inicial: Q_ = 0.0 * ureg.meter, velocidad_inicial: Q_ = 0.0 * ureg.meter / ureg.second):
        """
        Inicializa el objeto MovimientoRectilineoUniforme con condiciones iniciales.

        Args:
            posicion_inicial (Q_): Posición inicial del objeto (ej. `10 * ureg.meter`).
            velocidad_inicial (Q_): Velocidad inicial del objeto (ej. `5 * ureg.meter / ureg.second`).
        """
        if not isinstance(posicion_inicial, Q_) or not posicion_inicial.check('[length]'):
            raise InvalidPhysicsParameterError("La posición inicial debe ser una cantidad de longitud.")
        if not isinstance(velocidad_inicial, Q_) or not velocidad_inicial.check('[length] / [time]'):
            raise InvalidPhysicsParameterError("La velocidad inicial debe ser una cantidad de velocidad.")

        self.posicion_inicial = posicion_inicial
        self.velocidad_inicial = velocidad_inicial

    def posicion(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la posición en MRU.
        Ecuación: x = x0 + v * t

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`).

        Returns:
            Q_: Posición final (cantidad de longitud).
        
        Raises:
            NegativeTimeError: Si el tiempo es negativo.
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        if tiempo.magnitude < 0:
            raise NegativeTimeError("El tiempo no puede ser negativo.")
        return self.posicion_inicial + self.velocidad_inicial * tiempo

    def velocidad(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la velocidad en MRU (es constante).
        Ecuación: v = v0

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`). (Ignorado en MRU ya que la velocidad es constante)

        Returns:
            Q_: Velocidad (cantidad de velocidad).
        
        Raises:
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        return self.velocidad_inicial

    def aceleracion(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la aceleración en MRU (es cero).
        Ecuación: a = 0

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`). (Ignorado en MRU ya que la aceleración es cero)

        Returns:
            Q_: Aceleración (cantidad de aceleración).
        
        Raises:
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        return 0.0 * ureg.meter / ureg.second**2

    def graficar(self, t_max: Union[float, Q_], num_points: int = 100):
        """
        Genera y muestra gráficos de posición vs. tiempo y velocidad vs. tiempo para MRU.

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
            plot_mru(self, t_max.to(ureg.second).magnitude, num_points)
        elif isinstance(t_max, (int, float)):
            if t_max <= 0:
                raise InvalidPhysicsParameterError("El tiempo máximo debe ser positivo para generar el gráfico.")
            plot_mru(self, t_max, num_points)
        else:
            raise InvalidPhysicsParameterError("El tiempo máximo debe ser un número o una cantidad de tiempo.")
