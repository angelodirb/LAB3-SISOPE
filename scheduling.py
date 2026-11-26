from argparse import ArgumentParser
from bisect import bisect_left
from random import Random

import matplotlib.pyplot as plt

'''
para ejecutarlo con el cabezal en el cilindro 2150
python -m pip install matplotlib
python scheduling.py 2150
'''


MIN_CYLINDER = 0
MAX_CYLINDER = 4999
NUM_REQUESTS = 1000
SEED = 42


# Generación de solicitudes
def generate_requests(seed):
    generator = Random(seed)
    requests = []

    for _ in range(NUM_REQUESTS):
        requests.append(generator.randint(MIN_CYLINDER, MAX_CYLINDER))

    return requests


# Algoritmos de planificación
def calculate_fcfs(requests, start):
    return [start] + requests


def calculate_scan(requests, start):
    ordered = sorted(requests)
    first = bisect_left(ordered, start)
    route = [start] + ordered[first:]

    if first > 0:
        if route[-1] != MAX_CYLINDER:
            route.append(MAX_CYLINDER)
        route.extend(reversed(ordered[:first]))

    return route


def calculate_cscan(requests, start):
    ordered = sorted(requests)
    first = bisect_left(ordered, start)
    route = [start] + ordered[first:]

    if first > 0:
        if route[-1] != MAX_CYLINDER:
            route.append(MAX_CYLINDER)
        route.append(MIN_CYLINDER)
        route.extend(ordered[:first])

    return route


def calculate_movement(route):
    total = 0

    for index in range(1, len(route)):
        total += abs(route[index] - route[index - 1])

    return total


# Visualización de resultados
def plot_results(algorithms, routes, movements):
    figure, axes = plt.subplots(2, 2, figsize=(12, 8), layout="constrained")
    figure.suptitle("Planificación de discos con 1000 solicitudes")
    colors = ["tab:red", "tab:blue", "tab:green"]

    for axis, algorithm, route, color in zip(
        axes.flat, algorithms, routes, colors
    ):
        axis.plot(range(len(route)), route, color=color, linewidth=0.9)
        axis.set_title(algorithm)
        axis.set_xlabel("Paso del recorrido")
        axis.set_ylabel("Cilindro")
        axis.set_ylim(MIN_CYLINDER, MAX_CYLINDER)
        axis.grid(alpha=0.3)

    comparison = axes[1, 1]
    bars = comparison.bar(algorithms, movements, color=colors)
    comparison.set_title("Comparación del movimiento total")
    comparison.set_ylabel("Cilindros recorridos")
    comparison.set_ylim(0, max(movements) * 1.15)
    comparison.bar_label(bars, padding=3)
    comparison.ticklabel_format(axis="y", style="plain")

    plt.show()


# Ejecución
def main():
    parser = ArgumentParser(description="Simulador de planificación de discos")
    parser.add_argument("start", type=int, help="Cilindro inicial del cabezal")
    args = parser.parse_args()

    if not MIN_CYLINDER <= args.start <= MAX_CYLINDER:
        parser.error("La posición inicial debe estar entre 0 y 4999.")

    requests = generate_requests(SEED)
    algorithms = ["FCFS", "SCAN", "C-SCAN"]
    routes = [
        calculate_fcfs(requests, args.start),
        calculate_scan(requests, args.start),
        calculate_cscan(requests, args.start),
    ]
    movements = [calculate_movement(route) for route in routes]

    print(f"Posición inicial: {args.start}")
    print(f"Solicitudes: {NUM_REQUESTS}")

    for algorithm, movement in zip(algorithms, movements):
        print(f"{algorithm}: {movement} cilindros")

    plot_results(algorithms, routes, movements)


if __name__ == "__main__":
    main()