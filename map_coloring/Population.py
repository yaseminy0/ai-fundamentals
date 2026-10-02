import random
from Individual import Individual


class Population:
    def __init__(self, map, initialSize):
        self.vector = [Individual(map) for i in range(initialSize)]

    def randomSelection(self):
        weights = [individual.fitness + 1 for individual in self.vector]
        return random.choices(self.vector, weights=weights, k=1)[0]