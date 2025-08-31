# Configuración y utilidades comunes.
# Establece colores, constantes, detección de SO y garantiza NumPy disponible.

import sys
import subprocess
import locale
import platform

# Intenta importar NumPy; si no está, lo instala automáticamente.
try:
    import numpy as np  # Se asegura NumPy para el resto de módulos.
except ImportError:
    print(" [*]  Numpy no está instalado. Instalando numpy...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    import numpy as np
    print(" [*]  Numpy se ha instalado correctamente.")

# Colores ANSI.
RESET    = "\x1b[0m"
ROJO     = "\x1b[31m"
VERDE    = "\x1b[32m"
AMARILLO = "\x1b[33m"
AZUL     = "\x1b[34m"
CIAN     = "\x1b[36m"
MAGENTA  = "\x1b[35m"

# Prefijos/formatos comunes.
PUNTO = AMARILLO + " [*]  " + RESET
LINEA = VERDE + "+" + "-" * 80 + "+\n" + RESET
ERROR = ROJO + " [*]  ERROR: " + RESET

# Nombres de algoritmos.
BUS_ALE  = "Búsqueda Aleatoria"
BUS_LOC  = "Búsqueda Local"
REC_SIM  = "Recocido Simulado"
ALG_GEN  = "Algoritmo Genético"

# SO y limpieza de pantalla.
SISTEMA = platform.system()
if SISTEMA == 'Windows':
    CLEAR = "cls"
    STRCASECMP = lambda x, y: x.lower() == y.lower()
    CP_UTF8 = 65001

    def SET_UTF8():
        # Establece UTF-8 en la consola Windows.
        import ctypes
        try:
            ctypes.windll.kernel32.SetConsoleOutputCP(CP_UTF8)
        except Exception:
            pass
else:
    CLEAR = "clear && printf '\\033[3J]'"
    STRCASECMP = lambda x, y: x.lower() == y.lower()

    def SET_UTF8():
        # Establece locale UTF-8 si está disponible.
        try:
            locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")
        except Exception:
            try:
                locale.setlocale(locale.LC_ALL, "C.UTF-8")
            except Exception:
                pass

# Aplica UTF-8 al importar este módulo.
SET_UTF8()

__all__ = [
    "np",
    "RESET","ROJO","VERDE","AMARILLO","AZUL","CIAN","MAGENTA",
    "PUNTO","LINEA","ERROR",
    "BUS_ALE","BUS_LOC","REC_SIM","ALG_GEN",
    "SISTEMA","CLEAR","SET_UTF8"
]