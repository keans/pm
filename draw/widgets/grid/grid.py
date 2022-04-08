from svgwrite import Drawing
from svgwrite.container import Group

from draw.base import Position
from draw.shapes import Cell
from draw.widgets.grid.gridrow import GridRow


class Grid(Position):
    """
    a fixed grid that is based on cells
    """
    def __init__(self, x: int, y: int):
        Position.__init__(self, x=x, y=y)

        self.rows = []

    def _update_positions(self):
        """
        update the grid's rows
        """
        height = 0
        for row in self.rows:
            row.set_xy(self.x, self.y + height)
            height += row.height

    def add_row(self, row: GridRow):
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

    def get_cell(self, row: int, col: int) -> Cell:
        """
        get cell at specific coordinate

        :param row: row
        :type row: int
        :param col: column
        :type col: int
        :return: cell at given position
        :rtype: Cell
        """
        return self.rows[row][col]

    def draw(self, dwg: Drawing, grp: Group = None) -> Group:
        """
        draw grid and return it as group

        :param dwg: drawing
        :type dwg: Drawing
        :param grp: group, defaults to None
        :type grp: Group, optional
        :return: group
        :rtype: Group
        """
        # get group
        grp = grp or dwg.g()

        # draw cells
        for row in self.rows:
            grp.add(row.draw(dwg, None))

        return grp
