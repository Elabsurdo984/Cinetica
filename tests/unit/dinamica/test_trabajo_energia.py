"""
Tests unitarios para el módulo de trabajo y energía.
"""

import pytest
import math
import numpy as np
from cinetica.dinamica.trabajo_energia import TrabajoEnergia
from cinetica.units import ureg, Q_


class TestTrabajoEnergia:
    """Tests para la clase TrabajoEnergia."""

    def setup_method(self):
        """Configuración para cada test."""
        self.te = TrabajoEnergia()

    def test_trabajo_fuerza_constante(self):
        """Test cálculo de trabajo con fuerza constante."""
        W = self.te.trabajo_fuerza_constante(fuerza=50, desplazamiento=10)

        assert W.magnitude == pytest.approx(500.0)
        assert W.dimensionality == ureg.joule.dimensionality

    def test_trabajo_fuerza_constante_con_angulo(self):
        """Test trabajo con ángulo entre fuerza y desplazamiento."""
        W = self.te.trabajo_fuerza_constante(fuerza=100, desplazamiento=5, angulo=math.pi/3)

        expected = 100 * 5 * math.cos(math.pi/3)
        assert W.magnitude == pytest.approx(expected)

    def test_trabajo_fuerza_constante_con_unidades(self):
        """Test trabajo con unidades."""
        fuerza = Q_(75, ureg.newton)
        desplazamiento = Q_(8, ureg.meter)
        angulo = Q_(math.pi/4, ureg.radian)

        W = self.te.trabajo_fuerza_constante(fuerza=fuerza, desplazamiento=desplazamiento, angulo=angulo)

        expected = 75 * 8 * math.cos(math.pi/4)
        assert W.magnitude == pytest.approx(expected)

    def test_trabajo_fuerza_constante_fuerza_negativa(self):
        """Test error con fuerza negativa."""
        with pytest.raises(ValueError, match="magnitud de la fuerza debe ser no negativa"):
            self.te.trabajo_fuerza_constante(fuerza=-50, desplazamiento=10)

    def test_trabajo_fuerza_constante_desplazamiento_negativo(self):
        """Test error con desplazamiento negativo."""
        with pytest.raises(ValueError, match="magnitud del desplazamiento debe ser no negativa"):
            self.te.trabajo_fuerza_constante(fuerza=50, desplazamiento=-10)

    def test_trabajo_vectorial(self):
        """Test trabajo usando producto punto vectorial."""
        fuerza = [10, 20, 0]
        desplazamiento = [5, 0, 0]

        W = self.te.trabajo_vectorial(fuerza=fuerza, desplazamiento=desplazamiento)

        expected = 10 * 5 + 20 * 0 + 0 * 0
        assert W.magnitude == pytest.approx(expected)
        assert W.dimensionality == ureg.joule.dimensionality

    def test_trabajo_vectorial_con_unidades(self):
        """Test trabajo vectorial con unidades."""
        fuerza = Q_(np.array([15, 25, 10]), ureg.newton)
        desplazamiento = Q_(np.array([2, 3, 1]), ureg.meter)

        W = self.te.trabajo_vectorial(fuerza=fuerza, desplazamiento=desplazamiento)

        expected = 15*2 + 25*3 + 10*1
        assert W.magnitude == pytest.approx(expected)

    def test_trabajo_vectorial_dimensiones_diferentes(self):
        """Test error con vectores de diferentes dimensiones."""
        fuerza = [10, 20]
        desplazamiento = [5, 0, 0]

        with pytest.raises(ValueError, match="misma dimensión"):
            self.te.trabajo_vectorial(fuerza=fuerza, desplazamiento=desplazamiento)

    def test_energia_cinetica(self):
        """Test cálculo de energía cinética."""
        Ec = self.te.energia_cinetica(masa=10, velocidad=5)

        expected = 0.5 * 10 * 5**2
        assert Ec.magnitude == pytest.approx(expected)
        assert Ec.dimensionality == ureg.joule.dimensionality

    def test_energia_cinetica_con_unidades(self):
        """Test energía cinética con unidades."""
        masa = Q_(8, ureg.kilogram)
        velocidad = Q_(12, ureg.meter / ureg.second)

        Ec = self.te.energia_cinetica(masa=masa, velocidad=velocidad)

        expected = 0.5 * 8 * 12**2
        assert Ec.magnitude == pytest.approx(expected)

    def test_energia_cinetica_masa_negativa(self):
        """Test error con masa negativa."""
        with pytest.raises(ValueError, match="masa debe ser positiva"):
            self.te.energia_cinetica(masa=-5, velocidad=10)

    def test_energia_cinetica_velocidad_negativa(self):
        """Test error con velocidad negativa."""
        with pytest.raises(ValueError, match="velocidad debe ser no negativa"):
            self.te.energia_cinetica(masa=5, velocidad=-10)

    def test_energia_potencial_gravitacional(self):
        """Test cálculo de energía potencial gravitacional."""
        Ep = self.te.energia_potencial_gravitacional(masa=5, altura=10)

        expected = 5 * 9.81 * 10
        assert Ep.magnitude == pytest.approx(expected)
        assert Ep.dimensionality == ureg.joule.dimensionality

    def test_energia_potencial_gravitacional_con_unidades(self):
        """Test energía potencial con unidades."""
        masa = Q_(12, ureg.kilogram)
        altura = Q_(15, ureg.meter)
        gravedad = Q_(9.81, ureg.meter / ureg.second**2)

        Ep = self.te.energia_potencial_gravitacional(masa=masa, altura=altura, gravedad=gravedad)

        expected = 12 * 9.81 * 15
        assert Ep.magnitude == pytest.approx(expected)

    def test_energia_potencial_gravitacional_masa_negativa(self):
        """Test error con masa negativa."""
        with pytest.raises(ValueError, match="masa debe ser positiva"):
            self.te.energia_potencial_gravitacional(masa=-5, altura=10)

    def test_energia_potencial_elastica(self):
        """Test cálculo de energía potencial elástica."""
        Ep_elastica = self.te.energia_potencial_elastica(constante=200, deformacion=0.1)

        expected = 0.5 * 200 * 0.1**2
        assert Ep_elastica.magnitude == pytest.approx(expected)
        assert Ep_elastica.dimensionality == ureg.joule.dimensionality

    def test_energia_potencial_elastica_con_unidades(self):
        """Test energía potencial elástica con unidades."""
        k = Q_(150, ureg.newton / ureg.meter)
        x = Q_(0.08, ureg.meter)

        Ep_elastica = self.te.energia_potencial_elastica(constante=k, deformacion=x)

        expected = 0.5 * 150 * 0.08**2
        assert Ep_elastica.magnitude == pytest.approx(expected)

    def test_energia_potencial_elastica_constante_negativa(self):
        """Test error con constante elástica negativa."""
        with pytest.raises(ValueError, match="constante elástica debe ser no negativa"):
            self.te.energia_potencial_elastica(constante=-100, deformacion=0.1)

    def test_energia_mecanica_total(self):
        """Test cálculo de energía mecánica total."""
        Em = self.te.energia_mecanica_total(energia_cinetica=100, energia_potencial=50)

        assert Em.magnitude == pytest.approx(150.0)
        assert Em.dimensionality == ureg.joule.dimensionality

    def test_energia_mecanica_total_con_unidades(self):
        """Test energía mecánica total con unidades."""
        Ec = Q_(75, ureg.joule)
        Ep = Q_(125, ureg.joule)

        Em = self.te.energia_mecanica_total(energia_cinetica=Ec, energia_potencial=Ep)

        assert Em.magnitude == pytest.approx(200.0)

    def test_teorema_trabajo_energia(self):
        """Test aplicación del teorema trabajo-energía."""
        W_neto = self.te.teorema_trabajo_energia(masa=10, velocidad_inicial=0, velocidad_final=5)

        expected = 0.5 * 10 * (5**2 - 0**2)
        assert W_neto.magnitude == pytest.approx(expected)
        assert W_neto.dimensionality == ureg.joule.dimensionality

    def test_teorema_trabajo_energia_con_unidades(self):
        """Test teorema trabajo-energía con unidades."""
        masa = Q_(8, ureg.kilogram)
        v_inicial = Q_(3, ureg.meter / ureg.second)
        v_final = Q_(7, ureg.meter / ureg.second)

        W_neto = self.te.teorema_trabajo_energia(masa=masa, velocidad_inicial=v_inicial, velocidad_final=v_final)

        expected = 0.5 * 8 * (7**2 - 3**2)
        assert W_neto.magnitude == pytest.approx(expected)

    def test_teorema_trabajo_energia_masa_negativa(self):
        """Test error con masa negativa."""
        with pytest.raises(ValueError, match="masa debe ser positiva"):
            self.te.teorema_trabajo_energia(masa=-5, velocidad_inicial=0, velocidad_final=10)

    def test_potencia(self):
        """Test cálculo de potencia."""
        P = self.te.potencia(trabajo=1000, tiempo=10)

        assert P.magnitude == pytest.approx(100.0)
        assert P.dimensionality == ureg.watt.dimensionality

    def test_potencia_con_unidades(self):
        """Test potencia con unidades."""
        trabajo = Q_(2500, ureg.joule)
        tiempo = Q_(25, ureg.second)

        P = self.te.potencia(trabajo=trabajo, tiempo=tiempo)

        assert P.magnitude == pytest.approx(100.0)

    def test_potencia_tiempo_cero(self):
        """Test error con tiempo cero."""
        with pytest.raises(ValueError, match="tiempo debe ser positivo"):
            self.te.potencia(trabajo=1000, tiempo=0)

    def test_potencia_tiempo_negativo(self):
        """Test error con tiempo negativo."""
        with pytest.raises(ValueError, match="tiempo debe ser positivo"):
            self.te.potencia(trabajo=1000, tiempo=-5)

    def test_potencia_instantanea(self):
        """Test cálculo de potencia instantánea."""
        P_inst = self.te.potencia_instantanea(fuerza=50, velocidad=10)

        assert P_inst.magnitude == pytest.approx(500.0)
        assert P_inst.dimensionality == ureg.watt.dimensionality

    def test_potencia_instantanea_con_unidades(self):
        """Test potencia instantánea con unidades."""
        fuerza = Q_(25, ureg.newton)
        velocidad = Q_(8, ureg.meter / ureg.second)

        P_inst = self.te.potencia_instantanea(fuerza=fuerza, velocidad=velocidad)

        assert P_inst.magnitude == pytest.approx(200.0)
