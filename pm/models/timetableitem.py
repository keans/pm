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
    formats: dict

    @property
    def default(self) -> str:
        """
        get default value of the timetable item

        :return: DateType value of the timetable item
        :rtype: str
        """
        return getattr(self, self.dt_type.value)

    def _fmt(self, level: DateType) -> str:
        """
        helper function that applies the format of the given
        hierarchy level to the datetime value of the item
        If level is not existing in the formats and empty
        string is returned.

        :param level: hierarchy level
        :type level: DateType
        :return: formatted time
        :rtype: str
        """
        fmt = self.formats.get(level.value, None)
        if fmt is None:
            # format not found => empty string
            return ""

        return self.dt.strftime(fmt)

    @property
    def year(self) -> str:
        return self._fmt(DateType.YEAR)

    @property
    def quarter(self) -> str:
        fmt = self.formats.get("quarter", None)
        if fmt is None:
            # format not found => empty string
            return ""

        return f"{fmt}{math.ceil(self.dt.month/3.)}"

    @property
    def month(self) -> str:
        return self._fmt(DateType.MONTH)

    @property
    def week(self) -> str:
        return self._fmt(DateType.WEEK)

    @property
    def day(self) -> str:
        return self._fmt(DateType.DAY)

    def is_weekend(self) -> bool:
        """
        returns True, if weekday is on weekend, i.e.,
        either Saturday of Sunday

        :return: True, if weekday is a day on weekend
        :rtype: bool
        """
        return self.dt.weekday() in (5, 6)
