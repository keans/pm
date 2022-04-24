from svgwrite import Drawing
from svgwrite.container import Group

from draw.base import Position


class Text(Position):
    """
    simple text
    """
    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        text_anchor: str = "middle",
        text_dominant_baseline: str = "middle",
        class_: str = "default_text"
    ):
        Position.__init__(self, x, y)

        self.text = text
        self.text_anchor = text_anchor
        self.text_dominant_baseline = text_dominant_baseline
        self.class_ = class_

    def draw(self, dwg: Drawing, grp: Group = None) -> Group:
        """
        draw text and return it as group

        :param dwg: drawing used to draw the items
        :type dwg: Drawing
        :param grp: group, defaults to None
        :type grp: Group, optional
        :return: group with drawn items
        :rtype: Group
        """
        grp = grp or dwg

        grp.add(
            dwg.text(
                text=self.text,
                insert=(self.x, self.y),
                text_anchor=self.text_anchor,
                dominant_baseline=self.text_dominant_baseline,
                class_=self.class_
            )
        )

        return grp

    def __repr__(self) -> str:
        """
        returns the string representation of the text

        :return: string representation of the text
        :rtype: str
        """
        return (
            f"<Text(x={self.x}, y={self.y}, "
            f"text='{self.text}')>"
        )
