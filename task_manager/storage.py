# task_manager/storage.py (тимчасова версія)
tasks = []
next_id = 1

def add_task(task):
    global next_id
    task['id'] = next_id
    tasks.append(task)
    next_id += 1

def get_all_tasks():
    return tasks.copy()

def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]