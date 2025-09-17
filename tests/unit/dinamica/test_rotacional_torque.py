"""
Tests unitarios para el módulo de torque en dinámica rotacional.
"""

import numpy as np
import pytest
from cinetica.dinamica.rotacional.torque import Torque
from cinetica.units import ureg, Q_


class TestTorque:
    """Test cases for Torque class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.torque = Torque()

    def test_calcular_torque_basico(self):
        """Test basic torque calculation."""
        fuerza = Q_(10.0, 'N')
        posicion = np.array([2.0, 0.0, 0.0])
        
        resultado = self.torque.calcular_torque(fuerza, posicion)
        
        expected = np.array([0.0, 0.0, 20.0])
        np.testing.assert_array_equal(resultado.magnitude, expected)
        assert resultado.units == ureg('N * m')

    def test_torque_magnitud(self):
        """Test torque magnitude calculation."""
        fuerza = Q_(10.0, 'N')
        brazo = Q_(2.0, 'm')
        
        resultado = self.torque.torque_magnitud(fuerza, brazo)
        
        assert resultado.magnitude == 20.0
        assert resultado.units == ureg('N * m')

    def test_segunda_ley_newton_rotacional(self):
        """Test rotational Newton's second law."""
        momento_inercia = Q_(3.0, 'kg * m**2')
        aceleracion_angular = Q_(4.0, 'rad/s**2')
        
        resultado = self.torque.segunda_ley_newton_rotacional(
            momento_inercia, aceleracion_angular
        )
        
        assert resultado.magnitude == 12.0
        assert resultado.units == ureg('N * m')

    def test_cambio_momento_angular(self):
        """Test change in angular momentum."""
        momento_inicial = Q_(10.0, 'kg * m**2 / s')
        momento_final = Q_(18.0, 'kg * m**2 / s')
        tiempo = Q_(2.0, 's')
        
        resultado = self.torque.cambio_momento_angular(
            momento_inicial, momento_final, tiempo
        )
        
        assert resultado.magnitude == 4.0  # (18-10)/2 = 4
        assert resultado.units == ureg('N * m')

    def test_torque_3d(self):
        """Test 3D torque calculation."""
        fuerza = np.array([1.0, 2.0, 3.0])
        posicion = np.array([4.0, 5.0, 6.0])
        
        resultado = self.torque.calcular_torque_vectorial(fuerza, posicion)
        
        # τ = r × F
        expected = np.cross(posicion, fuerza)
        np.testing.assert_array_equal(resultado, expected)

    def test_torque_fuerza_paralela_posicion(self):
        """Test torque when force is parallel to position vector."""
        fuerza = Q_(10.0, 'N')
        posicion = np.array([2.0, 0.0, 0.0])
        
        resultado = self.torque.calcular_torque(fuerza, posicion)
        
        # Torque should be zero when force is parallel to position
        np.testing.assert_array_equal(resultado.magnitude, np.array([0.0, 0.0, 0.0]))

    def test_torque_cero_fuerza(self):
        """Test torque with zero force."""
        fuerza = Q_([0.0, 0.0, 0.0], 'N')
        posicion = np.array([2.0, 0.0, 0.0])
        
        resultado = self.torque.calcular_torque(fuerza, posicion)
        
        assert np.all(resultado.magnitude == 0.0)

    def test_torque_cero_brazo(self):
        """Test torque with zero lever arm."""
        fuerza = Q_(10.0, 'N')
        brazo = Q_(0.0, 'm')
        
        resultado = self.torque.torque_magnitud(fuerza, brazo)
        
        assert resultado.magnitude == 0.0

    def test_segunda_ley_cero_inercia(self):
        """Test rotational Newton's law with zero inertia."""
        momento_inercia = Q_(0.0, 'kg * m**2')
        aceleracion_angular = Q_(4.0, 'rad/s**2')
        
        resultado = self.torque.segunda_ley_newton_rotacional(
            momento_inercia, aceleracion_angular
        )
        
        assert resultado.magnitude == 0.0

    def test_cambio_momento_cero_tiempo(self):
        """Test momentum change with zero time."""
        momento_inicial = Q_(10.0, 'kg * m**2 / s')
        momento_final = Q_(18.0, 'kg * m**2 / s')
        tiempo = Q_(0.0, 's')
        
        with pytest.raises(ZeroDivisionError):
            self.torque.cambio_momento_angular(
                momento_inicial, momento_final, tiempo
            )

    def test_unidades_incompatibles(self):
        """Test with incompatible units."""
        fuerza = Q_(10.0, 'kg')  # Unidades incorrectas
        brazo = Q_(2.0, 'm')
        
        with pytest.raises(Exception):
            self.torque.torque_magnitud(fuerza, brazo)

    def test_torque_vectorial_cero_posicion(self):
        """Test vector torque with zero position."""
        fuerza = np.array([1.0, 2.0, 3.0])
        posicion = np.array([0.0, 0.0, 0.0])
        
        resultado = self.torque.calcular_torque_vectorial(fuerza, posicion)
        
        expected = np.array([0.0, 0.0, 0.0])
        np.testing.assert_array_equal(resultado, expected)