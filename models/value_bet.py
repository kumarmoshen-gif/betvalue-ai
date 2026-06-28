from dataclasses import dataclass


@dataclass
class ValueBet:
    odd: float
    ai_probability: float
    bookmaker_probability: float
    value: float
    decision: str