from dataclasses import dataclass
from typing import Optional

from models.team_rating import TeamRating
from models.value_bet import ValueBet


@dataclass
class MatchPrediction:
    home: int
    draw: int
    away: int

    diff: float

    confidence: int

    home_rating: TeamRating
    away_rating: TeamRating

    value_bet: Optional[ValueBet]

    fallback: bool = False
    message: str = ""