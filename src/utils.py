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
