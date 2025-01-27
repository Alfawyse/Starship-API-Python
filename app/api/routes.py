from fastapi import APIRouter
from app.services.swapi_service import fetch_starships, fetch_starship_by_name , fetch_all_pilots_with_starships , fetch_pilot_by_name

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





