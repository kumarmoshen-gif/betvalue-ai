def compute_confidence_score(diff):
    """
    Calcule un score de confiance IA sur 100
    à partir de l'écart de rating entre les deux équipes.
    """

    diff = abs(diff)

    if diff >= 30:
        return 90

    if diff >= 20:
        return 80

    if diff >= 10:
        return 70

    if diff >= 5:
        return 60

    return 50