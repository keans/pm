from draw.base import Position, Margin
from draw.shapes import Bar

from .grid import Grid


class GridWithBars(Grid):
    """
    a fixed grid that allows the placing of bars
    """
    def __init__(self, x, y):
        Grid.__init__(self, x, y)
        self.bars = []

    def add_bar(self, position, length, fill="black"):
        """
        add a bar to the grid
        """
        position = Position(*position)
        start_cell = self.get_cell(*position)
        end_cell = self.get_cell(position[0], position[1] + length)

        bar = Bar(
            start_cell.dimension.x, start_cell.dimension.y,
            width=end_cell.dimension.x2 - start_cell.dimension.x1,
            height=start_cell.dimension.height,
            fill=fill, margin=Margin(2, 2, 2, 2)
        )
        self.bars.append(bar)

    def draw(self, dwg, grp=None):
        grp = Grid.draw(self, dwg, grp)

        # draw bars
        bars_grp = dwg.g()
        for bar in self.bars:
            bar.draw(dwg, bars_grp)
        grp.add(bars_grp)

        return grp
