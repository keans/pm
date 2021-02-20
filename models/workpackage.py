class Workpackage:
    """
    a workpackage consists of several tasks 
    """
    def __init__(self, name, responsible):
        self.name = name
        self.responsible = responsible

        self.tasks = []
        self.milestones = []

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

    def __repr__(self):
        return (
            f"<Workpackage(name='{self.name}', "
            f"responsible='{self.responsible}')>"
        )
