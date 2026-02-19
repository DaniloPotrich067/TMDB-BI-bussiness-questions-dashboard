import streamlit as st

DEFAULT_TEXT = "Desenvolvido por Danilo Gomes Potrich | © 2026"

def render_footer(
    text: str = DEFAULT_TEXT,
    *,
    height_px: int = 46,
    bg: str = "rgba(15, 23, 42, 0.92)",
    fg: str = "rgba(255,255,255,0.85)",
    border: str = "rgba(255,255,255,0.10)",
):
    # st.markdown em função funciona normalmente; o HTML/CSS é aplicado na página [web:562]
    st.markdown(
        f"""
<style>
.stApp {{
  padding-bottom: {height_px + 18}px;
}}

.tmbd-footer {{
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  z-index: 9999;

  background: {bg};
  color: {fg};
  border-top: 1px solid {border};

  text-align: center;
  padding: 10px 12px;
  font-size: 13px;
  backdrop-filter: blur(6px);
}}
</style>

<div class="tmbd-footer">{text}</div>
        """,
        unsafe_allow_html=True,
    )
