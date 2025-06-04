from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""
    status: str = "todo" 
    created_at: datetime = Field(default_factory=datetime.now)
    due_date: Optional[datetime] = None

class TaskNotFoundError(Exception):
    """Custom exception raised when a task is not found."""
    pass