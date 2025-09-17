"""Property-based tests for Movimiento Rectilíneo Uniforme (MRU) using Hypothesis."""

import pytest
import math
from hypothesis import given, strategies as st, assume, settings
from cinetica.cinematica.rectilineo import MovimientoRectilineoUniforme
from cinetica.units import ureg


class TestMRUProperties:
    """Property-based tests for MRU physics laws and invariants."""

    @given(
        posicion_inicial=st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=200)
    def test_mru_position_linearity(self, posicion_inicial, velocidad_inicial, tiempo):
        """Property: Position should be linear with time for MRU."""
        # Skip edge cases that might cause numerical issues
        assume(abs(velocidad_inicial) > 1e-10 or abs(posicion_inicial) < 1e6)

        mru = MovimientoRectilineoUniforme(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second
        )

        # Test linearity: x(t) = x₀ + v₀*t
        posicion = mru.posicion(tiempo * ureg.second)
        expected = posicion_inicial + velocidad_inicial * tiempo

        assert abs(posicion.magnitude - expected) < 1e-10

    @given(
        posicion_inicial=st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        tiempo1=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False),
        tiempo2=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=200)
    def test_mru_velocity_constant(self, posicion_inicial, velocidad_inicial, tiempo1, tiempo2):
        """Property: Velocity should be constant for MRU at any time."""
        assume(abs(tiempo1 - tiempo2) > 1e-10)  # Avoid division by zero

        mru = MovimientoRectilineoUniforme(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second
        )

        vel1 = mru.velocidad(tiempo1 * ureg.second)
        vel2 = mru.velocidad(tiempo2 * ureg.second)

        # Velocity should be constant
        assert abs(vel1.magnitude - vel2.magnitude) < 1e-10
        assert abs(vel1.magnitude - velocidad_inicial) < 1e-10

    @given(
        posicion_inicial=st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        tiempo1=st.floats(min_value=0.1, max_value=50, allow_nan=False, allow_infinity=False),
        tiempo2=st.floats(min_value=0.1, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=200)
    def test_mru_average_velocity_equals_instantaneous(self, posicion_inicial, velocidad_inicial, tiempo1, tiempo2):
        """Property: Average velocity equals instantaneous velocity for MRU."""
        assume(abs(tiempo1 - tiempo2) > 1e-6)  # Avoid division by zero

        mru = MovimientoRectilineoUniforme(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second
        )

        pos1 = mru.posicion(tiempo1 * ureg.second)
        pos2 = mru.posicion(tiempo2 * ureg.second)
        vel_instantanea = mru.velocidad(tiempo1 * ureg.second)

        # Average velocity = (x2 - x1) / (t2 - t1)
        vel_promedio = (pos2.magnitude - pos1.magnitude) / (tiempo2 - tiempo1)

        assert abs(vel_promedio - vel_instantanea.magnitude) < 1e-9

    @given(
        posicion_inicial=st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mru_zero_acceleration(self, posicion_inicial, velocidad_inicial):
        """Property: Acceleration should always be zero for MRU."""
        mru = MovimientoRectilineoUniforme(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second
        )

        # Test acceleration at different times
        for tiempo in [0, 1, 5, 10, 100]:
            aceleracion = mru.aceleracion(tiempo * ureg.second)
            assert abs(aceleracion.magnitude) < 1e-15

    @given(
        posicion_inicial=st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
        delta_t=st.floats(min_value=0.1, max_value=10, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=150)
    def test_mru_displacement_proportional_to_time(self, posicion_inicial, velocidad_inicial, tiempo, delta_t):
        """Property: Displacement should be proportional to time interval for MRU."""
        assume(abs(velocidad_inicial) > 1e-10)  # Avoid zero velocity case

        mru = MovimientoRectilineoUniforme(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second
        )

        pos1 = mru.posicion(tiempo * ureg.second)
        pos2 = mru.posicion((tiempo + delta_t) * ureg.second)

        displacement = pos2.magnitude - pos1.magnitude
        expected_displacement = velocidad_inicial * delta_t

        assert abs(displacement - expected_displacement) < 1e-10

    @given(
        posicion_inicial=st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=0.1, max_value=100, allow_nan=False, allow_infinity=False),
        target_position=st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mru_time_calculation_consistency(self, posicion_inicial, velocidad_inicial, target_position):
        """Property: Time calculation should be consistent with position calculation."""
        assume(abs(target_position - posicion_inicial) > 1e-10)

        mru = MovimientoRectilineoUniforme(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second
        )

        # Calculate time to reach target position
        expected_time = (target_position - posicion_inicial) / velocidad_inicial

        if expected_time >= 0:  # Only test for positive times
            # Verify that position at calculated time equals target
            calculated_position = mru.posicion(expected_time * ureg.second)
            assert abs(calculated_position.magnitude - target_position) < 1e-10

    @given(
        posicion_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mru_units_consistency(self, posicion_inicial, velocidad_inicial, tiempo):
        """Property: Units should be consistent across all calculations."""
        mru = MovimientoRectilineoUniforme(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second
        )

        posicion = mru.posicion(tiempo * ureg.second)
        velocidad = mru.velocidad(tiempo * ureg.second)
        aceleracion = mru.aceleracion(tiempo * ureg.second)

        # Check units
        assert posicion.units == ureg.meter
        assert velocidad.units == ureg.meter / ureg.second
        assert aceleracion.units == ureg.meter / ureg.second**2

    @given(
        posicion_inicial=st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mru_time_translation_invariance(self, posicion_inicial, velocidad_inicial, tiempo):
        """Property: Physics should be invariant under time translation."""
        mru = MovimientoRectilineoUniforme(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second
        )

        # Position at time t
        pos_t = mru.posicion(tiempo * ureg.second)

        # Position at time t+dt should equal position at t plus displacement
        dt = 5.0
        pos_t_plus_dt = mru.posicion((tiempo + dt) * ureg.second)
        expected_pos = pos_t.magnitude + velocidad_inicial * dt

        assert abs(pos_t_plus_dt.magnitude - expected_pos) < 1e-10
