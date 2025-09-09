.. _desarrollo:

Guía para Desarrolladores
=======================

Esta guía está dirigida a desarrolladores que deseen contribuir al proyecto Cinetica.

Configuración del Entorno
------------------------

1. Clona el repositorio:

   .. code-block:: bash

       git clone https://github.com/Elabsurdo984/Cinetica.git
       cd Cinetica

2. Crea un entorno virtual (recomendado):

   .. code-block:: bash

       python -m venv venv
       .\venv\Scripts\activate  # En Windows
       # O en Unix/macOS:
       # source venv/bin/activate

3. Instala las dependencias de desarrollo:

   .. code-block:: bash

       pip install -e ".[dev]"

Estructura del Proyecto
---------------------

::

    Cinetica/
    ├── cinetica/                 # Código fuente del paquete
    │   ├── cinematica/          # Módulos de cinemática
    │   ├── dinamica/            # Módulos de dinámica
    │   ├── graficos/            # Utilidades de visualización
    │   └── unidades.py          # Manejo de unidades físicas
    ├── tests/                   # Pruebas unitarias
    ├── docs/                    # Documentación
    └── pyproject.toml           # Configuración del proyecto

Convenciones de Código
---------------------
- Sigue PEP 8 para el estilo de código
- Usa type hints en todas las funciones y métodos
- Documenta todas las funciones, clases y métodos con docstrings
- Usa Google Style para los docstrings

Ejecución de Pruebas
-------------------

Para ejecutar todas las pruebas:

.. code-block:: bash

    pytest tests/

Para ejecutar pruebas con cobertura:

.. code-block:: bash

    pytest --cov=cinetica tests/

Construcción de la Documentación
------------------------------

Para construir la documentación localmente:

.. code-block:: bash

    cd docs
    make html

La documentación generada estará disponible en ``docs/_build/html/index.html``

Flujo de Trabajo para Contribuciones
----------------------------------
1. Crea un fork del repositorio
2. Crea una rama para tu característica: ``git checkout -b mi-nueva-caracteristica``
3. Haz commit de tus cambios: ``git commit -m 'Añade alguna característica'``
4. Haz push a la rama: ``git push origin mi-nueva-caracteristica``
5. Abre un Pull Request

Reporte de Errores
-----------------
Por favor, reporta los errores en el `seguimiento de problemas de GitHub <https://github.com/Elabsurdo984/Cinetica/issues>`_.

Incluye la siguiente información:
1. Descripción detallada del error
2. Pasos para reproducir el error
3. Versión de Python y dependencias
4. Mensajes de error completos

Solicitud de Características
--------------------------
Si tienes una idea para una nueva característica, por favor:
1. Verifica que no exista ya una solicitud similar
2. Describe la característica en detalle
3. Explica por qué sería útil para la mayoría de los usuarios
