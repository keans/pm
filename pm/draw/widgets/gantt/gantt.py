from pm.draw.base import Position, Padding
from pm.draw.shapes.cell import DEFAULT_CELL_WIDTH
from pm.draw.widgets.grid import GridWithBars, GridRow
from pm.models.project import Project
from pm.models.types import DateType
from pm.utils.timetable import Timetable


class Gantt(GridWithBars):
    """
    gantt chart class
    """

    def __init__(
        self,
        x: int,
        y: int,
        project: Project,
        default_cell_width: int = DEFAULT_CELL_WIDTH,
        description_width: int = 200,
    ):
        GridWithBars.__init__(self, x=x, y=y)

        self.default_cell_width = default_cell_width
        self.description_width = description_width
        self.project = project

        # prepare timetabble
        self.timetable = Timetable(project.start_date, project.end_date)

        # add header based on hierarchy (year, quarter, month etc.)
        self.prepare_top_header()

        # add project data
        self.prepare_project_data()

    def _cell_format_class(
        self,
        dt: DateType,
        class_: str = "defaultcell",
        is_header: bool = False,
    ) -> str:
        """
        returns cell format class

        :param dt: date type
        :type dt: DateType
        :param class_: css class, defaults to "defaultcell"
        :type class_: str, optional
        :return: css class
        :rtype: str
        """
        class_ += f" {dt.dt_type.value}"

        if is_header is True:
            class_ += " header"

        if (dt.dt_type == DateType.DAY) and dt.is_weekend():
            class_ += " weekend"

        return class_

    def add_days(
        self,
        r: GridRow,
    ):
        """
        add days to row

        :param r: row
        :type r: Row
        """
        for dt in self.timetable.days:
            r.add_cell(
                self.default_cell_width, class_=self._cell_format_class(dt[0])
            )

    def prepare_top_header(self):
        """
        prepare the top header
        """
        for s in self.timetable.hierarchy():
            r = GridRow()

            # add empty column for descriptions in the following rows
            r.add_cell(
                cell_width=self.description_width,
            )

            # add items
            for items in s:
                r.add_cell(
                    cell_width=self.default_cell_width * len(items),
                    text=items[0].default,
                    class_=self._cell_format_class(items[0], is_header=True),
                )

            self.add_row(r)

    def prepare_project_data(self):
        """
        prepare project's data, i.e., gantt chart data
        """
        cellpos = {}
        i = 0
        for wp in self.project.workpackages:
            # add workpackage description
            r = GridRow()
            r.add_cell(
                cell_width=self.description_width,
                text=wp.name,
                text_anchor="start",
                padding=Padding(top=2, right=2, bottom=2, left=10),
                class_="defaultcell workpackage",
            )
            self.add_days(r)
            self.add_row(r)
            i += 1

            for t in wp.tasks:
                r = GridRow()

                # add task description
                r.add_cell(
                    cell_width=self.description_width,
                    text=t.name,
                    text_anchor="start",
                    text_alignment_baseline="middle",
                    padding=Padding(top=2, right=2, bottom=2, left=20),
                    class_="defaultcell task",
                )
                self.add_days(r)
                self.add_row(r)

                pos = Position(
                    x=self.timetable.hierarchy_count() + i,
                    y=self.timetable.get_pos(t.start_date),
                )

                # store task's position for dependency arrows
                cellpos[t.name] = Position(
                    x=self.timetable.hierarchy_count() + i,
                    y=self.timetable.get_pos(t.start_date) + t.duration.days,
                )

                # TODO: add colors per package? to inheritance
                self.add_bar(
                    position=pos,
                    length=t.duration.days - 1,
                    fill="lightblue",
                )

                # add milestones
                for m in t.milestones:
                    pos = Position(
                        x=self.timetable.hierarchy_count() + i,
                        y=self.timetable.get_pos(m.date) + 1,
                    )
                    self.add_milestone(pos, m.name)

                # add dependency arrows
                depend_pos = cellpos.get(t.depends_on)
                if depend_pos:
                    self.add_dependency(
                        start_position=depend_pos,
                        end_position=pos,
                    )

                i += 1

            # add additional class for last row
            for cell in self.rows[-1].cells:
                cell.class_ += " lastrow"

            # add special attributes for first cells and last cell in row
            for row in self.rows:
                row.cells[1].class_ += " firstcol"
                row.cells[-1].class_ += " lastcol"

        # add vertical lines to the grid
        for event in self.project.events:
            pos = Position(
                y=self.timetable.get_pos(event.date),
                x=self.timetable.hierarchy_count(),
            )
            self.add_event(pos, self.timetable.hierarchy_count())


# TODO: USE HIERARCHY COUNT TO GET CORRECT LENGTH
