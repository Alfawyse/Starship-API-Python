from typing import List

from pydantic import BaseModel


class StarshipUpdate(BaseModel):
    name: str
    model: str
    cost_in_credits: int
    max_atmosphering_speed: int
    crew_capacity: int
    passenger_capacity: int
    pilots: List[str]  # Lista de nombres de pilotos
