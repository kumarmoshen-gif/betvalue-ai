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