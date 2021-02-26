import math
import collections

from dateutil.rrule import rrule, DAILY


class Timetable:
    def __init__(
        self, start_date, end_date,
        show_years="%Y", show_quarters="Q", show_months="%m",
        show_weeks="CW%V", show_days="%d"
    ):
        self.start_date = start_date
        self.end_date = end_date

        self.shows = collections.OrderedDict()
        if show_years is not None:
            self.shows["year"] = lambda dt: dt.strftime(show_years)
        if show_quarters is not None:
            self.shows["quarter"] = lambda dt: f"Q{math.ceil(dt.month/3.)}"
        if show_months is not None:
            self.shows["month"] = lambda dt: dt.strftime(show_months)
        if show_weeks is not None:
            self.shows["week"] = lambda dt: dt.strftime(show_weeks)
        if show_days is not None:
            self.shows["day"] = lambda dt: dt.strftime(show_days)

    def days(self, fmt="%d", unique=False):
        """
        get a list of all days between the start date and the end date
        """
        li = [
            {
                "dt": dt,
                "fmt": dt.strftime(fmt)
            }
            for dt in rrule(
                DAILY, dtstart=self.start_date, until=self.end_date
            )
        ]

        if unique is True:
            # get unique items (concerning the previous entry)
            res = [li[0]]
            [res.append(x) for x in li[1:] if res[-1]["fmt"] != x["fmt"]]

            return res

        return li

    def weeks(self, fmt="CW%V", unique=False):
        """
        get a list of all weeks between the start date and the end date
        """
        return self.days(fmt, unique)

    def months(self, fmt="%b", unique=False):
        """
        get a list of all months between the start date and the end date
        """
        return self.days(fmt, unique)

    def quarters(self, unique=False):
        """
        get a list of all months between the start date and the end date
        """
        li = [
            {
                "dt": dt["dt"],
                "fmt": f"Q{math.ceil(dt['dt'].month/3.)}"
            }
            for dt in self.days()
        ]
        if unique is True:
            # get unique items (concerning the previous entry)
            res = [li[0]]
            [res.append(x) for x in li[1:] if res[-1]["fmt"] != x["fmt"]]

            return res

        return li

    def years(self, fmt="%Y", unique=False):
        """
        get a list of all months between the start date and the end date
        """
        return self.days(fmt, unique)

    def is_weekend(self):
        """
        get a list of weekend flags of all days
        """
        return [
            dt.weekday() in (0, 6)
            for dt, _ in self.days(fmt=None)
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
