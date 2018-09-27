from mocoma_minesweeper_src import ConsoleIO, MinesweeperGrid

io = ConsoleIO()
grid = MinesweeperGrid.gen_random(10, 10, 10)
while True:
    io.show_grid(grid)
    io.get_grid_input(grid.width, grid.height)

