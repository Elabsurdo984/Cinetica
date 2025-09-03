import numpy as np

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

    def velocidad_relativa(self, velocidad_objeto_a, velocidad_objeto_b):
        """
        Calcula la velocidad del objeto A con respecto al objeto B (V_A/B).
        V_A/B = V_A - V_B

        :param velocidad_objeto_a: Vector de velocidad del objeto A (lista o array de numpy).
        :param velocidad_objeto_b: Vector de velocidad del objeto B (lista o array de numpy).
        :return: Vector de velocidad relativa de A con respecto a B.
        :raises ValueError: Si los vectores de velocidad no tienen la misma dimensión.
        """
        v_a = np.array(velocidad_objeto_a)
        v_b = np.array(velocidad_objeto_b)

        if v_a.shape != v_b.shape:
            raise ValueError("Los vectores de velocidad deben tener la misma dimensión.")

        return v_a - v_b

    def velocidad_absoluta_a(self, velocidad_relativa_ab, velocidad_objeto_b):
        """
        Calcula la velocidad absoluta del objeto A (V_A) dado V_A/B y V_B.
        V_A = V_A/B + V_B

        :param velocidad_relativa_ab: Vector de velocidad de A con respecto a B.
        :param velocidad_objeto_b: Vector de velocidad del objeto B.
        :return: Vector de velocidad absoluta del objeto A.
        :raises ValueError: Si los vectores de velocidad no tienen la misma dimensión.
        """
        v_ab = np.array(velocidad_relativa_ab)
        v_b = np.array(velocidad_objeto_b)

        if v_ab.shape != v_b.shape:
            raise ValueError("Los vectores de velocidad deben tener la misma dimensión.")

        return v_ab + v_b

    def velocidad_absoluta_b(self, velocidad_objeto_a, velocidad_relativa_ab):
        """
        Calcula la velocidad absoluta del objeto B (V_B) dado V_A y V_A/B.
        V_B = V_A - V_A/B

        :param velocidad_objeto_a: Vector de velocidad del objeto A.
        :param velocidad_relativa_ab: Vector de velocidad de A con respecto a B.
        :return: Vector de velocidad absoluta del objeto B.
        :raises ValueError: Si los vectores de velocidad no tienen la misma dimensión.
        """
        v_a = np.array(velocidad_objeto_a)
        v_ab = np.array(velocidad_relativa_ab)

        if v_a.shape != v_ab.shape:
            raise ValueError("Los vectores de velocidad deben tener la misma dimensión.")

        return v_a - v_ab

    def magnitud_velocidad(self, velocidad_vector):
        """
        Calcula la magnitud de un vector de velocidad.

        :param velocidad_vector: Vector de velocidad (lista o array de numpy).
        :return: Magnitud del vector de velocidad.
        """
        return np.linalg.norm(velocidad_vector)

    def direccion_velocidad(self, velocidad_vector):
        """
        Calcula la dirección de un vector de velocidad en 2D (ángulo en radianes).
        Para 3D, devuelve el vector unitario.

        :param velocidad_vector: Vector de velocidad (lista o array de numpy).
        :return: Ángulo en radianes para 2D, o vector unitario para 3D.
        :raises ValueError: Si el vector es de dimensión 0.
        """
        v = np.array(velocidad_vector)
        norm = np.linalg.norm(v)

        if norm == 0:
            if len(v) == 2:
                return 0.0 # O se podría lanzar un error o devolver None
            else:
                return np.zeros_like(v) # Vector nulo para 3D

        if len(v) == 2:
            return np.arctan2(v[1], v[0])
        else:
            return v / norm
