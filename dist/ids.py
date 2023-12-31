import time
import sys

# Define a class to represent nodes in the search tree
class Node:
    def __init__(self, row, col, cost, parent=None):
        self.row = row
        self.col = col
        self.cost = cost
        self.parent = parent

# Function to read the map data from a file and store source/goal nodes
def read_map(filename):
    with open(filename, 'r') as file:
        dimensions = list(map(int, file.readline().split()))  # Read dimensions of the map
        start = tuple(map(int, file.readline().split()))      # Read starting coordinates
        goal = tuple(map(int, file.readline().split()))       # Read goal coordinates
        grid = [list(map(int, line.split())) for line in file] # Read the grid map
    return dimensions, start, goal, grid

# Depth-limited DFS function
def depth_limited_dfs(start, goal, grid, depth_limit, time_cutoff, visited, start_time):
    def dfs(node, depth):
        nonlocal visited
        visited.add((node.row, node.col))

        if (node.row, node.col) == goal:
            path = []
            while node:
                path.append((node.row, node.col))
                node = node.parent
            path.reverse()
            return path

        if depth <= 0 or (time.time() - start_time) * 1000 > time_cutoff:
            return None

        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in moves:
            r, c = node.row + dr, node.col + dc
            if (0 <= r < len(grid)) and (0 <= c < len(grid[0])) and (r, c) not in visited and grid[r][c]:
                child = Node(r, c, 0, node)
                result = dfs(child, depth - 1)
                if result:
                    return result

    return dfs(Node(start[0], start[1], 0), depth_limit)

# Iterative Deepening Search algorithm with time cut-off
def ids_search(start, goal, grid, time_cutoff):
    max_depth = 1
    nodes_expanded = 0
    max_memory = 0
    runtime = 0
    path = None

    while True:
        visited = set()  # Initialize the visited set for each iteration
        start_time = time.time()  # Store the start time for this iteration
        path = depth_limited_dfs(start, goal, grid, max_depth, time_cutoff, visited, start_time)
        nodes_expanded += len(visited)
        max_memory = max(max_memory, len(visited))
        end_time = time.time()
        runtime = (end_time - start_time) * 1000

        if path or runtime > time_cutoff:
            break

        max_depth += 1

    return path, nodes_expanded, max_memory, runtime

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python Ids.py my_map.txt ids time_cutoff(ms)")#if there is no code
        sys.exit(1)

    map_file = sys.argv[1]
    algorithm = sys.argv[2]
    time_cutoff = int(sys.argv[3])

    dimensions, start, goal, grid = read_map(map_file)

    if algorithm == "ids":
        path, nodes_expanded, max_memory, runtime = ids_search(start, goal, grid, time_cutoff)
    else:
        print("Invalid algorithm choice. Use 'ids'.")
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

