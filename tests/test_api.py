from fastapi.testclient import TestClient
from task_manager.api import app
import os
import json

client = TestClient(app)

def setup_module(module):
    # Очистити tasks.json перед запуском тестів
    with open("tasks.json", "w") as f:
        json.dump([], f)

def test_create_task():
    response = client.post("/tasks", json={
        "title": "API Test Task",
        "description": "Check API POST",
        "due_date": "2025-06-01"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "API Test Task"

def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1

def test_update_task():
    response = client.put("/tasks/1", json={
        "status": "done"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "done"

def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully."

def test_update_nonexistent_task():
    response = client.put("/tasks/999", json={"title": "Nothing"})
    assert response.status_code == 404

def test_delete_nonexistent_task():
    response = client.delete("/tasks/999")
    assert response.status_code == 404
