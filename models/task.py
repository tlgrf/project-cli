class Task:
    def __init__(self, title, assigned_to):
        self.title = title
        self.status = "Incomplete"
        self.assigned_to = assigned_to

    def complete(self):
        self.status = "Complete"

    def __repr__(self):
        return f"[{self.status}] {self.title} (Assigned to {self.assigned_to})"