# Documentación de la Librería Cinetica

`Cinetica` es una librería de Python diseñada para simular y analizar diversos tipos de movimiento en física. Proporciona clases y funciones para calcular posiciones, velocidades, aceleraciones y otras propiedades cinemáticas para movimientos rectilíneos, parabólicos, circulares, oscilatorios y relativos.

## Estructura de la Librería

La librería se organiza en paquetes y módulos, reflejando una estructura más modular:

- `cinematica`: Contiene todos los módulos relacionados con la cinemática.
  - `circular`: Movimiento Circular Uniforme y Movimiento Circular Uniformemente Variado.
  - `espacial`: Movimiento en 3D con vectores de posición, velocidad y aceleración.
  - `oscilatorio`: Movimiento Armónico Simple y Movimiento Armónico Complejo.
  - `parabolico`: Movimiento Parabólico (Base y Análisis).
  - `rectilineo`: Movimiento Rectilíneo Uniforme y Movimiento Rectilíneo Uniformemente Variado.
  - `relativo`: Cálculo de velocidades relativas.
- `dinamica`: Módulos completos para análisis dinámico incluyendo fuerzas, trabajo, energía y colisiones.
- `graficos`: Funciones para la visualización de los movimientos.

## Módulo de Choques y Colisiones

El módulo `ChoquesColisiones` proporciona herramientas para analizar diferentes tipos de colisiones en sistemas físicos.

### Características Principales

- **Colisiones Unidimensionales**: Cálculo de velocidades finales en colisiones 1D.
- **Colisiones Bidimensionales**: Análisis de colisiones 2D con ángulos de impacto.
- **Colisiones Tridimensionales**: Soporte para colisiones en el espacio 3D.
- **Coeficiente de Restitución**: Cálculo del coeficiente de restitución a partir de velocidades.
- **Pérdida de Energía**: Cálculo de la energía cinética perdida durante la colisión.
- **Soporte de Unidades**: Integración completa con Pint para manejo de unidades.

### Ejemplo Básico

```python
from cinetica.dinamica import ChoquesColisiones

# Crear una instancia del módulo de choques
choques = ChoquesColisiones()

# Colisión unidimensional elástica
v1f, v2f = choques.colision_unidimensional(
    m1=2.0, v1i=3.0,  # kg, m/s
    m2=5.0, v2i=-1.0,  # kg, m/s
    coeficiente_restitucion=1.0
)

print(f"Velocidades finales: v1f={v1f:.2f} m/s, v2f={v2f:.2f} m/s")
```

### Métodos Principales

- **`colision_unidimensional(m1, v1i, m2, v2i, coeficiente_restitucion, unidades=None)`**:
  - Calcula las velocidades finales en una colisión unidimensional.
  - Parámetros:
    - `m1`, `m2`: Masas de los objetos (kg).
    - `v1i`, `v2i`: Velocidades iniciales (m/s).
    - `coeficiente_restitucion`: Valor entre 0 (inelástico) y 1 (elástico).
    - `unidades`: Diccionario opcional para especificar unidades personalizadas.

- **`colision_bidimensional(m1, v1i, m2, v2i, angulo_impacto, coeficiente_restitucion, unidades=None)`**:
  - Analiza una colisión bidimensional con ángulo de impacto.
  - `v1i`, `v2i` deben ser listas o arrays [vx, vy].

- **`colision_tridimensional(m1, v1i, m2, v2i, normal_impacto, coeficiente_restitucion, unidades=None)`**:
  - Analiza una colisión tridimensional con vector normal de impacto.
  - `v1i`, `v2i`, `normal_impacto` deben ser listas o arrays [x, y, z].

- **`coeficiente_restitucion(v1i, v2i, v1f, v2f, unidades=None)`**:
  - Calcula el coeficiente de restitución a partir de las velocidades.

- **`energia_cinetica_perdida(m1, v1i, m2, v2i, v1f=None, v2f=None, coeficiente_restitucion=None, unidades=None)`**:
  - Calcula la energía cinética perdida durante la colisión.

### Ejemplo Avanzado

```python
import numpy as np
from cinetica.dinamica import ChoquesColisiones

choques = ChoquesColisiones()

# Colisión bidimensional
v1f, v2f = choques.colision_bidimensional(
    m1=2.0, v1i=[3.0, 2.0],
    m2=4.0, v2i=[-1.0, 0.0],
    angulo_impacto=np.pi/4,  # 45 grados
    coeficiente_restitucion=0.8
)

print(f"Velocidad final 1: {v1f}")
print(f"Velocidad final 2: {v2f}")
```

## Sistema de Configuración

Cinetica incluye un sistema de configuración centralizado que permite personalizar el comportamiento de la biblioteca. La configuración se puede establecer a través de variables de entorno o un archivo `.env` en el directorio raíz del proyecto.

### Configuración Básica

La configuración se carga automáticamente al importar el módulo `cinetica`:

```python
from cinetica import config

# Acceder a la configuración
print(f"Nivel de log: {config.logging.level}")
print(f"Workers máximos: {config.performance.max_workers}")
```

### Variables de Entorno

Puedes configurar la aplicación usando variables de entorno con el prefijo `CINETICA_` o directamente con los nombres de las opciones:

```bash
# Ejemplo de configuración con variables de entorno
export ENV=development
export LOGGING__LEVEL=DEBUG
export PERFORMANCE__MAX_WORKERS=8
```

### Archivo .env

Crea un archivo `.env` en el directorio raíz de tu proyecto:

```ini
# .env
ENV=development
LOG_LEVEL=DEBUG
LOG_FILE=logs/cinetica.log
MAX_WORKERS=8
CACHE_ENABLED=true
```

### Opciones de Configuración

#### Configuración General
- `ENV`: Entorno de ejecución (`development`, `testing`, `production`)
- `DEBUG`: Modo de depuración (booleano)
- `TESTING`: Modo de pruebas (booleano)

#### Configuración de Logging
- `LOG_LEVEL`: Nivel de log (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
- `LOG_FILE`: Ruta del archivo de log (opcional)
- `LOG_FORMAT`: Formato de los mensajes de log
- `LOG_DATE_FORMAT`: Formato de fecha en los logs

#### Configuración de Rendimiento
- `MAX_WORKERS`: Número máximo de workers para operaciones paralelas
- `CACHE_ENABLED`: Habilitar caché (booleano)
- `CACHE_TTL`: Tiempo de vida de la caché en segundos

### Uso Avanzado

Puedes sobrescribir la configuración en tiempo de ejecución:

```python
from cinetica.config import settings

# Modificar configuración
settings.logging.level = "DEBUG"
settings.performance.max_workers = 4

# Recargar configuración
settings = settings.model_validate(settings.model_dump())
```

## Sistema de Unidades con `pint`

La librería `Cinetica` ahora integra `pint` para un manejo robusto de unidades en los cálculos físicos. Esto permite definir cantidades con unidades y asegura la consistencia dimensional en las operaciones.

### Uso Básico de Unidades

Para utilizar el sistema de unidades, importa `ureg` (Unit Registry) y `Q_` (Quantity) desde `cinetica.units`.

```python
from cinetica.units import ureg, Q_

# Definir cantidades con unidades
longitud = 10 * ureg.meter
tiempo = 5 * ureg.second
velocidad = 20 * ureg.meter / ureg.second

# Realizar operaciones con unidades
distancia_recorrida = velocidad * tiempo
print(f"Distancia recorrida: {distancia_recorrida}") # Output: 100 meter

# Conversión de unidades
distancia_en_kilometros = distancia_recorrida.to(ureg.kilometer)
print(f"Distancia en kilómetros: {distancia_en_kilometros}") # Output: 0.1 kilometer
```

### Integración en Módulos

Los módulos de `Cinetica` que han sido actualizados para usar `pint` ahora aceptan y retornan objetos `pint.Quantity`. Por ejemplo, en `MovimientoRectilineoUniforme`:

```python
from cinetica.cinematica.rectilineo import MovimientoRectilineoUniforme
from cinetica.units import ureg

# Crear una instancia con cantidades y unidades
mru = MovimientoRectilineoUniforme(posicion_inicial=10 * ureg.meter, velocidad_inicial=5 * ureg.meter / ureg.second)

# Calcular posición con un tiempo con unidades
posicion_final = mru.posicion(2 * ureg.second)
print(f"Posición final: {posicion_final}") # Output: 20 meter

# También se pueden pasar valores sin unidades (se asumirán las unidades base por defecto)
mru_sin_unidades = MovimientoRectilineoUniforme(posicion_inicial=10, velocidad_inicial=5)
posicion_final_sin_unidades = mru_sin_unidades.posicion(2)
print(f"Posición final (sin unidades): {posicion_final_sin_unidades}") # Output: 20 meter
```

## Módulos y Clases

### 1. Movimiento Rectilíneo (`cinetica.cinematica.rectilineo`)

Este módulo maneja los movimientos en una sola dimensión con velocidad constante o aceleración constante.

#### `MovimientoRectilineoUniforme`

Clase para calcular posición y velocidad en Movimiento Rectilíneo Uniforme.

- **`__init__(self, posicion_inicial: float = 0.0, velocidad_inicial: float = 0.0)`**:
    Inicializa el objeto Movimiento Rectilíneo Uniforme.
    - `posicion_inicial` (m): Posición inicial.
    - `velocidad_inicial` (m/s): Velocidad inicial (constante).
- **`posicion(self, tiempo: float) -> float`**:
    Calcula la posición en Movimiento Rectilíneo Uniforme. Ecuación: `x = x0 + v * t`.
    - `tiempo` (s): Tiempo transcurrido.
- **`velocidad(self) -> float`**:
    Calcula la velocidad en Movimiento Rectilíneo Uniforme (es constante). Ecuación: `v = v0`.
- **`graficar(self, t_max: float, num_points: int = 100)`**:
    Genera gráficos de posición vs. tiempo y velocidad vs. tiempo para Movimiento Rectilíneo Uniforme.

#### `MovimientoRectilineoUniformementeVariado`

Clase para calcular posición, velocidad y aceleración en Movimiento Rectilíneo Uniformemente Variado.

- **`__init__(self, posicion_inicial: float = 0.0, velocidad_inicial: float = 0.0, aceleracion_inicial: float = 0.0)`**:
    Inicializa el objeto Movimiento Rectilíneo Uniformemente Variado.
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

### 2. Movimiento Parabólico (`cinetica.cinematica.parabolico`)

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

### 3. Movimiento Circular (`cinetica.cinematica.circular`)

Este módulo aborda los movimientos a lo largo de una trayectoria circular.

#### `MovimientoCircularUniforme`

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

#### `MovimientoCircularUniformementeVariado`

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

### 4. Movimiento Oscilatorio (`cinetica.cinematica.oscilatorio`)

Este módulo se centra en los movimientos periódicos.

#### `MovimientoArmonicoSimple`

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

#### `MovimientoArmonicoComplejo`

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

### 5. Movimiento Relativo (`cinetica.cinematica.relativo`)

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

### 6. Movimiento Espacial (`cinetica.cinematica.espacial`)

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
- **`graficar(self, t_max: float, num_points: int = 100)`**:
    Genera y muestra un gráfico 3D de la trayectoria.

## Uso Básico

Para utilizar la librería, simplemente importa las clases necesarias y crea instancias de ellas para realizar cálculos o simulaciones.

```python
from cinetica.cinematica.rectilineo import MovimientoRectilineoUniforme
from cinetica.cinematica.parabolico import MovimientoParabolicoBase, MovimientoParabolicoAnalisis
from cinetica.cinematica.espacial import MovimientoEspacial
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
```

## Módulo de Sistemas de Partículas (`cinetica.dinamica.SistemasParticulas`)

El módulo `SistemasParticulas` proporciona herramientas para analizar sistemas de partículas, incluyendo el cálculo de centros de masa, momentos de inercia, teoremas fundamentales, energía cinética rotacional y momento angular.

### Características principales

- Cálculo del centro de masa de un sistema de partículas
- Cálculo del momento de inercia para partículas individuales y sistemas
- Aplicación del teorema de Steiner (ejes paralelos)
- Cálculo de la energía cinética rotacional
- Cálculo del momento angular
- Soporte completo para unidades mediante Pint

### Ejemplo de uso

```python
from cinetica.dinamica import SistemasParticulas
import numpy as np

# Crear instancia
sp = SistemasParticulas()

# Definir un sistema de partículas
masas = [1.0, 2.0, 3.0]  # kg
posiciones = [
    [0.0, 0.0, 0.0],  # m
    [2.0, 0.0, 0.0],  # m
    [2.0, 3.0, 0.0]   # m
]

# Calcular centro de masa
centro_masa = sp.centro_masa(masas, posiciones)

# Calcular momento de inercia con respecto al eje z
I_z = sp.momento_inercia_sistema(masas, posiciones, eje=[0, 0, 1])

# Calcular energía cinética rotacional (2 rad/s)
omega = 2.0  # rad/s
K_rot = sp.energia_cinetica_rotacional(I_z, omega)

# Calcular momento angular
L = sp.momento_angular(I_z, omega)
```

### Métodos principales

- **`centro_masa(masas, posiciones, unidades=None)`**:
  Calcula el centro de masa de un sistema de partículas.
  - `masas`: Lista de masas de las partículas
  - `posiciones`: Lista de vectores de posición [x, y, z] de cada partícula
  - `unidades`: Diccionario opcional con unidades (ej: `{'masa': 'kg', 'longitud': 'm'}`)
  - Retorna: Vector de posición del centro de masa [x_cm, y_cm, z_cm]

- **`momento_inercia_particula(masa, posicion, eje=None, unidades=None)`**:
  Calcula el momento de inercia de una partícula con respecto a un eje.
  - `masa`: Masa de la partícula
  - `posicion`: Vector de posición [x, y, z] de la partícula
  - `eje`: Vector unitario que define la dirección del eje (si es None, se usa el origen)
  - `unidades`: Diccionario opcional con unidades
  - Retorna: Momento de inercia (escalar)

- **`momento_inercia_sistema(masas, posiciones, eje=None, unidades=None)`**:
  Calcula el momento de inercia de un sistema de partículas con respecto a un eje.
  - `masas`: Lista de masas de las partículas
  - `posiciones`: Lista de vectores de posición [x, y, z] de cada partícula
  - `eje`: Vector unitario que define la dirección del eje (si es None, se usa el origen)
  - `unidades`: Diccionario opcional con unidades
  - Retorna: Momento de inercia total del sistema

- **`teorema_steiner(I_cm, masa_total, distancia, unidades=None)`**:
  Aplica el teorema de Steiner (teorema de los ejes paralelos).
  - `I_cm`: Momento de inercia con respecto al centro de masa
  - `masa_total`: Masa total del sistema
  - `distancia`: Distancia entre los dos ejes paralelos
  - `unidades`: Diccionario opcional con unidades
  - Retorna: Momento de inercia con respecto al nuevo eje

- **`energia_cinetica_rotacional(momento_inercia, velocidad_angular, unidades=None)`**:
  Calcula la energía cinética rotacional.
  - `momento_inercia`: Momento de inercia del sistema
  - `velocidad_angular`: Velocidad angular (magnitud escalar)
  - `unidades`: Diccionario opcional con unidades
  - Retorna: Energía cinética rotacional

- **`momento_angular(momento_inercia, velocidad_angular, unidades=None)`**:
  Calcula el momento angular.
  - `momento_inercia`: Momento de inercia del sistema
  - `velocidad_angular`: Velocidad angular (magnitud escalar)
  - `unidades`: Diccionario opcional con unidades
  - Retorna: Momento angular

## Módulo de Dinámica (`cinetica.dinamica`)

El módulo de dinámica proporciona herramientas completas para el análisis de fuerzas, trabajo y energía en sistemas mecánicos.

### 7. Leyes de Newton (`cinetica.dinamica.newton`)

#### `LeyesNewton`

Clase para implementar las leyes de Newton y cálculos relacionados con fuerzas y aceleración.

- **`__init__(self)`**: Inicializa una instancia de LeyesNewton.
- **`segunda_ley(self, masa=None, aceleracion=None, fuerza=None)`**:
    Implementa la segunda ley de Newton (F = ma) con cálculo flexible de cualquier parámetro.
    - Proporciona exactamente dos de los tres parámetros para calcular el tercero.
    - Soporta valores escalares y vectoriales (numpy arrays).
    - Maneja unidades automáticamente con pint.
- **`fuerza_neta(self, fuerzas)`**:
    Calcula la fuerza neta de múltiples fuerzas.
    - Acepta lista de fuerzas escalares o vectoriales.
    - Retorna la suma vectorial de todas las fuerzas.
- **`equilibrio(self, fuerzas, tolerancia=1e-10)`**:
    Verifica si un sistema está en equilibrio.
    - Retorna True si la fuerza neta es menor que la tolerancia.
- **`peso(self, masa, gravedad=9.81)`**:
    Calcula el peso de un objeto.
    - Ecuación: W = m * g
- **`fuerza_centripeta(self, masa, velocidad, radio)`**:
    Calcula la fuerza centrípeta.
    - Ecuación: Fc = m * v² / r

### 8. Análisis de Fuerzas (`cinetica.dinamica.fuerzas`)

#### `AnalisisFuerzas`

Clase para análisis completo de diferentes tipos de fuerzas en sistemas físicos.

- **`__init__(self)`**: Inicializa una instancia de AnalisisFuerzas.
- **`friccion_estatica(self, normal, coeficiente)`**:
    Calcula la fuerza de fricción estática máxima.
    - Ecuación: fs = μs * N
- **`friccion_cinetica(self, normal, coeficiente)`**:
    Calcula la fuerza de fricción cinética.
    - Ecuación: fk = μk * N
- **`fuerza_elastica(self, constante, deformacion)`**:
    Calcula la fuerza elástica según la ley de Hooke.
    - Ecuación: Fe = k * x
- **`fuerza_gravitacional(self, masa1, masa2, distancia, G=6.67430e-11)`**:
    Calcula la fuerza gravitacional entre dos masas.
    - Ecuación: Fg = G * m1 * m2 / r²
- **`descomponer_fuerza(self, magnitud, angulo)`**:
    Descompone una fuerza en componentes rectangulares.
    - Retorna (Fx, Fy) donde Fx = F*cos(θ), Fy = F*sen(θ)
- **`magnitud_y_direccion(self, Fx, Fy)`**:
    Calcula magnitud y dirección desde componentes.
    - Retorna (magnitud, ángulo)
- **`plano_inclinado(self, peso, angulo)`**:
    Descompone el peso en un plano inclinado.
    - Retorna (componente_paralela, componente_perpendicular)
- **`tension_cuerda(self, masa, aceleracion=0, angulo=0, gravedad=9.81)`**:
    Calcula la tensión en una cuerda.
    - Considera aceleración del sistema y ángulo con la vertical.

### 9. Trabajo y Energía (`cinetica.dinamica.trabajo_energia`)

#### `TrabajoEnergia`

Clase para cálculos de trabajo, energía y potencia en sistemas mecánicos.

- **`__init__(self)`**: Inicializa una instancia de TrabajoEnergia.
- **`trabajo_fuerza_constante(self, fuerza, desplazamiento, angulo=0)`**:
    Calcula el trabajo realizado por una fuerza constante.
    - Ecuación: W = F * d * cos(θ)
- **`trabajo_vectorial(self, fuerza, desplazamiento)`**:
    Calcula el trabajo usando el producto punto de vectores.
    - Ecuación: W = F⃗ · d⃗
- **`energia_cinetica(self, masa, velocidad)`**:
    Calcula la energía cinética.
    - Ecuación: Ec = ½ * m * v²
- **`energia_potencial_gravitacional(self, masa, altura, gravedad=9.81)`**:
    Calcula la energía potencial gravitacional.
    - Ecuación: Ep = m * g * h
- **`energia_potencial_elastica(self, constante, deformacion)`**:
    Calcula la energía potencial elástica.
    - Ecuación: Ep = ½ * k * x²
- **`energia_mecanica_total(self, energia_cinetica, energia_potencial)`**:
    Calcula la energía mecánica total.
    - Ecuación: Em = Ec + Ep
- **`teorema_trabajo_energia(self, masa, velocidad_inicial, velocidad_final)`**:
    Aplica el teorema trabajo-energía.
    - Ecuación: Wneto = ΔEc = Ecf - Eci
- **`potencia(self, trabajo, tiempo)`**:
    Calcula la potencia promedio.
    - Ecuación: P = W / t
- **`potencia_instantanea(self, fuerza, velocidad)`**:
    Calcula la potencia instantánea.
    - Ecuación: P = F * v

### Ejemplo de Uso del Módulo de Dinámica

```python
from cinetica.dinamica import LeyesNewton, AnalisisFuerzas, TrabajoEnergia
import math

# Leyes de Newton
newton = LeyesNewton()
fuerza = newton.segunda_ley(masa=10, aceleracion=5)  # F = 50 N
print(f"Fuerza: {fuerza}")

# Análisis de fuerzas
fuerzas = AnalisisFuerzas()
f_friccion = fuerzas.friccion_cinetica(normal=200, coeficiente=0.3)  # 60 N
Fx, Fy = fuerzas.descomponer_fuerza(magnitud=100, angulo=math.pi/4)
print(f"Componentes: Fx={Fx:.2f}, Fy={Fy:.2f}")

# Trabajo y energía
te = TrabajoEnergia()
trabajo = te.trabajo_fuerza_constante(fuerza=50, desplazamiento=10)  # 500 J
energia_cinetica = te.energia_cinetica(masa=5, velocidad=10)  # 250 J
print(f"Trabajo: {trabajo}, Energía cinética: {energia_cinetica}")
```
