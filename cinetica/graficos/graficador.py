import matplotlib.pyplot as plt
import numpy as np

def configurar_estilo_grafico():
    """
    Configura el estilo común para todos los gráficos.
    """
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams['figure.figsize'] = [10, 6]
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.alpha'] = 0.7
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 11
    plt.rcParams['axes.titlepad'] = 10
    plt.rcParams['figure.titlesize'] = 12
    plt.rcParams['figure.titleweight'] = 'bold'
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['legend.fontsize'] = 9
    plt.rcParams['figure.subplot.wspace'] = 0.3
    plt.rcParams['figure.subplot.hspace'] = 0.3

def plot_mru(mru_obj, t_max: float, num_points: int = 100):
    """
    Genera y muestra gráficos de posición vs. tiempo y velocidad vs. tiempo para MRU.

    Args:
        mru_obj: Instancia de MovimientoRectilineoUniforme.
        t_max (float): Tiempo máximo para la simulación (s).
        num_points (int): Número de puntos a generar para el gráfico.
    """
    configurar_estilo_grafico()
    if t_max <= 0:
        raise ValueError("El tiempo máximo debe ser positivo para generar el gráfico.")

    tiempo = np.linspace(0, t_max, num_points)
    posiciones = [mru_obj.posicion(t) for t in tiempo]
    velocidades = [mru_obj.velocidad() for _ in tiempo] # Velocidad constante

    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    fig.suptitle('Movimiento Rectilíneo Uniforme (MRU)', y=0.98, fontsize=12, fontweight='bold')

    # Gráfico de Posición vs. Tiempo
    axs[0].plot(tiempo, posiciones, label='Posición (x)', linewidth=2)
    axs[0].set_xlabel('Tiempo (s)', fontsize=10)
    axs[0].set_ylabel('Posición (m)', fontsize=10)
    axs[0].set_title('Posición vs. Tiempo', pad=10, fontsize=11)
    axs[0].legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    axs[0].tick_params(labelsize=9)

    # Gráfico de Velocidad vs. Tiempo
    axs[1].plot(tiempo, velocidades, label='Velocidad (v)', color='orange', linewidth=2)
    axs[1].set_xlabel('Tiempo (s)', fontsize=10)
    axs[1].set_ylabel('Velocidad (m/s)', fontsize=10)
    axs[1].set_title('Velocidad vs. Tiempo', pad=10, fontsize=11)
    axs[1].legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    axs[1].tick_params(labelsize=9)

    plt.tight_layout(rect=[0, 0.03, 0.95, 0.95]) # Adjusted rect for legend
    plt.show()

def plot_mruv(mruv_obj, t_max: float, num_points: int = 100):
    """
    Genera y muestra gráficos de posición vs. tiempo, velocidad vs. tiempo y aceleración vs. tiempo para MRUV.

    Args:
        mruv_obj: Instancia de MovimientoRectilineoUniformementeVariado.
        t_max (float): Tiempo máximo para la simulación (s).
        num_points (int): Número de puntos a generar para el gráfico.
    """
    configurar_estilo_grafico()
    if t_max <= 0:
        raise ValueError("El tiempo máximo debe ser positivo para generar el gráfico.")

    tiempo = np.linspace(0, t_max, num_points)
    posiciones = [mruv_obj.posicion(t) for t in tiempo]
    velocidades = [mruv_obj.velocidad(t) for t in tiempo]
    aceleraciones = [mruv_obj.aceleracion() for _ in tiempo] # Aceleración constante

    fig, axs = plt.subplots(3, 1, figsize=(10, 12))
    fig.suptitle('Movimiento Rectilíneo Uniformemente Variado (MRUV)', y=0.98, fontsize=12, fontweight='bold')

    # Gráfico de Posición vs. Tiempo
    axs[0].plot(tiempo, posiciones, label='Posición (x)', linewidth=2)
    axs[0].set_xlabel('Tiempo (s)', fontsize=10)
    axs[0].set_ylabel('Posición (m)', fontsize=10)
    axs[0].set_title('Posición vs. Tiempo', pad=10, fontsize=11)
    axs[0].legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    axs[0].tick_params(labelsize=9)

    # Gráfico de Velocidad vs. Tiempo
    axs[1].plot(tiempo, velocidades, label='Velocidad (v)', color='orange', linewidth=2)
    axs[1].set_xlabel('Tiempo (s)', fontsize=10)
    axs[1].set_ylabel('Velocidad (m/s)', fontsize=10)
    axs[1].set_title('Velocidad vs. Tiempo', pad=10, fontsize=11)
    axs[1].legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    axs[1].tick_params(labelsize=9)

    # Gráfico de Aceleración vs. Tiempo
    axs[2].plot(tiempo, aceleraciones, label='Aceleración (a)', color='green', linewidth=2)
    axs[2].set_xlabel('Tiempo (s)', fontsize=10)
    axs[2].set_ylabel('Aceleración (m/s²)', fontsize=10)
    axs[2].set_title('Aceleración vs. Tiempo', pad=10, fontsize=11)
    axs[2].legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    axs[2].tick_params(labelsize=9)

    plt.tight_layout(rect=[0, 0.03, 0.95, 0.95]) # Adjusted rect for legend
    plt.show()

def plot_parabolico(parabolico_obj, t_max: float, num_points: int = 100):
    """
    Genera y muestra el gráfico de la trayectoria (y vs. x) para Movimiento Parabólico.

    Args:
        parabolico_obj: Instancia de MovimientoParabolicoBase.
        t_max (float): Tiempo máximo para la simulación (s).
        num_points (int): Número de puntos a generar para el gráfico.
    """
    configurar_estilo_grafico()
    if t_max <= 0:
        raise ValueError("El tiempo máximo debe ser positivo para generar el gráfico.")

    tiempo = np.linspace(0, t_max, num_points)
    posiciones_x = []
    posiciones_y = []
    for t in tiempo:
        x, y = parabolico_obj.posicion(t)
        if y >= 0: # Solo graficar mientras el proyectil esté por encima o en el suelo
            posiciones_x.append(x)
            posiciones_y.append(y)
        else:
            break # Detener si el proyectil cae por debajo del suelo

    fig = plt.figure(figsize=(10, 6))
    plt.plot(posiciones_x, posiciones_y, label='Trayectoria Parabólica', linewidth=2)
    plt.xlabel('Posición Horizontal (x) [m]', fontsize=10)
    plt.ylabel('Posición Vertical (y) [m]', fontsize=10)
    plt.title('Movimiento Parabólico: Trayectoria', pad=10, fontsize=12, fontweight='bold')
    plt.axhline(0, color='black', linestyle='--', linewidth=0.7) # Eje x
    plt.axvline(0, color='black', linestyle='--', linewidth=0.7) # Eje y
    plt.legend(loc='upper right', bbox_to_anchor=(1, 1))
    plt.gca().set_aspect('equal', adjustable='box') # Para que la escala sea igual en ambos ejes
    plt.tick_params(labelsize=9)
    
    # Añadir margen extra para evitar solapamiento
    plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95]) # Adjusted rect for legend and title
    plt.show()

def plot_mcu(mcu_obj, t_max: float, num_points: int = 100):
    """
    Genera y muestra gráficos de posición angular vs. tiempo, velocidad angular vs. tiempo
    y aceleración centrípeta vs. tiempo para MCU. También grafica la trayectoria circular.

    Args:
        mcu_obj: Instancia de MovimientoCircularUniforme.
        t_max (float): Tiempo máximo para la simulación (s).
        num_points (int): Número de puntos a generar para el gráfico.
    """
    configurar_estilo_grafico()
    if t_max <= 0:
        raise ValueError("El tiempo máximo debe ser positivo para generar el gráfico.")

    tiempo = np.linspace(0, t_max, num_points)
    posiciones_angulares = [mcu_obj.posicion_angular(t) for t in tiempo]
    velocidades_angulares = [mcu_obj.velocidad_angular() for _ in tiempo]
    aceleraciones_centripetas = [mcu_obj.aceleracion_centripeta() for _ in tiempo]

    fig, axs = plt.subplots(3, 1, figsize=(10, 12))
    fig.suptitle('Movimiento Circular Uniforme (MCU)', y=0.98, fontsize=12, fontweight='bold')

    # Gráfico de Posición Angular vs. Tiempo
    axs[0].plot(tiempo, posiciones_angulares, label='Posición Angular (θ)', linewidth=2)
    axs[0].set_xlabel('Tiempo (s)', fontsize=10)
    axs[0].set_ylabel('Posición Angular (rad)', fontsize=10)
    axs[0].set_title('Posición Angular vs. Tiempo', pad=10, fontsize=11)
    axs[0].legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    axs[0].tick_params(labelsize=9)

    # Gráfico de Velocidad Angular vs. Tiempo
    axs[1].plot(tiempo, velocidades_angulares, label='Velocidad Angular (ω)', color='orange', linewidth=2)
    axs[1].set_xlabel('Tiempo (s)', fontsize=10)
    axs[1].set_ylabel('Velocidad Angular (rad/s)', fontsize=10)
    axs[1].set_title('Velocidad Angular vs. Tiempo', pad=10, fontsize=11)
    axs[1].legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    axs[1].tick_params(labelsize=9)

    # Gráfico de Aceleración Centrípeta vs. Tiempo
    axs[2].plot(tiempo, aceleraciones_centripetas, label='Aceleración Centrípeta (ac)', color='green', linewidth=2)
    axs[2].set_xlabel('Tiempo (s)', fontsize=10)
    axs[2].set_ylabel('Aceleración Centrípeta (m/s²)', fontsize=10)
    axs[2].set_title('Aceleración Centrípeta vs. Tiempo', pad=10, fontsize=11)
    axs[2].legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    axs[2].tick_params(labelsize=9)

    plt.tight_layout(rect=[0, 0.03, 0.95, 0.95]) # Adjusted rect for legend
    plt.show()

    # Gráfico de la trayectoria circular (opcional, en un gráfico separado para claridad)
    fig = plt.figure(figsize=(8, 8))
    theta = np.linspace(0, 2 * np.pi, 100)
    x_circ = mcu_obj.radio * np.cos(theta)
    y_circ = mcu_obj.radio * np.sin(theta)
    plt.plot(x_circ, y_circ, label='Trayectoria Circular', linewidth=2)
    plt.scatter(0, 0, color='red', marker='o', s=100, label='Centro')
    plt.xlabel('X (m)', fontsize=10)
    plt.ylabel('Y (m)', fontsize=10)
    plt.title('Movimiento Circular Uniforme: Trayectoria', pad=10, fontsize=12, fontweight='bold')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1.1))
    plt.tick_params(labelsize=9)
    
    # Añadir márgenes para evitar solapamiento
    plt.tight_layout(rect=[0.05, 0.05, 0.9, 0.9]) # Adjusted rect for legend
    plt.show()

def plot_mcuv(mcuv_obj, t_max: float, num_points: int = 100):
    """
    Genera y muestra gráficos de posición angular vs. tiempo, velocidad angular vs. tiempo,
    aceleración angular vs. tiempo, aceleración centrípeta vs. tiempo y aceleración total vs. tiempo para MCUV.

    Args:
        mcuv_obj: Instancia de MovimientoCircularUniformementeVariado.
        t_max (float): Tiempo máximo para la simulación (s).
        num_points (int): Número de puntos a generar para el gráfico.
    """
    configurar_estilo_grafico()
    if t_max <= 0:
        raise ValueError("El tiempo máximo debe ser positivo para generar el gráfico.")

    tiempo = np.linspace(0, t_max, num_points)
    posiciones_angulares = [mcuv_obj.posicion_angular(t) for t in tiempo]
    velocidades_angulares = [mcuv_obj.velocidad_angular(t) for t in tiempo]
    aceleraciones_angulares = [mcuv_obj.aceleracion_angular() for _ in tiempo]
    aceleraciones_centripetas = [mcuv_obj.aceleracion_centripeta(t) for t in tiempo]
    aceleraciones_totales = [mcuv_obj.aceleracion_total(t) for t in tiempo]

    fig, axs = plt.subplots(5, 1, figsize=(10, 20))
    fig.suptitle('Movimiento Circular Uniformemente Variado (MCUV)', y=0.98, fontsize=12, fontweight='bold')

    # Gráfico de Posición Angular vs. Tiempo
    axs[0].plot(tiempo, posiciones_angulares, label='Posición Angular (θ)', linewidth=2)
    axs[0].set_xlabel('Tiempo (s)', fontsize=10)
    axs[0].set_ylabel('Posición Angular (rad)', fontsize=10)
    axs[0].set_title('Posición Angular vs. Tiempo', pad=10, fontsize=11)
    axs[0].legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    axs[0].tick_params(labelsize=9)

    # Gráfico de Velocidad Angular vs. Tiempo
    axs[1].plot(tiempo, velocidades_angulares, label='Velocidad Angular (ω)', color='orange', linewidth=2)
    axs[1].set_xlabel('Tiempo (s)', fontsize=10)
    axs[1].set_ylabel('Velocidad Angular (rad/s)', fontsize=10)
    axs[1].set_title('Velocidad Angular vs. Tiempo', pad=10, fontsize=11)
    axs[1].legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    axs[1].tick_params(labelsize=9)

    # Gráfico de Aceleración Angular vs. Tiempo
    axs[2].plot(tiempo, aceleraciones_angulares, label='Aceleración Angular (α)', color='green', linewidth=2)
    axs[2].set_xlabel('Tiempo (s)', fontsize=10)
    axs[2].set_ylabel('Aceleración Angular (rad/s²)', fontsize=10)
    axs[2].set_title('Aceleración Angular vs. Tiempo', pad=10, fontsize=11)
    axs[2].legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    axs[2].tick_params(labelsize=9)

    # Gráfico de Aceleración Centrípeta vs. Tiempo
    axs[3].plot(tiempo, aceleraciones_centripetas, label='Aceleración Centrípeta (ac)', color='red', linewidth=2)
    axs[3].set_xlabel('Tiempo (s)', fontsize=10)
    axs[3].set_ylabel('Aceleración Centrípeta (m/s²)', fontsize=10)
    axs[3].set_title('Aceleración Centrípeta vs. Tiempo', pad=10, fontsize=11)
    axs[3].legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    axs[3].tick_params(labelsize=9)

    # Gráfico de Aceleración Total vs. Tiempo
    axs[4].plot(tiempo, aceleraciones_totales, label='Aceleración Total (a_total)', color='purple', linewidth=2)
    axs[4].set_xlabel('Tiempo (s)', fontsize=10)
    axs[4].set_ylabel('Aceleración Total (m/s²)', fontsize=10)
    axs[4].set_title('Aceleración Total vs. Tiempo', pad=10, fontsize=11)
    axs[4].legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    axs[4].tick_params(labelsize=9)

    plt.tight_layout(rect=[0, 0.03, 0.95, 0.95]) # Adjusted rect for legend
    plt.show()
