"""
=========================================================
BetValue AI - Configuration Globale
=========================================================

Toutes les constantes du projet sont centralisées ici.

Ne pas utiliser de valeurs "magiques" dans le code.
Modifier uniquement ce fichier.
"""

# =========================================================
# Application
# =========================================================

APP_NAME = "BetValue AI"
APP_VERSION = "4.0-dev"

# =========================================================
# API Football
# =========================================================

DEFAULT_LEAGUE = 39          # Premier League
DEFAULT_SEASON = 2024
DEFAULT_LAST_MATCHES = 5

# =========================================================
# Team Rating
# =========================================================

ATTACK_WEIGHT = 0.35
DEFENSE_WEIGHT = 0.30
FORM_WEIGHT = 0.25
HOME_WEIGHT = 0.10

# =========================================================
# Home Advantage
# =========================================================

HOME_ADVANTAGE_SCORE = 65
AWAY_ADVANTAGE_SCORE = 50

# =========================================================
# Confidence Engine
# =========================================================

CONFIDENCE_HIGH = 85
CONFIDENCE_MEDIUM = 70
CONFIDENCE_LOW = 60

# =========================================================
# Value Bet
# =========================================================

DEFAULT_ODD = 2.10

# Une Value Bet est considérée intéressante
# lorsque l'écart est supérieur à ce seuil.
VALUE_THRESHOLD = 5.0

# =========================================================
# Match Predictor
# =========================================================

MAX_PROBABILITY = 95
MIN_PROBABILITY = 5

# =========================================================
# Cache
# =========================================================

ENABLE_MEMORY_CACHE = True
ENABLE_SQLITE_CACHE = True

# =========================================================
# SQLite
# =========================================================

DATABASE_NAME = "betvalue.db"

# =========================================================
# Logging
# =========================================================

LOG_LEVEL = "INFO"
LOG_FILE = "logs/betvalue.log"

# =========================================================
# Interface Streamlit
# =========================================================

DEFAULT_PAGE_TITLE = "BetValue AI"
DEFAULT_PAGE_ICON = "⚽"

# =========================================================
# Démonstration (Fallback)
# =========================================================

FALLBACK_HOME_PROBABILITY = 58
FALLBACK_DRAW_PROBABILITY = 20
FALLBACK_AWAY_PROBABILITY = 22

FALLBACK_CONFIDENCE = 80

FALLBACK_HOME_RATING = 69.5
FALLBACK_AWAY_RATING = 48.7

# Les predictions fallback servent a garder l'interface utilisable
# quand les APIs sont indisponibles. Elles ne doivent pas polluer
# l'historique ni les performances par defaut.
SAVE_FALLBACK_PREDICTIONS = False

# =========================================================
# Historique (V4)
# =========================================================

MAX_HISTORY_ROWS = 1000

# =========================================================
# Dashboard (V4)
# =========================================================

TOP_VALUE_BETS = 10

# =========================================================
# Machine Learning (V5)
# =========================================================

MIN_MATCHES_FOR_TRAINING = 1000
RANDOM_STATE = 42
TEST_SIZE = 0.20
