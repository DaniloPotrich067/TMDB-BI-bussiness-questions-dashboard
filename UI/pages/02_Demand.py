import streamlit as st
from components.data import load_curated
from components.filters import sidebar_common_filters, apply_common_filters
from components.charts import demand_scatter
from components.footer import render_footer
from components.viz_theme import enable_altair_theme

enable_altair_theme()

st.title("Demand – What attracts attention?")

st.markdown(
    """
**Questions this page answers**
- Which movies are attracting attention (demand) in my slice?
- Is popularity aligned with quality?
- Where are the outliers?

**Analyses**
- Ranking by `popularity`.
- Scatter log(popularity) vs `weighted_rating` with size by `vote_count`.
"""
)

df = load_curated()
(year_range, mv, genre_q, _) = sidebar_common_filters(df, show_genre=True, show_title=False)

with st.sidebar:
    topn = st.slider("Top N by popularity", 10, 100, 30, step=10)
    rating_alarm = st.slider("Alarm if weighted_rating below", 5.0, 9.5, 7.0, step=0.1)

df_f = apply_common_filters(df, year_range, mv, genre_q, "")

st.subheader("Top by popularity (proxy for demand)")
top = df_f.sort_values("popularity", ascending=False).head(topn)
tbl = top[["title", "release_year", "genres_str", "popularity", "weighted_rating", "vote_count"]].copy()
tbl["popularity"] = tbl["popularity"].round(2)
tbl["weighted_rating"] = tbl["weighted_rating"].round(2)
st.dataframe(tbl, hide_index=True, use_container_width=True)

st.subheader("Popularity vs weighted_rating (outliers)")
st.altair_chart(demand_scatter(df_f, rating_alarm=rating_alarm), use_container_width=True)

render_footer()
