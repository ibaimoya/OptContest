# Funciones de interfaz y visualización.

from ..core.config import (
    RESET, ROJO, VERDE, AMARILLO, CIAN, MAGENTA,
    PUNTO, LINEA, ERROR, SISTEMA, CLEAR
)
import os
import sys
import threading
import time

def imprimirASCII() -> None:
    # Imprime cabecera ASCII y limpia consola.
    os.system(CLEAR)
    print(LINEA + LINEA)
    print(AMARILLO + (
        "\n                               .,,uod8B8bou,,.\n"
        "                      ..,uod8BBBBBBBBBBBBBBBBRPFT?l!i:.\n"
        "                 ,=m8BBBBBBBBBBBBBBBRPFT?!||||||||||||||\n"
        "                 !...:!TVBBBRPFT||||||||||!!^^\"\"'   ||||\n"
        "                 !.......:!?|||||!!^^\"\"'            ||||\n"
        "                 !.........||||                     ||||\n"
        "                 !.........||||  " + VERDE + "##" + AMARILLO + "                 ||||\n"
        "                 !.........||||                     ||||\n"
        "                 !.........||||                     ||||\n"
        "                 !.........||||                     ||||\n"
        "                 !.........||||                     ||||\n"
        "                 `.........||||                    ,||||\n"
        "                  .;.......||||               _.-!!|||||\n"
        "           .,uodWBBBBb.....||||       _.-!!|||||||||!:'\n"
        "        YBBBBBBBBBBBBBBb..!|||:..-!!|||||||!iof68BBBBBb....\n"
        "        ..YBBBBBBBBBBBBBBb!!||||||||!iof68BBBBBBRPFT?!::   `.\n"
        "        ....YBBBBBBBBBBBBBBbaaitf68BBBBBBRPFT?!:::::::::     `.\n"
        "        ......YBBBBBBBBBBBBBBBBBBBRPFT?!::::::;:!^\"`;:::       `.\n"
        "        ........YBBBBBBBBBBRPFT?!::::::::::::::::::::::::;         iBBbo.\n"
        "        `..........YBRPFT?!::::::::::::::::::::::::;iof68bo.      WBBBBbo.\n"
        "          `..........:::::::::::::::::::::::;iof688888888888b.     `YBBBP^'\n"
        "            `........::::::::::::::::;iof688888888888888888888b.     `\n"
        "              `......:::::::::;iof688888888888888888888888888888b.\n"
        "                `....:::;iof688888888888888888888888888888888899fT!\n"
        "                  `..::!8888888888888888888888888888888899fT|!^\"'\n"
        "                    `' !!988888888888888888888888899fT|!^\"'\n"
        "                        `!!8888888888888888899fT|!^\"'\n"
        "                          `!988888888899fT|!^\"'\n"
        "                            `!9899fT|!^\"'\n"
        "                              `!^\"'\n"
    ) + RESET)
    nombre = "Ibai Moya Aroz"
    hueco = " " * ((len(LINEA) - 12) - (len(nombre) + 2))
    print(MAGENTA + hueco + "by " + nombre + "\n" + LINEA + LINEA)

def presentacion() -> None:
    # Presenta el programa.
    imprimirASCII()
    print(PUNTO + CIAN + "Práctica de Scheduling creada por " + MAGENTA + "Ibai Moya Aroz" + CIAN + " para " + SISTEMA + "."
          +" \n      A continuación se mostrará un listado de algoritmos con los que se puede \n"
          + "      resolver el problema del Flow Shop Permutacional sobre un fichero con el\n"
          + "      formato correspondiente.\n" + RESET)
    print(PUNTO + CIAN + "Para finalizar el programa escribe \"Salir\" o \"Exit\" en cualquier menú." + RESET)
    esperarInput()

def imprimirBarra(iteracionActual, totalIteraciones, longitudBarra=40) -> None:
    # Imprime una barra de progreso con porcentaje.
    try:
        porcentaje = 0 if totalIteraciones == 0 else min((iteracionActual + 1) / totalIteraciones, 1)
    except TypeError:
        porcentaje = 0 if totalIteraciones == 0 else min(iteracionActual / totalIteraciones, 1)
    numCaracteres = int(longitudBarra * porcentaje)
    barraColoreada = ''

    if SISTEMA == 'Windows':
        # Degrada de rojo a verde.
        colorInicio = (255, 0, 0)
        colorFin = (0, 255, 0)
        ratioPorcentaje = porcentaje
        rP = int(colorInicio[0] + (colorFin[0] - colorInicio[0]) * ratioPorcentaje)
        gP = int(colorInicio[1] + (colorFin[1] - colorInicio[1]) * ratioPorcentaje)
        bP = int(colorInicio[2] + (colorFin[2] - colorInicio[2]) * ratioPorcentaje)
        colorCodigoPorcentaje = f'\033[38;2;{rP};{gP};{bP}m'

        for i in range(longitudBarra):
            if i < numCaracteres:
                ratio = 0 if numCaracteres <= 1 else i / numCaracteres
                r = int(colorInicio[0] + (colorFin[0] - colorInicio[0]) * ratio)
                g = int(colorInicio[1] + (colorFin[1] - colorInicio[1]) * ratio)
                b = int(colorInicio[2] + (colorFin[2] - colorInicio[2]) * ratio)
                colorCodigo = f'\033[38;2;{r};{g};{b}m'
                barraColoreada += f'{colorCodigo}='
            else:
                barraColoreada += f'{RESET}-'
        barraColoreada += RESET
        textoPorcentaje = f' {int(porcentaje * 100)}%'
        porcentajeColoreado = f'{colorCodigoPorcentaje}{textoPorcentaje}{RESET}'
    else:
        if porcentaje < 0.33:
            color = ROJO
        elif porcentaje < 0.66:
            color = AMARILLO
        else:
            color = VERDE
        barraColoreada = color + '=' * numCaracteres + RESET + '-' * (longitudBarra - numCaracteres)
        porcentajeColoreado = f'{color} {round(porcentaje * 100)}%{RESET}'

    print(f"\r{PUNTO}{CIAN}Progreso: {AMARILLO}[{barraColoreada}{AMARILLO}]{porcentajeColoreado}", end='')
    sys.stdout.flush()

def imprimirResultados(mejorSolucion = None, mejorCostePromedio = None, mejorCosteMaximo = None) -> None:
    # Imprime resultados si están disponibles.
    hayResultados = False

    if mejorSolucion is not None and len(mejorSolucion) > 0:
        hayResultados = True
        encabezado = " [*]  Mejor solución encontrada: "
        separador = MAGENTA + " -> " + RESET
        separadorVisible = " -> "
        espacioEncabezado = " " * (len(encabezado) - len(separadorVisible))
        anchoNumero = max(len(str(abs(int(num)))) for num in mejorSolucion)

        longitudEncabezado = len(encabezado)
        anchoNum = anchoNumero
        anchoSep = len(separadorVisible)
        anchoTotal = anchoNum + anchoSep

        elementosPrimeraLinea = int(((len(LINEA) - 12) - longitudEncabezado - anchoNum) / anchoTotal) + 1
        elementosOtrasLineas = int(((len(LINEA) - 12) - longitudEncabezado - anchoSep - anchoNum) / anchoTotal) + 1
        maxElementosPorFila = max(1, min(elementosPrimeraLinea, elementosOtrasLineas))

        print("\n" + PUNTO + CIAN + "Mejor solución encontrada: " + RESET, end="")
        for i, numero in enumerate(mejorSolucion):
            if i == 0:
                print(f"{numero:>{anchoNumero}}", end="")
            else:
                if i % maxElementosPorFila == 0:
                    print("\n" + espacioEncabezado + separador, end="")
                else:
                    print(separador, end="")
                print(f"{numero:>{anchoNumero}}", end="")
        print("\n", end="")

    if mejorCostePromedio is not None:
        print(PUNTO + CIAN + "Coste promedio acumulado (fmed): " + RESET + "{:.2f}".format(mejorCostePromedio))
        hayResultados = True

    if mejorCosteMaximo is not None:
        print(PUNTO + CIAN + "Coste máximo acumulado (fmax): " + RESET + "{:.2f}".format(mejorCosteMaximo))
        hayResultados = True

    if not hayResultados:
        sys.stderr.write("\n" + ERROR + ROJO + "No hay resultados para imprimir.\n" + RESET + "\n")

def esperarInput() -> None:
    # Espera ENTER con animación simple.
    if not sys.stdout.isatty():
        # Si no hay TTY, solicita la entrada sin animación.
        input(f"\n{CIAN} Pulsa {AMARILLO}[ENTER]{CIAN} para continuar{RESET}")
        return

    print("\n", end="")
    mensaje = f"{CIAN} Pulsa {AMARILLO}[ENTER]{CIAN} para continuar{RESET}"
    pararAnimacion = threading.Event()
    animacionExcepcion = [None]

    def animar() -> None:
        # Actualiza la línea con puntos animados.
        try:
            i = 0
            direccion = 1
            while not pararAnimacion.is_set():
                numPuntos = i % 4
                puntos = f"{CIAN}.{RESET}" * numPuntos
                print(f"\r{mensaje}{puntos}   ", end="", flush=True)
                time.sleep(0.5)
                if numPuntos == 3:
                    direccion = -1
                elif numPuntos == 0:
                    direccion = 1
                i += direccion
        except Exception as e:
            animacionExcepcion[0] = e
        finally:
            print("\r" + " " * (len(mensaje) + 5), end="\r")

    hiloAnimacion = threading.Thread(target=animar)
    hiloAnimacion.start()
    try:
        input()
    finally:
        pararAnimacion.set()
        hiloAnimacion.join()
    if animacionExcepcion[0]:
        raise animacionExcepcion[0]
