from cinetica.cinematica.circular.movimiento_circular_uniformemente_variado import MovimientoCircularUniformementeVariado
import math

# MCUV con radio de 1m, vel. angular inicial 1 rad/s, acel. angular 0.5 rad/s^2
mcuv = MovimientoCircularUniformementeVariado(radio=1.0, velocidad_angular_inicial=1.0, aceleracion_angular_inicial=0.5)

# Velocidad angular a los 2s
vel_angular_mcuv = mcuv.velocidad_angular(tiempo=2.0)
print(f"MCUV - Velocidad angular a 2s: {vel_angular_mcuv:.2f} rad/s")

# Aceleración tangencial y centrípeta a los 2s
acel_tangencial_mcuv = mcuv.aceleracion_tangencial()
acel_centripeta_mcuv = mcuv.aceleracion_centripeta(tiempo=2.0)
acel_total_mcuv = mcuv.aceleracion_total(tiempo=2.0)
print(f"MCUV - Aceleración tangencial: {acel_tangencial_mcuv:.2f} m/s^2, Aceleración centrípeta: {acel_centripeta_mcuv:.2f} m/s^2, Aceleración total: {acel_total_mcuv:.2f} m/s^2")

# MCUV - Tiempo a partir de la velocidad angular final
# Ejemplo: Calcular el tiempo para alcanzar una velocidad angular de 3 rad/s
tiempo_vel_angular = mcuv.tiempo_por_velocidad_angular(velocidad_angular_final=3.0)
print(f"MCUV - Tiempo para velocidad angular 3rad/s: {tiempo_vel_angular:.2f}s")
mcuv.graficar(t_max=10) # Ejemplo de graficación

# Corregir completamente el grafico
