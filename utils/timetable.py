from datetime import datetime
import math
import itertools

from dateutil.rrule import rrule, DAILY

from models.timetableitem import TimetableItem
from models.types import DateType


class Timetable:
    """
    timetable
    """
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
        return self._get(DateType.YEAR)

    @property
    def quarters(self) -> str:
        return self._get(DateType.QUARTER)

    @property
    def months(self) -> str:
        return self._get(DateType.MONTH)

    @property
    def weeks(self) -> str:
        return self._get(DateType.WEEK)

    @property
    def days(self) -> str:
        return self._get(DateType.DAY)

    def get_pos(self, dt: datetime) -> int:
        return [
            d.dt
            for d in itertools.chain(*self.days)
        ].index(dt)

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

    def hierarchy_count(self):
        return len(self.hierarchy())

    def __repr__(self):
        return str(self.hierarchy())
