from minesweeper_io import Console_IO
from collections import namedtuple
from random import randint

class Minesweeper_Grid(object):
    cells = []
    Cell = namedtuple("Cell", ("has_bomb", "state"))

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [self.Cell(False, "hidden")] * (width * height)

    @classmethod
    def gen_random(cls, width, height, n_bombs):
        def get_random_point():
            return (randint(0, width - 1), randint(0, height - 1))
        
        grid = cls(width, height)
        while n_bombs:
            x, y = get_random_point()
            while grid.get_cell(x, y).has_bomb:
                x, y = get_random_point()

            grid.put_bomb(x, y)
            n_bombs -= 1

        return grid
            
    
    def get_cell(self, x, y):
        return self.cells[y * self.height + x]

    def set_cell(self, x, y, cell):
        self.cells[y * self.height + x] = cell

    def put_bomb(self, x, y):
        c = self.get_cell(x, y)
        new_c = self.Cell(True, c.state)
        self.set_cell(x, y, new_c)

    def discover_cell(self, x, y):
        c = self.get_cell(x, y)
        new_c = self.Cell(c.has_bomb, "shown")
        self.set_cell(x, y, new_c)

    def flag_cell(self, x, y):
        c = self.get_cell(x, y)
        new_c = self.Cell(c.has_bomb, "flagged")
        self.set_cell(x, y, new_c)

    def hide_cell(self, x, y):
        c = self.get_cell(x, y)
        new_c = self.Cell(c.has_bomb, "hidden")
        self.set_cell(x, y, new_c)


io = Console_IO()
grid = Minesweeper_Grid.gen_random(10, 10, 10)
while True:
    io.show_grid(grid)
    io.get_input(grid.width, grid.height)

