import streamlit as st

def _color(status: str) -> str:
    return {
        "ok": "#22c55e",
        "warn": "#f59e0b",
        "bad": "#ef4444",
        "neutral": "#60a5fa",
    }.get(status, "#60a5fa")

def kpi(label: str, value_text: str, status: str = "neutral", help: str | None = None):
    border = _color(status)
    st.markdown(
        f"""
<div style="
  border: 1px solid rgba(255,255,255,0.12);
  border-left: 6px solid {border};
  padding: 12px 14px;
  border-radius: 10px;
  background: rgba(255,255,255,0.02);
">
  <div style="font-size: 0.85rem; opacity: 0.85;">{label}</div>
  <div style="font-size: 1.8rem; font-weight: 700; margin-top: 4px;">{value_text}</div>
</div>
        """,
        unsafe_allow_html=True,
    )
    if help:
        st.caption(help)

def status_by_threshold(value: float, *, bad_lt: float, warn_lt: float) -> str:
    if value < bad_lt:
        return "bad"
    if value < warn_lt:
        return "warn"
    return "ok"
