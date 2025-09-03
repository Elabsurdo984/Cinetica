from cinetica.cinematica.oscilatorio.mas import MovimientoArmonicoSimple
import math

# M.A.S. con amplitud de 0.1m, frecuencia angular de 2*pi rad/s (f=1Hz)
mas = MovimientoArmonicoSimple(amplitud=0.1, frecuencia_angular=2 * math.pi)

# Posición, velocidad y aceleración a los 0.25s
tiempo = 0.25
posicion_mas = mas.posicion(tiempo)
velocidad_mas = mas.velocidad(tiempo)
aceleracion_mas = mas.aceleracion(tiempo)
print(f"MAS - Posición a {tiempo}s: {posicion_mas:.4f} m")
print(f"MAS - Velocidad a {tiempo}s: {velocidad_mas:.4f} m/s")
print(f"MAS - Aceleración a {tiempo}s: {aceleracion_mas:.4f} m/s^2")

# Período y frecuencia
periodo_mas = mas.periodo()
frecuencia_mas = mas.frecuencia()
print(f"MAS - Período: {periodo_mas:.2f} s, Frecuencia: {frecuencia_mas:.2f} Hz")

# Energías (requiere masa y constante elástica)
masa = 0.5 # kg
constante_elastica = mas.frecuencia_angular**2 * masa # k = m * omega^2
energia_cinetica_mas = mas.energia_cinetica(tiempo, masa)
energia_potencial_mas = mas.energia_potencial(tiempo, constante_elastica)
energia_total_mas = mas.energia_total(masa, constante_elastica)
print(f"MAS - Energía Cinética a {tiempo}s: {energia_cinetica_mas:.4f} J")
print(f"MAS - Energía Potencial a {tiempo}s: {energia_potencial_mas:.4f} J")
print(f"MAS - Energía Total: {energia_total_mas:.4f} J")
