from draw.base import Position, BorderStyle

from .cell import DEFAULT_CELL_HEIGHT, DEFAULT_CELL_WIDTH, \
    DEFAULT_CELL_STROKE_STYLE, DEFAULT_CELL_FILL, Cell


class Row:
    """
    row in a grid
    """
    def __init__(self, x=0, y=0, row_height=DEFAULT_CELL_HEIGHT):
        self.row_height = row_height
        self.cells = []
        self.set_pos(x, y)

    @property
    def width(self):
        """
        width of the row
        """
        return sum([cell.width for cell in self.cells])

    @property
    def height(self):
        """
        height of the row
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

    def __getitem__(self, col):
        """
        return cell by given column
        """
        print(col)
        return self.cells[col]

    def __next__(self):
        yield from self.cells

    def _update_positions(self):
        """
        update the positions of the children cells
        """
        width = 0
        for cell in self.cells:
            cell.set_pos(self.pos.x + width, self.pos.y)
            width += cell.width

    def set_pos(self, x, y):
        """
        set position
        """
        self.pos = Position(x, y)
        self._update_positions()

    def add_cell(
        self, cell_width=DEFAULT_CELL_WIDTH, text="",
        fill=DEFAULT_CELL_FILL,
        stroke_style=DEFAULT_CELL_STROKE_STYLE
    ):
        """
        add a cell to a row
        """
        cell = Cell(
            x=0, y=0,
            width=cell_width, height=self.row_height,
            text=text,
            fill=fill,
            border_style=BorderStyle(
                stroke_style, stroke_style,
                stroke_style, stroke_style
            )
        )
        self.cells.append(cell)
        self._update_positions()

        return cell

    def add_cols(
        self, col_count, cell_width=DEFAULT_CELL_WIDTH, text="",
        fill=DEFAULT_CELL_FILL, stroke_style=DEFAULT_CELL_STROKE_STYLE
    ):
        """
        add multiple columns of same style to the row
        """
        for x in range(col_count):
            self.add_cell(cell_width, text, fill, stroke_style)

    def draw(self, dwg, grp=None):
        grp = grp or dwg.g()

        # draw cells
        for cell in self.cells:
            grp.add(cell.draw(dwg, None))

        return grp

    def __repr__(self):
        return f"GridRow(width={self.width}, heigh={self.height})"
