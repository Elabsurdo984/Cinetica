import pytest
from cinetica.cinematica.rectilineo.movimiento_rectilineo_uniforme import (
    MovimientoRectilineoUniforme,
)
from cinetica.units import ureg, Q_


class TestMRUParametrized:
    """Parametrized tests for MRU with different unit configurations."""

    @pytest.mark.parametrize("pos_inicial, vel_inicial, tiempo, expected_pos", [
        # With units
        (10 * ureg.meter, 5 * ureg.meter / ureg.second, 2 * ureg.second, 20 * ureg.meter),
        (0 * ureg.meter, 10 * ureg.meter / ureg.second, 3 * ureg.second, 30 * ureg.meter),
        (5 * ureg.meter, -2 * ureg.meter / ureg.second, 4 * ureg.second, -3 * ureg.meter),
        # Without units (should auto-convert)
        (10, 5, 2, 20 * ureg.meter),
        (0, 10, 3, 30 * ureg.meter),
        (5, -2, 4, -3 * ureg.meter),
    ])
    def test_mru_posicion_parametrized(self, pos_inicial, vel_inicial, tiempo, expected_pos):
        """Test MRU position calculation with various parameters."""
        mru = MovimientoRectilineoUniforme(
            posicion_inicial=pos_inicial,
            velocidad_inicial=vel_inicial
        )
        pos = mru.posicion(tiempo)
        assert pos == expected_pos

    @pytest.mark.parametrize("pos_inicial, vel_inicial, expected_vel", [
        # With units
        (10 * ureg.meter, 5 * ureg.meter / ureg.second, 5 * ureg.meter / ureg.second),
        (0 * ureg.meter, -3 * ureg.meter / ureg.second, -3 * ureg.meter / ureg.second),
        (100 * ureg.meter, 0 * ureg.meter / ureg.second, 0 * ureg.meter / ureg.second),
        # Without units
        (10, 5, 5 * ureg.meter / ureg.second),
        (0, -3, -3 * ureg.meter / ureg.second),
        (100, 0, 0 * ureg.meter / ureg.second),
    ])
    def test_mru_velocidad_parametrized(self, pos_inicial, vel_inicial, expected_vel):
        """Test MRU velocity (constant) with various parameters."""
        mru = MovimientoRectilineoUniforme(
            posicion_inicial=pos_inicial,
            velocidad_inicial=vel_inicial
        )
        vel = mru.velocidad()
        assert vel == expected_vel

    @pytest.mark.parametrize("pos_inicial, vel_inicial", [
        # With units
        (10 * ureg.meter, 5 * ureg.meter / ureg.second),
        (0 * ureg.meter, -3 * ureg.meter / ureg.second),
        # Without units
        (10, 5),
        (0, -3),
    ])
    def test_mru_aceleracion_parametrized(self, pos_inicial, vel_inicial):
        """Test MRU acceleration (always zero) with various parameters."""
        mru = MovimientoRectilineoUniforme(
            posicion_inicial=pos_inicial,
            velocidad_inicial=vel_inicial
        )
        acc = mru.aceleracion()
        assert acc == 0.0 * ureg.meter / ureg.second**2


class TestMRUUnitConversions:
    """Parametrized tests for unit conversions in MRU."""

    @pytest.mark.parametrize("pos_inicial, vel_inicial, tiempo, pos_unit, vel_unit, time_unit", [
        # Different length units
        (1000 * ureg.millimeter, 2 * ureg.meter / ureg.second, 1 * ureg.second, ureg.millimeter, ureg.meter / ureg.second, ureg.second),
        (2 * ureg.kilometer, 50 * ureg.kilometer / ureg.hour, 0.5 * ureg.hour, ureg.kilometer, ureg.kilometer / ureg.hour, ureg.hour),
        (100 * ureg.centimeter, 3 * ureg.meter / ureg.second, 2 * ureg.second, ureg.centimeter, ureg.meter / ureg.second, ureg.second),
    ])
    def test_mru_mixed_units(self, pos_inicial, vel_inicial, tiempo, pos_unit, vel_unit, time_unit):
        """Test MRU with mixed unit systems."""
        mru = MovimientoRectilineoUniforme(
            posicion_inicial=pos_inicial,
            velocidad_inicial=vel_inicial
        )

        # Position calculation should work with mixed units
        pos = mru.posicion(tiempo)
        assert pos.dimensionality == ureg.meter.dimensionality

        # Velocity should maintain its units
        vel = mru.velocidad()
        assert vel.dimensionality == (ureg.meter / ureg.second).dimensionality


class TestMRUEdgeCases:
    """Parametrized tests for MRU edge cases."""

    @pytest.mark.parametrize("tiempo", [
        -1 * ureg.second,
        -5 * ureg.second,
        -0.1 * ureg.second,
    ])
    def test_mru_negative_time_behavior(self, tiempo):
        """Test MRU behavior with negative time (extrapolation to past)."""
        mru = MovimientoRectilineoUniforme(
            posicion_inicial=10 * ureg.meter,
            velocidad_inicial=5 * ureg.meter / ureg.second
        )
        # MRU should allow negative time for extrapolation
        pos = mru.posicion(tiempo)
        expected = 10 * ureg.meter + 5 * ureg.meter / ureg.second * tiempo
        assert pos == expected

    @pytest.mark.parametrize("pos_inicial, vel_inicial, tiempo_values", [
        (0, 0, [0, 1, 5, 10]),  # Zero initial conditions
        (100, 0, [0, 1, 5, 10]),  # Zero velocity
        (0, 50, [0, 1, 5, 10]),  # Zero initial position
    ])
    def test_mru_zero_conditions(self, pos_inicial, vel_inicial, tiempo_values):
        """Test MRU behavior with zero initial conditions."""
        mru = MovimientoRectilineoUniforme(
            posicion_inicial=pos_inicial * ureg.meter,
            velocidad_inicial=vel_inicial * ureg.meter / ureg.second
        )

        for t in tiempo_values:
            pos = mru.posicion(t * ureg.second)
            expected = (pos_inicial + vel_inicial * t) * ureg.meter
            assert pos == expected
