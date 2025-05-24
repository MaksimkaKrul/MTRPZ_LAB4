import json
from pathlib import Path
from .models import Task, TaskNotFoundError

JSON_FILE = Path("tasks.json")

# task_manager/storage.py
def _load_tasks():
    if not JSON_FILE.exists():
        return []
    
    try:
        with open(JSON_FILE, "r") as f:
            content = f.read()
            if not content.strip():
                return []
            return [Task(**task) for task in json.loads(content)]
    except json.JSONDecodeError:
        return []

def _save_tasks(tasks):
    with open(JSON_FILE, "w") as f:
        json.dump([task.__dict__ for task in tasks], f, indent=2)

def add_task(task: Task):
    tasks = _load_tasks()
    task.id = len(tasks) + 1
    tasks.append(task)
    _save_tasks(tasks)

def get_all_tasks():
    return _load_tasks()

def delete_task(task_id: int):
    tasks = _load_tasks()
    filtered = [t for t in tasks if t.id != task_id]
    if len(filtered) == len(tasks):
        raise TaskNotFoundError(f"Task {task_id} not found")
    _save_tasks(filtered)

def update_task(task_id: int, **fields):
    tasks = _load_tasks()
    for task in tasks:
        if task.id == task_id:
            for key, value in fields.items():
                setattr(task, key, value)
            _save_tasks(tasks)
            return
    raise TaskNotFoundError(f"Task {task_id} not found")