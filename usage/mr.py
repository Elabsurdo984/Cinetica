from cinetica.cinematica.relativo.velocidad_relativa import MovimientoRelativo
import numpy as np

mr = MovimientoRelativo()

# Velocidades de los objetos
v_tren = [50, 0] # Tren moviéndose en el eje X a 50 km/h
v_persona = [5, 0] # Persona caminando en el tren en la misma dirección a 5 km/h
v_viento = [0, -20] # Viento soplando en el eje Y negativo a 20 km/h

# Velocidad de la persona con respecto a tierra (V_P/T = V_P/Tren + V_Tren/Tierra)
# Aquí, V_P/Tren es la velocidad de la persona relativa al tren, y V_Tren/Tierra es la velocidad absoluta del tren.
# Si la persona camina en el tren, su velocidad absoluta es la suma de su velocidad relativa al tren y la velocidad del tren.
v_persona_tierra = mr.velocidad_absoluta_a(v_persona, v_tren)
print(f"Velocidad de la persona con respecto a tierra: {v_persona_tierra} km/h")

# Velocidad del tren con respecto a la persona (V_Tren/P = V_Tren/Tierra - V_P/Tierra)
v_tren_persona = mr.velocidad_relativa(v_tren, v_persona_tierra)
print(f"Velocidad del tren con respecto a la persona: {v_tren_persona} km/h")

# Escenario 2D: Barco en un río
v_barco_rio = [10, 0] # Velocidad del barco respecto al río (10 km/h río abajo)
v_rio_tierra = [0, 5] # Velocidad del río respecto a tierra (5 km/h hacia el norte)

# Velocidad del barco respecto a tierra (V_B/T = V_B/R + V_R/T)
v_barco_tierra = mr.velocidad_absoluta_a(v_barco_rio, v_rio_tierra)
print(f"Velocidad del barco con respecto a tierra: {v_barco_tierra} km/h")
print(f"Magnitud de la velocidad del barco: {mr.magnitud_velocidad(v_barco_tierra):.2f} km/h")
print(f"Dirección de la velocidad del barco (radianes): {mr.direccion_velocidad(v_barco_tierra):.2f} rad")

# Escenario 3D: Avión con viento
v_avion_aire = [200, 50, 0] # Velocidad del avión respecto al aire
v_aire_tierra = [20, -10, 5] # Velocidad del aire (viento) respecto a tierra

# Velocidad del avión respecto a tierra (V_A/T = V_A/Aire + V_Aire/Tierra)
v_avion_tierra = mr.velocidad_absoluta_a(v_avion_aire, v_aire_tierra)
print(f"Velocidad del avión con respecto a tierra: {v_avion_tierra} km/h")
print(f"Magnitud de la velocidad del avión: {mr.magnitud_velocidad(v_avion_tierra):.2f} km/h")
print(f"Dirección de la velocidad del avión (vector unitario): {mr.direccion_velocidad(v_avion_tierra)}")
