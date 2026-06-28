CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id INTEGER UNIQUE,
    name TEXT NOT NULL,
    country TEXT,
    logo TEXT,
    raw_data TEXT NOT NULL,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS team_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_api_id INTEGER,
    league_id INTEGER,
    season INTEGER,
    data TEXT NOT NULL,
    updated_at TEXT,
    UNIQUE(team_api_id, league_id, season)
);

CREATE TABLE IF NOT EXISTS team_form (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_api_id INTEGER,
    data TEXT NOT NULL,
    updated_at TEXT,
    UNIQUE(team_api_id)
);

-- =====================================================
-- Historique des prédictions
-- =====================================================

CREATE TABLE IF NOT EXISTS prediction_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    created_at TEXT NOT NULL,

    match TEXT NOT NULL,

    home_team TEXT NOT NULL,

    away_team TEXT NOT NULL,

    predicted_result TEXT,

    home_probability REAL,

    draw_probability REAL,

    away_probability REAL,

    confidence INTEGER,

    odd REAL,

    bookmaker_probability REAL,

    value REAL,

    decision TEXT,

    fallback INTEGER DEFAULT 0
);