"""
Ejemplo de uso del módulo ChoquesColisiones

Este script muestra cómo utilizar las diferentes funcionalidades del módulo de choques
y colisiones de la biblioteca Cinetica.
"""

import numpy as np
from cinetica.dinamica import ChoquesColisiones

# Crear una instancia del módulo de choques
choques = ChoquesColisiones()

def mostrar_resultados_1d(m1, v1i, m2, v2i, e, v1f, v2f):
    """Muestra los resultados de una colisión 1D de forma formateada."""
    print(f"\n{'='*50}")
    print("COLISIÓN UNIDIMENSIONAL")
    print(f"Masa 1: {m1} kg, Velocidad inicial: {v1i} m/s")
    print(f"Masa 2: {m2} kg, Velocidad inicial: {v2i} m/s")
    print(f"Coeficiente de restitución: {e}")
    print(f"\nVelocidad final 1: {v1f:.2f} m/s")
    print(f"Velocidad final 2: {v2f:.2f} m/s")
    print(f"Momento lineal inicial: {m1*v1i + m2*v2i:.2f} kg·m/s")
    print(f"Momento lineal final: {m1*v1f + m2*v2f:.2f} kg·m/s")
    
    # Calcular energía cinética perdida
    energia_perdida = choques.energia_cinetica_perdida(
        m1, v1i, m2, v2i, v1f, v2f
    )
    print(f"Energía cinética perdida: {energia_perdida:.2f} J")

def ejemplo_colision_1d():
    """Ejemplo de colisión unidimensional."""
    print("\n" + "="*50)
    print("EJEMPLO 1: COLISIÓN UNIDIMENSIONAL")
    
    # Parámetros de la colisión
    m1 = 2.0  # kg
    v1i = 3.0  # m/s
    m2 = 5.0   # kg
    v2i = -1.0 # m/s
    
    # 1. Colisión perfectamente elástica (e = 1.0)
    e = 1.0
    v1f, v2f = choques.colision_unidimensional(m1, v1i, m2, v2i, e)
    mostrar_resultados_1d(m1, v1i, m2, v2i, e, v1f, v2f)
    
    # 2. Colisión perfectamente inelástica (e = 0.0)
    e = 0.0
    v1f, v2f = choques.colision_unidimensional(m1, v1i, m2, v2i, e)
    mostrar_resultados_1d(m1, v1i, m2, v2i, e, v1f, v2f)
    
    # 3. Colisión parcialmente elástica (0 < e < 1)
    e = 0.7
    v1f, v2f = choques.colision_unidimensional(m1, v1i, m2, v2i, e)
    mostrar_resultados_1d(m1, v1i, m2, v2i, e, v1f, v2f)

def ejemplo_colision_2d():
    """Ejemplo de colisión bidimensional."""
    print("\n" + "="*50)
    print("EJEMPLO 2: COLISIÓN BIDIMENSIONAL")
    
    # Parámetros de la colisión
    m1 = 2.0  # kg
    v1i = [3.0, 2.0]  # m/s [vx, vy]
    m2 = 4.0  # kg
    v2i = [-1.0, 0.0]  # m/s [vx, vy]
    angulo_impacto = np.pi/4  # 45 grados en radianes
    e = 0.8  # Coeficiente de restitución
    
    # Calcular velocidades finales
    v1f, v2f = choques.colision_bidimensional(
        m1, v1i, m2, v2i, angulo_impacto, e
    )
    
    # Mostrar resultados
    print(f"\nMasa 1: {m1} kg, Velocidad inicial: {v1i} m/s")
    print(f"Masa 2: {m2} kg, Velocidad inicial: {v2i} m/s")
    print(f"Ángulo de impacto: {np.degrees(angulo_impacto):.1f}°")
    print(f"Coeficiente de restitución: {e}")
    
    print(f"\nVelocidad final 1: [{v1f[0]:.2f}, {v1f[1]:.2f}] m/s")
    print(f"Velocidad final 2: [{v2f[0]:.2f}, {v2f[1]:.2f}] m/s")
    
    # Calcular momento lineal total (debe conservarse)
    p_i = np.array(v1i) * m1 + np.array(v2i) * m2
    p_f = np.array(v1f) * m1 + np.array(v2f) * m2
    print(f"\nMomento lineal inicial: [{p_i[0]:.2f}, {p_i[1]:.2f}] kg·m/s")
    print(f"Momento lineal final:   [{p_f[0]:.2f}, {p_f[1]:.2f}] kg·m/s")

def ejemplo_coeficiente_restitucion():
    """Ejemplo de cálculo del coeficiente de restitución."""
    print("\n" + "="*50)
    print("EJEMPLO 3: CÁLCULO DEL COEFICIENTE DE RESTITUCIÓN")
    
    # Velocidades medidas experimentalmente
    v1i = 4.0  # m/s
    v2i = -2.0  # m/s
    v1f = -1.5  # m/s
    v2f = 2.5   # m/s
    
    # Calcular coeficiente de restitución
    e = choques.coeficiente_restitucion(v1i, v2i, v1f, v2f)
    
    print(f"\nVelocidad inicial 1: {v1i} m/s")
    print(f"Velocidad inicial 2: {v2i} m/s")
    print(f"Velocidad final 1: {v1f} m/s")
    print(f"Velocidad final 2: {v2f} m/s")
    print(f"\nCoeficiente de restitución calculado: {e:.2f}")

def main():
    """Función principal que ejecuta todos los ejemplos."""
    print("="*50)
    print("EJEMPLOS DE USO DEL MÓDULO DE CHOQUES Y COLISIONES")
    print("="*50)
    
    # Ejecutar ejemplos
    ejemplo_colision_1d()
    ejemplo_colision_2d()
    ejemplo_coeficiente_restitucion()
    
    print("\n¡Ejemplos completados!")

if __name__ == "__main__":
    main()
