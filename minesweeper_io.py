from abc import ABC, abstractmethod

class IO_Controller(ABC):
    @abstractmethod
    def show_grid(self, grid):
        pass

    @abstractmethod
    def get_input(self, g_width, g_height):
        pass


class Console_IO(IO_Controller):
    def show_grid(self, grid):
        out = []
        for y in range(grid.height):
            line = ""
            for x in range(grid.width):
                bomb_c, hidden_c, flagged_c, empty_c = "B", "■", "!", "□"
                cell = grid.get_cell(x, y)
                if cell.state == "hidden":
                    line += hidden_c
                elif cell.state == "flagged":
                    line += flagged_c
                elif cell.state == "shown":
                    line += bomb_c if cell.has_bomb else empty_c

                line += " "

            out.append(line)

        print("\n".join(out))
        print("=" * (grid.width * 2))

    def get_input(self, g_width, g_height):
        print("Introduce D para descubrir y M para marcar, seguido de las coordenadas de la celda separadas por una coma")
        while True:
            action, coords = input().split()
        try:
            coords = (int(c) for c in coords.split(","))
        except:
            print("Ha introducido unas coordenadas no validas, por favor intentelo de nuevo")

        if action not in ["M", "D"]:
            print("Ha introducido una acción no válida, por favor intentelo de nuevo")
        else:
            return ("flag" if action == "M" else "show", coords)
