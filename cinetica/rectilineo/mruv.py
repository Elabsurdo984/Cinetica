import math
from typing import Union
from ..graficos.graficador import plot_mruv
from ..exceptions import NegativeTimeError, InvalidPhysicsParameterError, PhysicallyImpossibleError, ZeroDivisionError
from ..movimiento_base import MovimientoBase
from ..units import ureg, Q_

class MovimientoRectilineoUniformementeVariado(MovimientoBase):
    """
    Clase para calcular posición, velocidad y aceleración en Movimiento Rectilíneo Uniformemente Variado (MRUV).
    """

    def __init__(self, posicion_inicial: Q_ = 0.0 * ureg.meter, velocidad_inicial: Q_ = 0.0 * ureg.meter / ureg.second, aceleracion_inicial: Q_ = 0.0 * ureg.meter / ureg.second**2):
        """
        Inicializa el objeto MovimientoRectilineoUniformementeVariado con condiciones iniciales.

        Args:
            posicion_inicial (Q_): Posición inicial del objeto (ej. `10 * ureg.meter`).
            velocidad_inicial (Q_): Velocidad inicial del objeto (ej. `5 * ureg.meter / ureg.second`).
            aceleracion_inicial (Q_): Aceleración inicial del objeto (ej. `2 * ureg.meter / ureg.second**2`).
        """
        if not isinstance(posicion_inicial, Q_) or not posicion_inicial.check('[length]'):
            raise InvalidPhysicsParameterError("La posición inicial debe ser una cantidad de longitud.")
        if not isinstance(velocidad_inicial, Q_) or not velocidad_inicial.check('[length] / [time]'):
            raise InvalidPhysicsParameterError("La velocidad inicial debe ser una cantidad de velocidad.")
        if not isinstance(aceleracion_inicial, Q_) or not aceleracion_inicial.check('[length] / [time]**2'):
            raise InvalidPhysicsParameterError("La aceleración inicial debe ser una cantidad de aceleración.")

        self.posicion_inicial = posicion_inicial
        self.velocidad_inicial = velocidad_inicial
        self.aceleracion_inicial = aceleracion_inicial

    def posicion(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la posición en MRUV.
        Ecuación: x = x0 + v0 * t + 0.5 * a * t^2

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
        return self.posicion_inicial + self.velocidad_inicial * tiempo + 0.5 * self.aceleracion_inicial * (tiempo ** 2)

    def velocidad(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la velocidad en MRUV.
        Ecuación: v = v0 + a * t

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`).

        Returns:
            Q_: Velocidad final (cantidad de velocidad).
        
        Raises:
            NegativeTimeError: Si el tiempo es negativo.
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        if tiempo.magnitude < 0:
            raise NegativeTimeError("El tiempo no puede ser negativo.")
        return self.velocidad_inicial + self.aceleracion_inicial * tiempo

    def aceleracion(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la aceleración en MRUV (es constante).
        Ecuación: a = a0

        Args:
            tiempo (Q_): Tiempo transcurrido (ej. `10 * ureg.second`). (Ignorado en MRUV ya que la aceleración es constante)

        Returns:
            Q_: Aceleración (cantidad de aceleración).
        
        Raises:
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        return self.aceleracion_inicial

    def velocidad_sin_tiempo(self, posicion_final: Q_) -> Q_:
        """
        Calcula la velocidad final en MRUV sin conocer el tiempo.
        Ecuación: v^2 = v0^2 + 2 * a * (x - x0)

        Args:
            posicion_final (Q_): Posición final del objeto (ej. `50 * ureg.meter`).

        Returns:
            Q_: Velocidad final (cantidad de velocidad).
        
        Raises:
            PhysicallyImpossibleError: Si la velocidad al cuadrado es negativa, indicando una situación físicamente imposible.
            InvalidPhysicsParameterError: Si la posición final no es una cantidad de longitud.
        """
        if not isinstance(posicion_final, Q_) or not posicion_final.check('[length]'):
            raise InvalidPhysicsParameterError("La posición final debe ser una cantidad de longitud.")
        
        delta_x = posicion_final - self.posicion_inicial
        v_squared = (self.velocidad_inicial ** 2) + 2 * self.aceleracion_inicial * delta_x
        if v_squared.magnitude < 0:
            raise PhysicallyImpossibleError("No se puede calcular la velocidad real (velocidad al cuadrado negativa).")
        return math.sqrt(v_squared.magnitude) * v_squared.units**0.5

    def tiempo_por_posicion(self, posicion_final: Q_) -> tuple[Q_, Q_]:
        """
        Calcula el tiempo a partir de la posición final en MRUV, resolviendo la ecuación cuadrática.
        Ecuación: x = x0 + v0 * t + 0.5 * a * t^2  =>  0.5 * a * t^2 + v0 * t + (x0 - x_f) = 0

        Args:
            posicion_final (Q_): Posición final del objeto (ej. `50 * ureg.meter`).

        Returns:
            tuple[Q_, Q_]: Una tupla con los dos posibles valores de tiempo (cantidad de tiempo).
                                 Si solo hay una solución válida, el segundo valor será `math.nan * ureg.second`.
                                 Si no hay soluciones reales, ambos valores serán `math.nan * ureg.second`.
        
        Raises:
            PhysicallyImpossibleError: Si la aceleración es cero y la velocidad inicial también es cero,
                                       o si el discriminante es negativo (no hay soluciones reales).
            NegativeTimeError: Si el tiempo calculado es negativo.
            InvalidPhysicsParameterError: Si la posición final no es una cantidad de longitud.
        """
        if not isinstance(posicion_final, Q_) or not posicion_final.check('[length]'):
            raise InvalidPhysicsParameterError("La posición final debe ser una cantidad de longitud.")

        a_val = 0.5 * self.aceleracion_inicial.to(ureg.meter / ureg.second**2).magnitude
        b_val = self.velocidad_inicial.to(ureg.meter / ureg.second).magnitude
        c_val = (self.posicion_inicial - posicion_final).to(ureg.meter).magnitude

        if a_val == 0:  # Caso de MRU
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

    def tiempo_por_velocidad(self, velocidad_final: Q_) -> Q_:
        """
        Calcula el tiempo a partir de la velocidad final en MRUV.
        Ecuación: v = v0 + a * t  =>  t = (v - v0) / a

        Args:
            velocidad_final (Q_): Velocidad final del objeto (ej. `20 * ureg.meter / ureg.second`).

        Returns:
            Q_: Tiempo transcurrido (cantidad de tiempo).
        
        Raises:
            PhysicallyImpossibleError: Si la aceleración es cero y la velocidad final no coincide con la inicial.
            NegativeTimeError: Si el tiempo calculado es negativo.
            InvalidPhysicsParameterError: Si la velocidad final no es una cantidad de velocidad.
        """
        if not isinstance(velocidad_final, Q_) or not velocidad_final.check('[length] / [time]'):
            raise InvalidPhysicsParameterError("La velocidad final debe ser una cantidad de velocidad.")

        if self.aceleracion_inicial.magnitude == 0:
            if velocidad_final != self.velocidad_inicial:
                raise PhysicallyImpossibleError("La aceleración es cero, por lo que la velocidad no puede cambiar.")
            return math.inf * ureg.second
        
        tiempo = (velocidad_final - self.velocidad_inicial) / self.aceleracion_inicial
        if tiempo.magnitude < 0:
            raise NegativeTimeError("El tiempo calculado es negativo, lo cual no es físicamente posible.")
        return tiempo.to(ureg.second)

    def desplazamiento_sin_tiempo(self, velocidad_final: Q_) -> Q_:
        """
        Calcula el desplazamiento (delta_x) en MRUV sin conocer el tiempo.
        Ecuación: v_f^2 = v_0^2 + 2 * a * delta_x  =>  delta_x = (v_f^2 - v_0^2) / (2 * a)

        Args:
            velocidad_final (Q_): Velocidad final del objeto (ej. `20 * ureg.meter / ureg.second`).

        Returns:
            Q_: Desplazamiento (cantidad de longitud).
        
        Raises:
            PhysicallyImpossibleError: Si la aceleración es cero y la velocidad final es diferente de la inicial.
            ZeroDivisionError: Si el denominador es cero.
            InvalidPhysicsParameterError: Si la velocidad final no es una cantidad de velocidad.
        """
        if not isinstance(velocidad_final, Q_) or not velocidad_final.check('[length] / [time]'):
            raise InvalidPhysicsParameterError("La velocidad final debe ser una cantidad de velocidad.")

        if self.aceleracion_inicial.magnitude == 0:
            if velocidad_final != self.velocidad_inicial:
                raise PhysicallyImpossibleError("La aceleración es cero, por lo que la velocidad no puede cambiar y el desplazamiento es indefinido si las velocidades son diferentes.")
            return 0.0 * ureg.meter
        
        denominador = 2 * self.aceleracion_inicial
        if denominador.magnitude == 0:
            raise ZeroDivisionError("El denominador es cero, no se puede calcular el desplazamiento.")
        
        delta_x = (velocidad_final**2 - self.velocidad_inicial**2) / denominador
        return delta_x.to(ureg.meter)

    def graficar(self, t_max: Union[float, Q_], num_points: int = 100):
        """
        Genera y muestra gráficos de posición vs. tiempo, velocidad vs. tiempo y aceleración vs. tiempo para MRUV.

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
            plot_mruv(self, t_max.to(ureg.second).magnitude, num_points)
        elif isinstance(t_max, (int, float)):
            if t_max <= 0:
                raise InvalidPhysicsParameterError("El tiempo máximo debe ser positivo para generar el gráfico.")
            plot_mruv(self, t_max, num_points)
        else:
            raise InvalidPhysicsParameterError("El tiempo máximo debe ser un número o una cantidad de tiempo.")
