import numpy as np
from ..base_movimiento import Movimiento

class MovimientoEspacial(Movimiento):
    """
    Clase para simular y calcular la trayectoria de un objeto en 3D
    utilizando vectores de posición, velocidad y aceleración.
    """

    def __init__(self,
                 posicion_inicial: np.ndarray = np.array([0.0, 0.0, 0.0]),
                 velocidad_inicial: np.ndarray = np.array([0.0, 0.0, 0.0]),
                 aceleracion_constante: np.ndarray = np.array([0.0, 0.0, 0.0])):
        """
        Inicializa el objeto MovimientoEspacial con vectores de condiciones iniciales.

        Args:
            posicion_inicial (np.ndarray): Vector de posición inicial (m).
            velocidad_inicial (np.ndarray): Vector de velocidad inicial (m/s).
            aceleracion_constante (np.ndarray): Vector de aceleración constante (m/s^2).
        
        Raises:
            ValueError: Si los vectores no son de 3 dimensiones.
        """
        if not (len(posicion_inicial) == 3 and len(velocidad_inicial) == 3 and len(aceleracion_constante) == 3):
            raise ValueError("Todos los vectores (posición, velocidad, aceleración) deben ser de 3 dimensiones.")

        self.posicion_inicial = np.array(posicion_inicial, dtype=float)
        self.velocidad_inicial = np.array(velocidad_inicial, dtype=float)
        self.aceleracion_constante = np.array(aceleracion_constante, dtype=float)

    def graficar(self, t_max: float = 10.0, num_points: int = 100):
        """
        Grafica la trayectoria del movimiento en 3D.

        Args:
            t_max (float): Tiempo máximo a graficar (s).
            num_points (int): Número de puntos a graficar.
        """
        import matplotlib.pyplot as plt

        t = np.linspace(0, t_max, num_points)
        posiciones = np.array([self.posicion(ti) for ti in t])

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2])
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('Trayectoria en 3D')
        plt.show()

    def posicion(self, tiempo: float) -> np.ndarray:
        """
        Calcula el vector de posición en un tiempo dado.
        Ecuación: r = r0 + v0 * t + 0.5 * a * t^2

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            np.ndarray: Vector de posición (m).
        
        Raises:
            ValueError: Si el tiempo es negativo.
        """
        if tiempo < 0:
            raise ValueError("El tiempo no puede ser negativo.")
        return self.posicion_inicial + self.velocidad_inicial * tiempo + 0.5 * self.aceleracion_constante * (tiempo ** 2)

    def velocidad(self, tiempo: float) -> np.ndarray:
        """
        Calcula el vector de velocidad en un tiempo dado.
        Ecuación: v = v0 + a * t

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            np.ndarray: Vector de velocidad (m/s).
        
        Raises:
            ValueError: Si el tiempo es negativo.
        """
        if tiempo < 0:
            raise ValueError("El tiempo no puede ser negativo.")
        return self.velocidad_inicial + self.aceleracion_constante * tiempo

    def aceleracion(self, tiempo: float = None) -> np.ndarray:
        """
        Retorna el vector de aceleración (es constante).
        Ecuación: a = a_constante

        Args:
            tiempo (float, optional): Tiempo transcurrido (s). No afecta al resultado.

        Returns:
            np.ndarray: Vector de aceleración (m/s^2).
        """
        # La aceleración es constante, no depende del tiempo
        return self.aceleracion_constante

    def magnitud_aceleracion(self) -> float:
        """
        Calcula la magnitud del vector aceleración.

        Returns:
            float: Magnitud de la aceleración (m/s²).
        """
        return float(np.linalg.norm(self.aceleracion_constante))

    def magnitud_velocidad(self, tiempo: float) -> float:
        """
        Calcula la magnitud de la velocidad en un tiempo dado.

        Args:
            tiempo (float): Tiempo transcurrido (s).

        Returns:
            float: Magnitud de la velocidad (m/s).
        """
        return np.linalg.norm(self.velocidad(tiempo))

    def magnitud_aceleracion_constante(self) -> float:
        """
        Calcula la magnitud de la aceleración constante.

        Returns:
            float: Magnitud de la aceleración (m/s^2).
        """
        return np.linalg.norm(self.aceleracion_constante)
