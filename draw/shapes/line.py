from draw.base.dimension import Dimension


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
#        stroke_style=DEFAULT_STROKE_STYLE
    ):
        Dimension.__init__(self, x1, y1, x2 - x1, y2 - y2)
#        self.stroke_style = stroke_style

    def draw(self, dwg, grp=None):
        grp = grp or dwg
        # extra = {
        #     "stroke": self.stroke_style.stroke,
        #     "stroke_width": self.stroke_style.width,
        #     "stroke_linecap": self.stroke_style.linecap,
        #     "stroke_linejoin": self.stroke_style.linejoin
        # }
        # if self.stroke_style.dasharray not in (None, ""):
        #     extra["stroke_dasharray"] = self.stroke_style.dasharray

        grp.add(
            dwg.line(
                self.xy, self.wh
                #self.start_position,
                #self.end_position,
                #**extra
            )
        )

        return grp

    def __repr__(self):
        return (
            f"<Line(x1={self.x1}, y1={self.y1}, "
            f"x2={self.x2}, y2={self.y2})>"
        )
