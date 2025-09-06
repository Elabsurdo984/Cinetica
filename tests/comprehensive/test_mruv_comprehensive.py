import pytest
import math
import numpy as np
from cinetica.cinematica.rectilineo import MovimientoRectilineoUniformementeVariado
from cinetica.units import ureg, Q_


class TestMRUVTiempoPorPosicion:
    """Comprehensive tests for tiempo_por_posicion method."""

    def test_tiempo_por_posicion_cuadratico_dos_soluciones(self):
        """Test quadratic case with two valid solutions."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=10 * ureg.meter / ureg.second,
            aceleracion_inicial=-2 * ureg.meter / ureg.second**2
        )

        # Position that can be reached at two different times
        tiempos = mruv.tiempo_por_posicion(24 * ureg.meter)

        assert len(tiempos) == 2
        assert all(t.magnitude >= 0 for t in tiempos)
        # Verify both solutions are correct
        for t in tiempos:
            pos = mruv.posicion(t)
            assert abs(pos.magnitude - 24) < 1e-10

    def test_tiempo_por_posicion_cuadratico_una_solucion(self):
        """Test quadratic case with one solution (vertex)."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=10 * ureg.meter / ureg.second,
            aceleracion_inicial=-2 * ureg.meter / ureg.second**2
        )

        # Maximum position (vertex of parabola)
        # x_max = x0 + v0²/(2|a|) = 0 + 100/4 = 25
        tiempos = mruv.tiempo_por_posicion(25 * ureg.meter)

        assert len(tiempos) == 1
        assert tiempos[0].magnitude > 0
        # Verify solution is correct
        pos = mruv.posicion(tiempos[0])
        assert abs(pos.magnitude - 25) < 1e-10

    def test_tiempo_por_posicion_cuadratico_sin_solucion(self):
        """Test quadratic case with no real solutions."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=10 * ureg.meter / ureg.second,
            aceleracion_inicial=-2 * ureg.meter / ureg.second**2
        )

        # Position beyond maximum reach
        with pytest.raises(ValueError, match="No hay soluciones reales"):
            mruv.tiempo_por_posicion(30 * ureg.meter)

    def test_tiempo_por_posicion_lineal_solucion_valida(self):
        """Test linear case (zero acceleration) with valid solution."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=5 * ureg.meter,
            velocidad_inicial=3 * ureg.meter / ureg.second,
            aceleracion_inicial=0 * ureg.meter / ureg.second**2
        )

        tiempos = mruv.tiempo_por_posicion(11 * ureg.meter)

        assert len(tiempos) == 1
        assert tiempos[0].magnitude == 2.0  # (11-5)/3 = 2
        # Verify solution
        pos = mruv.posicion(tiempos[0])
        assert abs(pos.magnitude - 11) < 1e-10

    def test_tiempo_por_posicion_lineal_tiempo_negativo(self):
        """Test linear case with negative time result."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=10 * ureg.meter,
            velocidad_inicial=2 * ureg.meter / ureg.second,
            aceleracion_inicial=0 * ureg.meter / ureg.second**2
        )

        # Position in the past
        with pytest.raises(ValueError, match="El tiempo calculado es negativo"):
            mruv.tiempo_por_posicion(5 * ureg.meter)

    def test_tiempo_por_posicion_velocidad_cero_aceleracion_cero_posicion_igual(self):
        """Test case with zero velocity and acceleration, same position."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=7 * ureg.meter,
            velocidad_inicial=0 * ureg.meter / ureg.second,
            aceleracion_inicial=0 * ureg.meter / ureg.second**2
        )

        tiempos = mruv.tiempo_por_posicion(7 * ureg.meter)

        assert len(tiempos) == 1
        assert tiempos[0].magnitude == 0

    def test_tiempo_por_posicion_velocidad_cero_aceleracion_cero_posicion_diferente(self):
        """Test case with zero velocity and acceleration, different position."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=7 * ureg.meter,
            velocidad_inicial=0 * ureg.meter / ureg.second,
            aceleracion_inicial=0 * ureg.meter / ureg.second**2
        )

        with pytest.raises(ValueError, match="No se puede alcanzar la posición final"):
            mruv.tiempo_por_posicion(10 * ureg.meter)

    def test_tiempo_por_posicion_filtrar_negativos(self):
        """Test filtering of negative time solutions."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=-5 * ureg.meter / ureg.second,
            aceleracion_inicial=2 * ureg.meter / ureg.second**2
        )

        # Position that gives one positive and one negative solution
        tiempos = mruv.tiempo_por_posicion(-4 * ureg.meter)

        # Should only return positive solutions
        assert len(tiempos) >= 1
        assert all(t.magnitude >= 0 for t in tiempos)

    def test_tiempo_por_posicion_unidades_float(self):
        """Test with float input (no units)."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=5 * ureg.meter / ureg.second,
            aceleracion_inicial=1 * ureg.meter / ureg.second**2
        )

        # Input as float
        tiempos = mruv.tiempo_por_posicion(12.0)  # No units

        assert len(tiempos) >= 1
        assert all(isinstance(t, Q_) for t in tiempos)
        assert all(t.units == ureg.second for t in tiempos)


class TestMRUVVelocidadSinTiempo:
    """Comprehensive tests for velocidad_sin_tiempo method."""

    def test_velocidad_sin_tiempo_aceleracion_positiva(self):
        """Test velocity calculation with positive acceleration."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=3 * ureg.meter / ureg.second,
            aceleracion_inicial=2 * ureg.meter / ureg.second**2
        )

        vel = mruv.velocidad_sin_tiempo(8 * ureg.meter)

        # v² = v₀² + 2a(x - x₀) = 9 + 2*2*8 = 9 + 32 = 41
        expected = np.sqrt(41)
        assert abs(vel.magnitude - expected) < 1e-10
        assert vel.units == ureg.meter / ureg.second

    def test_velocidad_sin_tiempo_aceleracion_negativa(self):
        """Test velocity calculation with negative acceleration."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=10 * ureg.meter / ureg.second,
            aceleracion_inicial=-1 * ureg.meter / ureg.second**2
        )

        vel = mruv.velocidad_sin_tiempo(25 * ureg.meter)

        # v² = v₀² + 2a(x - x₀) = 100 + 2*(-1)*25 = 100 - 50 = 50
        expected = np.sqrt(50)
        assert abs(vel.magnitude - expected) < 1e-10

    def test_velocidad_sin_tiempo_discriminante_negativo(self):
        """Test velocidad_sin_tiempo with negative discriminant (no real solution)."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=1 * ureg.meter / ureg.second,
            aceleracion_inicial=1 * ureg.meter / ureg.second**2
        )

        # This should raise ValueError for negative discriminant
        # With v₀=1, a=1, x₀=0: 1 + 2*1*(x - 0) < 0 => x < -0.5
        with pytest.raises(ValueError, match="No se puede calcular la velocidad real"):
            mruv.velocidad_sin_tiempo(-1 * ureg.meter)

    def test_velocidad_sin_tiempo_aceleracion_cero(self):
        """Test velocity calculation with zero acceleration (MRU case)."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=2 * ureg.meter,
            velocidad_inicial=4 * ureg.meter / ureg.second,
            aceleracion_inicial=0 * ureg.meter / ureg.second**2
        )

        vel = mruv.velocidad_sin_tiempo(10 * ureg.meter)

        # In MRU, velocity is constant
        assert abs(vel.magnitude - 4) < 1e-10

    def test_velocidad_sin_tiempo_unidades_float(self):
        """Test with float input (no units)."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0,
            velocidad_inicial=5,
            aceleracion_inicial=2
        )
        
        vel = mruv.velocidad_sin_tiempo(16)
        # Using v² = v₀² + 2a(x - x₀): v² = 5² + 2(2)(16) = 25 + 64 = 89, so v = √89
        expected = math.sqrt(89) * ureg.meter / ureg.second
        assert abs(vel - expected) < 1e-6 * ureg.meter / ureg.second

    def test_aceleracion_tiempo_negativo(self):
        """Test acceleration with negative time (should work since acceleration is constant)."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=5 * ureg.meter / ureg.second,
            aceleracion_inicial=2 * ureg.meter / ureg.second**2
        )

        # Acceleration should be constant regardless of time
        acel = mruv.aceleracion(-1 * ureg.second)
        assert abs(acel.magnitude - 2) < 1e-10


class TestMRUVUnitsHandling:
    """Test proper units handling."""

    def test_init_with_mixed_units(self):
        """Test initialization with mixed but compatible units."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=100 * ureg.centimeter,  # cm
            velocidad_inicial=3.6 * ureg.kilometer / ureg.hour,  # km/h
            aceleracion_inicial=2 * ureg.meter / ureg.second**2  # m/s²
        )

        # Check that units are preserved (MRUV doesn't auto-convert)
        assert mruv.posicion_inicial.units == ureg.centimeter
        assert abs(mruv.posicion_inicial.magnitude - 100.0) < 1e-10

        assert mruv.velocidad_inicial.units == ureg.kilometer / ureg.hour
        assert abs(mruv.velocidad_inicial.magnitude - 3.6) < 1e-10

        assert mruv.aceleracion_inicial.units == ureg.meter / ureg.second**2
        assert abs(mruv.aceleracion_inicial.magnitude - 2.0) < 1e-10

    def test_calculations_with_different_time_units(self):
        """Test calculations with different time units."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=5 * ureg.meter / ureg.second,
            aceleracion_inicial=1 * ureg.meter / ureg.second**2
        )

        # Test with minutes
        pos_min = mruv.posicion(0.5 * ureg.minute)  # 30 seconds
        pos_sec = mruv.posicion(30 * ureg.second)

        assert abs(pos_min.magnitude - pos_sec.magnitude) < 1e-10

        # Test with milliseconds
        vel_ms = mruv.velocidad(2000 * ureg.millisecond)  # 2 seconds
        vel_sec = mruv.velocidad(2 * ureg.second)

        assert abs(vel_ms.magnitude - vel_sec.magnitude) < 1e-10


class TestMRUVPhysicsValidation:
    """Test physics consistency and validation."""

    def test_kinematic_equations_consistency(self):
        """Test that all kinematic equations are consistent."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=2 * ureg.meter,
            velocidad_inicial=3 * ureg.meter / ureg.second,
            aceleracion_inicial=1.5 * ureg.meter / ureg.second**2
        )

        t = 4 * ureg.second

        # Calculate using different methods
        pos = mruv.posicion(t)
        vel = mruv.velocidad(t)

        # Verify v² = v₀² + 2a(x - x₀)
        vel_from_pos = mruv.velocidad_sin_tiempo(pos)
        assert abs(vel.magnitude - vel_from_pos.magnitude) < 1e-10

        # Verify time calculation gives back original time
        tiempos = mruv.tiempo_por_posicion(pos)
        assert any(abs(t_calc.magnitude - t.magnitude) < 1e-10 for t_calc in tiempos)

    def test_zero_acceleration_reduces_to_mru(self):
        """Test that zero acceleration reduces to MRU behavior."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=5 * ureg.meter,
            velocidad_inicial=3 * ureg.meter / ureg.second,
            aceleracion_inicial=0 * ureg.meter / ureg.second**2
        )

        # Should behave like MRU
        for t_val in [1, 2, 5, 10]:
            t = t_val * ureg.second
            pos = mruv.posicion(t)
            vel = mruv.velocidad(t)

            # MRU: x = x₀ + vt, v = constant
            expected_pos = 5 + 3 * t_val
            assert abs(pos.magnitude - expected_pos) < 1e-10
            assert abs(vel.magnitude - 3) < 1e-10
