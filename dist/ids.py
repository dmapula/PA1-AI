
class GridGraph:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def is_valid_move(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row][col] == 1

    def get_neighbors(self, row, col):
        neighbors = []
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_move(new_row, new_col):
                neighbors.append((new_row, new_col))
        return neighbors


def iterative_deepening_search(grid_graph, start, goal, max_depth):
    for depth_limit in range(max_depth + 1):
        visited = [[False for _ in range(grid_graph.cols)] for _ in range(grid_graph.rows)]
        if dfs(grid_graph, start, goal, visited, depth_limit):
            return True
    return False


def dfs(grid_graph, node, goal, visited, depth_limit):
    row, col = node
    if (row, col) == goal:
        return True
    if depth_limit <= 0:
        return False
    if not visited[row][col]:
        visited[row][col] = True
        neighbors = grid_graph.get_neighbors(row, col)
        for neighbor in neighbors:
            if dfs(grid_graph, neighbor, goal, visited, depth_limit - 1):
                return True
    return False


# Read grid from file
def read_grid_from_file(file_path):
    with open(file_path, 'r') as file:
        rows, cols = map(int, file.readline().strip().split())
        grid = []
        for _ in range(rows):
            row = list(map(int, file.readline().strip().split()))
            grid.append(row)
        return GridGraph(grid)


# Test the IDS algorithm with grid from file


testcase1 = "dist/5x5.txt"  # Provide the correct path to your grid file
grid_graph1 = read_grid_from_file(testcase1)
start_node = (0, 0)  # Starting position
goal_node = (4, 4)   # Goal position
max_depth = 5         # Maximum depth limit
print("Path exists from {} to {} within depth {}: {}".format(start_node, goal_node, max_depth,iterative_deepening_search(grid_graph1, start_node,goal_node, max_depth)))

testcase2 = "dist/10x10.txt"  # Provide the correct path to your grid file
grid_graph2 = read_grid_from_file(testcase2)
start_node = (0, 0)  # Starting position
goal_node = (9, 9)   # Goal position
max_depth = 10         # Maximum depth limit
print("Path exists from {} to {} within depth {}: {}".format(start_node, goal_node, max_depth,iterative_deepening_search(grid_graph2, start_node,goal_node, max_depth)))

testcase3 = 'dist/15x15.txt'  # Provide the correct path to your grid file
grid_graph3 = read_grid_from_file(testcase3)
start_node = (0, 0)  # Starting position
goal_node = (14, 14)   # Goal position
max_depth = 15         # Maximum depth limit
print("Path exists from {} to {} within depth {}: {}".format(start_node, goal_node, max_depth,iterative_deepening_search(grid_graph2, start_node,goal_node, max_depth)))

testcase4 = 'dist/20x20.txt'  # Provide the correct path to your grid file
grid_graph4 = read_grid_from_file(testcase4)
start_node = (0, 0)  # Starting position
goal_node = (4, 4)   # Goal position
max_depth = 5         # Maximum depth limit
print("Path exists from {} to {} within depth {}: {}".format(start_node, goal_node, max_depth,iterative_deepening_search(grid_graph3, start_node,goal_node, max_depth)))

