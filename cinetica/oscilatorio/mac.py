"""
Módulo para el Movimiento Armónico Complejo (MAC).

Este módulo define clases y funciones para simular y analizar el movimiento
armónico complejo, que es la superposición de varios movimientos armónicos simples.
"""

import numpy as np
from typing import Union
from ..exceptions import InvalidPhysicsParameterError
from ..movimiento_base import MovimientoBase
from ..units import ureg, Q_

class MovimientoArmonicoComplejo(MovimientoBase):
    """
    Representa un Movimiento Armónico Complejo (MAC) como la superposición
    de múltiples Movimientos Armónicos Simples (MAS).
    """
    def __init__(self, mas_components: list[dict]):
        """
        Inicializa un objeto de Movimiento Armónico Complejo.

        Args:
            mas_components (list): Una lista de diccionarios, donde cada diccionario
                                   representa un MAS con las siguientes claves:
                                   - 'amplitud' (Q_): Amplitud del MAS (ej. `0.1 * ureg.meter`).
                                   - 'frecuencia_angular' (Q_): Frecuencia angular (ej. `10 * ureg.radian / ureg.second`).
                                   - 'fase_inicial' (Q_): Fase inicial (ej. `0.0 * ureg.radian`).
        
        Raises:
            InvalidPhysicsParameterError: Si `mas_components` no es una lista válida o si alguna componente
                                          MAS no tiene las claves requeridas o valores numéricos/unidades válidos.
        """
        if not isinstance(mas_components, list) or not mas_components:
            raise InvalidPhysicsParameterError("mas_components debe ser una lista no vacía de diccionarios.")
        
        for comp in mas_components:
            if not all(k in comp for k in ['amplitud', 'frecuencia_angular', 'fase_inicial']):
                raise InvalidPhysicsParameterError("Cada componente MAS debe tener 'amplitud', 'frecuencia_angular' y 'fase_inicial'.")
            
            A = comp['amplitud']
            omega = comp['frecuencia_angular']
            phi = comp['fase_inicial']

            if not isinstance(A, Q_) or not A.check('[length]'):
                raise InvalidPhysicsParameterError("La amplitud debe ser una cantidad de longitud.")
            if A.magnitude <= 0:
                raise InvalidPhysicsParameterError("La amplitud debe ser un valor positivo.")
            
            if not isinstance(omega, Q_) or not omega.check('[angle] / [time]'):
                raise InvalidPhysicsParameterError("La frecuencia angular debe ser una cantidad de velocidad angular.")
            if omega.magnitude <= 0:
                raise InvalidPhysicsParameterError("La frecuencia angular debe ser un valor positivo.")
            
            if not isinstance(phi, Q_) or not phi.check('[angle]'):
                raise InvalidPhysicsParameterError("La fase inicial debe ser una cantidad de ángulo.")

        self.mas_components = mas_components

    def posicion(self, tiempo: Union[Q_, np.ndarray]) -> Union[Q_, np.ndarray]:
        """
        Calcula la posición del objeto en un tiempo dado para el MAC.

        Args:
            tiempo (Union[Q_, np.ndarray]): El tiempo o array de tiempos (ej. `10 * ureg.second` o `np.array([1,2])*ureg.second`).

        Returns:
            Union[Q_, np.ndarray]: La posición total en el tiempo especificado (cantidad de longitud o array de cantidades).
        
        Raises:
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo o un array de cantidades de tiempo.
        """
        if isinstance(tiempo, Q_):
            if not tiempo.check('[time]'):
                raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
            tiempo_val = tiempo.to(ureg.second).magnitude
            is_scalar = True
        elif isinstance(tiempo, np.ndarray):
            if not all(isinstance(t, Q_) and t.check('[time]') for t in tiempo.flatten()):
                raise InvalidPhysicsParameterError("Todos los elementos del array de tiempo deben ser cantidades de tiempo.")
            tiempo_val = np.array([t.to(ureg.second).magnitude for t in tiempo.flatten()]).reshape(tiempo.shape)
            is_scalar = False
        else:
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo o un array de cantidades de tiempo.")

        posiciones_val = np.zeros_like(tiempo_val, dtype=float)
        for comp in self.mas_components:
            A = comp['amplitud'].to(ureg.meter).magnitude
            omega = comp['frecuencia_angular'].to(ureg.radian / ureg.second).magnitude
            phi = comp['fase_inicial'].to(ureg.radian).magnitude
            posiciones_val += A * np.cos(omega * tiempo_val + phi)
        
        if is_scalar:
            return posiciones_val * ureg.meter
        else:
            return posiciones_val * ureg.meter

    def velocidad(self, tiempo: Union[Q_, np.ndarray]) -> Union[Q_, np.ndarray]:
        """
        Calcula la velocidad del objeto en un tiempo dado para el MAC.

        Args:
            tiempo (Union[Q_, np.ndarray]): El tiempo o array de tiempos (ej. `10 * ureg.second` o `np.array([1,2])*ureg.second`).

        Returns:
            Union[Q_, np.ndarray]: La velocidad total en el tiempo especificado (cantidad de velocidad o array de cantidades).
        
        Raises:
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo o un array de cantidades de tiempo.
        """
        if isinstance(tiempo, Q_):
            if not tiempo.check('[time]'):
                raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
            tiempo_val = tiempo.to(ureg.second).magnitude
            is_scalar = True
        elif isinstance(tiempo, np.ndarray):
            if not all(isinstance(t, Q_) and t.check('[time]') for t in tiempo.flatten()):
                raise InvalidPhysicsParameterError("Todos los elementos del array de tiempo deben ser cantidades de tiempo.")
            tiempo_val = np.array([t.to(ureg.second).magnitude for t in tiempo.flatten()]).reshape(tiempo.shape)
            is_scalar = False
        else:
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo o un array de cantidades de tiempo.")

        velocidades_val = np.zeros_like(tiempo_val, dtype=float)
        for comp in self.mas_components:
            A = comp['amplitud'].to(ureg.meter).magnitude
            omega = comp['frecuencia_angular'].to(ureg.radian / ureg.second).magnitude
            phi = comp['fase_inicial'].to(ureg.radian).magnitude
            velocidades_val += -A * omega * np.sin(omega * tiempo_val + phi)
        
        if is_scalar:
            return velocidades_val * ureg.meter / ureg.second
        else:
            return velocidades_val * ureg.meter / ureg.second

    def aceleracion(self, tiempo: Union[Q_, np.ndarray]) -> Union[Q_, np.ndarray]:
        """
        Calcula la aceleración del objeto en un tiempo dado para el MAC.

        Args:
            tiempo (Union[Q_, np.ndarray]): El tiempo o array de tiempos (ej. `10 * ureg.second` o `np.array([1,2])*ureg.second`).

        Returns:
            Union[Q_, np.ndarray]: La aceleración total en el tiempo especificado (cantidad de aceleración o array de cantidades).
        
        Raises:
            InvalidPhysicsParameterError: Si el tiempo no es una cantidad de tiempo o un array de cantidades de tiempo.
        """
        if isinstance(tiempo, Q_):
            if not tiempo.check('[time]'):
                raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo.")
            tiempo_val = tiempo.to(ureg.second).magnitude
            is_scalar = True
        elif isinstance(tiempo, np.ndarray):
            if not all(isinstance(t, Q_) and t.check('[time]') for t in tiempo.flatten()):
                raise InvalidPhysicsParameterError("Todos los elementos del array de tiempo deben ser cantidades de tiempo.")
            tiempo_val = np.array([t.to(ureg.second).magnitude for t in tiempo.flatten()]).reshape(tiempo.shape)
            is_scalar = False
        else:
            raise InvalidPhysicsParameterError("El tiempo debe ser una cantidad de tiempo o un array de cantidades de tiempo.")

        aceleraciones_val = np.zeros_like(tiempo_val, dtype=float)
        for comp in self.mas_components:
            A = comp['amplitud'].to(ureg.meter).magnitude
            omega = comp['frecuencia_angular'].to(ureg.radian / ureg.second).magnitude
            phi = comp['fase_inicial'].to(ureg.radian).magnitude
            aceleraciones_val += -A * (omega**2) * np.cos(omega * tiempo_val + phi)
        
        if is_scalar:
            return aceleraciones_val * ureg.meter / ureg.second**2
        else:
            return aceleraciones_val * ureg.meter / ureg.second**2

# Ejemplo de uso (opcional, para demostración)
if __name__ == "__main__":
    # Definir componentes MAS
    componente1 = {'amplitud': 2.0, 'frecuencia_angular': 1.0, 'fase_inicial': 0.0}
    componente2 = {'amplitud': 1.0, 'frecuencia_angular': 3.0, 'fase_inicial': np.pi / 2}
    componente3 = {'amplitud': 0.5, 'frecuencia_angular': 5.0, 'fase_inicial': np.pi}

    mac = MovimientoArmonicoComplejo([componente1, componente2, componente3])

    tiempos = np.linspace(0, 10, 500)

    posiciones = mac.posicion(tiempos)
    velocidades = mac.velocidad(tiempos)
    aceleraciones = mac.aceleracion(tiempos)

    print(f"Posición en t=0: {mac.posicion(0):.4f}")
    print(f"Velocidad en t=0: {mac.velocidad(0):.4f}")
    print(f"Aceleración en t=0: {mac.aceleracion(0):.4f}")

    # Puedes graficar estos resultados para visualizarlos
    # import matplotlib.pyplot as plt
    # plt.figure(figsize=(10, 6))
    # plt.plot(tiempos, posiciones, label='Posición')
    # plt.plot(tiempos, velocidades, label='Velocidad')
    # plt.plot(tiempos, aceleraciones, label='Aceleración')
    # plt.title('Movimiento Armónico Complejo')
    # plt.xlabel('Tiempo (s)')
    # plt.ylabel('Magnitud')
    # plt.legend()
    # plt.grid(True)
    # plt.show()
