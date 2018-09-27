from abc import ABC, abstractmethod
from collections import namedtuple
from random import randint

class IO_Controller(ABC):
    @abstractmethod
    def show_grid(self, grid):
        pass

    @abstractmethod
    def get_input(self, g_width, g_height):
        pass


class Console_IO(IO_Controller):
    def show_grid(self, grid):
        out = []
        for y in range(grid.height):
            line = ""
            for x in range(grid.width):
                bomb_c, hidden_c, flagged_c, empty_c = "B", "■", "!", "□"
                cell = grid.get_cell(x, y)
                if cell.state == "hidden":
                    line += hidden_c
                elif cell.state == "flagged":
                    line += flagged_c
                elif cell.state == "shown":
                    line += bomb_c if cell.has_bomb else empty_c

                line += " "

            out.append(line)

        print("\n".join(out))
        print("=" * (grid.width * 2))

    def get_input(self, g_width, g_height):
        print("Introduce D para descubrir y M para marcar, seguido de las coordenadas de la celda separadas por una coma")
        while True:
            action, coords = input().split()
        try:
            coords = (int(c) for c in coords.split(","))
        except:
            print("Ha introducido unas coordenadas no validas, por favor intentelo de nuevo")

        if action not in ["M", "D"]:
            print("Ha introducido una acción no válida, por favor intentelo de nuevo")
        else:
            return ("flag" if action == "M" else "show", coords)


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
