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
def depth_limited_dfs(start, goal, grid, depth_limit):
    visited = set()

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

        if depth <= 0:
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

# Iterative Deepening Search algorithm
def iterative_deepening_search(start, goal, grid):
    max_depth = 1
    while True:
        path = depth_limited_dfs(start, goal, grid, max_depth)
        if path:
            return path
        max_depth += 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python IDS.py my_map.txt")
        sys.exit(1)

    map_file = sys.argv[1]
    dimensions, start, goal, grid = read_map(map_file)

    path = iterative_deepening
