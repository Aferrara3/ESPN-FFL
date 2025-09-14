import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def _parse_years(raw: str, default_year: int):
    """
    Convert comma-separated string from .env into a list of ints.
    Falls back to [default_year] if not set.
    """
    if not raw:
        return [default_year]
    return [int(y.strip()) for y in raw.split(",") if y.strip().isdigit()]

class Config:
    # Core settings from .env
    league_id = os.getenv("LEAGUE_ID")
    year = int(os.getenv("YEAR", "2025"))
    years = _parse_years(os.getenv("YEARS"), year)

    # Secrets
    cookies = {
        "swid": os.getenv("SWID"),
        "espn_s2": os.getenv("ESPN_S2"),
    }

    # Public/static headers
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "X-Fantasy-Source": "kona",
        "X-Fantasy-Platform": "kona-PROD-ffl",
    }

config = Config()
