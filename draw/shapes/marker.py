from draw.base import Dimension


class Marker(Dimension):
    # see https://matplotlib.org/3.1.0/api/markers_api.html
    SUPPORTED_MARKER = {
        "d": "diamond",
        "o": "circle",
        "s": "square",
    }
    def __init__(
        self,
        symbol,
        cx: int,
        cy: int,
        width: int,
        height: int = None,
        #stroke_style: StrokeStyle = DEFAULT_STROKE_STYLE,
        fill: str = "black",
        class_: str = ""
    ):
        Dimension.__init__(self, cx - width/2, cy - height/2, width, height)
        self.symbol = symbol
        #self.stroke_style = stroke_style
        self.fill = fill
        self.class_ = class_

    def draw(self, dwg, grp=None):
        grp = grp or dwg.g()

        if self.symbol == "d":
            grp.add(
                self.parent.polygon(
                    [
                        (
                            self.dimension.x + self.dimension.width / 2,
                            self.dimension.y
                        ),
                        (
                            self.dimension.x,
                            self.dimension.y - self.h / 2
                        ),
                        (
                            self.dimenison.x + self.w / 2,
                            self.cy
                        ),
                        (
                            self.dimension.x,
                            self.cy + self.h / 2
                        )
                    ],
                    stroke=self.stroke,
                    fill=self.fill,
                    class_ = self.class_
                )
            )

        # elif self.symbol == "o":
        #     grp.add(
        #         self.parent.rect(
        #             (self.cx - self.w / 2, self.cy - self.w / 2),
        #             (self.w, self.w),
        #             stroke=self.stroke, fill=self.fill
        #         )
        #     )

        # elif self.symbol == "circle":
        #     grp.add(
        #         self.parent.circle(
        #             (self.cx, self.cy),
        #             r=self.w/2,
        #             stroke=self.stroke, fill=self.fill
        #         )
        #     )

        return grp
