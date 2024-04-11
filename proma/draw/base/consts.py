from enum import Enum

from proma.draw.base import Margin, Padding


# default parameter
DEFAULT_MARGIN = Margin(0, 0, 0, 0)
DEFAULT_PADDING = Padding(0, 0, 0, 0)

# default cell dimensions
DEFAULT_CELL_WIDTH = 25
DEFAULT_CELL_HEIGHT = 25
DEFAULT_CELL_FILL = "white"


class TextAnchor(Enum):
    """
    text anchor
    for horizontal text alignment
    """

    START = "start"
    END = "end"
    MIDDLE = "middle"


class TextDominantBaseline(Enum):
    """
    text dominiant baseline
    for vertical text alignment
    """

    AUTO = "auto"
    TEXT_BOTTOM = "text-bottom"
    ALPHABETIC = "alphabetic"
    IDEOGRAPHIC = "ideographic"
    MIDDLE = "middle"
    CENTRAL = "central"
    MATHEMATICAL = "mathematical"
    HANGING = "hanging"
    TEXT_TOP = "text-top"
