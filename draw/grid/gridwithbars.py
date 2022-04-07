from draw.base import Position #, Margin
from draw.shapes import Bar, PathWithArrow

from .grid import Grid


class GridWithBars(Grid):
    """
    a fixed grid that allows the placing of bars
    """
    def __init__(self, x, y):
        Grid.__init__(self, x, y)
        self.bars = []
        self.dependencies = []

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
            #margin=Margin(2, 2, 2, 2)
        )
        self.bars.append(bar)

    def add_dependency(
        self,
        start_position: Position,
        end_position: Position
    ):
        start_cell = self.get_cell(*start_position.tuple)
        end_cell = self.get_cell(*end_position.tuple)

        p = PathWithArrow(
            start_cell.pos.x,
            start_cell.cy,
            end_cell.pos.x,
            end_cell.cy
        )
        self.dependencies.append(p)

    def draw(self, dwg, grp=None):
        grp = Grid.draw(self, dwg, grp)

        # draw bars
        bars_grp = dwg.g()
        for bar in self.bars:
            bar.draw(dwg, bars_grp)
        grp.add(bars_grp)

        # draw dependencies (arrows)
        dependencies_grp = dwg.g()
        for dep in self.dependencies:
            dep.draw(dwg, dependencies_grp)
        grp.add(dependencies_grp)

        return grp
