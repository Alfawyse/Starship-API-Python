from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_starships():
    response = client.get("/starships")
    assert response.status_code == 200
    assert "starships" in response.json()
