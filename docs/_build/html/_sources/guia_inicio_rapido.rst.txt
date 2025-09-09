.. _guia_inicio_rapido:

Guía de Inicio Rápido
====================

Este documento te guiará a través de los conceptos básicos de Cinetica.

Primeros pasos
--------------

Importar el paquete:

.. code-block:: python

    import cinetica
    from cinetica import unidades as u

Ejemplo básico: Movimiento Rectilíneo Uniforme (MRU)
---------------------------------------------------

.. code-block:: python

    from cinetica.cinematica.rectilineo import MRU
    
    # Crear un objeto MRU con posición inicial 0 y velocidad 5 m/s
    mru = MRU(posicion_inicial=0 * u.m, velocidad=5 * u.m/u.s)
    
    # Calcular posición después de 2 segundos
    posicion = mru.calcular_posicion(2 * u.s)
    print(f"Posición después de 2 segundos: {posicion}")

Ejemplo avanzado: Segunda Ley de Newton
--------------------------------------

.. code-block:: python

    from cinetica.dinamica import LeyesNewton
    import numpy as np
    
    # Fuerza de 10 N en el eje x, masa de 2 kg
    fuerza = np.array([10, 0, 0]) * u.N
    masa = 2 * u.kg
    
    # Calcular aceleración
    aceleracion = LeyesNewton.segunda_ley(fuerza, masa)
    print(f"Aceleración: {aceleracion}")

Visualización de datos
---------------------

Cinetica incluye utilidades para visualización con Matplotlib:

.. code-block:: python

    import matplotlib.pyplot as plt
    from cinetica.graficos import graficar_movimiento
    
    # Generar datos de posición en función del tiempo
    tiempos = np.linspace(0, 10, 100) * u.s
    posiciones = 0.5 * 2 * u.m/(u.s**2) * tiempos**2
    
    # Graficar
    graficar_movimiento(tiempos, posiciones, "Tiempo (s)", "Posición (m)", "Caída libre")
    plt.show()

Próximos pasos
--------------
- Explora la :ref:`referencia de la API <api>` para ver todas las funcionalidades disponibles
- Revisa los :doc:`ejemplos` para más casos de uso
- Consulta la sección de :doc:`desarrollo` si quieres contribuir al proyecto
