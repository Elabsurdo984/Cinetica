"""
Ejemplo de uso del módulo SistemasParticulas

Este script muestra cómo utilizar las diferentes funcionalidades del módulo de sistemas
de partículas de la biblioteca Cinetica.
"""

import numpy as np
from cinetica.dinamica import SistemasParticulas

def ejemplo_centro_masa():
    """Ejemplo de cálculo del centro de masa."""
    print("\n" + "="*50)
    print("EJEMPLO 1: CÁLCULO DEL CENTRO DE MASA")
    
    # Crear una instancia del módulo
    sp = SistemasParticulas()
    
    # Definir un sistema de partículas simple
    masas = [1.0, 2.0, 3.0]  # kg
    posiciones = [
        [0.0, 0.0, 0.0],  # m
        [2.0, 0.0, 0.0],  # m
        [2.0, 3.0, 0.0]   # m
    ]
    
    # Calcular el centro de masa
    cm = sp.centro_masa(masas, posiciones)
    
    # Mostrar resultados
    print(f"\nSistema de {len(masas)} partículas:")
    for i, (m, r) in enumerate(zip(masas, posiciones), 1):
        print(f"  Partícula {i}: m = {m} kg, r = {r} m")
    
    print(f"\nCentro de masa: {cm} m")

def ejemplo_momento_inercia():
    """Ejemplo de cálculo del momento de inercia."""
    print("\n" + "="*50)
    print("EJEMPLO 2: MOMENTO DE INERCIA")
    
    sp = SistemasParticulas()
    
    # Definir un sistema de partículas en un cuadrado en el plano xy
    lado = 2.0  # m
    masas = [1.0, 1.0, 1.0, 1.0]  # kg
    posiciones = [
        [0.0, 0.0, 0.0],
        [lado, 0.0, 0.0],
        [lado, lado, 0.0],
        [0.0, lado, 0.0]
    ]
    
    # Calcular el momento de inercia con respecto al eje z
    I_z = sp.momento_inercia_sistema(masas, posiciones, eje=[0, 0, 1])
    
    # Calcular el momento de inercia con respecto al centro de masa
    cm = sp.centro_masa(masas, posiciones)
    
    # Distancia desde el centro de masa al origen
    d = np.linalg.norm(cm)
    
    # Usar el teorema de Steiner para verificar
    I_cm = sp.momento_inercia_sistema(
        masas, 
        [[x-cm[0], y-cm[1], z-cm[2]] for x, y, z in posiciones],
        eje=[0, 0, 1]
    )
    
    I_steiner = sp.teorema_steiner(I_cm, sum(masas), d)
    
    # Mostrar resultados
    print(f"\nSistema de {len(masas)} partículas formando un cuadrado de lado {lado} m")
    print(f"Momento de inercia con respecto al eje z: {I_z:.2f} kg·m²")
    print(f"Momento de inercia con respecto al centro de masa: {I_cm:.2f} kg·m²")
    print(f"Verificación con teorema de Steiner: {I_steiner:.2f} kg·m²")

def ejemplo_energia_rotacional():
    """Ejemplo de cálculo de energía cinética rotacional."""
    print("\n" + "="*50)
    print("EJEMPLO 3: ENERGÍA CINÉTICA ROTACIONAL")
    
    sp = SistemasParticulas()
    
    # Definir un sistema de dos partículas girando alrededor del eje z
    masas = [1.0, 1.0]  # kg
    posiciones = [
        [1.0, 0.0, 0.0],  # m
        [-1.0, 0.0, 0.0]  # m
    ]
    
    # Velocidad angular (rad/s)
    omega = 2.0  # rad/s
    
    # Calcular el momento de inercia con respecto al eje z
    I = sp.momento_inercia_sistema(masas, posiciones, eje=[0, 0, 1])
    
    # Calcular la energía cinética rotacional
    K = sp.energia_cinetica_rotacional(I, omega)
    
    # Calcular el momento angular
    L = sp.momento_angular(I, omega)
    
    # Mostrar resultados
    print(f"\nSistema de {len(masas)} partículas girando a {omega} rad/s")
    print(f"Momento de inercia: {I:.2f} kg·m²")
    print(f"Energía cinética rotacional: {K:.2f} J")
    print(f"Momento angular: {L:.2f} kg·m²/s")

def main():
    """Función principal que ejecuta todos los ejemplos."""
    print("="*50)
    print("EJEMPLOS DE USO DEL MÓDULO DE SISTEMAS DE PARTÍCULAS")
    print("="*50)
    
    # Ejecutar ejemplos
    ejemplo_centro_masa()
    ejemplo_momento_inercia()
    ejemplo_energia_rotacional()
    
    print("\n¡Ejemplos completados!")

if __name__ == "__main__":
    main()
