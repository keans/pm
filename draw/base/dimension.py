from .position import Position
from .size import Size


class Dimension:
    """
    dimension (x, y, width, height)
    """
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int
    ):
        self.pos = Position(x, y)
        self.size = Size(width, height)

    @property
    def tuple(self) -> tuple:
        """
        return the dimension as tuple

        :return: (x, y, width, height)-tuple
        :rtype: tuple
        """
        return (self.pos.x, self.pos.y, self.size.width, self.size.height)

    @property
    def xy(self) -> tuple:
        """
        return the (x, y) tuple

        :return: (x, y)-tuple
        :rtype: tuple
        """
        return (self.pos.x, self.pos.y)

    @property
    def wh(self) -> tuple:
        """
        return the (w, h) tuple

        :return: (w, h)-tuple
        :rtype: tuple
        """
        return (self.size.width, self.size.height)

    @property
    def tuple(self) -> tuple:
        """
        return the dimension as tuple

        :return: (x, y, width, height)-tuple
        :rtype: tuple
        """
        return (self.x, self.y, self.width, self.height)

    @property
    def rect(self) -> tuple:
        """
        return the dimension as rectangle

        :return: (x1, y1, x2, y2)-tuple
        :rtype: tuple
        """
        return (self.x1, self.y1, self.x2, self.y2)

    @property
    def pos(self) -> Position:
        """
        return position

        :return: position
        :rtype: Position
        """
        return self._pos

    @pos.setter
    def pos(self, value: Position):
        """
        set the position
        """
        assert isinstance(value, Position)

        self._pos = value

    @property
    def size(self) -> Size:
        """
        return size

        :return: size
        :rtype: size
        """
        return self._size

    @size.setter
    def size(self, value: Size):
        """
        set the size
        """
        assert isinstance(value, Size)

        self._size = value

    def set_xy(self, x: int, y: int):
        """
        set x and y at the same time

        :param x: x
        :type x: int
        :param y: y
        :type y: int
        """
        self.pos.set_xy(x,y)

    def set(self, dim: "Dimension"):
        """
        set the dimension

        :param dim: dimension
        :type dim: Dimension
        """
        self.pos = dim.pos
        self.size = dim.size

    @property
    def x1(self) -> int:
        return self.pos.x

    @x1.setter
    def x1(self, value: int) -> int:
        assert isinstance(value, int)

        self.pos.x = value

    @property
    def y1(self) -> int:
        return self.pos.y

    @y1.setter
    def y1(self, value: int) -> int:
        assert isinstance(value, int)

        self.pos.y = value

    @property
    def x2(self) -> int:
        return self.pos.x + self.size.width

    @x2.setter
    def x2(self, value: int) -> int:
        assert isinstance(value, int)

        self.size.width = value - self.pos.x

    @property
    def y2(self) -> int:
        return self.pos.y + self.size.height

    @y2.setter
    def y2(self, value: int) -> int:
        assert isinstance(value, int)

        self.size.height = value - self.pos.y

    @property
    def cx(self) -> int:
        return int(self.pos.x + self.size.width / 2)

    @property
    def cy(self) -> int:
        return int(self.pos.y + self.size.height / 2)

    @property
    def width(self) -> int:
        return self.size.width

    @width.setter
    def width(self, value: int) -> int:
        assert isinstance(value, int)

        self.size.width = value

    @property
    def height(self) -> int:
        return self.size.height

    @height.setter
    def height(self, value: int) -> int:
        assert isinstance(value, int)

        self.size.height = value


    def __repr__(self):
        return (
            f"<Dimension(x={self.pos.x}, y={self.pos.y}, "
            f"width={self.size.width}, height={self.size.height})>"
        )
