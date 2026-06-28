def compute_home_advantage_score(is_home=True):
    """
    Score simple d'avantage du terrain.
    Domicile : bonus positif
    Extérieur : neutre
    """

    if is_home:
        return 65

    return 50