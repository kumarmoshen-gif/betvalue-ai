CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id INTEGER UNIQUE,
    name TEXT,
    country TEXT,
    logo TEXT,
    raw_data TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS team_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_api_id INTEGER,
    league_id INTEGER,
    season INTEGER,
    data TEXT,
    updated_at TEXT,
    UNIQUE(team_api_id, league_id, season)
);

CREATE TABLE IF NOT EXISTS team_form (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_api_id INTEGER,
    league_id INTEGER,
    season INTEGER,
    data TEXT,
    updated_at TEXT,
    UNIQUE(team_api_id, league_id, season)
);

CREATE TABLE IF NOT EXISTS fixtures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id INTEGER UNIQUE,
    league_id INTEGER,
    season INTEGER,
    match_date TEXT,
    status TEXT,
    home_team TEXT,
    away_team TEXT,
    home_team_api_id INTEGER,
    away_team_api_id INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    raw_data TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS prediction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    created_at TEXT,

    match TEXT,

    home_team TEXT,

    away_team TEXT,

    predicted_result TEXT,

    home_probability REAL,

    draw_probability REAL,

    away_probability REAL,

    confidence INTEGER,

    odd REAL,

    bookmaker_probability REAL,

    value REAL,

    decision TEXT,

    fallback INTEGER,

    stake REAL DEFAULT 1,

    result TEXT,

    bet_won INTEGER,

    profit REAL DEFAULT 0,

    league TEXT,

    season INTEGER,

    match_date TEXT,

    home_score INTEGER,

    away_score INTEGER,

    bookmaker TEXT,

    bet_type TEXT,

    fixture_api_id INTEGER,

    settled_at TEXT
);
