from mocoma_minesweeper_src import ConsoleIO, MinesweeperGrid, MinesweeperGame, PygameIO
from math import ceil
from random import randint

io = PygameIO()
width, height = io.get_user_dimensions()
grid = MinesweeperGrid.gen_random(width, height, width * height * 0.5)
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
