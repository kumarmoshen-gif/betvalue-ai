from core.attack_score import compute_attack_score
from core.defense_score import compute_defense_score
from core.recent_form_score import compute_recent_form_score


def compute_team_rating(stats, form=None):
    """
    Calcule une note globale sur 100.

    Pondération actuelle :
    - Attaque : 40 %
    - Défense : 35 %
    - Forme récente : 25 %
    """

    attack = compute_attack_score(stats)
    defense = compute_defense_score(stats)
    recent_form = compute_recent_form_score(form)

    rating = (
        attack * 0.40
        + defense * 0.35
        + recent_form * 0.25
    )

    return {
        "attack": attack,
        "defense": defense,
        "form": recent_form,
        "rating": round(rating, 1),
    }