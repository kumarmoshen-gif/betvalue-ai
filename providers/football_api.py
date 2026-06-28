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
    from database.repository import load_team_statistics, save_team_statistics

    cached_stats = load_team_statistics(team_id, league_id, season)

    if cached_stats is not None:
        return cached_stats

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
        return None

    response.raise_for_status()

    result = response.json()

    if result.get("errors"):
        return None

    stats = result["response"]

    stats_cache[key] = stats
    save_team_statistics(team_id, league_id, season, stats)

    return stats


def search_team(team_name):
    from database.repository import load_team_by_name, save_team

    if team_name in team_cache:
        return team_cache[team_name]

    cached_team = load_team_by_name(team_name)

    if cached_team is not None:
        team_cache[team_name] = cached_team
        return cached_team

    url = f"{BASE_URL}/teams"

    params = {
        "search": team_name
    }

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 429:
        return None

    response.raise_for_status()

    result = response.json()

    if result.get("errors"):
        return None

    teams = result["response"]

    if len(teams) == 0:
        team_cache[team_name] = None
        return None

    team = teams[0]

    save_team(team)

    team_cache[team_name] = team

    return team


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

    if response.status_code == 429:
        return []

    response.raise_for_status()

    result = response.json()

    if result.get("errors"):
        return []

    matches = result["response"]

    last_matches_cache[key] = matches

    return matches