import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import safe_figure_save

def plot_heatmap(normed, pivot, outpath):
    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(
        normed,
        annot=pivot.round(0),
        fmt="g",
        cmap="coolwarm",
        cbar_kws={"label": "Relative Points (within season)"}
    )
    ax.set_title("Week 1 Points by Season (2020–2025)\nColor scaled per season; Numbers = raw points", pad=15)
    ax.set_xlabel("Season")
    ax.set_ylabel("Owner")
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    #plt.savefig(outpath, dpi=200, bbox_inches="tight")
    safe_figure_save(plt, outpath, dpi=200, bbox_inches="tight")
    plt.close()


def plot_line_chart(df, splotlight_team, outpath, spotlight_label="Me"):
    plt.figure(figsize=(10,6))
    others_labeled = False
    for tid, sub in df.groupby("teamId"):
        if tid == splotlight_team:
            style = dict(color="red", alpha=1, linewidth=2.5, label=spotlight_label)
        else:
            if not others_labeled:
                style = dict(color="gray", alpha=0.3, linewidth=1, label="Everyone else")
                others_labeled = True
            else:
                style = dict(color="gray", alpha=0.3, linewidth=1)
        plt.plot(sub["season"], sub["points"], marker="o", **style)

    plt.title("Week 1 Scores by Year")
    plt.ylabel("Points")
    plt.legend()
    plt.tight_layout()
    #plt.savefig(outpath, dpi=200, bbox_inches="tight")
    safe_figure_save(plt, outpath, dpi=200, bbox_inches="tight")
    plt.close()


def plot_boxplot(df, splotlight_team, outpath, spotlight_label="Me", ):
    plt.figure(figsize=(10,6))
    sns.boxplot(x="season", y="points", data=df)
    sns.stripplot(
        x="season", y="points", data=df[df["teamId"]==splotlight_team],
        color="red", size=8, label=spotlight_label
    )
    plt.title("Week 1 Score Distribution (with me highlighted)")
    plt.legend()
    plt.tight_layout()
    #plt.savefig(outpath, dpi=200, bbox_inches="tight")
    safe_figure_save(plt, outpath, dpi=200, bbox_inches="tight")
    plt.close()
