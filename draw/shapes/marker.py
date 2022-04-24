from svgwrite import Drawing
from svgwrite.container import Group
from svgwrite.shapes import Polygon, Circle, Rect

from draw.base import Dimension
from draw.shapes import Text


class Marker(Dimension):
    """
    marker symbol
    """

    # inspired by https://matplotlib.org/3.1.0/api/markers_api.html
    SUPPORTED_MARKERS = {
        "d": "_diamond",
        "o": "_circle",
        "s": "_square",
        "^": "_triangle",
        "v": "_triangle_down",
    }

    def __init__(
        self,
        symbol,
        cx: int,
        cy: int,
        width: int,
        height: int = None,
        text: str = "",
        fill: str = "black",
        text_anchor: str = "middle",
        text_alignment_baseline: str = "middle",
        text_x_offset: int = 0,
        text_y_offset: int = 0,
        class_: str = "defaultmarker"
    ):
        # store text offset -> used later during moving
        self._text_x_offset = text_x_offset
        self._text_y_offset = text_y_offset

        # prepare text at (0, 0)
        self.text = Text(
            x=0,
            y=0,
            text=text,
            text_anchor=text_anchor,
            text_dominant_baseline=text_alignment_baseline,
            class_=class_
        )

        Dimension.__init__(
            self,
            x=int(cx - width/2),
            y=int(cy - height/2),
            width=width,
            height=height
        )

        self.symbol = symbol
        self.fill = fill
        self.class_ = class_

    @property
    def symbol(self) -> str:
        """
        returns marker symbol

        :return: marker symbol (character)
        :rtype: str
        """
        return self._symbol

    @symbol.setter
    def symbol(self, value: str):
        """
        set the marker symbol

        :param value: marker symbol (see supported markers)
        :type value: str
        """
        assert isinstance(value, str) and len(value) == 1
        assert value in self.SUPPORTED_MARKERS

        self._symbol = value

    def on_dimension_changed(self, dim: "Dimension"):
        """
        react to dimension changes

        :param pos: new dimension
        :type pos: Dimension
        """
        # adapt position of the text to marker's center position
        self.text.set_xy(
            dim.cx + self._text_x_offset,
            dim.cy + self._text_y_offset
        )

    def _diamond(self, dwg: Drawing) -> Polygon:
        """
        returns diamond polygon

        :param dwg: drawing that is used to create the polygon
        :type dwg: Drawing
        :return: diamond polygon
        :rtype: Polygon
        """
        return dwg.polygon(
            [
                (
                    int(self.cx + self.width / 2),
                    self.cy
                ),
                (
                    self.cx,
                    int(self.cy - self.height / 2)
                ),
                (
                    int(self.cx + self.width/ 2),
                    self.cy
                ),
                (
                    int(self.cx),
                    int(self.cy + self.height / 2)
                ),
                (
                    int(self.cx - self.width/ 2),
                    self.cy
                ),
                (
                    int(self.cx),
                    int(self.cy - self.height / 2)
                )
            ],
            stroke="black",
            fill=self.fill,
            class_=self.class_
        )

    def _circle(self, dwg: Drawing) -> Circle:
        """
        returns circle

        :param dwg: drawing that is used to create the circle
        :type dwg: Drawing
        :return: circle
        :rtype: Circle
        """
        return dwg.circle(
            (
                self.cx,
                self.cy
            ),
            r=self.width / 2,
            stroke="black",
            fill=self.fill,
            class_=self.class_
        )

    def _square(self, dwg: Drawing) -> Rect:
        """
        returns rectangle

        :param dwg: drawing that is used to create the rectangle
        :type dwg: Drawing
        :return: rectangle
        :rtype: Rect
        """
        return dwg.rect(
            (
                self.cx - self.width / 2,
                self.cy - self.width / 2
            ),
            (
                self.width,
                self.width
            ),
            fill=self.fill,
            class_=self.class_
        )

    def _triangle(self, dwg: Drawing) -> Polygon:
        """
        returns triangle polygon

        :param dwg: drawing that is used to create the triangle
        :type dwg: Drawing
        :return: triangle polygon
        :rtype: Polygon
        """
        return dwg.polygon(
            [
                (
                    self.cx,
                    int(self.cy - self.height / 2)
                ),
                (
                    int(self.cx + self.width / 2),
                    int(self.cy + self.height / 2)
                ),
                (
                    int(self.cx - self.width / 2),
                    int(self.cy + self.height / 2)
                ),
            ],
            stroke="black",
            fill=self.fill,
            class_ = self.class_
        )

    def _triangle_down(self, dwg: Drawing) -> Polygon:
        """
        returns triangle down polygon

        :param dwg: drawing that is used to create the triangle down
        :type dwg: Drawing
        :return: triangle down polygon
        :rtype: Polygon
        """
        return dwg.polygon(
            [
                (
                    self.cx,
                    int(self.cy + self.height / 2)
                ),
                (
                    int(self.cx + self.width / 2),
                    int(self.cy - self.height / 2)
                ),
                (
                    int(self.cx - self.width / 2),
                    int(self.cy - self.height / 2)
                ),
            ],
            stroke="black",
            fill=self.fill,
            class_ = self.class_
        )

    def draw(self, dwg: Drawing, grp: Group = None) -> Group:
        """
        draw marker and return it as group

        :param dwg: drawing used to draw the items
        :type dwg: Drawing
        :param grp: group, defaults to None
        :type grp: Group, optional
        :return: group with drawn items
        :rtype: Group
        """
        grp = grp or dwg.g()

        if self.symbol == "d":
            # diamond
            grp.add(self._diamond(dwg))

        elif self.symbol == "o":
            # circle
            grp.add(self._circle(dwg))

        elif self.symbol == "s":
            # square
            grp.add(self._square(dwg))

        elif self.symbol == "^":
            # triangle
            grp.add(self._triangle(dwg))

        elif self.symbol == "v":
            # triangle
            grp.add(self._triangle_down(dwg))

        # draw text on top, if set
        if self.text.text != "":
            self.text.draw(dwg, grp)

        return grp

    def __repr__(self) -> str:
        """
        returns the string representation of the marker

        :return: string representation of the marker
        :rtype: str
        """
        return (
            f"<Marker(cx={self.cx}, cx={self.cy}, "
            f"symbol='{self.symbol}')>"
        )
