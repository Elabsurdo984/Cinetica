from cinetica.cinematica.rectilineo.movimiento_rectilineo_uniforme import MovimientoRectilineoUniforme

# MRU
mru = MovimientoRectilineoUniforme(posicion_inicial=10.0, velocidad_inicial=2.0)
posicion_mru = mru.posicion(tiempo=5.0)
velocidad_mru = mru.velocidad()
print(f"MRU - Posición a los 5s: {mru.posicion(5.0)} m, Velocidad: {mru.velocidad(5.0)} m/s, Aceleración: {mru.aceleracion(5.0)} m/s^2")
# mru.graficar(t_max=10) # Graficación se manejará por una clase Graficador separada
