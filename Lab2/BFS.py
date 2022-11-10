import pygame as pg
from collections import deque
import time


class BFS:

    def __init__(self, maze, graph, start_node, end_node, visual, speed, size):
        self.maze = maze
        self.graph = graph
        self.start_node = start_node
        self.end_node = end_node
        self.speed = speed
        self.size = size
        self.visual = visual
        self.states = 0
        self.iterations = 0
        self.stored_states = len(self.maze)**2

        if self.visual:
            pg.init()
            self.sc = pg.display.set_mode([len(maze) * size, len(maze[0]) * size])
            self.clock = pg.time.Clock()
            self.sc.fill(pg.Color(21, 35, 51))
            [[pg.draw.rect(self.sc, pg.Color(190, 0, 0), self.get_rect(x, y, self.size))
              for x, col in enumerate(row) if col] for y, row in enumerate(self.maze)]

    @staticmethod
    def get_rect(x, y, size):
        return x * size + 1, y * size + 1, size - 2, size - 2

    def print_path(self, visited, cur_node):
        [pg.draw.rect(self.sc, pg.Color(120, 150, 0), self.get_rect(x, y, self.size)) for x, y in visited]
        path_segment = cur_node
        while path_segment:
            pg.draw.rect(self.sc, pg.Color('white'), self.get_rect(*path_segment, self.size))
            path_segment = visited[path_segment]
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(self.speed)

    def bfs(self):
        start = time.time()
        queue = deque([self.start_node])
        visited = {self.start_node: None}

        while queue:
            self.iterations += 1
            cur_node = queue.popleft()
            if cur_node == self.end_node:
                break
            next_nodes = self.graph[cur_node]
            for next_node in next_nodes:
                if next_node not in visited:
                    self.states += 1
                    queue.append(next_node)
                    visited[next_node] = cur_node
            if self.visual:
                [pg.draw.rect(self.sc, pg.Color(120, 150, 0), self.get_rect(x, y, self.size)) for x, y in visited]
                path_segment = cur_node
                while path_segment:
                    pg.draw.rect(self.sc, pg.Color('white'), self.get_rect(*path_segment, self.size))
                    path_segment = visited[path_segment]
                [exit() for event in pg.event.get() if event.type == pg.QUIT]
                pg.display.flip()
                self.clock.tick(self.speed)
        if self.visual:
            self.print_path(visited, cur_node)
        return self.iterations, self.states, self.stored_states, str(time.time()-start)
