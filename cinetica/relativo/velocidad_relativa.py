import numpy as np
from typing import Union
from ..exceptions import InvalidPhysicsParameterError, ZeroDivisionError
from ..units import ureg, Q_

class MovimientoRelativo:
    """
    Clase para calcular velocidades relativas entre objetos.
    Permite trabajar con vectores de velocidad en 2D o 3D.
    """

    def __init__(self):
        """
        Inicializa la clase MovimientoRelativo.
        No requiere parámetros iniciales ya que los vectores de velocidad
        se pasan directamente a los métodos de cálculo.
        """
        pass

    def _validate_velocity_vector(self, vector: Union[list, np.ndarray, Q_], name: str) -> np.ndarray:
        """Valida que el input sea un vector de velocidad con unidades correctas."""
        if isinstance(vector, Q_):
            if not vector.check('[length] / [time]'):
                raise InvalidPhysicsParameterError(f"El vector de {name} debe ser una cantidad de velocidad.")
            return np.array([vector.to(ureg.meter / ureg.second).magnitude]) if vector.dimensionless else np.array([vector.to(ureg.meter / ureg.second).magnitude]) # Simplified for now, needs proper handling for vector quantities
        elif isinstance(vector, (list, np.ndarray)):
            # Assume SI units if no pint quantity is provided, or convert if mixed
            # For simplicity, we'll assume raw floats/lists are in m/s for now.
            # A more robust solution would require all inputs to be Q_ objects.
            return np.array(vector)
        else:
            raise InvalidPhysicsParameterError(f"El {name} debe ser una lista, un array de numpy o una cantidad de Pint.")

    def velocidad_relativa(self, velocidad_objeto_a: Union[list, np.ndarray, Q_], velocidad_objeto_b: Union[list, np.ndarray, Q_]) -> Union[np.ndarray, Q_]:
        """
        Calcula la velocidad del objeto A con respecto al objeto B (V_A/B).
        V_A/B = V_A - V_B

        :param velocidad_objeto_a: Vector de velocidad del objeto A (lista, array de numpy o cantidad de Pint).
        :param velocidad_objeto_b: Vector de velocidad del objeto B (lista, array de numpy o cantidad de Pint).
        :return: Vector de velocidad relativa de A con respecto a B (array de numpy o cantidad de Pint).
        :raises InvalidPhysicsParameterError: Si los vectores de velocidad no tienen la misma dimensión o unidades incorrectas.
        """
        v_a = self._validate_velocity_vector(velocidad_objeto_a, "velocidad del objeto A")
        v_b = self._validate_velocity_vector(velocidad_objeto_b, "velocidad del objeto B")

        if v_a.shape != v_b.shape:
            raise InvalidPhysicsParameterError("Los vectores de velocidad deben tener la misma dimensión.")
        
        result = v_a - v_b
        if isinstance(velocidad_objeto_a, Q_): # If input was a pint quantity, return a pint quantity
            return result[0] * ureg.meter / ureg.second if result.size == 1 else result * ureg.meter / ureg.second
        return result

    def velocidad_absoluta_a(self, velocidad_relativa_ab: Union[list, np.ndarray, Q_], velocidad_objeto_b: Union[list, np.ndarray, Q_]) -> Union[np.ndarray, Q_]:
        """
        Calcula la velocidad absoluta del objeto A (V_A) dado V_A/B y V_B.
        V_A = V_A/B + V_B

        :param velocidad_relativa_ab: Vector de velocidad de A con respecto a B (lista, array de numpy o cantidad de Pint).
        :param velocidad_objeto_b: Vector de velocidad del objeto B (lista, array de numpy o cantidad de Pint).
        :return: Vector de velocidad absoluta del objeto A (array de numpy o cantidad de Pint).
        :raises InvalidPhysicsParameterError: Si los vectores de velocidad no tienen la misma dimensión o unidades incorrectas.
        """
        v_ab = self._validate_velocity_vector(velocidad_relativa_ab, "velocidad relativa A/B")
        v_b = self._validate_velocity_vector(velocidad_objeto_b, "velocidad del objeto B")

        if v_ab.shape != v_b.shape:
            raise InvalidPhysicsParameterError("Los vectores de velocidad deben tener la misma dimensión.")
        
        result = v_ab + v_b
        if isinstance(velocidad_relativa_ab, Q_):
            return result[0] * ureg.meter / ureg.second if result.size == 1 else result * ureg.meter / ureg.second
        return result

    def velocidad_absoluta_b(self, velocidad_objeto_a: Union[list, np.ndarray, Q_], velocidad_relativa_ab: Union[list, np.ndarray, Q_]) -> Union[np.ndarray, Q_]:
        """
        Calcula la velocidad absoluta del objeto B (V_B) dado V_A y V_A/B.
        V_B = V_A - V_A/B

        :param velocidad_objeto_a: Vector de velocidad del objeto A (lista, array de numpy o cantidad de Pint).
        :param velocidad_relativa_ab: Vector de velocidad de A con respecto a B (lista, array de numpy o cantidad de Pint).
        :return: Vector de velocidad absoluta del objeto B (array de numpy o cantidad de Pint).
        :raises InvalidPhysicsParameterError: Si los vectores de velocidad no tienen la misma dimensión o unidades incorrectas.
        """
        v_a = self._validate_velocity_vector(velocidad_objeto_a, "velocidad del objeto A")
        v_ab = self._validate_velocity_vector(velocidad_relativa_ab, "velocidad relativa A/B")

        if v_a.shape != v_ab.shape:
            raise InvalidPhysicsParameterError("Los vectores de velocidad deben tener la misma dimensión.")
        
        result = v_a - v_ab
        if isinstance(velocidad_objeto_a, Q_):
            return result[0] * ureg.meter / ureg.second if result.size == 1 else result * ureg.meter / ureg.second
        return result

    def magnitud_velocidad(self, velocidad_vector: Union[list, np.ndarray, Q_]) -> Q_:
        """
        Calcula la magnitud de un vector de velocidad.

        :param velocidad_vector: Vector de velocidad (lista, array de numpy o cantidad de Pint).
        :return: Magnitud del vector de velocidad (cantidad de velocidad).
        :raises InvalidPhysicsParameterError: Si el vector no es una cantidad de velocidad o tiene unidades incorrectas.
        """
        if isinstance(velocidad_vector, Q_):
            if not velocidad_vector.check('[length] / [time]'):
                raise InvalidPhysicsParameterError("El vector de velocidad debe ser una cantidad de velocidad.")
            return np.linalg.norm(velocidad_vector.to(ureg.meter / ureg.second).magnitude) * ureg.meter / ureg.second
        elif isinstance(velocidad_vector, (list, np.ndarray)):
            # Assume SI units if no pint quantity is provided
            return np.linalg.norm(velocidad_vector) * ureg.meter / ureg.second
        else:
            raise InvalidPhysicsParameterError("El vector de velocidad debe ser una lista, un array de numpy o una cantidad de Pint.")

    def direccion_velocidad(self, velocidad_vector: Union[list, np.ndarray, Q_]) -> Union[Q_, np.ndarray]:
        """
        Calcula la dirección de un vector de velocidad en 2D (ángulo en radianes).
        Para 3D, devuelve el vector unitario.

        :param velocidad_vector: Vector de velocidad (lista, array de numpy o cantidad de Pint).
        :return: Ángulo en radianes para 2D (cantidad de ángulo), o vector unitario para 3D (array de numpy).
        :raises ZeroDivisionError: Si la magnitud del vector de velocidad es cero.
        :raises InvalidPhysicsParameterError: Si el vector es de dimensión 0 o unidades incorrectas.
        """
        if isinstance(velocidad_vector, Q_):
            if not velocidad_vector.check('[length] / [time]'):
                raise InvalidPhysicsParameterError("El vector de velocidad debe ser una cantidad de velocidad.")
            v = np.array([velocidad_vector.to(ureg.meter / ureg.second).magnitude])
            norm = np.linalg.norm(v)
            if norm == 0:
                raise ZeroDivisionError("No se puede determinar la dirección para un vector de velocidad cero.")
            return v / norm * ureg.dimensionless # Return dimensionless for unit vector
        elif isinstance(velocidad_vector, (list, np.ndarray)):
            v = np.array(velocidad_vector)
            norm = np.linalg.norm(v)

            if norm == 0:
                if len(v) == 2:
                    raise ZeroDivisionError("No se puede determinar la dirección para un vector de velocidad cero en 2D.")
                else:
                    raise ZeroDivisionError("No se puede determinar la dirección para un vector de velocidad cero en 3D.")

            if len(v) == 2:
                return np.arctan2(v[1], v[0]) * ureg.radian
            else:
                return v / norm
        else:
            raise InvalidPhysicsParameterError("El vector de velocidad debe ser una lista, un array de numpy o una cantidad de Pint.")
