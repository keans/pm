from .position import Position
from .size import Size
from .dimension import Dimension
from .margin import Margin
from .padding import Padding


# StrokeStyle = collections.namedtuple(
#     "StrokeStyle", ["stroke", "width", "linecap", "linejoin", "dasharray"]
# )

# TextStyle = collections.namedtuple(
#     "TextStyle", ["fill", "font_size", "font_family", "font_weight"]
# )


# class BorderStyle:
#     def __init__(
#         self,
#         top: StrokeStyle,
#         right: StrokeStyle,
#         bottom: StrokeStyle,
#         left: StrokeStyle
#     ):
#         assert(
#             all([
#                 isinstance(m, StrokeStyle)
#                 for m in [top, right, bottom, left]
#             ])
#         )
#         self.top = top
#         self.right = right
#         self.bottom = bottom
#         self.left = left

