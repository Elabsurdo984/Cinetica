import pytest
import math
import numpy as np
from cinetica.cinematica.circular.movimiento_circular_uniforme import (
    MovimientoCircularUniforme,
)
from cinetica.cinematica.circular.movimiento_circular_uniformemente_variado import (
    MovimientoCircularUniformementeVariado,
)
from cinetica.units import ureg, Q_


class TestMCUParametrized:
    """Parametrized tests for MCU (Uniform Circular Motion)."""
    
    @pytest.mark.parametrize("radio, pos_ang_inicial, vel_ang_inicial", [
        # With units
        (10 * ureg.meter, 0.5 * ureg.radian, 2 * ureg.radian / ureg.second),
        (5 * ureg.meter, math.pi * ureg.radian, 1.5 * ureg.radian / ureg.second),
        (2.5 * ureg.meter, 0 * ureg.radian, 4 * ureg.radian / ureg.second),
        # Without units (should auto-convert)
        (10, 0.5, 2),
        (5, math.pi, 1.5),
        (2.5, 0, 4),
    ])
    def test_mcu_initialization_parametrized(self, radio, pos_ang_inicial, vel_ang_inicial):
        """Test MCU initialization with various parameters."""
        mcu = MovimientoCircularUniforme(
            radio=radio,
            posicion_angular_inicial=pos_ang_inicial,
            velocidad_angular_inicial=vel_ang_inicial
        )
        
        # Check that values are properly converted to units
        expected_radio = radio if hasattr(radio, 'units') else radio * ureg.meter
        expected_pos = pos_ang_inicial if hasattr(pos_ang_inicial, 'units') else pos_ang_inicial * ureg.radian
        expected_vel = vel_ang_inicial if hasattr(vel_ang_inicial, 'units') else vel_ang_inicial * ureg.radian / ureg.second
        
        assert mcu.radio == expected_radio
        assert mcu.posicion_angular_inicial == expected_pos
        assert mcu.velocidad_angular_inicial == expected_vel
    
    @pytest.mark.parametrize("radio, pos_ang_inicial, vel_ang_inicial, tiempo, expected_pos_ang", [
        # With units
        (10 * ureg.meter, 0 * ureg.radian, 2 * ureg.radian / ureg.second, 1 * ureg.second, 2 * ureg.radian),
        (5 * ureg.meter, math.pi/2 * ureg.radian, 3 * ureg.radian / ureg.second, 2 * ureg.second, (math.pi/2 + 6) * ureg.radian),
        (8 * ureg.meter, math.pi * ureg.radian, 0.5 * ureg.radian / ureg.second, 4 * ureg.second, (math.pi + 2) * ureg.radian),
        # Without units
        (10, 0, 2, 1, 2 * ureg.radian),
        (5, math.pi/2, 3, 2, (math.pi/2 + 6) * ureg.radian),
        (8, math.pi, 0.5, 4, (math.pi + 2) * ureg.radian),
    ])
    def test_mcu_posicion_angular_parametrized(self, radio, pos_ang_inicial, vel_ang_inicial, tiempo, expected_pos_ang):
        """Test MCU angular position calculation with various parameters."""
        mcu = MovimientoCircularUniforme(radio, pos_ang_inicial, vel_ang_inicial)
        pos_ang = mcu.posicion_angular(tiempo)
        assert abs(pos_ang - expected_pos_ang) < 1e-10 * ureg.radian
    
    @pytest.mark.parametrize("radio, vel_ang_inicial, expected_vel_tang", [
        # With units
        (10 * ureg.meter, 2 * ureg.radian / ureg.second, 20 * ureg.meter / ureg.second),
        (5 * ureg.meter, 3 * ureg.radian / ureg.second, 15 * ureg.meter / ureg.second),
        (2.5 * ureg.meter, 4 * ureg.radian / ureg.second, 10 * ureg.meter / ureg.second),
        # Without units
        (10, 2, 20 * ureg.meter / ureg.second),
        (5, 3, 15 * ureg.meter / ureg.second),
        (2.5, 4, 10 * ureg.meter / ureg.second),
    ])
    def test_mcu_velocidad_tangencial_parametrized(self, radio, vel_ang_inicial, expected_vel_tang):
        """Test MCU tangential velocity calculation with various parameters."""
        mcu = MovimientoCircularUniforme(radio, 0, vel_ang_inicial)
        vel_tang = mcu.velocidad_tangencial()
        assert abs(vel_tang - expected_vel_tang) < 1e-10 * ureg.meter / ureg.second
    
    @pytest.mark.parametrize("radio, vel_ang_inicial, expected_acc_centripeta", [
        # With units
        (10 * ureg.meter, 2 * ureg.radian / ureg.second, 40 * ureg.meter / ureg.second**2),
        (5 * ureg.meter, 3 * ureg.radian / ureg.second, 45 * ureg.meter / ureg.second**2),
        (8 * ureg.meter, 1.5 * ureg.radian / ureg.second, 18 * ureg.meter / ureg.second**2),
        # Without units
        (10, 2, 40 * ureg.meter / ureg.second**2),
        (5, 3, 45 * ureg.meter / ureg.second**2),
        (8, 1.5, 18 * ureg.meter / ureg.second**2),
    ])
    def test_mcu_aceleracion_centripeta_parametrized(self, radio, vel_ang_inicial, expected_acc_centripeta):
        """Test MCU centripetal acceleration calculation with various parameters."""
        mcu = MovimientoCircularUniforme(radio, 0, vel_ang_inicial)
        acc_centripeta = mcu.aceleracion_centripeta()
        assert abs(acc_centripeta - expected_acc_centripeta) < 1e-10 * ureg.meter / ureg.second**2


class TestMCUVParametrized:
    """Parametrized tests for MCUV (Uniformly Accelerated Circular Motion)."""
    
    @pytest.mark.parametrize("radio, pos_ang_inicial, vel_ang_inicial, acc_ang", [
        # With units
        (10 * ureg.meter, 0 * ureg.radian, 2 * ureg.radian / ureg.second, 1 * ureg.radian / ureg.second**2),
        (5 * ureg.meter, math.pi/4 * ureg.radian, 1.5 * ureg.radian / ureg.second, -0.5 * ureg.radian / ureg.second**2),
        (8 * ureg.meter, math.pi * ureg.radian, 0 * ureg.radian / ureg.second, 2 * ureg.radian / ureg.second**2),
        # Without units
        (10, 0, 2, 1),
        (5, math.pi/4, 1.5, -0.5),
        (8, math.pi, 0, 2),
    ])
    def test_mcuv_initialization_parametrized(self, radio, pos_ang_inicial, vel_ang_inicial, acc_ang):
        """Test MCUV initialization with various parameters."""
        mcuv = MovimientoCircularUniformementeVariado(
            radio=radio,
            posicion_angular_inicial=pos_ang_inicial,
            velocidad_angular_inicial=vel_ang_inicial,
            aceleracion_angular_inicial=acc_ang
        )
        
        # Check that values are properly converted to units
        expected_radio = radio if hasattr(radio, 'units') else radio * ureg.meter
        expected_pos = pos_ang_inicial if hasattr(pos_ang_inicial, 'units') else pos_ang_inicial * ureg.radian
        expected_vel = vel_ang_inicial if hasattr(vel_ang_inicial, 'units') else vel_ang_inicial * ureg.radian / ureg.second
        expected_acc = acc_ang if hasattr(acc_ang, 'units') else acc_ang * ureg.radian / ureg.second**2
        
        assert mcuv.radio == expected_radio
        assert mcuv.posicion_angular_inicial == expected_pos
        assert mcuv.velocidad_angular_inicial == expected_vel
        assert mcuv.aceleracion_angular_inicial == expected_acc


class TestCircularMotionUnitConversions:
    """Parametrized tests for unit conversions in circular motion."""
    
    @pytest.mark.parametrize("radio_mm, vel_ang_rpm", [
        (1000, 60),  # 1m radius, 60 RPM
        (500, 120),  # 0.5m radius, 120 RPM
        (2000, 30),  # 2m radius, 30 RPM
    ])
    def test_mcu_unit_conversions(self, radio_mm, vel_ang_rpm):
        """Test MCU with different unit systems (mm, RPM)."""
        # Convert RPM to rad/s: RPM * 2π / 60
        vel_ang_rad_s = vel_ang_rpm * 2 * math.pi / 60
        
        mcu = MovimientoCircularUniforme(
            radio=radio_mm * ureg.millimeter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=vel_ang_rpm * ureg.revolution / ureg.minute
        )
        
        # Check that internal conversion works
        assert mcu.radio.to(ureg.meter).magnitude == radio_mm / 1000
        
        # Tangential velocity should be consistent
        vel_tang = mcu.velocidad_tangencial()
        expected_vel_tang = (radio_mm / 1000) * vel_ang_rad_s * ureg.meter / ureg.second
        assert abs(vel_tang - expected_vel_tang) < 1e-6 * ureg.meter / ureg.second


class TestCircularMotionEdgeCases:
    """Parametrized tests for circular motion edge cases."""
    
    @pytest.mark.parametrize("tiempo", [
        -1 * ureg.second,
        -5 * ureg.second,
        -0.1 * ureg.second,
    ])
    def test_mcu_negative_time_error(self, tiempo):
        """Test that MCU raises error for negative time."""
        mcu = MovimientoCircularUniforme(
            radio=5 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=2 * ureg.radian / ureg.second
        )
        with pytest.raises(ValueError, match="El tiempo no puede ser negativo"):
            mcu.posicion_angular(tiempo)
    
    @pytest.mark.parametrize("radio", [
        -1 * ureg.meter,
        -5 * ureg.meter,
        0 * ureg.meter,
    ])
    def test_mcu_invalid_radius_error(self, radio):
        """Test that MCU raises error for invalid radius."""
        with pytest.raises(ValueError, match="El radio debe ser un valor positivo"):
            MovimientoCircularUniforme(
                radio=radio,
                posicion_angular_inicial=0 * ureg.radian,
                velocidad_angular_inicial=2 * ureg.radian / ureg.second
            )
    
    @pytest.mark.parametrize("radio, vel_ang, tiempo_values", [
        (1, 0, [0, 1, 5, 10]),  # Zero angular velocity
        (10, 1, [0, math.pi, 2*math.pi, 4*math.pi]),  # Multiple revolutions
        (5, 2, [0, 0.5, 1, 2]),  # Various time points
    ])
    def test_mcu_special_conditions(self, radio, vel_ang, tiempo_values):
        """Test MCU behavior with special conditions."""
        mcu = MovimientoCircularUniforme(
            radio=radio * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=vel_ang * ureg.radian / ureg.second
        )
        
        for t in tiempo_values:
            pos_ang = mcu.posicion_angular(t * ureg.second)
            expected_pos = vel_ang * t * ureg.radian
            assert abs(pos_ang - expected_pos) < 1e-10 * ureg.radian


# Keep existing individual tests for backward compatibility
def test_mcu_velocidad_tangencial_with_units():
    mcu = MovimientoCircularUniforme(
        10 * ureg.meter, 0 * ureg.radian, 2 * ureg.radian / ureg.second
    )
    vel_tan = mcu.velocidad_tangencial()
    assert vel_tan == 20 * ureg.meter / ureg.second


def test_mcu_aceleracion_centripeta_with_units():
    mcu = MovimientoCircularUniforme(
        10 * ureg.meter, 0 * ureg.radian, 2 * ureg.radian / ureg.second
    )
    acc_cent = mcu.aceleracion_centripeta()
    assert acc_cent == 40 * ureg.meter / ureg.second**2  # (2 rad/s)^2 * 10 m = 40 m/s^2


def test_mcu_periodo_with_units():
    mcu = MovimientoCircularUniforme(
        10 * ureg.meter, 0 * ureg.radian, 2 * ureg.radian / ureg.second
    )
    period = mcu.periodo()
    assert period == (2 * math.pi / 2) * ureg.second


def test_mcu_frecuencia_with_units():
    mcu = MovimientoCircularUniforme(
        10 * ureg.meter, 0 * ureg.radian, 2 * ureg.radian / ureg.second
    )
    freq = mcu.frecuencia()
    assert freq == (2 / (2 * math.pi)) * ureg.hertz


def test_mcu_posicion_vector_with_units():
    mcu = MovimientoCircularUniforme(
        1 * ureg.meter, 0 * ureg.radian, math.pi / 2 * ureg.radian / ureg.second
    )
    pos_vec = mcu.posicion(1 * ureg.second)  # At t=1s, theta = pi/2, so x=0, y=1
    assert np.allclose(pos_vec.magnitude, np.array([0.0, 1.0]))
    assert pos_vec.units == ureg.meter


def test_mcu_velocidad_vector_with_units():
    mcu = MovimientoCircularUniforme(
        1 * ureg.meter, 0 * ureg.radian, math.pi / 2 * ureg.radian / ureg.second
    )
    vel_vec = mcu.velocidad(
        1 * ureg.second
    )  # At t=1s, theta = pi/2, v_tan = pi/2, vx = -pi/2, vy = 0
    assert np.allclose(vel_vec, np.array([-math.pi / 2, 0.0]))
    assert isinstance(vel_vec, np.ndarray)


def test_mcu_aceleracion_vector_with_units():
    mcu = MovimientoCircularUniforme(
        1 * ureg.meter, 0 * ureg.radian, math.pi / 2 * ureg.radian / ureg.second
    )
    acc_magnitude = mcu.aceleracion(
        1 * ureg.second
    )  # At t=1s, ac = (pi/2)^2 * 1 = pi^2/4
    expected_magnitude = (math.pi / 2) ** 2 * 1  # ω²r
    assert np.allclose(acc_magnitude.magnitude, expected_magnitude, atol=1e-8)
    assert acc_magnitude.units.dimensionality == (ureg.meter / ureg.second**2).dimensionality


# --- MovimientoCircularUniformementeVariado Tests ---
def test_mcuv_init_with_units():
    mcuv = MovimientoCircularUniformementeVariado(
        radio=5 * ureg.meter,
        posicion_angular_inicial=0 * ureg.radian,
        velocidad_angular_inicial=1 * ureg.radian / ureg.second,
        aceleracion_angular_inicial=0.5 * ureg.radian / ureg.second**2,
    )
    assert mcuv.radio == 5 * ureg.meter
    assert mcuv.posicion_angular_inicial == 0 * ureg.radian
    assert mcuv.velocidad_angular_inicial == 1 * ureg.radian / ureg.second
    assert mcuv.aceleracion_angular_inicial == 0.5 * ureg.radian / ureg.second**2


def test_mcuv_posicion_angular_with_units():
    mcuv = MovimientoCircularUniformementeVariado(
        5 * ureg.meter,
        0 * ureg.radian,
        1 * ureg.radian / ureg.second,
        0.5 * ureg.radian / ureg.second**2,
    )
    pos_ang = mcuv.posicion_angular(2 * ureg.second)
    assert pos_ang == (0 + 1 * 2 + 0.5 * 0.5 * 2**2) * ureg.radian  # 2 + 1 = 3 rad


def test_mcuv_velocidad_angular_with_units():
    mcuv = MovimientoCircularUniformementeVariado(
        5 * ureg.meter,
        0 * ureg.radian,
        1 * ureg.radian / ureg.second,
        0.5 * ureg.radian / ureg.second**2,
    )
    vel_ang = mcuv.velocidad_angular(2 * ureg.second)
    assert vel_ang == (1 + 0.5 * 2) * ureg.radian / ureg.second  # 1 + 1 = 2 rad/s


def test_mcuv_aceleracion_angular_with_units():
    mcuv = MovimientoCircularUniformementeVariado(
        5 * ureg.meter, aceleracion_angular_inicial=0.5 * ureg.radian / ureg.second**2
    )
    acc_ang = mcuv.aceleracion_angular()
    assert acc_ang == 0.5 * ureg.radian / ureg.second**2


def test_mcuv_velocidad_tangencial_with_units():
    mcuv = MovimientoCircularUniformementeVariado(
        5 * ureg.meter,
        0 * ureg.radian,
        1 * ureg.radian / ureg.second,
        0.5 * ureg.radian / ureg.second**2,
    )
    vel_tan = mcuv.velocidad_tangencial(2 * ureg.second)
    assert vel_tan == (2 * 5) * ureg.meter / ureg.second  # 10 m/s


def test_mcuv_aceleracion_tangencial_with_units():
    mcuv = MovimientoCircularUniformementeVariado(
        5 * ureg.meter, aceleracion_angular_inicial=0.5 * ureg.radian / ureg.second**2
    )
    acc_tan = mcuv.aceleracion_tangencial()
    assert acc_tan == (0.5 * 5) * ureg.meter / ureg.second**2  # 2.5 m/s^2


def test_mcuv_aceleracion_centripeta_with_units():
    mcuv = MovimientoCircularUniformementeVariado(
        5 * ureg.meter,
        0 * ureg.radian,
        1 * ureg.radian / ureg.second,
        0.5 * ureg.radian / ureg.second**2,
    )
    acc_cent = mcuv.aceleracion_centripeta(2 * ureg.second)
    assert (
        acc_cent == (2**2 * 5) * ureg.meter / ureg.second**2
    )  # (2 rad/s)^2 * 5 m = 20 m/s^2


def test_mcuv_aceleracion_total_with_units():
    mcuv = MovimientoCircularUniformementeVariado(
        5 * ureg.meter,
        0 * ureg.radian,
        1 * ureg.radian / ureg.second,
        0.5 * ureg.radian / ureg.second**2,
    )
    acc_total = mcuv.aceleracion_total(2 * ureg.second)
    at = mcuv.aceleracion_tangencial().magnitude  # 2.5
    an = mcuv.aceleracion_centripeta(2 * ureg.second).magnitude  # 20
    assert acc_total == math.sqrt(at**2 + an**2) * ureg.meter / ureg.second**2


def test_mcuv_posicion_vector_with_units():
    mcuv = MovimientoCircularUniformementeVariado(
        1 * ureg.meter,
        0 * ureg.radian,
        0 * ureg.radian / ureg.second,
        math.pi / 2 * ureg.radian / ureg.second**2,
    )
    pos_vec = mcuv.posicion(
        1 * ureg.second
    )  # At t=1s, theta = 0.5 * pi/2 * 1^2 = pi/4, x = cos(pi/4), y = sin(pi/4)
    assert np.allclose(
        pos_vec.magnitude, np.array([math.cos(math.pi / 4), math.sin(math.pi / 4)])
    )
    assert pos_vec.units == ureg.meter


def test_mcuv_velocidad_vector_with_units():
    mcuv = MovimientoCircularUniformementeVariado(
        1 * ureg.meter,
        0 * ureg.radian,
        0 * ureg.radian / ureg.second,
        math.pi / 2 * ureg.radian / ureg.second**2,
    )
    vel_vec = mcuv.velocidad(
        1 * ureg.second
    )  # At t=1s, omega = pi/2, theta = pi/4, v_tan = omega * R = pi/2
    # vx = -v_tan * sin(theta) = -pi/2 * sin(pi/4)
    # vy = v_tan * cos(theta) = pi/2 * cos(pi/4)
    expected_vx = -(math.pi / 2) * math.sin(math.pi / 4)
    expected_vy = (math.pi / 2) * math.cos(math.pi / 4)
    assert np.allclose(vel_vec.magnitude, np.array([expected_vx, expected_vy]))
    assert vel_vec.units == ureg.meter / ureg.second


def test_mcuv_aceleracion_vector_with_units():
    mcuv = MovimientoCircularUniformementeVariado(
        1 * ureg.meter,
        0 * ureg.radian,
        0 * ureg.radian / ureg.second,
        math.pi / 2 * ureg.radian / ureg.second**2,
    )
    acc_vec = mcuv.aceleracion(1 * ureg.second)
    # At t=1s, omega = pi/2, alpha = pi/2, theta = pi/4, R = 1
    # at = alpha * R = pi/2 * 1 = pi/2
    # an = omega^2 * R = (pi/2)^2 * 1 = pi^2/4
    # ax = -an * cos(theta) - at * sin(theta) = -pi^2/4 * cos(pi/4) - pi/2 * sin(pi/4)
    # ay = -an * sin(theta) + at * cos(theta) = -pi^2/4 * sin(pi/4) + pi/2 * cos(pi/4)
    expected_ax = -(math.pi**2 / 4) * math.cos(math.pi / 4) - (
        math.pi / 2
    ) * math.sin(math.pi / 4)
    expected_ay = -(math.pi**2 / 4) * math.sin(math.pi / 4) + (
        math.pi / 2
    ) * math.cos(math.pi / 4)
    assert np.allclose(acc_vec.magnitude, np.array([expected_ax, expected_ay]))
    assert acc_vec.units == ureg.meter / ureg.second**2
