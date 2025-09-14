import requests
import logging
from datetime import datetime
from src.data import load_cache_entry, save_cache_entry

logger = logging.getLogger(__name__)
BASE_URL = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl"


def get_league_data(
    league_id: str,
    year: int,
    scoring_period: int = 1,
    views=None,
    cookies=None,
    headers=None,
    use_cache: bool = True,
    force_refresh: bool = False,
):
    """
    Fetch and cache raw ESPN league data for a given year/scoring period.

    Returns parsed JSON dict on success, None on failure.
    """
    views = views or ["mMatchup", "mTeam"]

    # --- Try cache first ---
    if use_cache and not force_refresh:
        cached = load_cache_entry(league_id, year, scoring_period, views)
        if cached is not None:
            return cached

    # --- Fetch from ESPN API ---
    url = f"{BASE_URL}/seasons/{year}/segments/0/leagues/{league_id}"
    data = None
    success = False

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
        success = True
    except requests.exceptions.RequestException as e:
        logger.warning(
            f"⚠️ Request failed (league={league_id}, year={year}, "
            f"period={scoring_period}, views={views}): {e}"
        )

    # --- Validate payload ---
    if success:
        has_core_keys = data and "teams" in data and "schedule" in data
        has_matchups = any(
            row.get("matchupPeriodId") == scoring_period
            for row in data.get("schedule", [])
        ) if has_core_keys else False

        if not (has_core_keys and has_matchups):
            logger.warning(
                f"⚠️ No valid matchups found (league={league_id}, "
                f"year={year}, period={scoring_period}, views={views})"
            )
            success = False

    # --- Caching decision ---
    current_year = datetime.now().year
    if success:
        save_cache_entry(league_id, year, scoring_period, views, data)
    else:
        if year < current_year:
            # Past year → cache None permanently (don’t retry)
            save_cache_entry(league_id, year, scoring_period, views, None)
        else:
            # Current year → skip caching so it will retry in future
            logger.info(
                f"Skipping cache for current-year miss "
                f"(league={league_id}, year={year}, "
                f"period={scoring_period}, views={views})"
            )

    return data if success else None
