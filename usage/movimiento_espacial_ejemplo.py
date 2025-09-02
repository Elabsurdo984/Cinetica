import numpy as np
from cinetica.espacial import MovimientoEspacial

def main():
    """
    Ejemplo de uso de la clase MovimientoEspacial para simular un objeto en 3D.
    """
    print("--- Ejemplo de Movimiento Espacial (3D) ---")

    # Definir condiciones iniciales
    posicion_inicial = np.array([0.0, 0.0, 10.0])  # Parte de (0,0,10)
    velocidad_inicial = np.array([5.0, 2.0, 0.0])  # Velocidad inicial en X, Y
    aceleracion_constante = np.array([0.0, 0.0, -9.81]) # Aceleración de la gravedad en Z

    # Crear una instancia de MovimientoEspacial
    movimiento_3d = MovimientoEspacial(
        posicion_inicial=posicion_inicial,
        velocidad_inicial=velocidad_inicial,
        aceleracion_constante=aceleracion_constante
    )

    print(f"Posición inicial: {movimiento_3d.posicion_inicial}")
    print(f"Velocidad inicial: {movimiento_3d.velocidad_inicial}")
    print(f"Aceleración constante: {movimiento_3d.aceleracion_constante}")

    # Calcular posición y velocidad en diferentes tiempos
    tiempos = [0, 0.5, 1.0, 1.5, 2.0]

    for t in tiempos:
        pos = movimiento_3d.posicion(tiempo=t)
        vel = movimiento_3d.velocidad(tiempo=t)
        mag_vel = movimiento_3d.magnitud_velocidad(tiempo=t)
        print(f"\n--- Tiempo = {t} s ---")
        print(f"Posición: {pos}")
        print(f"Velocidad: {vel}")
        print(f"Magnitud de la velocidad: {mag_vel:.2f} m/s")

    # Calcular la magnitud de la aceleración
    mag_acel = movimiento_3d.magnitud_aceleracion()
    print(f"\nMagnitud de la aceleración: {mag_acel:.2f} m/s^2")

    # Ejemplo de un caso de error (tiempo negativo)
    try:
        movimiento_3d.posicion(tiempo=-1)
    except ValueError as e:
        print(f"\nError esperado al usar tiempo negativo: {e}")

if __name__ == "__main__":
    main()
