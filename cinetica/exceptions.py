"""
Módulo para excepciones personalizadas de la librería Cinetica.
"""

class CineticaError(Exception):
    """Clase base para todas las excepciones personalizadas de la librería Cinetica."""
    pass

class InvalidPhysicsParameterError(CineticaError):
    """Excepción levantada cuando un parámetro físico tiene un valor inválido (ej. radio <= 0)."""
    pass

class NegativeTimeError(CineticaError):
    """Excepción levantada cuando se proporciona un valor de tiempo negativo."""
    pass

class PhysicallyImpossibleError(CineticaError):
    """Excepción levantada cuando un cálculo resulta en una situación físicamente imposible (ej. velocidad al cuadrado negativa)."""
    pass

class ZeroDivisionError(CineticaError):
    """Excepción levantada cuando se intenta una división por cero en un contexto físico."""
    pass
