import random
import time

#States and Neighbors
neighbors = {
    "NC": ["SC", "VA", "TN", "GA"],
    "SC": ["NC", "GA"],
    "VA": ["NC", "TN", "KY", "WV"],
    "TN": ["NC", "VA", "KY", "GA", "AL", "MS"],
    "KY": ["VA", "TN", "WV"],
    "WV": ["VA", "KY"],
    "GA": ["NC", "SC", "TN", "AL", "FL"],
    "AL": ["TN", "GA", "MS", "FL"],
    "MS": ["TN", "AL"],
    "FL": ["GA", "AL"]
}

states = list(neighbors.keys())
colors = ["Red", "Green", "Blue", "Yellow"]


# Check color is allowed
def safe(state, color, assignment):
    for neighbor in neighbors[state]:
        if neighbor in assignment:
            if assignment[neighbor] == color:
                return False

    return True


# Copy domains --branches do not affect each other
def copy_domains(domains):
    new_domains = {}

    for state in states:
        new_domains[state] = domains[state].copy()

    return new_domains


# Forward checking
def forward_check(state, assignment, domains):
    color = assignment[state]

    for neighbor in neighbors[state]:
        if neighbor not in assignment:
            if color in domains[neighbor]:
                domains[neighbor].remove(color)

            if len(domains[neighbor]) == 0:
                return False

    return True


# AC-3
def ac3(domains):
    queue = []

    for state in states:
        for neighbor in neighbors[state]:
            queue.append((state, neighbor))

    while len(queue) > 0:
        x, y = queue.pop(0)
        changed = False

        for color_x in domains[x].copy():
            supported = False

            for color_y in domains[y]:
                if color_x != color_y:
                    supported = True
                    break

            if supported == False:
                domains[x].remove(color_x)
                changed = True

        if changed:
            if len(domains[x]) == 0:
                return False

            for neighbor in neighbors[x]:
                if neighbor != y:
                    queue.append((neighbor, x))

    return True


# Backtracking for BT, FC, and AC3
def backtrack(assignment, domains, method):
    if len(assignment) == len(states):
        return assignment.copy()

    # Select the first unassigned state
    for state in states:
        if state not in assignment:
            break

    for color in domains[state]:
        if safe(state, color, assignment):
            assignment[state] = color

            new_domains = copy_domains(domains)
            new_domains[state] = [color]

            possible = True

            if method == "FC":
                possible = forward_check(
                    state, assignment, new_domains
                )

            elif method == "AC3":
                possible = ac3(new_domains)

            if possible:
                result = backtrack(
                    assignment, new_domains, method
                )

                if result is not None:
                    return result

            # Remove the color - try another one
            del assignment[state]

    return None


#prepare domains - start search
def solve(initial, method):
    assignment = initial.copy()
    domains = {}

    for state in states:
        domains[state] = colors.copy()

    for state in initial:
        domains[state] = [initial[state]]

    # Apply the initial assignment 
    if method == "FC":
        for state in initial:
            if not forward_check(state, assignment, domains):
                return None

    elif method == "AC3":
        if not ac3(domains):
            return None

    return backtrack(assignment, domains, method)


#count neighbors with the same color
def conflicts(state, color, assignment):
    count = 0

    for neighbor in neighbors[state]:
        if assignment[neighbor] == color:
            count += 1

    return count


# Min-conflicts
def min_conflicts(initial):
    assignment = initial.copy()

    for state in states:
        if state not in assignment:
            assignment[state] = random.choice(colors)

    for step in range(10000):
        bad_states = []

        for state in states:
            if not safe(state, assignment[state], assignment):
                bad_states.append(state)

        if len(bad_states) == 0:
            return assignment

        # Keep initial assignment fixed
        movable_states = []

        for state in bad_states:
            if state not in initial:
                movable_states.append(state)

        if len(movable_states) == 0:
            return None

        state = random.choice(movable_states)

        best_colors = []
        lowest_count = len(neighbors[state]) + 1

        for color in colors:
            count = conflicts(state, color, assignment)

            if count < lowest_count:
                lowest_count = count
                best_colors = [color]

            elif count == lowest_count:
                best_colors.append(color)

        assignment[state] = random.choice(best_colors)

    #check the last repair
    for state in states:
        if not safe(state, assignment[state], assignment):
            return None

    return assignment


# solution
def valid(solution, initial):
    if solution is None:
        return False

    for state in states:
        if state not in solution:
            return False

        if solution[state] not in colors:
            return False

        if not safe(state, solution[state], solution):
            return False

    for state in initial:
        if solution[state] != initial[state]:
            return False

    return True


# Evaluate algorithms
algorithms = ["BT", "FC", "AC3", "Min-conflicts"]
initial_assignments = [{}, {"NC": "Red"}]
runs = 100

print("Algorithm | Initial assignment | Average ms | Solved")

for algorithm in algorithms:
    for initial in initial_assignments:
        total_time = 0
        solved = 0
        example = None

        for run in range(runs):
            random.seed(run)

            start = time.perf_counter()

            if algorithm == "Min-conflicts":
                solution = min_conflicts(initial)
            else:
                solution = solve(initial, algorithm)

            total_time += time.perf_counter() - start

            if valid(solution, initial):
                solved += 1
                example = solution

        average_ms = total_time / runs * 1000

        if len(initial) == 0:
            label = "None"
        else:
            label = "NC = Red"

        print(
            algorithm, "|",
            label, "|",
            round(average_ms, 6), "|",
            str(solved) + "/" + str(runs)
        )

        print("solution:", example)
        print()