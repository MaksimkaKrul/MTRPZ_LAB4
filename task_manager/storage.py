import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from .models import Task, TaskNotFoundError

STORAGE_FILE = "tasks.json"

_tasks_in_memory: List[Task] = []
_next_id: int = 1

def _load_tasks_from_json():
    global _tasks_in_memory, _next_id
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            _tasks_in_memory = [Task(**item) for item in data]
            if _tasks_in_memory:
                _next_id = max(task.id for task in _tasks_in_memory) + 1
            else:
                _next_id = 1
    except FileNotFoundError:
        _tasks_in_memory = []
        _next_id = 1
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {STORAGE_FILE}. Starting with empty tasks.")
        _tasks_in_memory = []
        _next_id = 1

def _save_tasks_to_json():
    try:
        with open(STORAGE_FILE, "w", encoding="utf-8") as f:
            serialized_tasks = [task.model_dump(mode='json') if hasattr(task, 'model_dump') else task.dict() for task in _tasks_in_memory]
            json.dump(serialized_tasks, f, indent=4, ensure_ascii=False, default=str)
    except Exception as e:
        print(f"Error saving tasks to JSON: {e}")

_load_tasks_from_json()

def _reset_storage_for_tests():
    global _tasks_in_memory, _next_id
    _tasks_in_memory = []
    _next_id = 1
    _save_tasks_to_json() 

def get_all_tasks() -> List[Task]:
    return _tasks_in_memory.copy()

def get_task_by_id(task_id: int) -> Optional[Task]:
    for task in _tasks_in_memory:
        if task.id == task_id:
            return task
    return None

def add_task(task_data: Dict[str, Any]) -> Task:
    global _next_id
    new_task = Task(id=_next_id, **task_data)
    _tasks_in_memory.append(new_task)
    _next_id += 1
    _save_tasks_to_json()
    return new_task

def update_task(task_id: int, **update_fields: Any) -> Task:
    task_found = False
    updated_task = None
    for i, task in enumerate(_tasks_in_memory):
        if task.id == task_id:
            task_found = True
            for field, value in update_fields.items():
                if field == "status" and value not in ["todo", "in_progress", "done"]:
                    raise ValueError("Invalid status value.")
                if field == "due_date" and value is not None and not isinstance(value, datetime):
                    try:
                        value = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except ValueError:
                        raise ValueError("Invalid due_date format. Use ISO 8601.")
                setattr(task, field, value)
            updated_task = task
            break
    if not task_found:
        raise TaskNotFoundError(f"Task with id {task_id} not found.")
    _save_tasks_to_json()
    return updated_task

def delete_task(task_id: int):
    global _tasks_in_memory
    initial_len = len(_tasks_in_memory)
    _tasks_in_memory = [t for t in _tasks_in_memory if t.id != task_id]
    if len(_tasks_in_memory) == initial_len:
        raise TaskNotFoundError(f"Task with id {task_id} not found.")
    _save_tasks_to_json()