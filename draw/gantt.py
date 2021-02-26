from draw.grid.cell import DEFAULT_CELL_WIDTH
from draw.grid import GridWithBars, Row
from utils.timetable import Timetable


class Gantt(GridWithBars):
    """
    gantt chart class
    """
    def __init__(
        self, x, y, project,
        default_cell_width=DEFAULT_CELL_WIDTH
    ):
        GridWithBars.__init__(self, x, y)
        self.default_cell_width = default_cell_width

        self.timetable = Timetable(
            project.start_date, project.end_date
        )
        self.project = project

        self.prepare_top_header()

        for entry in range(project.entries):
            r = Row()
            r.add_cols(len(self.timetable.days()))
            self.add_row(r)

            for wp in project.workpackages:
                for t in wp.tasks:
                    print(wp, t)
            #g.add_bar((5, 3), 5)

            # ACCESS DATES BY DICT ?! =>DRAW BARS


    def prepare_top_header(self):
        """
        prepare the top header
        """
        def count(li):
            res = []

            c = 0
            last = None
            for x in li:
                if x["fmt"] != last:
                    if c > 0:
                        res.append(c)
                    last = x["fmt"]
                    c = 0
                c += 1
            res.append(c)

            return res

        fmap = {
            "year": self.timetable.years,
            "quarter": self.timetable.quarters,
            "month": self.timetable.months,
            "week": self.timetable.weeks,
            "day": self.timetable.days,
        }
        for s in self.timetable.shows:
            r = Row()
            for m, c in zip(fmap[s](unique=True), count(fmap[s]())):
                cell = r.add_cell(
                    cell_width=self.default_cell_width * c,
                    text=m["fmt"]
                )
                if (s == "day") and (m["dt"].weekday() in (0, 6)):
                    cell.set_fill("lightgray")

            self.add_row(r)
