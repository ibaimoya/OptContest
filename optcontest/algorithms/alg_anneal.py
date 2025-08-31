# Recocido Simulado.

from ..core.config import PUNTO, CIAN, AMARILLO, ROJO, RESET
from ..core.ui import imprimirASCII, imprimirResultados, imprimirBarra
from ..core.io_utils import solicitarEntradaNumerica
from ..core.costs import crearMatrizDeCostes, obtenerCostePromedio, obtenerCosteMaximo
from ..core.config import np
import warnings
import copy
import time
import sys

def obtenerVecinoAleatorio(solucion):
    # Intercambia dos posiciones aleatorias.
    copia = copy.deepcopy(solucion)
    i, j = np.random.choice(len(copia), 2, replace=False)
    copia[i], copia[j] = copia[j], copia[i]
    return copia

def aceptarCambio(solucionInicial, cosPromedSolInicial, nuevaSolucion, temperatura, datos):
    # Decide si acepta el cambio en función de T.
    pre = cosPromedSolInicial
    post = obtenerCostePromedio(datos, nuevaSolucion)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        probAceptacion = np.exp((-(post - pre) / temperatura))
        if w and issubclass(w[-1].category, RuntimeWarning):
            sys.stderr.write("\n" + PUNTO + AMARILLO + "ADVERTENCIA: Temperatura demasiado baja, posible desbordamiento de pila.\n" + RESET)
    if post < pre:
        return nuevaSolucion, post
    elif np.random.random() < probAceptacion:
        return nuevaSolucion, post
    else:
        return solucionInicial, pre

def recocidoSimulado(intentos, factorTempInicial, alpha, solucionActual, tiempoLimite, datos):
    # Ejecuta el recocido simulado durante un tiempo.
    tiempoInicio = time.time()
    tiempoFin = tiempoInicio + tiempoLimite - 0.1
    costePromedioActual = obtenerCostePromedio(datos, solucionActual)
    temperatura = factorTempInicial
    while time.time() < tiempoFin:
        tiempoTranscurrido = time.time() - tiempoInicio
        imprimirBarra(tiempoTranscurrido, tiempoLimite)
        for _ in range(intentos):
            vecino = obtenerVecinoAleatorio(solucionActual)
            solucionActual, costePromedioActual = aceptarCambio(solucionActual, costePromedioActual, vecino, temperatura, datos)
        nuevaTemperatura = temperatura * alpha / 100
        if temperatura - nuevaTemperatura > 0.1:
            temperatura -= nuevaTemperatura
    return solucionActual + 1, costePromedioActual

def ejecutarRecocidoSimulado(datos) -> None:
    # Pide parámetros, ejecuta y muestra resultados.
    imprimirASCII()
    intentos = solicitarEntradaNumerica(
        PUNTO + CIAN + "Introduce el número de intentos por iteración: " + RESET,
        int,
        lambda x: x >= 0
    )
    factorTempInicial = solicitarEntradaNumerica(
        PUNTO + CIAN + "Introduce el factor de temperatura inicial: " + RESET,
        float,
        lambda x: x > 0
    )
    alpha = solicitarEntradaNumerica(
        PUNTO + CIAN + "Introduce el valor de alpha " + AMARILLO + "(0 < alpha < 100)" + CIAN + ": " + RESET,
        float,
        lambda x: 0 < x < 100
    )
    tiempoLimite = solicitarEntradaNumerica(
        PUNTO + CIAN + "Introduce el tiempo límite en segundos: " + RESET,
        int,
        lambda x: x > 0
    )
    imprimirASCII()
    print(PUNTO + CIAN + "El algoritmo se ejecutará durante " + AMARILLO + str(tiempoLimite) + CIAN + " segundos." + RESET)
    print(PUNTO + CIAN + "Número de intentos por iteración: " + RESET + str(intentos))
    print(PUNTO + CIAN + "Factor de temperatura inicial: " + RESET + str(factorTempInicial))
    print(PUNTO + CIAN + "Valor de alpha: " + RESET + str(alpha))
    solucionInicial = np.random.permutation(len(datos))
    mejorSolucion, mejorCostePromedio = recocidoSimulado(intentos, factorTempInicial, alpha, solucionInicial, tiempoLimite, datos)
    mejorCosteMaximo = obtenerCosteMaximo(crearMatrizDeCostes(datos, mejorSolucion - 1))
    imprimirResultados(mejorSolucion, mejorCostePromedio, mejorCosteMaximo)
    from ..algorithms.alg_local import mejorarConBúsquedaLocal
    mejorarConBúsquedaLocal(mejorSolucion - 1, datos)
