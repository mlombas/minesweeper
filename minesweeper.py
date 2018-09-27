from mocoma_minesweeper_src import Console_IO, Minesweeper_Grid

io = Console_IO()
grid = Minesweeper_Grid.gen_random(10, 10, 10)
while True:
    io.show_grid(grid)
    io.get_input(grid.width, grid.height)

