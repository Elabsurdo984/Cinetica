from cinetica.cinematica import circular
import math

# MCU con radio de 2m y velocidad angular de pi/2 rad/s
mcu = circular.movimiento_circular_uniforme.MovimientoCircularUniforme(
    radio=2.0, velocidad_angular_inicial=math.pi / 2
)

# Posición angular a los 1s
pos_angular_mcu = mcu.posicion_angular(tiempo=1.0)
print(f"MCU - Posición angular a 1s: {pos_angular_mcu:.2f} rad")

# Velocidad tangencial y aceleración centrípeta
vel_mcu = mcu.velocidad(tiempo=1.0)
acel_mcu = mcu.aceleracion(tiempo=1.0)
print(
    f"MCU - Posición a 1s: {mcu.posicion(1.0)}, Velocidad a 1s: {vel_mcu}, Aceleración a 1s: {acel_mcu}"
)
# mcu.graficar(t_max=10) # Graficación se manejará por una clase Graficador separada

# hspace = 0.557
