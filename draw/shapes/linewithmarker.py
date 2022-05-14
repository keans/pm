from svgwrite import Drawing
from svgwrite.container import Group

from draw.base import Dimension
from draw.shapes import Label


class LineWithMarker(Dimension):
    """
    line with marker at the end
    """
    def __init__(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        text: str = "",
        text_anchor: str = "middle",
        text_alignment_baseline: str = "middle",
        class_: str = "linewithmarker"
    ):
        Dimension.__init__(self, x1, y1, x2 - x1, y2 - y1)

        # prepare text
        self.text = Label(
            x=0,
            y=0,
            text=text,
            text_anchor=text_anchor,
            text_dominant_baseline=text_alignment_baseline,
            class_=class_
        )

        self.class_ = class_

    def set_xy(self, x: int, y: int):
        """
        set line position
        """

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

    def draw(self, dwg: Drawing, grp: Group = None) -> Group:
        """
        draw line with marker and return it as group

        :param dwg: drawing used to draw the items
        :type dwg: Drawing
        :param grp: group, defaults to None
        :type grp: Group, optional
        :return: group with drawn items
        :rtype: Group
        """
        grp = grp or dwg

        # grp.add(path)

        return grp

    def __repr__(self) -> str:
        """
        returns the string representation of the line with marker

        :return: string representation of the line with marker
        :rtype: str
        """
        return (
            f"<LineWithMarker(x1={self.x1}, y1={self.y1}, "
            f"x2={self.x2}, y2={self.y2})>"
        )
