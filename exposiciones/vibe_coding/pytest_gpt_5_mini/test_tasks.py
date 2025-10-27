import pytest


def test_create_task(client):
    payload = {
        "title": "Tarea de prueba",
        "description": "Descripción de prueba",
        "priority": "high",
        "due_date": "2025-10-30",
    }

    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["status"] == "pending"
    assert "id" in data


def test_list_and_get_task(client):
    # Crear dos tareas
    t1 = client.post("/tasks", json={"title": "Lista 1"}).json()
    t2 = client.post("/tasks", json={"title": "Lista 2"}).json()

    # Listar
    r = client.get("/tasks")
    assert r.status_code == 200
    tasks = r.json()
    ids = [t["id"] for t in tasks]
    assert t1["id"] in ids
    assert t2["id"] in ids

    # Obtener uno específico
    r2 = client.get(f"/tasks/{t1['id']}")
    assert r2.status_code == 200
    assert r2.json()["title"] == "Lista 1"


def test_update_task(client):
    t = client.post("/tasks", json={"title": "Actualizar"}).json()
    update_payload = {"title": "Actualizada", "priority": "low"}
    r = client.put(f"/tasks/{t['id']}", json=update_payload)
    assert r.status_code == 200
    updated = r.json()
    assert updated["title"] == "Actualizada"
    assert updated["priority"] == "low"


def test_delete_task(client):
    t = client.post("/tasks", json={"title": "Eliminar"}).json()

    # Borrar (soft-delete)
    r = client.delete(f"/tasks/{t['id']}")
    assert r.status_code == 204

    # Intentar obtener devuelve 404
    r2 = client.get(f"/tasks/{t['id']}")
    assert r2.status_code == 404


def test_integration_db_direct(db_session, client):
    # Crear vía API
    created = client.post("/tasks", json={"title": "Integración DB"}).json()

    # Comprobar directamente en la sesión de SQLAlchemy
    from models import Task

    record = db_session.query(Task).filter(Task.id == created["id"]).first()
    assert record is not None
    assert record.title == "Integración DB"
    assert record.is_deleted is False
