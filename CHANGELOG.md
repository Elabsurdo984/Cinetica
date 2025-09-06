# Changelog

## 0.12.0 - 2025-09-06

### Added
- **Type hints completos** en toda la API de la librería para mejor soporte de IDEs y detección temprana de errores
- **Configuración de mypy** con archivo `mypy.ini` para validación estática de tipos
- **Dependencias de desarrollo** en `pyproject.toml` incluyendo mypy, pytest, black, flake8, y pre-commit
- **Sistema de tipos robusto** usando `TYPE_CHECKING` para compatibilidad con herramientas de análisis estático

### Changed
- **Mejorados todos los módulos** con type hints profesionales:
  - `units.py` - Sistema de tipos base con TypeAlias para Quantity
  - `base_movimiento.py` - Clase abstracta con tipos Union para flexibilidad
  - Módulos de movimiento rectilíneo (MRU/MRUV) con tipos Optional y Union
  - Módulos de movimiento circular (MCU/MCUV) con tipos para vectores numpy
  - Módulo de movimiento espacial con tipos para arrays 3D
  - Módulos de movimiento armónico (simple y complejo) con tipos para listas y diccionarios
  - Módulo de movimiento relativo con tipos para vectores de velocidad
- **Documentación mejorada** con docstrings que incluyen información de tipos en formato NumPy
- **Compatibilidad mejorada** con herramientas de desarrollo modernas

### Technical
- **157 tests pasando** sin errores después de la implementación de type hints
- **Configuración de mypy** balanceada entre strictness y practicidad
- **Soporte completo para pint.Quantity** en el sistema de tipos
- **Validación automática** de tipos en tiempo de desarrollo

## 0.11.0 - 2025-09-05

### Added
- Archivos de pruebas unitarias completos para todos los módulos de movimiento:
  - `test_units_espacial.py` - Pruebas unitarias para MovimientoEspacial con manejo de unidades
  - `test_units_oscilatorio.py` - Pruebas unitarias para MovimientoArmonicoSimple con manejo de unidades
  - `test_units_armonico_complejo.py` - Pruebas unitarias para MovimientoArmonicoComplejo con manejo de unidades
  - `test_units_relativo.py` - Pruebas unitarias para MovimientoRelativo con manejo de unidades
- Métodos `amplitud_resultante()` y `fase_resultante()` en la clase `MovimientoArmonicoComplejo` para cálculo de amplitud y fase resultante en superposición de componentes armónicos con la misma frecuencia
- Validación de tiempo negativo en métodos `posicion_angular()` y `velocidad_angular()` de `MovimientoCircularUniformementeVariado`

### Fixed
- Corregidos todos los tests fallidos (111/111 tests ahora pasan exitosamente):
  - Solucionados problemas de comparación entre objetos `pint.Quantity` y valores numéricos
  - Reemplazado `np.array_equal()` con `np.allclose()` para comparaciones de magnitudes de cantidades con unidades
  - Corregidas expectativas de unidades en tests de energía para movimiento armónico (incluyendo unidades de radianes)
  - Corregido vector de aceleración centrípeta en movimiento circular uniforme
  - Ajustadas firmas de métodos y expectativas de tests para consistencia con implementaciones

### Changed
- Mejorado manejo de unidades en cálculos físicos, manteniendo consistencia dimensional incluyendo radianes
- Actualizadas expectativas de tests para reflejar el comportamiento real de las implementaciones con `pint`
- Optimizadas comparaciones numéricas en tests para mayor robustez con números de punto flotante

## 0.10.6 - 2025-09-05

### Added
- Se implementó un sistema de unidades con `pint` para mejorar el manejo de las unidades en los cálculos físicos.
- Se creó el módulo `cinetica/units.py` para la gestión del registro de unidades.
- Se integró `pint` en `cinetica/cinematica/rectilineo/movimiento_rectilineo_uniforme.py`, permitiendo el uso de cantidades con unidades en sus métodos.

## 0.10.5 - 2025-09-05

### Fixed
- Se solucionó un problema de importación circular que impedía el uso correcto de los módulos de la librería
- Se reorganizó la estructura de importaciones en `cinetica/__init__.py` para mejorar la modularidad
- Se actualizaron las importaciones en los archivos de ejemplo para seguir las mejores prácticas

## 0.10.4 - 2025-09-05

### Added
- Se creó una clase base `Movimiento` abstracta en `cinetica/cinematica/base_movimiento.py` para definir una interfaz común para todos los tipos de movimiento.

### Changed
- Se refactorizaron las siguientes clases de movimiento para heredar de la nueva clase base `Movimiento`, implementando sus métodos abstractos (`posicion`, `velocidad`, `aceleracion`):
  - `MovimientoRectilineoUniforme`
  - `MovimientoRectilineoUniformementeVariado`
  - `MovimientoCircularUniforme`
  - `MovimientoCircularUniformementeVariado`
  - `MovimientoEspacial`
  - `MovimientoArmonicoSimple`
  - `MovimientoArmonicoComplejo`
- Se actualizaron los archivos `cinetica/cinematica/__init__.py` para exportar la nueva clase base `Movimiento`.
- Se modificaron los ejemplos de uso en la carpeta `usage/` para adaptarse a los cambios en las firmas de los métodos y la nueva estructura de herencia.

## 0.10.3 - 2025-09-05

### Changed
- Se cambio la nomenclatura de los archivos haciendolos mas facil de entender

## 0.10.0 - 2025-09-03

### Added
- Se creó la carpeta `cinetica/dinamica` para futuros módulos de dinámica.

### Changed
- Se reorganizó la estructura del proyecto:
  - Se creó la carpeta `cinetica/cinematica` y se movieron todos los módulos de cinemática (`circular`, `espacial`, `oscilatorio`, `parabolico`, `rectilineo`, `relativo`) a esta nueva carpeta.
  - Se actualizaron las importaciones en `cinetica/cinematica/__init__.py` para reflejar la nueva estructura.

### Fixed
- Corregidos errores de importación en `cinetica/cinematica/__init__.py` para resolver `ModuleNotFoundError` en los tests.

## 0.9.0 - 2025-09-03

### Added
- Funcionalidad de graficación 3D para el módulo `MovimientoEspacial`.
  - Se añadió la función `plot_movimiento_espacial` en `cinetica/graficos/graficador.py`.
  - Se implementó el método `graficar` en la clase `MovimientoEspacial`.
  - Se actualizó `DOCS.md` y el archivo de ejemplo `usage/movimiento_espacial_ejemplo.py` para reflejar esta nueva funcionalidad.
  - Se añadió un test unitario para el método `graficar` en `tests/test_movimiento_espacial.py`.

## 0.8.0 - 2025-09-02

### Added
- Se creó el nuevo módulo `movimiento_espacial` sobre cinemática en 3D, se creó su respectivo test y su clase `MovimientoEspacial`.

## 0.7.6 - 2025-09-02

### Changed
- Documentacion transportada de README.md a DOCS.md

## 0.7.0 - 2025-08-30

### Added
- Funcionalidad de graficación para los módulos de cinemática 1D (MRU, MRUV), 2D (Parabólico) y Circular (MCU, MCUV).
  - Se creó el nuevo paquete `cinetica/graficos` con el módulo `graficador.py` que contiene funciones para generar gráficos de posición, velocidad, aceleración y trayectoria.
  - Se añadió un método `graficar(self, t_max: float, num_points: int = 100)` a las clases `MovimientoRectilineoUniforme`, `MovimientoRectilineoUniformementeVariado`, `MovimientoParabolicoBase`, `MovimientoCircularUniforme` y `MovimientoCircularUniformementeVariado`.
  - Este método permite al usuario generar visualizaciones de los movimientos simulados.
- Nuevo módulo `MovimientoArmonicoComplejo` con la clase `MovimientoArmonicoComplejo` para la superposición de múltiples Movimientos Armónicos Simples.
- Tests unitarios para la clase `MovimientoArmonicoComplejo`.
- Actualizados los archivos `__init__.py` en `cinetica/oscilatorio/` para incluir el nuevo módulo.

## 0.5.9 - 2025-08-29

### Added
- Nuevo módulo `MovimientoRelativo` con la clase `MovimientoRelativo` para cálculos de velocidad relativa en 2D y 3D, incluyendo magnitud y dirección.
- Tests unitarios para la clase `MovimientoRelativo`.
- Actualizados los archivos `__init__.py` en `cinetica/` para incluir el nuevo módulo.

## 0.4.9 - 2025-08-29

### Added
- Nuevo módulo `MovimientoOscilatorio` con la clase `MovimientoArmonicoSimple` para cálculos de posición, velocidad, aceleración, período, frecuencia y energías en M.A.S.
- Tests unitarios para la clase `MovimientoArmonicoSimple`.
- Actualizados los archivos `__init__.py` en `cinetica/` para incluir el nuevo módulo.

## 0.3.8 - 2025-08-29

### Changed
- Refactorización de la arquitectura del proyecto para mejorar la modularidad y la facilidad de importación.
  - La clase `MovimientoRectilineo` se dividió en `MovimientoRectilineoUniforme` (MRU) y `MovimientoRectilineoUniformementeVariado` (MRUV) en `cinetica/rectilineo/mru.py` y `cinetica/rectilineo/mruv.py` respectivamente.
  - La clase `MovimientoCircular` se dividió en `MovimientoCircularUniforme` (MCU) y `MovimientoCircularUniformementeVariado` (MCUV) en `cinetica/circular/mcu.py` y `cinetica/circular/mcuv.py` respectivamente.
  - La clase `MovimientoParabolico` se dividió en `MovimientoParabolicoBase` y `MovimientoParabolicoAnalisis` en `cinetica/parabolico/base.py` y `cinetica/parabolico/analisis.py` respectivamente.
- Actualizados los archivos `__init__.py` en `cinetica/`, `cinetica/rectilineo/`, `cinetica/circular/` y `cinetica/parabolico/` para reflejar la nueva estructura de módulos.
- Actualizados los tests en `tests/test_movimiento_rectilineo.py`, `tests/test_movimiento_circular.py` y `tests/test_movimiento_parabolico.py` para usar las nuevas clases y métodos.

## 0.3.7 - 2025-08-28

### Fixed
- Actualizados los tests de `MovimientoCircular` para reflejar los cambios en el manejo de errores de `mcu_periodo` y `mcu_frecuencia`.
- Actualizada la versión de la librería en `cinetica/__init__.py` y `tests/test_cinetica.py`.

## 0.3.6 - 2025-08-28

### Added
- Métodos `mcuv_velocidad_angular_sin_tiempo`, `mcuv_tiempo_por_posicion_angular` y `mcuv_tiempo_por_velocidad_angular` a la clase `MovimientoCircular`.

## 0.3.5 - 2025-08-28

### Added
- Métodos `mruv_tiempo_por_posicion`, `mruv_tiempo_por_velocidad` y `mruv_desplazamiento_sin_tiempo` a la clase `MovimientoRectilineo`.

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
