import pygame as pg
from Cell import Cell
from BFS import BFS
from sys import maxsize


class RBFS:
    iterations = 0
    states = 0
    stored_states = 0

    def __init__(self, maze, start_node, end_node, visual, speed, size):
        self.maze = maze
        self.start_node = start_node
        self.end_node = end_node
        self.speed = speed
        self.size = size
        self.visual = visual
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.maze_cells = [[Cell]*self.cols for _ in range(self.rows)]
        self.last = []
        self.visited = []
        self.graph = {}

        if self.visual:
            pg.init()
            self.sc = pg.display.set_mode([len(maze) * size, len(maze[0]) * size])
            self.clock = pg.time.Clock()
            self.sc.fill(pg.Color(21, 35, 51))
            [[pg.draw.rect(self.sc, pg.Color(190, 0, 0), BFS.get_rect(x, y, self.size))
              for x, col in enumerate(row) if col] for y, row in enumerate(self.maze)]
            [exit() for event in pg.event.get() if event.type == pg.QUIT]

    def _rbfs(self):
        self.generate_cells()
        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)
        self.rbfs(self.start_node, maxsize - 1)
        return RBFS.iterations, RBFS.states, RBFS.stored_states

    def get_next_nodes(self, x, y):
        check_next_node = lambda x, y: True if 0 <= x < self.cols and 0 <= y < self.rows and self.maze[y][x] != 1 else False
        ways = ([-1, 0], [0, -1], [1, 0], [0, 1])
        return [self.maze_cells[x + dx][y + dy] for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def generate_cells(self):
        for i in range(self.cols):
            for j in range(self.rows):
                self.maze_cells[i][j] = Cell(i, j, self.maze[j][i])
                self.maze_cells[i][j].set_value(self.end_node)

    def rbfs(self, node, f_limit):
        successors = []
        result = None

        if node == self.end_node:
            return node, None

        neighbours = self.graph[node.x, node.y]
        self.last.append(node)
        self.visited.append(node)

        count = -1

        for neighbour in neighbours:
            count += 1
            if neighbour not in self.last:
                successors.append((neighbour.value, count, neighbour))
        RBFS.states += len(successors)
        if RBFS.stored_states < len(successors): RBFS.stored_states = len(successors)

        if not len(successors):
            return None, maxsize

        if self.visual:
            [pg.draw.rect(self.sc, pg.Color(120, 150, 0), BFS.get_rect(point.x, point.y, self.size)) for point in
             self.visited]
            [pg.draw.rect(self.sc, pg.Color("white"), BFS.get_rect(point.x, point.y, self.size)) for point in self.last]
            pg.draw.rect(self.sc, pg.Color("white"), BFS.get_rect(self.end_node.x, self.end_node.y, self.size))
            pg.display.flip()
            self.clock.tick(self.speed)

        while len(successors):
            RBFS.iterations += 1
            successors.sort()
            best_node = successors[0][2]

            if best_node.value > f_limit:
                self.last.remove(node)
                return None, best_node.value

            try:
                alternative = successors[1][0]
            except (Exception,):
                alternative = f_limit+1

            result, best_node.value = self.rbfs(best_node, min(f_limit, alternative))
            successors[0] = (best_node.value, successors[0][1], best_node)

            if result != None:
                break
        return result, None






