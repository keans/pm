from proma.draw.base.listener import OnChangeDimensionListener
from proma.draw.base.position import Position
from proma.draw.base.size import Size


class Dimension(OnChangeDimensionListener):
    """
    dimension (x, y, width, height)
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
    ):
        OnChangeDimensionListener.__init__(self)
        self.pos = Position(x, y)
        self.size = Size(width, height)

        OnChangeDimensionListener.add_listener(self, self)
        self.pos.add_listener(self)
        self.size.add_listener(self)

    def on_change_position(
        self,
        position: Position,
    ):
        """
        forward on change position event to dimension change event

        :param size: position
        :type size: Position
        """
        OnChangeDimensionListener.notify(
            self,
            dimension=self,
        )

    def on_change_size(
        self,
        size: Size,
    ):
        """
        forward on change size event to dimension change event

        :param size: size
        :type size: Size
        """
        OnChangeDimensionListener.notify(
            self,
            dimension=self,
        )

    def on_change_dimension(
        self,
        dimension: "Dimension",
    ):
        """
        override this method in a subclass to obtain dimension changes

        :param dimension: dimension
        :type dimension: Dimension
        """
        assert issubclass(dimension.__class__, Dimension)

    @property
    def tuple(self) -> tuple:
        """
        return the dimension as tuple

        :return: (x, y, width, height)-tuple
        :rtype: tuple
        """
        return (
            self.pos.x,
            self.pos.y,
            self.size.width,
            self.size.height,
        )

    @property
    def x(self) -> int:
        """
        return x

        :return: x
        :rtype: int
        """
        return self.pos.x

    @property
    def y(self) -> int:
        """
        return y

        :return: y
        :rtype: int
        """
        return self.pos.y

    @property
    def xy(self) -> tuple:
        """
        return the (x, y) tuple

        :return: (x, y)-tuple
        :rtype: tuple
        """
        return (self.pos.x, self.pos.y)

    @property
    def x2y2(self) -> tuple:
        """
        return the (x2, y2) tuple

        :return: (x2, y2)-tuple
        :rtype: tuple
        """
        return (
            self.pos.x + self.size.width,
            self.pos.y + self.size.height,
        )

    @property
    def wh(self) -> tuple:
        """
        return the (w, h) tuple

        :return: (w, h)-tuple
        :rtype: tuple
        """
        return (
            self.size.width,
            self.size.height,
        )

    @property
    def tuple(self) -> tuple:
        """
        return the dimension as tuple

        :return: (x, y, width, height)-tuple
        :rtype: tuple
        """
        return (
            self.x,
            self.y,
            self.width,
            self.height,
        )

    @property
    def rect(self) -> tuple:
        """
        return the dimension as rectangle

        :return: (x1, y1, x2, y2)-tuple
        :rtype: tuple
        """
        return (
            self.x1,
            self.y1,
            self.x2,
            self.y2,
        )

    @property
    def pos(self) -> Position:
        """
        return position

        :return: position
        :rtype: Position
        """
        return self._pos

    @property
    def cpos(self) -> Position:
        """
        return center position

        :return: center position
        :rtype: Position
        """
        return Position(
            self.cx,
            self.cy,
        )

    @pos.setter
    def pos(self, value: Position):
        """
        set the position
        """
        assert isinstance(value, Position)

        self._pos = value
        OnChangeDimensionListener.notify(
            self,
            dimension=self,
        )

    @property
    def size(self) -> Size:
        """
        return size

        :return: size
        :rtype: size
        """
        return self._size

    @size.setter
    def size(
        self,
        value: Size,
    ):
        """
        set the size
        """
        assert isinstance(value, Size)

        self._size = value
        OnChangeDimensionListener.notify(self, dimension=self)

    def set_xy(
        self,
        x: int,
        y: int,
    ):
        """
        set x and y at the same time

        :param x: x
        :type x: int
        :param y: y
        :type y: int
        """
        self.pos.set_xy(x, y)

    def set(
        self,
        dim: "Dimension",
    ):
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
    def x1(
        self,
        value: int,
    ) -> int:
        assert isinstance(value, int)

        self.pos.x = value

    @property
    def y1(self) -> int:
        return self.pos.y

    @y1.setter
    def y1(
        self,
        value: int,
    ) -> int:
        assert isinstance(value, int)

        self.pos.y = value

    @property
    def x2(self) -> int:
        return self.pos.x + self.size.width

    @x2.setter
    def x2(
        self,
        value: int,
    ) -> int:
        assert isinstance(value, int)

        self.size.width = value - self.pos.x

    @property
    def y2(self) -> int:
        return self.pos.y + self.size.height

    @y2.setter
    def y2(
        self,
        value: int,
    ) -> int:
        assert isinstance(value, int)

        self.size.height = value - self.pos.y

    @property
    def cx(self) -> int:
        if getattr(self, "_size", None) is None:
            # size not yet set
            return -1

        return int(self.pos.x + self.size.width / 2)

    @property
    def cy(self) -> int:
        if getattr(self, "_size", None) is None:
            # size not yet set
            return -1

        return int(self.pos.y + self.size.height / 2)

    @property
    def width(self) -> int:
        return self.size.width

    @width.setter
    def width(
        self,
        value: int,
    ) -> int:
        assert isinstance(value, int)

        self.size.width = value

    @property
    def height(self) -> int:
        return self.size.height

    @height.setter
    def height(
        self,
        value: int,
    ) -> int:
        assert isinstance(value, int)

        self.size.height = value

    def set_wh(
        self,
        width: int,
        height: int,
    ):
        """
        set width and height at the same time

        :param width: w
        :type width: int
        :param height: h
        :type height: int
        """
        self.size.set_wh(width=width, height=height)

    def __repr__(self) -> str:
        """
        returns the string reprentation of the dimension

        :return: string reprentation of the dimension
        :rtype: str
        """
        return (
            f"<Dimension(x={self.pos.x}, y={self.pos.y}, "
            f"width={self.size.width}, height={self.size.height})>"
        )
