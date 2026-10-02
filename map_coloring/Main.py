import random

from Border import Border
from Individual import Individual
from Map import Map
from Population import Population

# Author Fan Zhang
def initMap(map):
    map.states.append("North Carolina")
    map.states.append("South Carolina")
    map.states.append("Virginia")
    map.states.append("Tennessee")
    map.states.append("Kentucky")
    map.states.append("West Virginia")
    map.states.append("Georgia")
    map.states.append("Alabama")
    map.states.append("Mississippi")
    map.states.append("Florida")

    map.borders.append(Border(0, 1))
    map.borders.append(Border(0, 2))
    map.borders.append(Border(0, 3))
    map.borders.append(Border(0, 6))
    map.borders.append(Border(1, 6))
    map.borders.append(Border(2, 3))
    map.borders.append(Border(2, 4))
    map.borders.append(Border(2, 5))
    map.borders.append(Border(3, 4))
    map.borders.append(Border(3, 6))
    map.borders.append(Border(3, 7))
    map.borders.append(Border(3, 8))
    map.borders.append(Border(4, 5))
    map.borders.append(Border(6, 7))
    map.borders.append(Border(6, 9))
    map.borders.append(Border(7, 8))
    map.borders.append(Border(7, 9))

def initMap51(map):
    with open("us_states_51_ij.txt", "r") as file:
        rows = [line.strip().split(",") for line in file if line.strip()]

    for row in rows:
        map.states.append(row[0])

    addedBorders = set()

    for row in rows:
        state = row[0]

        for neighbor in row[1:]:
            pair = tuple(sorted((state, neighbor)))

            if pair not in addedBorders:
                i = map.states.index(state)
                j = map.states.index(neighbor)
                map.borders.append(Border(i, j))
                addedBorders.add(pair)

def runAlgorithm(map, name):
    populationSize = 200
    population = Population(map, populationSize)

    maxIterations = 10000
    currentIteration = 0
    bestIndividual = max(population.vector, key=lambda individual: individual.fitness)
    goalFound = bestIndividual.isGoal()

    while currentIteration < maxIterations and goalFound == False:
        newPopulation = Population(map, 0)

        # Keep the best individual for the next generation.
        newPopulation.vector.append(bestIndividual)

        for i in range(populationSize - 1):
            x = population.randomSelection()
            y = population.randomSelection()
            child = Individual.reproduce(x, x, y)

            if random.random() < 0.05:
                child.mutate()

            if child.fitness > bestIndividual.fitness:
                bestIndividual = child

            if child.isGoal():
                goalFound = True
                bestIndividual = child

            newPopulation.vector.append(child)

        currentIteration += 1
        population = newPopulation

    print("\n" + name)

    if goalFound:
        print("Found a solution after", currentIteration, "iterations")
    else:
        print("Did not find a solution after", currentIteration, "iterations")

    bestIndividual.printresult()


if __name__ == '__main__':
    map10 = Map()
    initMap(map10)
    runAlgorithm(map10, "10-state map")

    map51 = Map()
    initMap51(map51)
    runAlgorithm(map51, "51-region map")