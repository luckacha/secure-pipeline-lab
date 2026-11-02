import pytest
from fastapi.testclient import TestClient

import main
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_tasks():
    main.tasks.clear()
    main.next_id = 1


def test_list_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == 201
    assert response.json() == []


def test_create_task():
    response = client.post("/tasks", json={"title": "Купить хлеб"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "title": "Купить хлеб", "done": False}
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "title": "Купить хлеб", "done": False}]


def test_get_missing_task():
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_create_task_without_title():
    response = client.post("/tasks", json={})
    assert response.status_code == 422
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_complete_task():
    response = client.post("/tasks", json={"title": "Купить хлеб"})
    assert response.status_code == 201
    task_id = response.json()["id"]
    response = client.patch(f"/tasks/{task_id}/done")
    assert response.status_code == 200
    assert response.json()["done"] is True
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["done"] is True


def test_delete_task():
    response = client.post("/tasks", json={"title": "Купить хлеб"})
    assert response.status_code == 201
    task_id = response.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []
