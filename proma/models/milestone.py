from dataclasses import dataclass
import datetime


@dataclass
class Milestone:
    """
    a milestone of a workpackage
    """

    name: str
    responsible: str
    date: datetime.datetime
