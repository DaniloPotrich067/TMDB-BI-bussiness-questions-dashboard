import streamlit as st
from components.data import load_curated
from components.filters import sidebar_common_filters, apply_common_filters
from components.kpi import kpi, status_by_threshold
from components.formatters import fmt2, fmt0
from components.charts import hist_weighted_rating, titles_per_year
from components.footer import render_footer
from components.viz_theme import enable_altair_theme

enable_altair_theme()

st.title("Curation – What should we highlight?")

st.markdown(
    """
**Questions this page answers**
- Which titles should I highlight with confidence (editorial curation)?
- How is quality distributed in my slice?
- Does my slice have enough volume for me to trust?

**Analyses**
- Ranking by `weighted_rating` with vote floor.
- Distribution (histogram) to avoid 'blind average'.
"""
)

df = load_curated()
(year_range, mv, genre_q, title_q) = sidebar_common_filters(df, show_genre=True, show_title=True)

with st.sidebar:
    topn = st.slider("Top N", 10, 100, 20, step=10)

df_f = apply_common_filters(df, year_range, mv, genre_q, title_q)
rank = df_f.sort_values(["weighted_rating", "vote_count"], ascending=False).head(topn)

avg_wr = float(df_f["weighted_rating"].mean()) if len(df_f) else 0.0
avg_votes = float(df_f["vote_count"].mean()) if len(df_f) else 0.0

c1, c2, c3 = st.columns(3)
with c1:
    kpi("Movies in filter", fmt0(len(df_f)), "neutral")
with c2:
    kpi("Avg weighted_rating", fmt2(avg_wr), status_by_threshold(avg_wr, bad_lt=7.0, warn_lt=7.5))
with c3:
    kpi("Avg votes", fmt2(avg_votes), status_by_threshold(avg_votes, bad_lt=2000, warn_lt=6000))

st.subheader("Top titles (quality with confidence)")
show_cols = ["title", "release_year", "genres_str", "weighted_rating", "vote_count", "popularity"]
tbl = rank[show_cols].copy()
for c in ["weighted_rating", "popularity"]:
    if c in tbl.columns:
        tbl[c] = tbl[c].round(2)
st.dataframe(tbl, hide_index=True, use_container_width=True)

st.subheader("Titles per year (supply in this slice)")
st.altair_chart(titles_per_year(df_f), use_container_width=True)

st.subheader("Distribution of weighted_rating")
st.altair_chart(hist_weighted_rating(df_f), use_container_width=True)

render_footer()
