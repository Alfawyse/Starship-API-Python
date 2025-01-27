import httpx

BASE_URL = "https://swapi.py4e.com/api"

async def fetch_starships():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/starships/")
        response.raise_for_status()
        data = response.json()

    starships = []
    for starship in data["results"]:
        starships.append({
            "name": starship.get("name"),
            "model": starship.get("model"),
            "cost_in_credits": starship.get("cost_in_credits"),
            "max_atmosphering_speed": starship.get("max_atmosphering_speed"),
        })

    return {"starships": starships, "next": data.get("next")}


async def fetch_starship_by_name(starship_name: str):
    async with httpx.AsyncClient() as client:
        # Usa el parámetro ?search para buscar por nombre
        response = await client.get(f"{BASE_URL}/starships/?search={starship_name}")
        response.raise_for_status()
        data = response.json()

        # Verifica si hay resultados
        if data["results"]:
            starship = data["results"][0]  # Toma la primera coincidencia
            return {
                "name": starship.get("name"),
                "model": starship.get("model"),
                "cost_in_credits": starship.get("cost_in_credits"),
                "max_atmosphering_speed": starship.get("max_atmosphering_speed"),
                "crew_capacity": starship.get("crew"),
                "passenger_capacity": starship.get("passengers"),
                "cargo_capacity": starship.get("cargo_capacity"),
            }

    # Si no se encuentra la nave
    return {"error": "Starship not found"}

