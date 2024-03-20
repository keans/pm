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
    year_format: str
    quarter_format: str
    month_format: str
    week_format: str
    day_format: str

    @property
    def default(self) -> str:
        return getattr(self, self.dt_type.value)

    @property
    def year(self) -> str:
        return self.dt.strftime(self.year_format)

    @property
    def quarter(self) -> str:
        return f"{self.quarter_format}{math.ceil(self.dt.month/3.)}"

    @property
    def month(self) -> str:
        return self.dt.strftime(self.month_format)

    @property
    def week(self) -> str:
        return self.dt.strftime(self.week_format)

    @property
    def day(self) -> str:
        return self.dt.strftime(self.day_format)

    def is_weekend(self) -> bool:
        return self.dt.weekday() in (5, 6)
