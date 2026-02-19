import pandas as pd
import streamlit as st

def sidebar_common_filters(df: pd.DataFrame, *, show_genre: bool = True, show_title: bool = False):
    with st.sidebar:
        st.header("Filters")

        years = df["release_year"].dropna().astype(int)
        y0, y1 = int(years.min()), int(years.max())
        year_range = st.slider("Year range", y0, y1, (y0, y1))

        min_votes = st.number_input("Minimum votes", min_value=0, value=2000, step=500)

        genre_q = ""
        if show_genre:
            genre_q = st.text_input("Genre contains (optional)", "")

        title_q = ""
        if show_title:
            title_q = st.text_input("Title contains (optional)", "")

        st.divider()

    return year_range, int(min_votes), genre_q, title_q

def apply_common_filters(df: pd.DataFrame, year_range, min_votes: int, genre_q: str = "", title_q: str = "") -> pd.DataFrame:
    y0, y1 = year_range
    out = df.copy()

    if "release_year" in out.columns:
        out = out[out["release_year"].between(y0, y1)]

    if "vote_count" in out.columns:
        out = out[out["vote_count"].fillna(0) >= min_votes]

    if genre_q.strip() and "genres_str" in out.columns:
        out = out[out["genres_str"].str.contains(genre_q, case=False, na=False)]

    if title_q.strip() and "title" in out.columns:
        out = out[out["title"].str.contains(title_q, case=False, na=False)]

    return out
