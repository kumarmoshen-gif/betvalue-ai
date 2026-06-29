from core.result_settlement import (
    compute_profit,
    is_bet_won,
    result_from_score,
)


assert result_from_score("Arsenal", "Chelsea", 2, 1) == "Arsenal"
assert result_from_score("Arsenal", "Chelsea", 1, 2) == "Chelsea"
assert result_from_score("Arsenal", "Chelsea", 1, 1) == "Draw"

assert is_bet_won("Arsenal", "arsenal") is True
assert is_bet_won("Draw", "Chelsea") is False

assert compute_profit(True, 2.1, 1) == 1.1
assert compute_profit(False, 2.1, 1) == -1
