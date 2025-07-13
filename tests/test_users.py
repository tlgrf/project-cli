import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.user import User

def test_user_creation():
    u = User("Alice", "alice@example.com")
    assert u.name == "Alice"
    assert u.email == "alice@example.com"