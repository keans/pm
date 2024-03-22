from typing import Optional

from svgwrite import Drawing
from svgwrite.container import Group

from pm.draw.base import Margin, Padding, Dimension
from pm.draw.base.consts import (
    DEFAULT_MARGIN,
    DEFAULT_PADDING,
    DEFAULT_CELL_FILL,
)
from pm.draw.shapes import Box, Label


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
        text_anchor: str = "middle",
        text_alignment_baseline: str = "middle",
        margin: Margin = DEFAULT_MARGIN,
        padding: Padding = DEFAULT_PADDING,
        class_: str = "defaultcell",
    ):
        Box.__init__(
            self,
            x=x,
            y=y,
            width=width,
            height=height,
            fill=fill,
            margin=margin,
            padding=padding,
            class_=class_,
        )

        # prepare text
        self.label = Label(
            x=0,
            y=0,
            width=width,
            height=height,
            text=text,
            text_anchor=text_anchor,
            text_dominant_baseline=text_alignment_baseline,
            class_=class_,
        )

    def on_change_dimension(
        self,
        dimension: Dimension,
    ):
        """
        on dimension change adapt text

        :param pos: new dimension
        :type pos: Dimension
        """
        self.label.set(dimension)

    def set_fill(self, fill):
        self.fill = fill

    def draw(
        self,
        dwg: Drawing,
        grp: Optional[Group] = None,
    ) -> Group:
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
        if self.label.text != "":
            self.label.draw(dwg, grp)

        return grp

    def __repr__(self) -> str:
        """
        returns the string representation of the cell

        :return: string representation of the cell
        :rtype: str
        """
        return (
            f"<Cell(x1={self.x1}, y1={self.y1}, "
            f"x2={self.x2}, y2={self.y2}, text='{self.label.text}')>"
        )
