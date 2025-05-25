from fastapi import FastAPI, HTTPException
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .storage import get_all_tasks, add_task, update_task, delete_task
from .models import Task, TaskNotFoundError

app = FastAPI(title="Task Manager API")

STATUSES = ["todo", "in_progress", "done"]

# Вхідна модель для створення задачі
class TaskIn(BaseModel):
    title: str
    description: Optional[str] = ""
    due_date: Optional[datetime] = None

# Модель для оновлення задачі
class TaskUpdate(BaseModel):
    status: Optional[str] = Field(None, description="One of: todo, in_progress, done")
    due_date: Optional[datetime] = None

@app.get("/tasks", response_model=List[Task])
def list_tasks(status: Optional[str] = None):
    tasks = get_all_tasks()
    if status:
        if status not in STATUSES:
            raise HTTPException(status_code=400, detail="Invalid status")
        tasks = [t for t in tasks if t.status == status]
    return tasks

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_in: TaskIn):
    task = Task(id=0, title=task_in.title, description=task_in.description, due_date=task_in.due_date)
    add_task(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def modify_task(task_id: int, update: TaskUpdate):
    try:
        update_fields = update.dict(exclude_none=True)
        update_task(task_id, **update_fields)
        tasks = get_all_tasks()
        updated = next(t for t in tasks if t.id == task_id)
        return updated
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: int):
    try:
        delete_task(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
