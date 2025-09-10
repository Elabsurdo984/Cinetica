"""
Test script to verify the optimized MRUV implementation works correctly.
"""

import sys
import numpy as np
from cinetica.cinematica.rectilineo.movimiento_rectilineo_uniformemente_variado import (
    MovimientoRectilineoUniformementeVariado as MRUVOriginal,
)

from cinetica.cinematica.rectilineo.mruv_optimizado import (
    MovimientoRectilineoUniformementeVariadoOptimizado as MRUVOptimizado,
)

def test_basic_functionality():
    """Test basic functionality of both implementations."""
    print("Testing basic functionality...")
    
    # Create instances
    original = MRUVOriginal(posicion_inicial=0, velocidad_inicial=10, aceleracion_inicial=2)
    optimizado = MRUVOptimizado(posicion_inicial=0, velocidad_inicial=10, aceleracion_inicial=2)
    
    # Test position calculation
    t = 5.0
    pos_orig = original.posicion(t)
    pos_opt = optimizado.posicion(t)
    
    print(f"Original position at t={t}: {pos_orig}")
    print(f"Optimized position at t={t}: {pos_opt}")
    pos_diff = abs(pos_orig.magnitude - pos_opt.magnitude)
    print(f"Positions match: {pos_diff < 1e-10} (difference: {pos_diff:.2e} {pos_orig.units})")
    
    # Test velocity calculation
    vel_orig = original.velocidad(t)
    vel_opt = optimizado.velocidad(t)
    
    print(f"Original velocity at t={t}: {vel_orig}")
    print(f"Optimized velocity at t={t}: {vel_opt}")
    vel_diff = abs(vel_orig.magnitude - vel_opt.magnitude)
    print(f"Velocities match: {vel_diff < 1e-10} (difference: {vel_diff:.2e} {vel_orig.units})")
    
    # Test velocity without time
    x = 50.0
    v_orig = original.velocidad_sin_tiempo(x)
    v_opt = optimizado.velocidad_sin_tiempo(x)
    
    print(f"Original velocity at x={x}: {v_orig}")
    print(f"Optimized velocity at x={x}: {v_opt}")
    v_diff = abs(v_orig.magnitude - v_opt.magnitude)
    print(f"Velocities without time match: {v_diff < 1e-10} (difference: {v_diff:.2e} {v_orig.units})")
    
    # Test time by position
    times_orig = original.tiempo_por_posicion(x)
    times_opt = optimizado.tiempo_por_posicion(x)
    
    print(f"Original times to reach x={x}: {times_orig}")
    print(f"Optimized times to reach x={x}: {times_opt}")
    
    # Compare magnitudes of Quantity objects
    times_match = all(
        abs(t1.magnitude - t2.magnitude) < 1e-10 
        for t1, t2 in zip(times_orig, times_opt)
    )
    print(f"Times match: {times_match}")
    
    # Print differences for debugging
    for i, (t1, t2) in enumerate(zip(times_orig, times_opt)):
        diff = abs(t1.magnitude - t2.magnitude)
        print(f"  Time {i+1} difference: {diff:.2e} seconds")
    
    print("\nBasic functionality tests completed!")

def test_vectorization():
    """Test vectorized operations."""
    print("\nTesting vectorized operations...")
    
    optimizado = MRUVOptimizado(posicion_inicial=0, velocidad_inicial=10, aceleracion_inicial=2)
    
    # Test with array input
    times = np.linspace(0, 10, 5)  # 5 time points from 0 to 10
    
    print(f"\nTimes array: {times}")
    
    # Calculate positions for all times at once
    positions = optimizado.posicion(times)
    print(f"Positions: {[f'{p:.2f}' for p in positions.magnitude]} {positions.units}")
    
    # Calculate velocities for all times at once
    velocities = optimizado.velocidad(times)
    print(f"Velocities: {[f'{v:.2f}' for v in velocities.magnitude]} {velocities.units}")
    
    # Verify calculations using magnitudes to avoid unit conflicts
    x0 = optimizado.posicion_inicial.magnitude
    v0 = optimizado.velocidad_inicial.magnitude
    a = optimizado.aceleracion_inicial.magnitude
    
    expected_positions = x0 + v0 * times + 0.5 * a * times**2
    expected_velocities = v0 + a * times
    
    pos_match = np.allclose(positions.magnitude, expected_positions, rtol=1e-10, atol=1e-10)
    vel_match = np.allclose(velocities.magnitude, expected_velocities, rtol=1e-10, atol=1e-10)
    
    print(f"Positions calculation correct: {pos_match}")
    if not pos_match:
        print(f"  Expected: {expected_positions}")
        print(f"  Got:      {positions.magnitude}")
        print(f"  Differences: {np.abs(positions.magnitude - expected_positions)}")
    
    print(f"Velocities calculation correct: {vel_match}")
    if not vel_match:
        print(f"  Expected: {expected_velocities}")
        print(f"  Got:      {velocities.magnitude}")
        print(f"  Differences: {np.abs(velocities.magnitude - expected_velocities)}")
    
    print("\nVectorization tests completed!")

if __name__ == "__main__":
    print("=== Testing MRUV Optimizations ===\n")
    
    # Add the parent directory to the path
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    
    # Run tests
    test_basic_functionality()
    test_vectorization()
    
    print("\n=== All tests completed! ===")
