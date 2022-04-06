from draw.base import DEFAULT_MARGIN, DEFAULT_PADDING, DEFAULT_STROKE_STYLE, \
    DEFAULT_BORDER_STYLE, DEFAULT_TEXT_STYLE, DEFAULT_PATH_ARROW_STYLE, \
    Dimension, Position

from svgwrite.path import Path


class Text:
    """
    simple text
    """
    def __init__(
        self, x, y, text,
        text_style=DEFAULT_TEXT_STYLE,
        text_anchor="middle", text_dominant_baseline="middle",
    ):
        self.text = text
        self.text_anchor = text_anchor
        self.text_dominant_baseline = text_dominant_baseline
        self.text_style = text_style
        self.set_pos(x, y)

    def set_pos(self, x, y):
        """
        set new position
        """
        self.position = Position(x, y)

    def draw(self, dwg, grp=None):
        grp = grp or dwg

        grp.add(
            dwg.text(
                text=self.text,
                insert=(self.position.x, self.position.y),
                fill=self.text_style.fill,
                font_size=self.text_style.font_size,
                font_family=self.text_style.font_family,
                text_anchor=self.text_anchor,
                dominant_baseline=self.text_dominant_baseline
            )
        )

        return grp


class Line:
    """
    simple line with stroke style
    """
    def __init__(self, x1, y1, x2, y2, stroke_style=DEFAULT_STROKE_STYLE):
        self.start_position = Position(x1, y1)
        self.end_position = Position(x2, y2)
        self.stroke_style = stroke_style

    def draw(self, dwg, grp=None):
        grp = grp or dwg
        extra = {
            "stroke": self.stroke_style.stroke,
            "stroke_width": self.stroke_style.width,
            "stroke_linecap": self.stroke_style.linecap,
            "stroke_linejoin": self.stroke_style.linejoin
        }
        if self.stroke_style.dasharray not in (None, ""):
            extra["stroke_dasharray"] = self.stroke_style.dasharray

        grp.add(
            dwg.line(
                self.start_position,
                self.end_position,
                **extra
            )
        )

        return grp


class PathArrow:
    """
    simple line with stroke style
    """
    def __init__(self, x1, y1, x2, y2, stroke_style=DEFAULT_PATH_ARROW_STYLE):
        self.start_position = Position(x1, y1)
        self.end_position = Position(x2, y2)
        self.stroke_style = stroke_style

    def draw(self, dwg, grp=None):
        grp = grp or dwg

        extra = {
            "stroke": self.stroke_style.stroke,
            "stroke_width": self.stroke_style.width,
            "stroke_linecap": self.stroke_style.linecap,
            "stroke_linejoin": self.stroke_style.linejoin,
            "fill": "none",
            "marker-end": "url(#arrow)"
        }

        arrow_size = 4

        # prepare arrow marker
        arrow = dwg.marker(
            id="arrow",
            insert=(1, arrow_size / 2),
            size=(arrow_size, arrow_size),
            orient="auto", markerUnits="strokeWidth"
        )
        arrow.viewbox(width=arrow_size, height=arrow_size)
        arrow.add(
            dwg.polyline(
                [
                    (0,0), (arrow_size,arrow_size/2),
                    (0,arrow_size), (1,arrow_size/2)
                ],
                fill=self.stroke_style.stroke
            )
        )
        dwg.defs.add(arrow)

        h = (self.end_position.y - self.start_position.y) * 0.5

        path = Path(
            d=("M", self.start_position.x - 2, self.start_position.y),
            **extra
        )
        path.push("L", self.start_position.x + 5, self.start_position.y)

        if self.start_position.x >= self.end_position.x:
            # same x position => go down and back
            path.push("L", self.start_position.x + 5, self.start_position.y + h)
            path.push("L", self.end_position.x - 5, self.start_position.y + h)
            path.push("L", self.end_position.x - 5, self.end_position.y)
            path.push("L", self.end_position.x, self.end_position.y)

        else:
            # far away x position => simply go down
            path.push("L", self.start_position.x + 5, self.end_position.y)
            path.push("L", self.end_position.x, self.end_position.y)

        grp.add(path)

        return grp

        grp = grp or dwg
        extra = {
            "stroke": self.stroke_style.stroke,
            "stroke_width": self.stroke_style.width,
            "stroke_linecap": self.stroke_style.linecap,
            "stroke_linejoin": self.stroke_style.linejoin
        }
        if self.stroke_style.dasharray not in (None, ""):
            extra["stroke_dasharray"] = self.stroke_style.dasharray

        grp.add(
            dwg.line(
                self.start_position,
                self.end_position,
                **extra
            )
        )

        return grp


class Box:
    """
    box that has a position, a size, a filling and a borderstyle (per side);
    additionally, margin and padding is considered
    """
    def __init__(
        self, x, y, width, height, fill="white",
        border_style=DEFAULT_BORDER_STYLE,
        margin=DEFAULT_MARGIN, padding=DEFAULT_PADDING,
    ):
        self.dimension = Dimension(x, y, width, height)
        self.fill = fill
        self.border_style = border_style
        self.margin = margin
        self.padding = padding

    def draw(self, dwg, grp=None):
        grp = grp or dwg.g()

        # rectangle for background
        grp.add(
            dwg.rect(
                (
                    self.dimension.x1 + self.margin.left,
                    self.dimension.y1 + self.margin.top,
                ),
                (
                    self.dimension.width - self.margin.right - self.margin.left,
                    self.dimension.height - self.margin.bottom - self.margin.top,
                ),
                stroke="none", fill=self.fill
            )
        )

        # top
        top_line = Line(
            self.dimension.x1 + self.margin.left,
            self.dimension.y1 + self.margin.top,
            self.dimension.x2 - self.margin.right - self.margin.left,
            self.dimension.y1 + self.margin.top,
            self.border_style.top
        )
        top_line.draw(dwg, grp)

        # right
        right_line = Line(
            self.dimension.x2 - self.margin.right - self.margin.left,
            self.dimension.y1 + self.margin.top,
            self.dimension.x2 - self.margin.right - self.margin.left,
            self.dimension.y2 - self.margin.bottom - self.margin.top,
            self.border_style.right
        )
        right_line.draw(dwg, grp)

        # bottom
        bottom_line = Line(
            self.dimension.x1 + self.margin.left,
            self.dimension.y2 - self.margin.bottom - self.margin.top,
            self.dimension.x2 - self.margin.right - self.margin.left,
            self.dimension.y2 - self.margin.bottom - self.margin.top,
            self.border_style.bottom
        )
        bottom_line.draw(dwg, grp)

        # left
        left_line = Line(
            self.dimension.x1 + self.margin.left,
            self.dimension.y1 + self.margin.top,
            self.dimension.x1 + self.margin.left,
            self.dimension.y2 - self.margin.bottom - self.margin.top,
            self.border_style.left
        )
        left_line.draw(dwg, grp)

        return grp

    def __repr__(self):
        return f"Box(dimension={self.dimension})"


class Bar:
    """
    bar that has a position, a size, a filling and a strokestyle;
    additionally, margin and padding is considered
    """
    def __init__(
        self, x, y, width, height, rx=3, ry=3,
        fill="white", stroke="black",
        margin=DEFAULT_MARGIN, padding=DEFAULT_PADDING,
    ):
        self.dimension = Dimension(x, y, width, height)
        self.rx = rx
        self.ry = ry
        self.stroke = stroke
        self.fill = fill
        self.margin = margin
        self.padding = padding

    def draw(self, dwg, grp=None):
        grp = grp or dwg.g()

        # add rounded rectangle
        grp.add(
            dwg.rect(
                (
                    self.dimension.x1 + self.margin.left,
                    self.dimension.y1 + self.margin.top,
                ),
                (
                    self.dimension.width - self.margin.right - self.margin.left,
                    self.dimension.height - self.margin.bottom - self.margin.top,
                ),
                stroke=self.stroke, fill=self.fill,
                rx=self.rx, ry=self.ry
            )
        )

        return grp

    def __repr__(self):
        return f"Bar(dimension={self.dimension})"


class Marker:
    # see https://matplotlib.org/3.1.0/api/markers_api.html
    SUPPORTED_MARKER = {
        "d": "diamond",
        "o": "circle",
        "s": "square",
    }
    def __init__(
        self, symbol, cx, cy, width, height=None,
        stroke_style=DEFAULT_STROKE_STYLE, fill="black"
    ):
        self.symbol = symbol
        self.dimension = Dimension(cx - width/2, cy - height/2, width, height)
        self.stroke_style = stroke_style
        self.fill = fill

    def draw(self, dwg, grp=None):
        grp = grp or dwg.g()

        if self.symbol == "d":
            grp.add(
                self.parent.polygon([
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
                ], stroke=self.stroke, fill=self.fill)
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
