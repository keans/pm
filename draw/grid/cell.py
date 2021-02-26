from draw.base import DEFAULT_MARGIN, DEFAULT_PADDING, DEFAULT_TEXT_STYLE, \
    DEFAULT_BORDER_STYLE, StrokeStyle
from draw.shapes import Box, Text


# default cell dimensions
DEFAULT_CELL_WIDTH = 25
DEFAULT_CELL_HEIGHT = 25
DEFAULT_CELL_STROKE_STYLE = StrokeStyle("gray", 1, "round", "round", None)
DEFAULT_CELL_FILL = "white"


class Cell(Box):
    """
    a cell in a grid that can have different borders per side
    and contain a text
    """
    def __init__(
        self, x, y, width, height, text="",
        fill=DEFAULT_CELL_FILL,
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

    @property
    def width(self):
        return self.dimension.width

    @property
    def height(self):
        return self.dimension.height

    def set_pos(self, x, y):
        """
        set cell position
        """
        self.dimension.x = x
        self.dimension.y = y
        self.text.set_pos(self.dimension.cx, self.dimension.cy)

    def set_fill(self, fill):
        self.fill = fill

    def draw(self, dwg, grp=None):
        grp = grp or dwg.g()

        # draw box in background
        Box.draw(self, dwg, grp)

        # draw text on top
        if self.text.text != "":
            self.text.draw(dwg, grp)

        return grp

    def __repr__(self):
        return f"Cell(dimension={self.dimension})"
