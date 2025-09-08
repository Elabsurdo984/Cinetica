"""
Pruebas unitarias para el módulo de configuración.
"""

import os
from pathlib import Path
import tempfile
from unittest import TestCase, mock

from cinetica.config import (
    Settings,
    LoggingSettings,
    PerformanceSettings,
    settings as app_settings,
)


class TestLoggingSettings(TestCase):
    """Pruebas para la configuración de logging."""

    def test_default_values(self):
        """Verificar valores por defecto."""
        config = LoggingSettings()
        self.assertEqual(config.level, "INFO")
        self.assertIsNone(config.file)
        self.assertIn("%(asctime)s", config.format)
        self.assertIn("%H:%M:%S", config.date_format)

    def test_validate_log_level(self):
        """Verificar validación de niveles de log."""
        # Niveles válidos
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            config = LoggingSettings(level=level)
            self.assertEqual(config.level, level)

        # Nivel inválido
        with self.assertRaises(ValueError):
            LoggingSettings(level="INVALID_LEVEL")


class TestPerformanceSettings(TestCase):
    """Pruebas para la configuración de rendimiento."""

    def test_default_values(self):
        """Verificar valores por defecto."""
        config = PerformanceSettings()
        self.assertEqual(config.max_workers, 4)
        self.assertTrue(config.cache_enabled)
        self.assertEqual(config.cache_ttl, 300)

    def test_validation(self):
        """Verificar validación de valores."""
        # max_workers debe ser >= 1 y <= 64
        with self.assertRaises(ValueError):
            PerformanceSettings(max_workers=0)
        with self.assertRaises(ValueError):
            PerformanceSettings(max_workers=65)

        # cache_ttl no puede ser negativo
        with self.assertRaises(ValueError):
            PerformanceSettings(cache_ttl=-1)


class TestSettings(TestCase):
    """Pruebas para la configuración principal."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

    def test_default_values(self):
        """Verificar valores por defecto."""
        with mock.patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            # Valores por defecto
            self.assertEqual(settings.env, "production")
            self.assertFalse(settings.debug)
            self.assertFalse(settings.testing)
            
            # Sub-configuraciones
            self.assertIsInstance(settings.logging, LoggingSettings)
            self.assertIsInstance(settings.performance, PerformanceSettings)

    def test_environment_development(self):
        """Verificar configuración para entorno de desarrollo."""
        settings = Settings(env="development")
        self.assertTrue(settings.debug)
        self.assertEqual(settings.logging.level, "DEBUG")

    def test_environment_testing(self):
        """Verificar configuración para entorno de pruebas."""
        settings = Settings(env="testing")
        self.assertTrue(settings.testing)
        self.assertTrue(settings.debug)
        self.assertFalse(settings.performance.cache_enabled)

    def test_log_file_auto_creation(self):
        """Verificar creación automática de directorio de logs."""
        log_dir = Path(self.temp_dir.name) / "custom_logs"
        log_file = log_dir / "test.log"
        
        try:
            # Crear configuración con el archivo de log
            settings = Settings(env="development", logging={"file": log_file})
            
            # El directorio se crea al acceder al logger
            from cinetica.logger import setup_logger, get_logger
            logger = setup_logger("test_logger", log_file=log_file)
            
            # Forzar la creación del directorio y archivo
            logger.info("Test message")
            
            # Verificar que el directorio se creó
            self.assertTrue(log_file.parent.exists())
            self.assertTrue(log_file.exists())
        finally:
            # Limpiar manejadores para liberar el archivo
            if 'logger' in locals():
                for handler in logger.handlers[:]:
                    handler.close()
                    logger.removeHandler(handler)


class TestEnvironmentVariables(TestCase):
    """Pruebas para la carga de variables de entorno."""

    def test_load_from_env_vars(self):
        """Verificar carga de configuración desde variables de entorno."""
        env_vars = {
            "ENV": "development",
            "LOGGING__LEVEL": "DEBUG",
            "LOGGING__FILE": "/tmp/cinetica.log",
            "PERFORMANCE__MAX_WORKERS": "8",
            "PERFORMANCE__CACHE_ENABLED": "false",
        }
        
        with mock.patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            
            self.assertEqual(settings.env, "development")
            self.assertEqual(settings.logging.level, "DEBUG")
            self.assertEqual(settings.logging.file, Path("/tmp/cinetica.log"))
            self.assertEqual(settings.performance.max_workers, 8)
            self.assertFalse(settings.performance.cache_enabled)


class TestGlobalSettings(TestCase):
    """Pruebas para la configuración global."""

    def test_global_settings_initialized(self):
        """Verificar que la configuración global se inicializa correctamente."""
        self.assertIsInstance(app_settings, Settings)
        self.assertIsInstance(app_settings.logging, LoggingSettings)
        self.assertIsInstance(app_settings.performance, PerformanceSettings)

    def test_global_settings_singleton(self):
        """Verificar que solo hay una instancia de configuración."""
        from cinetica.config import settings as settings2
        self.assertIs(app_settings, settings2)
