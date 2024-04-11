from typing import Optional

from svgwrite import Drawing
from svgwrite.container import Group

from proma.draw.base.dimension import Dimension


class Line(Dimension):
    """
    simple line with stroke style
    """

    def __init__(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        class_: str = "defaultline",
    ):
        Dimension.__init__(self, x1, y1, x2 - x1, y2 - y1)
        self.class_ = class_

    def draw(
        self,
        dwg: Drawing,
        grp: Optional[Group] = None,
    ) -> Group:
        """
        draw line and return it as group

        :param dwg: drawing used to draw the items
        :type dwg: Drawing
        :param grp: group, defaults to None
        :type grp: Group, optional
        :return: group with drawn items
        :rtype: Group
        """
        grp = grp or dwg

        grp.add(
            dwg.line(
                self.xy,
                self.x2y2,
                class_=self.class_,
            )
        )

        return grp

    def __repr__(self) -> str:
        """
        returns the string representation of the line

        :return: string representation of the line
        :rtype: str
        """
        return (
            f"<Line(x1={self.x1}, y1={self.y1}, "
            f"x2={self.x2}, y2={self.y2})>"
        )
