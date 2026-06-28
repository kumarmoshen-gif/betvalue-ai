from providers.odds_api import get_odds


def get_league_odds(sport_key: str, limit: int = 15):
    events = get_odds(sport_key)

    data = []

    for event in events[:limit]:
        for bookmaker in event["bookmakers"][:1]:
            for market in bookmaker["markets"]:
                for outcome in market["outcomes"]:
                    data.append({
                        "Sport": "Football",
                        "Match": f'{event["home_team"]} - {event["away_team"]}',
                        "Bookmaker": bookmaker["title"],
                        "Pari": outcome["name"],
                        "Cote": outcome["price"],
                    })

    return data