from random import randint, choice
from Cell import Cell
from PIL import Image, ImageDraw


class Maze:
    def __init__(self, width=20, height=20, cell_width=20):
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cells = []
        self.entry = self._set_cell_state()
        self.exit = self._set_cell_state(self.entry)

    def get_distance(self, x, y):
        h = abs(x[1] - x[0])
        v = abs(y[0] - y[1])
        return h + v

    def _set_cell_state(self, used=[0, 0]):
        state = used
        while state == used and self.get_distance(state, used) <= self.cell_width * 2:
            side = randint(0, 3)

            if side == 0:  # north
                state = (0, randint(0, self.width - 1))
            elif side == 1:  # south
                state = (randint(0, self.height - 1), self.width - 1)
            elif side == 2:  # east
                state = (self.height - 1, randint(0, self.width - 1))
            elif side == 3:  # west
                state = (randint(0, self.height - 1), 0)
        return state

    def generate(self):
        self.cells = list()
        for i in range(self.height):
            self.cells.append(list())
            for j in range(self.width):
                self.cells[i].append(Cell(i, j))

        x, y = choice(range(self.width)), choice(range(self.height))
        self.cells[x][y].visited = True
        path = [(x, y)]

        while not all(all(c.visited for c in cell) for cell in self.cells):
            x, y = path[len(path) - 1][0], path[len(path) - 1][1]

            good_adj_cells = []
            if self.exists(x, y - 1) and not self.cells[x][y - 1].visited:
                good_adj_cells.append('north')
            if self.exists(x, y + 1) and not self.cells[x][y + 1].visited:
                good_adj_cells.append('south')
            if self.exists(x + 1, y) and not self.cells[x + 1][y].visited:
                good_adj_cells.append('east')
            if self.exists(x - 1, y) and not self.cells[x - 1][y].visited:
                good_adj_cells.append('west')

            if good_adj_cells:
                go = choice(good_adj_cells)
                if go == 'north':
                    self.cells[x][y].north = False
                    self.cells[x][y - 1].south = False
                    self.cells[x][y - 1].visited = True
                    path.append((x, y - 1))
                if go == 'south':
                    self.cells[x][y].south = False
                    self.cells[x][y + 1].north = False
                    self.cells[x][y + 1].visited = True
                    path.append((x, y + 1))
                if go == 'east':
                    self.cells[x][y].east = False
                    self.cells[x + 1][y].west = False
                    self.cells[x + 1][y].visited = True
                    path.append((x + 1, y))
                if go == 'west':
                    self.cells[x][y].west = False
                    self.cells[x - 1][y].east = False
                    self.cells[x - 1][y].visited = True
                    path.append((x - 1, y))
            else:
                path.pop()
        self.cells[self.entry[0]][self.entry[1]]._set_entry(self.height - 1, self.width - 1)
        self.cells[self.exit[0]][self.exit[1]]._set_exit(self.height - 1, self.width - 1)

    def exists(self, x, y):
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return False
        return True

    def draw(self):
        canvas_width, canvas_height = self.cell_width * self.width, self.cell_width * self.height
        im = Image.new('RGB', (canvas_width, canvas_height), color="white")
        draw = ImageDraw.Draw(im)

        for x in range(self.width):
            for y in range(self.height):
                if self.cells[x][y].is_entry:
                    print("Start = (X: %s Y: %s)" % (y * self.cell_width, x * self.cell_width))
                    draw.rectangle((y * self.cell_width - 2, x * self.cell_width - 2, (y + 1) * self.cell_width - 2,
                                    (x + 1) * self.cell_width - 2), fill="green")
                elif self.cells[x][y].is_exit:
                    print("End = (X: %s Y: %s)" % (y * self.cell_width, x * self.cell_width))
                    draw.rectangle((y * self.cell_width - 2, x * self.cell_width - 2, (y + 1) * self.cell_width - 2,
                                    (x + 1) * self.cell_width - 2), fill="red")

                if self.cells[x][y].north:
                    draw.line(
                        (x * self.cell_width, y * self.cell_width, (x + 1) * self.cell_width, y * self.cell_width),
                        fill="black", width=5)
                if self.cells[x][y].south:
                    draw.line((x * self.cell_width, (y + 1) * self.cell_width, (x + 1) * self.cell_width,
                               (y + 1) * self.cell_width), fill="black", width=5)
                if self.cells[x][y].east:
                    draw.line(((x + 1) * self.cell_width, y * self.cell_width, (x + 1) * self.cell_width,
                               (y + 1) * self.cell_width), fill="black", width=5)
                if self.cells[x][y].west:
                    draw.line(
                        (x * self.cell_width, y * self.cell_width, x * self.cell_width, (y + 1) * self.cell_width),
                        fill="black", width=5)
        im.show()


if __name__ == '__main__':
    maze = Maze(width=20, height=20, cell_width=20)
    maze.generate()
    maze.draw()
