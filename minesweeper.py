from mocoma_minesweeper_src import ConsoleIO, MinesweeperGrid, MinesweeperGame, PygameIO
from math import ceil
from random import randint

io = ConsoleIO()
hardness_levels = {
    "facil": 0.07,
    "medio": 0.10,
    "dificil": 0.15,
    "extremo": 0.20,
    "infierno": 0.25
}
width, height = io.get_user_dimensions()
hardness = io.get_user_hardness(hardness_levels)
n_mines = ceil(width * height * hardness_levels[hardness])
grid = MinesweeperGrid.gen_random(width, height, n_mines)

game = MinesweeperGame(grid, io)
game.play_until_end()

io.print_end(grid)
