class Milestone:
    """
    a milestone of a workpackage
    """
    def __init__(self, name, responsible, date):
        self.name = name
        self.responsible = responsible
        self.date = date
    
    def __repr__(self):
        return (
            f"<Milestone(name='{self.name}', "
            f"responsible='{self.responsible}', date={self.date})>"
        )
