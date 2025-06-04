# tests/test_api.py
from fastapi.testclient import TestClient
from task_manager.api import app
import os
import json
from task_manager import storage 

client = TestClient(app)

def setup_function(function):
    """Очистить состояние хранилища перед каждым тестом."""
    storage._reset_storage_for_tests() 

def test_initial_empty_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

def test_create_task():
    response = client.post("/tasks", json={
        "title": "API Test Task",
        "description": "Check API POST",
        "due_date": "2025-06-01T10:00:00" 
    })
    assert response.status_code == 201 
    data = response.json()
    assert data["title"] == "API Test Task"
    assert data["id"] == 1 
    assert data["status"] == "todo" 

def test_get_tasks():
    client.post("/tasks", json={"title": "Task A"}) 
    client.post("/tasks", json={"title": "Task B"}) 

    client.put("/tasks/2", json={"status": "in_progress"})

    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2 

    response_todo = client.get("/tasks?status=todo")
    assert response_todo.status_code == 200
    assert len(response_todo.json()) == 1 
    assert response_todo.json()[0]["title"] == "Task A"

    response_in_progress = client.get("/tasks?status=in_progress")
    assert response_in_progress.status_code == 200
    assert len(response_in_progress.json()) == 1
    assert response_in_progress.json()[0]["title"] == "Task B"

    response_invalid_status = client.get("/tasks?status=invalid")
    assert response_invalid_status.status_code == 400
    assert "Invalid status" in response_invalid_status.json()["detail"]


def test_update_task():
    create_response = client.post("/tasks", json={
        "title": "Task to update"
    })
    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={
        "status": "done"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "done"

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.json()["status"] == "done"

def test_delete_task():
    create_response = client.post("/tasks", json={
        "title": "Task to delete"
    })
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204 
    assert response.text == ""

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_update_nonexistent_task():
    response = client.put("/tasks/999", json={"status": "done"})
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]

def test_delete_nonexistent_task():
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]

def test_get_nonexistent_task():
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]