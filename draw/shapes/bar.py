from draw.base import Dimension


class Bar(Dimension):
    """
    bar that has a position, a size, a filling and a strokestyle;
    additionally, margin and padding is considered
    """
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        rx: int = 3,
        ry: int = 3,
        fill: str = "white",
        stroke: str = "black",
        #margin: Margin = DEFAULT_MARGIN,
        #padding: Padding = DEFAULT_PADDING,
        class_: str = "defaultbar",
    ):
        Dimension.__init__(self, x, y, width, height)
        self.rx = rx
        self.ry = ry
        self.stroke = stroke
        self.fill = fill
        #self.margin = margin
        #self.padding = padding
        self.class_ = class_

    def draw(self, dwg, grp=None):
        grp = grp or dwg.g()

        # add rounded rectangle
        grp.add(
            dwg.rect(
                (
                    self.x1, # + self.margin.left,
                    self.y1 #+ self.margin.top,
                ),
                (
                    self.width, # - self.margin.right - self.margin.left,
                    self.height # - self.margin.bottom - self.margin.top,
                ),
                stroke=self.stroke,
                fill=self.fill,
                rx=self.rx,
                ry=self.ry,
                class_=self.class_
            )
        )

        return grp

    def __repr__(self):
        return (
            f"<Bar(x1={self.x1}, y1={self.y1}, "
            f"x2={self.x2}, y2={self.y2})>"
        )
