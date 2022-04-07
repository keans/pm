from draw.base import Position
from .row import Row


class Grid:
    """
    a fixed grid that is based on cells
    """
    def __init__(self, x, y):
        self.rows = []
        self.set_pos(x, y)

    def _update_positions(self):
        # update row positions
        height = 0
        for row in self.rows:
            row.set_pos(self.pos.x, self.pos.y + height)
            height += row.height

    def set_pos(self, x, y):
        self.pos = Position(x, y)
        self._update_positions()

    def add_row(self, row: Row):
        """
        add a row to the grid's rows
        """
        self.rows.append(row)
        self._update_positions()

    def set_text(self, row, col, text):
        """
        set text for specific coordinate
        """
        self.rows[row][col].text.text = text

    def set_fill(self, row, col, fill):
        """
        set background for specific coordinate
        """
        self.rows[row][col].fill = fill

    def get_cell(self, row, col):
        """
        get cell at specific coordinate
        """
        return self.rows[row][col]

    def draw(self, dwg, grp=None):
        grp = grp or dwg.g()

        # draw cells
        for row in self.rows:
            grp.add(row.draw(dwg, None))

        return grp
