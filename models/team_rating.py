from dataclasses import dataclass


@dataclass
class TeamRating:
    attack: float
    defense: float
    form: float
    home: float
    rating: float