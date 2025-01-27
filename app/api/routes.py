from fastapi import APIRouter
from app.services.swapi_service import fetch_starships, fetch_starship_by_name

router = APIRouter()

@router.get("/starships")
async def get_starships():
    data = await fetch_starships()
    return data

@router.get("/starships/details/{starship_name}")
async def get_starship_details(starship_name: str):
    starship_details = await fetch_starship_by_name(starship_name)
    return starship_details



