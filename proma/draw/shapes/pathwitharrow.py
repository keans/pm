from typing import Optional

from svgwrite import Drawing
from svgwrite.container import Group
from svgwrite.path import Path

from proma.draw.base import Dimension


class PathWithArrow(Dimension):
    """
    path with an arrow at the tail
    """

    def __init__(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        arrow_size: int = 6,
        class_: str = "defaultpathwitharrow",
    ):
        Dimension.__init__(self, x1, y1, x2 - x1, y2 - y1)

        self.arrow_size = arrow_size
        self.class_ = class_

    def draw(
        self,
        dwg: Drawing,
        grp: Optional[Group] = None,
    ) -> Group:
        """
        draw path with arrow and return it as group

        :param dwg: drawing used to draw the items
        :type dwg: Drawing
        :param grp: group, defaults to None
        :type grp: Group, optional
        :return: group with drawn items
        :rtype: Group
        """
        grp = grp or dwg

        # prepare arrow marker
        arrow = dwg.marker(
            id="arrow",
            insert=(1, self.arrow_size / 2),
            size=(self.arrow_size, self.arrow_size),
            orient="auto",
            markerUnits="strokeWidth",
        )
        arrow.viewbox(width=self.arrow_size, height=self.arrow_size)
        arrow.add(
            dwg.polyline(
                [
                    (0, 0),
                    (self.arrow_size, self.arrow_size / 2),
                    (0, self.arrow_size),
                    (1, self.arrow_size / 2),
                ],
            )
        )
        dwg.defs.add(arrow)

        h = (self.y2 - self.y1) * 0.5

        path = Path(
            d=("M", self.x1 - 2, self.y1), **{"marker-end": "url(#arrow)"}
        )
        path.push("L", self.x1 + 5, self.y1)

        if self.x1 >= self.x2:
            # same x position => go down and back
            path.push("L", self.x1 + 5, self.y1 + h + 1)
            path.push("L", self.x2 - 5, self.y1 + h + 1)
            path.push("L", self.x2 - 5, self.y2 + 1)
            path.push("L", self.x2 - 2, self.y2 + 1)

        else:
            # far away x position => simply go down
            path.push("L", self.x1 + 5, self.y2)
            path.push("L", self.x2 - 2, self.y2)

        grp.add(path)

        return grp

    def __repr__(self) -> str:
        """
        returns the string representation of the path with arrow

        :return: string representation of the path with arrow
        :rtype: str
        """
        return (
            f"<PathWithArrow(x1={self.x1}, y1={self.y1}, "
            f"x2={self.x2}, y2={self.y2}, "
            f"arrow_size={self.arrow_size})>"
        )
