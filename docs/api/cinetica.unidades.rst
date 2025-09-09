.. _api-unidades:

Módulo cinetica.unidades
=======================

.. automodule:: cinetica.unidades
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Unidades disponibles
-------------------

El módulo de unidades proporciona las siguientes constantes y conversiones:

Longitud
~~~~~~~~
- ``metro``, ``m``
- ``kilometro``, ``km``
- ``centimetro``, ``cm``
- ``milimetro``, ``mm``

Tiempo
~~~~~~
- ``segundo``, ``s``
- ``minuto``, ``min``
- ``hora``, ``h``

Masa
~~~~
- ``kilogramo``, ``kg``
- ``gramo``, ``g``
- ``tonelada``, ``t``

Fuerza
~~~~~~
- ``newton``, ``N``
- ``kilogramo_fuerza``, ``kgf``
- ``dina``, ``dyn``

Ángulo
~~~~~~
- ``radian``, ``rad``
- ``grado``, ``deg``
- ``revolucion``, ``rev``

Ejemplos de uso
--------------

.. code-block:: python

    from cinetica.unidades import m, s, kg, N
    
    # Conversión de unidades
    velocidad = 100 * m / s
    print(f"100 m/s = {velocidad.to('km/h'):.2f}")
    
    # Cálculos con unidades
    fuerza = 10 * N
    masa = 2 * kg
    aceleracion = fuerza / masa
    print(f"Aceleración: {aceleracion}")
