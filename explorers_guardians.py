from collections import deque
#Yasemin Aleyna Yilmaz assignment2

#I use breadth-first search (BFS) to find the optimal solution. 
# A state is represented as (E, G, B)
# Where E and G must be numbers of explorers and guardians on the LEFT bank, B represent the location of the boat (L or R)

#A state is valid only when safety conditions holds on both side of the river: 

initial_state = (3, 3, 'L')
goal_state = (0, 0, 'R')

#Possible boat passengers: 
#Explorers and guardians

MOVES = [
    (1,0), #one explorer
    (2,0), #two explorer
    (0,1), #one guardian
    (0,2), #two guardian
    (1,1) #one explorer and one guardian
]


#Check both river banks satisfy the safety rule:
def valid_state(e,g):
    #numbers on the right bank:
    right_e = 3 - e
    right_g = 3 - g

    #counts must remain within valid bounds
    if not (0 <= e <= 3 and 0 <= g <= 3):
        return False

    #Left bank safety condition
    if e > 0 and g > e:
        return False

    #Right bank safety condition
    if right_e > 0 and right_g > right_e:
        return False

    return True


def successors(state):
    e, g, boat = state
    result = []

    for move_e, move_g in MOVES:

        if boat == 'L':
            new_e = e - move_e
            new_g = g - move_g
            new_boat = 'R'

            if move_e > e or move_g > g:
                continue

        else:
            new_e = e + move_e
            new_g = g + move_g
            new_boat = 'L'

            right_e = 3 - e
            right_g = 3 - g

            if move_e > right_e or move_g > right_g:
                continue

        if valid_state(new_e, new_g):
            result.append(
                ((new_e, new_g, new_boat), (move_e, move_g))
            )

    return result
        
def bfs():
    start = (3, 3, 'L')
    goal = (0, 0, 'R')

    queue = deque([(start, [])])
    visited = {start}

    while queue:
        state, path = queue.popleft()

        if state == goal:
            return path

        for next_state, move in successors(state):

            if next_state not in visited:
                visited.add(next_state)

                new_path = path + [(next_state, move)]
                queue.append((next_state, new_path))

    return None

solution = bfs()
current = (3, 3, 'L')

for i, (state, move) in enumerate(solution, 1):
    e, g = move
    direction = "->" if current[2] == 'L' else "<-"

    print(
        f"{i}: Move {e} explorers, "
        f"{g} guardians {direction} {state}"
    )

    current = state

print("Number of crossings:", len(solution))
