.. _guia_instalacion:

Guía de Instalación
==================

Requisitos
----------
- Python 3.11 o superior
- pip (gestor de paquetes de Python)

Instalación con pip
-------------------
Puedes instalar Cinetica directamente desde PyPI usando pip:

.. code-block:: bash

    pip install cinetica

Instalación desde el código fuente
---------------------------------
1. Clona el repositorio:

   .. code-block:: bash

       git clone https://github.com/Elabsurdo984/Cinetica.git
       cd Cinetica

2. Instala las dependencias:

   .. code-block:: bash

       pip install -e .

   Para desarrollo, instala también las dependencias adicionales:

   .. code-block:: bash

       pip install -e ".[dev]"

Verificación de la instalación
-----------------------------
Para verificar que la instalación fue exitosa, ejecuta:

.. code-block:: python

    import cinetica
    print(f"Cinetica versión: {cinetica.__version__}")

Solución de problemas
--------------------
Si encuentras algún problema durante la instalación:

1. Asegúrate de tener las herramientas de compilación de Python instaladas
2. Verifica que tienes una versión compatible de Python
3. Revisa los mensajes de error para obtener más detalles

Si el problema persiste, por favor abre un issue en el `repositorio de GitHub <https://github.com/Elabsurdo984/Cinetica/issues>`_.
