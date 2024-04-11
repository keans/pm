from datetime import datetime
from typing import Tuple

from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY, YEARLY

from proma.models.timetableitem import TimetableItem
from proma.models.timetablelevel import TimetableLevel
from proma.models.types import DateType


# default formats per hierachy
DEFAULT_YEAR_FMT = "%Y"
DEFAULT_QUARTER_FMT = "Q"
DEFAULT_MONTH_FMT = "%B"
DEFAULT_MONTH_SHORT_FMT = "%b"
DEFAULT_WEEK_FMT = "CW%V"
DEFAULT_WEEK_SHORT_FMT = "%V"
DEFAULT_DAY_FMT = "%d"


# show year, quarter, month, week and day
YEAR_QUARTER_MONTH_WEEK_DAY_FMT = {
    DateType.YEAR: DEFAULT_YEAR_FMT,
    DateType.QUARTER: DEFAULT_QUARTER_FMT,
    DateType.MONTH: DEFAULT_MONTH_FMT,
    DateType.WEEK: DEFAULT_WEEK_FMT,
    DateType.DAY: DEFAULT_DAY_FMT,
}

# show year, month and week
YEAR_MONTH_WEEK_FMT = {
    DateType.YEAR: DEFAULT_YEAR_FMT,
    DateType.MONTH: DEFAULT_MONTH_SHORT_FMT,
    DateType.WEEK: DEFAULT_WEEK_SHORT_FMT,
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

    @property
    def freq(self) -> int:
        """
        get dateutil rrule frequency based on lowest level in hierachy, e.g.,
        DAILY, WEEKLY, MONTHLY etc.

        please notice that QUARTER is not existing for rrule
        thus cannot be used as lowest level!

        :return: rrule frequency
        :rtype: int
        """
        return {
            DateType.DAY: DAILY,
            DateType.WEEK: WEEKLY,
            DateType.MONTH: MONTHLY,
            DateType.YEAR: YEARLY,
        }[self.hierarchy[-1]]

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

    def _get_timetable_level(
        self,
        dt_type: DateType,
    ) -> TimetableLevel:
        """
        returns timetable level of the date type including
        all timetable items between start and end date

        :param dt_type: date type
        :type dt_type: DateType
        :return: timetable level
        :rtype: TimetableLevel
        """
        # get all timetable items based on rrule
        items = [
            TimetableItem(
                dt_type=dt_type,
                dt=dt,
                format=self.formats[dt_type],
            )
            for dt in rrule(
                freq=self.freq,
                dtstart=self.start_date,
                until=self.end_date,
            )
        ]

        return TimetableLevel(dt_type=dt_type, items=items)

    @property
    def items_per_hierarchy(self) -> list:
        """
        return list of timetable levels based on hierachy

        :return: list of timetable levels based on hierachy
        :rtype: list
        """
        return [
            self._get_timetable_level(level)
            for level in DateType
            if level in self.formats
        ]

    @property
    def hierarchy(self) -> list[str]:
        """
        hierarchy of different DateType

        :return: list of strings each from hierarchy
        :rtype: list[str]
        """
        return [level for level in DateType if level in self.formats]

    def get_pos(
        self,
        dt: datetime,
    ) -> int:
        """
        returns the position of the given date
        on the lowest hierarchy

        :param dt: datetime for which position is obtained
        :type dt: datetime
        :return: position of the given datetime
        :rtype: int
        """
        # get all formatted dates of lowest level in hierarchy
        dates = [str(item) for item in self.items_per_hierarchy[-1].items]

        # find given date in prepared list
        return dates.index(dt.strftime(self.formats[self.hierarchy[-1]]))

    def get_from_and_length_pos(
        self,
        from_date: datetime,
        to_date: datetime,
        col_offset: int,
    ) -> Tuple[int, int]:
        """
        returns the position of the from date and
        the length of the to date

        :param from_date: from date
        :type from_date: datetime
        :param to_date: to date
        :type to_date: datetime
        :param col_offset: offset the column is shifted
        :type col_offset: int
        :return: tuple with position of from data and length
        :rtype: Tuple[int, int]
        """
        # compute pos
        pos = self.get_pos(from_date) + col_offset

        # get length between start and end date
        items_len = self.get_pos(to_date) - self.get_pos(from_date)

        if self.freq == DAILY:
            # in case of daily
            items_len -= 1

        return (pos, items_len)

    def __repr__(self) -> str:
        """
        returns the string representation of the hierarchy

        :return: string representation of the hierarchy
        :rtype: str
        """
        return str(self.hierarchy)
