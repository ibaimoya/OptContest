# Funciones de evaluación de costes (f, fmed, fmax).

from ..core.config import np

def crearMatrizDeCostes(datos, secuencia):
    # Crea la matriz de costes f para una secuencia dada.
    matrizCostes = np.zeros_like(datos)
    matrizCostes[0] = np.add.accumulate(datos[secuencia[0]])
    for i in range(1, len(secuencia)):
        for j in range(len(datos[0])):
            izquierda = 0 if j == 0 else matrizCostes[i][j - 1]
            arriba = matrizCostes[i - 1][j]
            matrizCostes[i][j] = max(arriba, izquierda) + datos[secuencia[i]][j]
    return matrizCostes

def obtenerCostePromedio(datos, solucion):
    # Calcula fmed medio de la última columna.
    matrizCostes = np.zeros_like(datos)
    matrizCostes[0] = np.add.accumulate(datos[solucion[0]])
    sumaUltimaColumna = matrizCostes[0, -1]
    numFilas = len(solucion)
    numColumnas = len(datos[0])
    for i in range(1, numFilas):
        for j in range(numColumnas):
            izquierda = 0 if j == 0 else matrizCostes[i][j - 1]
            arriba = matrizCostes[i - 1][j]
            matrizCostes[i][j] = max(arriba, izquierda) + datos[solucion[i]][j]
            if j == numColumnas - 1:
                sumaUltimaColumna += matrizCostes[i][j]
    return sumaUltimaColumna / numFilas

def obtenerCosteMaximo(matrizCostes):
    # Devuelve fmax de la matriz f.
    return matrizCostes[-1, -1]