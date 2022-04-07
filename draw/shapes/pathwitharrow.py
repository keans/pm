from svgwrite.path import Path

from draw.base import Dimension


class PathWithArrow(Dimension):
    """
    path with an arrow at the end
    """
    def __init__(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
#        stroke_style: StrokeStyle = DEFAULT_PATH_ARROW_STYLE,
        class_: str = "defaultpathwitharrow"
    ):
        Dimension.__init__(self, x1, y1, x2 - x1, y2 - y1)
        #self.stroke_style = stroke_style
        self.class_ = class_

    def draw(self, dwg, grp=None):
        grp = grp or dwg

        # extra = {
        #     "stroke": self.stroke_style.stroke,
        #     "stroke_width": self.stroke_style.width,
        #     "stroke_linecap": self.stroke_style.linecap,
        #     "stroke_linejoin": self.stroke_style.linejoin,
        #     "fill": "none",
        #     "marker-end": "url(#arrow)"
        # }

        arrow_size = 4

        # prepare arrow marker
        arrow = dwg.marker(
            id="arrow",
            insert=(1, arrow_size / 2),
            size=(arrow_size, arrow_size),
            orient="auto",
            markerUnits="strokeWidth"
        )
        arrow.viewbox(width=arrow_size, height=arrow_size)
        arrow.add(
            dwg.polyline(
                [
                    (0,0), (arrow_size,arrow_size/2),
                    (0,arrow_size), (1,arrow_size/2)
                ],
                #fill=self.stroke_style.stroke
            )
        )
        dwg.defs.add(arrow)

        h = (self.y2 - self.y1) * 0.5

        path = Path(
            d=("M", self.x1 - 2, self.y1),
            #**extra
        )
        path.push("L", self.x1 + 5, self.y1)

        if self.x1 >= self.x2:
            # same x position => go down and back
            path.push("L", self.x1 + 5, self.y1 + h)
            path.push("L", self.x2 - 5, self.y1 + h)
            path.push("L", self.x2 - 5, self.y2)
            path.push("L", self.x2, self.y2)

        else:
            # far away x position => simply go down
            path.push("L", self.x1 + 5, self.y2)
            path.push("L", self.x2, self.y2)

        grp.add(path)

        return grp
