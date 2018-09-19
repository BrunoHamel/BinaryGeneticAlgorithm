import random
from copy import copy
from typing import Callable


class Chromosome:

    def __init__(self, fitness_func: Callable, genes_length=0):
        self.genes = [random.getrandbits(1) for _ in range(genes_length)]
        self.fitness_func = fitness_func

    @staticmethod
    def copy(chromosome: 'Chromosome') -> 'Chromosome':
        child = Chromosome(chromosome.fitness_func)
        child.genes = copy(chromosome.genes)
        return child

    def cross(self, other_chromosome) -> tuple:
        crossover_point = random.randint(1, len(self.genes) - 2)

        def cross_at_point(parent_1, parent_2, point):
            child = Chromosome(self.fitness_func)
            child.genes = parent_1.genes[:point] + parent_2.genes[point:]
            return child

        child_1 = cross_at_point(self, other_chromosome, crossover_point)
        child_2 = cross_at_point(other_chromosome, self, crossover_point)

        return child_1, child_2

    def mutate(self, chance_of_mutation: float) -> 'Chromosome':
        child = Chromosome.copy(self)
        for i, v in enumerate(child.genes):
            if random.uniform(0, 1) <= chance_of_mutation:
                child.genes[i] = int(not v)
        return child

    def fitness(self) -> float:
        return self.fitness_func(self)

    def __str__(self):
        return ' '.join(str(g) for g in self.genes)
