"""Property-based tests for Movimiento Rectilíneo Uniformemente Variado (MRUV) using Hypothesis."""

import pytest
import math
from hypothesis import given, strategies as st, assume, settings
from cinetica.cinematica.rectilineo import MovimientoRectilineoUniformementeVariado
from cinetica.units import ureg


class TestMRUVProperties:
    """Property-based tests for MRUV physics laws and invariants."""

    @given(
        posicion_inicial=st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        aceleracion=st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=200)
    def test_mruv_kinematic_equation_consistency(self, posicion_inicial, velocidad_inicial, aceleracion, tiempo):
        """Property: Position should follow kinematic equation x = x₀ + v₀t + ½at²."""
        assume(abs(aceleracion) > 1e-12 or abs(velocidad_inicial) > 1e-12)
        
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second,
            aceleracion_inicial=aceleracion * ureg.meter / ureg.second**2
        )
        
        posicion = mruv.posicion(tiempo * ureg.second)
        expected = posicion_inicial + velocidad_inicial * tiempo + 0.5 * aceleracion * tiempo**2
        
        assert abs(posicion.magnitude - expected) < 1e-10

    @given(
        posicion_inicial=st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        aceleracion=st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=200)
    def test_mruv_velocity_equation_consistency(self, posicion_inicial, velocidad_inicial, aceleracion, tiempo):
        """Property: Velocity should follow kinematic equation v = v₀ + at."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second,
            aceleracion_inicial=aceleracion * ureg.meter / ureg.second**2
        )
        
        velocidad = mruv.velocidad(tiempo * ureg.second)
        expected = velocidad_inicial + aceleracion * tiempo
        
        assert abs(velocidad.magnitude - expected) < 1e-10

    @given(
        posicion_inicial=st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        aceleracion=st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mruv_acceleration_constant(self, posicion_inicial, velocidad_inicial, aceleracion, tiempo):
        """Property: Acceleration should be constant for MRUV."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second,
            aceleracion_inicial=aceleracion * ureg.meter / ureg.second**2
        )
        
        accel_calculated = mruv.aceleracion(tiempo * ureg.second)
        assert abs(accel_calculated.magnitude - aceleracion) < 1e-12

    @given(
        posicion_inicial=st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        aceleracion=st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False),
        tiempo1=st.floats(min_value=0.1, max_value=25, allow_nan=False, allow_infinity=False),
        tiempo2=st.floats(min_value=0.1, max_value=25, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=150)
    def test_mruv_average_velocity_formula(self, posicion_inicial, velocidad_inicial, aceleracion, tiempo1, tiempo2):
        """Property: Average velocity should equal (v₁ + v₂)/2 for MRUV."""
        assume(abs(tiempo2 - tiempo1) > 1e-6)
        
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second,
            aceleracion_inicial=aceleracion * ureg.meter / ureg.second**2
        )
        
        pos1 = mruv.posicion(tiempo1 * ureg.second)
        pos2 = mruv.posicion(tiempo2 * ureg.second)
        vel1 = mruv.velocidad(tiempo1 * ureg.second)
        vel2 = mruv.velocidad(tiempo2 * ureg.second)
        
        # Average velocity from displacement
        avg_vel_displacement = (pos2.magnitude - pos1.magnitude) / (tiempo2 - tiempo1)
        
        # Average velocity from velocities
        avg_vel_formula = (vel1.magnitude + vel2.magnitude) / 2
        
        assert abs(avg_vel_displacement - avg_vel_formula) < 1e-10

    @given(
        posicion_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False),
        aceleracion=st.floats(min_value=0.1, max_value=20, allow_nan=False, allow_infinity=False),
        desplazamiento=st.floats(min_value=1, max_value=500, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mruv_velocity_without_time_formula(self, posicion_inicial, velocidad_inicial, aceleracion, desplazamiento):
        """Property: v² = v₀² + 2a(x - x₀) should hold for MRUV."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second,
            aceleracion_inicial=aceleracion * ureg.meter / ureg.second**2
        )

        target_position = posicion_inicial + desplazamiento

        # Calculate velocity using the formula v² = v₀² + 2a(x - x₀)
        vel_squared = velocidad_inicial**2 + 2 * aceleracion * desplazamiento

        if vel_squared >= 0:  # Only test for real velocities
            # The method returns signed velocity, so we need to handle both positive and negative cases
            calculated_velocity = mruv.velocidad_sin_tiempo(target_position * ureg.meter)
            expected_velocity_magnitude = math.sqrt(vel_squared)
            
            # Check if the magnitude matches (velocity can be positive or negative)
            assert abs(abs(calculated_velocity.magnitude) - expected_velocity_magnitude) < 1e-10

    @given(
        posicion_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False),
        aceleracion=st.floats(min_value=0.1, max_value=20, allow_nan=False, allow_infinity=False),
        target_position=st.floats(min_value=-500, max_value=500, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mruv_time_calculation_consistency(self, posicion_inicial, velocidad_inicial, aceleracion, target_position):
        """Property: Time calculation should be consistent with position calculation."""
        assume(abs(target_position - posicion_inicial) > 1e-6)
        
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second,
            aceleracion_inicial=aceleracion * ureg.meter / ureg.second**2
        )
        
        try:
            tiempos = mruv.tiempo_por_posicion(target_position * ureg.meter)
            
            # Test each valid positive time
            for tiempo in tiempos:
                if tiempo.magnitude >= 0:
                    calculated_position = mruv.posicion(tiempo)
                    assert abs(calculated_position.magnitude - target_position) < 1e-10
        except ValueError:
            # No real solutions exist, which is valid
            pass

    @given(
        posicion_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False),
        aceleracion=st.floats(min_value=-20, max_value=20, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mruv_energy_considerations(self, posicion_inicial, velocidad_inicial, aceleracion, tiempo):
        """Property: Kinetic energy change should equal work done by constant force."""
        assume(abs(aceleracion) > 1e-12)
        
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second,
            aceleracion_inicial=aceleracion * ureg.meter / ureg.second**2
        )
        
        # Initial and final velocities
        v0 = velocidad_inicial
        vf = mruv.velocidad(tiempo * ureg.second).magnitude
        
        # Initial and final positions
        x0 = posicion_inicial
        xf = mruv.posicion(tiempo * ureg.second).magnitude
        
        # Change in kinetic energy (per unit mass)
        delta_ke = 0.5 * (vf**2 - v0**2)
        
        # Work done by force (per unit mass): W = F*d = a*d
        work_done = aceleracion * (xf - x0)
        
        assert abs(delta_ke - work_done) < 1e-9

    @given(
        velocidad_inicial=st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False),
        aceleracion=st.floats(min_value=-20, max_value=20, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=30, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mruv_reduces_to_mru_when_acceleration_zero(self, velocidad_inicial, aceleracion, tiempo):
        """Property: MRUV should reduce to MRU when acceleration is zero."""
        assume(abs(aceleracion) < 1e-12)
        
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=0 * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second,
            aceleracion_inicial=aceleracion * ureg.meter / ureg.second**2
        )
        
        # Position should be linear: x = v₀*t
        posicion = mruv.posicion(tiempo * ureg.second)
        expected_position = velocidad_inicial * tiempo
        
        assert abs(posicion.magnitude - expected_position) < 1e-10
        
        # Velocity should be constant
        velocidad = mruv.velocidad(tiempo * ureg.second)
        assert abs(velocidad.magnitude - velocidad_inicial) < 1e-12

    @given(
        posicion_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False),
        aceleracion=st.floats(min_value=-20, max_value=20, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mruv_units_consistency(self, posicion_inicial, velocidad_inicial, aceleracion, tiempo):
        """Property: Units should be consistent across all calculations."""
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second,
            aceleracion_inicial=aceleracion * ureg.meter / ureg.second**2
        )
        
        posicion = mruv.posicion(tiempo * ureg.second)
        velocidad = mruv.velocidad(tiempo * ureg.second)
        aceleracion_calc = mruv.aceleracion(tiempo * ureg.second)
        
        # Check units
        assert posicion.units == ureg.meter
        assert velocidad.units == ureg.meter / ureg.second
        assert aceleracion_calc.units == ureg.meter / ureg.second**2

    @given(
        posicion_inicial=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_inicial=st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False),
        aceleracion=st.floats(min_value=-20, max_value=20, allow_nan=False, allow_infinity=False),
        tiempo1=st.floats(min_value=0, max_value=25, allow_nan=False, allow_infinity=False),
        tiempo2=st.floats(min_value=0, max_value=25, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mruv_time_reversal_symmetry(self, posicion_inicial, velocidad_inicial, aceleracion, tiempo1, tiempo2):
        """Property: Physics equations should be consistent under time transformations."""
        assume(abs(tiempo2 - tiempo1) > 1e-6)
        
        mruv = MovimientoRectilineoUniformementeVariado(
            posicion_inicial=posicion_inicial * ureg.meter,
            velocidad_inicial=velocidad_inicial * ureg.meter / ureg.second,
            aceleracion_inicial=aceleracion * ureg.meter / ureg.second**2
        )
        
        # Calculate positions at two different times
        pos1 = mruv.posicion(tiempo1 * ureg.second)
        pos2 = mruv.posicion(tiempo2 * ureg.second)
        
        # Calculate velocities at those times
        vel1 = mruv.velocidad(tiempo1 * ureg.second)
        vel2 = mruv.velocidad(tiempo2 * ureg.second)
        
        # The change in velocity should equal acceleration times time interval
        delta_v = vel2.magnitude - vel1.magnitude
        expected_delta_v = aceleracion * (tiempo2 - tiempo1)
        
        assert abs(delta_v - expected_delta_v) < 1e-10
