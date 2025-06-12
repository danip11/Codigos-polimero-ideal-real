"""
Simulacion Monte Carlo de cadenas polimericas auto-evitantes (SAW) en 3D
con algoritmo de pivote.

Este script:
  1. Genera una caminata auto-evitante (SAW) de longitud N por crecimiento paso a paso.
  2. Equilibra la configuracion mediante movimientos de pivote aleatorios.
  3. Calcula para cada cadena el radio de giro (R_g) y la distancia extremo–extremo (R_ee).
  4. Repite la simulacion multiples veces para cada valor de N, obteniendo medias e incertidumbres.
  5. Guarda los resultados en ficheros de texto ("rg.txt" y "ree.txt").
  6. Grafica la ultima caminata equilibrada en 3D, marcando el punto de inicio y de fin.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def random_rotation_matrix():
    """
    Genera una matriz de rotacion aleatoria en 3D utilizando el metodo de Rodrigues.
    """
    axis = np.random.normal(size=3)
    axis /= np.linalg.norm(axis)  # Normalizar el eje
    theta = np.random.uniform(0, 2 * np.pi)
    K = np.array([[0, -axis[2], axis[1]],
                  [axis[2], 0, -axis[0]],
                  [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)

def inicializar_saw_3d(n, longitud_paso):
    """
    Inicializa una caminata auto-evitante aleatoria en 3D.
    Utiliza un algoritmo de crecimiento paso a paso con verificacion de colisiones.
    """
    movimientos = np.array([[1, 0, 0], [-1, 0, 0],
                            [0, 1, 0], [0, -1, 0],
                            [0, 0, 1], [0, 0, -1]]) * longitud_paso

    camino = [np.array([0, 0, 0])]
    ocupados = {tuple(camino[0])}

    for _ in range(n):
        np.random.shuffle(movimientos)
        for m in movimientos:
            nuevo_punto = camino[-1] + m
            if tuple(nuevo_punto) not in ocupados:
                camino.append(nuevo_punto)
                ocupados.add(tuple(nuevo_punto))
                break
        else:
            # Si no hay movimientos validos, reiniciar intento completo
            return inicializar_saw_3d(n, longitud_paso)

    return np.array(camino)


def es_auto_evitante(camino):
    """
    Verifica si el camino es auto-evitante (sin puntos repetidos) utilizando conjuntos (set).
    """
    return len(np.unique(camino, axis=0)) == len(camino)


def intento_pivot(camino):
    """
    Realiza un intento de movimiento pivot. Se rota la parte posterior de un punto pivote.
    """
    n = len(camino)
    indice_pivot = np.random.randint(1, n-1)  # Excluye los extremos
    R = random_rotation_matrix()  # Rotacion aleatoria
    punto_pivot = camino[indice_pivot]
    
    # Aplicar la rotacion vectorialmente a los puntos despues del pivote
    vector_post_pivot = camino[indice_pivot+1:] - punto_pivot
    nuevos_puntos = (R @ vector_post_pivot.T).T + punto_pivot
    nuevo_camino = np.vstack((camino[:indice_pivot+1], nuevos_puntos))
    
    if es_auto_evitante(nuevo_camino):
        return nuevo_camino, True
    return camino, False

def radio_de_giro(camino):
    """
    Calcula el radio de giro R_g del polimero.
    """
    centro_masa = np.mean(camino, axis=0)
    return np.sqrt(np.mean(np.sum((camino - centro_masa) ** 2, axis=1)))

def distancia_extremos(camino):
    """
    Calcula la distancia entre el primer y ultimo punto del camino R_ee.
    """
    return np.linalg.norm(camino[-1] - camino[0])

def graficar_camino_3d(camino, titulo="SAW 3D", etiqueta="Polimero"):
    """
    Dibuja la caminata en 3D utilizando lineas, marcando el inicio (verde) y el final (rojo).
    """
    xs, ys, zs = zip(*camino)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(xs, ys, zs, lw=0.5, color="blue", label=etiqueta)
    ax.scatter(xs[0], ys[0], zs[0], c='green', s=50, label="Inicio")
    ax.scatter(xs[-1], ys[-1], zs[-1], c='red', s=50, label="Final")
    ax.set_title(titulo)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    plt.show()


def guardar_resultados(fichero, grados, valores, errores):
    """
    Guarda los resultados (grado de polimerizacion, valores promedio y errores estandar).
    """
    with open(fichero, "w") as f:
        f.write("N\tValor\tError\n")
        for N, valor, error in zip(grados, valores, errores):
            f.write(f"{N}\t{valor:.4f}\t{error:.4f}\n")

# ---------------------------
# Parametros de simulacion
longitud_paso = 1.0
grados_polimerizacion = [500 * i for i in range(1, 21)] # Diferentes numeros de monomeros 
num_simulaciones = 100  
calentamiento = 15000    # Movimientos de pivot para equilibrar

# Almacenamiento de resultados
rg_medios, rg_errores = [], []
ree_medios, ree_errores = [], []

# Simulacion para cada grado de polimerizacion
for N in grados_polimerizacion:
    rg_sim, ree_sim = [], []
    
    for _ in range(num_simulaciones):
        # Crear una SAW inicial y calentarla con movimientos pivot
        camino = inicializar_saw_3d(N, longitud_paso)
        for _ in range(calentamiento):
            camino, _ = intento_pivot(camino)
        
        # Calcular propiedades del camino equilibrado
        rg_sim.append(radio_de_giro(camino))
        ree_sim.append(distancia_extremos(camino))
    
    # Calcular promedio y errores estandar
    rg_medios.append(np.mean(rg_sim))
    rg_errores.append(np.std(rg_sim, ddof=1) / np.sqrt(num_simulaciones))
    ree_medios.append(np.mean(ree_sim))
    ree_errores.append(np.std(ree_sim, ddof=1) / np.sqrt(num_simulaciones))
    
    print(f"N = {N}, Rg = {rg_medios[-1]:.4f} ± {rg_errores[-1]:.4f}, "
          f"Ree = {ree_medios[-1]:.4f} ± {ree_errores[-1]:.4f}")

# Guardar resultados
guardar_resultados("rg.txt", grados_polimerizacion, rg_medios, rg_errores)
guardar_resultados("ree.txt", grados_polimerizacion, ree_medios, ree_errores)

# Graficar la caminata 
graficar_camino_3d(camino, titulo="Simulacion de un Polimero Real - Algoritmo de Pivot", etiqueta="Polimero SAW")