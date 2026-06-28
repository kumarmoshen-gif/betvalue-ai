from providers.football_api import get_match_probability

prob = get_match_probability(
    "Manchester United",
    "Liverpool"
)

print(prob)
