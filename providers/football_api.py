import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

stats_cache = {}
team_cache = {}
probability_cache = {}
last_matches_cache = {}


def get_team_statistics(team_id, league_id=39, season=2024):
    key = (team_id, league_id, season)

    if key in stats_cache:
        return stats_cache[key]

    url = f"{BASE_URL}/teams/statistics"

    params = {
        "league": league_id,
        "season": season,
        "team": team_id
    }

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 429:
        print("API LIMIT sur teams/statistics")
        return None

    response.raise_for_status()

    stats = response.json()["response"]
    stats_cache[key] = stats

    return stats


def search_team(team_name):
    if team_name in team_cache:
        return team_cache[team_name]

    url = f"{BASE_URL}/teams"

    params = {
        "search": team_name
    }

    response = requests.get(url, headers=HEADERS, params=params)

    print("=" * 60)
    print("Recherche équipe :", team_name)
    print("Status :", response.status_code)
    print("URL :", response.url)
    print("Réponse API :")
    print(response.text[:1000])
    print("=" * 60)

    if response.status_code == 429:
        print("API LIMIT ATTEINTE")
        return None

    response.raise_for_status()

    teams = response.json()["response"]

    if len(teams) == 0:
        print("Aucune équipe trouvée.")
        team_cache[team_name] = None
        return None

    print("Equipe trouvée :", teams[0]["team"]["name"])

    team_cache[team_name] = teams[0]
    return teams[0]


def get_team_id(team_name):
    team = search_team(team_name)

    if team is None:
        return None

    return team["team"]["id"]


def get_match_probability(home_team, away_team, league_id=39, season=2024):
    key = (home_team, away_team, league_id, season)

    if key in probability_cache:
        return probability_cache[key]

    home_id = get_team_id(home_team)
    away_id = get_team_id(away_team)

    if home_id is None or away_id is None:
        return None

    home_stats = get_team_statistics(home_id, league_id, season)
    away_stats = get_team_statistics(away_id, league_id, season)

    if home_stats is None or away_stats is None:
        return None

    from core.stats_model import estimate_probability

    probability = estimate_probability(home_stats, away_stats)
    probability = max(5, min(95, probability))

    probability_cache[key] = probability

    return probability


def get_last_matches(team_id, league_id=None, season=None, last=5):
    key = (team_id, league_id, season, last)

    if key in last_matches_cache:
        return last_matches_cache[key]

    url = f"{BASE_URL}/fixtures"

    params = {
        "team": team_id,
        "last": last
    }

    if league_id is not None:
        params["league"] = league_id

    if season is not None:
        params["season"] = season

    response = requests.get(url, headers=HEADERS, params=params)

    print("=" * 60)
    print("Récupération des derniers matchs")
    print("Team ID :", team_id)
    print("Status :", response.status_code)
    print("URL :", response.url)
    print("Réponse API :")
    print(response.text[:1000])
    print("=" * 60)

    if response.status_code == 429:
        print("API LIMIT sur fixtures")
        return []

    response.raise_for_status()

    matches = response.json()["response"]

    print("Nombre de matchs récupérés :", len(matches))

    last_matches_cache[key] = matches

    return matches