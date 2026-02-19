from pathlib import Path
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CURATED_DIR = PROJECT_ROOT / "DATA" / "CURATED"

CURATED_FILE = CURATED_DIR / "top10k_tmdb_clean_enriched.jsonl"
CURATED_FIN_FILE = CURATED_DIR / "top10k_tmdb_financial_enriched.jsonl"

@st.cache_data(ttl=3600)
def _load_jsonl(path: Path) -> pd.DataFrame:
    df = pd.read_json(path, lines=True)
    if "release_date" in df.columns:
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    return df

def load_curated() -> pd.DataFrame:
    return _load_jsonl(CURATED_FILE)

def load_financial_curated() -> pd.DataFrame:
    if CURATED_FIN_FILE.exists():
        return _load_jsonl(CURATED_FIN_FILE)
    return _load_jsonl(CURATED_FILE)
