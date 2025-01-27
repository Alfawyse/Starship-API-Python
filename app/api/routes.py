from fastapi import APIRouter
from app.services.swapi_service import fetch_starships

router = APIRouter()

@router.get("/starships")
async def get_starships():
    data = await fetch_starships()
    starships = [{"name": s["name"], "model": s["model"], "cost": s["cost_in_credits"], "speed": s["max_atmosphering_speed"]} for s in data["results"]]
    return {"starships": starships}

