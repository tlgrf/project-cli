import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.project import Project
from models.task import Task

def test_project_creation():
    project = Project("App", "Simple CLI", "2025-08-01")
    assert project.title == "App"
    assert project.due_date == "2025-08-01"

def test_add_task_to_project():
    project = Project("CLI", "Build it", "2025-09-01")
    task = Task("Write code", "Dev")
    project.add_task(task)
    assert len(project.tasks) == 1