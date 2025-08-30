import math
from typing import Union
from ..graficos.graficador import plot_mcuv
from ..exceptions import InvalidPhysicsParameterError, NegativeTimeError, PhysicallyImpossibleError, ZeroDivisionError
from ..movimiento_base import MovimientoBase
from ..units import ureg, Q_

class MovimientoCircularUniformementeVariado(MovimientoBase):
    """
    Clase para calcular y simular Movimiento Circular Uniformemente Variado (MCUV).
    """

    def __init__(self, radio: Q_, posicion_angular_inicial: Q_ = 0.0 * ureg.radian, velocidad_angular_inicial: Q_ = 0.0 * ureg.radian / ureg.second, aceleracion_angular_inicial: Q_ = 0.0 * ureg.radian / ureg.second**2):
        """
        Inicializa el objeto MovimientoCircularUniformementeVariado con las condiciones iniciales.

        Args:
            radio (Q_): Radio de la trayectoria circular (ej. `5 * ureg.meter`).
            posicion_angular_inicial (Q_): Posición angular inicial (ej. `0.0 * ureg.radian`).
            velocidad_angular_inicial (Q_): Velocidad angular inicial (ej. `2 * ureg.radian / ureg.second`).
            aceleracion_angular_inicial (Q_): Aceleración angular inicial (ej. `0.5 * ureg.radian / ureg.second**2`).
        
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
        if not isinstance(aceleracion_angular_inicial, Q_) or not aceleracion_angular_inicial.check('[angle] / [time]**2'):
            raise InvalidPhysicsParameterError("La aceleración angular inicial debe ser una cantidad de aceleración angular.")

        self.radio = radio
        self.posicion_angular_inicial = posicion_angular_inicial
        self.velocidad_angular_inicial = velocidad_angular_inicial
        self.aceleracion_angular_inicial = aceleracion_angular_inicial

    def posicion(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la posición angular en MCUV.
        Ecuación: theta = theta0 + omega0 * t + 0.5 * alpha * t^2

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
        return self.posicion_angular_inicial + self.velocidad_angular_inicial * tiempo + 0.5 * self.aceleracion_angular_inicial * (tiempo ** 2)

    def velocidad(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la velocidad angular en MCUV.
        Ecuación: omega = omega0 + alpha * t

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`).

        Returns:
            Q_: Velocidad angular final (cantidad de velocidad angular).
        
        Raises:
            NegativeTimeError: Si el tiempo es negativo.
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        if tiempo.magnitude < 0:
            raise NegativeTimeError("El tiempo no puede ser negativo.")
        return self.velocidad_angular_inicial + self.aceleracion_angular_inicial * tiempo

    def aceleracion(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la aceleración angular en MCUV (es constante).
        Ecuación: alpha = alpha0

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`). (Ignorado en MCUV ya que la aceleración angular es constante)

        Returns:
            Q_: Aceleración angular (cantidad de aceleración angular).
        
        Raises:
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        return self.aceleracion_angular_inicial

    def velocidad_tangencial(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la velocidad tangencial en MCUV.
        Ecuación: v = omega * R

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`).

        Returns:
            Q_: Velocidad tangencial (cantidad de velocidad).
        """
        return self.velocidad_angular(tiempo) * self.radio

    def aceleracion_tangencial(self) -> Q_:
        """
        Calcula la aceleración tangencial en MCUV.
        Ecuación: at = alpha * R

        Returns:
            Q_: Aceleración tangencial (cantidad de aceleración).
        """
        return self.aceleracion_angular_inicial * self.radio

    def aceleracion_centripeta(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la aceleración centrípeta en MCUV.
        Ecuación: ac = omega^2 * R

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`).

        Returns:
            Q_: Aceleración centrípeta (cantidad de aceleración).
        """
        return (self.velocidad_angular(tiempo) ** 2) * self.radio

    def aceleracion_total(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la magnitud de la aceleración total en MCUV.
        Ecuación: a_total = sqrt(at^2 + ac^2)

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`).

        Returns:
            Q_: Magnitud de la aceleración total (cantidad de aceleración).
        """
        at = self.aceleracion_tangencial()
        ac = self.aceleracion_centripeta(tiempo)
        return math.sqrt(at.magnitude**2 + ac.magnitude**2) * ureg.meter / ureg.second**2

    def velocidad_angular_sin_tiempo(self, posicion_angular_final: Q_) -> Q_:
        """
        Calcula la velocidad angular final en MCUV sin conocer el tiempo.
        Ecuación: omega_f^2 = omega_0^2 + 2 * alpha * (theta_f - theta_0)

        Args:
            posicion_angular_final (Q_): Posición angular final (ej. `5 * ureg.radian`).

        Returns:
            Q_: Velocidad angular final (cantidad de velocidad angular).
        
        Raises:
            PhysicallyImpossibleError: Si la velocidad angular al cuadrado es negativa, indicando una situación físicamente imposible.
            InvalidPhysicsParameterError: Si la posición angular final no es una cantidad de ángulo.
        """
        if not isinstance(posicion_angular_final, Q_) or not posicion_angular_final.check('[angle]'):
            raise InvalidPhysicsParameterError("La posición angular final debe ser una cantidad de ángulo.")

        delta_theta = posicion_angular_final - self.posicion_angular_inicial
        omega_squared = (self.velocidad_angular_inicial ** 2) + 2 * self.aceleracion_angular_inicial * delta_theta
        if omega_squared.magnitude < 0:
            raise PhysicallyImpossibleError("No se puede calcular la velocidad angular real (velocidad angular al cuadrado negativa).")
        return math.sqrt(omega_squared.magnitude) * omega_squared.units**0.5

    def tiempo_por_posicion_angular(self, posicion_angular_final: Q_) -> tuple[Q_, Q_]:
        """
        Calcula el tiempo a partir de la posición angular final en MCUV, resolviendo la ecuación cuadrática.
        Ecuación: theta_f = theta0 + omega0 * t + 0.5 * alpha * t^2  =>  0.5 * alpha * t^2 + omega0 * t + (theta0 - theta_f) = 0

        Args:
            posicion_angular_final (Q_): Posición angular final del objeto (ej. `5 * ureg.radian`).

        Returns:
            tuple[Q_, Q_]: Una tupla con los dos posibles valores de tiempo (cantidad de tiempo).
                                 Si solo hay una solución válida, el segundo valor será `math.nan * ureg.second`.
                                 Si no hay soluciones reales, ambos valores serán `math.nan * ureg.second`.
        
        Raises:
            PhysicallyImpossibleError: Si la aceleración angular es cero y la velocidad angular inicial también es cero,
                                       o si el discriminante es negativo (no hay soluciones reales).
            NegativeTimeError: Si el tiempo calculado es negativo.
            InvalidPhysicsParameterError: Si la posición angular final no es una cantidad de ángulo.
        """
        if not isinstance(posicion_angular_final, Q_) or not posicion_angular_final.check('[angle]'):
            raise InvalidPhysicsParameterError("La posición angular final debe ser una cantidad de ángulo.")

        a_val = 0.5 * self.aceleracion_angular_inicial.to(ureg.radian / ureg.second**2).magnitude
        b_val = self.velocidad_angular_inicial.to(ureg.radian / ureg.second).magnitude
        c_val = (self.posicion_angular_inicial - posicion_angular_final).to(ureg.radian).magnitude

        if a_val == 0:  # Caso de MCU
            if b_val == 0:
                if c_val == 0:
                    return (math.inf * ureg.second, math.nan * ureg.second)
                else:
                    return (math.nan * ureg.second, math.nan * ureg.second)
            else:
                tiempo_val = -c_val / b_val
                if tiempo_val < 0:
                    raise NegativeTimeError("El tiempo calculado es negativo, lo cual no es físicamente posible.")
                return (tiempo_val * ureg.second, math.nan * ureg.second)

        discriminante = b_val**2 - 4 * a_val * c_val

        if discriminante < 0:
            return (math.nan * ureg.second, math.nan * ureg.second)
        elif discriminante == 0:
            tiempo_val = (-b_val) / (2 * a_val)
            if tiempo_val < 0:
                raise NegativeTimeError("El tiempo calculado es negativo, lo cual no es físicamente posible.")
            return (tiempo_val * ureg.second, math.nan * ureg.second)
        else:
            tiempo1_val = (-b_val + math.sqrt(discriminante)) / (2 * a_val)
            tiempo2_val = (-b_val - math.sqrt(discriminante)) / (2 * a_val)
            
            valid_times = []
            if tiempo1_val >= 0:
                valid_times.append(tiempo1_val)
            if tiempo2_val >= 0:
                valid_times.append(tiempo2_val)
            
            if not valid_times:
                raise NegativeTimeError("Ambos tiempos calculados son negativos, lo cual no es físicamente posible.")
            elif len(valid_times) == 1:
                return (valid_times[0] * ureg.second, math.nan * ureg.second)
            else:
                return (min(valid_times) * ureg.second, max(valid_times) * ureg.second)

    def tiempo_por_velocidad_angular(self, velocidad_angular_final: Q_) -> Q_:
        """
        Calcula el tiempo a partir de la velocidad angular final en MCUV.
        Ecuación: omega_f = omega_0 + alpha * t  =>  t = (omega_f - omega_0) / alpha

        Args:
            velocidad_angular_final (Q_): Velocidad angular final del objeto (ej. `5 * ureg.radian / ureg.second`).

        Returns:
            Q_: Tiempo transcurrido (cantidad de tiempo).
        
        Raises:
            PhysicallyImpossibleError: Si la aceleración angular es cero y la velocidad angular final no coincide con la inicial.
            NegativeTimeError: Si el tiempo calculado es negativo.
            InvalidPhysicsParameterError: Si la velocidad angular final no es una cantidad de velocidad angular.
        """
        if not isinstance(velocidad_angular_final, Q_) or not velocidad_angular_final.check('[angle] / [time]'):
            raise InvalidPhysicsParameterError("La velocidad angular final debe ser una cantidad de velocidad angular.")

        if self.aceleracion_angular_inicial.magnitude == 0:
            if velocidad_angular_final != self.velocidad_angular_inicial:
                raise PhysicallyImpossibleError("La aceleración angular es cero, por lo que la velocidad angular no puede cambiar.")
            return math.inf * ureg.second
        
        tiempo = (velocidad_angular_final - self.velocidad_angular_inicial) / self.aceleracion_angular_inicial
        if tiempo.magnitude < 0:
            raise NegativeTimeError("El tiempo calculado es negativo, lo cual no es físicamente posible.")
        return tiempo.to(ureg.second)

    def graficar(self, t_max: Union[float, Q_], num_points: int = 100):
        """
        Genera y muestra gráficos de posición angular vs. tiempo, velocidad angular vs. tiempo,
        aceleración angular vs. tiempo, aceleración centrípeta vs. tiempo y aceleración total vs. tiempo para MCUV.

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
            plot_mcuv(self, t_max.to(ureg.second).magnitude, num_points)
        elif isinstance(t_max, (int, float)):
            if t_max <= 0:
                raise InvalidPhysicsParameterError("El tiempo máximo debe ser positivo para generar el gráfico.")
            plot_mcuv(self, t_max, num_points)
        else:
            raise InvalidPhysicsParameterError("El tiempo máximo debe ser un número o una cantidad de tiempo.")
