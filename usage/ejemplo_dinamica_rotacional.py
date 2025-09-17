#!/usr/bin/env python3
"""
Ejemplo de uso del módulo de dinámica rotacional de Cinetica.

Este ejemplo demuestra las capacidades del módulo de dinámica rotacional,
including cálculos de momento angular, torque, energía rotacional y cuerpos rígidos.
"""

import numpy as np
import cinetica
from cinetica.dinamica.rotacional import MomentoAngular, Torque, EnergiaRotacional, CuerposRigidos, EcuacionesEuler
from cinetica.units import ureg, Q_

def main():
    """Función principal del ejemplo."""
    print("=== Ejemplo de Dinámica Rotacional ===\n")
    
    # Inicializar clases
    momento = MomentoAngular()
    torque = Torque()
    energia = EnergiaRotacional()
    cuerpo = CuerposRigidos()
    euler = EcuacionesEuler()
    
    print("1. Momento Angular")
    print("-" * 20)
    
    # Ejemplo 1: Momento angular de una rueda
    inercia_rueda = Q_(2.5, 'kg * m**2')
    velocidad_angular = Q_(10, 'rad/s')
    
    momento_angular = momento.calcular_momento_angular(inercia_rueda, velocidad_angular)
    print(f"Momento angular de la rueda: {momento_angular}")
    
    # Ejemplo 2: Momento angular de una partícula
    masa = Q_(0.5, 'kg')
    posicion = np.array([2, 0, 0])
    velocidad = np.array([0, 3, 0])
    
    momento_particula = momento.momento_angular_particula(masa, posicion, velocidad)
    print(f"Momento angular de la partícula: {momento_particula}")
    
    print("\n2. Torque")
    print("-" * 20)
    
    # Ejemplo 3: Torque aplicado a una puerta
    fuerza = Q_(50, 'N')
    posicion = np.array([0.8, 0, 0])
    
    torque_puerta = torque.calcular_torque(fuerza, posicion)
    print(f"Torque en la puerta: {torque_puerta}")
    
    # Ejemplo 4: Torque usando brazo de palanca
    brazo = Q_(0.5, 'm')
    torque_mag = torque.torque_magnitud(fuerza, brazo)
    print(f"Torque (magnitud): {torque_mag}")
    
    # Ejemplo 5: Segunda ley de Newton rotacional
    aceleracion_angular = Q_(2, 'rad/s**2')
    torque_newton = torque.segunda_ley_newton_rotacional(inercia_rueda, aceleracion_angular)
    print(f"Torque (2ª ley rotacional): {torque_newton}")
    
    print("\n3. Energía Rotacional")
    print("-" * 20)
    
    # Ejemplo 6: Energía cinética rotacional
    energia_cinetica = energia.energia_cinetica_rotacional(inercia_rueda, velocidad_angular)
    print(f"Energía cinética rotacional: {energia_cinetica}")
    
    # Ejemplo 7: Energía cinética total (traslación + rotación)
    masa_esfera = Q_(1.0, 'kg')
    velocidad_lineal = Q_(5, 'm/s')
    inercia_esfera = Q_(0.4, 'kg * m**2')  # I = (2/5) * m * r² para esfera
    
    energia_total = energia.energia_cinetica_total(masa_esfera, velocidad_lineal, inercia_esfera, velocidad_angular)
    print(f"Energía cinética total: {energia_total}")
    
    # Ejemplo 8: Trabajo por torque
    angulo_rotacion = Q_(np.pi, 'rad')
    trabajo = energia.trabajo_torque(torque_mag, angulo_rotacion)
    print(f"Trabajo por torque: {trabajo}")
    
    print("\n4. Cuerpos Rígidos")
    print("-" * 20)
    
    # Ejemplo 9: Momento de inercia de diferentes formas
    masa_cilindro = Q_(2.0, 'kg')
    radio_cilindro = Q_(0.3, 'm')
    
    inercia_cilindro = cuerpo.inercia_cilindro_solido(masa_cilindro, radio_cilindro)
    print(f"Momento de inercia cilindro sólido: {inercia_cilindro}")
    
    masa_varilla = Q_(0.5, 'kg')
    longitud_varilla = Q_(1.0, 'm')
    
    inercia_varilla = cuerpo.inercia_varilla_centro(masa_varilla, longitud_varilla)
    print(f"Momento de inercia varilla (centro): {inercia_varilla}")
    
    # Ejemplo 10: Radio de giro
    radio_giro = cuerpo.radio_giro(inercia_cilindro, masa_cilindro)
    print(f"Radio de giro: {radio_giro}")
    
    print("\n5. Ecuaciones de Euler")
    print("-" * 20)
    
    # Ejemplo 11: Estabilidad de rotación
    # Definir tensor de inercia para un cuerpo asimétrico
    ixx = Q_(0.1, 'kg * m**2')
    iyy = Q_(0.2, 'kg * m**2')
    izz = Q_(0.3, 'kg * m**2')
    
    euler.set_tensor_inercia(ixx, iyy, izz)
    
    estabilidad_x = euler.estabilidad_rotacion('x')
    estabilidad_y = euler.estabilidad_rotacion('y')
    estabilidad_z = euler.estabilidad_rotacion('z')
    
    print(f"Estabilidad rotación eje x: {estabilidad_x}")
    print(f"Estabilidad rotación eje y: {estabilidad_y}")
    print(f"Estabilidad rotación eje z: {estabilidad_z}")
    
    # Ejemplo 12: Precesión de giroscopio
    velocidad_spin = Q_(100, 'rad/s')
    torque_giroscopio = Q_(0.5, 'N * m')
    
    velocidad_precesion = euler.precesion_giroscopio(velocidad_spin, torque_giroscopio)
    print(f"Velocidad de precesión: {velocidad_precesion}")
    
    print("\n6. Conservación de Cantidades")
    print("-" * 20)
    
    # Ejemplo 13: Conservación de momento angular
    momento_inicial = Q_(25, 'kg * m**2 / s')
    momento_final = Q_(24.8, 'kg * m**2 / s')
    
    conservado = momento.conservacion_momento_angular(momento_inicial, momento_final)
    print(f"¿Se conserva el momento angular? {conservado}")
    
    # Ejemplo 14: Conservación de energía mecánica
    energia_inicial = Q_(100, 'J')
    energia_final = Q_(95, 'J')
    
    energia_conservada = energia.conservacion_energia_mecanica(energia_inicial, energia_final)
    print(f"¿Se conserva la energía mecánica? {energia_conservada}")
    
    print("\n=== Ejemplo completado ===")

if __name__ == "__main__":
    main()