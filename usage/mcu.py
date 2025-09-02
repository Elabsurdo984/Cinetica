from cinetica.circular import MovimientoCircularUniforme
import math

# MCU con radio de 2m y velocidad angular de pi/2 rad/s
mcu = MovimientoCircularUniforme(radio=2.0, velocidad_angular_inicial=math.pi/2)

# Posición angular a los 1s
pos_angular_mcu = mcu.posicion_angular(tiempo=1.0)
print(f"MCU - Posición angular a 1s: {pos_angular_mcu:.2f} rad")

# Velocidad tangencial y aceleración centrípeta
vel_tangencial_mcu = mcu.velocidad_tangencial()
acel_centripeta_mcu = mcu.aceleracion_centripeta()
print(f"MCU - Velocidad tangencial: {vel_tangencial_mcu:.2f} m/s, Aceleración centrípeta: {acel_centripeta_mcu:.2f} m/s^2")
mcu.graficar(t_max=10) # Ejemplo de graficación

# hspace = 0.557