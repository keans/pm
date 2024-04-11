from typing import Optional

from svgwrite import Drawing
from svgwrite.container import Group

from proma.draw.base import Position
from proma.draw.shapes import Cell
from proma.draw.widgets.grid.gridrow import GridRow


class Grid(Position):
    """
    a fixed grid that is based on cells
    """

    def __init__(
        self,
        x: int,
        y: int,
    ):
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

    def _check_row(self, row: int, col: int) -> None:
        """
        check for valid row and col number
        if it is invalid, a ValueError is raised

        :param row: row number
        :type row: int
        :param col: column number
        :type col: int
        :raises ValueError: if row or col is not existing
        """
        if row >= len(self.rows):
            # wrong row number
            raise ValueError(
                f"The row '{row}' is not existing in {self.rows}! Abort."
            )

        if col >= len(self.rows[row]):
            # wrong col number
            raise ValueError(
                f"The col '{col}' is not existing in {self.rows[row]}! Abort."
            )

    def add_row(self, row: GridRow):
        """
        add a row to the grid's rows

        :param row: grid row
        :type row: GridRow
        """
        self.rows.append(row)
        self._update_positions()

    def set_text(
        self,
        row: int,
        col: int,
        text: str,
    ):
        """
        set text for specific coordinate

        :param row: row number
        :type row: int
        :param col: column number
        :type col: int
        :param text: text set to cell
        :type text: str
        """
        self._check_row(row, col)

        self.rows[row][col].text.text = text

    def set_fill(
        self,
        row: int,
        col: int,
        fill: str,
    ):
        """
        set background for specific coordinate

        :param row: row number
        :type row: int
        :param col: column number
        :type col: int
        :param fill: background color
        :type fill: str
        """
        self._check_row(row, col)

        self.rows[row][col].fill = fill

    def get_cell(
        self,
        row: int,
        col: int,
    ) -> Cell:
        """
        get cell at specific coordinate

        :param row: row
        :type row: int
        :param col: column
        :type col: int
        :return: cell at given position
        :rtype: Cell
        """
        self._check_row(row, col)

        return self.rows[row][col]

    def draw(
        self,
        dwg: Drawing,
        grp: Optional[Group] = None,
    ) -> Group:
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
