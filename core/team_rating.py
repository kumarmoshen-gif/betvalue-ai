from core.attack_score import compute_attack_score
from core.defense_score import compute_defense_score
from core.recent_form_score import compute_recent_form_score
from core.home_advantage import compute_home_advantage_score


def compute_team_rating(stats, form=None, is_home=False):
    """
    Calcule une note globale sur 100.

    Pondération actuelle :
    - Attaque : 35 %
    - Défense : 30 %
    - Forme : 25 %
    - Avantage domicile : 10 %
    """

    attack = compute_attack_score(stats)
    defense = compute_defense_score(stats)
    recent_form = compute_recent_form_score(form)
    home_bonus = compute_home_advantage_score(is_home)

    rating = (
        attack * 0.35
        + defense * 0.30
        + recent_form * 0.25
        + home_bonus * 0.10
    )

    return {
        "attack": attack,
        "defense": defense,
        "form": recent_form,
        "home": home_bonus,
        "rating": round(rating, 1),
    }