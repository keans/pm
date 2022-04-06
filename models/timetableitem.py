import math
import datetime

from models.types import DateType


class TimetableItem:
    """
    item in the timetable
    """
    def __init__(
        self,
        dt_type: DateType,
        dt: datetime,
        year_format: str,
        quarter_format: str,
        month_format: str,
        week_format: str,
        day_format: str
    ):
        self.dt_type = dt_type
        self.dt = dt

        self.year_format = year_format
        self.quarter_format = quarter_format
        self.month_format = month_format
        self.week_format = week_format
        self.day_format = day_format

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

    def __repr__(self) -> str:
        return (
            f"<TimetableItem(dt={self.dt}, dt_type={self.dt_type}, "
            f"year='{self.year}', quarter='{self.quarter}', "
            f"month='{self.month}', week='{self.week}', day='{self.day}')>"
        )
