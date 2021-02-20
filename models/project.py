import datetime

import yaml
import cerberus
from dateutil.parser import parse as dateutil_parse
from pytimeparse import parse as pytimeparse_parse

from models.schema import schema
from models import Workpackage, Task, Milestone


class Project:
    """
    a project consists of multiple workpackages
    """
    def __init__(self, name, responsible, start_date, end_date):
        self.name = name
        self.responsible = responsible
        self.start_date = start_date
        self.end_date = end_date

        self.workpackages = []
    
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
        return sum([
            1
            for wp in self.workpackages
            for t in wp.tasks
        ])

    def add_workpackage(self, wp):
        """
        add a workpackage to the project
        """
        self.workpackages.append(wp)

    def load(self, filename):
        """
        read yaml project file
        """
        with open(filename, "r") as f:
            project = yaml.safe_load(f)
        
            v = cerberus.Validator(schema)
            if v.validate(project) is False:
                raise Exception(v.errors)
        
        # set internal variables based on doc
        self.name = project["name"]
        self.responsible = project["responsible"]
        self.start_date = dateutil_parse(project["start_date"])
        self.end_date = dateutil_parse(project["end_date"])

        self.workpackages = []
        for wp in project["workpackages"]:
            # add workpackage
            workpackage = Workpackage(
                wp["name"], wp["responsible"]
            )
            self.workpackages.append(workpackage)

            # add tasks to workpackage
            for t in wp.get("tasks", []):
                task = Task(
                    t["name"], 
                    t.get("responsible", "tbd"), 
                    dateutil_parse(t["start_date"]), 
                    datetime.timedelta(
                        seconds=pytimeparse_parse(t["duration"])
                    ), 
                    t.get("is_done", False)
                )
                workpackage.add_task(task)

            # add milestones to workpackage
            for ms in wp.get("milestones", []):
                milestone = Milestone(
                    ms["name"], 
                    ms.get("responsible", "tbd"), 
                    dateutil_parse(ms["date"]), 
                )
                workpackage.add_milestone(milestone)
    
    def __repr__(self):
        return (
            f"<Project(name='{self.name}', responsible='{self.responsible}', "
            f"start_date={self.start_date}, end_date={self.end_date})>"
        )
