from cinetica.cinematica.circular.movimiento_circular_uniformemente_variado import MovimientoCircularUniformementeVariado
import math

# MCUV con radio de 1m, vel. angular inicial 1 rad/s, acel. angular 0.5 rad/s^2
mcuv = MovimientoCircularUniformementeVariado(radio=1.0, velocidad_angular_inicial=1.0, aceleracion_angular_inicial=0.5)

# Velocidad angular a los 2s
pos_mcuv = mcuv.posicion(tiempo=2.0)
vel_mcuv = mcuv.velocidad(tiempo=2.0)
acel_mcuv = mcuv.aceleracion(tiempo=2.0)
print(f"MCUV - Posición a 2s: {pos_mcuv}, Velocidad a 2s: {vel_mcuv}, Aceleración a 2s: {acel_mcuv}")
# mcuv.graficar(t_max=10) # Graficación se manejará por una clase Graficador separada

# Corregir completamente el grafico
