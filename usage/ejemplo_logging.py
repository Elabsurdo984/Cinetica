"""
Ejemplo de uso del sistema de logging de Cinetica.

Este ejemplo muestra cómo configurar y utilizar el sistema de logging
en diferentes niveles de la aplicación.
"""

import numpy as np
from cinetica import setup_logger, get_logger

# Configurar el logger raíz
logger = setup_logger('cinetica', level='DEBUG')

# También puedes obtener loggers específicos para módulos
module_logger = get_logger('cinetica.ejemplo')

class CalculadoraFisica:
    """Clase de ejemplo que utiliza logging para rastrear operaciones."""
    
    def __init__(self):
        self.logger = get_logger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info("Inicializando CalculadoraFisica")
    
    def calcular_velocidad(self, distancia: float, tiempo: float) -> float:
        """Calcula la velocidad dado distancia y tiempo."""
        self.logger.debug(f"Calculando velocidad para distancia={distancia}, tiempo={tiempo}")
        
        try:
            if tiempo <= 0:
                raise ValueError("El tiempo debe ser mayor que cero")
                
            velocidad = distancia / tiempo
            self.logger.info(f"Velocidad calculada: {velocidad} m/s")
            return velocidad
            
        except Exception as e:
            self.logger.error(f"Error al calcular velocidad: {e}", exc_info=True)
            raise

def main():
    # Ejemplo de uso
    logger.info("Iniciando ejemplo de logging")
    
    calculadora = CalculadoraFisica()
    
    # Cálculo exitoso
    try:
        velocidad = calculadora.calcular_velocidad(100, 10)
        logger.info(f"Resultado exitoso: {velocidad} m/s")
    except Exception as e:
        logger.error(f"Error en el cálculo: {e}")
    
    # Cálculo con error
    try:
        velocidad = calculadora.calcular_velocidad(100, 0)
    except Exception as e:
        logger.warning(f"Se esperaba este error: {e}")
    
    logger.info("Ejemplo de logging completado")

if __name__ == "__main__":
    main()
