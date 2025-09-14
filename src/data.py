import pickle
from pathlib import Path

CACHE_PATH = Path("cache.pkl")

def load_cache():
    if CACHE_PATH.exists():
        with open(CACHE_PATH, "rb") as f:
            return pickle.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_PATH, "wb") as f:
        pickle.dump(cache, f)
