import pandas as pd

def extract_teams(data):
    teams_df = pd.json_normalize(data["teams"], sep=".")
    if {"location","nickname"}.issubset(teams_df.columns):
        teams_df["name"] = teams_df["location"] + " " + teams_df["nickname"]
    elif "name" in teams_df.columns:
        teams_df["name"] = teams_df["name"]
    elif "abbrev" in teams_df.columns:
        teams_df["name"] = teams_df["abbrev"]
    else:
        raise ValueError("No team name field found")
    return teams_df[["id","name"]]

def extract_week_scores(data, season, week=1):
    rows = []
    for row in data.get("schedule", []):
        if row.get("matchupPeriodId") != week:
            continue
        for side in ["home","away"]:
            if side in row and row[side]:
                rows.append({
                    "season": season,
                    "teamId": row[side]["teamId"],
                    "points": row[side].get("totalPoints", 0),
                })
    return pd.DataFrame(rows)
