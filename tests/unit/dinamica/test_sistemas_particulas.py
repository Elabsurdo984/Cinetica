"""
Tests para el módulo de sistemas de partículas.

Este módulo contiene pruebas unitarias para las funcionalidades implementadas
en el módulo cinetica.dinamica.sistemas_particulas.
"""

import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_array_almost_equal

from cinetica.dinamica.sistemas_particulas import SistemasParticulas


class TestSistemasParticulas(unittest.TestCase):
    """Pruebas para la clase SistemasParticulas."""
    
    def setUp(self):
        """Configuración común para las pruebas."""
        self.sp = SistemasParticulas()
    
    def test_centro_masa_simple(self):
        """Prueba el cálculo del centro de masa para un sistema simple."""
        masas = [1.0, 2.0, 3.0]  # kg
        posiciones = [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [2.0, 0.0, 0.0]
        ]
        
        cm = self.sp.centro_masa(masas, posiciones)
        
        # El centro de masa debería estar más cerca de la partícula con más masa
        expected_cm = np.array([4/3, 0.0, 0.0])  # (0*1 + 1*2 + 2*3) / (1+2+3)
        assert_array_almost_equal(cm, expected_cm, decimal=10)
    
    def test_momento_inercia_particula(self):
        """Prueba el cálculo del momento de inercia para una partícula."""
        masa = 2.0  # kg
        posicion = [3.0, 4.0, 0.0]  # m
        
        # Momento de inercia con respecto al origen
        I = self.sp.momento_inercia_particula(masa, posicion)
        
        # I = m * r² = 2 * (3² + 4² + 0²) = 2 * 25 = 50 kg·m²
        self.assertAlmostEqual(I, 50.0, places=10)
        
        # Momento de inercia con respecto al eje z (eje [0,0,1])
        I_eje = self.sp.momento_inercia_particula(
            masa, posicion, eje=[0, 0, 1]
        )
        # I = m * (x² + y²) = 2 * (3² + 4²) = 50 kg·m²
        self.assertAlmostEqual(I_eje, 50.0, places=10)
    
    def test_momento_inercia_sistema(self):
        """Prueba el cálculo del momento de inercia para un sistema de partículas."""
        masas = [1.0, 1.0, 1.0]  # kg
        posiciones = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ]
        
        I_total = self.sp.momento_inercia_sistema(masas, posiciones)
        
        # Cada partícula está a distancia 1 del origen, I = 3 * (1 * 1²) = 3 kg·m²
        self.assertAlmostEqual(I_total, 3.0, places=10)
    
    def test_teorema_steiner(self):
        """Prueba el teorema de los ejes paralelos (Steiner)."""
        I_cm = 10.0  # kg·m²
        masa_total = 5.0  # kg
        distancia = 2.0  # m
        
        I = self.sp.teorema_steiner(I_cm, masa_total, distancia)
        
        # I = I_cm + M*d² = 10 + 5*4 = 30 kg·m²
        self.assertAlmostEqual(I, 30.0, places=10)
    
    def test_energia_cinetica_rotacional(self):
        """Prueba el cálculo de la energía cinética rotacional."""
        I = 2.0  # kg·m²
        omega = 3.0  # rad/s
        
        K = self.sp.energia_cinetica_rotacional(I, omega)
        
        # K = (1/2) * I * ω² = 0.5 * 2 * 9 = 9 J
        self.assertAlmostEqual(K, 9.0, places=10)
    
    def test_momento_angular(self):
        """Prueba el cálculo del momento angular."""
        I = 4.0  # kg·m²
        omega = 2.0  # rad/s
        
        L = self.sp.momento_angular(I, omega)
        
        # L = I * ω = 4 * 2 = 8 kg·m²/s
        self.assertAlmostEqual(L, 8.0, places=10)
    
    def test_unidades(self):
        """Prueba el manejo de unidades con Pint."""
        from pint import UnitRegistry
        ureg = UnitRegistry()
        
        # Definir cantidades con unidades
        masas = [1.0, 2.0] * ureg.kg
        posiciones = [[0, 0, 0], [1, 0, 0]] * ureg.meter
        
        # Centro de masa
        cm = self.sp.centro_masa(
            masas, posiciones,
            unidades={'masa': 'kg', 'longitud': 'meter'}
        )
        
        # Verificar que el resultado sea consistente
        assert_array_almost_equal(cm, [2/3, 0, 0], decimal=10)
        
        # Momento de inercia con unidades
        I = self.sp.momento_inercia_sistema(
            masas, posiciones,
            unidades={'masa': 'kg', 'longitud': 'meter'}
        )
        
        # Verificar el valor numérico (magnitud) del momento de inercia
        if hasattr(I, 'magnitude'):
            I_value = I.magnitude
        else:
            I_value = I
            
        self.assertAlmostEqual(I_value, 2.0, places=10)


if __name__ == '__main__':
    unittest.main()
