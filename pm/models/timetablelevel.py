import itertools
from dataclasses import dataclass

from .types import DateType
from .timetableitem import TimetableItem


@dataclass
class TimetableLevel:
    """
    level in timetable hierarchy
    """

    dt_type: DateType
    items: list[TimetableItem]

    @property
    def grouped_items(self) -> list[TimetableItem, int]:
        """
        returns a list of grouped items as tuple, each
        consisting of the first representative of that
        group and count

        :return: list of grouped items
        :rtype: list[TimetableItem, int]
        """
        grouped_items = []
        for _, items in itertools.groupby(
            self.items,
            key=lambda item: str(item),
        ):
            # convert iterator to list, otherwise length cannot be obtained
            li = list(items)

            # create tuple of first item as representative
            # and the length of the list
            grouped_items.append(
                (
                    li[0],
                    len(li),
                )
            )

        return grouped_items
