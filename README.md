# Códigos: Polímero Ideal y Real

## Simulación de Cadenas Poliméricas 3D

Este repositorio contiene dos scripts en Python para la simulación de cadenas poliméricas en 3D:

* **PolimeroIdeal.py**: Modelo de cadena libremente unida (Random Walk 3D).
* **PolimeroRealPivote.py**: Cadenas auto-evitantes (Self-Avoiding Walk, SAW) usando el algoritmo de pivote.

---

## Descripción

### 1. PolimeroIdeal.py

Este script simula cadenas poliméricas siguiendo el modelo de cadena libremente unida (random walk) en 3D. Para distintos grados de polimerización (N):

1. Genera configuraciones de polímeros mediante caminatas aleatorias normalizadas.
2. Calcula el radio de giro (Rg) y la distancia extremo–extremo (Rn) para cada cadena.
3. Repite la simulación múltiples veces para obtener medias y errores estadísticos de Rg y Rn.
4. Guarda los resultados en los archivos `valores_rg.txt` y `valores_rn.txt`.
5. Grafica la última cadena simulada en un gráfico 3D, marcando el inicio (verde) y el final (rojo).

### 2. PolimeroRealPivote.py

Este script implementa una simulación Monte Carlo de cadenas auto-evitantes (SAW) en 3D mediante el algoritmo de pivote:

1. Genera una caminata auto-evitante paso a paso comprobando colisiones.
2. Equilibra la configuración con movimientos de pivote aleatorios.
3. Calcula el radio de giro (Rg) y la distancia extremo–extremo (R\_ee) de la cadena equilibrada.
4. Repite el proceso para distintos valores de N y obtiene medias y errores.
5. Guarda los resultados en `rg.txt` y `ree.txt`.
6. Grafica la última caminata equilibrada en 3D.

---

## Requisitos

* Python 3.7 o superior
* Paquetes de Python:

  * `numpy`
  * `matplotlib`

Instálalos con:

```bash
pip install numpy matplotlib
```

---

## Uso

1. Clona el repositorio:

```bash
git clone <URL-del-repositorio>
cd <carpeta-del-repositorio>
```

2. Ejecuta **PolimeroIdeal.py**:

```bash
python PolimeroIdeal.py
```

* Genera los archivos `valores_rg.txt` y `valores_rn.txt`.
* Muestra un gráfico 3D de la última cadena simulada.

3. Ejecuta **PolimeroRealPivote.py**:

```bash
python PolimeroRealPivote.py
```

* Genera los archivos `rg.txt` y `ree.txt`.
* Imprime en consola los valores promedio y los errores.
* Muestra un gráfico 3D de la última caminata equilibrada.

---

## Estructura del repositorio

```
├── PolimeroIdeal.py         # Simulación de cadena ideal (random walk 3D)
├── PolimeroRealPivote.py    # Simulación SAW con algoritmo de pivote
├── valores_rg.txt           # Resultados de radio de giro (modelo ideal)
├── valores_rn.txt           # Resultados de distancia extremo–extremo (modelo ideal)
├── rg.txt                   # Resultados de radio de giro (SAW)
├── ree.txt                  # Resultados de R_ee (SAW)
└── README.md                # Documentación del proyecto
```

---

## Personalización de parámetros

Ambos scripts incluyen parámetros de simulación al inicio del archivo:

* **longitud\_paso**: Tamaño del paso en la caminata.
* **grados\_polimerizacion**: Lista de valores de N a simular.
* **num\_simulaciones**: Número de réplicas para promediar.
* **calentamiento** (solo en SAW): Número de movimientos de pivote para equilibrar.

Edita estos valores según tus necesidades antes de ejecutar los scripts.

---

## Autor

* Daniel Pérez Pérez
* Contacto: [danielp1003@gmail.com](mailto:danielp1003@gmail.com)


