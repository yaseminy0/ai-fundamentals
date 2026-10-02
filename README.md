# AI Fundamentals

A collection of Python projects exploring AI agents, search algorithms, and genetic algorithms.

## Projects

### 1. Vacuum World
A simulation of a two-location vacuum-cleaner environment using a simple reflex agent.

- Separates the agent from the environment.
- Tests all eight initial configurations.
- Evaluates performance over 1,000 time steps.
- Achieves an average score of 1999.25 out of 2000.
- Does not penalize movement or introduce new dirt.

**Run:**
python vacuum_world.py

### 2. River Crossing
A Breadth-First Search (BFS) solution for the explorers and guardians river-crossing problem.

- Represents states using explorer counts, guardian counts, and boat location.
- Checks safety constraints on both riverbanks.
- Uses a visited set to avoid repeated states.
- Finds a minimum-crossing solution in 11 crossings when each crossing has equal cost.

**Run:**
python explorers_guardians.py

### 3. Pathfinding
A comparison of A*, Greedy Best-First Search, and Uniform-Cost Search in an environment with polygon obstacles.

- Constructs a visibility graph.
- Uses Euclidean distance for path costs.
- Uses straight-line distance to the goal as the heuristic.
- Compares total path cost and expanded nodes.

Results recorded for the example environment:

| Algorithm | Path Cost | Expanded Nodes |
|---|---:|---:|
| A* | 1041.218190 | 47 |
| Greedy Best-First Search | 1290.803698 | 6 |
| Uniform-Cost Search | 1041.218190 | 139 |

In this example, A* found the same path cost as Uniform-Cost Search while expanding fewer nodes. Greedy expanded fewer nodes but returned a longer path.

**Run:**
python pathfinding/main.py

Keep environment.txt in the pathfinding folder and update the loading line in main.py to:

env = Environment(folder / "environment.txt")

The program creates an output folder for the generated results.

### 4. Map Coloring
A genetic algorithm that searches for valid four-color assignments on a 10-state map and a 51-region map.

- Evaluates fitness using correctly colored borders.
- Uses weighted selection, single-point crossover, and mutation.
- Preserves the best individual through elitism.
- Reports color assignments and constraint violations.

Parameters:
- Population size: 200
- Mutation probability per child: 0.05
- Maximum generations: 10,000

A valid solution has zero constraint violations. Results vary between runs because the algorithm uses randomness.

**Run from the map-coloring folder:**
cd map-coloring
python Main.py

## Requirements

- Python 3
- Python standard library only

## Background and Acknowledgments

These projects began as academic exercises.

The pathfinding project builds on an instructor-provided framework. The map-coloring project also uses an instructor-provided framework, with source comments crediting Fan Zhang. Original author credits are retained.

## Limitations

These are small educational implementations. Results depend on the example environments and algorithm settings. The genetic algorithm does not guarantee finding a solution within the generation limit, and the pathfinding geometry checks have not been fully validated for arbitrary polygon configurations.
### 5. CSP Map Coloring — Algorithm Comparison

A Python comparison of four approaches to solving a 10-state map-coloring problem:

- Backtracking
- Backtracking with Forward Checking
- Backtracking with AC-3 constraint propagation
- Min-Conflicts

Each state is a variable with four possible colors. Neighboring states must have different colors.

#### Evaluation

Each method is evaluated over 100 runs under two initial conditions:
- No fixed colors.
- North Carolina fixed to Red.

The program reports average runtime in milliseconds, the number of valid solutions, and an example coloring. Solution validation checks all neighbor constraints and preserves the initial assignment.

In a verification run, all four methods found valid solutions in 100/100 runs under both conditions. Runtime depends on the machine, and results on this small map do not establish which method performs best on larger problems.

Min-Conflicts uses random initialization and tie-breaking, with a maximum of 10,000 repair steps. A solution is not guaranteed within that limit.

#### Requirements

Python 3. No external packages or data files are required.

#### Run

From the repository root:

    python csp-map-coloring/map_coloring_csp.py
