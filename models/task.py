import datetime


class Task:
    """
    a task that needs to be done; an have multiple milestones
    """
    def __init__(
        self, name: str, responsible: str, 
        start_date: datetime.date, duration: datetime.timedelta, 
        is_done: bool
    ):
        self.name = name
        self.responsible = responsible
        self.start_date = start_date
        self.duration = duration
        self.is_done = is_done

        self.dependencies = []

    @property
    def end_date(self):
        return self.start_date + self.duration

    def add_dependency(self, dependency: "Task"):
        """
        add another task as dependency
        """
        self.dependencies.append(dependency)

    def __repr__(self):
        return (
            f"<Task(name='{self.name}', responsible='{self.responsible}', "
            f"start_date={self.start_date}, duration={self.duration}, "
            f"is_done={self.is_done})>"
        )
