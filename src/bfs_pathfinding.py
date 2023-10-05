from collections import deque
import sys
import time

# Define a class to represent nodes in the search tree
class Node:
    def __init__(self, row, col, cost, parent=None):
        self.row = row            # Row coordinate of the node
        self.col = col            # Column coordinate of the node
        self.cost = cost          # Cost to reach this node from the start
        self.parent = parent      # Reference to the parent node in the search tree

# Function to read the map data from a file
def read_map(filename):
    with open(filename, 'r') as file:
        dimensions = list(map(int, file.readline().split()))  # Read dimensions of the map
        start = tuple(map(int, file.readline().split()))      # Read starting coordinates
        goal = tuple(map(int, file.readline().split()))        # Read goal coordinates
        grid = [list(map(int, line.split())) for line in file] # Read the grid map
    return dimensions, start, goal, grid

# Function to generate successor nodes for the BFS algorithm
def generate_successors(node, grid):
    successors = []
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Possible moves: down, up, right, left
    for dr, dc in moves:
        r, c = node.row + dr, node.col + dc
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c]:
            successors.append(Node(r, c, node.cost + grid[r][c], node))
    return successors

# Breadth-First Search algorithm
def bfs_search(start, goal, grid, time_cutoff):
    visited = set()  # Set to store visited nodes
    queue = deque([Node(start[0], start[1], 0)])  # Queue for BFS
    max_memory = 0  # Variable to track the maximum number of nodes held in memory
    start_time = time.time()  # Start time to measure runtime
    
    while queue:
        current_node = queue.popleft()  # Dequeue the first node in the queue
        
        if (current_node.row, current_node.col) == goal:
            end_time = time.time()
            # Found the goal, return information including visited nodes, max memory, and runtime
            return current_node, visited, max_memory, (end_time - start_time) * 1000  
        
        if (current_node.row, current_node.col) not in visited:
            visited.add((current_node.row, current_node.col))  # Mark the node as visited
            successors = generate_successors(current_node, grid)
            queue.extend(successors)  # Enqueue the successor nodes
            # Update max memory
            max_memory = max(max_memory, len(queue))
        
        # Check the time cutoff
        if (time.time() - start_time) * 1000 > time_cutoff:
            return None, visited, max_memory, None  # Time cutoff reached, no result
    
    return None, visited, max_memory, None  # No path found

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python bfs_pathfinding.py my_map.txt BFS")
        sys.exit(1)

    map_file = sys.argv[1]
    algorithm = sys.argv[2]


    dimensions, start, goal, grid = read_map(map_file)

    result_node, visited, max_memory, runtime = bfs_search(start, goal, grid, 180000)  # 3-minute time cutoff

    if result_node is not None:
        path = []
        while result_node:
            path.append((result_node.row, result_node.col))
            result_node = result_node.parent
        path.reverse()  # Reverse the path to get it from start to goal
        print("Cost of the path:", sum(grid[row][col] for row, col in path))
        print("Number of nodes expanded:", len(visited))
        print("Maximum number of nodes held in memory:", max_memory)
        print("Runtime of the algorithm in milliseconds:", runtime)
        print("Path as a sequence of coordinates:", path)
    else:
        print("No path found. Path cost: -1, Path sequence: NULL")
