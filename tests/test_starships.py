import respx
from fastapi.testclient import TestClient
from httpx import Response

from app.main import app

client = TestClient(app)


# Test para listar starships
@respx.mock
def test_list_starships():
    respx.get("https://swapi.py4e.com/api/starships/").mock(
        return_value=Response(
            200,
            json={
                "results": [
                    {
                        "name": "X-wing",
                        "model": "T-65 X-wing",
                        "cost_in_credits": "149999",
                        "max_atmosphering_speed": "1050",
                    },
                    {
                        "name": "Millennium Falcon",
                        "model": "YT-1300 light freighter",
                        "cost_in_credits": "100000",
                        "max_atmosphering_speed": "1050",
                    },
                ],
                "next": None,
            },
        )
    )

    response = client.get("/starships")
    assert response.status_code == 200
    data = response.json()
    assert len(data["starships"]) == 2
    assert data["starships"][0]["name"] == "X-wing"
    assert data["starships"][1]["name"] == "Millennium Falcon"


# Test para buscar una starship por nombre
@respx.mock
def test_search_starship_by_name():
    respx.get("https://swapi.py4e.com/api/starships/?search=X-wing").mock(
        return_value=Response(
            200,
            json={
                "results": [
                    {
                        "name": "X-wing",
                        "model": "T-65 X-wing",
                        "cost_in_credits": "149999",
                        "max_atmosphering_speed": "1050",
                        "crew": "1",
                        "passengers": "0",
                        "cargo_capacity": "110",
                    }
                ]
            },
        )
    )

    response = client.get("/starships/details/X-wing")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "X-wing"
    assert data["model"] == "T-65 X-wing"
    assert data["cost_in_credits"] == "149999"
    assert data["max_atmosphering_speed"] == "1050"


# Test para starship inexistente
@respx.mock
def test_starship_not_found():
    respx.get("https://swapi.py4e.com/api/starships/?search=Nonexistent").mock(
        return_value=Response(200, json={"results": []})
    )

    response = client.get("/starships/details/Nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Starship not found"


# Test para fallo en SWAPI
@respx.mock
def test_starship_service_error():
    respx.get("https://swapi.py4e.com/api/starships/").mock(return_value=Response(500))

    response = client.get("/starships")
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Error fetching starships from SWAPI"


# Test para actualizar una starship
@respx.mock
def test_update_starship():
    # Datos de entrada para actualizar la nave
    updated_data = {
        "name": "Millennium Falcon",
        "model": "YT-1300 Updated",
        "cost_in_credits": 150000,
        "max_atmosphering_speed": 1100,
        "crew_capacity": 6,
        "passenger_capacity": 8,
        "pilots": ["Han Solo", "Chewbacca"],
    }

    # Realiza la solicitud de actualización
    response = client.put("/starships/update", json=updated_data)

    # Aserciones
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Starship updated successfully"
    assert data["data"]["name"] == "Millennium Falcon"
    assert data["data"]["model"] == "YT-1300 Updated"
    assert data["data"]["cost_in_credits"] == 150000
    assert data["data"]["max_atmosphering_speed"] == 1100
    assert data["data"]["crew_capacity"] == 6
    assert data["data"]["passenger_capacity"] == 8
    assert data["data"]["pilots"] == ["Han Solo", "Chewbacca"]
