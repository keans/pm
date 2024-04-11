from dataclasses import dataclass
import datetime


@dataclass
class Event:
    """
    an event
    """

    name: str
    date: datetime.datetime
