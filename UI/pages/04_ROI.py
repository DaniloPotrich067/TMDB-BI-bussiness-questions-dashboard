import streamlit as st

from components.data import load_financial_curated
from components.filters import sidebar_common_filters, apply_common_filters
from components.kpi import kpi, status_by_threshold
from components.formatters import money_short, pct2, fmt2, fmt0
from components.charts import roi_budget_vs_revenue, quality_vs_roi
from components.footer import render_footer
from components.viz_theme import enable_altair_theme
from components.quality import roi_ready_coverage

enable_altair_theme()

st.title("ROI – Budget vs revenue")

st.markdown(
    """
**Perguntas que esta página responde**
- Quais filmes dão maior retorno (ROI) e quais dão maior lucro (profit)?
- Qual é a cobertura real de dados financeiros no meu recorte?
- Qualidade se relaciona com retorno?

**Análises**
- ROI e profit calculados a partir de budget/revenue.
- Filtros mínimos (budget/revenue) para evitar ranking distorcido.
- Gráfico budget vs revenue em escala log.
"""
)

df = load_financial_curated()

need = {"budget", "revenue", "profit", "roi"}
missing = [c for c in need if c not in df.columns]
if missing:
    st.error(f"Financial curated não está pronto. Rode: python refresh.py | Missing columns: {missing}")
    st.stop()

(year_range, mv, genre_q, _) = sidebar_common_filters(df, show_genre=True, show_title=False)

with st.sidebar:
    min_budget = st.number_input("Minimum budget (USD)", min_value=0, value=1_000_000, step=500_000)
    min_revenue = st.number_input("Minimum revenue (USD)", min_value=0, value=1_000_000, step=500_000)
    topn = st.slider("Top N", 10, 100, 30, step=10)

df_f = apply_common_filters(df, year_range, mv, genre_q, "")

# Coverage calculado por função única (mesma regra da Home quando usar o mesmo piso)
coverage, n_ok, n_total = roi_ready_coverage(df_f, min_budget=min_budget, min_revenue=min_revenue)

# Base ROI-ready para análise
df_ok = df_f[
    (df_f["budget"].fillna(0) >= min_budget) &
    (df_f["revenue"].fillna(0) >= min_revenue)
].dropna(subset=["roi", "profit"]).copy()

avg_roi = float(df_ok["roi"].mean()) if len(df_ok) else 0.0
avg_profit = float(df_ok["profit"].mean()) if len(df_ok) else 0.0

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    kpi("Movies (filtered)", fmt0(len(df_f)), "neutral")
with c2:
    kpi("Valid financials", fmt0(len(df_ok)), status_by_threshold(len(df_ok), bad_lt=50, warn_lt=150))
with c3:
    kpi(
        "Coverage (ROI-ready)",
        pct2(coverage),
        status_by_threshold(coverage, bad_lt=0.30, warn_lt=0.60),
        help=f"{n_ok}/{n_total} títulos com ROI calculável acima do piso.",
    )
with c4:
    kpi("Avg ROI", pct2(avg_roi), status_by_threshold(avg_roi, bad_lt=0.10, warn_lt=0.20))
with c5:
    kpi("Avg profit", money_short(avg_profit), "neutral")

st.subheader("Top by ROI")
top_roi = df_ok.sort_values("roi", ascending=False).head(topn).copy()

top_roi_show = top_roi[["title", "release_year", "genres_str", "budget", "revenue", "profit", "roi", "weighted_rating", "vote_count"]].copy()
top_roi_show["budget"] = top_roi_show["budget"].apply(money_short)
top_roi_show["revenue"] = top_roi_show["revenue"].apply(money_short)
top_roi_show["profit"] = top_roi_show["profit"].apply(money_short)
top_roi_show["roi"] = top_roi_show["roi"].apply(pct2)
top_roi_show["weighted_rating"] = top_roi_show["weighted_rating"].apply(fmt2)

st.dataframe(top_roi_show, hide_index=True, use_container_width=True)

st.subheader("Budget vs revenue (log scale)")
st.altair_chart(roi_budget_vs_revenue(df_ok), use_container_width=True)

st.subheader("Quality vs ROI")
st.altair_chart(quality_vs_roi(df_ok), use_container_width=True)

render_footer()
