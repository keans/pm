from draw.base import Position
from draw.grid.cell import DEFAULT_CELL_FILL, DEFAULT_CELL_WIDTH
from draw.grid import GridWithBars, Row
from models.types import DateType
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

        cellpos = {}
        for entry in range(project.entries):
            i = 0
            for wp in project.workpackages:
                for t in wp.tasks:
                    r = Row()
                    r.add_cols(len(self.timetable.days))
                    self.add_row(r)

                    pos = Position(
                        x=self.timetable.hierarchy_count() + i,
                        y=self.timetable.get_pos(t.start_date)
                    )

                    cellpos[t.name] = Position(
                        x=self.timetable.hierarchy_count() + i,
                        y=self.timetable.get_pos(t.start_date) + t.duration.days
                    )

                    # TODO: add colors per package? to inheritance
                    self.add_bar(
                        position=pos,
                        length=t.duration.days - 1
                    )

                    # add dependency arrows
                    depend_pos = cellpos.get(t.depends_on)
                    if depend_pos:
                        self.add_dependency(
                            start_position=depend_pos,
                            end_position=pos
                        )

                    i += 1


    def prepare_top_header(self):
        """
        prepare the top header
        """
        for s in self.timetable.hierarchy():
            r = Row()
            for items in s:
                fill = DEFAULT_CELL_FILL
                if (items[0].dt_type == DateType.DAY) and items[0].is_weekend():
                    # mark weekends
                    fill = "gray"

                cell = r.add_cell(
                    cell_width=self.default_cell_width * len(items),
                    text=items[0].default, fill=fill
                )

            self.add_row(r)
