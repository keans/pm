class Padding:
    """
    padding (top, right, bottom, left)
    """
    def __init__(
        self,
        top: int,
        right: int,
        bottom: int,
        left: int
    ):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    @property
    def tuple(self) -> tuple:
        """
        return padding a tuple (top, right, bottom, left)

        :return: tuple (top, right, bottom, left)
        :rtype: tuple
        """
        return (self.top, self.right, self.bottom, self.left)

    def __repr__(self):
        return (
            f"<Padding(top={self.top}, right={self.right}, "
            f"bottom={self.bottom}, left={self.left})>"
        )
