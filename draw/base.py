import collections

Position = collections.namedtuple("Position", ["x", "y"])
Size = collections.namedtuple("Size", ["width", "height"])
Margin = collections.namedtuple("Margin", ["top", "right", "bottom", "left"])
Padding = collections.namedtuple("Padding", ["top", "right", "bottom", "left"])
StrokeStyle = collections.namedtuple(
    "StrokeStyle", ["stroke", "width", "linecap", "linejoin", "dasharray"]
)

TextStyle = collections.namedtuple(
    "TextStyle", ["fill", "font_size", "font_family", "font_weight"]
)

class Dimension:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def x1(self):
        return self.x

    @property
    def y1(self):
        return self.y

    @property
    def x2(self):
        return self.x + self.width

    @property
    def y2(self):
        return self.y + self.height

    @property
    def cx(self):
        return self.x + self.width / 2

    @property
    def cy(self):
        return self.y + self.height / 2

    @property
    def size(self):
        return (self.width, self.height)

    def __repr__(self):
        return (
            f"Dimension(x={self.x}, y={self.y}, "
            f"width={self.width}, height={self.height})"
        )


class BorderStyle:
    def __init__(self, top, right, bottom, left):
        assert(
            all([
                isinstance(m, StrokeStyle)
                for m in [top, right, bottom, left]
            ])
        )
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left


# default parameter
DEFAULT_MARGIN = Margin(0, 0, 0, 0)
DEFAULT_PADDING = Padding(0, 0, 0, 0)
DEFAULT_STROKE_STYLE = StrokeStyle("black", 1, "round", "round", "")
DEFAULT_BORDER_STYLE = BorderStyle(
    DEFAULT_STROKE_STYLE, DEFAULT_STROKE_STYLE,
    DEFAULT_STROKE_STYLE, DEFAULT_STROKE_STYLE
)
DEFAULT_TEXT_STYLE = TextStyle("black", 12, "Helvetica", 300)
DEFAULT_PATH_ARROW_STYLE = StrokeStyle("red", 2, "round", "round", "")
