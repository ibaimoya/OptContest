# Algoritmo: Búsqueda Aleatoria.

from ..core.config import PUNTO, CIAN, AMARILLO, RESET
from ..core.config import np
from ..core.ui import imprimirASCII, imprimirResultados, imprimirBarra
from ..core.io_utils import solicitarEntradaNumerica
from ..core.costs import crearMatrizDeCostes, obtenerCostePromedio, obtenerCosteMaximo

def obtenerSolucionAleatoria(tam):
    # Devuelve una permutación aleatoria.
    return np.random.permutation(range(tam))

def algoritmoAleatorio(datos, n_iter):
    # Genera soluciones aleatorias y conserva la mejor.
    mejorSolucion = []
    mejorCostePromedio = np.inf
    for i in range(n_iter):
        imprimirBarra(i, n_iter)
        solucion = obtenerSolucionAleatoria(len(datos))
        solCostePromedio = obtenerCostePromedio(datos, solucion)
        if solCostePromedio < mejorCostePromedio:
            mejorSolucion = solucion
            mejorCostePromedio = solCostePromedio
    return mejorSolucion + 1, mejorCostePromedio

def ejecutarAlgoritmoAleatorio(datos) -> None:
    # Ejecuta el algoritmo y muestra resultados.
    imprimirASCII()
    numIteraciones = solicitarEntradaNumerica(
        PUNTO + CIAN + "Introduce el número de iteraciones: " + RESET,
        int,
        lambda x: x > 0
    )
    imprimirASCII()
    print(PUNTO + CIAN + "Número de iteraciones: " + RESET + str(numIteraciones))
    mejorSolucion, mejorCostePromedio = algoritmoAleatorio(datos, int(numIteraciones))
    mejorCosteMaximo = obtenerCosteMaximo(crearMatrizDeCostes(datos, mejorSolucion - 1))
    imprimirResultados(mejorSolucion, mejorCostePromedio, mejorCosteMaximo)