from mocoma_minesweeper_src import ConsoleIO, MinesweeperGrid, MinesweeperGame, PygameIO
from math import ceil
from random import randint

io = PygameIO()
grid = MinesweeperGrid.gen_random(10, 10, 20)
for x in range(10):
    for y in range(10):
        n = randint(0, 2)
        if n == 0: grid.show_cell(x, y)
        elif n == 1: grid.flag_cell(x, y)

MinesweeperGame(grid, io).play_until_end()

"""hardness_levels = {
    "facil": 0.07,
    "medio": 0.10,
    "dificil": 0.15,
    "extremo": 0.20,
    "infierno": 0.25
}
width, height = io.get_user_dimensions()
hardness = io.get_user_hardness(hardness_levels)
n_mines = ceil(width * height * hardness)
grid = MinesweeperGrid.gen_random(width, height, n_mines)

game = MinesweeperGame(grid, io)
game.play_until_end()

io.show_grid(grid)
io.print_end(grid.is_win())"""
