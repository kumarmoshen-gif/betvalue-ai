from providers.odds_api import get_odds

events = get_odds("soccer_epl")

for event in events[:5]:
    print("=" * 50)
    print(event["home_team"], "-", event["away_team"])

    for bookmaker in event["bookmakers"][:2]:
        print("Bookmaker :", bookmaker["title"])

        for market in bookmaker["markets"]:
            for outcome in market["outcomes"]:
                print(f'  {outcome["name"]} : {outcome["price"]}')