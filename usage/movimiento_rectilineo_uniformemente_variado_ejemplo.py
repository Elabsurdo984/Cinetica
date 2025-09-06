from cinetica.cinematica import rectilineo

# MRUV
mruv = rectilineo.movimiento_rectilineo_uniformemente_variado.MovimientoRectilineoUniformementeVariado(
    posicion_inicial=0.0, velocidad_inicial=10.0, aceleracion_inicial=2.0
)
posicion_mruv = mruv.posicion(tiempo=3.0)
velocidad_mruv = mruv.velocidad(tiempo=3.0)
aceleracion_mruv = mruv.aceleracion(tiempo=3.0)
print(
    f"MRUV - Posición a los 3s: {posicion_mruv} m, Velocidad: {velocidad_mruv} m/s, Aceleración: {aceleracion_mruv} m/s^2"
)

# MRUV sin tiempo
mruv_sin_tiempo = rectilineo.movimiento_rectilineo_uniformemente_variado.MovimientoRectilineoUniformementeVariado(
    posicion_inicial=0.0, velocidad_inicial=0.0, aceleracion_inicial=2.0
)
velocidad_final_sin_tiempo = mruv_sin_tiempo.velocidad_sin_tiempo(posicion_final=16.0)
print(
    f"MRUV - Velocidad final sin tiempo (para posición 16m): {velocidad_final_sin_tiempo} m/s"
)

# MRUV - Tiempo a partir de la posición final
# Ejemplo: Calcular el tiempo para alcanzar una posición de 16m
tiempos_posicion = mruv.tiempo_por_posicion(posicion_final=16.0)
print(
    f"MRUV - Tiempos para posición 16m: {tiempos_posicion[0]:.2f}s, {tiempos_posicion[0]:.2f}s"
)

# MRUV - Tiempo a partir de la velocidad final
# Ejemplo: Calcular el tiempo para alcanzar una velocidad de 20 m/s
tiempo_velocidad = mruv.tiempo_por_velocidad(velocidad_final=20.0)
print(f"MRUV - Tiempo para velocidad 20m/s: {tiempo_velocidad:.2f}s")

# MRUV - Desplazamiento sin conocer el tiempo
# Ejemplo: Calcular el desplazamiento para alcanzar una velocidad final de 20 m/s
desplazamiento_sin_tiempo = mruv.desplazamiento_sin_tiempo(velocidad_final=20.0)
print(
    f"MRUV - Desplazamiento sin tiempo (para velocidad 20m/s): {desplazamiento_sin_tiempo:.2f}m"
)
# mruv.graficar(t_max=10) # Graficación se manejará por una clase Graficador separada

# hspace = 0.486
