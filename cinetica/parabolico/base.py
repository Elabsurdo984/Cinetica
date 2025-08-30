import math
from typing import Union
from ..graficos.graficador import plot_parabolico
from ..exceptions import InvalidPhysicsParameterError, NegativeTimeError
from ..movimiento_base import MovimientoBase
from ..units import ureg, Q_

class MovimientoParabolicoBase(MovimientoBase):
    """
    Clase base para simular trayectorias en Movimiento Parabólico.
    Se asume que el lanzamiento se realiza desde el origen (0,0) y la gravedad actúa hacia abajo.
    """

    def __init__(self, velocidad_inicial: Q_, angulo_grados: float, gravedad: Q_ = 9.81 * ureg.meter / ureg.second**2):
        """
        Inicializa el objeto MovimientoParabolicoBase con las condiciones iniciales.

        Args:
            velocidad_inicial (Q_): Magnitud de la velocidad inicial (ej. `10 * ureg.meter / ureg.second`).
            angulo_grados (float): Ángulo de lanzamiento con respecto a la horizontal (grados).
            gravedad (Q_): Aceleración debido a la gravedad (ej. `9.81 * ureg.meter / ureg.second**2`).
        
        Raises:
            InvalidPhysicsParameterError: Si la velocidad inicial es negativa, el ángulo no está entre 0 y 90 grados,
                                          o la gravedad es menor o igual a cero, o las unidades son incorrectas.
        """
        if not isinstance(velocidad_inicial, Q_) or not velocidad_inicial.check('[length] / [time]'):
            raise InvalidPhysicsParameterError("La velocidad inicial debe ser una cantidad de velocidad.")
        if velocidad_inicial.magnitude < 0:
            raise InvalidPhysicsParameterError("La velocidad inicial no puede ser negativa.")
        if not (0 <= angulo_grados <= 90):
            raise InvalidPhysicsParameterError("El ángulo de lanzamiento debe estar entre 0 y 90 grados.")
        if not isinstance(gravedad, Q_) or not gravedad.check('[length] / [time]**2'):
            raise InvalidPhysicsParameterError("La gravedad debe ser una cantidad de aceleración.")
        if gravedad.magnitude <= 0:
            raise InvalidPhysicsParameterError("La gravedad debe ser un valor positivo.")

        self.velocidad_inicial = velocidad_inicial
        self.angulo_radianes = math.radians(angulo_grados)
        self.gravedad = gravedad

        self.velocidad_inicial_x = self.velocidad_inicial * math.cos(self.angulo_radianes)
        self.velocidad_inicial_y = self.velocidad_inicial * math.sin(self.angulo_radianes)

    def posicion(self, tiempo: Q_ = 0.0 * ureg.second) -> tuple[Q_, Q_]:
        """
        Calcula la posición (x, y) del proyectil en un tiempo dado.

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`).

        Returns:
            tuple: Una tupla (x, y) con las coordenadas de la posición (cantidades de longitud).
        
        Raises:
            NegativeTimeError: Si el tiempo es negativo.
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        if tiempo.magnitude < 0:
            raise NegativeTimeError("El tiempo no puede ser negativo.")

        posicion_x = self.velocidad_inicial_x * tiempo
        posicion_y = (self.velocidad_inicial_y * tiempo) - (0.5 * self.gravedad * (tiempo ** 2))
        return (posicion_x.to(ureg.meter), posicion_y.to(ureg.meter))

    def velocidad(self, tiempo: Q_ = 0.0 * ureg.second) -> tuple[Q_, Q_]:
        """
        Calcula la velocidad (vx, vy) del proyectil en un tiempo dado.

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`).

        Returns:
            tuple: Una tupla (vx, vy) con las componentes de la velocidad (cantidades de velocidad).
        
        Raises:
            NegativeTimeError: Si el tiempo es negativo.
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        if tiempo.magnitude < 0:
            raise NegativeTimeError("El tiempo no puede ser negativo.")

        velocidad_x = self.velocidad_inicial_x
        velocidad_y = self.velocidad_inicial_y - (self.gravedad * tiempo)
        return (velocidad_x.to(ureg.meter / ureg.second), velocidad_y.to(ureg.meter / ureg.second))

    def aceleracion(self, tiempo: Q_ = 0.0 * ureg.second) -> tuple[Q_, Q_]:
        """
        Calcula la aceleración (ax, ay) del proyectil en un tiempo dado.

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`). (Ignorado en movimiento parabólico ya que la aceleración es constante)

        Returns:
            tuple: Una tupla (ax, ay) con las componentes de la aceleración (cantidades de aceleración).
        
        Raises:
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        return (0.0 * ureg.meter / ureg.second**2, -self.gravedad.to(ureg.meter / ureg.second**2))

    def graficar(self, t_max: Union[float, Q_], num_points: int = 100):
        """
        Genera y muestra el gráfico de la trayectoria (y vs. x) para Movimiento Parabólico.

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
            plot_parabolico(self, t_max.to(ureg.second).magnitude, num_points)
        elif isinstance(t_max, (int, float)):
            if t_max <= 0:
                raise InvalidPhysicsParameterError("El tiempo máximo debe ser positivo para generar el gráfico.")
            plot_parabolico(self, t_max, num_points)
        else:
            raise InvalidPhysicsParameterError("El tiempo máximo debe ser un número o una cantidad de tiempo.")
