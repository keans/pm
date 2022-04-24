from svgwrite import Drawing
from svgwrite.container import Group

from draw.base import Position, Margin
from draw.shapes import Bar, PathWithArrow, Marker, Line
from draw.widgets.grid import Grid


class GridWithBars(Grid):
    """
    a fixed grid that allows the placing of bars
    """
    def __init__(
        self,
        x: int,
        y: int
    ):
        Grid.__init__(self, x=x, y=y)

        self.bars = []
        self.dependencies = []
        self.milestones = []
        self.events = []

    def add_bar(
        self,
        position: Position,
        length: int,
        fill: str = "black"
    ):
        """
        add a bar to the grid
        """
        start_cell = self.get_cell(*position.tuple)
        end_cell = self.get_cell(position.x, position.y + length)

        bar = Bar(
            x=start_cell.pos.x,
            y=start_cell.pos.y,
            width=end_cell.x2 - start_cell.x1,
            height=start_cell.height,
            fill=fill,
            margin=Margin(3, 2, 3, 2)
        )
        self.bars.append(bar)

    def add_dependency(
        self,
        start_position: Position,
        end_position: Position
    ):
        """
        add dependency arrow between start position and end position
        within the grid

        :param start_position: start position
        :type start_position: Position
        :param end_position: end position
        :type end_position: Position
        """
        start_cell = self.get_cell(*start_position.tuple)
        end_cell = self.get_cell(*end_position.tuple)

        path = PathWithArrow(
            start_cell.pos.x,
            start_cell.cy,
            end_cell.pos.x,
            end_cell.cy
        )
        self.dependencies.append(path)

    def add_milestone(
        self,
        pos: Position,
        text: str
    ):
        """
        add milestone to the grid

        :param pos: position
        :type start_position: Position
        """
        cell = self.get_cell(*pos.tuple)

        marker= Marker(
            symbol="v",
            cx=cell.cx,
            cy=cell.cy,
            width=12,
            height=12,
            text=text,
            text_y_offset=20,
        )
        self.milestones.append(marker)

    def add_event(
        self,
        position: Position,
        hierarchy_count: int
    ):
        """
        add an event to the grid
        """
        start_cell = self.get_cell(*position.tuple)
        end_cell = self.get_cell(
            position.x + len(self.rows) - hierarchy_count - 1,
            position.y
        )

        #
        # TODO: combine line + marker + text in new vertical line event
        #
        #
        event = Line(
            x1=start_cell.cx,
            y1=start_cell.pos.y,
            x2=start_cell.cx,
            y2=end_cell.pos.y + 50,
            class_="defaultevent"
        )
        self.events.append(event)

    def draw(self, dwg: Drawing, grp: Group = None) -> Group:
        """
        draw grid with bars including bars and dependency arrows

        :param dwg: drawing
        :type dwg: Drawing
        :param grp: group, defaults to None
        :type grp: Group, optional
        :return: group
        :rtype: Group
        """
        # get group
        grp = Grid.draw(self, dwg, grp)

        # draw vertical lines
        events_group = dwg.g()
        for event in self.events:
            event.draw(dwg, events_group)
        grp.add(events_group)

        # draw bars
        bars_grp = dwg.g()
        for bar in self.bars:
            bar.draw(dwg, bars_grp)
        grp.add(bars_grp)

        # draw milestones
        milestones_grp = dwg.g()
        for milestone in self.milestones:
            milestone.draw(dwg, milestones_grp)
        grp.add(milestones_grp)

        # draw dependency arrows
        dependencies_grp = dwg.g()
        for dep in self.dependencies:
            dep.draw(dwg, dependencies_grp)
        grp.add(dependencies_grp)

        return grp
