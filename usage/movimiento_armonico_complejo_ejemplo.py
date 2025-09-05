from cinetica.cinematica import oscilatorio
import numpy as np

# Definir componentes MAS
componente1 = {'amplitud': 2.0, 'frecuencia_angular': 1.0, 'fase_inicial': 0.0}
componente2 = {'amplitud': 1.0, 'frecuencia_angular': 3.0, 'fase_inicial': np.pi / 2}
componente3 = {'amplitud': 0.5, 'frecuencia_angular': 5.0, 'fase_inicial': np.pi}

mac = oscilatorio.movimiento_armonico_complejo.MovimientoArmonicoComplejo([componente1, componente2, componente3])

# Calcular posición, velocidad y aceleración en un tiempo específico
tiempo_mac = 0.5
posicion_mac = mac.posicion(tiempo_mac)
velocidad_mac = mac.velocidad(tiempo_mac)
aceleracion_mac = mac.aceleracion(tiempo_mac)

print(f"MAC - Posición a {tiempo_mac}s: {posicion_mac:.4f} m")
print(f"MAC - Velocidad a {tiempo_mac}s: {velocidad_mac:.4f} m/s")
print(f"MAC - Aceleración a {tiempo_mac}s: {aceleracion_mac:.4f} m/s^2")
