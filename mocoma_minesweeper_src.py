"""Provides main functionality of the minesweeper

You can use this module to create your own version of minesweeper
provides a Minesweeper_Grid to store the mine grid and several
classes for IO
"""

from abc import ABC, abstractmethod
from collections import namedtuple
from random import randint
import pygame
from pygame.locals import *

class MinesweeperIO(ABC):
    """Parent class for those who controls IO

    This provides a default interface so swapping
    between various IO (console, frame, HTML server, etc) is
    far simpler.
    This class is abstract and thus can not be instantied
    """
    def __init__(self, hidden_src, empty_src, number_range_src, flagged_src, mine_src):
        self.hidden_src = hidden_src
        self.shown_src = [empty_src] + number_range_src
        self.flagged_src = flagged_src
        self.mine_src = mine_src

    @abstractmethod
    def print_end(self, won=False):
        """Prints to the player something to mark the end of the game

        Input:
            won - A boolean checking wether the game was won or not

        Output: None
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

    @abstractmethod
    def get_user_dimensions(self):
        pass

    @abstractmethod
    def get_user_hardness(self, hardness_levels):
        pass


class PygameIO(MinesweeperIO):
    def show_grid(self, grid):
        pass

    def get_grid_input(self, g_width, g_height):
        pass
    
    def get_user_dimensions(self):
        pass
    
    def get_user_hardness(self):
        pass


class ConsoleIO(MinesweeperIO):
    """Provides a minesweeper inyterface for cmd
    See IO_Controller for more details
    """

    def __init__(self, hidden_src = "■", empty_src="□", number_range_src=[str(n) for n in range(1, 10)], flagged_src="F", mine_src="M"):
        super().__init__(hidden_src, empty_src, number_range_src, flagged_src, mine_src)

    def show_grid(self, grid):
        out = []
        for y in range(grid.height):
            line = ""
            for x in range(grid.width):
                cell = grid.get_cell(x, y)
                if cell.state == "hidden":
                    line += self.hidden_src
                elif cell.state == "flagged":
                    line += self.flagged_src
                elif cell.state == "shown":
                    if cell.has_mine:
                        line += self.mine_src
                    else:
                        n_around = grid.n_mines_around(x, y)
                        line += self.shown_src[n_around]

                line += " "

            out.append(line)

        print("\n".join(out))
        print("=" * (grid.width * 2))

    def get_grid_input(self, g_width, g_height):
        print("Introduce D para descubrir y M para marcar, seguido de las coordenadas de la celda separadas por una coma")
        while True:
            try:
                action, coords = input().split(" ", maxsplit=1)
                coords = (int(c) - 1 for c in coords.split(","))
            except:
                print("Ha introducido una entrada no valida, por favor intentelo de nuevo")
            else:
                if action not in ["M", "D"]:
                    print("Ha introducido una acción no válida, por favor intentelo de nuevo")
                else:
                    return ("flag" if action == "M" else "show", coords)

    def get_user_dimensions(self):
        print("Introduzca las dimensiones del tablero en formato anchoxalto")
        while True:
            try:    
                width, height = (int(x) for x in input().split("x"))
            except:
                print("Ha introducido valores no válidos, intentelo de nuevo")
            else: break
            
        return (width, height)

    def get_user_hardness(self, hardness_levels):
        print("Elige un nivel de dificultad")
        for key in hardness_levels.keys():
            print(" " + key)

        lvl = input().strip()
        while lvl not in hardness_levels:
            print("Nivel no válido")
            lvl = input().strip()
        return hardness_levels[lvl]
    
    def print_end(self, won=False):
        possible_names = [
                            "amego", "wey", "boludo", "puto",
                            "compañero", "pringado", "parguela",
                            "sempai", "onee-chan", "baka"
                         ]
        name = possible_names[randint(0, len(possible_names) - 1)]
        if won:
            print("Ganaste", name)
        else:
            print("Perdiste", name)

        input("Pulsa enter para salir") 


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
    def gen_random(cls, width, height, n_mines, forbidden_coords=[]):
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
            while (x, y) in forbidden_coords and grid.get_cell(x, y).has_mine:
                x, y = get_random_point()

            grid.put_mine(x, y)
            n_mines -= 1

        return grid

    def coords_are_valid(self, x, y):
        """Checks wether a pair of coordinates is in the grid or not

        Input:
            x - The x coordinate
            y - The y coordinate

        Output:
            True if coords are valid, False otherwise
        """
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

    def clear_from(self, x, y):
        """Recrusively shows all the surrounding cells that don't have bombs nearby

        Input:
            x - The x coordinate of the cell
            y - The y coordinate of the cell

        Output: None
        """
        self.show_cell(x, y)
        n_around = self.n_mines_around(x, y)
        if n_around == 0:
            self.show_cell(x, y)
            coords_around = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for coord in coords_around:
                if self.coords_are_valid(*coord) and self.get_cell(*coord).state == "hidden":
                    self.clear_from(*coord)

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
        """Checks wether the game is lost or not

        Input: None
        Output:
            True if game is lost, False otherwise
        """
        return any([cell.has_mine and cell.state == "shown" for cell in self._cells])

    def is_win(self):
        """Checks wether the game is won or not

        Input: None
        Output:
            True if game is won, False otherwise
        """
        return all([(cell.has_mine and cell.state == "flagged") or (not cell.has_mine and cell.state != "flagged")
                        for cell in self._cells])

    def ended(self):
        """Check if the game has ended either winning it or lossing it
        
        Input: None
        Output:
            True if game has ended, False otherwise
        """
        return self.is_loss() or self.is_win()
    
    def n_mines_around(self, x, y):
        """Returns the number of mines surrounding the cell, itself included

        Input:
            x - The x coordinate of the cell
            y - The y coordinate of the cell

        Output:
            The number of mines
        """
        count = 0
        for dx in range(max(0, x - 1), min(x + 2, self.width)):
            for dy in range(max(0, y - 1), min(y + 2, self.height)):
                if self.get_cell(dx, dy).has_mine:
                    count += 1

        return count

    def get_n_mines(self):
        return len(cell for cell in self._cells if cell.has_mine == True)


class MinesweeperGame:
    grid = None
    io_controller = None

    def __init__(self, grid, io_controller):
        self.grid = grid
        self.io_controller = io_controller

    def do_action(self, action, coords):
        if action == "flag":
            self.grid.flag_cell(*coords)
        elif action == "show":
            self.grid.clear_from(*coords)

    def play_until_end(self):
        while not self.grid.ended():
            self.io_controller.show_grid(self.grid)
            action, coords = self.io_controller.get_grid_input(
                                self.grid.width,
                                self.grid.height
                            )
            self.do_action(action, coords)
        
    
