"""
Tests unitarios para el módulo de Leyes de Newton.
"""

import pytest
import math
import numpy as np
from cinetica.dinamica.newton import LeyesNewton
from cinetica.units import ureg, Q_


class TestLeyesNewton:
    """Tests para la clase LeyesNewton."""
    
    def setup_method(self):
        """Configuración para cada test."""
        self.newton = LeyesNewton()
    
    def test_segunda_ley_calcular_fuerza(self):
        """Test cálculo de fuerza usando F = ma."""
        fuerza = self.newton.segunda_ley(masa=10, aceleracion=5)
        
        assert fuerza.magnitude == pytest.approx(50.0)
        assert fuerza.dimensionality == ureg.newton.dimensionality
    
    def test_segunda_ley_calcular_masa(self):
        """Test cálculo de masa usando m = F/a."""
        masa = self.newton.segunda_ley(fuerza=100, aceleracion=10)
        
        assert masa.magnitude == pytest.approx(10.0)
        assert masa.dimensionality == ureg.kilogram.dimensionality
    
    def test_segunda_ley_calcular_aceleracion(self):
        """Test cálculo de aceleración usando a = F/m."""
        aceleracion = self.newton.segunda_ley(masa=5, fuerza=25)
        
        assert aceleracion.magnitude == pytest.approx(5.0)
        assert aceleracion.dimensionality == (ureg.meter / ureg.second**2).dimensionality
    
    def test_segunda_ley_con_unidades(self):
        """Test segunda ley con cantidades que ya tienen unidades."""
        masa = Q_(2, ureg.kilogram)
        aceleracion = Q_(3, ureg.meter / ureg.second**2)
        
        fuerza = self.newton.segunda_ley(masa=masa, aceleracion=aceleracion)
        
        assert fuerza.magnitude == pytest.approx(6.0)
        assert fuerza.dimensionality == ureg.newton.dimensionality
    
    def test_segunda_ley_vectorial(self):
        """Test segunda ley con aceleración vectorial."""
        masa = 2
        aceleracion_vec = np.array([3, 4, 0])
        
        fuerza = self.newton.segunda_ley(masa=masa, aceleracion=aceleracion_vec)
        
        expected = np.array([6, 8, 0])
        np.testing.assert_array_almost_equal(fuerza.magnitude, expected)
    
    def test_segunda_ley_parametros_insuficientes(self):
        """Test error cuando no se proporcionan suficientes parámetros."""
        with pytest.raises(ValueError, match="exactamente dos de los tres parámetros"):
            self.newton.segunda_ley(masa=10)
    
    def test_segunda_ley_demasiados_parametros(self):
        """Test error cuando se proporcionan todos los parámetros."""
        with pytest.raises(ValueError, match="exactamente dos de los tres parámetros"):
            self.newton.segunda_ley(masa=10, aceleracion=5, fuerza=50)
    
    def test_segunda_ley_masa_negativa(self):
        """Test error con masa negativa."""
        with pytest.raises(ValueError, match="masa debe ser un valor positivo"):
            self.newton.segunda_ley(masa=-5, aceleracion=10)
    
    def test_fuerza_neta_escalar(self):
        """Test cálculo de fuerza neta con fuerzas escalares."""
        fuerzas = [10, -5, 8, -3]
        
        fuerza_neta = self.newton.fuerza_neta(fuerzas)
        
        assert fuerza_neta.magnitude == pytest.approx(10.0)
        assert fuerza_neta.dimensionality == ureg.newton.dimensionality
    
    def test_fuerza_neta_vectorial(self):
        """Test cálculo de fuerza neta con fuerzas vectoriales."""
        fuerzas = [
            np.array([10, 0]),
            np.array([0, 15]),
            np.array([-5, -3])
        ]
        
        fuerza_neta = self.newton.fuerza_neta(fuerzas)
        
        expected = np.array([5, 12])
        np.testing.assert_array_almost_equal(fuerza_neta.magnitude, expected)
    
    def test_fuerza_neta_con_unidades(self):
        """Test fuerza neta con cantidades que ya tienen unidades."""
        fuerzas = [
            Q_(20, ureg.newton),
            Q_(-8, ureg.newton),
            Q_(3, ureg.newton)
        ]
        
        fuerza_neta = self.newton.fuerza_neta(fuerzas)
        
        assert fuerza_neta.magnitude == pytest.approx(15.0)
    
    def test_fuerza_neta_lista_vacia(self):
        """Test error con lista vacía de fuerzas."""
        with pytest.raises(ValueError, match="al menos una fuerza"):
            self.newton.fuerza_neta([])
    
    def test_equilibrio_verdadero(self):
        """Test sistema en equilibrio."""
        fuerzas = [10, -10, 5, -5]
        
        en_equilibrio = self.newton.equilibrio(fuerzas)
        
        assert en_equilibrio is True
    
    def test_equilibrio_falso(self):
        """Test sistema no en equilibrio."""
        fuerzas = [10, -5, 3]
        
        en_equilibrio = self.newton.equilibrio(fuerzas)
        
        assert en_equilibrio is False
    
    def test_equilibrio_vectorial(self):
        """Test equilibrio con fuerzas vectoriales."""
        fuerzas = [
            np.array([10, 0]),
            np.array([-10, 5]),
            np.array([0, -5])
        ]
        
        en_equilibrio = self.newton.equilibrio(fuerzas)
        
        assert en_equilibrio == True
    
    def test_equilibrio_con_tolerancia(self):
        """Test equilibrio con tolerancia personalizada."""
        fuerzas = [10.001, -10.0]  # Diferencia muy pequeña
        
        en_equilibrio = self.newton.equilibrio(fuerzas, tolerancia=1e-2)
        
        assert en_equilibrio is True
    
    def test_aceleracion_desde_fuerzas(self):
        """Test cálculo de aceleración desde múltiples fuerzas."""
        masa = 5
        fuerzas = [20, -5, 10]
        
        aceleracion = self.newton.aceleracion_desde_fuerzas(masa, fuerzas)
        
        assert aceleracion.magnitude == pytest.approx(5.0)
        assert aceleracion.dimensionality == (ureg.meter / ureg.second**2).dimensionality
    
    def test_peso_tierra(self):
        """Test cálculo del peso en la Tierra."""
        peso = self.newton.peso(masa=10)
        
        assert peso.magnitude == pytest.approx(98.1)
        assert peso.dimensionality == ureg.newton.dimensionality
    
    def test_peso_luna(self):
        """Test cálculo del peso en la Luna."""
        peso = self.newton.peso(masa=10, gravedad=1.62)
        
        assert peso.magnitude == pytest.approx(16.2)
    
    def test_peso_con_unidades(self):
        """Test peso con cantidades que tienen unidades."""
        masa = Q_(5, ureg.kilogram)
        gravedad = Q_(9.81, ureg.meter / ureg.second**2)
        
        peso = self.newton.peso(masa, gravedad)
        
        assert peso.magnitude == pytest.approx(49.05)
    
    def test_fuerza_centripeta(self):
        """Test cálculo de fuerza centrípeta."""
        fuerza_c = self.newton.fuerza_centripeta(masa=2, velocidad=10, radio=5)
        
        assert fuerza_c.magnitude == pytest.approx(40.0)
        assert fuerza_c.dimensionality == ureg.newton.dimensionality
    
    def test_fuerza_centripeta_con_unidades(self):
        """Test fuerza centrípeta con unidades."""
        masa = Q_(1, ureg.kilogram)
        velocidad = Q_(6, ureg.meter / ureg.second)
        radio = Q_(3, ureg.meter)
        
        fuerza_c = self.newton.fuerza_centripeta(masa, velocidad, radio)
        
        assert fuerza_c.magnitude == pytest.approx(12.0)
    
    def test_fuerza_centripeta_radio_cero(self):
        """Test error con radio cero."""
        with pytest.raises(ValueError, match="radio debe ser un valor positivo"):
            self.newton.fuerza_centripeta(masa=1, velocidad=5, radio=0)
    
    def test_fuerza_centripeta_radio_negativo(self):
        """Test error con radio negativo."""
        with pytest.raises(ValueError, match="radio debe ser un valor positivo"):
            self.newton.fuerza_centripeta(masa=1, velocidad=5, radio=-2)
