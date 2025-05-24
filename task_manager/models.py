from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: str = "todo"
    due_date: datetime = None

class TaskNotFoundError(Exception):
    pass

class InvalidStatusError(Exception):
    pass