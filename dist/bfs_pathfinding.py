from collections import deque
import sys
import time
 
class Node:
    def __init__(self, row, col, cost, parent=None):
        self.row = row            # node row coordinate
        self.col = col            # node column coordinate
        self.cost = cost          # node cost from the start
        self.parent = parent      # referece for the parent node


# Reads map data from a file: dimensions of the map, starting coordinates,
# goal coordinates, and grid map
def read_map(filename):

    with open(filename, 'r') as file:

        grid_dimensions = list(map(int, file.readline().split())) # Read dimensions of the map
        start_coordinate = tuple(map(int, file.readline().split()))
        goal_coordinate = tuple(map(int, file.readline().split()))
        grid = [list(map(int, line.split())) for line in file]   # Read the grid map

    return grid_dimensions, start_coordinate, goal_coordinate, grid

# Generates successor nodes for the BFS algorithm
def create_successors(node, grid):

    successor_nodes = []
    # Possible moves: down, up, right, left
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]  
    for dr, dc in moves:

        r, c = node.row + dr, node.col + dc
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c]:
            successor_nodes.append(Node(r, c, node.cost + grid[r][c], node))

    return successor_nodes

# Breadth-First Search algorithm
def bfs_search(start_coordinate, goal_coordinate, grid, time_cutoff):

    visited_node = set()  # Stores visited nodes
    queue = deque([Node(start_coordinate[0], start_coordinate[1], 0)])  # Queue for BFS
    in_memory = 0  # Tracks maximum number of nodes held in memory
    start_time = time.time()  # Start time to measure runtime
    
    while queue:
        # Dequeue first node in the queue
        current_node = queue.popleft()
        
        if (current_node.row, current_node.col) == goal_coordinate:
            end_time = time.time()
            # Found the goal, return information including visited 
            # nodes, max memory, and runtime
            return current_node, visited_node, in_memory, (end_time - start_time) * 1000  
        
        if (current_node.row, current_node.col) not in visited_node:
            visited_node.add((current_node.row, current_node.col))  # Marks node as visited
            successor_nodes = create_successors(current_node, grid)
            queue.extend(successor_nodes)  # Enqueue the successor nodes
            # Update max memory
            in_memory = max(in_memory, len(queue))
        
        # Check time cutoff
        if (time.time() - start_time) * 1000 > time_cutoff:
            return None, visited_node, in_memory, None  # Reached time cutoff, no result
    
    return None, visited_node, in_memory, None  # No path found

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Use: python bfs_pathfinding.py my_map.txt BFS")
        sys.exit(1)

    map_file = sys.argv[1]
    algorithm = sys.argv[2]


    grid_dimensions, start_coordinate, goal_coordinate, grid = read_map(map_file)

    # 3-minute time cutoff
    result_node, visited_node, in_memory, runtime = bfs_search(start_coordinate, goal_coordinate, grid, 180000)

    if result_node is not None:

        path = []
        while result_node:
            path.append((result_node.row, result_node.col))
            result_node = result_node.parent
        path.reverse()  # Reverses path to get it from start to goal
        print("Cost of the path:", sum(grid[row][col] for row, col in path))
        print("Number of nodes expanded:", len(visited_node))
        print("Maximum number of nodes held in memory:", in_memory)
        print("Runtime of the algorithm in milliseconds:", runtime)
        print("Path as a sequence of coordinates:", path)

    else:
        print("No path found. Path cost: -1, Path sequence: NULL")
