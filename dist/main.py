import sys
from bfs_pathfinding import bfs_search, read_map
from A_Search import astar_search, read_map

def main():
    if len(sys.argv) != 4:
        print("Usage: main.py map_file algorithm time_cutoff(ms)")
        sys.exit(1)

    map_file = sys.argv[1]
    algorithm = sys.argv[2]
    time_cutoff = int(sys.argv[3])

    dimensions, start, goal, grid = read_map(map_file)  # Import the read_map function

    if algorithm == "bfs":
        path, visited, max_memory, runtime = bfs_search(start, goal, grid, time_cutoff)
    elif algorithm == "astar":
        path, visited, max_memory, runtime = astar_search(start, goal, grid, time_cutoff)
    else:
        print("Invalid algorithm choice. Use 'bfs' or 'astar'.")
        sys.exit(1)

    if path is not None:
        print("Cost of the path:", sum(grid[row][col] for row, col in path))
        print("Number of nodes expanded:", visited)
        print("Maximum number of nodes held in memory:", max_memory)
        print("Runtime of the algorithm in milliseconds:", runtime)
        print("Path as a sequence of coordinates:", path)
    else:
        print("Path cost: -1")
        print("Number of nodes expanded:", visited)
        print("Maximum number of nodes held in memory:", max_memory)
        print("Runtime of the algorithm in milliseconds: -1")
        print("Path as a sequence of coordinates: NO PATH")

if __name__ == "__main__":
    main()
