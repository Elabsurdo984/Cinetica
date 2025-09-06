import pytest
from abc import ABC
from cinetica.cinematica.base_movimiento import Movimiento
from cinetica.units import ureg, Q_


class TestMovimientoAbstractClass:
    """Tests for the abstract Movimiento base class."""
    
    def test_cannot_instantiate_abstract_class(self):
        """Test that Movimiento cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            Movimiento()
    
    def test_is_abstract_base_class(self):
        """Test that Movimiento is properly defined as ABC."""
        assert issubclass(Movimiento, ABC)
        assert hasattr(Movimiento, '__abstractmethods__')
        
        # Check that all required methods are abstract
        abstract_methods = Movimiento.__abstractmethods__
        expected_methods = {'posicion', 'velocidad', 'aceleracion'}
        assert abstract_methods == expected_methods


class ConcreteMovimiento(Movimiento):
    """Concrete implementation for testing purposes."""
    
    def __init__(self, pos_value=1.0, vel_value=2.0, accel_value=3.0):
        self.pos_value = pos_value
        self.vel_value = vel_value
        self.accel_value = accel_value
    
    def posicion(self, tiempo):
        return self.pos_value * tiempo
    
    def velocidad(self, tiempo):
        return self.vel_value * tiempo
    
    def aceleracion(self, tiempo=None):
        return self.accel_value


class IncompleteMovimiento(Movimiento):
    """Incomplete implementation missing some abstract methods."""
    
    def posicion(self, tiempo):
        return tiempo
    
    # Missing velocidad and aceleracion methods


class TestMovimientoImplementation:
    """Tests for concrete implementations of Movimiento."""
    
    def test_concrete_implementation_works(self):
        """Test that a complete concrete implementation can be instantiated."""
        mov = ConcreteMovimiento()
        assert isinstance(mov, Movimiento)
        
        # Test that methods work
        assert mov.posicion(5) == 5.0
        assert mov.velocidad(3) == 6.0
        assert mov.aceleracion() == 3.0
    
    def test_incomplete_implementation_fails(self):
        """Test that incomplete implementations cannot be instantiated."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteMovimiento()
    
    def test_method_signatures_are_enforced(self):
        """Test that method signatures match the abstract definitions."""
        mov = ConcreteMovimiento()
        
        # Test posicion method signature
        result = mov.posicion(1.0)
        assert result is not None
        
        # Test velocidad method signature
        result = mov.velocidad(1.0)
        assert result is not None
        
        # Test aceleracion method signature (with optional parameter)
        result = mov.aceleracion()
        assert result is not None
        
        result = mov.aceleracion(1.0)
        assert result is not None


class MovimientoWithUnits(Movimiento):
    """Concrete implementation that uses pint units."""
    
    def posicion(self, tiempo):
        if not isinstance(tiempo, Q_):
            tiempo = Q_(tiempo, ureg.second)
        return 5 * ureg.meter * tiempo
    
    def velocidad(self, tiempo):
        if not isinstance(tiempo, Q_):
            tiempo = Q_(tiempo, ureg.second)
        return 5 * ureg.meter / ureg.second
    
    def aceleracion(self, tiempo=None):
        return 0 * ureg.meter / ureg.second**2


class MovimientoWithArrays(Movimiento):
    """Concrete implementation that returns numpy arrays."""
    
    def posicion(self, tiempo):
        import numpy as np
        return np.array([tiempo, tiempo * 2])
    
    def velocidad(self, tiempo):
        import numpy as np
        return np.array([1, 2])
    
    def aceleracion(self, tiempo=None):
        import numpy as np
        return np.array([0, 0])


class TestMovimientoReturnTypes:
    """Test different return types supported by the interface."""
    
    def test_units_implementation(self):
        """Test implementation that uses pint units."""
        mov = MovimientoWithUnits()
        
        # Test with float input
        pos = mov.posicion(2.0)
        assert isinstance(pos, Q_)
        assert pos.units == ureg.meter * ureg.second
        
        # Test with Quantity input
        pos = mov.posicion(2 * ureg.second)
        assert isinstance(pos, Q_)
        
        vel = mov.velocidad(1.0)
        assert isinstance(vel, Q_)
        assert vel.units == ureg.meter / ureg.second
        
        accel = mov.aceleracion()
        assert isinstance(accel, Q_)
        assert accel.units == ureg.meter / ureg.second**2
    
    def test_array_implementation(self):
        """Test implementation that returns numpy arrays."""
        import numpy as np
        mov = MovimientoWithArrays()
        
        pos = mov.posicion(3.0)
        assert isinstance(pos, np.ndarray)
        assert len(pos) == 2
        assert pos[0] == 3.0
        assert pos[1] == 6.0
        
        vel = mov.velocidad(1.0)
        assert isinstance(vel, np.ndarray)
        assert len(vel) == 2
        
        accel = mov.aceleracion()
        assert isinstance(accel, np.ndarray)
        assert len(accel) == 2


class MovimientoWithValidation(Movimiento):
    """Implementation with input validation."""
    
    def posicion(self, tiempo):
        if tiempo < 0:
            raise ValueError("Tiempo no puede ser negativo")
        return tiempo * 2
    
    def velocidad(self, tiempo):
        if tiempo < 0:
            raise ValueError("Tiempo no puede ser negativo")
        return 2.0
    
    def aceleracion(self, tiempo=None):
        if tiempo is not None and tiempo < 0:
            raise ValueError("Tiempo no puede ser negativo")
        return 0.0


class TestMovimientoValidation:
    """Test validation capabilities in implementations."""
    
    def test_validation_in_implementation(self):
        """Test that implementations can add their own validation."""
        mov = MovimientoWithValidation()
        
        # Valid inputs should work
        assert mov.posicion(1.0) == 2.0
        assert mov.velocidad(1.0) == 2.0
        assert mov.aceleracion(1.0) == 0.0
        assert mov.aceleracion() == 0.0
        
        # Invalid inputs should raise errors
        with pytest.raises(ValueError, match="Tiempo no puede ser negativo"):
            mov.posicion(-1.0)
        
        with pytest.raises(ValueError, match="Tiempo no puede ser negativo"):
            mov.velocidad(-1.0)
        
        with pytest.raises(ValueError, match="Tiempo no puede ser negativo"):
            mov.aceleracion(-1.0)


class TestMovimientoDocumentation:
    """Test that the abstract class has proper documentation."""
    
    def test_class_has_docstring(self):
        """Test that the Movimiento class has documentation."""
        assert Movimiento.__doc__ is not None
        assert len(Movimiento.__doc__.strip()) > 0
        assert "clase base abstracta" in Movimiento.__doc__.lower()
    
    def test_methods_have_docstrings(self):
        """Test that abstract methods have documentation."""
        assert Movimiento.posicion.__doc__ is not None
        assert Movimiento.velocidad.__doc__ is not None
        assert Movimiento.aceleracion.__doc__ is not None
        
        # Check for key documentation elements
        pos_doc = Movimiento.posicion.__doc__
        assert "Parameters" in pos_doc
        assert "Returns" in pos_doc
        assert "tiempo" in pos_doc.lower()
        
        vel_doc = Movimiento.velocidad.__doc__
        assert "Parameters" in vel_doc
        assert "Returns" in vel_doc
        
        accel_doc = Movimiento.aceleracion.__doc__
        assert "Parameters" in accel_doc
        assert "Returns" in accel_doc


class TestMovimientoInheritance:
    """Test inheritance behavior."""
    
    def test_subclass_relationship(self):
        """Test that concrete implementations are proper subclasses."""
        mov = ConcreteMovimiento()
        assert isinstance(mov, Movimiento)
        assert issubclass(ConcreteMovimiento, Movimiento)
    
    def test_method_resolution_order(self):
        """Test that method resolution works correctly."""
        mov = ConcreteMovimiento(pos_value=10, vel_value=20, accel_value=30)
        
        # Methods should resolve to the concrete implementation
        assert mov.posicion(2) == 20  # 10 * 2
        assert mov.velocidad(3) == 60  # 20 * 3
        assert mov.aceleracion() == 30
    
    def test_multiple_inheritance_compatibility(self):
        """Test that the abstract class works with multiple inheritance."""
        
        class Mixin:
            def extra_method(self):
                return "extra"
        
        class MultipleInheritanceMovimiento(Movimiento, Mixin):
            def posicion(self, tiempo):
                return tiempo
            
            def velocidad(self, tiempo):
                return 1.0
            
            def aceleracion(self, tiempo=None):
                return 0.0
        
        mov = MultipleInheritanceMovimiento()
        assert isinstance(mov, Movimiento)
        assert isinstance(mov, Mixin)
        assert mov.extra_method() == "extra"
        assert mov.posicion(5) == 5
