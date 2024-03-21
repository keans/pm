from datetime import datetime
import itertools
from typing import Optional

from dateutil.rrule import rrule, DAILY

from pm.models.timetableitem import TimetableItem
from pm.models.types import DateType


# default formats per hierachy
DEFAULT_YEAR_FMT = "%Y"
DEFAULT_QUARTER_FMT = "Q"
DEFAULT_MONTH_FMT = "%B"
DEFAULT_MONTH_SHORT_FMT = "%b"
DEFAULT_WEEK_FMT = "CW%V"
DEFAULT_WEEK_SHORT_FMT = "%V"
DEFAULT_DAY_FMT = "%d"


# show all in hierarchy
FULL_FMT = {
    "year": DEFAULT_YEAR_FMT,
    "quarter": DEFAULT_QUARTER_FMT,
    "month": DEFAULT_MONTH_FMT,
    "week": DEFAULT_WEEK_FMT,
    "day": DEFAULT_DAY_FMT,
}

# show all in hierarchy
YEAR_MONTH_WEEK_FMT = {
    "year": DEFAULT_YEAR_FMT,
    "month": DEFAULT_MONTH_SHORT_FMT,
    "week": DEFAULT_WEEK_SHORT_FMT,
}


class Timetable:
    """
    timetable
    """

    def __init__(
        self,
        start_date: datetime,
        end_date: datetime,
        formats: dict = YEAR_MONTH_WEEK_FMT,
    ):
        # start and end date
        self.start_date = start_date
        self.end_date = end_date

        # ensure valid format entries
        self.formats = self._check_formats(formats)

    def _check_formats(self, formats: dict) -> dict:
        """
        check given format for valid entries
        => will raise an ValueError exception if wrong entry is found

        :param formats: formats that are checked
        :type formats: dict
        :raises ValueError: raised when wrong entry in formats dict found
        :return: simply the input formats dict
        :rtype: dict
        """
        for k in formats:
            if k not in DateType:
                # invalid format
                raise ValueError(
                    f"Unknown format '{k}' for Timetable! Abort.",
                )

        return formats

    def _get(
        self,
        dt_type: DateType,
    ) -> list:
        """
        returns a list of TimeTableItem between start and end date

        :param dt_type: _des
        :type dt_type: DateType
        :return: _description_
        :rtype: list
        """
        # get all timetable items between start and end date
        tt_items = [
            TimetableItem(
                dt_type=dt_type,
                dt=dt,
                formats=self.formats,
            )
            for dt in rrule(
                freq=DAILY,
                dtstart=self.start_date,
                until=self.end_date,
            )
        ]

        # group them by the given date type
        return [
            list(group)
            for _, group in itertools.groupby(
                tt_items,
                key=lambda x: x.default,
            )
        ]

    @property
    def years(self) -> list:
        """
        list of years

        :return: list of years
        :rtype: list
        """
        return self._get(DateType.YEAR)

    @property
    def quarters(self) -> list:
        """
        list of quarters

        :return: list of quarters
        :rtype: list
        """
        return self._get(DateType.QUARTER)

    @property
    def months(self) -> list:
        """
        list of months

        :return: list of months
        :rtype: list
        """
        return self._get(DateType.MONTH)

    @property
    def weeks(self) -> list:
        """
        list of weeks

        :return: list of weeks
        :rtype: list
        """
        return self._get(DateType.WEEK)

    @property
    def days(self) -> list:
        """
        list of days

        :return: list of days
        :rtype: list
        """
        return self._get(DateType.DAY)
   
    @property
    def hierarchy(self) -> list[str]:
        """
        hierarchy of different date resolutions in depth

        :return: list of strings each from hierarchy
        :rtype: list[str]
        """
        return [
            getattr(self, f"{level.value}s")
            for level in DateType
            if level.value in self.formats
        ]
    
    @property
    def hierarchy_count(self) -> int:
        """
        number of levels in the hierarchy

        :return: number of levels in hierarchy
        :rtype: int
        """
        return len(self.hierarchy)

    def get_pos(self, dt: datetime,) -> int:
        """
        returns the position of the given date
        on the lowest hierarchy

        :param dt: datetime for which position is obtained
        :type dt: datetime
        :return: position of the given datetime
        :rtype: int
        """
        TODO: ONLY ON LOWEST LEVEL!!!
        return [
            d.dt 
            for d in itertools.chain(*self.days)
        ].index(dt)

    def __repr__(self) -> str:
        return str(self.hierarchy)
