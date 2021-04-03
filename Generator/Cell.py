class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.north = True
        self.south = True
        self.east = True
        self.west = True
        self.visited = False
        self.is_entry = False
        self.is_exit = False

    def _set_entry(self, row_limit, col_limit):
        if self.row == 0:
            self.north = False
        elif self.row == row_limit:
            self.south = False
        elif self.col == 0:
            self.west = False
        elif self.col == col_limit:
            self.east = False

        self.is_entry = True

    def _set_exit(self, row_limit, col_limit):
        if self.row == 0:
            self.north = False
        elif self.row == row_limit:
            self.south = False
        elif self.col == 0:
            self.west = False
        elif self.col == col_limit:
            self.east = False

        self.is_exit = True

