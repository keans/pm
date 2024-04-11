from typing import Optional, Iterator

from svgwrite import Drawing
from svgwrite.container import Group

from proma.draw.base import Position, Margin, Padding
from proma.draw.base.consts import (
    DEFAULT_MARGIN,
    DEFAULT_PADDING,
    DEFAULT_CELL_HEIGHT,
    DEFAULT_CELL_WIDTH,
    TextAnchor,
    TextDominantBaseline,
)
from proma.draw.shapes import Cell


class GridRow(Position):
    """
    row in a grid
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        row_height: int = DEFAULT_CELL_HEIGHT,
    ):
        self.row_height = row_height
        self.cells = []

        Position.__init__(self, x=x, y=y)

    @property
    def width(self) -> int:
        """
        width of the row

        :return: width
        :rtype: int
        """
        return sum([cell.width for cell in self.cells])

    @property
    def height(self) -> int:
        """
        height of the row

        :return: height
        :rtype: int
        """
        if len(self.cells) == 0:
            return 0

        return self.cells[0].height

    def __len__(self) -> int:
        """
        returns the number of columns

        :return: number of columns
        :rtype: int
        """
        return len(self.cells)

    def __getitem__(
        self,
        col: int,
    ) -> Cell:
        """
        return cell by given column

        :param col: column
        :type col: int
        :return: cell in row
        :rtype: Cell
        """
        if col >= len(self.cells):
            # invalid column
            raise ValueError(f"Invalid column {col} in {self}! Abort.")

        return self.cells[col]

    def __next__(self) -> Iterator[Cell]:
        """
        return next cell

        :yield: cell
        :rtype: Iterator[Cell]
        """
        yield from self.cells

    def set_xy(
        self,
        x: int,
        y: int,
    ):
        """
        set new position and update corresponding cells

        :param x: x
        :type x: int
        :param y: y
        :type y: int
        """
        Position.set_xy(self, x=x, y=y)
        self._update_positions()

    def _update_positions(self):
        """
        update the positions of the children cells
        """
        width = 0
        for cell in self.cells:
            cell.set_xy(self.x + width, self.y)
            width += cell.width

    def add_cell(
        self,
        cell_width: int = DEFAULT_CELL_WIDTH,
        text: str = "",
        text_anchor: TextAnchor = TextAnchor.MIDDLE,
        text_alignment_baseline: TextDominantBaseline = (
            TextDominantBaseline.CENTRAL
        ),
        margin: Margin = DEFAULT_MARGIN,
        padding: Padding = DEFAULT_PADDING,
        class_: str = "defaultcell",
    ) -> Cell:
        """
        add a cell to a row

        :param cell_width: width of the cell, defaults to DEFAULT_CELL_WIDTH
        :type cell_width: int, optional
        :param text: text for cell, defaults to ""
        :type text: str, optional
        :param text_anchor: horizontal alignment, defaults to "middle"
        :type text_anchor: TextAnchor, optional
        :param text_alignment_baseline: vertical alignment,
                                        defaults to "middle"
        :type text_alignment_baseline: TextDominantBaseline, optional
        :param margin: margin, defaults to DEFAULT_MARGIN
        :type margin: Margin, optional
        :param padding: padding, defaults to DEFAULT_PADDING
        :type padding: Padding, optional
        :param class_: CSS class, defaults to "defaultcell"
        :type class_: str, optional
        :return: created cell
        :rtype: Cell
        """
        cell = Cell(
            x=0,
            y=0,
            width=cell_width,
            height=self.row_height,
            text=text,
            text_anchor=text_anchor,
            text_alignment_baseline=text_alignment_baseline,
            margin=margin,
            padding=padding,
            class_=class_,
        )
        self.cells.append(cell)

        # update cell positions
        self._update_positions()

        return cell

    def add_cols(
        self,
        col_count: int,
        cell_width: int = DEFAULT_CELL_WIDTH,
        text: str = "",
        class_: str = "defaultcell",
    ):
        """
        add multiple columns of same style to the row

        :param col_count: number of columns to create
        :type col_count: int
        :param cell_width: width of the cells, defaults to DEFAULT_CELL_WIDTH
        :type cell_width: int, optional
        :param text: text for the cells, defaults to ""
        :type text: str, optional
        :param class_: CSS class, defaults to "defaultcell"
        :type class_: str, optional
        """
        for _ in range(col_count):
            self.add_cell(cell_width=cell_width, text=text, class_=class_)

    def draw(
        self,
        dwg: Drawing,
        grp: Optional[Group] = None,
    ) -> Group:
        """
        draw row and return it as group

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
        for cell in self.cells:
            grp.add(cell.draw(dwg, None))

        return grp

    def __repr__(self):
        return (
            f"<GridRow(x={self.x}, y={self.y}, "
            f"row_height={self.row_height}, cells={len(self.cells)})>"
        )
