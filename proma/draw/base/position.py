from proma.draw.base.listener import OnChangePositionListener


class Position(OnChangePositionListener):
    """
    position (x, y)
    """

    def __init__(
        self,
        x: int,
        y: int,
    ):
        self._x = 0
        self._y = 0

        OnChangePositionListener.__init__(self)
        OnChangePositionListener.add_listener(self, self)

        self.set_xy(x, y)

    @property
    def tuple(self) -> tuple:
        """
        return the position as tuple

        :return: (x, y)-tuple
        :rtype: tuple
        """
        return (self.x, self.y)

    @property
    def x(self) -> int:
        """
        return the x

        :return: x
        :rtype: int
        """
        return self._x

    @x.setter
    def x(
        self,
        value: int,
    ):
        """
        set the x

        :param value: x
        :type value: int
        """
        assert isinstance(value, int)

        self._x = value
        OnChangePositionListener.notify(self, position=self)

    @property
    def y(self) -> int:
        """
        return the y

        :return: y
        :rtype: int
        """
        return self._y

    @y.setter
    def y(
        self,
        value: int,
    ):
        """
        set the y

        :param value: y
        :type value: int
        """
        assert isinstance(value, int)

        self._y = value
        OnChangePositionListener.notify(self, position=self)

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
        self.x = x
        self.y = y

    def set(
        self,
        pos: "Position",
    ):
        """
        set new position

        :param pos: new position
        :type pos: Position
        """
        assert isinstance(pos, Position)

        self.x = pos.x
        self.y = pos.y

    def on_change_position(
        self,
        position: "Position",
    ):
        """
        override this method in a subclass to obtain position changes

        :param pos: new position
        :type pos: Position
        """
        assert issubclass(position.__class__, Position)

    def __repr__(self) -> str:
        """
        returns string representation of the position

        :return: representation of the position
        :rtype: str
        """
        return f"<Position(x={self.x}, y={self.y}>"
