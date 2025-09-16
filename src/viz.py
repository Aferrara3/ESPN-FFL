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


def plot_fanboy_heatmap(fanboy_df, outpath):
    """
    Heatmap of starts by owner (rows) vs NFL teams (columns).
    fanboy_df: DataFrame indexed by owner, columns = NFL teams, values = counts (or %)
    """
    plt.figure(figsize=(14, 8))
    ax = sns.heatmap(
        fanboy_df,
        annot=False,
        cmap="Blues",
        cbar_kws={"label": "Starts"}
    )
    ax.set_title("Fanboy Index Heatmap (Starts by NFL Team)", pad=15)
    ax.set_xlabel("NFL Team")
    ax.set_ylabel("Fantasy Owner")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    safe_figure_save(plt, outpath, dpi=200, bbox_inches="tight")
    plt.close()


def plot_fanboy_stacked_bars(fanboy_df, outpath, top_n=5):
    """
    Stacked bar chart of top_n NFL teams per owner.
    fanboy_df: DataFrame indexed by owner, columns = NFL teams, values = counts
    """
    # keep only each owner’s top_n columns
    trimmed = fanboy_df.apply(lambda row: row[row > 0].nlargest(top_n), axis=1).fillna(0)

    # union of all owners’ top_n teams
    all_top_teams = sorted(set(trimmed.columns))

    # re-expand trimmed to have consistent columns across owners
    trimmed = trimmed.reindex(columns=all_top_teams, fill_value=0)

    # plot
    trimmed.plot(
        kind="bar",
        stacked=True,
        figsize=(12, 6),
        colormap="tab20"
    )
    plt.title(f"Fanboy Index: Top {top_n} NFL Teams per Owner")
    plt.ylabel("Total Starts")
    plt.xlabel("Fantasy Owner")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    safe_figure_save(plt, outpath, dpi=200, bbox_inches="tight")
    plt.close()


def plot_fanboy_pies(fanboy_df, outdir, top_n=5):
    """
    Pie chart grid of top_n NFL teams per owner.
    Saves one pie per owner into outdir.
    """
    for owner, row in fanboy_df.iterrows():
        top = row[row > 0].nlargest(top_n)
        fig, ax = plt.subplots(figsize=(4,4))
        ax.pie(top, labels=top.index, autopct="%1.0f%%", startangle=90, counterclock=False)
        ax.set_title(f"{owner} – Fanboy Index")
        safe_figure_save(plt, f"{outdir}/fanboy_{owner}.png", dpi=200, bbox_inches="tight")
        plt.close()


def plot_fanboy_leaguewide(fanboy_df, outpath, top_n=10):
    """
    Show which NFL teams have been started the most across the entire league.
    fanboy_df: DataFrame indexed by owner, columns = NFL teams, values = counts
    """
    totals = fanboy_df.sum(axis=0).sort_values(ascending=False).head(top_n)

    plt.figure(figsize=(10,6))
    sns.barplot(x=totals.values, y=totals.index, palette="viridis")
    plt.title(f"League-Wide Fanboy Trophy: Top {top_n} Most-Started NFL Teams")
    plt.xlabel("Total Starts Across All Owners")
    plt.ylabel("NFL Team")
    plt.tight_layout()
    safe_figure_save(plt, outpath, dpi=200, bbox_inches="tight")
    plt.close()

import plotly.graph_objects as go

def plot_fanboy_sankey(fanboy_df, outpath, top_n=5):
    """
    Sankey diagram: owners → their top_n NFL teams by starts.
    fanboy_df: DataFrame indexed by owner, columns = NFL teams, values = counts
    """
    owners = fanboy_df.index.tolist()
    links = []

    # Collect links: owner → top_n teams
    for owner, row in fanboy_df.iterrows():
        top_teams = row.sort_values(ascending=False).head(top_n)
        for team, val in top_teams.items():
            if val > 0:
                links.append((owner, team, int(val)))

    # Build node list
    nodes = list(fanboy_df.index) + list({team for _, team, _ in links})
    node_index = {name: i for i, name in enumerate(nodes)}

    # Build Sankey links
    source = [node_index[o] for o, t, v in links]
    target = [node_index[t] for o, t, v in links]
    value = [v for o, t, v in links]

    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=20,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodes,
            color=["#636EFA"]*len(owners) + ["#EF553B"]*(len(nodes)-len(owners))
        ),
        link=dict(source=source, target=target, value=value)
    )])

    fig.update_layout(title_text="Fanboy Flow: Owners → NFL Teams", font_size=12)

    # Save as static image (requires kaleido) or HTML fallback
    try:
        fig.write_image(outpath)
    except Exception:
        html_path = outpath.replace(".png", ".html")
        fig.write_html(html_path)
        print(f"⚠️ Could not save PNG, wrote interactive HTML instead: {html_path}")
