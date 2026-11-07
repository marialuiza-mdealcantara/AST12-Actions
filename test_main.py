from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root_status_code():
    response = client.get("/")
    assert response.status_code == 200


def test_read_root_content():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensagem": "API AST12 funcionando!"}


def test_somar_positivos():
    response = client.get("/somar/5/3")
    assert response.status_code == 200
    assert response.json() == {"resultado": 8}


def test_somar_negativos():
    response = client.get("/somar/-5/-3")
    assert response.status_code == 200
    assert response.json() == {"resultado": -8}


def test_multiplicar():
    response = client.get("/multiplicar/2/2")
    assert response.status_code == 200
    assert response.json() == {"resultado": 5}


def test_multiplicar_por_zero():
    response = client.get("/multiplicar/10/0")
    assert response.status_code == 200
    assert response.json() == {"resultado": 0}
