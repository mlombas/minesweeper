"""Provides main functionality of the minesweeper

You can use this module to create your own version of minesweeper
provides a Minesweeper_Grid to store the mine grid and several
classes for IO
"""

from abc import ABC, abstractmethod
from collections import namedtuple
from random import randint

class MinesweeperIO(ABC):
    """Parent class for those who controls IO

    This provides a default interface so swapping
    between various IO (console, frame, HTML server, etc) is
    far simpler.
    This class is abstract and thus can not be instantied
    """

    @abstractmethod
    def show_grid(self, grid):
        """Shows the grid to the viewing port

        Input:
            grid - a instance of the Minesweeper_Grid class, that will be
                displayed on the viewing port

        Output: None
        """
        pass

    @abstractmethod
    def get_grid_input(self, g_width, g_height):
        """Asks the user to chose an action and a tile

        Input:
            g_width - the width of the grid
            g_height - the height of the grid

        Output:
            A tuple in the form (action, coords)
            action is either "flag" or "show", represents the action the user wants to take
            coords is a tuple representing the x and y coordinates on the grid
        """
        pass


class ConsoleIO(MinesweeperIO):
    """Provides a minesweeper inyterface for cmd
    See IO_Controller for more details
    """

    def show_grid(self, grid):
        out = []
        for y in range(grid.height):
            line = ""
            for x in range(grid.width):
                mine_c, hidden_c, flagged_c, empty_c = "M", "■", "!", "□"
                cell = grid.get_cell(x, y)
                if cell.state == "hidden":
                    line += hidden_c
                elif cell.state == "flagged":
                    line += flagged_c
                elif cell.state == "shown":
                    if cell.has_mine:
                        line += mine_c
                    else:
                        n_around = grid.n_mines_around(x, y)
                        line += str(n_around) if n_around else empty_c

                line += " "

            out.append(line)

        print("\n".join(out))
        print("=" * (grid.width * 2))

    def get_grid_input(self, g_width, g_height):
        print("Introduce D para descubrir y M para marcar, seguido de las coordenadas de la celda separadas por una coma")
        while True:
            action, coords = input().split() #TODO prevent user from introducing only one value 
            try:
                coords = (int(c) - 1 for c in coords.split(","))
            except:
                print("Ha introducido unas coordenadas no validas, por favor intentelo de nuevo")

            if action not in ["M", "D"]:
                print("Ha introducido una acción no válida, por favor intentelo de nuevo")
            else:
                return ("flag" if action == "M" else "show", coords)

    def print_end(self, won=False):
        if won:
            print("You won motherfucker")
        else:
            print("You lost pussy")

class MinesweeperGrid(object):
    """Provides support for storing a mine grid

    Also provides several methods to manipulate it and a classmethod
    to instantly create a grid with mines in random positions

    Attributes:
        _cells - The cell list, DO NOT TOUCH THIS LIST, use the get_cell() asnd set_cell() instead
        Cell - A class representing a cell of the grid
    """

    _cells = []
    Cell = namedtuple("Cell", ("has_mine", "state"))

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._cells = [self.Cell(False, "hidden")] * (width * height)

    @classmethod
    def gen_random(cls, width, height, n_mines):
        """Creates a grid with mines in random positions

        Input:
            width - the width of the grid
            height - the height of the grid
            n_mines - the number of mines
        
        Output:
            The random grid
        """
        def get_random_point():
            return (randint(0, width - 1), randint(0, height - 1))
        
        grid = cls(width, height)
        while n_mines:
            x, y = get_random_point()
            while grid.get_cell(x, y).has_mine:
                x, y = get_random_point()

            grid.put_mine(x, y)
            n_mines -= 1

        return grid

    def coords_in_grid(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height
            
    
    def get_cell(self, x, y):
        """Returns a cell of the grid

        Input:
            x - the x coordinate of the cell
            y - the y coordinate of the cell
        
        Output:
            The cell, an instance of the Cell class
        """
        return self._cells[y * self.height + x]

    def set_cell(self, x, y, cell):
        """Sets a cell on the grid

        Input:
            x - the x coordinate of the cell
            y - the y coordinate of the cell
            cell - the new cell, an instance of the Cell class
        
        Output: None
        """
        self._cells[y * self.height + x] = cell

    def put_mine(self, x, y):
        """Puts a mine in the grid

        Input:
            x - the x coordinate of the cell
            y - the y coordinate of the cell
        
        Output: None
        """
        c = self.get_cell(x, y)
        new_c = self.Cell(True, c.state)
        self.set_cell(x, y, new_c)

    def show_cell(self, x, y):
        """Shows a cell, this is its state changes to "shown"

        Input:
            x - the x coordinate of the cell
            y - the y coordinate of the cell
        
        Output: None
        """
        c = self.get_cell(x, y)
        new_c = self.Cell(c.has_mine, "shown")
        self.set_cell(x, y, new_c)

    def show_empty_cells(self, x, y):
        self.show_cell(x, y)
        n_around = self.n_mines_around(x, y)
        if n_around == 0:
            self.show_cell(x, y)
            coords_around = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for coord in coords_around:
                if self.coords_in_grid(*coord) and self.get_cell(*coord).state == "hidden":
                    self.show_empty_cells(*coord)

    def flag_cell(self, x, y):
        """Flags a cell, this is its state changes to "flagged"

        Input:
            x - the x coordinate of the cell
            y - the y coordinate of the cell
        
        Output: None
        """
        c = self.get_cell(x, y)
        new_c = self.Cell(c.has_mine, "flagged")
        self.set_cell(x, y, new_c)

    def hide_cell(self, x, y):
        """Hides a cell, this is its state changes to "hidden"

        Input:
            x - the x coordinate of the cell
            y - the y coordinate of the cell
        
        Output: None
        """
        c = self.get_cell(x, y)
        new_c = self.Cell(c.has_mine, "hidden")
        self.set_cell(x, y, new_c)

    def is_loss(self):
        return any([cell.has_mine and cell.state == "shown" for cell in self._cells])

    def is_win(self):
        return all([(cell.has_mine and cell.state == "flagged") or not cell.has_mine
                        for cell in self._cells])

    def ended(self):
        return self.is_loss() or self.is_win()
    
    def n_mines_around(self, x, y):
        count = 0
        for dx in range(max(0, x - 1), min(x + 2, self.width)):
            for dy in range(max(0, y - 1), min(y + 2, self.height)):
                if (dx != x or dy != y) and self.get_cell(dx, dy).has_mine:
                    count += 1

        return count
