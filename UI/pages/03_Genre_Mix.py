import streamlit as st
from components.data import load_curated
from components.filters import sidebar_common_filters, apply_common_filters
from components.charts import genre_tradeoff_scatter
from components.footer import render_footer
from components.viz_theme import enable_altair_theme

enable_altair_theme()

st.title("Genre mix – Quality vs volume")

st.markdown(
    """
**Perguntas que esta página responde**
- Quais gêneros performam melhor em qualidade no meu recorte?
- Tenho volume suficiente por gênero para confiar?
- Quais gêneros equilibram qualidade e escala?

**Análises**
- Explode de gêneros + agregação por gênero.
- Scatter “volume vs qualidade” com cor por faixa de qualidade.
"""
)

df = load_curated()

if "genres_names" not in df.columns:
    if "genres_str" not in df.columns:
        st.error("Missing genre columns (genres_str/genres_names). Rode o ETL com transform_enrich.")
        st.stop()
    df["genres_names"] = df["genres_str"].fillna("").apply(lambda s: [x.strip() for x in s.split(",") if x.strip()])

(year_range, mv, _, _) = sidebar_common_filters(df, show_genre=False, show_title=False)

with st.sidebar:
    min_movies = st.slider("Min movies per genre", 1, 200, 20, step=5)

df_f = apply_common_filters(df, year_range, mv, "", "")

df_g = df_f.explode("genres_names").rename(columns={"genres_names": "genre"})
df_g = df_g.dropna(subset=["genre", "weighted_rating"])

agg = (
    df_g.groupby("genre")
        .agg(
            movies=("id", "count"),
            avg_wr=("weighted_rating", "mean"),
            avg_votes=("vote_count", "mean"),
            avg_popularity=("popularity", "mean"),
        )
        .reset_index()
)

agg = agg[agg["movies"] >= min_movies].sort_values("avg_wr", ascending=False)
agg_show = agg.copy()
for c in ["avg_wr", "avg_votes", "avg_popularity"]:
    agg_show[c] = agg_show[c].round(2)

st.subheader("Genres ranked by avg weighted_rating (volume constrained)")
st.dataframe(agg_show, hide_index=True, use_container_width=True)

st.subheader("Top 15 genres by avg weighted_rating")
st.bar_chart(agg.head(15).set_index("genre")[["avg_wr"]])

st.subheader("Trade-off: volume vs quality")
st.altair_chart(genre_tradeoff_scatter(agg), use_container_width=True)

render_footer()
