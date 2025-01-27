import httpx
from fastapi import HTTPException

BASE_URL = "https://swapi.py4e.com/api"


async def enrich_pilot_data(person: dict, client: httpx.AsyncClient) -> dict:
    """
    Enrich pilot data with species, homeworld, and starships information.

    Args:
        person (dict): The raw pilot data from SWAPI.
        client (httpx.AsyncClient): The HTTP client to make additional API requests.

    Returns:
        dict: A dictionary containing enriched pilot data.
    """
    species_name = None
    homeworld_name = None
    starships = []

    try:
        # Fetch species name
        if person.get("species"):
            response = await client.get(person["species"][0])
            response.raise_for_status()
            species_name = response.json().get("name")

        # Fetch homeworld name
        if person.get("homeworld"):
            response = await client.get(person["homeworld"])
            response.raise_for_status()
            homeworld_name = response.json().get("name")

        # Fetch starships details
        for starship_url in person.get("starships", []):
            response = await client.get(starship_url)
            response.raise_for_status()
            starship_data = response.json()
            starships.append({
                "name": starship_data.get("name"),
                "model": starship_data.get("model"),
            })
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=500, detail="Failed to fetch additional pilot data.")

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


async def fetch_starships():
    """
    Fetch a list of starships from the SWAPI.

    Returns:
        dict: A dictionary containing starship details and the next page URL if applicable.
    """
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
    """
    Fetch details of a specific starship by its name.

    Args:
        starship_name (str): The name of the starship to fetch.

    Returns:
        dict: A dictionary containing the starship's details or an error message.
    """
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
    """
    Fetch all pilots who pilot starships, enriched with additional data.

    Returns:
        list: A list of dictionaries containing enriched pilot data.
    """
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
                    enriched_pilot = await enrich_pilot_data(person, client)
                    pilots.append(enriched_pilot)

            url = data.get("next")

        return pilots


async def fetch_pilot_by_name(pilot_name: str):
    """
    Fetch detailed information about a specific pilot by name.

    Args:
        pilot_name (str): The name of the pilot to fetch.

    Returns:
        dict: A dictionary containing the pilot's details or an error message.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/people/?search={pilot_name}")
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError:
            return {"error": "Failed to fetch pilot details."}

        for person in data["results"]:
            if person.get("starships") and person["name"].lower() == pilot_name.lower():
                return await enrich_pilot_data(person, client)

        return {"error": "Pilot not found or has no starships."}


