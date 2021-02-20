import math
import datetime
import collections

from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY, YEARLY


class Timetable:
    def __init__(
        self, start_date, end_date,
        show_years=True, show_quarters=True, show_months=True,
        show_weeks=True, show_days=True
    ):
        self.start_date = start_date
        self.end_date = end_date

        self.shows = []
        if show_years is True:
            self.shows.append("year")
        if show_quarters is True:
            self.shows.append("quarter")
        if show_months is True:
            self.shows.append("month")
        if show_weeks is True:
            self.shows.append("week")
        if show_days is True:
            self.shows.append("day")

    def index(self, item):
        return self.show.index(item)

    def days(self, fmt="%d"):
        """
        get a list of all days between the start date and the end date
        """
        return [
            dt #.strftime(fmt)
            for dt in rrule(
                DAILY, dtstart=self.start_date, until=self.end_date
            )
        ]

    def weeks(self, fmt="%V"):
        """
        get a list of all weeks between the start date and the end date
        """
        # get first day of week of start date
        start_date = (
            self.start_date - datetime.timedelta(days=self.start_date.weekday())
        )
        # get last day of week of end date
        end_date = self.end_date + datetime.timedelta(days=6)

        return [
            dt.strftime(fmt)
            for dt in rrule(
                WEEKLY, dtstart=self.start_date, until=self.end_date
            )
        ]

    def months(self, fmt="%m"):
        """
        get a list of all months between the start date and the end date
        """
        # get first day of month for start date
        start_date = datetime.date(
            self.start_date.year, self.start_date.month, 1
        )
        # get first day of month for end date
        end_date = datetime.date(self.end_date.year, self.end_date.month, 1)

        return [
            dt.strftime(fmt)
            for dt in rrule(MONTHLY, dtstart=start_date, until=end_date)
        ]

    def quarters(self):
        """
        get a list of all months between the start date and the end date
        """
        # get first day of month for start date
        start_date = datetime.date(
            self.start_date.year, self.start_date.month, 1
        )
        # get first day of month for end date
        end_date = datetime.date(self.end_date.year, self.end_date.month, 1)

        return [
            f"Q{math.ceil(dt.month/3.)}"
            for dt in rrule(
                MONTHLY, dtstart=start_date, until=end_date,
                bymonth=(3, 6, 9, 12), bymonthday=1
            )
        ]

    def years(self, fmt="%Y"):
        """
        get a list of all year between the start date and the end date
        """
        # get first day of January for start date
        start_date = datetime.date(
            self.start_date.year, 1, 1
        )
        # get first day of January for end date
        end_date = datetime.date(self.end_date.year, 1, 1)

        return [
            dt.strftime(fmt)
            for dt in rrule(
                YEARLY, dtstart=start_date, until=end_date
            )
        ]

    def hierarchy(self):
        """
        hierarchy of different date resolutions with depth
        """
        res = []
        if "year" in self.shows:
            res.append(self.years())
        
        if "quarter" in self.shows:
            res.append(self.quarters())

        if "month" in self.shows:
            res.append(self.months())
        
        if "week" in self.shows:
            res.append(self.weeks())

        if "day" in self.shows:
            res.append(self.days())

        return res

    def __repr__(self):
        return str(self.hierarchy())
