import requests
import logging
from src.data import load_cache, save_cache

logger = logging.getLogger(__name__)

BASE_URL = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl"

def get_league_data(
    league_id,
    year,
    scoring_period=1,
    views=None,
    cookies=None,
    headers=None,
    use_cache=True
):
    cache = load_cache()
    views = views or ["mMatchup", "mTeam"]
    cache_key = (league_id, year, scoring_period, tuple(sorted(views)))

    # Return cached response if exists
    if use_cache and cache_key in cache:
        return cache[cache_key]

    url = f"{BASE_URL}/seasons/{year}/segments/0/leagues/{league_id}"
    data = None

    try:
        resp = requests.get(
            url,
            cookies=cookies,
            headers=headers,
            params={"scoringPeriodId": scoring_period, "view": views},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.HTTPError as e:
        logger.warning(
            f"⚠️ HTTP {resp.status_code} for league={league_id}, year={year}, "
            f"period={scoring_period}, views={views}: {e}"
        )
    except requests.exceptions.RequestException as e:
        logger.error(
            f"⚠️ Request failed for league={league_id}, year={year}, "
            f"period={scoring_period}, views={views}: {e}"
        )

    # Validate JSON payload
    if not data or "teams" not in data or "schedule" not in data:
        logger.warning(
            f"⚠️ No valid data retrieved for league={league_id}, year={year}, "
            f"period={scoring_period}, views={views}"
        )
        data = None

    # Always cache (even None, to avoid repeat failed calls)
    cache[cache_key] = data
    save_cache(cache)
    return data
