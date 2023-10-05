from queue import PriorityQueue
import time

# Define a class to represent nodes in the search tree
class Node:
    def __init__(self, row, col, cost, parent=None):
        self.row = row            # Row coordinate of the node
        self.col = col            # Column coordinate of the node
        self.cost = cost          # Cost to reach this node from the start
        self.parent = parent      # Reference to the parent node in the search tree

    def __lt__(self, other):
        return self.cost < other.cost  # Comparator for priority queue

# Function to read the map data from a file and store source/goal nodes
def read_map(filename):
    with open(filename, 'r') as file:
        dimensions = list(map(int, file.readline().split()))  # Read dimensions of the map
        start = tuple(map(int, file.readline().split()))      # Read starting coordinates
        goal = tuple(map(int, file.readline().split()))       # Read goal coordinates
        grid = [list(map(int, line.split())) for line in file] # Read the grid map
    return dimensions, start, goal, grid

# Function to calculate the Manhattan distance heuristic
def manhattan_distance(node, goal):
    return abs(node.row - goal[0]) + abs(node.col - goal[1])

# A* Search algorithm
def astar_search(start, goal, grid, time_cutoff=None):
    visited = set()  # Set to store visited nodes
    queue = PriorityQueue()  # Priority queue for A* search
    start_node = Node(start[0], start[1], 0)
    queue.put(start_node)
    start_time = time.time()  # Start time to measure runtime

    while not queue.empty():
        current_node = queue.get()  # Get the node with the lowest cost

        if (current_node.row, current_node.col) == goal:
            path = []
            while current_node:
                path.append((current_node.row, current_node.col))
                current_node = current_node.parent
            path.reverse()  # Reverse the path to get it from start to goal
            end_time = time.time()
            runtime = (end_time - start_time) * 1000  # Calculate runtime in milliseconds
            return path, len(visited), runtime

        visited.add((current_node.row, current_node.col))  # Mark the node as visited

        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Possible moves: down, up, right, left
        for dr, dc in moves:
            r, c = current_node.row + dr, current_node.col + dc
            if (0 <= r < len(grid)) and (0 <= c < len(grid[0])) and (r, c) not in visited and grid[r][c]:
                cost = current_node.cost + grid[r][c] + manhattan_distance(Node(r, c, 0), goal)
                queue.put(Node(r, c, cost, current_node))

        # Check time cutoff
        if time_cutoff is not None and (time.time() - start_time) * 1000 > time_cutoff:
            return None, len(visited), None  # Time cutoff reached, no result

    return None, len(visited), None  # No path found

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python pathfinding.py my_map.txt astar time_cutoff(ms)")
        sys.exit(1)

    my_map = sys.argv[1]
    algorithm = sys.argv[2]
    time_cutoff = int(sys.argv[3])

    dimensions, start, goal, grid = read_map(my_map)

    if algorithm == "astar":
        path, nodes_expanded, runtime = astar_search(start, goal, grid, time_cutoff)
    else:
        print("Invalid algorithm choice. Use 'astar'.")
        sys.exit(1)

    if path is not None:
        print("Path:", path)
        print("Path Cost:", sum(grid[row][col] for row, col in path))
        print("Nodes Expanded:", nodes_expanded)
        print("Runtime (ms):", runtime)
    else:
        print("No path found within the time cutoff.")
