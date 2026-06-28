from providers.football_api import get_team_statistics

stats = get_team_statistics(
    team_id=33,
    league_id=39,
    season=2024
)

print(stats)