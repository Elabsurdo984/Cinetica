"""
Módulo de logging centralizado para la librería Cinetica.

Este módulo proporciona una configuración consistente de logging para toda la aplicación,
permitiendo un registro detallado de eventos, advertencias y errores.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Union, Dict, Any

# Niveles de log predefinidos
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

# Configuración por defecto
DEFAULT_LEVEL = 'INFO'
DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Logger raíz de la aplicación
_root_logger = None

def setup_logger(
    name: str = "cinetica",
    level: Union[str, int] = DEFAULT_LEVEL,
    log_file: Optional[Union[str, Path]] = None,
    log_format: str = DEFAULT_FORMAT,
    date_format: str = DEFAULT_DATE_FORMAT,
    propagate: bool = False,
    **kwargs: Any
) -> logging.Logger:
    """
    Configura y retorna un logger con formato consistente.
    
    Args:
        name: Nombre del logger (usualmente __name__)
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL) o valor numérico
        log_file: Ruta opcional para guardar logs en archivo
        log_format: Formato de los mensajes de log
        date_format: Formato de la fecha en los logs
        propagate: Si es True, los mensajes se propagan a los loggers padres
        **kwargs: Argumentos adicionales para FileHandler si se usa log_file
        
    Returns:
        logging.Logger: Logger configurado
        
    Examples:
        >>> logger = setup_logger(__name__)
        >>> logger.info("Mensaje informativo")
    """
    global _root_logger
    
    # Si es el logger raíz, configurarlo como tal
    is_root = (name == 'cinetica' or name == 'root')
    
    # Obtener el logger
    logger = logging.getLogger(name)
    
    # Evitar múltiples configuraciones
    if not _is_configured(logger, is_root):
        # Configurar nivel
        log_level = _get_log_level(level)
        logger.setLevel(log_level)
        
        # Crear formateador
        formatter = logging.Formatter(log_format, datefmt=date_format)
        
        # Configurar manejador para consola
        console_handler = _get_console_handler(formatter)
        
        # Si es el logger raíz, configurarlo como tal
        if is_root:
            # Eliminar manejadores existentes
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
                handler.close()
            
            logger.addHandler(console_handler)
            logger.propagate = propagate
            _root_logger = logger
            
            # Configurar también el logger raíz de logging
            logging.basicConfig(handlers=[console_handler], level=log_level)
        else:
            # Para loggers hijos, solo agregar manejador si no hay ninguno
            if not logger.handlers:
                logger.addHandler(console_handler)
            logger.propagate = True  # Propagar al logger raíz
        
        # Configurar archivo de log si se especifica
        if log_file:
            file_handler = _get_file_handler(log_file, formatter, **kwargs)
            logger.addHandler(file_handler)
            
            if is_root and _root_logger:
                _root_logger.addHandler(file_handler)
    
    return logger

def _is_configured(logger: logging.Logger, is_root: bool) -> bool:
    """Verifica si el logger ya está configurado."""
    if is_root and _root_logger is not None:
        return True
    return bool(logger.handlers)

def _get_log_level(level: Union[str, int]) -> int:
    """Obtiene el nivel de log como entero."""
    if isinstance(level, str):
        return LOG_LEVELS.get(level.upper(), LOG_LEVELS[DEFAULT_LEVEL])
    return level

def _get_console_handler(formatter: logging.Formatter) -> logging.StreamHandler:
    """Configura el manejador para consola."""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    return console_handler

def _get_file_handler(
    log_file: Union[str, Path], 
    formatter: logging.Formatter,
    **kwargs: Any
) -> logging.FileHandler:
    """Configura el manejador para archivo."""
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(log_path, **kwargs)
    file_handler.setFormatter(formatter)
    return file_handler

def get_logger(name: str = None) -> logging.Logger:
    """
    Obtiene un logger configurado.
    
    Si no se especifica nombre, retorna el logger raíz.
    """
    if not name:
        return _root_logger or setup_logger('cinetica')
    return logging.getLogger(name)

# Configurar logger raíz por defecto al importar el módulo
if _root_logger is None:
    setup_logger('cinetica')
