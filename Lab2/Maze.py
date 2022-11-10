import random
import pygame as pg
from collections import deque


class Maze:
    def __init__(self, cols, rows, visualize, size, speed):
        self.cols = cols
        self.rows = rows
        self.visualize = visualize
        self.size = size
        self.speed = speed
        self.maze = [[1]*self.cols for _ in range(self.rows)]
        self.unvisited = []

    def get_rect(self, x, y):
        return x * self.size + 1, y * self.size + 1, self.size - 2, self.size - 2

    def generate_matrix(self):
        for i in range(self.cols):
            for j in range(self.rows):
                if i % 2 != 0 and j % 2 != 0:
                    self.unvisited.append([i, j])
                    self.maze[j][i] = 0
        return self.unvisited

    def remove_wall(self, first, second):
        x_diff = second[0] - first[0]
        y_diff = second[1] - first[1]
        add_x = int((x_diff / abs(x_diff))) if (x_diff != 0) else 0
        add_y = int((y_diff / abs(y_diff))) if (y_diff != 0) else 0
        self.maze[first[0] + add_x][first[1] + add_y] = 0

    def get_neighbours(self, x, y):
        check_next_node = lambda x, y: True if 0 <= x < self.cols and 0 <= y < self.rows and not self.maze[x][y] else False
        ways = ([-2, 0], [0, -2], [2, 0], [0, 2])
        return [[x + dx, y + dy] for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def create_graph(self, x, y):
        check_next_node = lambda x, y: True if 0 <= x < self.cols and 0 <= y < self.rows and not self.maze[y][x] else False
        ways = ([-1, 0], [0, -1], [1, 0], [0, 1])
        return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def maze_generate(self):
        start = [1, 1]
        cur_node = start
        unvisited = self.generate_matrix()
        stack = deque([start])

        if self.visualize:
            pg.init()
            sc = pg.display.set_mode([self.cols * self.size, self.rows * self.size])
            clock = pg.time.Clock()
            [[pg.draw.rect(sc, pg.Color(190, 0, 0), self.get_rect(x, y))
              for x, col in enumerate(row) if col] for y, row in enumerate(self.maze)]

        while len(unvisited) > 0:
            neighbours_node = self.get_neighbours(cur_node[0], cur_node[1])
            if len(neighbours_node) != 0:
                random_number = random.randint(0, len(neighbours_node)-1)
                neighbour_node = neighbours_node[random_number]
                neighbours_node.remove(neighbour_node)
                unvisited.remove(neighbour_node)
                stack.append(neighbour_node)
                self.remove_wall(cur_node, neighbour_node)
                cur_node = neighbour_node
                self.maze[cur_node[0]][cur_node[1]] = 2
                if self.visualize:
                    [[pg.draw.rect(sc, pg.Color(145, 105, 205), self.get_rect(x, y))
                      for x, col in enumerate(row) if col == 0 or col == 2] for y, row in enumerate(self.maze)]
                    [exit() for event in pg.event.get() if event.type == pg.QUIT]
                    pg.display.flip()
                    clock.tick(self.speed)

            elif len(stack) > 0:
                cur_node = stack.popleft()
            else:
                random_number = random.randint(0, len(unvisited))-1
                cur_node = unvisited[random_number]
                unvisited.remove(cur_node)

        for i in range(self.cols):
            for j in range(self.rows):
                if self.maze[i][j] != 1:
                    self.maze[i][j] = 0

        graph = {}
        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):
                if not col:
                    graph[(x, y)] = graph.get((x, y), []) + self.create_graph(x, y)

        return self.maze, graph
