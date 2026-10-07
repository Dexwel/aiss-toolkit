import pandas as pd
import streamlit as st
from aiss import ui, logic
from aiss.data import RUBRIC

ui.setup("Project Rubric", "🎯")
st.title("🎯 Project Rubric Scorer")
st.write("Score a student project on five criteria (1 to 3 points each, maximum 15). "
         "Suggested bands: 5-7 Emerging, 8-11 Proficient, 12-15 Advanced.")

if "projects" not in st.session_state:
    st.session_state["projects"] = []

with st.form("rubric"):
    name = st.text_input("Student name or ID")
    title = st.text_input("Project title (optional)")
    scores = {}
    for crit, levels in RUBRIC.items():
        scores[crit] = st.radio(crit, [1, 2, 3], horizontal=False,
                                format_func=lambda i, lv=levels: f"{i} pt: {lv[i-1]}", key=f"r_{crit}")
    add = st.form_submit_button("Score and add to list", type="primary")

if add:
    total = logic.rubric_total(scores)
    band = logic.rubric_band(total)
    st.success(f"Total: **{total} / 15** ({band})")
    st.session_state["projects"].append({"Student": name or "(unnamed)", "Project": title, **scores, "Total": total, "Band": band})

if st.session_state["projects"]:
    df = pd.DataFrame(st.session_state["projects"])
    st.markdown("#### Scored projects")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.bar_chart(df["Band"].value_counts())
    c1, c2 = st.columns(2)
    c1.download_button("Download scores (CSV)", ui.csv_bytes(df), file_name="aiss_project_scores.csv", mime="text/csv")
    if c2.button("Clear list"):
        st.session_state["projects"] = []
        st.rerun()
