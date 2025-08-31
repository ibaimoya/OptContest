# Algoritmos de Búsqueda Local: Mejor y Primer Mejor.

from ..core.config import PUNTO, CIAN, AMARILLO, VERDE, ROJO, MAGENTA,RESET, BUS_LOC
from ..core.ui import imprimirASCII, imprimirBarra, imprimirResultados
from ..core.io_utils import solicitarEntradaNumerica
from ..core.costs import crearMatrizDeCostes, obtenerCostePromedio, obtenerCosteMaximo
from ..core.config import np
import time
import sys

def generadorDeVecinos(solucion):
    # Genera vecinos por intercambio.
    tam = len(solucion)
    for i in range(tam - 1):
        for j in range(i + 1, tam):
            vecino = solucion.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]
            yield vecino

def algoritmoDelMejor(solucionActual, costePromedioActual, datos, limiteTiempo):
    # Explora todo el vecindario quedándose con el mejor.
    mejorCostePromedio = costePromedioActual
    mejorSolucion = solucionActual
    tiempoInicio = time.time()
    tiempoFin = tiempoInicio + limiteTiempo
    while time.time() < tiempoFin:
        for vecino in generadorDeVecinos(mejorSolucion):
            if time.time() < tiempoFin:
                costePromedioVecino = obtenerCostePromedio(datos, vecino)
                if costePromedioVecino <= mejorCostePromedio:
                    mejorSolucion, mejorCostePromedio = vecino, costePromedioVecino
            else:
                return mejorSolucion + 1, mejorCostePromedio
            tiempoTranscurrido = time.time() - tiempoInicio
            imprimirBarra(tiempoTranscurrido, limiteTiempo)
    return mejorSolucion + 1, mejorCostePromedio

def algoritmoDelPrimerMejor(solucionActual, costePromedioActual, datos, limiteTiempo):
    # Acepta la primera mejora encontrada.
    tiempoInicio = time.time()
    tiempoFin = tiempoInicio + limiteTiempo
    mejorSolucion = solucionActual
    mejorCostePromedio = costePromedioActual
    while time.time() < tiempoFin:
        costePromedioObjetivo = mejorCostePromedio
        for vecino in generadorDeVecinos(mejorSolucion):
            costePromedioVecino = obtenerCostePromedio(datos, vecino)
            if costePromedioVecino < mejorCostePromedio:
                mejorSolucion, mejorCostePromedio = vecino, costePromedioVecino
            tiempoTranscurrido = time.time() - tiempoInicio
            imprimirBarra(tiempoTranscurrido, limiteTiempo)
        if costePromedioObjetivo == mejorCostePromedio:
            break
    imprimirBarra(limiteTiempo, limiteTiempo)
    return mejorSolucion + 1, mejorCostePromedio

def ejecutarAlgoritmoBusquedaLocal(datos, tipo, solucionInicial = None) -> None:
    # Ejecuta la variante de búsqueda local indicada.
    imprimirASCII()
    tiempoLimite = solicitarEntradaNumerica(
        PUNTO + CIAN + "Introduce el número de segundos: " + RESET,
        int,
        lambda x: x >= 0
    )
    imprimirASCII()
    if solucionInicial is None:
        solucionInicial = np.random.permutation(len(datos))
    # Corrige el coste inicial usando los datos originales.
    solCostePromedioInicial = obtenerCostePromedio(datos, solucionInicial)
    if tipo == "mejor":
        print(PUNTO + CIAN + "El algoritmo se ejecutará durante " + AMARILLO + str(tiempoLimite) + CIAN + " segundos." + RESET)
        mejorSolucion, mejorCoste = algoritmoDelMejor(solucionInicial, solCostePromedioInicial, datos, tiempoLimite)
    elif tipo == "primer":
        print(PUNTO + CIAN + "El algoritmo se ejecutará durante como máximo " + AMARILLO + str(tiempoLimite) + CIAN + " segundos." + RESET)
        mejorSolucion, mejorCoste = algoritmoDelPrimerMejor(solucionInicial, solCostePromedioInicial, datos, tiempoLimite)
    else:
        sys.stderr.write(ROJO + "Algoritmo de búsqueda local no válido.\n" + RESET + "\n")
        return
    mejorCosteMaximo = obtenerCosteMaximo(crearMatrizDeCostes(datos, mejorSolucion - 1))
    imprimirResultados(mejorSolucion, mejorCoste, mejorCosteMaximo)

def mejorarConBúsquedaLocal(solucionInicial, datos):
    # Ofrece mejorar una solución mediante búsqueda local.
    confirmaciones = ["y", "yes", "s", "si", "sí"]
    negaciones = ["n", "no"]
    mensaje = PUNTO + CIAN + "¿Quieres mejorar el resultado mediante una búsqueda local? (" + VERDE + "y" + CIAN + "/" + ROJO + "n" + CIAN + ")  " + RESET
    print("\n", end="")
    decisionTomada = False
    while not decisionTomada:
        try:
            decision = input(mensaje).lower()
        except (EOFError, KeyboardInterrupt):
            print("\n" + ROJO + "Entrada interrumpida." + RESET)
            return
        if decision in confirmaciones or decision in negaciones:
            decisionTomada = True
        else:
            print(ROJO + "Opción no válida. Por favor, responde con \"Sí\" o con \"No\"." + RESET)

    if decision in confirmaciones:
        intento = 0
        algoritmoElegido = False
        while not algoritmoElegido:
            imprimirASCII()
            if intento > 0:
                sys.stderr.write(ROJO + "La opción elegida no existe.\n" + RESET)
            print(
                PUNTO + CIAN + "Listado de algoritmos de búsqueda local:\n" + RESET +
                MAGENTA + "\t[0] " + CIAN + "Volver al menú principal.\n" +
                MAGENTA + "\t[1] " + CIAN + BUS_LOC + " del Mejor.\n" +
                MAGENTA + "\t[2] " + CIAN + BUS_LOC + " del Primer Mejor.\n"
            )
            opcion = input(PUNTO + CIAN + "Selecciona el algoritmo para resolver el problema: " + RESET)
            if opcion == "0":
                return
            elif opcion == "1":
                print(CIAN + "Has elegido el algoritmo de Búsqueda Local del Mejor." + RESET)
                ejecutarAlgoritmoBusquedaLocal(datos, "mejor", solucionInicial)
                algoritmoElegido = True
            elif opcion == "2":
                print(CIAN + "Has elegido el algoritmo de Búsqueda Local del Primer Mejor." + RESET)
                ejecutarAlgoritmoBusquedaLocal(datos, "primer", solucionInicial)
                algoritmoElegido = True
            else:
                intento += 1
