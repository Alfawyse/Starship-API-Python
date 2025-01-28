from typing import List
from pydantic import BaseModel


class StarshipUpdate(BaseModel):
    """
    Schema representing the structure for updating a starship.

    Attributes:
        name (str): The name of the starship.
        model (str): The model of the starship.
        cost_in_credits (int): The cost of the starship in credits.
        max_atmosphering_speed (int): The maximum atmospheric speed of the starship.
        crew_capacity (int): The number of crew members the starship can hold.
        passenger_capacity (int): The number of passengers the starship can accommodate.
        pilots (List[str]): A list of pilot names associated with the starship.
    """
    name: str
    model: str
    cost_in_credits: int
    max_atmosphering_speed: int
    crew_capacity: int
    passenger_capacity: int
    pilots: List[str]
