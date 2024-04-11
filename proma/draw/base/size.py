from proma.draw.base.listener import OnChangeSizeListener


class Size(OnChangeSizeListener):
    """
    size (width, height)
    """

    def __init__(
        self,
        width: int,
        height: int,
    ):
        self._width = 0
        self._height = 0

        OnChangeSizeListener.__init__(self)
        OnChangeSizeListener.add_listener(self, self)

        self.set_wh(width=width, height=height)

    @property
    def tuple(self) -> tuple:
        """
        return the size as tuple

        :return: (width, height)-tuple
        :rtype: tuple
        """
        return (self.width, self.height)

    @property
    def width(self) -> int:
        """
        return the width

        :return: width
        :rtype: int
        """
        return self._width

    @width.setter
    def width(
        self,
        value: int,
    ):
        """
        set the width

        :param value: width
        :type value: int
        """
        assert isinstance(value, int)

        self._width = value
        OnChangeSizeListener.notify(self, size=self)

    @property
    def height(self) -> int:
        """
        return the height

        :return: height
        :rtype: int
        """
        return self._height

    @height.setter
    def height(
        self,
        value: int,
    ):
        """
        set the height

        :param value: height
        :type value: int
        """
        assert isinstance(value, int)

        self._height = value
        OnChangeSizeListener.notify(self, size=self)

    def set_wh(
        self,
        width: int,
        height: int,
    ):
        """
        set width and height at the same time

        :param width: width
        :type width: int
        :param height: height
        :type height: int
        """
        self.width = width
        self.height = height

    def set(
        self,
        size: "Size",
    ):
        """
        set new size

        :param size: new size
        :type size: Size
        """
        assert isinstance(size, Size)

        self.width = size.width
        self.height = size.height

    def on_change_size(
        self,
        size: "Size",
    ):
        """
        override this method in a subclass to obtain size changes

        :param pos: new size
        :type pos: Size
        """
        assert issubclass(size.__class__, Size)

    def __repr__(self) -> str:
        """
        returns string representation of the size

        :return: string representation of the size
        :rtype: str
        """
        return f"<Size(width={self.width}, height={self.height}>"
