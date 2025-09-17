"""
Tests unitarios para el módulo de cuerpos rígidos en dinámica rotacional.
"""

import numpy as np
import pytest
from cinetica.dinamica.rotacional.cuerpos_rigidos import CuerposRigidos
from cinetica.units import ureg, Q_


class TestCuerposRigidos:
    """Test cases for CuerposRigidos class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cuerpo = CuerposRigidos()

    def test_inercia_cilindro_solido(self):
        """Test solid cylinder moment of inertia."""
        masa = Q_(2.0, 'kg')
        radio = Q_(0.5, 'm')
        
        resultado = self.cuerpo.inercia_cilindro_solido(masa, radio)
        
        expected = 0.5 * 2.0 * (0.5 ** 2)  # I = 0.5 * m * r² = 0.5 * 2 * 0.25 = 0.25
        assert resultado.magnitude == expected
        assert resultado.units == ureg('kg * m**2')

    def test_inercia_cilindro_hueco(self):
        """Test hollow cylinder moment of inertia."""
        masa = Q_(2.0, 'kg')
        radio = Q_(0.5, 'm')
        
        resultado = self.cuerpo.inercia_cilindro_hueco(masa, radio)
        
        expected = masa.magnitude * (radio.magnitude ** 2)  # I = m * r² = 2 * 0.25 = 0.5
        assert resultado.magnitude == expected
        assert resultado.units == ureg('kg * m**2')

    def test_inercia_esfera_solido(self):
        """Test solid sphere moment of inertia."""
        masa = Q_(2.0, 'kg')
        radio = Q_(0.5, 'm')
        
        resultado = self.cuerpo.inercia_esfera_solido(masa, radio)
        
        expected = 0.4 * 2.0 * (0.5 ** 2)  # I = 0.4 * m * r² = 0.4 * 2 * 0.25 = 0.2
        assert resultado.magnitude == expected
        assert resultado.units == ureg('kg * m**2')

    def test_inercia_esfera_hueco(self):
        """Test hollow sphere moment of inertia."""
        masa = Q_(2.0, 'kg')
        radio = Q_(0.5, 'm')
        
        resultado = self.cuerpo.inercia_esfera_hueco(masa, radio)
        
        expected = (2.0 / 3.0) * 2.0 * (0.5 ** 2)  # I = (2/3) * m * r² = (2/3) * 2 * 0.25 = 0.333...
        assert abs(resultado.magnitude - expected) < 1e-10
        assert resultado.units == ureg('kg * m**2')

    def test_inercia_varilla_centro(self):
        """Test rod through center moment of inertia."""
        masa = Q_(1.0, 'kg')
        longitud = Q_(2.0, 'm')
        
        resultado = self.cuerpo.inercia_varilla_centro(masa, longitud)
        
        expected = (1.0 / 12.0) * 1.0 * (2.0 ** 2)  # I = (1/12) * m * L² = (1/12) * 1 * 4 = 0.333...
        assert abs(resultado.magnitude - expected) < 1e-10
        assert resultado.units == ureg('kg * m**2')

    def test_inercia_varilla_extremo(self):
        """Test rod through end moment of inertia."""
        masa = Q_(1.0, 'kg')
        longitud = Q_(2.0, 'm')
        
        resultado = self.cuerpo.inercia_varilla_extremo(masa, longitud)
        
        expected = (1.0 / 3.0) * 1.0 * (2.0 ** 2)  # I = (1/3) * m * L² = (1/3) * 1 * 4 = 1.333...
        assert abs(resultado.magnitude - expected) < 1e-10
        assert resultado.units == ureg('kg * m**2')

    def test_inercia_placa_rectangular_centro(self):
        """Test rectangular plate through center moment of inertia."""
        masa = Q_(2.0, 'kg')
        ancho = Q_(0.5, 'm')
        largo = Q_(1.0, 'm')
        
        resultado = self.cuerpo.inercia_placa_rectangular_centro(masa, ancho, largo)
        
        expected = (1.0 / 12.0) * 2.0 * ((0.5 ** 2) + (1.0 ** 2))  # I = (1/12) * m * (w² + l²)
        assert abs(resultado.magnitude - expected) < 1e-10
        assert resultado.units == ureg('kg * m**2')

    def test_inercia_placa_rectangular_eje_ancho(self):
        """Test rectangular plate through width axis moment of inertia."""
        masa = Q_(2.0, 'kg')
        ancho = Q_(0.5, 'm')
        largo = Q_(1.0, 'm')
        
        resultado = self.cuerpo.inercia_placa_rectangular_eje_ancho(masa, ancho, largo)
        
        expected = (1.0 / 12.0) * 2.0 * (largo.magnitude ** 2)  # I = (1/12) * m * l²
        assert abs(resultado.magnitude - expected) < 1e-10
        assert resultado.units == ureg('kg * m**2')

    def test_radio_giro(self):
        """Test radius of gyration calculation."""
        momento_inercia = Q_(2.0, 'kg * m**2')
        masa = Q_(1.0, 'kg')
        
        resultado = self.cuerpo.radio_giro(momento_inercia, masa)
        
        expected = np.sqrt(2.0 / 1.0)  # k = √(I/m) = √2 = 1.414...
        assert abs(resultado.magnitude - expected) < 1e-10
        assert resultado.units == ureg('m')

    def test_momento_inercia_combinado(self):
        """Test combined moment of inertia."""
        momentos = [
            Q_(1.0, 'kg * m**2'),
            Q_(2.0, 'kg * m**2'),
            Q_(3.0, 'kg * m**2')
        ]
        
        resultado = self.cuerpo.momento_inercia_combinado(momentos)
        
        expected = 1.0 + 2.0 + 3.0  # I_total = ΣI_i = 6.0
        assert resultado.magnitude == expected
        assert resultado.units == ureg('kg * m**2')

    def test_inercia_cero_masa(self):
        """Test moment of inertia with zero mass."""
        masa = Q_(0.0, 'kg')
        radio = Q_(0.5, 'm')
        
        resultado = self.cuerpo.inercia_cilindro_solido(masa, radio)
        
        assert resultado.magnitude == 0.0

    def test_inercia_cero_dimension(self):
        """Test moment of inertia with zero dimension."""
        masa = Q_(2.0, 'kg')
        radio = Q_(0.0, 'm')
        
        resultado = self.cuerpo.inercia_cilindro_solido(masa, radio)
        
        assert resultado.magnitude == 0.0

    def test_radio_giro_cero_masa(self):
        """Test radius of gyration with zero mass."""
        momento_inercia = Q_(2.0, 'kg * m**2')
        masa = Q_(0.0, 'kg')
        
        with pytest.raises(ZeroDivisionError):
            self.cuerpo.radio_giro(momento_inercia, masa)

    def test_momento_inercia_combinado_vacio(self):
        """Test combined moment of inertia with empty list."""
        momentos = []
        
        resultado = self.cuerpo.momento_inercia_combinado(momentos)
        
        assert resultado.magnitude == 0.0

    def test_unidades_incompatibles(self):
        """Test with incompatible units."""
        masa = Q_(2.0, 'N')  # Unidades incorrectas
        radio = Q_(0.5, 'm')
        
        with pytest.raises(Exception):
            self.cuerpo.inercia_cilindro_solido(masa, radio)

    def test_inercia_esfera_vs_cilindro(self):
        """Test that sphere has different inertia than cylinder."""
        masa = Q_(2.0, 'kg')
        radio = Q_(0.5, 'm')
        
        inercia_esfera = self.cuerpo.inercia_esfera_solido(masa, radio)
        inercia_cilindro = self.cuerpo.inercia_cilindro_solido(masa, radio)
        
        assert inercia_esfera.magnitude != inercia_cilindro.magnitude
        assert inercia_esfera.magnitude < inercia_cilindro.magnitude  # 0.4 < 0.5