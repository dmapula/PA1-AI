from queue import PriorityQueue
import time

# Define a class to represent nodes in the search tree
class Node:
    def __init__(self, row, col, cost, parent=None):
        self.row = row
        self.col = col
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost

# Heuristic function (Manhattan distance)
def manhattan_distance(node, goal):
    return abs(node.row - goal[0]) + abs(node.col - goal[1])

# Function to read the map data from a file and store source/goal nodes
def read_map(filename):
    with open(filename, 'r') as file:
        dimensions = list(map(int, file.readline().split()))  # Read dimensions of the map
        start = tuple(map(int, file.readline().split()))      # Read starting coordinates
        goal = tuple(map(int, file.readline().split()))       # Read goal coordinates
        grid = [list(map(int, line.split())) for line in file] # Read the grid map
    return dimensions, start, goal, grid

# A* Search algorithm with optimizations
def astar_search(start, goal, grid, time_cutoff):
    visited = set()
    queue = PriorityQueue()
    start_node = Node(start[0], start[1], 0)
    queue.put(start_node)
    start_time = time.time()
    max_memory = 0

    while not queue.empty():
        current_node = queue.get()

        if (current_node.row, current_node.col) == goal:
            path = []
            while current_node:
                path.append((current_node.row, current_node.col))
                current_node = current_node.parent
            path.reverse()
            end_time = time.time()
            runtime = (end_time - start_time) * 1000
            return path, len(visited), max_memory, runtime

        visited.add((current_node.row, current_node.col))

        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in moves:
            r, c = current_node.row + dr, current_node.col + dc
            if (0 <= r < len(grid)) and (0 <= c < len(grid[0])) and (r, c) not in visited and grid[r][c]:
                cost = current_node.cost + grid[r][c] + manhattan_distance(Node(r, c, 0), goal)
                queue.put(Node(r, c, cost, current_node))
                max_memory = max(max_memory, queue.qsize())

        # Check time cutoff
        if (time.time() - start_time) * 1000 > time_cutoff:
            return None, len(visited), max_memory, None

    return None, len(visited), max_memory, None

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python astar.py my_map.txt astar time_cutoff(ms)")
        sys.exit(1)

    map_file = sys.argv[1]
    algorithm = sys.argv[2]
    time_cutoff = int(sys.argv[3])

    dimensions, start, goal, grid = read_map(map_file)

    if algorithm == "astar":
        path, nodes_expanded, max_memory, runtime = astar_search(start, goal, grid, time_cutoff)
    else:
        print("Invalid algorithm choice. Use 'astar'.")
        sys.exit(1)

    if path is not None:
        print("Cost of the path:", sum(grid[row][col] for row, col in path))
        print("Number of nodes expanded:", nodes_expanded)
        print("Maximum number of nodes held in memory:", max_memory)
        print("Runtime of the algorithm in milliseconds:", runtime)
        print("Path as a sequence of coordinates:", path)
    else:
        print("Cost of the path: -1")
        print("Number of nodes expanded:", nodes_expanded)
        print("Maximum number of nodes held in memory:", max_memory)
        print("Runtime of the algorithm in milliseconds: -1")
        print("Path as a sequence of coordinates: NO PATH")
