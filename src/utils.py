from pathlib import Path
import matplotlib.pyplot as plt

def ensure_parent_dir(path):
    """
    Ensure the parent directory for `path` exists.
    Returns a Path object.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def safe_figure_save(fig_or_plt, outpath, **kwargs):
    """
    Save a matplotlib figure safely by ensuring the parent folder exists.

    Parameters
    ----------
    fig_or_plt : matplotlib.figure.Figure or matplotlib.pyplot
        The figure object or pyplot module.
    outpath : str or Path
        Path to save the figure.
    **kwargs :
        Extra keyword arguments passed to savefig.
    """
    outpath = ensure_parent_dir(outpath)
    if hasattr(fig_or_plt, "savefig"):   # figure object
        fig_or_plt.savefig(outpath, **kwargs)
    else:                                # pyplot module
        plt.savefig(outpath, **kwargs)
    plt.close()

import pandas as pd
from src.data import load_cache_entry

def cache_summary(years, max_period=20, league_id=None, views=("mMatchup","mTeam")):
    from src.data import cache_path
    import pandas as pd

    rows = []
    for year in years:
        row = {}
        for period in range(1, max_period+1):
            path = cache_path(league_id, year, period, views)
            if not path.exists():
                row[period] = "⬜"
            else:
                val = load_cache_entry(league_id, year, period, views)
                row[period] = "✅" if val else "✗"
        rows.append(pd.Series(row, name=year))
    return pd.DataFrame(rows)
