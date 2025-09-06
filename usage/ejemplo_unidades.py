from cinetica.cinematica.rectilineo.movimiento_rectilineo_uniforme import (
    MovimientoRectilineoUniforme,
)
from cinetica.units import ureg

# Con unidades
mru_con_unidades = MovimientoRectilineoUniforme(
    posicion_inicial=10 * ureg.meter, velocidad_inicial=5 * ureg.meter / ureg.second
)
posicion_final_con_unidades = mru_con_unidades.posicion(2 * ureg.second)
velocidad_final_con_unidades = mru_con_unidades.velocidad()
aceleracion_final_con_unidades = mru_con_unidades.aceleracion()

print(f"Posición final (con unidades): {posicion_final_con_unidades}")
print(f"Velocidad final (con unidades): {velocidad_final_con_unidades}")
print(f"Aceleración final (con unidades): {aceleracion_final_con_unidades}")

# Sin unidades (se asumen unidades base)
mru_sin_unidades = MovimientoRectilineoUniforme(
    posicion_inicial=10, velocidad_inicial=5
)
posicion_final_sin_unidades = mru_sin_unidades.posicion(2)
velocidad_final_sin_unidades = mru_sin_unidades.velocidad()
aceleracion_final_sin_unidades = mru_sin_unidades.aceleracion()

print(f"Posición final (sin unidades): {posicion_final_sin_unidades}")
print(f"Velocidad final (sin unidades): {velocidad_final_sin_unidades}")
print(f"Aceleración final (sin unidades): {aceleracion_final_sin_unidades}")
