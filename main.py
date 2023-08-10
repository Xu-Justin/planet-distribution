import os, shutil, sys
import math
import numpy as np
import matplotlib.pyplot as plt
import itertools
from typing import Tuple
from tqdm import tqdm

plt.rcParams["figure.figsize"] = (8,8)

def generate_random() -> int:
    return np.random.randint(1, 1000000)

def generate_point() -> np.float32:
    return np.float32(generate_random()) / np.float32((generate_random() + 1))

def generate_planet(n_dimension: int) -> np.ndarray:
    planet = []
    for _ in range(n_dimension):
        planet.append(generate_point())
    return np.array(planet, np.float32)

def generate_planets(n_planet: int, n_dimension: int) -> np.ndarray:
    planets = []
    for _ in range(n_planet):
        planets.append(generate_planet(n_dimension))
    return np.array(planets, np.float32)

def calculate_distance(planetA: np.ndarray, planetB: np.ndarray) -> np.float32:
    return np.float32(np.linalg.norm(planetA - planetB))

def calculate_cost(planets: np.ndarray, terminal_planets: np.ndarray) -> np.float32:
    cost = 0
    for planet in planets:
        costs = []
        for terminal_planet in terminal_planets:
            costs.append(calculate_distance(planet, terminal_planet))
        cost += np.min(costs)
    return np.float32(cost)

def generate_solution(planets: np.ndarray, n_terminal_planet: int) -> Tuple[np.ndarray, np.float32]:
    min_cost = np.Infinity
    min_solution = None
    terminal_planets_combinations = itertools.combinations(planets, n_terminal_planet)
    len_terminal_planets_combinations = math.comb(len(planets), n_terminal_planet)
    for terminal_planets in tqdm(terminal_planets_combinations, total=len_terminal_planets_combinations, desc=f'Generating Solutions'):
        terminal_planets = np.array(terminal_planets)
        cost = calculate_cost(planets, terminal_planets)
        if (cost < min_cost):
            min_cost = cost
            min_solution = terminal_planets
    return (min_solution, min_cost)

def plot_solution_2d(planets: np.ndarray, terminal_planets: np.ndarray, filename: str):
    assert planets.shape[1] == 2, f'Invalid plot_solution_2d with planet n_dimension: {planets.shape[1]}'
    assert terminal_planets.shape[1] == 2, f'Invalid plot_solution_2d with terminal_planet n_dimension: {terminal_planets.shape[1]}'
    plt.clf()
    plt.scatter(planets[:, 0], planets[:, 1], c=None, marker='.', alpha=0.2)
    plt.scatter(terminal_planets[:, 0], terminal_planets[:, 1], c='#FF0000', marker='o', alpha=0.5)
    right = max(plt.xlim()[1], plt.ylim()[1])
    left = -0.01 * right
    plt.xlim(left, right)
    plt.ylim(left, right)
    plt.savefig(filename, dpi=300)

def plot_solution_3d(planets: np.ndarray, terminal_planets: np.ndarray, filename: str):
    assert planets.shape[1] == 3, f'Invalid plot_solution_3d with planet n_dimension: {planets.shape[1]}'
    assert terminal_planets.shape[1] == 3, f'Invalid plot_solution_3d with terminal_planet n_dimension: {terminal_planets.shape[1]}'
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(planets[:, 0], planets[:, 1], planets[:, 2], c=None, marker='.', alpha=0.2)
    ax.scatter(terminal_planets[:, 0], terminal_planets[:, 1], terminal_planets[:, 2], c='#FF0000', marker='o', alpha=0.5)
    right = max(planets[:, 0].max(), planets[:, 1].max(), planets[:, 2].max())
    left = - 0.01 * right
    ax.axes.set_xlim3d(left, right)
    ax.axes.set_ylim3d(left, right)
    ax.axes.set_zlim3d(left, right)
    fig.savefig(filename, dpi=300)

def simulate(n_dimension: int, n_planet: int, n_terminal_planet: int, filename: str = None):
    planets = generate_planets(n_planet, n_dimension)
    terminal_planets, _ = generate_solution(planets, n_terminal_planet)
    if filename:
        if n_dimension == 2:
            plot_solution_2d(planets, terminal_planets, filename=filename)
        elif n_dimension == 3:
            plot_solution_3d(planets, terminal_planets, filename=filename)
        else:
            print(f'Unknown way to plot solution with n_dimensions: {n_dimension}')
    else:
        print(terminal_planets)

def get_args_parser():
    import argparse
    parser = argparse.ArgumentParser(description="Run simulations of planets in a multi-dimensional space.")
    parser.add_argument('--folder', type=str, default="result", help='Folder where simulation images will be saved.')
    parser.add_argument('--filename', type=str, default="simulation", help='Prefix for the filenames of the simulation images.')
    parser.add_argument('--dimensions', type=int, default=3, help='Number of dimensions for the simulation space.')
    parser.add_argument('--planets', type=int, default=50, help='Total number of planets in the simulation.')
    parser.add_argument('--terminal-planets', type=int, default=3, help='Number of terminal planets in the simulation.')
    parser.add_argument('--iterations', type=int, default=1, help='Number of simulation iterations to run.')
    parser.add_argument('--replace-folder', action='store_true', help='Replace the folder if it already exists.')
    args = parser.parse_args()
    return args

def main(args):

    if os.path.exists(args.folder):
        if args.replace_folder:
            print(f"Deleting existing folder: {args.folder}")
            shutil.rmtree(args.folder)
        else:
            print(f"Folder '{args.folder}' already exists. Use --replace-folder to replace it.")
            sys.exit(1)
    
    os.makedirs(args.folder)
    
    for index in range(args.iterations):
        simulate(args.dimensions, args.planets, args.terminal_planets, os.path.join(args.folder, args.filename + '_' + str(index).zfill(3) + '.png'))

if __name__ == '__main__':
    args = get_args_parser()
    print(args)
    main(args)