def compute_home_advantage_score(is_home=True):
    """
    Score simple d'avantage du terrain.
    Domicile : bonus positif
    Extérieur : neutre
    """

from config import HOME_ADVANTAGE_SCORE, AWAY_ADVANTAGE_SCORE


def compute_home_advantage_score(is_home=True):
    """
    Score d'avantage du terrain.
    """

    if is_home:
        return HOME_ADVANTAGE_SCORE

    return AWAY_ADVANTAGE_SCORE