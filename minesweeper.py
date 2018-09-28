from mocoma_minesweeper_src import ConsoleIO, MinesweeperGrid

io = ConsoleIO()
grid = MinesweeperGrid.gen_random(3, 3, 1)
while not grid.is_loss() or not grid.is_win():
    io.show_grid(grid)
    action, coords = io.get_grid_input(grid.width, grid.height)
    if action == "flag":
        grid.flag_cell(*coords)
    elif action == "show":
        grid.show_empty_cells(*coords)

    print(grid.is_loss(), grid.is_win())

io.print_end(won=grid.is_won())

