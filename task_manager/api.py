from fastapi import FastAPI, HTTPException
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .storage import get_all_tasks, add_task, update_task, delete_task, get_task_by_id
from .models import Task, TaskNotFoundError

app = FastAPI(title="Task Manager API")

STATUSES = ["todo", "in_progress", "done"]

class TaskIn(BaseModel):
    title: str
    description: Optional[str] = ""
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    status: Optional[str] = Field(None, description="One of: todo, in_progress, done")
    due_date: Optional[datetime] = None

@app.get("/tasks", response_model=List[Task])
def list_tasks(status: Optional[str] = None):
    tasks = get_all_tasks()
    if status:
        if status not in STATUSES:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(STATUSES)}")
        tasks = [t for t in tasks if t.status == status]
    return tasks

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_in: TaskIn):
    created_task = add_task(task_in.model_dump(exclude_unset=True))
    return created_task

@app.get("/tasks/{task_id}", response_model=Task)
def get_single_task(task_id: int):
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def modify_task(task_id: int, update: TaskUpdate):
    try:
        update_fields = update.model_dump(exclude_none=True)
        updated_task = update_task(task_id, **update_fields)
        return updated_task
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: int):
    try:
        delete_task(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")