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

async def fetch_all_pilots_with_starships():
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}/people/"
        pilots = []

        # Recorrer todas las páginas
        while url:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            for person in data["results"]:
                # Filtra solo los personajes que tienen starships
                if person.get("starships"):
                    # Recoge información adicional
                    species_name = None
                    homeworld_name = None
                    Starships = []

                    # Obtén especie
                    if person.get("species"):
                        response = await client.get(person["species"][0])
                        response.raise_for_status()
                        species_name = response.json().get("name")

                    # Obtén planeta de origen
                    if person.get("homeworld"):
                        response = await client.get(person["homeworld"])
                        response.raise_for_status()
                        homeworld_name = response.json().get("name")

                    # Obtén nombres de vehículos
                    for vehicle_url in person.get("starships", []):
                        response = await client.get(vehicle_url)
                        response.raise_for_status()
                        Starships.append(response.json().get("name"))

                    pilots.append({
                        "name": person.get("name"),
                        "height": person.get("height"),
                        "gender": person.get("gender"),
                        "weight": person.get("mass"),
                        "birth_year": person.get("birth_year"),
                        "species_name": species_name,
                        "Starships": Starships,
                        "homeworld": homeworld_name,
                    })

            url = data.get("next")  # Ir a la siguiente página

        return pilots


async def fetch_pilot_by_name(pilot_name: str):
    async with httpx.AsyncClient() as client:
        # Usa el parámetro ?search para buscar por nombre
        response = await client.get(f"{BASE_URL}/people/?search={pilot_name}")
        response.raise_for_status()
        data = response.json()

        # Verifica si hay resultados
        for person in data["results"]:
            # Verifica si tiene starships
            if person.get("starships") and person["name"].lower() == pilot_name.lower():
                # Inicializa los datos adicionales
                species_name = None
                homeworld_name = None
                Starships = []

                # Obtén el nombre de la especie (si existe)
                if person.get("species"):
                    response = await client.get(person["species"][0])
                    response.raise_for_status()
                    species_name = response.json().get("name")

                # Obtén el nombre del planeta de origen (si existe)
                if person.get("homeworld"):
                    response = await client.get(person["homeworld"])
                    response.raise_for_status()
                    homeworld_name = response.json().get("name")

                # Obtén los nombres de las naves pilotadas
                for starship_url in person.get("starships", []):
                    response = await client.get(starship_url)
                    response.raise_for_status()
                    Starships.append(response.json().get("name"))

                # Devuelve la información del piloto
                return {
                    "name": person.get("name"),
                    "height": person.get("height"),
                    "gender": person.get("gender"),
                    "weight": person.get("mass"),
                    "birth_year": person.get("birth_year"),
                    "species_name": species_name,
                    "Starships": Starships,
                    "homeworld": homeworld_name,
                }

        # Si no se encuentra el piloto
        return {"error": "Pilot not found or has no starships."}

