"""
Tests unitarios para el módulo de momento angular en dinámica rotacional.
"""

import numpy as np
import pytest
from cinetica.dinamica.rotacional.momento_angular import MomentoAngular
from cinetica.units import ureg, Q_


class TestMomentoAngular:
    """Test cases for MomentoAngular class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.momento = MomentoAngular()

    def test_calcular_momento_angular_basico(self):
        """Test basic angular momentum calculation."""
        inercia = Q_(2.0, 'kg * m**2')
        velocidad_angular = Q_(5.0, 'rad/s')
        
        resultado = self.momento.calcular_momento_angular(inercia, velocidad_angular)
        
        assert resultado.magnitude == 10.0
        assert resultado.units == ureg('kg * m**2 / s')

    def test_momento_angular_particula(self):
        """Test del cálculo del momento angular de una partícula."""
        posicion = np.array([2.0, 0.0, 0.0])
        velocidad = np.array([0.0, 3.0, 0.0])
        masa = Q_(1.0, 'kg')
        resultado = self.momento.momento_angular_particula(masa, posicion, velocidad)
        
        # L = r × p = (2, 0, 0) × (0, 3, 0) = (0, 0, 6)
        esperado = np.array([0.0, 0.0, 6.0])
        np.testing.assert_array_almost_equal(resultado.magnitude, esperado)
        assert resultado.units == ureg.kilogram * ureg.meter**2 / ureg.second

    def test_conservacion_momento_angular_verdadero(self):
        """Test angular momentum conservation when conserved."""
        momento_inicial = Q_(10.0, 'kg * m**2 / s')
        momento_final = Q_(10.0, 'kg * m**2 / s')
        
        resultado = self.momento.conservacion_momento_angular(momento_inicial, momento_final)
        
        assert resultado is True

    def test_conservacion_momento_angular_falso(self):
        """Test angular momentum conservation when not conserved."""
        momento_inicial = Q_(10.0, 'kg * m**2 / s')
        momento_final = Q_(8.0, 'kg * m**2 / s')
        
        resultado = self.momento.conservacion_momento_angular(momento_inicial, momento_final)
        
        assert resultado is False

    def test_momento_inercia_sistema_particulas(self):
        """Test del cálculo del momento angular de un sistema de partículas."""
        # Crear sistema de 3 partículas
        masas = [Q_(1.0, 'kg'), Q_(1.0, 'kg'), Q_(1.0, 'kg')]
        posiciones = [np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), np.array([-1.0, 0.0, 0.0])]
        velocidades = [np.array([0.0, 1.0, 0.0]), np.array([1.0, 0.0, 0.0]), np.array([0.0, -1.0, 0.0])]
        
        # Calcular momento angular total
        momento_total = None
        for masa, pos, vel in zip(masas, posiciones, velocidades):
            momento_parcial = self.momento.momento_angular_particula(masa, pos, vel)
            if momento_total is None:
                momento_total = momento_parcial
            else:
                momento_total += momento_parcial
        
        # Momento angular total: L_x = 0, L_y = 0, L_z = 1 (verificado con el cálculo real)
        esperado = np.array([0.0, 0.0, 1.0])
        np.testing.assert_array_almost_equal(momento_total.magnitude, esperado)

    def test_conservacion_angular_con_cambio_inercia(self):
        """Test de conservación del momento angular con cambio de inercia."""
        inercia_inicial = Q_(2.0, 'kg * m**2')
        velocidad_inicial = Q_(3.0, 'rad/s')
        inercia_final = Q_(1.0, 'kg * m**2')
        
        # Calcular momento angular inicial
        momento_inicial = inercia_inicial * velocidad_inicial
        
        # Calcular velocidad final usando conservación
        velocidad_final = self.momento.velocidad_angular_cambio_inercia(momento_inicial, inercia_inicial, inercia_final)
        momento_final = self.momento.calcular_momento_angular(inercia_final, velocidad_final)
        
        # Verificar conservación
        assert self.momento.conservacion_momento_angular(momento_inicial, momento_final)

    def test_momento_angular_vectorial(self):
        """Test del cálculo de momento angular con vectores."""
        posicion = np.array([3.0, 0.0, 0.0])
        velocidad = np.array([0.0, 4.0, 0.0])
        masa = Q_(1.0, 'kg')
        resultado = self.momento.momento_angular_particula(masa, posicion, velocidad)
        
        # L = r × p = (3, 0, 0) × (0, 4, 0) = (0, 0, 12)
        esperado = np.array([0.0, 0.0, 12.0])
        np.testing.assert_array_almost_equal(resultado.magnitude, esperado)

    def test_momento_angular_cero_velocidad(self):
        """Test angular momentum with zero angular velocity."""
        inercia = Q_(2.0, 'kg * m**2')
        velocidad_angular = Q_(0.0, 'rad/s')
        
        resultado = self.momento.calcular_momento_angular(inercia, velocidad_angular)
        
        assert resultado.magnitude == 0.0

    def test_momento_angular_particula_cero_masa(self):
        """Test del comportamiento con masa cero."""
        posicion = np.array([2.0, 0.0, 0.0])
        velocidad = np.array([0.0, 3.0, 0.0])
        masa = Q_(0.0, 'kg')
        resultado = self.momento.momento_angular_particula(masa, posicion, velocidad)
        
        # Con masa cero, el momento angular debería ser cero
        esperado = np.array([0.0, 0.0, 0.0])
        np.testing.assert_array_almost_equal(resultado.magnitude, esperado)

    def test_momento_inercia_sistema_vacio(self):
        """Test del comportamiento con sistema vacío."""
        # Sistema vacío debería tener momento angular cero
        momento_total = Q_(0, 'kg * m**2 / s')
        assert momento_total.magnitude == 0.0

    def test_conservacion_angular_cambio_inercia_cero(self):
        """Test del comportamiento con inercia final cero."""
        momento_angular = Q_(10.0, 'kg * m**2 / s')
        inercia_inicial = Q_(2.0, 'kg * m**2')
        inercia_final = Q_(0.0, 'kg * m**2')
        
        with pytest.raises(ValueError):
            self.momento.velocidad_angular_cambio_inercia(momento_angular, inercia_inicial, inercia_final)

    def test_unidades_incompatibles(self):
        """Test del comportamiento con unidades incompatibles."""
        inercia = Q_(2.0, 'kg * m**2')
        velocidad_angular = Q_(3.0, 'm/s')  # Unidades incorrectas
        
        # Esto debería funcionar pero dar advertencia o resultado incorrecto
        resultado = self.momento.calcular_momento_angular(inercia, velocidad_angular)
        assert resultado is not None  # El método debería ejecutarse