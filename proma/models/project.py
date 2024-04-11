import datetime
from dataclasses import dataclass, field

import yaml
import cerberus
from dateutil.parser import parse as dateutil_parse
from pytimeparse import parse as pytimeparse_parse

from .schema import proma_schema
from . import Workpackage, Task, Milestone, Event


@dataclass
class Project:
    """
    a project consists of multiple workpackages
    """

    name: str
    responsible: str
    start_date: datetime.datetime
    end_time: datetime.datetime
    workpackages: list = field(default_factory=list)

    @staticmethod
    def create_from(filename):
        """
        load a project from file and return it
        """
        project = Project(None, None, None, None)
        project.load(filename)

        return project

    @property
    def duration(self):
        return self.end_date - self.start_date

    @property
    def entries(self):
        """
        entries are the number of all tasks of all workpackages
        """
        return sum([1 for wp in self.workpackages for t in wp.tasks])

    def add_workpackage(
        self,
        wp: Workpackage,
    ):
        """
        add a workpackage to the project
        """
        self.workpackages.append(wp)

    def load(self, filename: str):
        """
        read yaml project file
        """
        with open(filename, "r") as f:
            project = yaml.safe_load(f)

            v = cerberus.Validator(proma_schema)
            if v.validate(project) is False:
                raise Exception(v.errors)

        # set internal variables based on doc
        self.name = project["name"]
        self.responsible = project["responsible"]
        self.start_date = dateutil_parse(
            project["start_date"],
            dayfirst=True,
        )
        self.end_date = dateutil_parse(project["end_date"])

        self.events = []
        for ev in project.get("events", []):
            event = Event(
                name=ev["name"],
                date=dateutil_parse(ev["date"]),
            )
            self.events.append(event)

        self.workpackages = []
        for wp in project.get("workpackages", []):
            # add workpackage
            workpackage = Workpackage(
                name=wp["name"],
                responsible=wp.get("responsible", "unknown"),
            )
            self.workpackages.append(workpackage)

            # add tasks to workpackage
            for t in wp.get("tasks", []):
                task = Task(
                    name=t["name"],
                    responsible=t.get("responsible", "tbd"),
                    start_date=dateutil_parse(t["start_date"]),
                    duration=datetime.timedelta(
                        seconds=pytimeparse_parse(t["duration"])
                    ),
                    depends_on=t.get("depends_on", None),
                    is_done=t.get("is_done", False),
                )
                workpackage.add_task(task)

                # add milestones to workpackage
                for ms in t.get("milestones", []):
                    milestone = Milestone(
                        ms["name"],
                        ms.get("responsible", "tbd"),
                        dateutil_parse(ms["date"]),
                    )
                    task.add_milestone(milestone)
