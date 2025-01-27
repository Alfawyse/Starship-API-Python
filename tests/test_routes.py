from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_starships():
    response = client.get("/starships")
    assert response.status_code == 200
    assert "starships" in response.json()

def test_get_starship_details_found():
    response = client.get("/starships/details/Millennium%20Falcon")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert data["name"] == "Millennium Falcon"

def test_get_starship_details_not_found():
    response = client.get("/starships/details/Nonexistent%20Starship")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "Starship not found"
