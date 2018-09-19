import random

from chromosome import Chromosome
from population import Population

POPULATION_SIZE = 10
GENES_COUNT = 20
ELITISM_RATE = 0.2
MUTATION_RATE = 0.09
MAX_GENERATION = 100
BEST_FITNESS = 1.0


def terminal_condition() -> bool:
    return any([chromosome.fitness() >= BEST_FITNESS for chromosome in population.chromosomes])


def fitness(chromosome: Chromosome) -> float:
    return sum(chromosome.genes) / len(chromosome.genes)


# Initial population
population = Population(fitness, POPULATION_SIZE, GENES_COUNT)
generation = 1

while generation <= MAX_GENERATION and not terminal_condition():
    population.sort()

    # Elites
    elite_count = int(ELITISM_RATE * POPULATION_SIZE)
    elite_chromosomes = population.chromosomes[:elite_count]

    # Crossing
    crossed_chromosomes = []
    crossover_count = int((POPULATION_SIZE - elite_count) / 2)

    for _ in range(crossover_count):
        parent_1, parent_2 = random.choices(population.chromosomes, k=2)
        crossed_chromosomes.extend(parent_1.cross(parent_2))

    # Mutation

    for i, v in enumerate(crossed_chromosomes):
        crossed_chromosomes[i] = v.mutate(MUTATION_RATE)

    print(f'------- Generation {generation} -------')
    print(f'Average fitness:\t{population.average_fitness()} / {BEST_FITNESS}')
    print(f'Best:\t\t\t\t{population.chromosomes[0]}')
    print(f'Mid:\t\t\t\t{population.chromosomes[int(len(population.chromosomes)/2)]}')
    print(f'Worst:\t\t\t\t{population.chromosomes[-1]}')
    print(f'Number of elites:\t{elite_count}')
    print(f'Crossover count:\t{crossover_count} pair')
    print(f'Mutation count:\t\t{len(crossed_chromosomes)}')

    # New generation
    population.chromosomes = elite_chromosomes + crossed_chromosomes
    generation += 1

    print('')

population.sort()
fittest = population.chromosomes[0]
print(f'** Generation {generation} has the best chromosome {fittest} with a fitness of {fittest.fitness()}')
