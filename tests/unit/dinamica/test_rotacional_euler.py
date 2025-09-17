"""
Tests unitarios para el módulo de ecuaciones de Euler en dinámica rotacional.
"""

import numpy as np
import pytest
from cinetica.dinamica.rotacional.ecuaciones_euler import EcuacionesEuler
from cinetica.units import ureg, Q_


class TestEcuacionesEuler:
    """Test cases for EcuacionesEuler class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.euler = EcuacionesEuler()

    def test_set_tensor_inercia(self):
        """Test setting inertia tensor."""
        ixx = Q_(1.0, 'kg * m**2')
        iyy = Q_(2.0, 'kg * m**2')
        izz = Q_(3.0, 'kg * m**2')
        
        self.euler.set_tensor_inercia(ixx, iyy, izz)
        
        tensor = self.euler.tensor_inercia
        assert tensor[0, 0] == 1.0
        assert tensor[1, 1] == 2.0
        assert tensor[2, 2] == 3.0
        assert tensor[0, 1] == 0.0  # Off-diagonal should be zero
        assert tensor[0, 2] == 0.0
        assert tensor[1, 2] == 0.0

    def test_resolver_ecuaciones_euler_estacionario(self):
        """Test solving Euler equations for steady rotation."""
        ixx = Q_(1.0, 'kg * m**2')
        iyy = Q_(2.0, 'kg * m**2')
        izz = Q_(3.0, 'kg * m**2')
        self.euler.set_tensor_inercia(ixx, iyy, izz)
        
        velocidades_angulares = [Q_(1.0, 'rad/s'), Q_(0.0, 'rad/s'), Q_(0.0, 'rad/s')]
        
        resultado = self.euler.resolver_ecuaciones_euler(velocidades_angulares)
        
        # For steady rotation about x-axis, torque should be zero
        assert len(resultado) == 3
        assert abs(resultado[0].magnitude) < 1e-10  # τ_x ≈ 0
        assert abs(resultado[1].magnitude) < 1e-10  # τ_y ≈ 0
        assert abs(resultado[2].magnitude) < 1e-10  # τ_z ≈ 0

    def test_estabilidad_rotacion_eje_intermedio(self):
        """Test rotation stability for intermediate axis."""
        ixx = Q_(1.0, 'kg * m**2')
        iyy = Q_(2.0, 'kg * m**2')
        izz = Q_(3.0, 'kg * m**2')
        self.euler.set_tensor_inercia(ixx, iyy, izz)
        
        resultado = self.euler.estabilidad_rotacion('y')
        
        assert resultado is False  # Intermediate axis is unstable

    def test_estabilidad_rotacion_eje_mayor(self):
        """Test rotation stability for major axis."""
        ixx = Q_(1.0, 'kg * m**2')
        iyy = Q_(2.0, 'kg * m**2')
        izz = Q_(3.0, 'kg * m**2')
        self.euler.set_tensor_inercia(ixx, iyy, izz)
        
        resultado = self.euler.estabilidad_rotacion('z')
        
        assert resultado is True  # Major axis is stable

    def test_estabilidad_rotacion_eje_menor(self):
        """Test rotation stability for minor axis."""
        ixx = Q_(1.0, 'kg * m**2')
        iyy = Q_(2.0, 'kg * m**2')
        izz = Q_(3.0, 'kg * m**2')
        self.euler.set_tensor_inercia(ixx, iyy, izz)
        
        resultado = self.euler.estabilidad_rotacion('x')
        
        assert resultado is True  # Minor axis is stable

    def test_precesion_giroscopio(self):
        """Test gyroscope precession."""
        velocidad_spin = Q_(100.0, 'rad/s')
        torque_externo = Q_(5.0, 'N * m')
        momento_inercia = Q_(0.1, 'kg * m**2')
        
        resultado = self.euler.precesion_giroscopio(velocidad_spin, torque_externo, momento_inercia)
        
        expected = torque_externo.magnitude / (momento_inercia.magnitude * velocidad_spin.magnitude)
        assert abs(resultado.magnitude - expected) < 1e-10
        assert resultado.units == ureg('rad/s')

    def test_energia_cinetica_rotacional_euler(self):
        """Test rotational kinetic energy using Euler approach."""
        ixx = Q_(1.0, 'kg * m**2')
        iyy = Q_(2.0, 'kg * m**2')
        izz = Q_(3.0, 'kg * m**2')
        self.euler.set_tensor_inercia(ixx, iyy, izz)
        
        velocidades_angulares = [Q_(2.0, 'rad/s'), Q_(1.0, 'rad/s'), Q_(0.5, 'rad/s')]
        
        resultado = self.euler.energia_cinetica_rotacional(velocidades_angulares)
        
        # E = 0.5 * (I_xx*ω_x² + I_yy*ω_y² + I_zz*ω_z²)
        expected = 0.5 * (1.0 * 4.0 + 2.0 * 1.0 + 3.0 * 0.25)  # 0.5 * (4 + 2 + 0.75) = 3.375
        assert abs(resultado.magnitude - expected) < 1e-10
        assert resultado.units == ureg('J')

    def test_torque_cambio_momento_euler(self):
        """Test torque from change in angular momentum."""
        velocidades_angulares_inicial = [Q_(1.0, 'rad/s'), Q_(0.0, 'rad/s'), Q_(0.0, 'rad/s')]
        velocidades_angulares_final = [Q_(2.0, 'rad/s'), Q_(0.0, 'rad/s'), Q_(0.0, 'rad/s')]
        tiempo = Q_(1.0, 's')
        
        resultado = self.euler.torque_cambio_momento(
            velocidades_angulares_inicial, velocidades_angulares_final, tiempo
        )
        
        # τ = ΔL/Δt = I * Δω/Δt
        assert len(resultado) == 3
        assert resultado[0].magnitude == 1.0  # I_xx * Δω_x / Δt = 1 * 1 / 1 = 1
        assert resultado[1].magnitude == 0.0
        assert resultado[2].magnitude == 0.0

    def test_tensor_inercia_no_establecido(self):
        """Test operations without setting inertia tensor."""
        velocidades_angulares = [Q_(1.0, 'rad/s'), Q_(0.0, 'rad/s'), Q_(0.0, 'rad/s')]
        
        with pytest.raises(ValueError):
            self.euler.resolver_ecuaciones_euler(velocidades_angulares)

    def test_estabilidad_eje_invalido(self):
        """Test stability with invalid axis."""
        ixx = Q_(1.0, 'kg * m**2')
        iyy = Q_(2.0, 'kg * m**2')
        izz = Q_(3.0, 'kg * m**2')
        self.euler.set_tensor_inercia(ixx, iyy, izz)
        
        with pytest.raises(ValueError):
            self.euler.estabilidad_rotacion('a')

    def test_precesion_cero_spin(self):
        """Test precession with zero spin velocity."""
        velocidad_spin = Q_(0.0, 'rad/s')
        torque_externo = Q_(5.0, 'N * m')
        momento_inercia = Q_(0.1, 'kg * m**2')
        
        with pytest.raises(ZeroDivisionError):
            self.euler.precesion_giroscopio(velocidad_spin, torque_externo, momento_inercia)

    def test_energia_cinetica_cero_velocidades(self):
        """Test kinetic energy with zero angular velocities."""
        ixx = Q_(1.0, 'kg * m**2')
        iyy = Q_(2.0, 'kg * m**2')
        izz = Q_(3.0, 'kg * m**2')
        self.euler.set_tensor_inercia(ixx, iyy, izz)
        
        velocidades_angulares = [Q_(0.0, 'rad/s'), Q_(0.0, 'rad/s'), Q_(0.0, 'rad/s')]
        
        resultado = self.euler.energia_cinetica_rotacional(velocidades_angulares)
        
        assert resultado.magnitude == 0.0

    def test_tensor_inercia_simetrico(self):
        """Test that inertia tensor is symmetric."""
        ixx = Q_(1.0, 'kg * m**2')
        iyy = Q_(2.0, 'kg * m**2')
        izz = Q_(3.0, 'kg * m**2')
        self.euler.set_tensor_inercia(ixx, iyy, izz)
        
        tensor = self.euler.tensor_inercia
        
        # Check symmetry
        assert tensor[0, 1] == tensor[1, 0]
        assert tensor[0, 2] == tensor[2, 0]
        assert tensor[1, 2] == tensor[2, 1]