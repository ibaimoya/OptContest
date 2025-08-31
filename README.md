<p align="center">
  <img src="./images/banner.png" alt="OptContest — Flow Shop Permutacional (Ibai Moya Aroz)" width="100%" />
</p>

# OptContest
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**OptContest** es una actividad de optimización en el grado de **Ingeniería Informática** (Universidad de Burgos). Se publican unas **instancias** de un problema combinatorio y el alumnado desarrolla **heurísticas** y **metaheurísticas** para obtener buenas soluciones en **tiempo limitado**, con métricas objetivas para comparar resultados. Este proyecto está preparado para ese formato: lee instancias desde un dataset, ejecuta varios algoritmos clásicos y reporta métricas comparables.

---
## Índice

* [El problema del Flow Shop Permutacional](#el-problema-del-flow-shop-permutacional)
* [¿Qué implementa este código?](#qué-implementa-este-código)
* [Parámetros por algoritmo (resumen)](#parámetros-por-algoritmo-resumen)
* [Ejecución](#ejecución)
* [Estructura del código](#estructura-del-código)
  * [Entradas / Salidas](#entradas--salidas)
* [Consejos](#consejos)

---

## El problema del Flow Shop Permutacional

En muchos entornos productivos y de servicios existe una **cadena fija de etapas** por la que deben pasar todos los trabajos: por ejemplo, mecanizado → pulido → inspección, o preimpresión → impresión → encuadernación. Este escenario se modela como *flow shop*: varias **máquinas/etapas** aplicadas en el **mismo orden** a un conjunto de **trabajos/pedidos**. La decisión clave es **en qué orden** lanzar los trabajos para que el sistema rinda mejor.

En la variante **permutacional**, el orden que se decide para entrar en la **primera** máquina se mantiene en **todas** las máquinas. Esto representa líneas donde no es viable reordenar entre etapas (transportadores, buffers pequeños, lotes cerrados). Cada trabajo `i` necesita un tiempo `p[i][j]` en la máquina `j`. Las máquinas procesan **un trabajo a la vez**, los trabajos **no se preemiten** (una vez empiezan en una máquina, terminan) y un trabajo solo puede iniciar en la máquina `j` cuando:

1. Ha terminado en la máquina `j-1`, y
2. La máquina `j` está libre.

Para evaluar un orden concreto (una **permutación**), se construye una **matriz de finalización** `f` que indica el instante de finalización de cada trabajo en cada máquina. La dinámica captura tanto las **colas por recurso** (máquinas ocupadas) como las **esperas por flujo** (el trabajo todavía no llega). Dos métricas útiles son:

* **Makespan (`fmax`)**: el tiempo total hasta completar **todos** los trabajos (última celda de `f`). Resume la duración total del plan.
* **`fmed`**: una media de finalizaciones en la **última máquina**, útil para comparar “suavidad”/rendimiento medio entre instancias.

Encontrar el orden óptimo es **NP-difícil**, por lo que se recurre a **heurísticas** y **metaheurísticas** que logran soluciones de alta calidad en tiempo razonable. Este es precisamente el tipo de reto que encaja con **OptContest**: mismas instancias para todo el mundo, límite temporal y comparación objetiva de resultados.

---

## ¿Qué implementa este código?

* Menú interactivo con **4 algoritmos**: Aleatorio, Búsqueda Local (Mejor/Primer Mejor), Recocido Simulado y Genético.
* Visualización con **barra de progreso** (usa `\r`) y banner ASCII.
* Módulo de **costes** común: matriz de finalización `f`, `fmax` (makespan) y `fmed` (media de la última columna de `f`).

---

## Parámetros por algoritmo (resumen)

* **Aleatorio**: nº de iteraciones.
* **Búsqueda Local**: tiempo (s) y variante (**Mejor** o **Primer Mejor**).
* **Recocido Simulado**: intentos por iteración, **temperatura inicial**, **alpha** (0–100) y tiempo (s).
* **Genético**: tamaño de población, **tasa de mutación** (0–100) y tiempo (s).

---

## Ejecución

1. (Opcional) Instalar dependencias:

```powershell
pip install -r requirements.txt
```

> Si no se instala previamente, el programa intentará instalar `numpy` automáticamente.

2. Ejecutar:

```powershell
python main.py
```

*O bien:*

```powershell
python -m optcontest
```

3. Cuando lo pida, introducir el nombre del fichero de datos, por ejemplo:

```
Doc1.txt
```

> Si no lo encuentra en el directorio actual, el programa lo buscará también en `./dataset/`.



## Estructura del código

```
OtpContest/
├── main.py                     # Lanzador (permite `python main.py`)
├── requirements.txt            # Dependencias externas (numpy)
├── dataset/                    # (Opcional) Instancias de prueba
└── optcontest/
    ├── __init__.py
    ├── __main__.py             # Punto de entrada (`python -m optcontest`)
    ├── core/
    │   ├── config.py           # Colores, UTF-8, constantes, import/instalación de numpy
    │   ├── ui.py               # Banner ASCII, barra de progreso e impresión de resultados
    │   ├── io_utils.py         # Entrada por consola y lectura de fichero (con fallback a ./dataset/)
    │   └── costs.py            # Cálculo de matriz de costes f, fmed y fmax
    └── algorithms/
        ├── alg_random.py       # Búsqueda Aleatoria
        ├── alg_local.py        # Búsqueda Local (Mejor / Primer Mejor)
        ├── alg_anneal.py       # Recocido Simulado
        └── alg_genetic.py      # Algoritmo Genético
```

### Entradas / Salidas

* **Entrada**: fichero de instancia (p. ej., `Doc1.txt`) con tiempos de proceso.
* **Salida**: mejor **secuencia** encontrada (indexada desde **1**), **fmed** (coste promedio acumulado) y **fmax** (makespan).


---

## Consejos

* Consola recomendada en Windows: **Windows Terminal / PowerShell / CMD**.
* Coloca las instancias en el **directorio actual** o en `./dataset/`.
