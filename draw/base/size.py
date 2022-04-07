

class Size:
    """
    size (width, height)
    """
    def __init__(
        self,
        width: int,
        height: int
    ):
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
    def width(self, value: int):
        """
        set the width

        :param value: width
        :type value: int
        """
        assert isinstance(value, int)

        self._width = value

    @property
    def height(self) -> int:
        """
        return the height

        :return: height
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, value: int):
        """
        set the height

        :param value: height
        :type value: int
        """
        assert isinstance(value, int)

        self._height = value

    def set_wh(self, width: int, height: int):
        """
        set width and height at the same time

        :param width: width
        :type width: int
        :param height: height
        :type height: int
        """
        self.width = width
        self.height = height

    def set(self, size: "Size"):
        """
        set new size

        :param size: new size
        :type size: Size
        """
        assert isinstance(size, Size)

        self.width = size.width
        self.height = size.height

    def __repr__(self):
        return (
            f"<Size(width={self.width}, height={self.height}>"
        )
