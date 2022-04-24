from svgwrite import Drawing
from svgwrite.container import Group

#from draw.base import DEFAULT_MARGIN, DEFAULT_PADDING, DEFAULT_TEXT_STYLE, \
#    DEFAULT_BORDER_STYLE, BorderStyle, Margin, Padding, StrokeStyle, TextStyle
from draw.base import Margin, Padding, Dimension
from draw.base.consts import DEFAULT_MARGIN, DEFAULT_PADDING
from draw.shapes import Box, Text


# default cell dimensions
DEFAULT_CELL_WIDTH = 25
DEFAULT_CELL_HEIGHT = 25
#DEFAULT_CELL_STROKE_STYLE = StrokeStyle("gray", 1, "round", "round", None)
DEFAULT_CELL_FILL = "white"


class Cell(Box):
    """
    a cell in a grid that can have different borders per side
    and contain a text
    """
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str = "",
        fill: str = DEFAULT_CELL_FILL,
        # border_style: BorderStyle = DEFAULT_BORDER_STYLE,
        # text_style: TextStyle = DEFAULT_TEXT_STYLE,
        text_anchor: str = "middle",
        text_alignment_baseline: str = "middle",
        margin: Margin = DEFAULT_MARGIN,
        padding: Padding = DEFAULT_PADDING,
        class_: str = "defaultcell"
    ):
        Box.__init__(
            self,
            x=x,
            y=y,
            width=width,
            height=height,
            fill=fill,
            # border_style=border_style,
            margin=margin,
            padding=padding,
            class_=class_
        )

        # prepare text
        self.text = Text(
            x=0,
            y=0,
            text=text,
            text_anchor=text_anchor,
            text_dominant_baseline=text_alignment_baseline,
            class_=class_
        )

    def set_xy(self, x: int, y: int):
        """
        set cell position
        """
        Box.set_xy(self, x, y)

        # align horizontal text
        if self.text.text_anchor == "start":
            text_x = self.x1  + self.padding.left

        elif self.text.text_anchor == "end":
            text_x = self.x2 - self.padding.right

        elif self.text.text_anchor == "middle":
            text_x = self.cx

        # align vertical text
        if self.text.text_dominant_baseline == "hanging":
            text_y = self.y1 + self.padding.top

        elif self.text.text_dominant_baseline == "auto":
            text_y = self.y2 -  self.padding.bottom

        elif self.text.text_dominant_baseline == "middle":
            text_y = self.cy

        # set text position
        self.text.set_xy(text_x, text_y)

    def set_fill(self, fill):
        self.fill = fill

    def draw(self, dwg: Drawing, grp: Group = None) -> Group:
        """
        draw cell and return it as group

        :param dwg: drawing used to draw the items
        :type dwg: Drawing
        :param grp: group, defaults to None
        :type grp: Group, optional
        :return: group with drawn items
        :rtype: Group
        """
        grp = grp or dwg.g()

        # draw box in background
        Box.draw(self, dwg, grp)

        # draw text on top, if set
        if self.text.text != "":
            self.text.draw(dwg, grp)

        return grp

    def __repr__(self) -> str:
        """
        returns the string representation of the cell

        :return: string representation of the cell
        :rtype: str
        """
        return (
            f"<Cell(x1={self.x1}, y1={self.y1}, "
            f"x2={self.x2}, y2={self.y2}, text='{self.text}')>"
        )
