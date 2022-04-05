from datetime import datetime
import math
import collections
import itertools
from enum import Enum

from dateutil.rrule import rrule, DAILY


class DateType(Enum):
    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"
    QUARTERS = "quarters"
    YEARS = "years"


class TimetableItem:
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
        if self.dt_type == DateType.YEARS:
            return self.year
        elif self.dt_type == DateType.QUARTERS:
            return self.quarter
        elif self.dt_type == DateType.MONTHS:
            return self.month
        elif self.dt_type == DateType.WEEKS:
            return self.week
        elif self.dt_type == DateType.DAYS:
            return self.day

        raise NotImplemented(f"Unknown date type '{self.dt_type}'!")

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
        return self.dt.weekday() in (0, 6)

    def __repr__(self) -> str:
        return (
            f"<TimetableItem(dt={self.dt}, year='{self.year}', "
            f"quarter='{self.quarter}', month='{self.month}', "
            f"week='{self.week}', day='{self.day}')>"
        )


class Timetable:
    def __init__(
        self,
        start_date: datetime,
        end_date: datetime,
        year_format: str = "%Y",
        quarter_format: str = "Q",
        month_format: str = "%b",
        week_format: str = "CW%V",
        day_format: str ="%d"
    ):
        # start and end date
        self.start_date = start_date
        self.end_date = end_date

        # formats
        self.year_format = year_format
        self.quarter_format = quarter_format
        self.month_format = month_format
        self.week_format = week_format
        self.day_format = day_format

    def _get(self, dt_type: DateType):
        # get all timetable items between start and end date
        tt_items = [
            TimetableItem(
                dt_type=dt_type,
                dt=dt,
                year_format=self.year_format,
                quarter_format=self.quarter_format,
                month_format=self.month_format,
                week_format=self.week_format,
                day_format=self.day_format
            )
            for dt in rrule(
                freq=DAILY,
                dtstart=self.start_date,
                until=self.end_date
            )
        ]

        # group them by the given date type
        return [
            list(g)
            for _, g in itertools.groupby(tt_items, key=lambda x: x.default)
        ]

    @property
    def years(self) -> str:
        return self._get(DateType.YEARS)

    @property
    def quarters(self) -> str:
        return self._get(DateType.QUARTERS)

    @property
    def months(self) -> str:
        return self._get(DateType.MONTHS)

    @property
    def weeks(self) -> str:
        return self._get(DateType.WEEKS)

    @property
    def days(self) -> str:
        return self._get(DateType.DAYS)

    def hierarchy(self):
        """
        hierarchy of different date resolutions with depth
        """
        res = []
        if self.year_format:
            res.append(self.years)

        if self.quarter_format:
            res.append(self.quarters)

        if self.month_format:
            res.append(self.months)

        if self.week_format:
            res.append(self.weeks)

        if self.day_format:
            res.append(self.days)

        return res

    def __repr__(self):
        return str(self.hierarchy())
