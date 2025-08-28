# Changelog
## 0.3.4 - 2025-08-28

### Changed
- Se han revisado y estandarizado los docstrings de todos los métodos en las clases `MovimientoRectilineo`, `MovimientoCircular` y `MovimientoParabolico`, incluyendo detalles sobre argumentos, valores de retorno y excepciones/notas de valores límite.

## 0.3.3 - 2025-08-28

### Changed
- Estandarizado el manejo de errores en las clases `MovimientoRectilineo` y `MovimientoCircular`, utilizando `ValueError` para entradas inválidas y `math.inf` o `0.0` para escenarios físicamente definidos con valores límite.

## 0.3.2 - 2025-08-28

### Changed
- Añadidas sugerencias de tipo a todas las firmas de métodos y sus parámetros en las clases `MovimientoRectilineo`, `MovimientoCircular` y `MovimientoParabolico`.

## 0.3.1 - 2025-08-28

### Changed
- Se corrigió un error al intentar subir la versión 0.3.1 a PyPI, ya que esta versión ya existía.

## 0.3.0 - 2025-08-24

### Added
- Módulo `MovimientoCircular` para cálculos de MCU y MCUV.
- Tests unitarios para la clase `MovimientoCircular`.
- Documentación de uso para `MovimientoCircular` en `README.md`.
  
## 0.2.0 - 2025-08-24

### Added
- Módulo `MovimientoParabolico` para simulación de trayectorias, alcance y tiempo de vuelo.
- Tests unitarios para la clase `MovimientoParabolico`.
- Documentación de uso para `MovimientoParabolico` en `README.md`.

## 0.1.0 - 2025-08-24

### Added
- Módulo `MovimientoRectilineo` para cálculos de MRU y MRUV.
- Tests unitarios para la clase `MovimientoRectilineo`.
- Documentación de uso para `MovimientoRectilineo` en `README.md`.
- Enlaces de GitHub (Homepage y Bug Tracker) en `pyproject.toml`.
- Módulo `MovimientoParabolico` para simulación de trayectorias, alcance y tiempo de vuelo.
- Tests unitarios para la clase `MovimientoParabolico`.
- Documentación de uso para `MovimientoParabolico` en `README.md`.
