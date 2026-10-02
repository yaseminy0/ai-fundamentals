import heapq
import math
from pathlib import Path
from vector2d import Vector2D
from environment import Environment


# ---------- 1. GEOMETRY ----------
# Two simple, standard tests replace the parametric clipping version:
#   (a) does segment ab properly cross a polygon edge?
#   (b) does the midpoint of ab lie inside the polygon?
# If either is true for any obstacle, the straight line from a to b is blocked.

def orientation(a, b, c):
    """+1 = left turn, -1 = right turn, 0 = collinear."""
    val = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
    if val > 1e-9:
        return 1
    if val < -1e-9:
        return -1
    return 0


def on_segment(a, b, p):
    return (min(a.x, b.x) - 1e-9 <= p.x <= max(a.x, b.x) + 1e-9 and
            min(a.y, b.y) - 1e-9 <= p.y <= max(a.y, b.y) + 1e-9)


def segments_intersect(a, b, c, d):
    """True if segment ab properly crosses segment cd."""
    o1, o2 = orientation(a, b, c), orientation(a, b, d)
    o3, o4 = orientation(c, d, a), orientation(c, d, b)

    if o1 != o2 and o3 != o4:
        return True

    # collinear touching cases
    return ((o1 == 0 and on_segment(a, b, c)) or
            (o2 == 0 and on_segment(a, b, d)) or
            (o3 == 0 and on_segment(c, d, a)) or
            (o4 == 0 and on_segment(c, d, b)))


def point_in_polygon(p, polygon):
    """Ray-casting test: True if p is strictly inside the polygon."""
    vertices = polygon.vertices
    inside = False
    n = len(vertices)
    for i in range(n):
        a, b = vertices[i], vertices[(i + 1) % n]
        if (a.y > p.y) != (b.y > p.y):
            x_cross = (b.x - a.x) * (p.y - a.y) / (b.y - a.y + 1e-15) + a.x
            if p.x < x_cross:
                inside = not inside
    return inside


def blocked_by(polygon, a, b):
    midpoint_x, midpoint_y = (a.x + b.x) / 2, (a.y + b.y) / 2
    mid = Vector2D(midpoint_x, midpoint_y)


    if point_in_polygon(mid, polygon):
        return True

    vertices = polygon.vertices
    n = len(vertices)
    for i in range(n):
        edge_a, edge_b = vertices[i], vertices[(i + 1) % n]
        if a in (edge_a, edge_b) or b in (edge_a, edge_b):
            continue  # segments sharing an endpoint don't count as "crossing"
        if segments_intersect(a, b, edge_a, edge_b):
            return True
    return False


def visible(a, b, obstacles):
    for polygon in obstacles:
        if blocked_by(polygon, a, b):
            return False

    return True


# ---------- 2. STATES AND SUCCESSORS (visibility graph) ----------

def same_polygon_neighbors(a, b, obstacles):
    """Adjacent vertices of the same polygon are always connected (they
    form an edge of the obstacle itself)."""
    for polygon in obstacles:
        vertices = polygon.vertices
        if a in vertices and b in vertices:
            i, j = vertices.index(a), vertices.index(b)
            n = len(vertices)
            if j == (i + 1) % n or i == (j + 1) % n:
                return True
    return False


def create_graph(env):
    points = [env.start, env.goal]
    for polygon in env.obstacles:
        points.extend(polygon.vertices)

    n = len(points)
    graph = [[] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            a, b = points[i], points[j]
            can_see = (same_polygon_neighbors(a, b, env.obstacles) or
                       visible(a, b, env.obstacles))
            if can_see:
                d = a.distance(b)
                graph[i].append((j, d))
                graph[j].append((i, d))

    return points, graph, 1  # start = index 0, goal = index 1


# ---------- 3. SEARCH ----------
# f(n) = (2 - w) * g(n) + w * h(n)   (Exercise 3.1's formula)
#   w = 0 -> Uniform-Cost Search, w = 1 -> A*, w = 2 -> Greedy Best-First

WEIGHTS = {"uniformcost": 0, "astar": 1, "greedy": 2}


def search(points, graph, goal, algorithm):
    w = WEIGHTS[algorithm]
    start = 0

    g_cost = {start: 0}
    parent = {start: None}
    frontier = [(w * points[start].distance(points[goal]), start)]
    visited = set()
    expanded = 0

    while frontier:
        _, node = heapq.heappop(frontier)
        if node in visited:
            continue
        visited.add(node)
        expanded += 1

        if node == goal:
            path, n = [], node
            while n is not None:
                path.append(points[n])
                n = parent[n]
            path.reverse()
            return path, g_cost[goal], expanded

        for neighbor, step_cost in graph[node]:
            new_g = g_cost[node] + step_cost
            if new_g < g_cost.get(neighbor, math.inf):
                g_cost[neighbor] = new_g
                parent[neighbor] = node
                h = points[neighbor].distance(points[goal])
                f = (2 - w) * new_g + w * h
                heapq.heappush(frontier, (f, neighbor))

    return [], math.inf, expanded


#run

def main():
    folder = Path(__file__).resolve().parent
    env = Environment(folder / "environment.txt")
    output = folder / "output"
    output.mkdir(exist_ok=True)

    points, graph, goal = create_graph(env)

    report_lines = [f"Start: {env.start}; Goal: {env.goal}"]

    for algorithm in ["astar", "greedy", "uniformcost"]:
        path, cost, expanded = search(points, graph, goal, algorithm)
        route = " -> ".join(str(p) for p in path) if path else "No path found"

        report_lines.append(
            f"\n{algorithm}\n"
            f"Path: {route}\n"
            f"Total cost: {cost:.6f}\n"
            f"Expanded nodes: {expanded}"
        )
        Environment.printPath(algorithm, path, output)

    report = "\n".join(report_lines)
    print(report)
    (output / "results.txt").write_text(report + "\n")


if __name__ == "__main__":
    main()
