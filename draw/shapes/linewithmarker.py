from svgwrite import Drawing
from svgwrite.container import Group

from draw.base import Dimension
from draw.shapes import Line, Label


class LineWithMarker(Line):
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
        text_alignment_baseline: str = "auto",
        text_y_offset = 20,
        class_: str = "linewithmarker"
    ):
        Line.__init__(self, x1, y1, x1, y2)

        # prepare text
        self.label = Label(
            x=0,
            y=0,
            width=0,
            height=0,
            text=text,
            text_anchor=text_anchor,
            text_dominant_baseline=text_alignment_baseline,
            class_=class_
        )
        self.notify(dimension=self)

        self.class_ = class_

    def on_change_dimension(self, dimension: Dimension):
        """
        on dimension change adapt text

        :param pos: new dimension
        :type pos: Dimension
        """
        self.label.set_xy(dimension.x, dimension.y)
        self.label.set_wh(dimension.width, dimension.height + 25)

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
        grp = grp or dwg.g()

        # draw line
        Line.draw(self, dwg, grp)

        # draw text
        if self.label.text != "":
            self.label.draw(dwg, grp)

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
