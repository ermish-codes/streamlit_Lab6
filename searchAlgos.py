import math
import heapq

# ============================================================
# HOSPITAL GRAPH (same for both GBFS and A*)
# ============================================================
locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}

hospital_graph = {
    "Pharmacy": {
        "Main_Corridor": 2.2,
        "Patient_Wing": 4.1
    },
    "Main_Corridor": {
        "Nursing_Station": 2.2,
        "Patient_Wing": 3.5
    },
    "Patient_Wing": {
        "Laboratory": 5.0,
        "Nursing_Station": 3.0
    },
    "Nursing_Station": {
        "Laboratory": 3.0,
        "Emergency_Ward": 5.0
    },
    "Laboratory": {
        "Emergency_Ward": 2.8
    },
    "Emergency_Ward": {}
}

# ============================================================
# EUCLIDEAN HEURISTIC
# ============================================================
def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# ============================================================
# GBFS (Greedy Best-First Search)
# ============================================================
def gbfs(start, goal, graph):
    priority_queue = []
    heapq.heappush(priority_queue, (heuristic(start, goal), start))

    visited = set()
    visited.add(start)

    parent = {start: None}
    expansion_order = []

    while priority_queue:
        h_val, current = heapq.heappop(priority_queue)

        if current in expansion_order:
            continue

        expansion_order.append(current)

        if current == goal:
            break

        for neighbor, cost in graph[current].items():
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                heapq.heappush(priority_queue, (heuristic(neighbor, goal), neighbor))

    # Reconstruct path
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    # Calculate actual cost
    total_cost = 0
    i = 0
    while i < len(path) - 1:
        total_cost = total_cost + graph[path[i]][path[i + 1]]
        i = i + 1

    return path, total_cost, expansion_order

# ============================================================
# A* SEARCH
# ============================================================
def a_star(start, goal, graph):
    priority_queue = []
    heapq.heappush(priority_queue, (heuristic(start, goal), 0, start))

    g_cost = {start: 0}
    parent = {start: None}
    expansion_order = []

    while priority_queue:
        f, g, current = heapq.heappop(priority_queue)

        if current in expansion_order:
            continue

        expansion_order.append(current)

        if current == goal:
            break

        for neighbor, cost in graph[current].items():
            new_g = g + cost
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                parent[neighbor] = current
                new_f = new_g + heuristic(neighbor, goal)
                heapq.heappush(priority_queue, (new_f, new_g, neighbor))

    # Reconstruct path
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    total_cost = g_cost[goal] if goal in g_cost else 0

    return path, total_cost, expansion_order