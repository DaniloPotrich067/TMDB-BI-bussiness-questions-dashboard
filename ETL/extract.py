from __future__ import annotations

from pathlib import Path
import os
import json
import time
import requests
import pandas as pd
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY não encontrada no .env")

DISCOVER_URL = "https://api.themoviedb.org/3/discover/movie"
CONFIG_URL = "https://api.themoviedb.org/3/configuration"
GENRE_URL = "https://api.themoviedb.org/3/genre/movie/list"
MOVIE_DETAIL_URL = "https://api.themoviedb.org/3/movie/{}"

CACHE_DIR = PROJECT_ROOT / "DATA" / "CACHE" / "tmdb_movie_financials"


def extract_tmdb_top_movies(
    limit: int = 1000,
    out_path: Path | str = PROJECT_ROOT / "DATA" / "ORIGINAL" / "RAW" / "top10k_tmdb.jsonl",
    start_page: int = 1,
) -> pd.DataFrame:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    params = {
        "api_key": API_KEY,
        "sort_by": "vote_average.desc",
        "vote_count.gte": 2000,
        "language": "pt-BR",
        "page": start_page,
    }

    movies: list[dict] = []
    while len(movies) < limit:
        resp = requests.get(DISCOVER_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        movies.extend(data.get("results", []))

        if params["page"] >= data.get("total_pages", 0):
            break
        params["page"] += 1

    movies = movies[:limit]

    with out_path.open("w", encoding="utf-8") as f:
        for m in movies:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    return pd.DataFrame.from_records(movies)


def fetch_tmdb_config(api_key: str) -> dict:
    resp = requests.get(CONFIG_URL, params={"api_key": api_key}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_genre_map(api_key: str, language: str = "pt-BR") -> dict[int, str]:
    resp = requests.get(GENRE_URL, params={"api_key": api_key, "language": language}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return {g["id"]: g["name"] for g in data.get("genres", [])}


def fetch_movie_financials(api_key: str, movie_id: int, language: str = "pt-BR") -> dict:
    url = MOVIE_DETAIL_URL.format(int(movie_id))
    resp = requests.get(url, params={"api_key": api_key, "language": language}, timeout=30)
    resp.raise_for_status()
    d = resp.json()
    return {
        "id": int(movie_id),
        "budget": d.get("budget"),
        "revenue": d.get("revenue"),
        "runtime": d.get("runtime"),
    }


def _cache_path(movie_id: int) -> Path:
    return CACHE_DIR / f"{int(movie_id)}.json"


def extract_movie_financials_df(
    movie_ids: list[int],
    api_key: str,
    language: str = "pt-BR",
    sleep_s: float = 0.15,
    use_cache: bool = True,
) -> pd.DataFrame:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for mid in movie_ids:
        mid = int(mid)
        p = _cache_path(mid)

        if use_cache and p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
        else:
            data = fetch_movie_financials(api_key, mid, language=language)
            if use_cache:
                p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            time.sleep(sleep_s)

        rows.append(data)

    return pd.DataFrame(rows)
