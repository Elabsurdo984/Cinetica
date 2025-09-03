"""
Módulo para el Movimiento Armónico Complejo (MAC).

Este módulo define clases y funciones para simular y analizar el movimiento
armónico complejo, que es la superposición de varios movimientos armónicos simples.
"""

import numpy as np

class MovimientoArmonicoComplejo:
    """
    Representa un Movimiento Armónico Complejo (MAC) como la superposición
    de múltiples Movimientos Armónicos Simples (MAS).
    """
    def __init__(self, mas_components):
        """
        Inicializa un objeto de Movimiento Armónico Complejo.

        Args:
            mas_components (list): Una lista de diccionarios, donde cada diccionario
                                   representa un MAS con las siguientes claves:
                                   - 'amplitud' (float): Amplitud del MAS.
                                   - 'frecuencia_angular' (float): Frecuencia angular (omega) del MAS.
                                   - 'fase_inicial' (float): Fase inicial (phi) del MAS en radianes.
        """
        if not isinstance(mas_components, list) or not mas_components:
            raise ValueError("mas_components debe ser una lista no vacía de diccionarios.")
        
        for comp in mas_components:
            if not all(k in comp for k in ['amplitud', 'frecuencia_angular', 'fase_inicial']):
                raise ValueError("Cada componente MAS debe tener 'amplitud', 'frecuencia_angular' y 'fase_inicial'.")
            if not all(isinstance(comp[k], (int, float)) for k in ['amplitud', 'frecuencia_angular', 'fase_inicial']):
                raise ValueError("Los valores de amplitud, frecuencia_angular y fase_inicial deben ser numéricos.")

        self.mas_components = mas_components

    def posicion(self, tiempo):
        """
        Calcula la posición del objeto en un tiempo dado para el MAC.

        Args:
            tiempo (float or np.ndarray): El tiempo o array de tiempos en segundos.

        Returns:
            float or np.ndarray: La posición total en el tiempo especificado.
        """
        posiciones = np.zeros_like(np.array(tiempo, dtype=float))
        for comp in self.mas_components:
            A = comp['amplitud']
            omega = comp['frecuencia_angular']
            phi = comp['fase_inicial']
            posiciones += A * np.cos(omega * tiempo + phi)
        return posiciones

    def velocidad(self, tiempo):
        """
        Calcula la velocidad del objeto en un tiempo dado para el MAC.

        Args:
            tiempo (float or np.ndarray): El tiempo o array de tiempos en segundos.

        Returns:
            float or np.ndarray: La velocidad total en el tiempo especificado.
        """
        velocidades = np.zeros_like(np.array(tiempo, dtype=float))
        for comp in self.mas_components:
            A = comp['amplitud']
            omega = comp['frecuencia_angular']
            phi = comp['fase_inicial']
            velocidades += -A * omega * np.sin(omega * tiempo + phi)
        return velocidades

    def aceleracion(self, tiempo):
        """
        Calcula la aceleración del objeto en un tiempo dado para el MAC.

        Args:
            tiempo (float or np.ndarray): El tiempo o array de tiempos en segundos.

        Returns:
            float or np.ndarray: La aceleración total en el tiempo especificado.
        """
        aceleraciones = np.zeros_like(np.array(tiempo, dtype=float))
        for comp in self.mas_components:
            A = comp['amplitud']
            omega = comp['frecuencia_angular']
            phi = comp['fase_inicial']
            aceleraciones += -A * (omega**2) * np.cos(omega * tiempo + phi)
        return aceleraciones

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
