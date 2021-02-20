import svgwrite

from svgwrite.base import BaseElement
from svgwrite.mixins import Presentation, Markers, Transform

from draw.base import DEFAULT_MARGIN, DEFAULT_PADDING, DEFAULT_STROKE_STYLE, \
    DEFAULT_BORDER_STYLE, Dimension, Position, BorderStyle, StrokeStyle, \
        Size, Margin, DEFAULT_TEXT_STYLE
from draw.shapes import Box, Bar, Text


class Cell(Box):
    """
    a cell in a grid that can have different borders per side
    and contain a text
    """
    def __init__(
        self, x, y, width, height, text="", fill="white",
        border_style=DEFAULT_BORDER_STYLE, 
        text_style=DEFAULT_TEXT_STYLE, 
        text_anchor="middle", text_alignment_baseline="middle",
        margin=DEFAULT_MARGIN, padding=DEFAULT_PADDING, 
    ):
        Box.__init__(
            self, x, y, width, height, fill, border_style, margin, padding
        )

        # prepare text
        self.text = Text(
            self.dimension.cx, self.dimension.cy, 
            text, text_style, text_anchor, text_alignment_baseline
        )

    def draw(self, dwg, grp=None):
        grp = grp or dwg.g()
        
        # draw box in background
        Box.draw(self, dwg, grp)

        # draw text on top
        self.text.draw(dwg, grp)

        return grp


class Grid:
    """
    a fixed grid that is based on cells
    """
    def __init__(
        self, x, y, rows, cols,
        cell_size=Size(25, 25),
        stroke_style=StrokeStyle("gray", 1, "round", "round", None), 
        fill="white"
    ):
        self.x = x 
        self.y = y
        self.rows = rows
        self.cols = cols
        self.fill = fill
        
        # prepare cells
        self.cells = {
            (i, k): Cell(
                x=x + k * cell_size.width, y=y + i * cell_size.height,
                width=cell_size.width, height=cell_size.height,
                text="",
                border_style=BorderStyle(
                    stroke_style, stroke_style, stroke_style, stroke_style
                )
            )
            for i in range(self.rows)
            for k in range(self.cols)
        }

    def set_text(self, row, col, text):
        """
        set text for specific coordinate
        """
        self.cells[(row, col)].text.text = text

    def set_fill(self, row, col, fill):
        """
        set background for specific coordinate
        """
        self.cells[(row, col)].fill = fill

    def get_cell(self, row, col):
        """
        get cell at specific coordinate
        """
        return self.cells[(row, col)]

    def draw(self, dwg, grp=None):
        grp = grp or dwg.g()

        # draw cells
        for cell in self.cells.values():
            grp.add(cell.draw(dwg, None))

        return grp


class GridWithBars(Grid):
    """
    a fixed grid that allows the placing of bars
    """
    def __init__(
        self, x, y, rows, cols,
        cell_size=Size(25, 25),
        stroke_style=StrokeStyle("gray", 1, "round", "round", None), 
        fill="white"
    ):
        Grid.__init__(self, x, y, rows, cols, cell_size, stroke_style, fill)
        self.bars = []

    def add_bar(self, position, length, fill="black"):
        """
        add bar to grid
        """
        position = Position(*position)
        start_cell = self.get_cell(*position)        
        end_cell = self.get_cell(position[0], position[1] + length)

        self.bars.append(
            Bar(
                start_cell.dimension.x, start_cell.dimension.y,
                width=end_cell.dimension.x2 - start_cell.dimension.x1,
                height=start_cell.dimension.height,
                fill=fill, margin=Margin(2, 2, 2, 2)
            )
        )

    def draw(self, dwg, grp=None):
        grp = Grid.draw(self, dwg, grp)

        # draw bars
        bars_grp = dwg.g()
        for bar in self.bars:
            bar.draw(dwg, bars_grp)
        grp.add(bars_grp)

        return grp
