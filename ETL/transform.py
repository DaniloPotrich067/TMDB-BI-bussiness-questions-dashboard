from __future__ import annotations
import pandas as pd


def build_image_url(config: dict, file_path: str | None, kind: str = "poster", size: str | None = None) -> str | None:
    if not file_path:
        return None

    images = config["images"]
    base = images["secure_base_url"]

    sizes = images["poster_sizes"] if kind == "poster" else images["backdrop_sizes"]
    chosen = size or ("w342" if "w342" in sizes else sizes[0])
    return f"{base}{chosen}{file_path}"


def transform_enrich(df: pd.DataFrame, genre_map: dict[int, str], tmdb_config: dict) -> pd.DataFrame:
    df = df.copy()

    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["release_year"] = df["release_date"].dt.year

    df["genres_names"] = df["genre_ids"].apply(
        lambda ids: [genre_map.get(i, f"UNKNOWN_{i}") for i in (ids or [])]
    )
    df["genres_str"] = df["genres_names"].apply(lambda xs: ", ".join(xs))

    m = 2000
    C = pd.to_numeric(df["vote_average"], errors="coerce").mean()
    v = pd.to_numeric(df["vote_count"], errors="coerce")
    R = pd.to_numeric(df["vote_average"], errors="coerce")

    df["weighted_rating"] = (v / (v + m)) * R + (m / (v + m)) * C
    df["weighted_rating"] = df["weighted_rating"].round(2)

    df["poster_url"] = df["poster_path"].apply(lambda p: build_image_url(tmdb_config, p, "poster"))
    df["backdrop_url"] = df["backdrop_path"].apply(lambda p: build_image_url(tmdb_config, p, "backdrop"))

    return df


def transform_clean(df: pd.DataFrame, drop_cols: bool = True) -> pd.DataFrame:
    df = df.copy()

    if "id" in df.columns:
        df = df.drop_duplicates(subset=["id"])

    str_cols = [c for c in [
        "title", "original_title", "overview",
        "poster_path", "backdrop_path", "original_language",
        "genres_str"
    ] if c in df.columns]

    for c in str_cols:
        df[c] = df[c].astype("string").str.strip()
        df.loc[df[c].isin(["", "None", "null", "NaN"]), c] = pd.NA

    for c in [x for x in ["popularity", "vote_average", "vote_count", "weighted_rating"] if x in df.columns]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    if "vote_average" in df.columns:
        df.loc[(df["vote_average"] < 0) | (df["vote_average"] > 10), "vote_average"] = pd.NA
    if "weighted_rating" in df.columns:
        df.loc[(df["weighted_rating"] < 0) | (df["weighted_rating"] > 10), "weighted_rating"] = pd.NA
        df["weighted_rating"] = df["weighted_rating"].round(2)

    critical = [c for c in ["id", "title", "vote_average", "vote_count"] if c in df.columns]
    df = df.dropna(subset=critical)

    if "id" in df.columns:
        df["id"] = pd.to_numeric(df["id"], errors="coerce").astype("Int64")
    if "vote_count" in df.columns:
        df["vote_count"] = df["vote_count"].astype("Int64")
    if "release_year" in df.columns:
        df["release_year"] = df["release_year"].astype("Int64")

    if drop_cols:
        df = df.drop(columns=["adult", "video"], errors="ignore")

    if "overview" in df.columns:
        df["overview"] = df["overview"].fillna("")

    return df


def transform_add_roi(df_movies: pd.DataFrame, df_fin: pd.DataFrame) -> pd.DataFrame:
    df = df_movies.copy().merge(df_fin, on="id", how="left")

    for c in ["budget", "revenue", "runtime"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df["profit"] = df["revenue"] - df["budget"]
    df["roi"] = (df["profit"] / df["budget"]).where(df["budget"] > 0)
    df["revenue_to_budget"] = (df["revenue"] / df["budget"]).where(df["budget"] > 0)
    df["revenue_per_min"] = (df["revenue"] / df["runtime"]).where(df["runtime"] > 0)

    return df
