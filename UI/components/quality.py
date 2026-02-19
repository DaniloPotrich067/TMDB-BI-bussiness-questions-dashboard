import pandas as pd

def roi_ready_coverage(
    df: pd.DataFrame,
    *,
    min_budget: float,
    min_revenue: float,
) -> tuple[float, int, int]:
    """
    Coverage = qtd ROI-ready / total (na mesma base).
    ROI-ready: budget>=min_budget, revenue>=min_revenue, roi e profit não nulos.
    Retorna: (coverage, n_ok, n_total)
    """
    if df is None or len(df) == 0:
        return 0.0, 0, 0

    need = {"budget", "revenue", "profit", "roi"}
    if any(c not in df.columns for c in need):
        return 0.0, 0, len(df)

    base = df.copy()

    ok = base[
        (base["budget"].fillna(0) >= min_budget) &
        (base["revenue"].fillna(0) >= min_revenue)
    ].dropna(subset=["roi", "profit"])

    n_total = len(base)
    n_ok = len(ok)
    cov = (n_ok / n_total) if n_total else 0.0
    return cov, n_ok, n_total
