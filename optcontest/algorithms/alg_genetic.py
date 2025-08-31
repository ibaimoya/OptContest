# Algoritmo Genético.

from ..core.config import PUNTO, CIAN, AMARILLO, RESET, ALG_GEN
from ..core.ui import imprimirASCII, imprimirResultados, imprimirBarra
from ..core.io_utils import solicitarEntradaNumerica
from ..core.costs import crearMatrizDeCostes, obtenerCostePromedio, obtenerCosteMaximo
from ..core.config import np

def inicializarPoblacion(tamSolucion, tamPoblacion, datosProblema):
    # Inicializa población aleatoria y calcula fmed.
    poblacion = []
    poblacionFmeds = []
    mejorSolucion = None
    mejorFmed = np.inf
    for _ in range(tamPoblacion):
        solucion = np.random.permutation(tamSolucion)
        fmedActual = obtenerCostePromedio(datosProblema, solucion)
        poblacion.append(solucion)
        poblacionFmeds.append(fmedActual)
        if fmedActual < mejorFmed:
            mejorFmed = fmedActual
            mejorSolucion = solucion
    return poblacion, poblacionFmeds, mejorSolucion, mejorFmed

def seleccionMediana(poblacion, poblacionFmeds):
    # Selecciona individuos con fmed ≤ mediana.
    fmedMediana = np.median(poblacionFmeds)
    nuevaPoblacion, nuevaPoblacionFmeds = [], []
    for solucion, fmedSolucion in zip(poblacion, poblacionFmeds):
        if fmedSolucion <= fmedMediana:
            nuevaPoblacion.append(solucion)
            nuevaPoblacionFmeds.append(fmedSolucion)
    return nuevaPoblacion, nuevaPoblacionFmeds

def crucePseudoOx(padre1, padre2):
    # Cruce OX parcial.
    i, j = sorted(np.random.choice(range(len(padre1)), 2, replace=False))
    segmento = padre1[i:j]
    restante = padre2[~np.isin(padre2, segmento)]
    hijo = np.concatenate((restante[:i], segmento, restante[i:]))
    return hijo

def mutacionIntercambio(solucion, tasaMutacion, numIntercambios=1):
    # Intercambia posiciones con cierta probabilidad.
    sol = solucion.copy()
    for _ in range(numIntercambios):
        if np.random.randint(100) < tasaMutacion:
            a, b = np.random.choice(len(sol), 2, replace=False)
            sol[a], sol[b] = sol[b], sol[a]
    return sol

def reproduccionOx(poblacion, longitudObjetivo, tamElite, probMutacion):
    # Genera nueva población con elitismo + cruce + mutación.
    nuevaPoblacion = poblacion[:tamElite]
    n = len(poblacion)
    for _ in range(tamElite, longitudObjetivo):
        i1, i2 = np.random.choice(n, 2)
        p1, p2 = poblacion[i1], poblacion[i2]
        hijo = crucePseudoOx(p1, p2)
        hijo = mutacionIntercambio(hijo, probMutacion)
        nuevaPoblacion.append(hijo)
    return nuevaPoblacion

def algoritmoGenetico(datosProblema, poblacion, poblacionFmeds, mejorSolucion, mejorFmed,
                      tiempoLimite=60, tamElite=5, tasaMutacion=10):
    # Ejecuta el AG hasta agotar tiempo.
    import time
    tiempoInicio = time.time()
    tiempoFinal = tiempoInicio + tiempoLimite - 0.5
    tamDiversidad = 0
    while time.time() < tiempoFinal:
        tiempoTranscurrido = time.time() - tiempoInicio
        imprimirBarra(tiempoTranscurrido, tiempoLimite)
        poblacion, poblacionFmeds = seleccionMediana(poblacion, poblacionFmeds)
        longitudObjetivo = len(poblacion) - tamDiversidad
        poblacion = reproduccionOx(poblacion, longitudObjetivo, tamElite, tasaMutacion)
        poblacion.append(mejorSolucion)  # Elitismo.
        poblacionFmeds = []
        for sol in poblacion:
            fmed = obtenerCostePromedio(datosProblema, sol)
            poblacionFmeds.append(fmed)
            if fmed < mejorFmed:
                mejorFmed = fmed
                mejorSolucion = sol
    return mejorSolucion, mejorFmed

def ejecutarAlgoritmoGenetico(datos) -> None:
    # Pide parámetros, ejecuta y muestra resultados.
    imprimirASCII()
    tamPoblacion = solicitarEntradaNumerica(
        PUNTO + CIAN + "Introduce el tamaño de la población: " + RESET,
        int,
        lambda x: x > 0
    )
    tasaDeMutacion = solicitarEntradaNumerica(
        PUNTO + CIAN + "Introduce la tasa de mutación (0-100): " + RESET,
        float,
        lambda x: 0 <= x <= 100
    )
    limiteDeTiempo = solicitarEntradaNumerica(
        PUNTO + CIAN + "Introduce el tiempo límite en segundos: " + RESET,
        int,
        lambda x: x > 0
    )
    imprimirASCII()
    print(PUNTO + CIAN + "El algoritmo se ejecutará durante " + AMARILLO + f"{limiteDeTiempo}" + CIAN + " segundos." + RESET)
    print(PUNTO + CIAN + "Tamaño de la población: " + RESET + f"{tamPoblacion}")
    print(PUNTO + CIAN + "Tasa de mutación (%): " + RESET + f"{tasaDeMutacion}")
    tamSolucion = len(datos)
    poblacion, poblacionFmeds, mejorSolucion, mejorFmed = inicializarPoblacion(tamSolucion, int(tamPoblacion), datos)
    tamElite = 5
    mejorSolucion, mejorCostePromedio = algoritmoGenetico(datos, poblacion, poblacionFmeds, mejorSolucion, mejorFmed,
                                                          int(limiteDeTiempo), tamElite, float(tasaDeMutacion))
    mejorCosteMaximo = obtenerCosteMaximo(crearMatrizDeCostes(datos, mejorSolucion))
    imprimirResultados(mejorSolucion + 1, mejorCostePromedio, mejorCosteMaximo)
    from ..algorithms.alg_local import mejorarConBúsquedaLocal
    mejorarConBúsquedaLocal(mejorSolucion, datos)