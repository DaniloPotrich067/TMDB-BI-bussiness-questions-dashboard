from pathlib import Path
import pandas as pd
from ETL import extract as ext
from ETL import transform as tf

PROJECT_ROOT = Path(__file__).resolve().parent
CURATED_DIR = PROJECT_ROOT / "DATA" / "CURATED"
CURATED_DIR.mkdir(parents=True, exist_ok=True)

CURATED_FILE = CURATED_DIR / "top10k_tmdb_clean_enriched.jsonl"
CURATED_FIN_FILE = CURATED_DIR / "top10k_tmdb_financial_enriched.jsonl"

RAW_FILE = PROJECT_ROOT / "DATA" / "ORIGINAL" / "RAW" / "top10k_tmdb.jsonl"


def main(limit: int = 10000, sleep_s: float = 0.15) -> None:
    df_raw = ext.extract_tmdb_top_movies(limit=limit, out_path=RAW_FILE)

    cfg = ext.fetch_tmdb_config(ext.API_KEY)
    genre_map = ext.fetch_genre_map(ext.API_KEY, language="pt-BR")

    df = tf.transform_enrich(df_raw, genre_map, cfg)
    df = tf.transform_clean(df, drop_cols=True)

    # salva curated "base" (sem financeiro)
    with CURATED_FILE.open("w", encoding="utf-8") as f:
        df.to_json(f, orient="records", lines=True, force_ascii=False, date_format="iso")

    # financeiro via extract (API) + ROI via transform (manipulação)
    movie_ids = df["id"].dropna().astype(int).tolist()
    df_fin = ext.extract_movie_financials_df(movie_ids, api_key=ext.API_KEY, language="pt-BR", sleep_s=0.15, use_cache=True)

    df_fin_curated = tf.transform_add_roi(df, df_fin)

    with CURATED_FIN_FILE.open("w", encoding="utf-8") as f:
        df_fin_curated.to_json(f, orient="records", lines=True, force_ascii=False, date_format="iso")

    print(f"Saved: {CURATED_FILE}")
    print(f"Saved: {CURATED_FIN_FILE}")


if __name__ == "__main__":
    main(limit=1000)
