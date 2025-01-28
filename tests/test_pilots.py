import respx
from fastapi.testclient import TestClient
from httpx import Response

from app.main import app

client = TestClient(app)


@respx.mock
def test_list_pilots():
    """
    Test retrieving a list of pilots with starships from the API.
    """
    # Mock SWAPI response for listing pilots
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
                        "starships": ["https://swapi.py4e.com/api/starships/12/"],
                    },
                    {
                        "name": "Han Solo",
                        "height": "180",
                        "gender": "male",
                        "mass": "80",
                        "birth_year": "29BBY",
                        "species": ["https://swapi.py4e.com/api/species/1/"],
                        "homeworld": "https://swapi.py4e.com/api/planets/2/",
                        "starships": ["https://swapi.py4e.com/api/starships/10/"],
                    },
                ],
                "next": None,
            },
        )
    )

    # Mock species, planets, and starships responses
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
        return_value=Response(
            200, json={"name": "Millennium Falcon", "model": "YT-1300 light freighter"}
        )
    )

    response = client.get("/pilots")
    assert response.status_code == 200
    data = response.json()
    assert len(data["pilots"]) == 2
    assert data["pilots"][0]["name"] == "Luke Skywalker"
    assert data["pilots"][1]["name"] == "Han Solo"


@respx.mock
def test_pilot_details_with_starships():
    """
    Test retrieving details for a pilot with starships.
    """
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
                        "starships": ["https://swapi.py4e.com/api/starships/12/"],
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


@respx.mock
def test_pilot_details_without_starships():
    """
    Test retrieving details for a pilot without starships.
    """
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
                        "starships": [],
                    }
                ]
            },
        )
    )

    response = client.get("/pilots/details/C3PO")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Pilot not found or has no starships."


@respx.mock
def test_pilot_details_not_found():
    """
    Test retrieving details for a non-existent pilot.
    """
    respx.get("https://swapi.py4e.com/api/people/?search=Nonexistent").mock(
        return_value=Response(200, json={"results": []})
    )

    response = client.get("/pilots/details/Nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Pilot not found or has no starships."


@respx.mock
def test_pilot_details_swapi_error():
    """
    Test handling a SWAPI connection error.
    """
    respx.get("https://swapi.py4e.com/api/people/?search=Luke%20Skywalker").mock(
        return_value=Response(500)
    )

    response = client.get("/pilots/details/Luke Skywalker")
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Failed to fetch pilot details from SWAPI."
