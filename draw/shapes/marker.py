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
        fill: str = "black",
        class_: str = "defaultmarker"
    ):
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

    def draw(self, dwg, grp=None):
        grp = grp or dwg.g()

        if self.symbol == "d":
            # diamond
            grp.add(
                dwg.polygon(
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
