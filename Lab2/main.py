from Maze import Maze
from RBFS import RBFS
from Cell import Cell
from BFS import BFS
import time

def main():
    cols, rows, visual, speed, size = 21, 21, True, 120, 10
    start_node_bfs, end_node_bfs = (1, 1), (cols-2, rows-2)
    start_node_rbfs, end_node_rbfs = Cell(1, 1, 0), Cell(cols-2, rows-2, 0)

    for i in range(20):
        maze = Maze(cols, rows, visual, size, speed).maze_generate()
        bfs_data = BFS(maze[0], maze[1], start_node_bfs, end_node_bfs, visual, speed, size).bfs()
        time.sleep(1)
        rbfs_data = RBFS(maze[0], start_node_rbfs, end_node_rbfs, visual, speed, size)._rbfs()
        time.sleep(1)
        print(f"{'-'*10}BFS{'-'*10}\n"
              f"Iterations: {bfs_data[0]}\nNumber of states: {rbfs_data[1]}\n")
        print(f"{'-'*10}RBFS{'-'*10}\n"
              f"Iterations: {rbfs_data[0]}\nNumber of states: {rbfs_data[1]}\nStored states: {rbfs_data[2]}\n")
main()