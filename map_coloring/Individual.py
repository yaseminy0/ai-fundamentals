import random


class Individual:
    def __init__(self, map):
        self.map = map
        self.colors = [random.randrange(4) for state in map.states]
        self.updateFitness()

    def updateFitness(self):
        self.fitness = 0

        for border in self.map.borders:
            if self.colors[border.index1] != self.colors[border.index2]:
                self.fitness += 1

    def reproduce(self, x, y):
        child = Individual(x.map)
        point = random.randrange(1, len(x.colors))
        child.colors = x.colors[:point] + y.colors[point:]
        child.updateFitness()
        return child

    def mutate(self):
        state = random.randrange(len(self.colors))
        other_colors = [0, 1, 2, 3]
        other_colors.remove(self.colors[state])
        self.colors[state] = random.choice(other_colors)
        self.updateFitness()

    def isGoal(self):
        return self.fitness == len(self.map.borders)

    def printresult(self):
        print("Coloring:")
        for state, color in zip(self.map.states, self.colors):
            print(f"{state}: {color}")

        violations = len(self.map.borders) - self.fitness
        print("Constraint violations:", violations)