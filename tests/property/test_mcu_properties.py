"""Property-based tests for Movimiento Circular Uniforme (MCU) using Hypothesis."""

import pytest
import math
import numpy as np
from hypothesis import given, strategies as st, assume, settings
from cinetica.cinematica.circular import MovimientoCircularUniforme
from cinetica.units import ureg


class TestMCUProperties:
    """Property-based tests for MCU physics laws and invariants."""

    @given(
        radio=st.floats(min_value=0.1, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_angular=st.floats(min_value=0.1, max_value=50, allow_nan=False, allow_infinity=False),
        angulo_inicial=st.floats(min_value=0, max_value=2*math.pi, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=200)
    def test_mcu_angular_position_linearity(self, radio, velocidad_angular, angulo_inicial, tiempo):
        """Property: Angular position should be linear with time for MCU."""
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=angulo_inicial * ureg.radian,
            velocidad_angular_inicial=velocidad_angular * ureg.radian / ureg.second
        )
        
        # Angular position: θ(t) = θ₀ + ωt
        posicion_angular = mcu.posicion_angular(tiempo * ureg.second)
        expected = angulo_inicial + velocidad_angular * tiempo
        
        assert abs(posicion_angular.magnitude - expected) < 1e-10

    @given(
        radio=st.floats(min_value=0.1, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_angular=st.floats(min_value=0.1, max_value=50, allow_nan=False, allow_infinity=False),
        angulo_inicial=st.floats(min_value=0, max_value=2*math.pi, allow_nan=False, allow_infinity=False),
        tiempo1=st.floats(min_value=0, max_value=25, allow_nan=False, allow_infinity=False),
        tiempo2=st.floats(min_value=0, max_value=25, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=150)
    def test_mcu_angular_velocity_constant(self, radio, velocidad_angular, angulo_inicial, tiempo1, tiempo2):
        """Property: Angular velocity should be constant for MCU."""
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=angulo_inicial * ureg.radian,
            velocidad_angular_inicial=velocidad_angular * ureg.radian / ureg.second
        )
        
        vel_ang1 = mcu.velocidad_angular(tiempo1 * ureg.second)
        vel_ang2 = mcu.velocidad_angular(tiempo2 * ureg.second)
        
        # Angular velocity should be constant
        assert abs(vel_ang1.magnitude - vel_ang2.magnitude) < 1e-12
        assert abs(vel_ang1.magnitude - velocidad_angular) < 1e-12

    @given(
        radio=st.floats(min_value=0.1, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_angular=st.floats(min_value=0.1, max_value=50, allow_nan=False, allow_infinity=False),
        angulo_inicial=st.floats(min_value=0, max_value=2*math.pi, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=150)
    def test_mcu_tangential_velocity_magnitude(self, radio, velocidad_angular, angulo_inicial, tiempo):
        """Property: Tangential velocity magnitude should equal r*ω."""
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=angulo_inicial * ureg.radian,
            velocidad_angular_inicial=velocidad_angular * ureg.radian / ureg.second
        )
        
        velocidad_vector = mcu.velocidad(tiempo * ureg.second)
        velocidad_magnitude = np.linalg.norm(velocidad_vector)
        expected_magnitude = radio * velocidad_angular
        
        assert abs(velocidad_magnitude - expected_magnitude) < 1e-10

    @given(
        radio=st.floats(min_value=0.1, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_angular=st.floats(min_value=0.1, max_value=50, allow_nan=False, allow_infinity=False),
        angulo_inicial=st.floats(min_value=0, max_value=2*math.pi, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=150)
    def test_mcu_centripetal_acceleration_magnitude(self, radio, velocidad_angular, angulo_inicial, tiempo):
        """Property: Centripetal acceleration magnitude should equal v²/r = ω²r."""
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=angulo_inicial * ureg.radian,
            velocidad_angular_inicial=velocidad_angular * ureg.radian / ureg.second
        )
        
        aceleracion_centripeta = mcu.aceleracion_centripeta(tiempo * ureg.second)
        expected_magnitude = velocidad_angular**2 * radio
        
        assert abs(aceleracion_centripeta.magnitude - expected_magnitude) < 1e-10

    @given(
        radio=st.floats(min_value=0.1, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_angular=st.floats(min_value=0.1, max_value=50, allow_nan=False, allow_infinity=False),
        angulo_inicial=st.floats(min_value=0, max_value=2*math.pi, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mcu_position_on_circle(self, radio, velocidad_angular, angulo_inicial, tiempo):
        """Property: Position vector should always have magnitude equal to radius."""
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=angulo_inicial * ureg.radian,
            velocidad_angular_inicial=velocidad_angular * ureg.radian / ureg.second
        )
        
        posicion_vector = mcu.posicion_vector(tiempo * ureg.second)
        posicion_magnitude = np.linalg.norm(posicion_vector)
        
        assert abs(posicion_magnitude - radio) < 1e-10

    @given(
        radio=st.floats(min_value=0.1, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_angular=st.floats(min_value=0.1, max_value=50, allow_nan=False, allow_infinity=False),
        angulo_inicial=st.floats(min_value=0, max_value=2*math.pi, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mcu_velocity_perpendicular_to_position(self, radio, velocidad_angular, angulo_inicial, tiempo):
        """Property: Velocity vector should be perpendicular to position vector."""
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=angulo_inicial * ureg.radian,
            velocidad_angular_inicial=velocidad_angular * ureg.radian / ureg.second
        )
        
        posicion_vector = mcu.posicion_vector(tiempo * ureg.second)
        velocidad_vector = mcu.velocidad(tiempo * ureg.second)
        
        # Dot product should be zero for perpendicular vectors
        dot_product = np.dot(posicion_vector, velocidad_vector)
        
        assert abs(dot_product) < 1e-10

    @given(
        radio=st.floats(min_value=0.1, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_angular=st.floats(min_value=0.1, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mcu_period_frequency_relationship(self, radio, velocidad_angular):
        """Property: Period and frequency should satisfy T = 1/f = 2π/ω."""
        assume(velocidad_angular > 1e-6)  # Avoid division by zero
        
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=velocidad_angular * ureg.radian / ureg.second
        )
        
        periodo = mcu.periodo()
        frecuencia = mcu.frecuencia()
        
        # T = 2π/ω
        expected_periodo = 2 * math.pi / velocidad_angular
        assert abs(periodo.magnitude - expected_periodo) < 1e-10
        
        # f = ω/(2π)
        expected_frecuencia = velocidad_angular / (2 * math.pi)
        assert abs(frecuencia.magnitude - expected_frecuencia) < 1e-10
        
        # T * f = 1
        assert abs(periodo.magnitude * frecuencia.magnitude - 1) < 1e-10

    @given(
        radio=st.floats(min_value=0.1, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_angular=st.floats(min_value=0.1, max_value=10, allow_nan=False, allow_infinity=False),
        angulo_inicial=st.floats(min_value=0, max_value=2*math.pi, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=50)
    def test_mcu_periodic_motion(self, radio, velocidad_angular, angulo_inicial):
        """Property: Motion should be periodic with period T = 2π/ω."""
        assume(velocidad_angular > 1e-6)
        
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=angulo_inicial * ureg.radian,
            velocidad_angular_inicial=velocidad_angular * ureg.radian / ureg.second
        )
        
        periodo = 2 * math.pi / velocidad_angular
        
        # Position should repeat after one period
        pos_0 = mcu.posicion(0 * ureg.second)
        pos_T = mcu.posicion(periodo * ureg.second)
        
        assert abs(pos_0.magnitude[0] - pos_T.magnitude[0]) < 1e-10
        assert abs(pos_0.magnitude[1] - pos_T.magnitude[1]) < 1e-10

    @given(
        radio=st.floats(min_value=0.1, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_angular=st.floats(min_value=0.1, max_value=50, allow_nan=False, allow_infinity=False),
        tiempo1=st.floats(min_value=0, max_value=25, allow_nan=False, allow_infinity=False),
        tiempo2=st.floats(min_value=0, max_value=25, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mcu_angular_acceleration_zero(self, radio, velocidad_angular, tiempo1, tiempo2):
        """Property: Angular acceleration should be zero for uniform circular motion."""
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=velocidad_angular * ureg.radian / ureg.second
        )
        
        # Angular velocity should be constant (no angular acceleration method exists)
        vel_angular_1 = mcu.velocidad_angular(tiempo1 * ureg.second)
        vel_angular_2 = mcu.velocidad_angular(tiempo2 * ureg.second)
        
        assert abs(vel_angular_1.magnitude - vel_angular_2.magnitude) < 1e-10

    @given(
        radio=st.floats(min_value=0.1, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_angular=st.floats(min_value=0.1, max_value=50, allow_nan=False, allow_infinity=False),
        angulo_inicial=st.floats(min_value=0, max_value=2*math.pi, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mcu_units_consistency(self, radio, velocidad_angular, angulo_inicial, tiempo):
        """Property: All calculations should maintain unit consistency."""
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=angulo_inicial * ureg.radian,
            velocidad_angular_inicial=velocidad_angular * ureg.radian / ureg.second
        )
        
        # Check units of position (should be meters)
        posicion_cartesiana = mcu.posicion(tiempo * ureg.second)
        assert posicion_cartesiana.dimensionality == ureg.meter.dimensionality
        
        # Check units of velocity tangential (should be m/s)
        velocidad_tangencial = mcu.velocidad_tangencial(tiempo * ureg.second)
        assert velocidad_tangencial.dimensionality == (ureg.meter / ureg.second).dimensionality
        
        # Check units of angular position (should be radians)
        pos_angular = mcu.posicion_angular(tiempo * ureg.second)
        assert pos_angular.dimensionality == ureg.radian.dimensionality
        
        # Check units of angular velocity (should be rad/s)
        vel_angular = mcu.velocidad_angular(tiempo * ureg.second)
        assert vel_angular.dimensionality == (ureg.radian / ureg.second).dimensionality

    @given(
        radio=st.floats(min_value=0.1, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_angular=st.floats(min_value=0.1, max_value=50, allow_nan=False, allow_infinity=False),
        angulo_inicial=st.floats(min_value=0, max_value=2*math.pi, allow_nan=False, allow_infinity=False),
        tiempo1=st.floats(min_value=0, max_value=25, allow_nan=False, allow_infinity=False),
        tiempo2=st.floats(min_value=0, max_value=25, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mcu_energy_conservation(self, radio, velocidad_angular, angulo_inicial, tiempo1, tiempo2):
        """Property: Kinetic energy should remain constant in uniform circular motion."""
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=angulo_inicial * ureg.radian,
            velocidad_angular_inicial=velocidad_angular * ureg.radian / ureg.second
        )
        
        # Calculate kinetic energy at two different times
        v1 = mcu.velocidad(tiempo1 * ureg.second)
        v2 = mcu.velocidad(tiempo2 * ureg.second)
        
        ke1 = 0.5 * np.linalg.norm(v1)**2
        ke2 = 0.5 * np.linalg.norm(v2)**2
        
        # Use relative tolerance for large energy values
        max_ke = max(ke1, ke2)
        if max_ke > 0:
            assert abs(ke1 - ke2) / max_ke < 1e-12
        else:
            assert abs(ke1 - ke2) < 1e-12

    @given(
        radio=st.floats(min_value=0.1, max_value=100, allow_nan=False, allow_infinity=False),
        velocidad_angular=st.floats(min_value=0.1, max_value=50, allow_nan=False, allow_infinity=False),
        angulo_inicial=st.floats(min_value=0, max_value=2*math.pi, allow_nan=False, allow_infinity=False),
        tiempo=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_mcu_coordinate_transformation(self, radio, velocidad_angular, angulo_inicial, tiempo):
        """Property: Cartesian coordinates should match polar coordinates."""
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=angulo_inicial * ureg.radian,
            velocidad_angular_inicial=velocidad_angular * ureg.radian / ureg.second
        )
        
        posicion_vector = mcu.posicion(tiempo * ureg.second)
        posicion_angular = mcu.posicion_angular(tiempo * ureg.second)
        
        # Convert from polar to Cartesian
        x_expected = radio * math.cos(posicion_angular.magnitude)
        y_expected = radio * math.sin(posicion_angular.magnitude)
        
        assert abs(posicion_vector.magnitude[0] - x_expected) < 1e-10
        assert abs(posicion_vector.magnitude[1] - y_expected) < 1e-10
