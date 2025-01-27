import pytest
import respx
from fastapi.testclient import TestClient
from app.main import app
from httpx import Response
import httpx

client = TestClient(app)

# Prueba para listar pilotos con starships
@respx.mock
def test_list_pilots():
    # Simula respuesta de SWAPI para listar pilotos
    respx.get("https://swapi.py4e.com/api/people/").mock(
        return_value=Response(
            200,
            json={
                "results": [
                    {
                        "name": "Luke Skywalker",
                        "height": "172",
                        "gender": "male",
                        "mass": "77",
                        "birth_year": "19BBY",
                        "species": ["https://swapi.py4e.com/api/species/1/"],
                        "homeworld": "https://swapi.py4e.com/api/planets/1/",
                        "starships": ["https://swapi.py4e.com/api/starships/12/"]
                    },
                    {
                        "name": "Han Solo",
                        "height": "180",
                        "gender": "male",
                        "mass": "80",
                        "birth_year": "29BBY",
                        "species": ["https://swapi.py4e.com/api/species/1/"],
                        "homeworld": "https://swapi.py4e.com/api/planets/2/",
                        "starships": ["https://swapi.py4e.com/api/starships/10/"]
                    }
                ],
                "next": None,
            },
        )
    )

    # Simula species, planets y starships
    respx.get("https://swapi.py4e.com/api/species/1/").mock(
        return_value=Response(200, json={"name": "Human"})
    )
    respx.get("https://swapi.py4e.com/api/planets/1/").mock(
        return_value=Response(200, json={"name": "Tatooine"})
    )
    respx.get("https://swapi.py4e.com/api/planets/2/").mock(
        return_value=Response(200, json={"name": "Corellia"})
    )
    respx.get("https://swapi.py4e.com/api/starships/12/").mock(
        return_value=Response(200, json={"name": "X-wing", "model": "T-65 X-wing"})
    )
    respx.get("https://swapi.py4e.com/api/starships/10/").mock(
        return_value=Response(200, json={"name": "Millennium Falcon", "model": "YT-1300 light freighter"})
    )

    response = client.get("/pilots")
    assert response.status_code == 200
    data = response.json()
    assert len(data["pilots"]) == 2
    assert data["pilots"][0]["name"] == "Luke Skywalker"
    assert data["pilots"][1]["name"] == "Han Solo"


# Prueba para detalles de un piloto con starships
@respx.mock
def test_pilot_details_with_starships():
    # Simula respuesta de SWAPI para buscar a Luke Skywalker
    respx.get("https://swapi.py4e.com/api/people/?search=Luke%20Skywalker").mock(
        return_value=Response(
            200,
            json={
                "results": [
                    {
                        "name": "Luke Skywalker",
                        "height": "172",
                        "gender": "male",
                        "mass": "77",
                        "birth_year": "19BBY",
                        "species": ["https://swapi.py4e.com/api/species/1/"],
                        "homeworld": "https://swapi.py4e.com/api/planets/1/",
                        "starships": ["https://swapi.py4e.com/api/starships/12/"]
                    }
                ]
            },
        )
    )

    respx.get("https://swapi.py4e.com/api/species/1/").mock(
        return_value=Response(200, json={"name": "Human"})
    )
    respx.get("https://swapi.py4e.com/api/planets/1/").mock(
        return_value=Response(200, json={"name": "Tatooine"})
    )
    respx.get("https://swapi.py4e.com/api/starships/12/").mock(
        return_value=Response(200, json={"name": "X-wing", "model": "T-65 X-wing"})
    )


    response = client.get("/pilots/details/Luke Skywalker")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Luke Skywalker"
    assert data["gender"] == "male"
    assert data["birth_year"] == "19BBY"
    assert "starships" in data
    assert len(data["starships"]) == 1
    assert data["starships"][0]["name"] == "X-wing"

# Prueba para detalles de un piloto sin starships
@respx.mock
def test_pilot_details_without_starships():
    # Simula respuesta de SWAPI para un piloto sin starships
    respx.get("https://swapi.py4e.com/api/people/?search=C3PO").mock(
        return_value=Response(
            200,
            json={
                "results": [
                    {
                        "name": "C-3PO",
                        "height": "167",
                        "gender": "n/a",
                        "mass": "75",
                        "birth_year": "112BBY",
                        "species": ["https://swapi.py4e.com/api/species/2/"],
                        "homeworld": "https://swapi.py4e.com/api/planets/1/",
                        "starships": []  # Sin starships
                    }
                ]
            },
        )
    )

    response = client.get("/pilots/details/C3PO")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"] == "Pilot not found or has no starships."



# Prueba para piloto inexistente
@respx.mock
def test_pilot_details_not_found():
    # Simula respuesta de SWAPI para un piloto que no existe
    respx.get("https://swapi.py4e.com/api/people/?search=Nonexistent").mock(
        return_value=Response(200, json={"results": []})  # Sin resultados
    )

    response = client.get("/pilots/details/Nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"] == "Pilot not found or has no starships."


# Prueba para fallo de conexión a SWAPI
@respx.mock
def test_pilot_details_swapi_error():
    # Simula un fallo de conexión o error de SWAPI
    respx.get("https://swapi.py4e.com/api/people/?search=Luke%20Skywalker").mock(
        return_value=Response(500)
    )

    response = client.get("/pilots/details/Luke%20Skywalker")
    assert response.status_code == 500  # Verifica que el código de estado es 500
    data = response.json()
    assert "error" in data
    assert data["error"] == "Failed to connect to SWAPI."


