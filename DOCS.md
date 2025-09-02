# Documentación de la Librería Cinetica

`Cinetica` es una librería de Python diseñada para simular y analizar diversos tipos de movimiento en física. Proporciona clases y funciones para calcular posiciones, velocidades, aceleraciones y otras propiedades cinemáticas para movimientos rectilíneos, parabólicos, circulares, oscilatorios y relativos.

## Estructura de la Librería

La librería se organiza en módulos, cada uno dedicado a un tipo específico de movimiento:

- `rectilineo`: Movimiento Rectilíneo Uniforme (MRU) y Movimiento Rectilíneo Uniformemente Variado (MRUV).
- `parabolico`: Movimiento Parabólico (Base y Análisis).
- `circular`: Movimiento Circular Uniforme (MCU) y Movimiento Circular Uniformemente Variado (MCUV).
- `oscilatorio`: Movimiento Armónico Simple (MAS) y Movimiento Armónico Complejo (MAC).
- `relativo`: Cálculo de velocidades relativas.
- `espacial`: Movimiento en 3D con vectores de posición, velocidad y aceleración.
- `graficos`: Funciones para la visualización de los movimientos.

## Módulos y Clases

### 1. Movimiento Rectilíneo (`cinetica.rectilineo`)

Este módulo maneja los movimientos en una sola dimensión con velocidad constante o aceleración constante.

#### `MovimientoRectilineoUniforme` (MRU)

Clase para calcular posición y velocidad en Movimiento Rectilíneo Uniforme.

- **`__init__(self, posicion_inicial: float = 0.0, velocidad_inicial: float = 0.0)`**:
    Inicializa el objeto MRU.
    - `posicion_inicial` (m): Posición inicial.
    - `velocidad_inicial` (m/s): Velocidad inicial (constante).
- **`posicion(self, tiempo: float) -> float`**:
    Calcula la posición en MRU. Ecuación: `x = x0 + v * t`.
    - `tiempo` (s): Tiempo transcurrido.
- **`velocidad(self) -> float`**:
    Calcula la velocidad en MRU (es constante). Ecuación: `v = v0`.
- **`graficar(self, t_max: float, num_points: int = 100)`**:
    Genera gráficos de posición vs. tiempo y velocidad vs. tiempo.

#### `MovimientoRectilineoUniformementeVariado` (MRUV)

Clase para calcular posición, velocidad y aceleración en Movimiento Rectilíneo Uniformemente Variado.

- **`__init__(self, posicion_inicial: float = 0.0, velocidad_inicial: float = 0.0, aceleracion_inicial: float = 0.0)`**:
    Inicializa el objeto MRUV.
    - `posicion_inicial` (m): Posición inicial.
    - `velocidad_inicial` (m/s): Velocidad inicial.
    - `aceleracion_inicial` (m/s^2): Aceleración inicial (constante).
- **`posicion(self, tiempo: float) -> float`**:
    Calcula la posición en MRUV. Ecuación: `x = x0 + v0 * t + 0.5 * a * t^2`.
- **`velocidad(self, tiempo: float) -> float`**:
    Calcula la velocidad en MRUV. Ecuación: `v = v0 + a * t`.
- **`aceleracion(self) -> float`**:
    Calcula la aceleración en MRUV (es constante). Ecuación: `a = a0`.
- **`velocidad_sin_tiempo(self, posicion_final: float) -> float`**:
    Calcula la velocidad final sin conocer el tiempo. Ecuación: `v^2 = v0^2 + 2 * a * (x - x0)`.
- **`tiempo_por_posicion(self, posicion_final: float) -> tuple[float, float]`**:
    Calcula el tiempo a partir de la posición final. Resuelve la ecuación cuadrática.
- **`tiempo_por_velocidad(self, velocidad_final: float) -> float`**:
    Calcula el tiempo a partir de la velocidad final. Ecuación: `t = (v - v0) / a`.
- **`desplazamiento_sin_tiempo(self, velocidad_final: float) -> float`**:
    Calcula el desplazamiento sin conocer el tiempo. Ecuación: `delta_x = (v_f^2 - v_0^2) / (2 * a)`.
- **`graficar(self, t_max: float, num_points: int = 100)`**:
    Genera gráficos de posición, velocidad y aceleración vs. tiempo.

### 2. Movimiento Parabólico (`cinetica.parabolico`)

Este módulo simula el movimiento de proyectiles bajo la influencia de la gravedad.

#### `MovimientoParabolicoBase`

Clase base para simular trayectorias en Movimiento Parabólico.

- **`__init__(self, velocidad_inicial: float, angulo_grados: float, gravedad: float = 9.81)`**:
    Inicializa el objeto.
    - `velocidad_inicial` (m/s): Magnitud de la velocidad inicial.
    - `angulo_grados` (grados): Ángulo de lanzamiento (0-90).
    - `gravedad` (m/s^2): Aceleración debido a la gravedad.
- **`posicion(self, tiempo: float) -> tuple[float, float]`**:
    Calcula la posición (x, y) en un tiempo dado.
- **`velocidad(self, tiempo: float) -> tuple[float, float]`**:
    Calcula la velocidad (vx, vy) en un tiempo dado.
- **`graficar(self, t_max: float, num_points: int = 100)`**:
    Genera el gráfico de la trayectoria (y vs. x).

#### `MovimientoParabolicoAnalisis`

Clase para calcular propiedades de análisis en Movimiento Parabólico.

- **`__init__(self, base_movimiento: MovimientoParabolicoBase)`**:
    Inicializa con una instancia de `MovimientoParabolicoBase`.
- **`tiempo_vuelo(self) -> float`**:
    Calcula el tiempo total de vuelo.
- **`altura_maxima(self) -> float`**:
    Calcula la altura máxima alcanzada.
- **`alcance_maximo(self) -> float`**:
    Calcula el alcance horizontal máximo.

### 3. Movimiento Circular (`cinetica.circular`)

Este módulo aborda los movimientos a lo largo de una trayectoria circular.

#### `MovimientoCircularUniforme` (MCU)

Clase para calcular y simular Movimiento Circular Uniforme.

- **`__init__(self, radio: float, posicion_angular_inicial: float = 0.0, velocidad_angular_inicial: float = 0.0)`**:
    Inicializa el objeto MCU.
    - `radio` (m): Radio de la trayectoria.
    - `posicion_angular_inicial` (rad): Posición angular inicial.
    - `velocidad_angular_inicial` (rad/s): Velocidad angular inicial (constante).
- **`posicion_angular(self, tiempo: float) -> float`**:
    Calcula la posición angular. Ecuación: `theta = theta0 + omega * t`.
- **`velocidad_angular(self) -> float`**:
    Calcula la velocidad angular (constante). Ecuación: `omega = omega0`.
- **`velocidad_tangencial(self) -> float`**:
    Calcula la velocidad tangencial. Ecuación: `v = omega * R`.
- **`aceleracion_centripeta(self) -> float`**:
    Calcula la aceleración centrípeta. Ecuación: `ac = omega^2 * R`.
- **`periodo(self) -> float`**:
    Calcula el período. Ecuación: `T = 2 * pi / omega`.
- **`frecuencia(self) -> float`**:
    Calcula la frecuencia. Ecuación: `f = 1 / T`.
- **`graficar(self, t_max: float, num_points: int = 100)`**:
    Genera gráficos de posición angular, velocidad angular, aceleración centrípeta y trayectoria.

#### `MovimientoCircularUniformementeVariado` (MCUV)

Clase para calcular y simular Movimiento Circular Uniformemente Variado.

- **`__init__(self, radio: float, posicion_angular_inicial: float = 0.0, velocidad_angular_inicial: float = 0.0, aceleracion_angular_inicial: float = 0.0)`**:
    Inicializa el objeto MCUV.
    - `radio` (m): Radio de la trayectoria.
    - `posicion_angular_inicial` (rad): Posición angular inicial.
    - `velocidad_angular_inicial` (rad/s): Velocidad angular inicial.
    - `aceleracion_angular_inicial` (rad/s^2): Aceleración angular inicial (constante).
- **`posicion_angular(self, tiempo: float) -> float`**:
    Calcula la posición angular. Ecuación: `theta = theta0 + omega0 * t + 0.5 * alpha * t^2`.
- **`velocidad_angular(self, tiempo: float) -> float`**:
    Calcula la velocidad angular. Ecuación: `omega = omega0 + alpha * t`.
- **`aceleracion_angular(self) -> float`**:
    Calcula la aceleración angular (constante). Ecuación: `alpha = alpha0`.
- **`velocidad_tangencial(self, tiempo: float) -> float`**:
    Calcula la velocidad tangencial. Ecuación: `v = omega * R`.
- **`aceleracion_tangencial(self) -> float`**:
    Calcula la aceleración tangencial. Ecuación: `at = alpha * R`.
- **`aceleracion_centripeta(self, tiempo: float) -> float`**:
    Calcula la aceleración centrípeta. Ecuación: `ac = omega^2 * R`.
- **`aceleracion_total(self, tiempo: float) -> float`**:
    Calcula la magnitud de la aceleración total. Ecuación: `a_total = sqrt(at^2 + ac^2)`.
- **`velocidad_angular_sin_tiempo(self, posicion_angular_final: float) -> float`**:
    Calcula la velocidad angular final sin conocer el tiempo. Ecuación: `omega_f^2 = omega_0^2 + 2 * alpha * (theta_f - theta_0)`.
- **`tiempo_por_posicion_angular(self, posicion_angular_final: float) -> tuple[float, float]`**:
    Calcula el tiempo a partir de la posición angular final.
- **`tiempo_por_velocidad_angular(self, velocidad_angular_final: float) -> float`**:
    Calcula el tiempo a partir de la velocidad angular final.
- **`graficar(self, t_max: float, num_points: int = 100)`**:
    Genera gráficos de posición angular, velocidad angular, aceleración angular, aceleración centrípeta y aceleración total.

### 4. Movimiento Oscilatorio (`cinetica.oscilatorio`)

Este módulo se centra en los movimientos periódicos.

#### `MovimientoArmonicoSimple` (MAS)

Clase para calcular posición, velocidad y aceleración en un Movimiento Armónico Simple.

- **`__init__(self, amplitud, frecuencia_angular, fase_inicial=0)`**:
    Inicializa el objeto MAS.
    - `amplitud` (A): Amplitud del movimiento.
    - `frecuencia_angular` (ω) (rad/s): Frecuencia angular.
    - `fase_inicial` (φ) (rad): Fase inicial.
- **`posicion(self, tiempo)`**:
    Calcula la posición. Ecuación: `x(t) = A * cos(ωt + φ)`.
- **`velocidad(self, tiempo)`**:
    Calcula la velocidad. Ecuación: `v(t) = -A * ω * sen(ωt + φ)`.
- **`aceleracion(self, tiempo)`**:
    Calcula la aceleración. Ecuación: `a(t) = -A * ω^2 * cos(ωt + φ)`.
- **`periodo(self)`**:
    Calcula el período. Ecuación: `T = 2π / ω`.
- **`frecuencia(self)`**:
    Calcula la frecuencia. Ecuación: `f = 1 / T`.
- **`energia_cinetica(self, tiempo, masa)`**:
    Calcula la energía cinética. Ecuación: `Ec = 0.5 * m * v(t)^2`.
- **`energia_potencial(self, tiempo, constante_elastica)`**:
    Calcula la energía potencial elástica. Ecuación: `Ep = 0.5 * k * x(t)^2`.
- **`energia_total(self, masa, constante_elastica)`**:
    Calcula la energía mecánica total. Ecuación: `E = 0.5 * k * A^2`.

#### `MovimientoArmonicoComplejo` (MAC)

Representa un Movimiento Armónico Complejo como la superposición de múltiples Movimientos Armónicos Simples.

- **`__init__(self, mas_components)`**:
    Inicializa el objeto MAC con una lista de diccionarios, cada uno representando un MAS.
    - `mas_components`: Lista de diccionarios con `amplitud`, `frecuencia_angular` y `fase_inicial`.
- **`posicion(self, tiempo)`**:
    Calcula la posición total del objeto en un tiempo dado.
- **`velocidad(self, tiempo)`**:
    Calcula la velocidad total del objeto en un tiempo dado.
- **`aceleracion(self, tiempo)`**:
    Calcula la aceleración total del objeto en un tiempo dado.

### 5. Movimiento Relativo (`cinetica.relativo`)

Este módulo permite calcular velocidades relativas entre objetos.

#### `MovimientoRelativo`

Clase para calcular velocidades relativas entre objetos.

- **`__init__(self)`**:
    Inicializa la clase.
- **`velocidad_relativa(self, velocidad_objeto_a, velocidad_objeto_b)`**:
    Calcula la velocidad de A con respecto a B (`V_A/B = V_A - V_B`).
- **`velocidad_absoluta_a(self, velocidad_relativa_ab, velocidad_objeto_b)`**:
    Calcula la velocidad absoluta de A (`V_A = V_A/B + V_B`).
- **`velocidad_absoluta_b(self, velocidad_objeto_a, velocidad_relativa_ab)`**:
    Calcula la velocidad absoluta de B (`V_B = V_A - V_A/B`).
- **`magnitud_velocidad(self, velocidad_vector)`**:
    Calcula la magnitud de un vector de velocidad.
- **`direccion_velocidad(self, velocidad_vector)`**:
    Calcula la dirección de un vector de velocidad (ángulo para 2D, vector unitario para 3D).

### 6. Movimiento Espacial (`cinetica.espacial`)

Este módulo permite simular y calcular la trayectoria de un objeto en 3D.

#### `MovimientoEspacial`

Clase para simular y calcular la trayectoria de un objeto en 3D utilizando vectores de posición, velocidad y aceleración.

- **`__init__(self, posicion_inicial: np.ndarray = np.array([0.0, 0.0, 0.0]), velocidad_inicial: np.ndarray = np.array([0.0, 0.0, 0.0]), aceleracion_constante: np.ndarray = np.array([0.0, 0.0, 0.0]))`**:
    Inicializa el objeto `MovimientoEspacial`.
    - `posicion_inicial` (np.ndarray): Vector de posición inicial (m).
    - `velocidad_inicial` (np.ndarray): Vector de velocidad inicial (m/s).
    - `aceleracion_constante` (np.ndarray): Vector de aceleración constante (m/s^2).
- **`posicion(self, tiempo: float) -> np.ndarray`**:
    Calcula el vector de posición en un tiempo dado. Ecuación: `r = r0 + v0 * t + 0.5 * a * t^2`.
- **`velocidad(self, tiempo: float) -> np.ndarray`**:
    Calcula el vector de velocidad en un tiempo dado. Ecuación: `v = v0 + a * t`.
- **`aceleracion(self) -> np.ndarray`**:
    Retorna el vector de aceleración (es constante). Ecuación: `a = a_constante`.
- **`magnitud_velocidad(self, tiempo: float) -> float`**:
    Calcula la magnitud de la velocidad en un tiempo dado.
- **`magnitud_aceleracion(self) -> float`**:
    Calcula la magnitud de la aceleración.

## Uso Básico

Para utilizar la librería, simplemente importa las clases necesarias y crea instancias de ellas para realizar cálculos o simulaciones.

```python
from cinetica.rectilineo import MovimientoRectilineoUniforme
from cinetica.parabolico import MovimientoParabolicoBase, MovimientoParabolicoAnalisis
from cinetica.espacial import MovimientoEspacial
import numpy as np

# Ejemplo de MRU
mru = MovimientoRectilineoUniforme(posicion_inicial=10, velocidad_inicial=2)
pos = mru.posicion(tiempo=5)
print(f"Posición en MRU: {pos} m")

# Ejemplo de Movimiento Parabólico
mp_base = MovimientoParabolicoBase(velocidad_inicial=30, angulo_grados=45)
mp_analisis = MovimientoParabolicoAnalisis(mp_base)
tiempo_vuelo = mp_analisis.tiempo_vuelo()
print(f"Tiempo de vuelo: {tiempo_vuelo} s")

# Ejemplo de Movimiento Espacial
me = MovimientoEspacial(posicion_inicial=np.array([0,0,0]), velocidad_inicial=np.array([1,2,3]), aceleracion_constante=np.array([0,0,-9.81]))
pos_espacial = me.posicion(tiempo=2)
print(f"Posición espacial a los 2s: {pos_espacial}")
vel_espacial = me.velocidad(tiempo=2)
print(f"Velocidad espacial a los 2s: {vel_espacial}")
