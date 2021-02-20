import math
import collections

from draw.base import Size, StrokeStyle
from draw.grid import GridWithBars
from utils.timetable import Timetable


class Gantt(GridWithBars):
    """
    gantt chart class
    """
    def __init__(
        self, x, y, project,
        cell_size=Size(25, 25),
        stroke_style=StrokeStyle("gray", 1, "round", "round", None), 
        fill="white"
    ):
        self.timetable = Timetable(
            project.start_date, project.end_date
        )
        self.project = project

        GridWithBars.__init__(
            self, x, y, 
            project.entries + len(self.timetable.shows), 
            len(self.timetable.hierarchy()[-1]), 
            cell_size, stroke_style, fill
        )

        self.prepare_top_header()

    def prepare_top_header(self):
        """
        prepare the top header
        """
        last = collections.defaultdict(str)
        for col, dt in enumerate(self.timetable.days()):
            for row, item in enumerate(self.timetable.shows):
                if item == "year":
                    text = dt.strftime("%Y")
                elif item == "quarter":
                    text = f"Q{math.ceil(dt.month/3.)}"
                elif item == "week":
                    text = dt.strftime("CW%V")
                elif item == "month":
                    text = dt.strftime("%b")
                elif item == "day":
                    text = dt.strftime("%d")

                    if dt.weekday() in (0, 6):
                        # color weekends
                        self.set_fill(row, col, "gray")

                if text != last[item]:
                    last[item] = text
                    self.set_text(row, col, text)
