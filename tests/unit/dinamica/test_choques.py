"""
Tests para el módulo de choques y colisiones.

Este módulo contiene pruebas unitarias para las funcionalidades implementadas
en el módulo cinetica.dinamica.choques.
"""

import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_array_almost_equal

from cinetica.dinamica.choques import ChoquesColisiones


class TestChoquesColisiones(unittest.TestCase):
    """Pruebas para la clase ChoquesColisiones."""
    
    def setUp(self):
        """Configuración común para las pruebas."""
        self.choques = ChoquesColisiones()
    
    def test_colision_unidimensional_elastica(self):
        """Prueba colisión unidimensional perfectamente elástica."""
        # Caso de prueba con colisión elástica (e=1.0)
        m1, v1i = 2.0, 3.0  # kg, m/s
        m2, v2i = 5.0, -1.0  # kg, m/s
        e = 1.0
        
        v1f, v2f = self.choques.colision_unidimensional(m1, v1i, m2, v2i, e)
        
        # Verificar conservación del momento lineal
        momento_inicial = m1 * v1i + m2 * v2i
        momento_final = m1 * v1f + m2 * v2f
        self.assertAlmostEqual(momento_final, momento_inicial, places=10)
        
        # Verificar coeficiente de restitución (debe ser 1.0 para colisión elástica)
        e_calculado = self.choques.coeficiente_restitucion(v1i, v2i, v1f, v2f)
        self.assertAlmostEqual(e_calculado, e, places=10)
    
    def test_colision_unidimensional_inelastica(self):
        """Prueba colisión unidimensional perfectamente inelástica."""
        m1, v1i = 2.0, 3.0  # kg, m/s
        m2, v2i = 5.0, -1.0  # kg, m/s
        e = 0.0  # Colisión perfectamente inelástica
        
        v1f, v2f = self.choques.colision_unidimensional(m1, v1i, m2, v2i, e)
        
        # En una colisión perfectamente inelástica, las velocidades finales deben ser iguales
        self.assertAlmostEqual(v1f, v2f, places=10)
        
        # Verificar conservación del momento lineal
        momento_inicial = m1 * v1i + m2 * v2i
        momento_final = m1 * v1f + m2 * v2f
        self.assertAlmostEqual(momento_final, momento_inicial, places=10)
    
    def test_colision_bidimensional_conservacion_momento(self):
        """Prueba que se conserva el momento lineal en colisión 2D."""
        m1, v1i = 2.0, [3.0, 2.0]  # kg, m/s
        m2, v2i = 4.0, [-1.0, 0.0]  # kg, m/s
        angulo = np.pi/4  # 45 grados
        e = 0.8
        
        v1f, v2f = self.choques.colision_bidimensional(m1, v1i, m2, v2i, angulo, e)
        
        # Calcular momentos lineales inicial y final
        p1i = np.array(v1i) * m1
        p2i = np.array(v2i) * m2
        p1f = np.array(v1f) * m1
        p2f = np.array(v2f) * m2
        
        # El momento lineal total debe conservarse en ambas componentes
        assert_array_almost_equal(p1i + p2i, p1f + p2f, decimal=10)
    
    def test_colision_tridimensional_conservacion_momento(self):
        """Prueba que se conserva el momento lineal en colisión 3D."""
        m1, v1i = 2.0, [3.0, 2.0, 1.0]  # kg, m/s
        m2, v2i = 4.0, [-1.0, 0.5, -0.5]  # kg, m/s
        normal = [1.0, 0.0, 0.0]  # Colisión frontal en el eje x
        e = 0.7
        
        v1f, v2f = self.choques.colision_tridimensional(m1, v1i, m2, v2i, normal, e)
        
        # Calcular momentos lineales inicial y final
        p1i = np.array(v1i) * m1
        p2i = np.array(v2i) * m2
        p1f = np.array(v1f) * m1
        p2f = np.array(v2f) * m2
        
        # El momento lineal total debe conservarse en las tres componentes
        assert_array_almost_equal(p1i + p2i, p1f + p2f, decimal=10)
    
    def test_coeficiente_restitucion(self):
        """Prueba el cálculo del coeficiente de restitución."""
        # Caso de prueba con valores conocidos
        v1i, v2i = 4.0, -2.0  # m/s
        v1f, v2f = -1.5, 2.5  # m/s
        
        # Coeficiente de restitución esperado: e = -(v2f - v1f)/(v2i - v1i)
        e_esperado = -(v2f - v1f) / (v2i - v1i)
        e_calculado = self.choques.coeficiente_restitucion(v1i, v2i, v1f, v2f)
        
        self.assertAlmostEqual(e_calculado, e_esperado, places=10)
    
    def test_energia_cinetica_perdida(self):
        """Prueba el cálculo de la energía cinética perdida."""
        m1, v1i = 2.0, 3.0  # kg, m/s
        m2, v2i = 5.0, -1.0  # kg, m/s
        e = 0.5  # Coeficiente de restitución
        
        # Calcular energías cinéticas inicial y final
        K_i = 0.5 * m1 * v1i**2 + 0.5 * m2 * v2i**2
        
        # Obtener velocidades finales
        v1f, v2f = self.choques.colision_unidimensional(m1, v1i, m2, v2i, e)
        K_f = 0.5 * m1 * v1f**2 + 0.5 * m2 * v2f**2
        
        # Calcular energía perdida esperada
        delta_K_esperado = K_i - K_f
        
        # Calcular energía perdida usando el método
        delta_K_calculado = self.choques.energia_cinetica_perdida(
            m1, v1i, m2, v2i, v1f, v2f
        )
        
        self.assertAlmostEqual(delta_K_calculado, delta_K_esperado, places=10)
    
    def test_colision_unidimensional_unidades(self):
        """Prueba el manejo de unidades en colisiones unidimensionales."""
        from pint import UnitRegistry
        ureg = UnitRegistry()
        
        # Definir cantidades con unidades
        m1 = 2.0 * ureg.kg
        v1i = 3.0 * ureg.meter / ureg.second
        m2 = 5.0 * ureg.kg
        v2i = -1.0 * ureg.meter / ureg.second
        e = 0.8
        
        # Realizar la colisión
        v1f, v2f = self.choques.colision_unidimensional(
            m1, v1i, m2, v2i, e, unidades={'masa': 'kg', 'velocidad': 'm/s'}
        )
        
        # Verificar que los resultados tengan las unidades correctas
        self.assertEqual(str(v1f.u), 'meter / second')
        self.assertEqual(str(v2f.u), 'meter / second')
        
        # Verificar que las magnitudes sean razonables
        self.assertTrue(-10 < v1f.magnitude < 10)
        self.assertTrue(-10 < v2f.magnitude < 10)


if __name__ == '__main__':
    unittest.main()
