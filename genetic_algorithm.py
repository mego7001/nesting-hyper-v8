# core/genetic_algorithm.py

import random
from shapely.affinity import rotate, translate

class GeneticAlgorithm:
    """
    Implements a configurable genetic algorithm for nesting.
    """
    def __init__(self, population_size, generations, rotation_angles):
        self.population_size = population_size
        self.generations = generations
        self.rotation_angles = rotation_angles
        self.population = []

    def initialize_population(self, parts, sheets):
        # Each individual: random placement and rotation
        for _ in range(self.population_size):
            individual = []
            for part in parts:
                angle = random.choice(self.rotation_angles)
                pos = (random.uniform(0, sheet['width']), random.uniform(0, sheet['height']))
                individual.append({'part': part, 'angle': angle, 'pos': pos})
            self.population.append(individual)

    def fitness(self, individual):
        # Placeholder: evaluate based on bounding box overlap and sheet use
        return random.random()

    def select(self):
        # Tournament selection
        sorted_pop = sorted(self.population, key=self.fitness, reverse=True)
        return sorted_pop[:self.population_size//2]

    def crossover(self, parents):
        # Single-point crossover
        offspring = []
        for _ in range(len(parents)):
            p1, p2 = random.sample(parents, 2)
            point = random.randint(1, len(p1)-1)
            child = p1[:point] + p2[point:]
            offspring.append(child)
        return offspring

    def mutate(self, individual):
        # Randomly change angle or position
        for gene in individual:
            if random.random() < 0.1:
                gene['angle'] = random.choice(self.rotation_angles)
                gene['pos'] = (gene['pos'][0] + random.uniform(-5,5), gene['pos'][1] + random.uniform(-5,5))

    def run(self, parts, sheets):
        self.initialize_population(parts, sheets)
        for _ in range(self.generations):
            parents = self.select()
            offspring = self.crossover(parents)
            for child in offspring:
                self.mutate(child)
            self.population = parents + offspring
        best = max(self.population, key=self.fitness)
        return best
