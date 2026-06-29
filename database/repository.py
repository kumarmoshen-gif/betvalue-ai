import json
from datetime import datetime

from core.result_settlement import (
    compute_profit,
    is_bet_won,
    result_from_score,
)
from database.database import get_connection


def _rows_to_dicts(rows):
    return [dict(row) for row in rows]


def _utc_now():
    return datetime.utcnow().isoformat()


def _exclude_fallback_clause(include_fallback):
    return "" if include_fallback else " AND COALESCE(fallback, 0) = 0"


def save_team(team):
    team_data = team.get("team", {})

    conn = get_connection()
    conn.execute(
        """
        INSERT INTO teams (
            api_id,
            name,
            country,
            logo,
            raw_data,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(api_id) DO UPDATE SET
            name = excluded.name,
            country = excluded.country,
            logo = excluded.logo,
            raw_data = excluded.raw_data,
            updated_at = excluded.updated_at
        """,
        (
            team_data.get("id"),
            team_data.get("name"),
            team_data.get("country"),
            team_data.get("logo"),
            json.dumps(team),
            _utc_now(),
        ),
    )
    conn.commit()
    conn.close()


def load_team_by_name(team_name):
    conn = get_connection()
    row = conn.execute(
        """
        SELECT raw_data
        FROM teams
        WHERE lower(name) = lower(?)
        LIMIT 1
        """,
        (team_name,),
    ).fetchone()
    conn.close()

    if row is None:
        return None

    return json.loads(row["raw_data"])


def save_team_statistics(team_api_id, league_id, season, stats):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO team_statistics (
            team_api_id,
            league_id,
            season,
            data,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(team_api_id, league_id, season) DO UPDATE SET
            data = excluded.data,
            updated_at = excluded.updated_at
        """,
        (
            team_api_id,
            league_id,
            season,
            json.dumps(stats),
            _utc_now(),
        ),
    )
    conn.commit()
    conn.close()


def load_team_statistics(team_api_id, league_id, season):
    conn = get_connection()
    row = conn.execute(
        """
        SELECT data
        FROM team_statistics
        WHERE team_api_id = ?
          AND league_id = ?
          AND season = ?
        LIMIT 1
        """,
        (team_api_id, league_id, season),
    ).fetchone()
    conn.close()

    if row is None:
        return None

    return json.loads(row["data"])


def save_team_form(team_api_id, league_id, season, form):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO team_form (
            team_api_id,
            league_id,
            season,
            data,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(team_api_id, league_id, season) DO UPDATE SET
            data = excluded.data,
            updated_at = excluded.updated_at
        """,
        (
            team_api_id,
            league_id,
            season,
            json.dumps(form),
            _utc_now(),
        ),
    )
    conn.commit()
    conn.close()


def load_team_form(team_api_id, league_id, season):
    conn = get_connection()
    row = conn.execute(
        """
        SELECT data
        FROM team_form
        WHERE team_api_id = ?
          AND league_id = ?
          AND season = ?
        LIMIT 1
        """,
        (team_api_id, league_id, season),
    ).fetchone()
    conn.close()

    if row is None:
        return None

    return json.loads(row["data"])


def _extract_fixture_row(fixture):
    fixture_info = fixture.get("fixture", {})
    league_info = fixture.get("league", {})
    teams = fixture.get("teams", {})
    goals = fixture.get("goals", {})

    home_team = teams.get("home", {})
    away_team = teams.get("away", {})
    status = fixture_info.get("status", {})

    return {
        "api_id": fixture_info.get("id"),
        "league_id": league_info.get("id"),
        "season": league_info.get("season"),
        "match_date": fixture_info.get("date"),
        "status": status.get("short"),
        "home_team": home_team.get("name"),
        "away_team": away_team.get("name"),
        "home_team_api_id": home_team.get("id"),
        "away_team_api_id": away_team.get("id"),
        "home_score": goals.get("home"),
        "away_score": goals.get("away"),
        "raw_data": json.dumps(fixture),
        "updated_at": _utc_now(),
    }


def save_fixture(fixture):
    row = _extract_fixture_row(fixture)

    conn = get_connection()
    conn.execute(
        """
        INSERT INTO fixtures (
            api_id,
            league_id,
            season,
            match_date,
            status,
            home_team,
            away_team,
            home_team_api_id,
            away_team_api_id,
            home_score,
            away_score,
            raw_data,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(api_id) DO UPDATE SET
            league_id = excluded.league_id,
            season = excluded.season,
            match_date = excluded.match_date,
            status = excluded.status,
            home_team = excluded.home_team,
            away_team = excluded.away_team,
            home_team_api_id = excluded.home_team_api_id,
            away_team_api_id = excluded.away_team_api_id,
            home_score = excluded.home_score,
            away_score = excluded.away_score,
            raw_data = excluded.raw_data,
            updated_at = excluded.updated_at
        """,
        (
            row["api_id"],
            row["league_id"],
            row["season"],
            row["match_date"],
            row["status"],
            row["home_team"],
            row["away_team"],
            row["home_team_api_id"],
            row["away_team_api_id"],
            row["home_score"],
            row["away_score"],
            row["raw_data"],
            row["updated_at"],
        ),
    )
    conn.commit()
    conn.close()


def save_fixtures(fixtures):
    for fixture in fixtures:
        save_fixture(fixture)


def load_fixtures(league_id=None, season=None, status=None, limit=500):
    clauses = []
    params = []

    if league_id is not None:
        clauses.append("league_id = ?")
        params.append(league_id)

    if season is not None:
        clauses.append("season = ?")
        params.append(season)

    if status is not None:
        clauses.append("status = ?")
        params.append(status)

    where_clause = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    params.append(limit)

    conn = get_connection()
    rows = conn.execute(
        f"""
        SELECT *
        FROM fixtures
        {where_clause}
        ORDER BY match_date DESC
        LIMIT ?
        """,
        params,
    ).fetchall()
    conn.close()

    return _rows_to_dicts(rows)


def find_finished_fixture_for_prediction(prediction):
    statuses = ("FT", "AET", "PEN")
    params = [
        prediction["home_team"],
        prediction["away_team"],
        *statuses,
    ]

    clauses = [
        "home_team = ?",
        "away_team = ?",
        f"status IN ({', '.join('?' for _ in statuses)})",
        "home_score IS NOT NULL",
        "away_score IS NOT NULL",
    ]

    if prediction.get("season") is not None:
        clauses.append("season = ?")
        params.append(prediction["season"])

    where_clause = " AND ".join(clauses)

    conn = get_connection()
    row = conn.execute(
        f"""
        SELECT *
        FROM fixtures
        WHERE {where_clause}
        ORDER BY match_date DESC
        LIMIT 1
        """,
        params,
    ).fetchone()
    conn.close()

    if row is None:
        return None

    return dict(row)


def save_prediction(prediction):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO prediction_history (
            created_at,
            match,
            home_team,
            away_team,
            predicted_result,
            home_probability,
            draw_probability,
            away_probability,
            confidence,
            odd,
            bookmaker_probability,
            value,
            decision,
            fallback,
            stake,
            result,
            bet_won,
            profit,
            league,
            season,
            match_date,
            home_score,
            away_score,
            bookmaker,
            bet_type,
            fixture_api_id,
            settled_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            prediction.get("created_at", _utc_now()),
            prediction["match"],
            prediction["home_team"],
            prediction["away_team"],
            prediction.get("selected_bet") or prediction.get("predicted_result"),
            prediction["home"],
            prediction["draw"],
            prediction["away"],
            prediction["confidence"],
            prediction.get("selected_odd") or prediction.get("odd"),
            prediction["value_bet"]["bookmaker_probability"]
            if prediction.get("value_bet")
            else None,
            prediction["value_bet"]["value"]
            if prediction.get("value_bet")
            else None,
            prediction["value_bet"]["decision"]
            if prediction.get("value_bet")
            else None,
            int(prediction.get("fallback", False)),
            prediction.get("stake", 1),
            prediction.get("result"),
            prediction.get("bet_won"),
            prediction.get("profit", 0),
            prediction.get("league"),
            prediction.get("season"),
            prediction.get("match_date"),
            prediction.get("home_score"),
            prediction.get("away_score"),
            prediction.get("bookmaker"),
            prediction.get("bet_type"),
            prediction.get("fixture_api_id"),
            prediction.get("settled_at"),
        ),
    )

    conn.commit()
    conn.close()


def load_prediction_history(limit=1000):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT *
        FROM prediction_history
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()

    return _rows_to_dicts(rows)


def load_pending_predictions():
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT *
        FROM prediction_history
        WHERE result IS NULL
        ORDER BY created_at DESC, id DESC
        """
    ).fetchall()
    conn.close()

    return _rows_to_dicts(rows)


def load_completed_predictions(limit=5000, include_fallback=True):
    conn = get_connection()
    rows = conn.execute(
        f"""
        SELECT *
        FROM prediction_history
        WHERE result IS NOT NULL
        {_exclude_fallback_clause(include_fallback)}
        ORDER BY created_at ASC, id ASC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()

    return _rows_to_dicts(rows)


def update_prediction_result(prediction_id, result, stake):
    conn = get_connection()
    prediction = conn.execute(
        """
        SELECT predicted_result, odd
        FROM prediction_history
        WHERE id = ?
        """,
        (prediction_id,),
    ).fetchone()

    if prediction is None:
        conn.close()
        raise ValueError(f"Prediction introuvable: {prediction_id}")

    bet_won = is_bet_won(prediction["predicted_result"], result)
    profit = compute_profit(bet_won, prediction["odd"], stake)

    conn.execute(
        """
        UPDATE prediction_history
        SET result = ?,
            stake = ?,
            bet_won = ?,
            profit = ?,
            settled_at = ?
        WHERE id = ?
        """,
        (
            result,
            stake,
            int(bet_won),
            profit,
            _utc_now(),
            prediction_id,
        ),
    )
    conn.commit()
    conn.close()

    return {
        "bet_won": bet_won,
        "profit": profit,
    }


def update_prediction_score_result(
    prediction_id,
    home_score,
    away_score,
    stake,
):
    conn = get_connection()
    prediction = conn.execute(
        """
        SELECT
            home_team,
            away_team,
            predicted_result,
            odd
        FROM prediction_history
        WHERE id = ?
        """,
        (prediction_id,),
    ).fetchone()

    if prediction is None:
        conn.close()
        raise ValueError(f"Prediction introuvable: {prediction_id}")

    result = result_from_score(
        prediction["home_team"],
        prediction["away_team"],
        home_score,
        away_score,
    )
    bet_won = is_bet_won(prediction["predicted_result"], result)
    profit = compute_profit(bet_won, prediction["odd"], stake)

    conn.execute(
        """
        UPDATE prediction_history
        SET result = ?,
            stake = ?,
            bet_won = ?,
            profit = ?,
            home_score = ?,
            away_score = ?,
            settled_at = ?
        WHERE id = ?
        """,
        (
            result,
            stake,
            int(bet_won),
            profit,
            home_score,
            away_score,
            _utc_now(),
            prediction_id,
        ),
    )
    conn.commit()
    conn.close()

    return {
        "result": result,
        "bet_won": bet_won,
        "profit": profit,
    }


def update_prediction_from_fixture(prediction_id, fixture, stake=None):
    conn = get_connection()
    prediction = conn.execute(
        """
        SELECT
            stake,
            home_team,
            away_team,
            predicted_result,
            odd
        FROM prediction_history
        WHERE id = ?
        """,
        (prediction_id,),
    ).fetchone()

    if prediction is None:
        conn.close()
        raise ValueError(f"Prediction introuvable: {prediction_id}")

    home_score = fixture["home_score"]
    away_score = fixture["away_score"]
    fixture_api_id = fixture.get("api_id")
    resolved_stake = stake if stake is not None else prediction["stake"]

    result = result_from_score(
        prediction["home_team"],
        prediction["away_team"],
        home_score,
        away_score,
    )
    bet_won = is_bet_won(prediction["predicted_result"], result)
    profit = compute_profit(bet_won, prediction["odd"], resolved_stake)

    conn.execute(
        """
        UPDATE prediction_history
        SET result = ?,
            stake = ?,
            bet_won = ?,
            profit = ?,
            home_score = ?,
            away_score = ?,
            fixture_api_id = ?,
            settled_at = ?
        WHERE id = ?
        """,
        (
            result,
            resolved_stake,
            int(bet_won),
            profit,
            home_score,
            away_score,
            fixture_api_id,
            _utc_now(),
            prediction_id,
        ),
    )
    conn.commit()
    conn.close()

    return {
        "result": result,
        "bet_won": bet_won,
        "profit": profit,
        "fixture_id": fixture_api_id,
    }


def load_performance_stats(include_fallback=False):
    conn = get_connection()
    row = conn.execute(
        f"""
        SELECT
            COUNT(*) AS total_bets,
            COALESCE(SUM(stake), 0) AS total_stake,
            COALESCE(SUM(profit), 0) AS total_profit,
            COALESCE(SUM(CASE WHEN bet_won = 1 THEN 1 ELSE 0 END), 0) AS won_bets,
            COALESCE(SUM(CASE WHEN bet_won = 0 THEN 1 ELSE 0 END), 0) AS lost_bets
        FROM prediction_history
        WHERE result IS NOT NULL
        {_exclude_fallback_clause(include_fallback)}
        """
    ).fetchone()
    conn.close()

    total_bets = row["total_bets"]
    total_stake = row["total_stake"]
    total_profit = row["total_profit"]

    return {
        "total_bets": total_bets,
        "total_stake": round(total_stake, 2),
        "total_profit": round(total_profit, 2),
        "won_bets": row["won_bets"],
        "lost_bets": row["lost_bets"],
        "hit_rate": round((row["won_bets"] / total_bets) * 100, 2)
        if total_bets
        else 0,
        "roi": round((total_profit / total_stake) * 100, 2)
        if total_stake
        else 0,
    }


def load_bankroll_history(initial_bankroll=0, include_fallback=False):
    conn = get_connection()
    rows = conn.execute(
        f"""
        SELECT created_at, profit
        FROM prediction_history
        WHERE result IS NOT NULL
        {_exclude_fallback_clause(include_fallback)}
        ORDER BY created_at ASC, id ASC
        """
    ).fetchall()
    conn.close()

    bankroll = initial_bankroll
    history = []

    for row in rows:
        bankroll += row["profit"]
        history.append({
            "created_at": row["created_at"],
            "bankroll": round(bankroll, 2),
        })

    return history


def load_profit_history(include_fallback=False):
    conn = get_connection()
    rows = conn.execute(
        f"""
        SELECT created_at, profit
        FROM prediction_history
        WHERE result IS NOT NULL
        {_exclude_fallback_clause(include_fallback)}
        ORDER BY created_at ASC, id ASC
        """
    ).fetchall()
    conn.close()

    cumulative_profit = 0
    history = []

    for row in rows:
        cumulative_profit += row["profit"]
        history.append({
            "created_at": row["created_at"],
            "cumulative_profit": round(cumulative_profit, 2),
        })

    return history


def load_roi_history(include_fallback=False):
    conn = get_connection()
    rows = conn.execute(
        f"""
        SELECT created_at, stake, profit
        FROM prediction_history
        WHERE result IS NOT NULL
        {_exclude_fallback_clause(include_fallback)}
        ORDER BY created_at ASC, id ASC
        """
    ).fetchall()
    conn.close()

    total_stake = 0
    total_profit = 0
    history = []

    for row in rows:
        total_stake += row["stake"]
        total_profit += row["profit"]
        roi = (total_profit / total_stake) * 100 if total_stake else 0
        history.append({
            "created_at": row["created_at"],
            "roi": round(roi, 2),
        })

    return history


def load_streak_stats(include_fallback=False):
    conn = get_connection()
    rows = conn.execute(
        f"""
        SELECT bet_won
        FROM prediction_history
        WHERE result IS NOT NULL
        {_exclude_fallback_clause(include_fallback)}
        ORDER BY created_at ASC, id ASC
        """
    ).fetchall()
    conn.close()

    current = 0
    current_type = "-"
    best_win = 0
    best_loss = 0
    win_streak = 0
    loss_streak = 0

    for row in rows:
        if row["bet_won"]:
            win_streak += 1
            loss_streak = 0
            current = win_streak
            current_type = "victoires"
            best_win = max(best_win, win_streak)
        else:
            loss_streak += 1
            win_streak = 0
            current = loss_streak
            current_type = "defaites"
            best_loss = max(best_loss, loss_streak)

    return {
        "current": current,
        "current_type": current_type,
        "best_win": best_win,
        "best_loss": best_loss,
    }


def load_monthly_profit(include_fallback=False):
    conn = get_connection()
    rows = conn.execute(
        f"""
        SELECT
            substr(created_at, 1, 7) AS month,
            ROUND(SUM(profit), 2) AS profit
        FROM prediction_history
        WHERE result IS NOT NULL
        {_exclude_fallback_clause(include_fallback)}
        GROUP BY substr(created_at, 1, 7)
        ORDER BY month
        """
    ).fetchall()
    conn.close()

    return _rows_to_dicts(rows)


def load_roi_by_confidence(include_fallback=False):
    conn = get_connection()
    rows = conn.execute(
        f"""
        SELECT
            CASE
                WHEN confidence >= 85 THEN '85+'
                WHEN confidence >= 70 THEN '70-84'
                WHEN confidence >= 60 THEN '60-69'
                ELSE '<60'
            END AS confidence,
            ROUND((SUM(profit) / SUM(stake)) * 100, 2) AS roi,
            COUNT(*) AS bets
        FROM prediction_history
        WHERE result IS NOT NULL
          AND stake > 0
        {_exclude_fallback_clause(include_fallback)}
        GROUP BY
            CASE
                WHEN confidence >= 85 THEN '85+'
                WHEN confidence >= 70 THEN '70-84'
                WHEN confidence >= 60 THEN '60-69'
                ELSE '<60'
            END
        ORDER BY MIN(confidence)
        """
    ).fetchall()
    conn.close()

    return _rows_to_dicts(rows)


def load_roi_by_odds(include_fallback=False):
    conn = get_connection()
    rows = conn.execute(
        f"""
        SELECT
            CASE
                WHEN odd < 1.50 THEN '<1.50'
                WHEN odd < 2.00 THEN '1.50-1.99'
                WHEN odd < 3.00 THEN '2.00-2.99'
                WHEN odd < 5.00 THEN '3.00-4.99'
                ELSE '5.00+'
            END AS odd_range,
            ROUND((SUM(profit) / SUM(stake)) * 100, 2) AS roi,
            COUNT(*) AS bets
        FROM prediction_history
        WHERE result IS NOT NULL
          AND stake > 0
          AND odd IS NOT NULL
        {_exclude_fallback_clause(include_fallback)}
        GROUP BY
            CASE
                WHEN odd < 1.50 THEN '<1.50'
                WHEN odd < 2.00 THEN '1.50-1.99'
                WHEN odd < 3.00 THEN '2.00-2.99'
                WHEN odd < 5.00 THEN '3.00-4.99'
                ELSE '5.00+'
            END
        ORDER BY MIN(odd)
        """
    ).fetchall()
    conn.close()

    return _rows_to_dicts(rows)


def load_drawdown_history(include_fallback=False):
    bankroll_history = load_bankroll_history(
        include_fallback=include_fallback,
    )
    peak = 0
    history = []

    for row in bankroll_history:
        bankroll = row["bankroll"]
        peak = max(peak, bankroll)
        drawdown = bankroll - peak
        history.append({
            "created_at": row["created_at"],
            "drawdown": round(drawdown, 2),
        })

    return history
