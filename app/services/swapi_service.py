import httpx
from fastapi import HTTPException

BASE_URL = "https://swapi.py4e.com/api"

async def fetch_starships():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/starships/")
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=response.status_code, detail="Error fetching starships from SWAPI")
        data = response.json()

    starships = [
        {
            "name": starship.get("name"),
            "model": starship.get("model"),
            "cost_in_credits": starship.get("cost_in_credits"),
            "max_atmosphering_speed": starship.get("max_atmosphering_speed"),
        }
        for starship in data.get("results", [])
    ]

    return {"starships": starships, "next": data.get("next")}


async def fetch_starship_by_name(starship_name: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/starships/?search={starship_name}")
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError:
            return {"error": "Failed to fetch starship details."}

        if data["results"]:
            starship = data["results"][0]
            return {
                "name": starship.get("name"),
                "model": starship.get("model"),
                "cost_in_credits": starship.get("cost_in_credits"),
                "max_atmosphering_speed": starship.get("max_atmosphering_speed"),
                "crew_capacity": starship.get("crew"),
                "passenger_capacity": starship.get("passengers"),
                "cargo_capacity": starship.get("cargo_capacity"),
            }

    return {"error": "Starship not found"}


async def fetch_all_pilots_with_starships():
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}/people/"
        pilots = []

        while url:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPStatusError:
                return {"error": "Failed to fetch pilots."}

            for person in data["results"]:
                if person.get("starships"):
                    species_name = None
                    homeworld_name = None
                    starships = []

                    try:
                        if person.get("species"):
                            response = await client.get(person["species"][0])
                            response.raise_for_status()
                            species_name = response.json().get("name")

                        if person.get("homeworld"):
                            response = await client.get(person["homeworld"])
                            response.raise_for_status()
                            homeworld_name = response.json().get("name")

                        for starship_url in person.get("starships", []):
                            response = await client.get(starship_url)
                            response.raise_for_status()
                            starships.append(response.json().get("name"))
                    except httpx.HTTPStatusError:
                        return {"error": "Failed to fetch additional pilot data."}

                    pilots.append({
                        "name": person.get("name"),
                        "height": person.get("height"),
                        "gender": person.get("gender"),
                        "weight": person.get("mass"),
                        "birth_year": person.get("birth_year"),
                        "species_name": species_name,
                        "starships": starships,  # Cambiado a minúsculas
                        "homeworld": homeworld_name,
                    })

            url = data.get("next")

        return pilots


async def fetch_pilot_by_name(pilot_name: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/people/?search={pilot_name}")
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError:
            return {"error": "Failed to fetch pilot details."}

        for person in data["results"]:
            if person.get("starships") and person["name"].lower() == pilot_name.lower():
                species_name = None
                homeworld_name = None
                starships = []

                try:
                    if person.get("species"):
                        response = await client.get(person["species"][0])
                        response.raise_for_status()
                        species_name = response.json().get("name")

                    if person.get("homeworld"):
                        response = await client.get(person["homeworld"])
                        response.raise_for_status()
                        homeworld_name = response.json().get("name")

                    for starship_url in person.get("starships", []):
                        response = await client.get(starship_url)
                        response.raise_for_status()
                        starship_data = response.json()
                        starships.append({
                            "name": starship_data.get("name"),
                            "model": starship_data.get("model"),
                        })
                except httpx.HTTPStatusError:
                    return {"error": "Failed to fetch additional pilot data."}

                return {
                    "name": person.get("name"),
                    "height": person.get("height"),
                    "gender": person.get("gender"),
                    "weight": person.get("mass"),
                    "birth_year": person.get("birth_year"),
                    "species_name": species_name,
                    "starships": starships,
                    "homeworld": homeworld_name,
                }

        return {"error": "Pilot not found or has no starships."}

