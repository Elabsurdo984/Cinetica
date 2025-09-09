.. _ejemplos:

Ejemplos
========

Esta sección contiene ejemplos prácticos de cómo usar Cinetica para resolver problemas comunes de física.

Movimiento Rectilíneo Uniforme (MRU)
-----------------------------------

.. code-block:: python

    from cinetica.cinematica.rectilineo import MRU
    from cinetica import unidades as u
    
    # Crear un objeto MRU con posición inicial 0 y velocidad 5 m/s
    mru = MRU(posicion_inicial=0 * u.m, velocidad=5 * u.m/u.s)
    
    # Calcular posición después de 2 segundos
    posicion = mru.calcular_posicion(2 * u.s)
    print(f"Posición después de 2 segundos: {posicion}")

Segunda Ley de Newton
--------------------

.. code-block:: python

    from cinetica.dinamica import LeyesNewton
    import numpy as np
    
    # Fuerza de 10 N en el eje x, masa de 2 kg
    fuerza = np.array([10, 0, 0]) * u.N
    masa = 2 * u.kg
    
    # Calcular aceleración
    aceleracion = LeyesNewton.segunda_ley(fuerza, masa)
    print(f"Aceleración: {aceleracion}")

Trabajo y Energía
----------------

.. code-block:: python

    from cinetica.dinamica import TrabajoEnergia
    
    # Calcular trabajo de una fuerza constante
    fuerza = 10 * u.N
    desplazamiento = 5 * u.m
    angulo = 30 * u.deg  # Ángulo entre fuerza y desplazamiento
    
    trabajo = TrabajoEnergia.calcular_trabajo(
        fuerza, 
        desplazamiento, 
        angulo=angulo
    )
    print(f"Trabajo realizado: {trabajo:.2f}")

Visualización de Movimiento
--------------------------

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    from cinetica.graficos import graficar_movimiento
    
    # Generar datos de movimiento parabólico
    t = np.linspace(0, 10, 100) * u.s
    x = 5 * t  # MRU en x
    y = -0.5 * 9.8 * t**2 + 50  # Caída libre en y
    
    # Graficar
    plt.figure(figsize=(10, 6))
    graficar_movimiento(t, x, "Tiempo (s)", "Posición X (m)", "Movimiento en X")
    plt.figure(figsize=(10, 6))
    graficar_movimiento(t, y, "Tiempo (s)", "Posición Y (m)", "Movimiento en Y")
    plt.show()

Análisis de Fuerzas en un Plano Inclinado
----------------------------------------

.. code-block:: python

    from cinetica.dinamica import AnalisisFuerzas
    import numpy as np
    
    # Parámetros
    masa = 5 * u.kg
    angulo_inclinacion = 30 * u.deg
    coeficiente_roce = 0.2
    
    # Calcular fuerzas
    peso = masa * 9.8 * u.m/u.s**2
    normal, roce, aceleracion = AnalisisFuerzas.plano_inclinado(
        masa=masa,
        angulo=angulo_inclinacion,
        coeficiente_roce=coeficiente_roce
    )
    
    print(f"Peso: {peso:.2f}")
    print(f"Normal: {normal:.2f}")
    print(f"Roce: {roce:.2f}")
    print(f"Aceleración: {aceleracion:.2f}")
