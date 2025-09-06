"""Property-based tests for Movimiento Espacial using Hypothesis."""

import pytest
import math
import numpy as np
from hypothesis import given, strategies as st, assume, settings
from cinetica.cinematica.espacial import MovimientoEspacial
from cinetica.units import ureg


class TestMovimientoEspacialProperties:
    """Property-based tests for 3D spatial motion physics laws and invariants."""

    @given(
        pos_inicial=st.lists(st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        vel_inicial=st.lists(st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        aceleracion=st.lists(st.floats(min_value=-20, max_value=20, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=150)
    def test_spatial_kinematic_equations(self, pos_inicial, vel_inicial, aceleracion, tiempo):
        """Property: 3D position should follow kinematic equation r = r₀ + v₀t + ½at²."""
        espacial = MovimientoEspacial(
            posicion_inicial=np.array(pos_inicial) * ureg.meter,
            velocidad_inicial=np.array(vel_inicial) * ureg.meter / ureg.second,
            aceleracion_constante=np.array(aceleracion) * ureg.meter / ureg.second**2
        )

        posicion = espacial.posicion(tiempo * ureg.second)

        # Calculate expected position for each component
        for i in range(3):
            expected = pos_inicial[i] + vel_inicial[i] * tiempo + 0.5 * aceleracion[i] * tiempo**2
            assert abs(posicion.magnitude[i] - expected) < 1e-10

    @given(
        pos_inicial=st.lists(st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        vel_inicial=st.lists(st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        aceleracion=st.lists(st.floats(min_value=-20, max_value=20, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=150)
    def test_spatial_velocity_equations(self, pos_inicial, vel_inicial, aceleracion, tiempo):
        """Property: 3D velocity should follow kinematic equation v = v₀ + at."""
        espacial = MovimientoEspacial(
            posicion_inicial=np.array(pos_inicial) * ureg.meter,
            velocidad_inicial=np.array(vel_inicial) * ureg.meter / ureg.second,
            aceleracion_constante=np.array(aceleracion) * ureg.meter / ureg.second**2
        )

        velocidad = espacial.velocidad(tiempo * ureg.second)

        # Calculate expected velocity for each component
        for i in range(3):
            expected = vel_inicial[i] + aceleracion[i] * tiempo
            assert abs(velocidad.magnitude[i] - expected) < 1e-10

    @given(
        pos_inicial=st.lists(st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        vel_inicial=st.lists(st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        aceleracion=st.lists(st.floats(min_value=-20, max_value=20, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_spatial_acceleration_constant(self, pos_inicial, vel_inicial, aceleracion, tiempo):
        """Property: Acceleration should be constant for spatial motion with constant acceleration."""
        espacial = MovimientoEspacial(
            posicion_inicial=np.array(pos_inicial) * ureg.meter,
            velocidad_inicial=np.array(vel_inicial) * ureg.meter / ureg.second,
            aceleracion_constante=np.array(aceleracion) * ureg.meter / ureg.second**2
        )

        accel_calculated = espacial.aceleracion(tiempo * ureg.second)

        # Check each component
        for i in range(3):
            assert abs(accel_calculated.magnitude[i] - aceleracion[i]) < 1e-12

    @given(
        pos_inicial=st.lists(st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        vel_inicial=st.lists(st.floats(min_value=-25, max_value=25, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        aceleracion=st.lists(st.floats(min_value=-10, max_value=10, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        tiempo1=st.floats(min_value=0.1, max_value=25, allow_nan=False, allow_infinity=False),
        tiempo2=st.floats(min_value=0.1, max_value=25, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_spatial_displacement_consistency(self, pos_inicial, vel_inicial, aceleracion, tiempo1, tiempo2):
        """Property: Displacement should be consistent with velocity integration."""
        assume(abs(tiempo2 - tiempo1) > 1e-6)

        espacial = MovimientoEspacial(
            posicion_inicial=np.array(pos_inicial) * ureg.meter,
            velocidad_inicial=np.array(vel_inicial) * ureg.meter / ureg.second,
            aceleracion_constante=np.array(aceleracion) * ureg.meter / ureg.second**2
        )

        pos1 = espacial.posicion(tiempo1 * ureg.second)
        pos2 = espacial.posicion(tiempo2 * ureg.second)
        vel1 = espacial.velocidad(tiempo1 * ureg.second)
        vel2 = espacial.velocidad(tiempo2 * ureg.second)

        # Average velocity should equal displacement / time
        displacement = pos2.magnitude - pos1.magnitude
        time_interval = tiempo2 - tiempo1
        avg_velocity_displacement = displacement / time_interval

        # Average velocity from velocities
        avg_velocity_formula = (vel1.magnitude + vel2.magnitude) / 2

        for i in range(3):
            assert abs(avg_velocity_displacement[i] - avg_velocity_formula[i]) < 1e-10

    @given(
        vel_inicial=st.lists(st.floats(min_value=-25, max_value=25, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        aceleracion=st.lists(st.floats(min_value=-10, max_value=10, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        tiempo=st.floats(min_value=0, max_value=30, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_spatial_reduces_to_uniform_when_no_acceleration(self, vel_inicial, aceleracion, tiempo):
        """Property: Spatial motion should reduce to uniform motion when acceleration is zero."""
        # Make acceleration very small (effectively zero)
        aceleracion_zero = [a * 1e-15 for a in aceleracion]

        espacial = MovimientoEspacial(
            posicion_inicial=np.array([0, 0, 0]) * ureg.meter,
            velocidad_inicial=np.array(vel_inicial) * ureg.meter / ureg.second,
            aceleracion_constante=np.array(aceleracion_zero) * ureg.meter / ureg.second**2
        )

        posicion = espacial.posicion(tiempo * ureg.second)
        velocidad = espacial.velocidad(tiempo * ureg.second)

        # Position should be linear: r = v₀*t
        for i in range(3):
            expected_position = vel_inicial[i] * tiempo
            assert abs(posicion.magnitude[i] - expected_position) < 1e-10

            # Velocity should be constant
            assert abs(velocidad.magnitude[i] - vel_inicial[i]) < 1e-12

    @given(
        pos_inicial=st.lists(st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        vel_inicial=st.lists(st.floats(min_value=-25, max_value=25, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        aceleracion=st.lists(st.floats(min_value=-10, max_value=10, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        tiempo=st.floats(min_value=0, max_value=30, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_spatial_energy_work_theorem(self, pos_inicial, vel_inicial, aceleracion, tiempo):
        """Property: Change in kinetic energy should equal work done by constant force."""
        assume(any(abs(a) > 1e-12 for a in aceleracion))

        espacial = MovimientoEspacial(
            posicion_inicial=np.array(pos_inicial) * ureg.meter,
            velocidad_inicial=np.array(vel_inicial) * ureg.meter / ureg.second,
            aceleracion_constante=np.array(aceleracion) * ureg.meter / ureg.second**2
        )

        # Initial and final states
        pos_initial = np.array(pos_inicial)
        vel_initial = np.array(vel_inicial)
        pos_final = espacial.posicion(tiempo * ureg.second).magnitude
        vel_final = espacial.velocidad(tiempo * ureg.second).magnitude

        # Change in kinetic energy (per unit mass)
        ke_initial = 0.5 * np.dot(vel_initial, vel_initial)
        ke_final = 0.5 * np.dot(vel_final, vel_final)
        delta_ke = ke_final - ke_initial

        # Work done by force (per unit mass): W = F·d = a·d
        displacement = pos_final - pos_initial
        work_done = np.dot(aceleracion, displacement)

        assert abs(delta_ke - work_done) < 1e-10

    @given(
        pos_inicial=st.lists(st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        vel_inicial=st.lists(st.floats(min_value=-25, max_value=25, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        aceleracion=st.lists(st.floats(min_value=-10, max_value=10, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        tiempo=st.floats(min_value=0, max_value=30, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_spatial_units_consistency(self, pos_inicial, vel_inicial, aceleracion, tiempo):
        """Property: Units should be consistent across all 3D calculations."""
        espacial = MovimientoEspacial(
            posicion_inicial=np.array(pos_inicial) * ureg.meter,
            velocidad_inicial=np.array(vel_inicial) * ureg.meter / ureg.second,
            aceleracion_constante=np.array(aceleracion) * ureg.meter / ureg.second**2
        )

        posicion = espacial.posicion(tiempo * ureg.second)
        velocidad = espacial.velocidad(tiempo * ureg.second)
        aceleracion_calc = espacial.aceleracion(tiempo * ureg.second)

        # Check units
        assert posicion.units == ureg.meter
        assert velocidad.units == ureg.meter / ureg.second
        assert aceleracion_calc.units == ureg.meter / ureg.second**2

        # Check dimensions
        assert len(posicion.magnitude) == 3
        assert len(velocidad.magnitude) == 3
        assert len(aceleracion_calc.magnitude) == 3

    @given(
        pos_inicial=st.lists(st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        vel_inicial=st.lists(st.floats(min_value=-25, max_value=25, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        aceleracion=st.lists(st.floats(min_value=-10, max_value=10, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        tiempo=st.floats(min_value=0, max_value=30, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_spatial_superposition_principle(self, pos_inicial, vel_inicial, aceleracion, tiempo):
        """Property: Motion in each dimension should be independent (superposition principle)."""
        espacial = MovimientoEspacial(
            posicion_inicial=np.array(pos_inicial) * ureg.meter,
            velocidad_inicial=np.array(vel_inicial) * ureg.meter / ureg.second,
            aceleracion_constante=np.array(aceleracion) * ureg.meter / ureg.second**2
        )

        posicion_3d = espacial.posicion(tiempo * ureg.second)
        velocidad_3d = espacial.velocidad(tiempo * ureg.second)

        # Test each dimension independently
        for i in range(3):
            # Create 1D motion for this dimension
            espacial_1d = MovimientoEspacial(
                posicion_inicial=np.array([pos_inicial[i] if j == i else 0 for j in range(3)]) * ureg.meter,
                velocidad_inicial=np.array([vel_inicial[i] if j == i else 0 for j in range(3)]) * ureg.meter / ureg.second,
                aceleracion_constante=np.array([aceleracion[i] if j == i else 0 for j in range(3)]) * ureg.meter / ureg.second**2
            )

            pos_1d = espacial_1d.posicion(tiempo * ureg.second)
            vel_1d = espacial_1d.velocidad(tiempo * ureg.second)

            # The i-th component should match
            assert abs(posicion_3d.magnitude[i] - pos_1d.magnitude[i]) < 1e-12
            assert abs(velocidad_3d.magnitude[i] - vel_1d.magnitude[i]) < 1e-12

    @given(
        pos_inicial=st.lists(st.floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        vel_inicial=st.lists(st.floats(min_value=-25, max_value=25, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        aceleracion=st.lists(st.floats(min_value=-10, max_value=10, allow_nan=False, allow_infinity=False), min_size=3, max_size=3),
        tiempo1=st.floats(min_value=0, max_value=15, allow_nan=False, allow_infinity=False),
        tiempo2=st.floats(min_value=0, max_value=15, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_spatial_time_translation_invariance(self, pos_inicial, vel_inicial, aceleracion, tiempo1, tiempo2):
        """Property: Physics should be invariant under time translation."""
        assume(abs(tiempo2 - tiempo1) > 1e-6)

        espacial = MovimientoEspacial(
            posicion_inicial=np.array(pos_inicial) * ureg.meter,
            velocidad_inicial=np.array(vel_inicial) * ureg.meter / ureg.second,
            aceleracion_constante=np.array(aceleracion) * ureg.meter / ureg.second**2
        )

        pos1 = espacial.posicion(tiempo1 * ureg.second)
        pos2 = espacial.posicion(tiempo2 * ureg.second)
        vel1 = espacial.velocidad(tiempo1 * ureg.second)
        vel2 = espacial.velocidad(tiempo2 * ureg.second)

        # The change in velocity should equal acceleration times time interval
        delta_v = vel2.magnitude - vel1.magnitude
        expected_delta_v = np.array(aceleracion) * (tiempo2 - tiempo1)

        for i in range(3):
            assert abs(delta_v[i] - expected_delta_v[i]) < 1e-10
