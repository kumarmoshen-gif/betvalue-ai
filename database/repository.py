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
            bet_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.utcnow().isoformat(),
            prediction["match"],
            prediction["home_team"],
            prediction["away_team"],
            prediction["selected_bet"],
            prediction["home"],
            prediction["draw"],
            prediction["away"],
            prediction["confidence"],
            prediction["selected_odd"],

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
        ),
    )

    conn.commit()
    conn.close()