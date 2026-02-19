import altair as alt
import pandas as pd
from components.viz_theme import PALETTE

def _wr_band(s: pd.Series, bad=7.0, warn=7.5) -> pd.Series:
    s = pd.to_numeric(s, errors="coerce")
    return pd.cut(
        s,
        bins=[-1e18, bad, warn, 1e18],
        labels=["Baixo", "Médio", "Alto"],
        include_lowest=True,
    )

def _roi_band(s: pd.Series, bad=0.0, warn=0.2) -> pd.Series:
    s = pd.to_numeric(s, errors="coerce")
    return pd.cut(
        s,
        bins=[-1e18, bad, warn, 1e18],
        labels=["Negativo", "Baixo", "Bom"],
        include_lowest=True,
    )

WR_SCALE = alt.Scale(
    domain=["Baixo", "Médio", "Alto"],
    range=[PALETTE["bad"], PALETTE["warn"], PALETTE["ok"]],
)

ROI_SCALE = alt.Scale(
    domain=["Negativo", "Baixo", "Bom"],
    range=[PALETTE["bad"], PALETTE["warn"], PALETTE["ok"]],
)

def titles_per_year(df: pd.DataFrame):
    by_year = (
        df.dropna(subset=["release_year"])
          .groupby("release_year")
          .size()
          .reset_index(name="movies")
          .sort_values("release_year")
    )
    return (
        alt.Chart(by_year)
        .mark_bar()
        .encode(
            x=alt.X("release_year:O", title="Year"),
            y=alt.Y("movies:Q", title="Movies"),
            color=alt.Color("movies:Q", scale=alt.Scale(scheme="blues"), legend=None),
            tooltip=[
                alt.Tooltip("release_year:O", title="Year"),
                alt.Tooltip("movies:Q", title="Movies", format=",.0f"),
            ],
        )
        .properties(height=260)
    )

def hist_weighted_rating(df: pd.DataFrame, *, bad=7.0, warn=7.5):
    base = df[["weighted_rating"]].dropna().copy()
    base["wr_band"] = _wr_band(base["weighted_rating"], bad=bad, warn=warn)
    return (
        alt.Chart(base)
        .mark_bar()
        .encode(
            x=alt.X("weighted_rating:Q", bin=alt.Bin(maxbins=24), title="Weighted rating"),
            y=alt.Y("count()", title="Movies"),
            color=alt.Color("wr_band:N", scale=WR_SCALE, title="Quality band"),
            tooltip=[alt.Tooltip("count()", title="Movies", format=",.0f")],
        )
        .properties(height=260)
    )

def demand_scatter(df: pd.DataFrame, *, rating_alarm: float = 7.0):
    # rating_alarm = limiar do “vermelho”
    warn = min(9.9, rating_alarm + 0.5)

    cols = ["title", "genres_str", "popularity", "weighted_rating", "vote_count", "release_year"]
    base = df[cols].dropna().copy()
    base["wr_band"] = _wr_band(base["weighted_rating"], bad=rating_alarm, warn=warn)

    # Cor por faixas é simples, legível e “BI” [web:543]
    return (
        alt.Chart(base)
        .mark_circle(opacity=0.70)
        .encode(
            x=alt.X("popularity:Q", scale=alt.Scale(type="log"), title="Popularity (log)"),
            y=alt.Y("weighted_rating:Q", title="Weighted rating"),
            size=alt.Size("vote_count:Q", legend=None),
            color=alt.Color("wr_band:N", scale=WR_SCALE, title="Quality band"),
            tooltip=[
                alt.Tooltip("title:N", title="Title"),
                alt.Tooltip("release_year:Q", title="Year"),
                alt.Tooltip("genres_str:N", title="Genres"),
                alt.Tooltip("vote_count:Q", title="Votes", format=",.0f"),
                alt.Tooltip("popularity:Q", title="Popularity", format=".2f"),
                alt.Tooltip("weighted_rating:Q", title="Weighted", format=".2f"),
            ],
        )
        .properties(height=380)
    )

def genre_tradeoff_scatter(agg: pd.DataFrame, *, bad=7.0, warn=7.5):
    base = agg.copy()
    base["wr_band"] = _wr_band(base["avg_wr"], bad=bad, warn=warn)

    return (
        alt.Chart(base)
        .mark_circle(opacity=0.70)
        .encode(
            x=alt.X("movies:Q", title="Movies (volume)"),
            y=alt.Y("avg_wr:Q", title="Avg weighted_rating"),
            size=alt.Size("avg_votes:Q", legend=None),
            color=alt.Color("wr_band:N", scale=WR_SCALE, title="Quality band"),
            tooltip=[
                alt.Tooltip("genre:N", title="Genre"),
                alt.Tooltip("movies:Q", title="Movies", format=",.0f"),
                alt.Tooltip("avg_wr:Q", title="Avg WR", format=".2f"),
                alt.Tooltip("avg_votes:Q", title="Avg votes", format=",.0f"),
                alt.Tooltip("avg_popularity:Q", title="Avg popularity", format=".2f"),
            ],
        )
        .properties(height=380)
    )

def roi_budget_vs_revenue(df: pd.DataFrame, *, roi_bad=0.0, roi_warn=0.2):
    cols = ["title", "genres_str", "budget", "revenue", "profit", "roi", "weighted_rating"]
    base = df[cols].dropna().copy()
    base["roi_band"] = _roi_band(base["roi"], bad=roi_bad, warn=roi_warn)

    return (
        alt.Chart(base)
        .mark_circle(opacity=0.65)
        .encode(
            x=alt.X("budget:Q", scale=alt.Scale(type="log"), title="Budget (log)"),
            y=alt.Y("revenue:Q", scale=alt.Scale(type="log"), title="Revenue (log)"),
            size=alt.Size("profit:Q", legend=None),
            color=alt.Color("roi_band:N", scale=ROI_SCALE, title="ROI band"),
            tooltip=[
                alt.Tooltip("title:N", title="Title"),
                alt.Tooltip("genres_str:N", title="Genres"),
                alt.Tooltip("budget:Q", title="Budget", format=",.0f"),
                alt.Tooltip("revenue:Q", title="Revenue", format=",.0f"),
                alt.Tooltip("profit:Q", title="Profit", format=",.0f"),
                alt.Tooltip("roi:Q", title="ROI", format=".2f"),
                alt.Tooltip("weighted_rating:Q", title="Weighted", format=".2f"),
            ],
        )
        .properties(height=380)
    )

def quality_vs_roi(df: pd.DataFrame, *, wr_bad=7.0, wr_warn=7.5):
    base = df[["weighted_rating", "roi", "title"]].dropna().copy()
    base["wr_band"] = _wr_band(base["weighted_rating"], bad=wr_bad, warn=wr_warn)

    return (
        alt.Chart(base)
        .mark_circle(opacity=0.65)
        .encode(
            x=alt.X("weighted_rating:Q", title="Weighted rating"),
            y=alt.Y("roi:Q", title="ROI"),
            color=alt.Color("wr_band:N", scale=WR_SCALE, title="Quality band"),
            tooltip=[
                alt.Tooltip("title:N", title="Title"),
                alt.Tooltip("weighted_rating:Q", title="Weighted", format=".2f"),
                alt.Tooltip("roi:Q", title="ROI", format=".2f"),
            ],
        )
        .properties(height=340)
    )
