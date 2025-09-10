"""
Benchmark para comparar el rendimiento de la implementación original vs optimizada de MRUV.
"""

import timeit
import numpy as np
from pathlib import Path
import sys

# Añadir el directorio raíz al path para importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

# Importar ambas implementaciones
from cinetica.cinematica.rectilineo.movimiento_rectilineo_uniformemente_variado import (
    MovimientoRectilineoUniformementeVariado as MRUVOriginal,
)

from cinetica.cinematica.rectilineo.mruv_optimizado import (
    MovimientoRectilineoUniformementeVariadoOptimizado as MRUVOptimizado,
)

def benchmark_posicion():
    """Benchmark para el cálculo de posición."""
    print("\n=== Benchmark: Cálculo de posición ===")
    
    # Configuración
    n = 10000
    tiempos = np.linspace(0, 10, n)
    
    # Crear instancias
    mruv_original = MRUVOriginal(posicion_inicial=0, velocidad_inicial=10, aceleracion_inicial=2)
    mruv_optimizado = MRUVOptimizado(posicion_inicial=0, velocidad_inicial=10, aceleracion_inicial=2)
    
    # Benchmark para un solo valor
    print("\n1. Cálculo de un solo valor:")
    
    # Original
    t_original = timeit.timeit(
        lambda: mruv_original.posicion(5.0),
        number=10000
    )
    print(f"  - Original: {t_original*1000:.2f} ms para 10,000 iteraciones")
    
    # Optimizado
    t_optimizado = timeit.timeit(
        lambda: mruv_optimizado.posicion(5.0),
        number=10000
    )
    print(f"  - Optimizado: {t_optimizado*1000:.2f} ms para 10,000 iteraciones")
    print(f"  - Mejora: {t_original/t_optimizado:.2f}x más rápido")
    
    # Benchmark para array de valores
    print("\n2. Cálculo con arrays (vectorizado):")
    
    # Optimizado con array
    t_optimizado_array = timeit.timeit(
        lambda: mruv_optimizado.posicion(tiempos),
        number=100
    )
    print(f"  - Optimizado (array de {n} elementos): {t_optimizado_array*1000:.2f} ms para 100 iteraciones")
    
    # Original con bucle (para comparación)
    t_original_array = timeit.timeit(
        lambda: [mruv_original.posicion(t) for t in tiempos],
        number=1
    )
    print(f"  - Original (bucle en Python): {t_original_array*1000:.2f} ms para 1 iteración")
    print(f"  - Mejora: {t_original_array/(t_optimizado_array/100):.2f}x más rápido")

def benchmark_velocidad():
    """Benchmark para el cálculo de velocidad."""
    print("\n=== Benchmark: Cálculo de velocidad ===")
    
    # Configuración
    n = 10000
    tiempos = np.linspace(0, 10, n)
    
    # Crear instancias
    mruv_original = MRUVOriginal(velocidad_inicial=10, aceleracion_inicial=2)
    mruv_optimizado = MRUVOptimizado(velocidad_inicial=10, aceleracion_inicial=2)
    
    # Benchmark para un solo valor
    print("\n1. Cálculo de un solo valor:")
    
    # Original
    t_original = timeit.timeit(
        lambda: mruv_original.velocidad(5.0),
        number=10000
    )
    print(f"  - Original: {t_original*1000:.2f} ms para 10,000 iteraciones")
    
    # Optimizado
    t_optimizado = timeit.timeit(
        lambda: mruv_optimizado.velocidad(5.0),
        number=10000
    )
    print(f"  - Optimizado: {t_optimizado*1000:.2f} ms para 10,000 iteraciones")
    print(f"  - Mejora: {t_original/t_optimizado:.2f}x más rápido")
    
    # Benchmark para array de valores
    print("\n2. Cálculo con arrays (vectorizado):")
    
    # Optimizado con array
    t_optimizado_array = timeit.timeit(
        lambda: mruv_optimizado.velocidad(tiempos),
        number=100
    )
    print(f"  - Optimizado (array de {n} elementos): {t_optimizado_array*1000:.2f} ms para 100 iteraciones")
    
    # Original con bucle (para comparación)
    t_original_array = timeit.timeit(
        lambda: [mruv_original.velocidad(t) for t in tiempos],
        number=1
    )
    print(f"  - Original (bucle en Python): {t_original_array*1000:.2f} ms para 1 iteración")
    print(f"  - Mejora: {t_original_array/(t_optimizado_array/100):.2f}x más rápido")

def benchmark_velocidad_sin_tiempo():
    """Benchmark para el cálculo de velocidad sin tiempo."""
    print("\n=== Benchmark: Cálculo de velocidad sin tiempo ===")
    
    # Configuración
    n = 1000
    posiciones = np.linspace(0, 100, n)
    
    # Crear instancias
    mruv_original = MRUVOriginal(velocidad_inicial=10, aceleracion_inicial=2)
    mruv_optimizado = MRUVOptimizado(velocidad_inicial=10, aceleracion_inicial=2)
    
    # Benchmark para un solo valor
    print("\n1. Cálculo de un solo valor:")
    
    # Original
    t_original = timeit.timeit(
        lambda: mruv_original.velocidad_sin_tiempo(50.0),
        number=1000
    )
    print(f"  - Original: {t_original*1000:.2f} ms para 1,000 iteraciones")
    
    # Optimizado
    t_optimizado = timeit.timeit(
        lambda: mruv_optimizado.velocidad_sin_tiempo(50.0),
        number=1000
    )
    print(f"  - Optimizado: {t_optimizado*1000:.2f} ms para 1,000 iteraciones")
    print(f"  - Mejora: {t_original/t_optimizado:.2f}x más rápido")

def benchmark_tiempo_por_posicion():
    """Benchmark para el cálculo de tiempo por posición."""
    print("\n=== Benchmark: Cálculo de tiempo por posición ===")
    
    # Configuración
    n = 1000
    posiciones = np.linspace(0, 100, n)
    
    # Crear instancias
    mruv_original = MRUVOriginal(velocidad_inicial=10, aceleracion_inicial=2)
    mruv_optimizado = MRUVOptimizado(velocidad_inicial=10, aceleracion_inicial=2)
    
    # Benchmark para un solo valor
    print("\n1. Cálculo de un solo valor:")
    
    # Original
    t_original = timeit.timeit(
        lambda: mruv_original.tiempo_por_posicion(50.0),
        number=1000
    )
    print(f"  - Original: {t_original*1000:.2f} ms para 1,000 iteraciones")
    
    # Optimizado
    t_optimizado = timeit.timeit(
        lambda: mruv_optimizado.tiempo_por_posicion(50.0),
        number=1000
    )
    print(f"  - Optimizado: {t_optimizado*1000:.2f} ms para 1,000 iteraciones")
    print(f"  - Mejora: {t_original/t_optimizado:.2f}x más rápido")

def main():
    """Función principal para ejecutar todos los benchmarks."""
    print("=== Iniciando benchmarks de MRUV ===")
    print(f"Python: {sys.version}")
    print(f"NumPy: {np.__version__}")
    
    # Ejecutar benchmarks
    benchmark_posicion()
    benchmark_velocidad()
    benchmark_velocidad_sin_tiempo()
    benchmark_tiempo_por_posicion()
    
    print("\n=== Benchmarks completados ===")

if __name__ == "__main__":
    main()
