import pandas as pd

def add_ranks(df):
    df["rank"] = df.groupby("season")["points"].rank(
        ascending=False, method="min"
    )
    return df

def filter_recent(df, min_year=2020):
    return df[df["season"] >= min_year].copy()

def build_owner_lookup(data):
    teams_current = pd.json_normalize(data["teams"])[["id","primaryOwner"]]\
                      .rename(columns={"id":"teamId"})
    members_current = pd.json_normalize(data["members"])[["id","lastName"]]\
                      .rename(columns={"id":"primaryOwner"})
    return (
        teams_current.merge(members_current, on="primaryOwner", how="left")
                     .set_index("teamId")["lastName"]
                     .to_dict()
    )

def pivot_scores(df, owner_lookup):
    pivot = df.pivot(index="teamId", columns="season", values="points")
    pivot.index = [owner_lookup.get(tid, str(tid)) for tid in pivot.index]
    row_order = pivot.mean(axis=1).sort_values(ascending=False).index
    return pivot.loc[row_order]

def normalize_per_column(pivot):
    normed = pivot.copy()
    for col in normed.columns:
        col_vals = normed[col]
        if col_vals.notna().any():
            cmin, cmax = col_vals.min(), col_vals.max()
            normed[col] = (
                (col_vals - cmin) / (cmax - cmin)
                if cmax > cmin else 0.5
            )
    return normed
