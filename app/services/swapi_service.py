import httpx

BASE_URL = "https://swapi.py4e.com/api"

async def fetch_starships():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/starships/")
        response.raise_for_status()  # Verifica errores HTTP
        return response.json()
