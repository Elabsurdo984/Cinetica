import math
from typing import Union
from ..exceptions import InvalidPhysicsParameterError
from ..movimiento_base import MovimientoBase
from ..units import ureg, Q_

class MovimientoArmonicoSimple(MovimientoBase):
    """
    Clase para calcular la posición, velocidad y aceleración en un Movimiento Armónico Simple (M.A.S.).
    """

    def __init__(self, amplitud: Q_, frecuencia_angular: Q_, fase_inicial: Q_ = 0.0 * ureg.radian):
        """
        Inicializa el objeto de Movimiento Armónico Simple.

        :param amplitud: Amplitud del movimiento (ej. `0.1 * ureg.meter`).
        :param frecuencia_angular: Frecuencia angular (ej. `10 * ureg.radian / ureg.second`).
        :param fase_inicial: Fase inicial (ej. `0.0 * ureg.radian`). Por defecto es 0.
        
        Raises:
            InvalidPhysicsParameterError: Si la amplitud o la frecuencia angular son menores o iguales a cero
                                          o las unidades son incorrectas.
        """
        if not isinstance(amplitud, Q_) or not amplitud.check('[length]'):
            raise InvalidPhysicsParameterError("La amplitud debe ser una cantidad de longitud.")
        if amplitud.magnitude <= 0:
            raise InvalidPhysicsParameterError("La amplitud debe ser un valor positivo.")
        if not isinstance(frecuencia_angular, Q_) or not frecuencia_angular.check('[angle] / [time]'):
            raise InvalidPhysicsParameterError("La frecuencia angular debe ser una cantidad de velocidad angular.")
        if frecuencia_angular.magnitude <= 0:
            raise InvalidPhysicsParameterError("La frecuencia angular debe ser un valor positivo.")
        if not isinstance(fase_inicial, Q_) or not fase_inicial.check('[angle]'):
            raise InvalidPhysicsParameterError("La fase inicial debe ser una cantidad de ángulo.")

        self.amplitud = amplitud
        self.frecuencia_angular = frecuencia_angular
        self.fase_inicial = fase_inicial

    def posicion(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la posición (x) en un tiempo dado.

        x(t) = A * cos(ωt + φ)

        :param tiempo: Tiempo (ej. `10 * ureg.second`).
        :return: Posición en el tiempo dado (cantidad de longitud).
        
        Raises:
            NegativeTimeError: Si el tiempo es negativo.
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        if tiempo.magnitude < 0:
            raise NegativeTimeError("El tiempo no puede ser negativo.")
        return self.amplitud * math.cos((self.frecuencia_angular * tiempo + self.fase_inicial).to(ureg.radian).magnitude)

    def velocidad(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la velocidad (v) en un tiempo dado.

        v(t) = -A * ω * sen(ωt + φ)

        :param tiempo: Tiempo (ej. `10 * ureg.second`).
        :return: Velocidad en el tiempo dado (cantidad de velocidad).
        
        Raises:
            NegativeTimeError: Si el tiempo es negativo.
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        if tiempo.magnitude < 0:
            raise NegativeTimeError("El tiempo no puede ser negativo.")
        return -self.amplitud * self.frecuencia_angular * math.sin((self.frecuencia_angular * tiempo + self.fase_inicial).to(ureg.radian).magnitude)

    def aceleracion(self, tiempo: Q_ = 0.0 * ureg.second) -> Q_:
        """
        Calcula la aceleración (a) en un tiempo dado.

        a(t) = -A * ω^2 * cos(ωt + φ) = -ω^2 * x(t)

        :param tiempo: Tiempo (ej. `10 * ureg.second`).
        :return: Aceleración en el tiempo dado (cantidad de aceleración).
        
        Raises:
            NegativeTimeError: Si el tiempo es negativo.
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo.
        """
        if not isinstance(tiempo, Q_) or not tiempo.check('[time]'):
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
        if tiempo.magnitude < 0:
            raise NegativeTimeError("El tiempo no puede ser negativo.")
        return -self.amplitud * (self.frecuencia_angular ** 2) * math.cos((self.frecuencia_angular * tiempo + self.fase_inicial).to(ureg.radian).magnitude)

    def periodo(self) -> Q_:
        """
        Calcula el período (T) del movimiento.

        T = 2π / ω

        :return: Período del movimiento (cantidad de tiempo).
        """
        return (2 * math.pi * ureg.radian) / self.frecuencia_angular

    def frecuencia(self) -> Q_:
        """
        Calcula la frecuencia (f) del movimiento.

        f = 1 / T = ω / (2π)

        :return: Frecuencia del movimiento (cantidad de frecuencia).
        """
        return self.frecuencia_angular / (2 * math.pi * ureg.radian)

    def energia_cinetica(self, tiempo: Q_, masa: Q_) -> Q_:
        """
        Calcula la energía cinética (Ec) en un tiempo dado.

        Ec = 0.5 * m * v(t)^2

        :param tiempo: Tiempo (ej. `10 * ureg.second`).
        :param masa: Masa del objeto (ej. `1 * ureg.kilogram`).
        :return: Energía cinética en Joules (cantidad de energía).
        
        Raises:
            InvalidPhysicsParameterError: Si la masa es menor o igual a cero o las unidades son incorrectas.
            NegativeTimeError: Si el tiempo es negativo.
        """
        if not isinstance(masa, Q_) or not masa.check('[mass]'):
            raise InvalidPhysicsParameterError("La masa debe ser una cantidad de masa.")
        if masa.magnitude <= 0:
            raise InvalidPhysicsParameterError("La masa debe ser un valor positivo.")
        return 0.5 * masa * (self.velocidad(tiempo) ** 2)

    def energia_potencial(self, tiempo: Q_, constante_elastica: Q_) -> Q_:
        """
        Calcula la energía potencial elástica (Ep) en un tiempo dado.

        Ep = 0.5 * k * x(t)^2

        :param tiempo: Tiempo (ej. `10 * ureg.second`).
        :param constante_elastica: Constante elástica (ej. `100 * ureg.newton / ureg.meter`).
        :return: Energía potencial en Joules (cantidad de energía).
        
        Raises:
            InvalidPhysicsParameterError: Si la constante elástica es menor o igual a cero o las unidades son incorrectas.
            NegativeTimeError: Si el tiempo es negativo.
        """
        if not isinstance(constante_elastica, Q_) or not constante_elastica.check('[mass] / [time]**2'):
            raise InvalidPhysicsParameterError("La constante elástica debe ser una cantidad de fuerza por longitud.")
        if constante_elastica.magnitude <= 0:
            raise InvalidPhysicsParameterError("La constante elástica debe ser un valor positivo.")
        return 0.5 * constante_elastica * (self.posicion(tiempo) ** 2)

    def energia_total(self, masa: Q_, constante_elastica: Q_) -> Q_:
        """
        Calcula la energía mecánica total (E) del sistema.

        E = 0.5 * k * A^2 = 0.5 * m * A^2 * ω^2

        :param masa: Masa del objeto (ej. `1 * ureg.kilogram`).
        :param constante_elastica: Constante elástica (ej. `100 * ureg.newton / ureg.meter`).
        :return: Energía total en Joules (cantidad de energía).
        
        Raises:
            InvalidPhysicsParameterError: Si la masa o la constante elástica son menores o iguales a cero
                                          o las unidades son incorrectas.
        """
        if not isinstance(masa, Q_) or not masa.check('[mass]'):
            raise InvalidPhysicsParameterError("La masa debe ser una cantidad de masa.")
        if not isinstance(constante_elastica, Q_) or not constante_elastica.check('[mass] / [time]**2'):
            raise InvalidPhysicsParameterError("La constante elástica debe ser una cantidad de fuerza por longitud.")
        if masa.magnitude <= 0 or constante_elastica.magnitude <= 0:
            raise InvalidPhysicsParameterError("La masa y la constante elástica deben ser valores positivos.")
        return 0.5 * constante_elastica * (self.amplitud ** 2)
