"""Shared Streamlit helpers."""
from pathlib import Path
import io
import pandas as pd
import streamlit as st

ASSETS = Path(__file__).resolve().parent.parent / "assets"
DISCLAIMER = ("Planning aid based on a conceptual framework that has not yet been empirically validated. "
              "This app does not store your data; entries exist only during your browser session.")


def setup(title: str, icon: str = "🎓", wide: bool = True) -> None:
    st.set_page_config(page_title=f"{title} | AISS Toolkit", page_icon=icon,
                       layout="wide" if wide else "centered", initial_sidebar_state="expanded")
    st.markdown(
        """<style>
        .block-container {padding-top: 2rem; max-width: 1150px;}
        div[data-testid="stMetricValue"] {font-size: 1.6rem;}
        .aiss-note {font-size: 0.85rem; color: #555;}
        </style>""", unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("### AISS Toolkit")
        tier = st.session_state.get("plan_tier")
        if tier is not None:
            st.success(f"Your planning tier: **Tier {tier}**")
        else:
            st.info("No tier set yet. Start with the School Audit.")
        st.caption(DISCLAIMER)


def show_image(name: str, caption: str) -> None:
    st.image(str(ASSETS / name), caption=caption, use_container_width=True)


def csv_bytes(df: pd.DataFrame) -> bytes:
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8")


def naira(x) -> str:
    try:
        return f"₦{x:,.0f}"
    except (TypeError, ValueError):
        return "n/a"
