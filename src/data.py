import pickle
from pathlib import Path

CACHE_DIR = Path("cache")

def cache_path(league_id, year, scoring_period, views):
    """Return path for given cache key."""
    safe_views = "_".join(views)
    return (
        CACHE_DIR / str(league_id) / str(year) /
        f"period_{scoring_period:02d}_{safe_views}.pkl"
    )

def load_cache_entry(league_id, year, scoring_period, views):
    path = cache_path(league_id, year, scoring_period, views)
    if path.exists():
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            print(f"⚠️ Corrupt cache file: {path}, deleting")
            path.unlink(missing_ok=True)
    return None

def save_cache_entry(league_id, year, scoring_period, views, data):
    path = cache_path(league_id, year, scoring_period, views)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "wb") as f:
        pickle.dump(data, f)
    tmp.replace(path)
