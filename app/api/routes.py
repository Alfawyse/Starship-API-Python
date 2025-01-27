from fastapi import APIRouter
from app.services.swapi_service import fetch_starships, fetch_starship_by_name , fetch_all_pilots_with_starships , fetch_pilot_by_name
from app.models.schemas import StarshipUpdate

router = APIRouter()

@router.get("/starships")
async def get_starships():
    data = await fetch_starships()
    return data

@router.get("/starships/details/{starship_name}")
async def get_starship_details(starship_name: str):
    starship_details = await fetch_starship_by_name(starship_name)
    return starship_details

@router.get("/pilots")
async def list_pilots():
    try:
        pilots = await fetch_all_pilots_with_starships()
        return {"pilots": pilots}
    except httpx.HTTPStatusError as e:
        return {"error": f"Failed to fetch pilots. {e}"}

@router.get("/pilots/details/{pilot_name}")
async def get_pilot_details(pilot_name: str):
    try:
        pilot_details = await fetch_pilot_by_name(pilot_name)
        return pilot_details
    except httpx.HTTPStatusError as e:
        return {"error": f"Failed to fetch pilot. {e}"}


# Simulamos una base de datos en memoria
starships_db = {
    "Millennium Falcon": {
        "name": "Millennium Falcon",
        "model": "YT-1300 light freighter",
        "cost_in_credits": 100000,
        "max_atmosphering_speed": 1050,
        "crew_capacity": 4,
        "passenger_capacity": 6,
        "pilots": ["Han Solo", "Chewbacca"],
    }
}


@router.put("/starships/update")
async def update_starship(starship: StarshipUpdate):
    # Verifica si la nave ya existe en la "base de datos"
    if starship.name not in starships_db:
        raise HTTPException(status_code=404, detail="Starship not found")

    # Actualiza los datos de la nave
    starships_db[starship.name] = {
        "name": starship.name,
        "model": starship.model,
        "cost_in_credits": starship.cost_in_credits,
        "max_atmosphering_speed": starship.max_atmosphering_speed,
        "crew_capacity": starship.crew_capacity,
        "passenger_capacity": starship.passenger_capacity,
        "pilots": starship.pilots,
    }

    return {
        "message": "Starship updated successfully",
        "data": starships_db[starship.name],
    }


