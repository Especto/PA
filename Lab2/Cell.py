from math import sqrt


class Cell:
    def __init__(self, x: int, y: int, stat: int, value=None):
        self.x = x
        self.y = y
        self.stat = stat
        self.value = value

    def set_value(self, cell):
        if self.stat != 1:
            self.value = sqrt((self.x - cell.x) ** 2 + (self.y - cell.y) ** 2)

    def __eq__(self, other):
        if other == None:
            return False
        else:
            return self.x == other.x and self.y == other.y