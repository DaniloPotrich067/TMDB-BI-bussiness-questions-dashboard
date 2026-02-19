import streamlit as st

from components.data import load_curated, load_financial_curated
from components.formatters import fmt2, fmt0, pct2, money_short
from components.kpi import kpi, status_by_threshold
from components.charts import hist_weighted_rating, titles_per_year
from components.footer import render_footer
from components.viz_theme import enable_altair_theme
from components.quality import roi_ready_coverage

st.set_page_config(
    page_title="TMDB – BI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

enable_altair_theme()

df = load_curated()
df_fin = load_financial_curated()

st.title("TMDB – Business Questions Dashboard")
st.markdown("Home de overview (estilo BI): resume o recorte inteiro e te dá próximos passos antes das páginas de análise.")

# Defaults (iguais ao ROI)
MIN_BUDGET_DEFAULT = 1_000_000
MIN_REVENUE_DEFAULT = 1_000_000

with st.sidebar:
    st.header("Quick actions")
    st.write("- **Curation**: o que destacar com confiança")
    st.write("- **Demand**: o que está puxando atenção")
    st.write("- **Genre mix**: trade-off qualidade x volume")
    st.write("- **ROI**: eficiência e retorno financeiro")
    st.divider()
    st.code("python refresh.py\nstreamlit run UI/app.py", language="bash")
    if st.button("Clear cache (dev)"):
        st.cache_data.clear()
        st.rerun()

min_year = int(df["release_year"].dropna().min()) if len(df) else 0
max_year = int(df["release_year"].dropna().max()) if len(df) else 0
avg_wr = float(df["weighted_rating"].mean()) if len(df) else 0.0
avg_votes = float(df["vote_count"].mean()) if "vote_count" in df.columns and len(df) else 0.0

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    kpi("Movies", fmt0(len(df)), "neutral")
with c2:
    kpi("Min year", fmt0(min_year), "neutral")
with c3:
    kpi("Max year", fmt0(max_year), "neutral")
with c4:
    kpi("Avg weighted_rating", fmt2(avg_wr), status_by_threshold(avg_wr, bad_lt=7.0, warn_lt=7.5))
with c5:
    kpi("Avg votes", fmt2(avg_votes), status_by_threshold(avg_votes, bad_lt=2000, warn_lt=6000))

st.subheader("Data quality signals")
dq1, dq2, dq3 = st.columns(3)

# Métrica CONSISTENTE: mesma regra do ROI (ROI-ready)
cov_roi_ready, n_ok, n_total = roi_ready_coverage(
    df_fin,
    min_budget=MIN_BUDGET_DEFAULT,
    min_revenue=MIN_REVENUE_DEFAULT,
)

with dq1:
    kpi(
        f"ROI-ready coverage (>= ${MIN_BUDGET_DEFAULT:,.0f} / >= ${MIN_REVENUE_DEFAULT:,.0f})",
        pct2(cov_roi_ready),
        status_by_threshold(cov_roi_ready, bad_lt=0.30, warn_lt=0.60),
        help=f"{n_ok}/{n_total} títulos com ROI calculável acima do piso.",
    )

with dq2:
    null_wr = float(df["weighted_rating"].isna().mean()) if "weighted_rating" in df.columns and len(df) else 0.0
    kpi(
        "Missing weighted_rating",
        pct2(null_wr),
        status_by_threshold(1 - null_wr, bad_lt=0.90, warn_lt=0.97),
        help="Se faltar nota, ranking e histograma perdem força.",
    )

with dq3:
    null_pop = float(df["popularity"].isna().mean()) if "popularity" in df.columns and len(df) else 0.0
    kpi(
        "Missing popularity",
        pct2(null_pop),
        status_by_threshold(1 - null_pop, bad_lt=0.90, warn_lt=0.97),
        help="Se faltar popularity, a página Demand perde sentido.",
    )

st.subheader("For you (highlights)")
colA, colB, colC = st.columns(3)

with colA:
    st.markdown("#### Curation pick")
    pick = (
        df.dropna(subset=["weighted_rating"])
          .sort_values(["weighted_rating", "vote_count"], ascending=False)
          .head(5)[["title", "release_year", "weighted_rating", "vote_count"]]
          .copy()
    )
    pick["weighted_rating"] = pick["weighted_rating"].round(2)
    st.dataframe(pick, hide_index=True, use_container_width=True)

with colB:
    st.markdown("#### Demand (top popularity)")
    top_pop = (
        df.dropna(subset=["popularity"])
          .sort_values("popularity", ascending=False)
          .head(5)[["title", "release_year", "popularity", "weighted_rating"]]
          .copy()
    )
    top_pop["popularity"] = top_pop["popularity"].round(2)
    top_pop["weighted_rating"] = top_pop["weighted_rating"].round(2)
    st.dataframe(top_pop, hide_index=True, use_container_width=True)

with colC:
    st.markdown("#### ROI (top)")
    # Usa o mesmo piso default da home para não “mentir” na highlight
    fin_for_top = df_fin.copy()
    if all(c in fin_for_top.columns for c in ["roi", "profit", "budget", "revenue"]):
        fin_for_top = fin_for_top[
            (fin_for_top["budget"].fillna(0) >= MIN_BUDGET_DEFAULT) &
            (fin_for_top["revenue"].fillna(0) >= MIN_REVENUE_DEFAULT)
        ].dropna(subset=["roi", "profit"])

    if len(fin_for_top):
        roi_top = (
            fin_for_top.sort_values("roi", ascending=False)
                       .head(5)[["title", "release_year", "roi", "profit"]]
                       .copy()
        )
        roi_top["roi"] = roi_top["roi"].apply(lambda x: f"{x*100:.2f}%")
        roi_top["profit"] = roi_top["profit"].apply(money_short)
        st.dataframe(roi_top, hide_index=True, use_container_width=True)
    else:
        st.info("ROI highlights indisponíveis para este piso (tente reduzir o mínimo na página ROI).")

st.subheader("Overview charts")
ch1, ch2 = st.columns(2)

with ch1:
    st.markdown("#### Titles per year")
    st.altair_chart(titles_per_year(df), use_container_width=True)

with ch2:
    st.markdown("#### Weighted_rating distribution")
    st.altair_chart(hist_weighted_rating(df), use_container_width=True)

render_footer()
