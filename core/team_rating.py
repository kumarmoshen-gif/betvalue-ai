from core.attack_score import compute_attack_score
from core.defense_score import compute_defense_score
from core.recent_form_score import compute_recent_form_score
from core.home_advantage import compute_home_advantage_score

from config import (
    ATTACK_WEIGHT,
    DEFENSE_WEIGHT,
    FORM_WEIGHT,
    HOME_WEIGHT,
)


def compute_team_rating(stats, form=None, is_home=False):
    """
    Calcule la note globale d'une équipe sur 100.

    La note est composée de :
    - Attaque
    - Défense
    - Forme récente
    - Avantage domicile

    Les pondérations sont définies dans config.py.
    """

    attack = compute_attack_score(stats)
    defense = compute_defense_score(stats)
    recent_form = compute_recent_form_score(form)
    home_bonus = compute_home_advantage_score(is_home)

    rating = (
        attack * ATTACK_WEIGHT
        + defense * DEFENSE_WEIGHT
        + recent_form * FORM_WEIGHT
        + home_bonus * HOME_WEIGHT
    )

    return {
        "attack": attack,
        "defense": defense,
        "form": recent_form,
        "home": home_bonus,
        "rating": round(rating, 1),
    }