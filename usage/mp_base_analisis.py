from cinetica.cinematica import parabolico

# Lanzamiento con velocidad inicial de 20 m/s y ángulo de 45 grados
mp_base = parabolico.base.MovimientoParabolicoBase(
    velocidad_inicial=20.0, angulo_grados=45
)
mp_analisis = parabolico.analisis.MovimientoParabolicoAnalisis(mp_base)

# Calcular posición a los 1.5 segundos
pos_x, pos_y = mp_base.posicion(tiempo=1.5)
print(f"MP - Posición a los 1.5s: x={pos_x:.2f} m, y={pos_y:.2f} m")

# Calcular velocidad a los 1.5 segundos
vel_x, vel_y = mp_base.velocidad(tiempo=1.5)
print(f"MP - Velocidad a los 1.5s: vx={vel_x:.2f} m/s, vy={vel_y:.2f} m/s")

# Calcular tiempo de vuelo, altura máxima y alcance máximo
tiempo_vuelo = mp_analisis.tiempo_vuelo()
altura_maxima = mp_analisis.altura_maxima()
alcance_maximo = mp_analisis.alcance_maximo()
print(f"MP - Tiempo de vuelo: {tiempo_vuelo:.2f} s")
print(f"MP - Altura máxima: {altura_maxima:.2f} m")
print(f"MP - Alcance máximo: {alcance_maximo:.2f} m")
# mp_base.graficar(t_max=4) # Graficación se manejará por una clase Graficador separada
