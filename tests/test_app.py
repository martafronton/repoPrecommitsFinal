import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.testing = True
    return flask_app.test_client()


import json
import app as app_module


def test_homepage_renders(client):
    """Verifica que la página de inicio se renderiza correctamente."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Mini To-Do" in response.data


def test_create_task_api():

    """
        Prueba unitaria para verificar la creación de una tarea a través de la API REST.
    """
    app_module.TAREAS.clear()
    app = app_module.app
    client = app.test_client()

    r = client.post("/api/tareas", json={"texto": "Probar test"})
    assert r.status_code == 201
    data = r.get_json()
    assert data["ok"] is True
    assert data["data"]["texto"] == "Probar test"

    r = client.get("/api/tareas")
    listado = r.get_json()["data"]
    assert len(listado) == 1
    assert listado[0]["texto"] == "Probar test"
