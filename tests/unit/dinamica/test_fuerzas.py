"""
Tests unitarios para el módulo de análisis de fuerzas.
"""

import pytest
import math
import numpy as np
from cinetica.dinamica.fuerzas import AnalisisFuerzas
from cinetica.units import ureg, Q_


class TestAnalisisFuerzas:
    """Tests para la clase AnalisisFuerzas."""
    
    def setup_method(self):
        """Configuración para cada test."""
        self.fuerzas = AnalisisFuerzas()
    
    def test_friccion_estatica(self):
        """Test cálculo de fricción estática."""
        f_s = self.fuerzas.friccion_estatica(normal=100, coeficiente=0.3)
        
        assert f_s.magnitude == pytest.approx(30.0)
        assert f_s.dimensionality == ureg.newton.dimensionality
    
    def test_friccion_estatica_con_unidades(self):
        """Test fricción estática con unidades."""
        normal = Q_(200, ureg.newton)
        f_s = self.fuerzas.friccion_estatica(normal=normal, coeficiente=0.4)
        
        assert f_s.magnitude == pytest.approx(80.0)
    
    def test_friccion_estatica_coeficiente_negativo(self):
        """Test error con coeficiente negativo."""
        with pytest.raises(ValueError, match="coeficiente de fricción debe ser no negativo"):
            self.fuerzas.friccion_estatica(normal=100, coeficiente=-0.1)
    
    def test_friccion_cinetica(self):
        """Test cálculo de fricción cinética."""
        f_k = self.fuerzas.friccion_cinetica(normal=150, coeficiente=0.25)
        
        assert f_k.magnitude == pytest.approx(37.5)
        assert f_k.dimensionality == ureg.newton.dimensionality
    
    def test_friccion_cinetica_con_unidades(self):
        """Test fricción cinética con unidades."""
        normal = Q_(120, ureg.newton)
        f_k = self.fuerzas.friccion_cinetica(normal=normal, coeficiente=0.2)
        
        assert f_k.magnitude == pytest.approx(24.0)
    
    def test_fuerza_elastica(self):
        """Test cálculo de fuerza elástica."""
        F_elastica = self.fuerzas.fuerza_elastica(constante=500, deformacion=0.1)
        
        assert F_elastica.magnitude == pytest.approx(50.0)
        assert F_elastica.dimensionality == ureg.newton.dimensionality
    
    def test_fuerza_elastica_con_unidades(self):
        """Test fuerza elástica con unidades."""
        k = Q_(200, ureg.newton / ureg.meter)
        x = Q_(0.05, ureg.meter)
        
        F_elastica = self.fuerzas.fuerza_elastica(constante=k, deformacion=x)
        
        assert F_elastica.magnitude == pytest.approx(10.0)
    
    def test_fuerza_elastica_constante_negativa(self):
        """Test error con constante elástica negativa."""
        with pytest.raises(ValueError, match="constante elástica debe ser positiva"):
            self.fuerzas.fuerza_elastica(constante=-100, deformacion=0.1)
    
    def test_fuerza_gravitacional(self):
        """Test cálculo de fuerza gravitacional."""
        F_grav = self.fuerzas.fuerza_gravitacional(masa1=100, masa2=200, distancia=10)
        
        # F = G * m1 * m2 / r^2
        expected = 6.67430e-11 * 100 * 200 / (10**2)
        assert F_grav.magnitude == pytest.approx(expected)
        assert F_grav.dimensionality == ureg.newton.dimensionality
    
    def test_fuerza_gravitacional_con_unidades(self):
        """Test fuerza gravitacional con unidades."""
        m1 = Q_(50, ureg.kilogram)
        m2 = Q_(75, ureg.kilogram)
        r = Q_(5, ureg.meter)
        
        F_grav = self.fuerzas.fuerza_gravitacional(masa1=m1, masa2=m2, distancia=r)
        
        expected = 6.67430e-11 * 50 * 75 / (5**2)
        assert F_grav.magnitude == pytest.approx(expected)
    
    def test_fuerza_gravitacional_distancia_cero(self):
        """Test error con distancia cero."""
        with pytest.raises(ValueError, match="distancia debe ser positiva"):
            self.fuerzas.fuerza_gravitacional(masa1=100, masa2=200, distancia=0)
    
    def test_fuerza_gravitacional_masa_negativa(self):
        """Test error con masa negativa."""
        with pytest.raises(ValueError, match="masas deben ser positivas"):
            self.fuerzas.fuerza_gravitacional(masa1=-100, masa2=200, distancia=10)
    
    def test_descomponer_fuerza(self):
        """Test descomposición de fuerza en componentes."""
        Fx, Fy = self.fuerzas.descomponer_fuerza(magnitud=100, angulo=math.pi/4)
        
        expected_x = 100 * math.cos(math.pi/4)
        expected_y = 100 * math.sin(math.pi/4)
        
        assert Fx.magnitude == pytest.approx(expected_x)
        assert Fy.magnitude == pytest.approx(expected_y)
    
    def test_descomponer_fuerza_con_unidades(self):
        """Test descomposición con unidades."""
        F = Q_(50, ureg.newton)
        angulo = Q_(math.pi/6, ureg.radian)
        
        Fx, Fy = self.fuerzas.descomponer_fuerza(magnitud=F, angulo=angulo)
        
        expected_x = 50 * math.cos(math.pi/6)
        expected_y = 50 * math.sin(math.pi/6)
        
        assert Fx.magnitude == pytest.approx(expected_x)
        assert Fy.magnitude == pytest.approx(expected_y)
    
    def test_descomponer_fuerza_magnitud_negativa(self):
        """Test error con magnitud negativa."""
        with pytest.raises(ValueError, match="magnitud de la fuerza debe ser no negativa"):
            self.fuerzas.descomponer_fuerza(magnitud=-50, angulo=0)
    
    def test_magnitud_y_direccion(self):
        """Test cálculo de magnitud y dirección desde componentes."""
        mag, ang = self.fuerzas.magnitud_y_direccion(Fx=30, Fy=40)
        
        expected_mag = math.sqrt(30**2 + 40**2)
        expected_ang = math.atan2(40, 30)
        
        assert mag.magnitude == pytest.approx(expected_mag)
        assert ang.magnitude == pytest.approx(expected_ang)
    
    def test_magnitud_y_direccion_con_unidades(self):
        """Test magnitud y dirección con unidades."""
        Fx = Q_(6, ureg.newton)
        Fy = Q_(8, ureg.newton)
        
        mag, ang = self.fuerzas.magnitud_y_direccion(Fx=Fx, Fy=Fy)
        
        expected_mag = math.sqrt(6**2 + 8**2)
        expected_ang = math.atan2(8, 6)
        
        assert mag.magnitude == pytest.approx(expected_mag)
        assert ang.magnitude == pytest.approx(expected_ang)
    
    def test_plano_inclinado(self):
        """Test descomposición en plano inclinado."""
        F_par, F_perp = self.fuerzas.plano_inclinado(peso=100, angulo=math.pi/6)
        
        expected_par = 100 * math.sin(math.pi/6)
        expected_perp = 100 * math.cos(math.pi/6)
        
        assert F_par.magnitude == pytest.approx(expected_par)
        assert F_perp.magnitude == pytest.approx(expected_perp)
    
    def test_plano_inclinado_con_unidades(self):
        """Test plano inclinado con unidades."""
        peso = Q_(200, ureg.newton)
        angulo = Q_(math.pi/3, ureg.radian)
        
        F_par, F_perp = self.fuerzas.plano_inclinado(peso=peso, angulo=angulo)
        
        expected_par = 200 * math.sin(math.pi/3)
        expected_perp = 200 * math.cos(math.pi/3)
        
        assert F_par.magnitude == pytest.approx(expected_par)
        assert F_perp.magnitude == pytest.approx(expected_perp)
    
    def test_plano_inclinado_peso_negativo(self):
        """Test error con peso negativo."""
        with pytest.raises(ValueError, match="peso debe ser positivo"):
            self.fuerzas.plano_inclinado(peso=-100, angulo=math.pi/4)
    
    def test_tension_cuerda_equilibrio(self):
        """Test tensión en equilibrio."""
        T = self.fuerzas.tension_cuerda(masa=10)
        
        expected = 10 * 9.81
        assert T.magnitude == pytest.approx(expected)
        assert T.dimensionality == ureg.newton.dimensionality
    
    def test_tension_cuerda_con_aceleracion(self):
        """Test tensión con aceleración."""
        T = self.fuerzas.tension_cuerda(masa=5, aceleracion=2)
        
        expected = 5 * (9.81 + 2)
        assert T.magnitude == pytest.approx(expected)
    
    def test_tension_cuerda_con_angulo(self):
        """Test tensión con ángulo."""
        T = self.fuerzas.tension_cuerda(masa=10, angulo=math.pi/4)
        
        expected = (10 * 9.81) / math.cos(math.pi/4)
        assert T.magnitude == pytest.approx(expected)
    
    def test_tension_cuerda_con_unidades(self):
        """Test tensión con unidades."""
        masa = Q_(8, ureg.kilogram)
        aceleracion = Q_(1.5, ureg.meter / ureg.second**2)
        gravedad = Q_(9.81, ureg.meter / ureg.second**2)
        
        T = self.fuerzas.tension_cuerda(masa=masa, aceleracion=aceleracion, gravedad=gravedad)
        
        expected = 8 * (9.81 + 1.5)
        assert T.magnitude == pytest.approx(expected)
    
    def test_tension_cuerda_masa_negativa(self):
        """Test error con masa negativa."""
        with pytest.raises(ValueError, match="masa debe ser positiva"):
            self.fuerzas.tension_cuerda(masa=-5)
    
    def test_tension_cuerda_angulo_90_grados(self):
        """Test error con ángulo de 90 grados."""
        with pytest.raises(ValueError, match="ángulo debe ser menor a 90 grados"):
            self.fuerzas.tension_cuerda(masa=10, angulo=math.pi/2)
