# Cinetica

Cinetica is a Python library designed to provide various modules for physics calculations and simulations.

## Installation

```bash
pip install cinetica
```

## Usage

### Movimiento Rectilíneo

El módulo `movimiento_rectilineo` proporciona la clase `MovimientoRectilineo` para calcular posición, velocidad y aceleración en Movimiento Rectilíneo Uniforme (MRU) y Movimiento Rectilíneo Uniformemente Variado (MRUV).

**Ejemplo de uso:**

```python
from cinetica.movimiento_rectilineo import MovimientoRectilineo

# MRU
mru = MovimientoRectilineo(posicion_inicial=10.0, velocidad_inicial=2.0)
posicion_mru = mru.mru_posicion(tiempo=5.0)
velocidad_mru = mru.mru_velocidad()
print(f"MRU - Posición a los 5s: {posicion_mru} m, Velocidad: {velocidad_mru} m/s")

# MRUV
mruv = MovimientoRectilineo(posicion_inicial=0.0, velocidad_inicial=10.0, aceleracion_inicial=2.0)
posicion_mruv = mruv.mruv_posicion(tiempo=3.0)
velocidad_mruv = mruv.mruv_velocidad(tiempo=3.0)
aceleracion_mruv = mruv.mruv_aceleracion()
print(f"MRUV - Posición a los 3s: {posicion_mruv} m, Velocidad: {velocidad_mruv} m/s, Aceleración: {aceleracion_mruv} m/s^2")

# MRUV sin tiempo
mruv_sin_tiempo = MovimientoRectilineo(posicion_inicial=0.0, velocidad_inicial=0.0, aceleracion_inicial=2.0)
velocidad_final_sin_tiempo = mruv_sin_tiempo.mruv_velocidad_sin_tiempo(posicion_final=16.0)
print(f"MRUV - Velocidad final sin tiempo (para posición 16m): {velocidad_final_sin_tiempo} m/s")
```

## Contributing

Contributions are welcome! Please see the `CONTRIBUTING.md` for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
