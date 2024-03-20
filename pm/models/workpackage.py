from dataclasses import dataclass, field


@dataclass
class Workpackage:
    """
    a workpackage consists of several tasks
    """

    name: str
    responsible: str
    tasks: list = field(default_factory=list)
    milestones: list = field(default_factory=list)

    def add_task(self, task):
        """
        add a task to the workpackage
        """
        self.tasks.append(task)

    def add_milestone(self, ms):
        """
        add a milestone to the workpackage
        """
        self.milestones.append(ms)
