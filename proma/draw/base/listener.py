from typing import Any


class Listener:
    """
    helper class to manage listeners
    """

    def __init__(self, name: str):
        self.name = name
        self.listeners = []

    def add_listener(
        self,
        instance: Any,
    ):
        """
        add a listener

        :param instance: instance of the class that should be notified
        :type instance: Any
        """
        self.listeners.append(instance)

    def notify(self, **kwargs):
        """
        notify all previously added listeners on notify
        by passing given arguments
        """
        for listener in self.listeners:
            getattr(listener, self.name)(**kwargs)


class OnChangePositionListener(Listener):
    """
    listener class that is called when position is changed
    """

    def __init__(self):
        Listener.__init__(self, "on_change_position")


class OnChangeSizeListener(Listener):
    """
    listener class that is called when size is changed
    """

    def __init__(self):
        Listener.__init__(self, "on_change_size")


class OnChangeDimensionListener(Listener):
    """
    listener class that is called when dimension is changed
    """

    def __init__(self):
        Listener.__init__(self, "on_change_dimension")
