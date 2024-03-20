from typing import Optional

from svgwrite import Drawing
from svgwrite.container import Group

from pm.draw.base import Margin, Padding, Dimension
from pm.draw.base.consts import DEFAULT_MARGIN, DEFAULT_PADDING
from pm.draw.shapes import Text


class Label(Dimension):
    """
    a text in a box
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str = "",
        text_anchor: str = "middle",
        text_dominant_baseline: str = "middle",
        margin: Margin = DEFAULT_MARGIN,
        padding: Padding = DEFAULT_PADDING,
        class_: str = "defaultlabel",
    ):
        self.padding = padding
        self.margin = margin

        # init text at (0,0) and move it later via dimension change
        self.text = Text(
            x=0,
            y=0,
            text=text,
            text_anchor=text_anchor,
            text_dominant_baseline=text_dominant_baseline,
            class_=class_,
        )

        Dimension.__init__(self, x, y, width, height)

    def _update(self):
        """
        update the text's position of the label
        """
        # align horizontal text
        if self.text.text_anchor == "start":
            text_x = self.x1 + self.padding.left

        elif self.text.text_anchor == "end":
            text_x = self.x2 - self.padding.right

        elif self.text.text_anchor == "middle":
            text_x = self.cx

        # align vertical text
        if self.text.text_dominant_baseline == "hanging":
            text_y = self.y1 + self.padding.top

        elif self.text.text_dominant_baseline == "auto":
            text_y = self.y2 - self.padding.bottom

        elif self.text.text_dominant_baseline == "middle":
            text_y = self.cy

        # set text position
        self.text.set_xy(text_x, text_y)

    def on_change_dimension(
        self,
        dimension: Dimension,
    ):
        """
        on dimension change adapt text

        :param pos: new dimension
        :type pos: Dimension
        """
        # on change of the label's dimension, update the text position
        self._update()

    def draw(
        self,
        dwg: Drawing,
        grp: Optional[Group] = None,
    ) -> Group:
        """
        draw label and return it as group

        :param dwg: drawing used to draw the items
        :type dwg: Drawing
        :param grp: group, defaults to None
        :type grp: Group, optional
        :return: group with drawn items
        :rtype: Group
        """
        grp = grp or dwg.g()
        self.text.draw(dwg, grp)

        return grp

    def __repr__(self) -> str:
        """
        returns the string representation of the label

        :return: string representation of the label
        :rtype: str
        """
        return (
            f"<Label(x={self.x}, y={self.y}, "
            f"width={self.width}, height={self.height}, "
            f"text='{self.text}')>"
        )
