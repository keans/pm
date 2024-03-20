class Margin:
    """
    margin (top, right, bottom, left)
    """

    def __init__(
        self,
        top: int,
        right: int,
        bottom: int,
        left: int,
    ):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    @property
    def tuple(self) -> tuple:
        """
        return margin a tuple (top, right, bottom, left)

        :return: tuple (top, right, bottom, left)
        :rtype: tuple
        """
        return (
            self.top,
            self.right,
            self.bottom,
            self.left,
        )

    def __repr__(self) -> str:
        """
        returns the string representation of the margin

        :return: string representation of the margin
        :rtype: str
        """
        return (
            f"<Margin(top={self.top}, right={self.right}, "
            f"bottom={self.bottom}, left={self.left})>"
        )
