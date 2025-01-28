import httpx
from fastapi import APIRouter, HTTPException

from app.models.schemas import StarshipUpdate
from app.services.swapi_service import (fetch_all_pilots_with_starships,
                                        fetch_pilot_by_name,
                                        fetch_starship_by_name,
                                        fetch_starships)

router = APIRouter()


@router.get("/starships")
async def get_starships():
    """
    Retrieve a list of all starships from the SWAPI service.

    Returns:
        dict: A dictionary containing starship details and the
        next page URL (if available).
    """
    return await fetch_starships()


@router.get("/starships/details/{starship_name}")
async def get_starship_details(starship_name: str):
    """
    Retrieve details for a specific starship by name.

    Args:
        starship_name (str): The name of the starship to search for.

    Returns:
        dict: The details of the requested starship.

    Raises:
        HTTPException: If the starship is not found.
    """
    starship = await fetch_starship_by_name(starship_name)
    if "error" in starship:
        raise HTTPException(
            status_code=404,
            detail=starship["error"],
        )
    return starship


@router.get("/pilots")
async def list_pilots():
    """
    Retrieve a list of pilots who have flown starships.

    Returns:
        dict: A dictionary containing a list of pilots.

    Raises:
        HTTPException: If there is an error fetching pilot data.
    """
    try:
        pilots = await fetch_all_pilots_with_starships()
        return {"pilots": pilots}
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch pilots: {exc}",
        )


@router.get("/pilots/details/{pilot_name}")
async def get_pilot_details(pilot_name: str):
    """
    Retrieve details for a specific pilot by name.

    Args:
        pilot_name (str): The name of the pilot to search for.

    Returns:
        dict: The details of the requested pilot.

    Raises:
        HTTPException: If there is an error or the pilot is not found.
    """
    try:
        pilot_details = await fetch_pilot_by_name(pilot_name)
        if "error" in pilot_details:
            raise HTTPException(
                status_code=404,
                detail=pilot_details["error"],
            )
        return pilot_details
    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=500,
            detail="Failed to connect to SWAPI.",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred.",
        )


# Simulated in-memory database for starships
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
    """
    Update the details of an existing starship.

    Args:
        starship (StarshipUpdate): The updated starship data.

    Returns:
        dict: A dictionary containing a success message
        and the updated starship details.

    Raises:
        HTTPException: If the starship is not found in the in-memory database.
    """
    if starship.name not in starships_db:
        raise HTTPException(status_code=404, detail="Starship not found")

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
