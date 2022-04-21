class Event:
    """
    an event
    """
    def __init__(self, name, date):
        self.name = name
        self.date = date

    def __repr__(self):
        return (
            f"<Event(name='{self.name}', "
            f"date='{self.date}')>"
        )
