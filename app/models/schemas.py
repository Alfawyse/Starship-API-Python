from pydantic import BaseModel
from typing import List

class StarshipUpdate(BaseModel):
    name: str
    model: str
    cost_in_credits: int
    max_atmosphering_speed: int
    crew_capacity: int
    passenger_capacity: int
    pilots: List[str]
