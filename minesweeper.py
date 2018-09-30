from mocoma_minesweeper_src import ConsoleIO, MinesweeperGrid

io = ConsoleIO()
grid = MinesweeperGrid.gen_random(10, 10, 10)
while not grid.ended():
    io.show_grid(grid)
    action, coords = io.get_grid_input(grid.width, grid.height)
    if action == "flag":
        grid.flag_cell(*coords)
    elif action == "show":
        grid.show_empty_cells(*coords)

io.show_grid(grid)
io.print_end(grid.is_win())
