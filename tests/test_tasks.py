import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.task import Task

def test_task_creation():
    task = Task("Refactor CLI", "Alex")
    assert task.title == "Refactor CLI"
    assert task.status == "Incomplete"

def test_complete_task():
    task = Task("Write docs", "Sam")
    task.complete()
    assert task.status == "Complete"