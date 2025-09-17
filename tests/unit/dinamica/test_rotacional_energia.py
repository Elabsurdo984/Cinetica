"""
Tests unitarios para el módulo de energía rotacional en dinámica rotacional.
"""

import numpy as np
import pytest
from cinetica.dinamica.rotacional.energia_rotacional import EnergiaRotacional
from cinetica.units import ureg, Q_


class TestEnergiaRotacional:
    """Test cases for EnergiaRotacional class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.energia = EnergiaRotacional()

    def test_energia_cinetica_rotacional_basica(self):
        """Test basic rotational kinetic energy calculation."""
        momento_inercia = Q_(2.0, 'kg * m**2')
        velocidad_angular = Q_(3.0, 'rad/s')
        
        resultado = self.energia.energia_cinetica_rotacional(momento_inercia, velocidad_angular)
        
        expected = 0.5 * 2.0 * (3.0 ** 2)  # 0.5 * I * ω² = 0.5 * 2 * 9 = 9
        assert resultado.magnitude == expected
        assert resultado.units == ureg('J')

    def test_energia_cinetica_total(self):
        """Test total kinetic energy (translation + rotation)."""
        masa = Q_(1.0, 'kg')
        velocidad_lineal = Q_(4.0, 'm/s')
        momento_inercia = Q_(0.5, 'kg * m**2')
        velocidad_angular = Q_(2.0, 'rad/s')
        
        resultado = self.energia.energia_cinetica_total(
            masa, velocidad_lineal, momento_inercia, velocidad_angular
        )
        
        # E_total = 0.5*m*v² + 0.5*I*ω² = 0.5*1*16 + 0.5*0.5*4 = 8 + 1 = 9
        assert resultado.magnitude == 9.0
        assert resultado.units == ureg('J')

    def test_energia_potencial_gravitacional(self):
        """Test gravitational potential energy."""
        masa = Q_(2.0, 'kg')
        altura = Q_(10.0, 'm')
        gravedad = Q_(9.81, 'm/s**2')
        
        resultado = self.energia.energia_potencial_gravitacional(masa, altura, gravedad)
        
        expected = 2.0 * 9.81 * 10.0  # m * g * h
        assert resultado.magnitude == expected
        assert resultado.units == ureg('J')

    def test_conservacion_energia_mecanica_verdadero(self):
        """Test mechanical energy conservation when conserved."""
        energia_inicial = Q_(100.0, 'J')
        energia_final = Q_(100.0, 'J')
        
        resultado = self.energia.conservacion_energia_mecanica(energia_inicial, energia_final)
        
        assert resultado is True

    def test_conservacion_energia_mecanica_falso(self):
        """Test mechanical energy conservation when not conserved."""
        energia_inicial = Q_(100.0, 'J')
        energia_final = Q_(90.0, 'J')
        
        resultado = self.energia.conservacion_energia_mecanica(energia_inicial, energia_final)
        
        assert resultado is False

    def test_trabajo_torque(self):
        """Test work done by torque."""
        torque = Q_(5.0, 'N * m')
        angulo_rotacion = Q_(np.pi, 'rad')
        
        resultado = self.energia.trabajo_torque(torque, angulo_rotacion)
        
        expected = 5.0 * np.pi  # W = τ * θ
        assert abs(resultado.magnitude - expected) < 1e-10
        assert resultado.units == ureg('J')

    def test_potencia_rotacional(self):
        """Test rotational power."""
        torque = Q_(10.0, 'N * m')
        velocidad_angular = Q_(2.0, 'rad/s')
        
        resultado = self.energia.potencia_rotacional(torque, velocidad_angular)
        
        expected = 10.0 * 2.0  # P = τ * ω
        assert resultado.magnitude == expected
        assert resultado.units == ureg('W')

    def test_energia_cilindro_rodando(self):
        """Test energy of rolling cylinder."""
        masa = Q_(1.0, 'kg')
        velocidad = Q_(3.0, 'm/s')
        radio = Q_(0.5, 'm')
        
        resultado = self.energia.energia_cilindro_rodando(masa, velocidad, radio)
        
        # E = 0.5*m*v² + 0.25*m*v² = 0.75*m*v² = 0.75*1*9 = 6.75
        expected = 0.75 * 1.0 * (3.0 ** 2)
        assert resultado.magnitude == expected
        assert resultado.units == ureg('J')

    def test_teorema_ejes_paralelos(self):
        """Test parallel axis theorem."""
        momento_inercia_cm = Q_(2.0, 'kg * m**2')
        masa = Q_(1.0, 'kg')
        distancia = Q_(3.0, 'm')
        
        resultado = self.energia.teorema_ejes_paralelos(momento_inercia_cm, masa, distancia)
        
        expected = 2.0 + 1.0 * (3.0 ** 2)  # I = I_cm + m*d² = 2 + 9 = 11
        assert resultado.magnitude == expected
        assert resultado.units == ureg('kg * m**2')

    def test_energia_cinetica_cero_velocidad(self):
        """Test rotational kinetic energy with zero angular velocity."""
        momento_inercia = Q_(2.0, 'kg * m**2')
        velocidad_angular = Q_(0.0, 'rad/s')
        
        resultado = self.energia.energia_cinetica_rotacional(momento_inercia, velocidad_angular)
        
        assert resultado.magnitude == 0.0

    def test_energia_cinetica_cero_inercia(self):
        """Test rotational kinetic energy with zero moment of inertia."""
        momento_inercia = Q_(0.0, 'kg * m**2')
        velocidad_angular = Q_(3.0, 'rad/s')
        
        resultado = self.energia.energia_cinetica_rotacional(momento_inercia, velocidad_angular)
        
        assert resultado.magnitude == 0.0

    def test_trabajo_torque_cero_angulo(self):
        """Test torque work with zero angle."""
        torque = Q_(5.0, 'N * m')
        angulo_rotacion = Q_(0.0, 'rad')
        
        resultado = self.energia.trabajo_torque(torque, angulo_rotacion)
        
        assert resultado.magnitude == 0.0

    def test_potencia_rotacional_cero_torque(self):
        """Test rotational power with zero torque."""
        torque = Q_(0.0, 'N * m')
        velocidad_angular = Q_(2.0, 'rad/s')
        
        resultado = self.energia.potencia_rotacional(torque, velocidad_angular)
        
        assert resultado.magnitude == 0.0

    def test_teorema_ejes_paralelos_cero_distancia(self):
        """Test parallel axis theorem with zero distance."""
        momento_inercia_cm = Q_(2.0, 'kg * m**2')
        masa = Q_(1.0, 'kg')
        distancia = Q_(0.0, 'm')
        
        resultado = self.energia.teorema_ejes_paralelos(momento_inercia_cm, masa, distancia)
        
        assert resultado.magnitude == 2.0  # I = I_cm + 0 = I_cm

    def test_unidades_incompatibles(self):
        """Test with incompatible units."""
        momento_inercia = Q_(2.0, 'kg')  # Unidades incorrectas
        velocidad_angular = Q_(3.0, 'rad/s')
        
        with pytest.raises(Exception):
            self.energia.energia_cinetica_rotacional(momento_inercia, velocidad_angular)