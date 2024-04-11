from proma.draw.base import Position, Padding
from proma.draw.base.consts import (
    DEFAULT_CELL_WIDTH,
    TextAnchor,
    TextDominantBaseline,
)
from proma.draw.widgets.grid import GridWithBars, GridRow
from proma.models.project import Project
from proma.models.types import DateType
from proma.utils.timetable import Timetable, YEAR_QUARTER_MONTH_WEEK_DAY_FMT


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
        formats=YEAR_QUARTER_MONTH_WEEK_DAY_FMT,
    ):
        GridWithBars.__init__(self, x=x, y=y)

        self.default_cell_width = default_cell_width
        self.description_width = description_width
        self.project = project

        # prepare timetabble
        self.timetable = Timetable(
            start_date=project.start_date,
            end_date=project.end_date,
            formats=formats,
        )

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

        if (dt.dt_type == DateType.DAY) and dt.is_weekend:
            class_ += " weekend"

        return class_

    def add_empty_cells(
        self,
        r: GridRow,
    ):
        """
        add empty cells to row

        :param r: row
        :type r: Row
        """
        for tti in self.timetable.items_per_hierarchy[-1].items:
            r.add_cell(
                self.default_cell_width,
                class_=self._cell_format_class(
                    dt=tti,
                ),
            )

    def prepare_top_header(self):
        """
        prepare the top header
        """
        for timetable_level in self.timetable.items_per_hierarchy:
            r = GridRow()

            # add empty column for descriptions in the following rows
            r.add_cell(
                cell_width=self.description_width,
            )

            # add items
            for item, count in timetable_level.grouped_items:
                r.add_cell(
                    cell_width=self.default_cell_width * count,
                    text=str(item),
                    class_=self._cell_format_class(
                        dt=item,
                        is_header=True,
                    ),
                )

            self.add_row(r)

    def prepare_project_data(self):
        """
        prepare project's data, i.e., gantt chart data
        """
        cellpos = {}
        i = 0
        for wp in self.project.workpackages:
            # -- workpackage description --
            r = GridRow()
            r.add_cell(
                cell_width=self.description_width,
                text=wp.name,
                text_anchor=TextAnchor.START,
                padding=Padding(top=2, right=0, bottom=2, left=5),
                class_="defaultcell workpackage",
            )
            self.add_empty_cells(r)
            self.add_row(r)
            i += 1

            # -- tasks --
            for t in wp.tasks:
                r = GridRow()

                # add task description
                r.add_cell(
                    cell_width=self.description_width,
                    text=t.name,
                    text_anchor=TextAnchor.START,
                    text_alignment_baseline=TextDominantBaseline.CENTRAL,
                    padding=Padding(top=2, right=2, bottom=2, left=10),
                    class_="defaultcell task",
                )
                self.add_empty_cells(r)
                self.add_row(r)

                # get start position and length
                # use col_offset by 1 since first column has description
                col, length = self.timetable.get_from_and_length_pos(
                    from_date=t.start_date, to_date=t.end_date, col_offset=1
                )

                # current row
                row = len(self.timetable.hierarchy) + i

                # position in grid
                # => please note that row=x and col=y due to nested
                #    list access order
                pos = Position(x=row, y=col)

                # store task's position for dependency arrows
                cellpos[t.name] = Position(x=row, y=col + length + 1)

                # add bar
                # TODO: add colors per package? to inheritance
                self.add_bar(
                    position=pos,
                    length=length,
                    fill="lightblue",
                )

                # add milestones
                for m in t.milestones:
                    pos = Position(
                        x=row,
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
                y=self.timetable.get_pos(event.date) + 1,
                x=len(self.timetable.hierarchy),
            )
            self.add_event(
                position=pos,
                hierarchy_count=len(self.timetable.hierarchy),
                text=event.name,
            )
