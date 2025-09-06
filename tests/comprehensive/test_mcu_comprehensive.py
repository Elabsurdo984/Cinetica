import pytest
import numpy as np
import math
from cinetica.cinematica.circular import MovimientoCircularUniforme
from cinetica.units import ureg, Q_


class TestMCUVectorMethods:
    """Comprehensive tests for MCU vector methods."""

    def test_posicion_vector_basic(self):
        """Test basic position vector calculation."""
        mcu = MovimientoCircularUniforme(
            radio=2 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=math.pi / 2 * ureg.radian / ureg.second
        )

        # At t=1s, theta = pi/2, so x=0, y=2
        pos_vec = mcu.posicion_vector(1 * ureg.second)

        assert isinstance(pos_vec, np.ndarray)
        assert len(pos_vec) == 2
        assert abs(pos_vec[0] - 0.0) < 1e-10  # x = r*cos(pi/2) = 0
        assert abs(pos_vec[1] - 2.0) < 1e-10  # y = r*sin(pi/2) = 2

    def test_posicion_vector_different_angles(self):
        """Test position vector at different angles."""
        mcu = MovimientoCircularUniforme(
            radio=1 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=1 * ureg.radian / ureg.second
        )

        # Test at t=0 (theta=0)
        pos_0 = mcu.posicion_vector(0 * ureg.second)
        assert abs(pos_0[0] - 1.0) < 1e-10  # x = cos(0) = 1
        assert abs(pos_0[1] - 0.0) < 1e-10  # y = sin(0) = 0

        # Test at t=pi/2 (theta=pi/2)
        pos_pi2 = mcu.posicion_vector(math.pi / 2 * ureg.second)
        assert abs(pos_pi2[0] - 0.0) < 1e-10  # x = cos(pi/2) = 0
        assert abs(pos_pi2[1] - 1.0) < 1e-10  # y = sin(pi/2) = 1

    def test_posicion_vector_tiempo_negativo(self):
        """Test position vector with negative time."""
        mcu = MovimientoCircularUniforme(
            radio=1 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=1 * ureg.radian / ureg.second
        )

        with pytest.raises(ValueError, match="El tiempo no puede ser negativo"):
            mcu.posicion_vector(-1 * ureg.second)

    def test_velocidad_vector_basic(self):
        """Test basic velocity vector calculation."""
        mcu = MovimientoCircularUniforme(
            radio=1 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=2 * ureg.radian / ureg.second
        )

        # At t=0, theta=0, vx = -omega*r*sin(0) = 0, vy = omega*r*cos(0) = 2
        vel_vec = mcu.velocidad(0 * ureg.second)

        assert isinstance(vel_vec, np.ndarray)
        assert len(vel_vec) == 2
        assert abs(vel_vec[0] - 0.0) < 1e-10
        assert abs(vel_vec[1] - 2.0) < 1e-10

    def test_velocidad_vector_tiempo_negativo(self):
        """Test velocity vector with negative time."""
        mcu = MovimientoCircularUniforme(
            radio=1 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=1 * ureg.radian / ureg.second
        )

        with pytest.raises(ValueError, match="El tiempo no puede ser negativo"):
            mcu.velocidad(-1 * ureg.second)


class TestMCUHelperMethods:
    """Test MCU helper and convenience methods."""

    def test_velocidad_angular_constante(self):
        """Test velocity angular constant method."""
        omega = 3 * ureg.radian / ureg.second
        mcu = MovimientoCircularUniforme(
            radio=2 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=omega
        )

        result = mcu.velocidad_angular_constante()
        assert result == omega
        assert result.units == ureg.radian / ureg.second

    def test_aceleracion_centripeta_constante(self):
        """Test centripetal acceleration constant method."""
        radio = 2 * ureg.meter
        omega = 3 * ureg.radian / ureg.second
        mcu = MovimientoCircularUniforme(
            radio=radio,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=omega
        )

        result = mcu.aceleracion_centripeta_constante()
        expected = omega**2 * radio  # ω²r
        assert abs(result.magnitude - expected.magnitude) < 1e-10
        assert result.units.dimensionality == (ureg.meter / ureg.second**2).dimensionality

    def test_periodo(self):
        """Test period calculation."""
        omega = 2 * math.pi * ureg.radian / ureg.second  # 1 Hz
        mcu = MovimientoCircularUniforme(
            radio=1 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=omega
        )

        periodo = mcu.periodo()
        expected = 2 * math.pi / omega  # T = 2π/ω
        assert abs(periodo.magnitude - expected.magnitude) < 1e-10
        assert periodo.units == ureg.second

    def test_periodo_omega_cero(self):
        """Test period calculation with zero angular velocity."""
        mcu = MovimientoCircularUniforme(
            radio=1 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=0 * ureg.radian / ureg.second
        )

        # MCU with zero angular velocity should return infinite period
        periodo = mcu.periodo()
        assert periodo.magnitude == float('inf')

    def test_frecuencia(self):
        """Test frequency calculation."""
        omega = 4 * math.pi * ureg.radian / ureg.second  # 2 Hz
        mcu = MovimientoCircularUniforme(
            radio=1 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=omega
        )

        frecuencia = mcu.frecuencia()
        expected = omega / (2 * math.pi)  # f = ω/(2π)
        assert abs(frecuencia.magnitude - expected.magnitude) < 1e-10
        assert frecuencia.units.dimensionality == ureg.hertz.dimensionality

    def test_frecuencia_omega_cero(self):
        """Test frequency calculation with zero angular velocity."""
        mcu = MovimientoCircularUniforme(
            radio=1 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=0 * ureg.radian / ureg.second
        )

        frecuencia = mcu.frecuencia()
        assert frecuencia.magnitude == 0
        assert frecuencia.units == ureg.hertz


class TestMCUEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_radio_muy_pequeno(self):
        """Test with very small radius."""
        mcu = MovimientoCircularUniforme(
            radio=1e-10 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=1 * ureg.radian / ureg.second
        )

        # Should still work, just with very small values
        pos = mcu.posicion_angular(1 * ureg.second)
        assert pos.magnitude == 1.0  # θ = ωt = 1*1 = 1 radian

        vel_mag = mcu.velocidad_tangencial()
        assert vel_mag.magnitude < 1e-9

    def test_velocidad_angular_muy_alta(self):
        """Test with very high angular velocity."""
        mcu = MovimientoCircularUniforme(
            radio=1 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=1000 * ureg.radian / ureg.second
        )

        # Should handle high velocities
        vel_mag = mcu.velocidad_tangencial()
        assert vel_mag.magnitude == 1000

        accel = mcu.aceleracion_centripeta()
        assert accel.magnitude == 1000000  # ω²r = 1000² * 1

    def test_angulo_inicial_no_cero(self):
        """Test with non-zero initial angle."""
        mcu = MovimientoCircularUniforme(
            radio=1 * ureg.meter,
            posicion_angular_inicial=math.pi / 4 * ureg.radian,
            velocidad_angular_inicial=1 * ureg.radian / ureg.second
        )

        # At t=0, should be at initial angle
        pos_0 = mcu.posicion_angular(0 * ureg.second)
        assert abs(pos_0.magnitude - math.pi / 4) < 1e-10

        # At t=pi/4, should be at pi/2
        pos_pi4 = mcu.posicion_angular(math.pi / 4 * ureg.second)
        assert abs(pos_pi4.magnitude - math.pi / 2) < 1e-10

    def test_multiples_revoluciones(self):
        """Test behavior over multiple revolutions."""
        mcu = MovimientoCircularUniforme(
            radio=1 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=1 * ureg.radian / ureg.second
        )

        # After 2π seconds, should complete one revolution
        pos_2pi = mcu.posicion_angular(2 * math.pi * ureg.second)
        assert abs(pos_2pi.magnitude - 2 * math.pi) < 1e-10

        # After 4π seconds, should complete two revolutions
        pos_4pi = mcu.posicion_angular(4 * math.pi * ureg.second)
        assert abs(pos_4pi.magnitude - 4 * math.pi) < 1e-10


class TestMCUUnitsHandling:
    """Test proper units handling in MCU."""

    def test_init_with_different_units(self):
        """Test initialization with different but compatible units."""
        mcu = MovimientoCircularUniforme(
            radio=200 * ureg.centimeter,  # cm
            posicion_angular_inicial=90 * ureg.degree,  # degrees
            velocidad_angular_inicial=60 * ureg.degree / ureg.second  # deg/s
        )

        # Check that units are preserved (MCU doesn't auto-convert)
        assert mcu.radio.units == ureg.centimeter
        assert abs(mcu.radio.magnitude - 200.0) < 1e-10

        assert mcu.posicion_angular_inicial.units == ureg.degree
        assert abs(mcu.posicion_angular_inicial.magnitude - 90.0) < 1e-10

        assert mcu.velocidad_angular_inicial.units == ureg.degree / ureg.second
        assert abs(mcu.velocidad_angular_inicial.magnitude - 60.0) < 1e-10

    def test_calculations_with_different_time_units(self):
        """Test calculations with different time units."""
        mcu = MovimientoCircularUniforme(
            radio=1 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=1 * ureg.radian / ureg.second
        )

        # Test with minutes
        pos_min = mcu.posicion_angular(1 * ureg.minute)  # 60 seconds
        pos_sec = mcu.posicion_angular(60 * ureg.second)

        assert abs(pos_min.magnitude - pos_sec.magnitude) < 1e-10

        # Test with milliseconds
        pos_ms = mcu.posicion_angular(1000 * ureg.millisecond)  # 1 second
        pos_1s = mcu.posicion_angular(1 * ureg.second)

        assert abs(pos_ms.magnitude - pos_1s.magnitude) < 1e-10


class TestMCUPhysicsConsistency:
    """Test physics consistency and relationships."""

    def test_velocidad_tangencial_relationship(self):
        """Test relationship between angular and tangential velocity."""
        radio = 2 * ureg.meter
        omega = 3 * ureg.radian / ureg.second
        mcu = MovimientoCircularUniforme(
            radio=radio,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=omega
        )

        v_tan = mcu.velocidad_tangencial()
        expected = omega * radio  # v = ωr
        assert abs(v_tan.magnitude - expected.magnitude) < 1e-10

    def test_aceleracion_centripeta_relationships(self):
        """Test different forms of centripetal acceleration."""
        radio = 2 * ureg.meter
        omega = 3 * ureg.radian / ureg.second
        mcu = MovimientoCircularUniforme(
            radio=radio,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=omega
        )

        # ac = ω²r
        ac1 = mcu.aceleracion_centripeta()
        expected1 = omega**2 * radio
        assert abs(ac1.magnitude - expected1.magnitude) < 1e-10

        # ac = v²/r where v = ωr
        v_tan = mcu.velocidad_tangencial()
        expected2 = v_tan**2 / radio
        assert abs(ac1.magnitude - expected2.magnitude) < 1e-10

    def test_periodo_frecuencia_relationship(self):
        """Test relationship between period and frequency."""
        mcu = MovimientoCircularUniforme(
            radio=1 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=2 * math.pi * ureg.radian / ureg.second
        )

        periodo = mcu.periodo()
        frecuencia = mcu.frecuencia()

        # T * f = 1
        product = periodo * frecuencia
        assert abs(product.magnitude - 1.0) < 1e-10
        assert product.dimensionless

    def test_position_continuity(self):
        """Test that position is continuous over time."""
        mcu = MovimientoCircularUniforme(
            radio=1 * ureg.meter,
            posicion_angular_inicial=0 * ureg.radian,
            velocidad_angular_inicial=1 * ureg.radian / ureg.second
        )

        # Test continuity at several points
        times = [0, 0.1, 0.5, 1.0, 2.0, 5.0]
        positions = []

        for t in times:
            pos = mcu.posicion_angular(t * ureg.second)
            positions.append(pos.magnitude)

        # Check that positions increase monotonically (for positive ω)
        for i in range(1, len(positions)):
            assert positions[i] > positions[i-1]

        # Check that the rate of change is constant (ω)
        for i in range(1, len(positions)):
            dt = times[i] - times[i-1]
            dpos = positions[i] - positions[i-1]
            rate = dpos / dt
            assert abs(rate - 1.0) < 1e-10  # Should equal ω = 1 rad/s
