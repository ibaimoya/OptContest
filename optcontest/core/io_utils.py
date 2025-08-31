# Entrada/salida por consola y lectura de fichero de datos.

from ..core.config import PUNTO, CIAN, AMARILLO, ROJO, RESET, ERROR
from ..core.ui import imprimirASCII
from ..core.config import np
import sys
import pathlib
from typing import Optional

def salir() -> None:
    # Finaliza el programa.
    print(PUNTO + AMARILLO + "El programa ha finalizado.\n\n" + RESET)
    sys.exit(0)

def verificarSalida(cadena) -> None:
    # Detecta "exit" o "salir" y termina.
    if cadena is not None and (cadena.lower() == "exit" or cadena.lower() == "salir"):
        salir()

def obtenerNombreFichero(primerIntento = True) -> str:
    # Solicita el nombre del fichero al usuario.
    imprimirASCII()
    pedirFichero = "Introduce el nombre del fichero"
    if primerIntento:
        nombreFichero = input(PUNTO + CIAN + "{}: ".format(pedirFichero) + RESET)
    else:
        sys.stderr.write(ERROR + ROJO + "No se ha podido encontrar el fichero.\n" + RESET)
        nombreFichero = input(PUNTO + CIAN + pedirFichero + ROJO + " (¡Cuidado con la ubicación!)" + CIAN + ": " + RESET)
    verificarSalida(nombreFichero)
    return nombreFichero

def _resolver_ruta_fichero(nombre: str) -> Optional[pathlib.Path]:
    '''
    Comprueba si el fichero existe en la ruta original y si no
    lo comprueba en 'dataset'.
    '''
    candidatos = []

    # 1) Directorio de trabajo actual.
    candidatos.append(pathlib.Path(nombre))

    # 2) Carpeta 'dataset' en la raíz del proyecto.
    try:
        raiz = pathlib.Path(__file__).resolve().parents[2]  # OtpContest/.
        candidatos.append(raiz / "dataset" / nombre)
    except Exception:
        pass

    for ruta in candidatos:
        if ruta.is_file():
            return ruta

    return None

def procesarFichero(fichero = None) -> "np.ndarray":
    # Lee el fichero de instancia y devuelve la matriz de tiempos.
    if fichero is None:
        fichero = obtenerNombreFichero()

    ruta = _resolver_ruta_fichero(fichero)
    if ruta is None:
        # Muestra aviso, pide de nuevo y reintenta ambas ubicaciones.
        fichero = obtenerNombreFichero(False)
        ruta = _resolver_ruta_fichero(fichero)

    if ruta is None:
        # Lanza el error final si tampoco existe en 'dataset'.
        sys.stderr.write(ERROR + ROJO + f"No se ha encontrado el fichero ni aquí ni en 'dataset': {fichero}\n" + RESET)
        raise FileNotFoundError(f"Fichero no encontrado: {fichero}")

    with open(ruta, "r") as f:
        lineas = f.readlines()

    filas, columnas = lineas[0].split()
    contenido = np.empty((int(filas), int(columnas)), dtype=int)
    i = 0
    for linea in lineas:
        contenido[i - 1] = np.array(linea.split()[1::2])
        i += 1
    return contenido

def solicitarEntradaNumerica(mensaje, tipoDato, validacion):
    # Pide un número al usuario con validación.
    valor = None
    while valor is None or not validacion(valor):
        try:
            valor = tipoDato(input(mensaje))
            if not validacion(valor):
                raise ValueError
        except ValueError:
            imprimirASCII()
            print(ERROR + ROJO + "Por favor, introduce un número válido." + RESET)
    return valor
