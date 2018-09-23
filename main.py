import random

import matplotlib.pyplot as plt
import numpy as np

from chromosome import Chromosome
from constants import *
from maze import Maze
from population import Population

maze = Maze([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
             [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
             [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
             [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
             [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
             [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
             [1, 0, 0, 0, 0, 3, 1, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

POPULATION_SIZE = 500
GENES_COUNT = 25
ELITISM_RATE = 0.01
MUTATION_RATE = 0.1
MAX_GENERATION = 50000

number_of_empty = np.count_nonzero(maze.structure == EMPTY)
max_distance = maze.flying_distance((0, 0), (len(maze.structure), len(maze.structure[0])))


def terminal_condition() -> bool:
    return False


def fitness(chromosome: Chromosome) -> float:
    _, position, move_count = maze.make_a_try(chromosome.genes)
    distance_to_end = maze.flying_distance(position, maze.end)

    if move_count == 0:
        move_count = 1

    fit = max_distance - distance_to_end + 2 ** (1 / move_count)

    return fit


# Initial population
population = Population(fitness, POPULATION_SIZE, GENES_COUNT)
generation = 1

average_fitness = []
best_fitness = []
mid_fitness = []
worst_fitness = []

while generation < MAX_GENERATION and not terminal_condition():
    population.sort()

    # Elites
    elite_count = int(ELITISM_RATE * POPULATION_SIZE)
    elite_chromosomes = population.chromosomes[:elite_count]

    # Crossing
    crossed_chromosomes = []
    crossover_count = int((POPULATION_SIZE - elite_count) / 2) - elite_count

    for _ in range(crossover_count):
        parent_1, parent_2 = random.choices(population.chromosomes, k=2)
        crossed_chromosomes.extend(parent_1.cross(parent_2))

    # Mutation
    mutated_elites = [elite.mutate(MUTATION_RATE) for elite in elite_chromosomes]

    for i, v in enumerate(crossed_chromosomes):
        crossed_chromosomes[i] = v.mutate(MUTATION_RATE)

    # Save generation values
    average_fitness.append(population.average_fitness())
    best_fitness.append(population.chromosomes[0].fitness())
    mid_fitness.append(population.chromosomes[int(len(population.chromosomes) / 2)].fitness())
    worst_fitness.append(population.chromosomes[-1].fitness())

    if generation % 100 == 0:
        print(f'------- Generation {generation} -------')
        print(f'Average fitness:\t{population.average_fitness()}')
        print(f'Best:\t\t\t\t({population.chromosomes[0].fitness()}){population.chromosomes[0]}')
        print(f'Worst:\t\t\t\t{population.chromosomes[-1]}')
        print(f'Number of elites:\t{elite_count}')
        print(f'Crossover count:\t{crossover_count} pair')
        print(f'Mutation count:\t\t{len(crossed_chromosomes)}')
        print('')

    # New generation
    population.chromosomes = elite_chromosomes + mutated_elites + crossed_chromosomes
    generation += 1

population.sort()
fittest = population.chromosomes[0]
print(f'** Generation {generation} has the best chromosome {fittest} with a fitness of {fittest.fitness()}')

plt.plot(range(generation - 1), average_fitness)
plt.plot(range(generation - 1), best_fitness)
plt.plot(range(generation - 1), worst_fitness)
plt.legend(['Average', 'Best', 'Worst'])
plt.title('Fitness to generation')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()
