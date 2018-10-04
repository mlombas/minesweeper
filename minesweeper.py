from mocoma_minesweeper_src import ConsoleIO, MinesweeperGrid, MinesweeperGame
from math import ceil

io = ConsoleIO()
hardness_levels = {
    "facil": 0.07,
    "medio": 0.10,
    "dificil": 0.15,
    "extremo": 0.20,
    "infierno": 0.25
}
dimensions, hardness = io.get_user_dimensions(hardness_levels)
n_mines = ceil(dimensions[0] * dimensions[1] * hardness)
grid = MinesweeperGrid.gen_random(*dimensions, n_mines)
game = MinesweeperGame(grid, io)
game.play_until_end()

io.show_grid(grid)
io.print_end(grid.is_win())
