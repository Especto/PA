from Maze import Maze
from RBFS import RBFS
from Cell import Cell
from BFS import BFS


def main():
    cols, rows = 21, 21  # Unpaired numbers
    visual = False  # True - show working of algorithms in pygame
    speed, size = 30, 10  # drawing speed and size of cell for drawing
    start_node_bfs, end_node_bfs = (1, 1), (cols-2, rows-2)
    start_node_rbfs, end_node_rbfs = Cell(1, 1, 0), Cell(cols-2, rows-2, 0)

    for i in range(20):
        maze = Maze(cols, rows, visual, size, speed).maze_generate()
        bfs_data = BFS(maze[0], maze[1], start_node_bfs, end_node_bfs, visual, speed, size).bfs()
        rbfs_data = RBFS(maze[0], start_node_rbfs, end_node_rbfs, visual, speed, size)._rbfs()
        print(f"{'-'*10}BFS{'-'*10}\n" і
              f"Iterations: {bfs_data[0]}\nNumber of states: {bfs_data[1]}\nStored states: {bfs_data[2]}\nTime: {bfs_data[3]}")
        print(f"{'-'*10}RBFS{'-'*10}\n"
              f"Iterations: {rbfs_data[0]}\nNumber of states: {rbfs_data[1]}\nStored states: {rbfs_data[2]}\nTime: {rbfs_data[3]}")


main()
