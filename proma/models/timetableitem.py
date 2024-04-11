import math
import datetime
from dataclasses import dataclass

from .types import DateType


@dataclass
class TimetableItem:
    """
    item in the timetable
    """

    dt_type: DateType
    dt: datetime
    format: str

    @property
    def is_weekend(self) -> bool:
        """
        returns True, if weekday is on weekend, i.e.,
        either Saturday of Sunday

        :return: True, if weekday is a day on weekend
        :rtype: bool
        """
        return self.dt.weekday() in (5, 6)

    def __str__(self) -> str:
        """
        return string representation of time table item

        :return: string representation of time table item
        :rtype: str
        """
        if self.format is None:
            # format not found => empty string
            return ""

        if self.dt_type == DateType.QUARTER:
            # special case for quarter
            return f"{self.format}{math.ceil(self.dt.month/3.)}"

        return self.dt.strftime(self.format)
