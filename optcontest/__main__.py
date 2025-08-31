# Punto de entrada y menú principal.

from .core.ui import presentacion, imprimirASCII
from .core.config import PUNTO, CIAN, MAGENTA, RESET, BUS_ALE, BUS_LOC, REC_SIM, ALG_GEN
from .core.io_utils import verificarSalida, procesarFichero, salir

from .algorithms.alg_random import ejecutarAlgoritmoAleatorio
from .algorithms.alg_local import ejecutarAlgoritmoBusquedaLocal
from .algorithms.alg_anneal import ejecutarRecocidoSimulado
from .algorithms.alg_genetic import ejecutarAlgoritmoGenetico

def mostrarMenu(primerIntento = True) -> None:
    # Muestra el menú y delega a la opción.
    imprimirASCII()
    print(PUNTO + CIAN + "Listado de algoritmos:\n" + RESET +
        MAGENTA + "\t[0] " + CIAN + "Salir.\n" +
        MAGENTA + "\t[1] " + CIAN + BUS_ALE + ".\n" +
        MAGENTA + "\t[2] " + CIAN + BUS_LOC + " del Mejor.\n" +
        MAGENTA + "\t[3] " + CIAN + BUS_LOC + " del Primer Mejor.\n" +
        MAGENTA + "\t[4] " + CIAN + REC_SIM + ".\n" +
        MAGENTA + "\t[5] " + CIAN + ALG_GEN + ".\n")
    if not primerIntento:
        import sys
        from .core.config import ERROR, ROJO
        sys.stderr.write(ERROR + ROJO + "La opción elegida no existe.\n" + RESET)
    opcion = input(PUNTO + CIAN + "Selecciona el algoritmo para resolver el problema: " + RESET)
    menu(opcion)

def menu(opcion) -> None:
    # Ejecuta la opción seleccionada.
    opciones = ["1", "2", "3", "4", "5"]
    if opcion == "0" or (opcion is not None and (opcion.lower() == "exit" or opcion.lower() == "salir")):
        salir()
        return
    elif opcion in opciones:
        datos = procesarFichero()
    else:
        mostrarMenu(False)
        return

    if opcion == opciones[0]:  # Aleatorio.
        ejecutarAlgoritmoAleatorio(datos)
    elif opcion == opciones[1]:  # BL Mejor.
        ejecutarAlgoritmoBusquedaLocal(datos, "mejor")
    elif opcion == opciones[2]:  # BL Primer Mejor.
        ejecutarAlgoritmoBusquedaLocal(datos, "primer")
    elif opcion == opciones[3]:  # Recocido Simulado.
        ejecutarRecocidoSimulado(datos)
    elif opcion == opciones[4]:  # Genético.
        ejecutarAlgoritmoGenetico(datos)

def main():
    # Bucle principal.
    from .core.ui import esperarInput
    presentacion()
    while True:
        try:

            mostrarMenu()
            esperarInput()

        except KeyboardInterrupt:
            from .core.config import ERROR, ROJO, RESET
            imprimirASCII()
            import sys
            sys.stderr.write(ERROR + ROJO + "Programa interrumpido.\n" + RESET + "\n")
            raise SystemExit(1)
        
        except Exception as excep:
            from .core.config import ERROR, ROJO, RESET
            imprimirASCII()
            import sys
            sys.stderr.write(ERROR + ROJO + f"Ha ocurrido un error inesperado: {excep}\n" + RESET)
            raise SystemExit(1)