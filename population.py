from typing import Callable

from chromosome import Chromosome


class Population:

    def __init__(self, fitness_func: Callable, size=0, genes_length=0):
        self.chromosomes = [Chromosome(fitness_func, genes_length) for _ in range(size)]

    def sort(self) -> None:
        self.chromosomes.sort(key=lambda c: c.fitness(), reverse=False)

    def __str__(self):
        return '\n'.join(([str(c) for c in self.chromosomes]))

    def average_fitness(self):
        return sum([chromosome.fitness() for chromosome in self.chromosomes]) / self.size

    @property
    def size(self) -> int:
        return len(self.chromosomes)

    def add(self, new_chromosomes: list) -> None:
        self.chromosomes += new_chromosomes
