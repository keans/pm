import datetime
from dataclasses import dataclass, field

from .milestone import Milestone


@dataclass
class Task:
    """
    a task that needs to be done; an have multiple milestones
    """

    name: str
    responsible: str
    start_date: datetime.datetime
    duration: datetime.timedelta
    depends_on: str
    is_done: bool
    dependencies: list = field(default_factory=list)
    milestones: list = field(default_factory=list)

    @property
    def end_date(self):
        return self.start_date + self.duration

    def add_dependency(self, dependency: "Task"):
        """
        add another task as dependency
        """
        assert isinstance(dependency, Task)

        self.dependencies.append(dependency)

    def add_milestone(self, milestone: "Milestone"):
        """
        add milestone to the task
        """
        assert isinstance(milestone, Milestone)

        self.milestones.append(milestone)
