import pytest
import math
from cinetica.cinematica.rectilineo.movimiento_rectilineo_uniformemente_variado import (
    MovimientoRectilineoUniformementeVariado,
)
from cinetica.units import ureg, Q_


class TestMRUVParametrized:
    """Parametrized tests for MRUV with different unit configurations."""

    @pytest.mark.parametrize("pos_inicial, vel_inicial, aceleracion, tiempo, expected_pos", [
        # With units - basic cases
        (10 * ureg.meter, 5 * ureg.meter / ureg.second, 2 * ureg.meter / ureg.second**2, 2 * ureg.second, 24 * ureg.meter),
        (0 * ureg.meter, 0 * ureg.meter / ureg.second, 10 * ureg.meter / ureg.second**2, 3 * ureg.second, 45 * ureg.meter),
        (20 * ureg.meter, 10 * ureg.meter / ureg.second, -5 * ureg.meter / ureg.second**2, 2 * ureg.second, 30 * ureg.meter),
        # Without units (should auto-convert)
        (10, 5, 2, 2, 24 * ureg.meter),
        (0, 0, 10, 3, 45 * ureg.meter),
        (20, 10, -5, 2, 30 * ureg.meter),
        # Zero acceleration (reduces to MRU)
        (5 * ureg.meter, 8 * ureg.meter / ureg.second, 0 * ureg.meter / ureg.second**2, 4 * ureg.second, 37 * ureg.meter),
        # Negative initial velocity
        (100 * ureg.meter, -20 * ureg.meter / ureg.second, 5 * ureg.meter / ureg.second**2, 3 * ureg.second, 62.5 * ureg.meter),
    ])
    def test_mruv_posicion_parametrized(self, pos_inicial, vel_inicial, aceleracion, tiempo, expected_pos):
        """Test MRUV position calculation with various parameters."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=pos_inicial,
            velocidad_inicial=vel_inicial,
            aceleracion_inicial=aceleracion
        )
        pos = mruv.posicion(tiempo)
        assert abs(pos - expected_pos) < 1e-10 * ureg.meter

    @pytest.mark.parametrize("pos_inicial, vel_inicial, aceleracion, tiempo, expected_vel", [
        # With units
        (10 * ureg.meter, 5 * ureg.meter / ureg.second, 2 * ureg.meter / ureg.second**2, 2 * ureg.second, 9 * ureg.meter / ureg.second),
        (0 * ureg.meter, 0 * ureg.meter / ureg.second, 10 * ureg.meter / ureg.second**2, 3 * ureg.second, 30 * ureg.meter / ureg.second),
        (20 * ureg.meter, 15 * ureg.meter / ureg.second, -3 * ureg.meter / ureg.second**2, 4 * ureg.second, 3 * ureg.meter / ureg.second),
        # Without units
        (10, 5, 2, 2, 9 * ureg.meter / ureg.second),
        (0, 0, 10, 3, 30 * ureg.meter / ureg.second),
        (20, 15, -3, 4, 3 * ureg.meter / ureg.second),
        # Zero time (initial velocity)
        (5, 12, 8, 0, 12 * ureg.meter / ureg.second),
    ])
    def test_mruv_velocidad_parametrized(self, pos_inicial, vel_inicial, aceleracion, tiempo, expected_vel):
        """Test MRUV velocity calculation with various parameters."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=pos_inicial,
            velocidad_inicial=vel_inicial,
            aceleracion_inicial=aceleracion
        )
        vel = mruv.velocidad(tiempo)
        assert abs(vel - expected_vel) < 1e-10 * ureg.meter / ureg.second

    @pytest.mark.parametrize("pos_inicial, vel_inicial, aceleracion, expected_acc", [
        # With units
        (10 * ureg.meter, 5 * ureg.meter / ureg.second, 2 * ureg.meter / ureg.second**2, 2 * ureg.meter / ureg.second**2),
        (0 * ureg.meter, 0 * ureg.meter / ureg.second, -9.8 * ureg.meter / ureg.second**2, -9.8 * ureg.meter / ureg.second**2),
        (100 * ureg.meter, 50 * ureg.meter / ureg.second, 0 * ureg.meter / ureg.second**2, 0 * ureg.meter / ureg.second**2),
        # Without units
        (10, 5, 2, 2 * ureg.meter / ureg.second**2),
        (0, 0, -9.8, -9.8 * ureg.meter / ureg.second**2),
        (100, 50, 0, 0 * ureg.meter / ureg.second**2),
    ])
    def test_mruv_aceleracion_parametrized(self, pos_inicial, vel_inicial, aceleracion, expected_acc):
        """Test MRUV acceleration (constant) with various parameters."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=pos_inicial,
            velocidad_inicial=vel_inicial,
            aceleracion_inicial=aceleracion
        )
        acc = mruv.aceleracion()
        assert acc == expected_acc


class TestMRUVPhysicsValidation:
    """Parametrized tests for MRUV physics validation."""

    @pytest.mark.parametrize("vel_inicial, aceleracion, desplazamiento, expected_vel_final", [
        # Using kinematic equation: v² = v₀² + 2aΔx
        (0, 10, 5, math.sqrt(100)),  # Free fall from rest
        (10, 2, 8, math.sqrt(132)),  # Acceleration
        (15, 3, 6, math.sqrt(261)),  # Another acceleration case
        (25, 4, 12, math.sqrt(721)),  # Strong acceleration
    ])
    def test_mruv_kinematic_equation_validation(self, vel_inicial, aceleracion, desplazamiento, expected_vel_final):
        """Test MRUV using kinematic equations for physics validation."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=vel_inicial * ureg.meter / ureg.second,
            aceleracion_inicial=aceleracion * ureg.meter / ureg.second**2
        )

        # Calculate time needed for given displacement
        # Using: x = v₀t + ½at²
        # Solving quadratic equation: ½at² + v₀t - x = 0
        a = aceleracion / 2
        b = vel_inicial
        c = -desplazamiento

        discriminant = b**2 - 4*a*c
        if discriminant >= 0 and a != 0:
            t1 = (-b + math.sqrt(discriminant)) / (2*a)
            t2 = (-b - math.sqrt(discriminant)) / (2*a)
            # Choose the positive time that makes physical sense
            t = t1 if t1 > 0 else t2

            if t > 0:
                vel_final = mruv.velocidad(t * ureg.second)
                expected = expected_vel_final * ureg.meter / ureg.second
                assert abs(vel_final - expected) < 1e-6 * ureg.meter / ureg.second


class TestMRUVUnitConversions:
    """Parametrized tests for unit conversions in MRUV."""

    @pytest.mark.parametrize("pos_inicial, vel_inicial, aceleracion, tiempo", [
        # Different unit systems
        (1000 * ureg.millimeter, 2 * ureg.meter / ureg.second, 5 * ureg.meter / ureg.second**2, 1 * ureg.second),
        (2 * ureg.kilometer, 50 * ureg.kilometer / ureg.hour, 10 * ureg.meter / ureg.second**2, 0.5 * ureg.hour),
        (100 * ureg.centimeter, 300 * ureg.centimeter / ureg.second, 200 * ureg.centimeter / ureg.second**2, 2 * ureg.second),
    ])
    def test_mruv_mixed_units(self, pos_inicial, vel_inicial, aceleracion, tiempo):
        """Test MRUV with mixed unit systems."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=pos_inicial,
            velocidad_inicial=vel_inicial,
            aceleracion_inicial=aceleracion
        )

        # All calculations should work with mixed units
        pos = mruv.posicion(tiempo)
        vel = mruv.velocidad(tiempo)
        acc = mruv.aceleracion()

        # Check dimensionality consistency
        assert pos.dimensionality == ureg.meter.dimensionality
        assert vel.dimensionality == (ureg.meter / ureg.second).dimensionality
        assert acc.dimensionality == (ureg.meter / ureg.second**2).dimensionality


class TestMRUVEdgeCases:
    """Parametrized tests for MRUV edge cases."""

    @pytest.mark.parametrize("tiempo", [
        -1 * ureg.second,
        -5 * ureg.second,
        -0.1 * ureg.second,
    ])
    def test_mruv_negative_time_error(self, tiempo):
        """Test that MRUV raises error for negative time."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=5 * ureg.meter / ureg.second,
            aceleracion_inicial=2 * ureg.meter / ureg.second**2
        )
        with pytest.raises(ValueError, match="El tiempo no puede ser negativo"):
            mruv.posicion(tiempo)
        with pytest.raises(ValueError, match="El tiempo no puede ser negativo"):
            mruv.velocidad(tiempo)

    @pytest.mark.parametrize("vel_inicial, aceleracion, tiempo_values", [
        (0, 0, [0, 1, 5, 10]),  # Zero initial conditions
        (100, 0, [0, 1, 5, 10]),  # Zero acceleration (MRU case)
        (0, 10, [0, 1, 2, 3]),  # Zero initial velocity
        (-50, 10, [0, 1, 2, 5]),  # Negative initial velocity
    ])
    def test_mruv_special_conditions(self, vel_inicial, aceleracion, tiempo_values):
        """Test MRUV behavior with special initial conditions."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=vel_inicial * ureg.meter / ureg.second,
            aceleracion_inicial=aceleracion * ureg.meter / ureg.second**2
        )

        for t in tiempo_values:
            pos = mruv.posicion(t * ureg.second)
            vel = mruv.velocidad(t * ureg.second)

            # Verify kinematic equations
            expected_pos = (vel_inicial * t + 0.5 * aceleracion * t**2) * ureg.meter
            expected_vel = (vel_inicial + aceleracion * t) * ureg.meter / ureg.second

            assert abs(pos - expected_pos) < 1e-10 * ureg.meter
            assert abs(vel - expected_vel) < 1e-10 * ureg.meter / ureg.second


def test_mruv_velocidad_sin_tiempo_with_units():
    mruv = MovimientoRectilineoUniformementeVariado(
        posicion_inicial=0 * ureg.meter,
        velocidad_inicial=0 * ureg.meter / ureg.second,
        aceleracion_inicial=2 * ureg.meter / ureg.second**2,
    )
    vel_final = mruv.velocidad_sin_tiempo(16 * ureg.meter)
    assert vel_final == 8 * ureg.meter / ureg.second  # v^2 = 0^2 + 2*2*16 = 64, v = 8


def test_mruv_velocidad_sin_tiempo_without_units():
    mruv = MovimientoRectilineoUniformementeVariado(
        posicion_inicial=0, velocidad_inicial=0, aceleracion_inicial=2
    )
    vel_final = mruv.velocidad_sin_tiempo(16)
    assert vel_final == 8 * ureg.meter / ureg.second
