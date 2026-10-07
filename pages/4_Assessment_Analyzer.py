import numpy as np
import pandas as pd
import streamlit as st
from aiss import ui, logic

ui.setup("Assessment Analyzer", "📝")
st.title("📝 Assessment Analyzer")
st.write("Analyse the 20-item paper quiz given at the **start** and **end** of the term, and check that the club reflects your school.")

tab1, tab2 = st.tabs(["Learning gain (baseline vs endline)", "Participation fairness"])

with tab1:
    max_score = st.number_input("Maximum quiz score", min_value=1, value=20, step=1)
    source = st.radio("Data source", ["Demo data", "Enter scores", "Upload CSV"], horizontal=True)
    template = pd.DataFrame({"student_id": ["S01", "S02"], "sex": ["F", "M"], "baseline": [8, 10], "endline": [13, 14]})
    st.download_button("Download CSV template", ui.csv_bytes(template), file_name="aiss_scores_template.csv", mime="text/csv")

    if source == "Demo data":
        rng = np.random.default_rng(42)
        b = rng.integers(5, 13, 24)
        e = np.clip(b + rng.integers(-1, 7, 24), 0, max_score)
        df = pd.DataFrame({"student_id": [f"S{i+1:02d}" for i in range(24)], "sex": ["F", "M"] * 12, "baseline": b, "endline": e})
        st.caption("Demo data is randomly generated for illustration only.")
    elif source == "Enter scores":
        start = pd.DataFrame({"student_id": [""] * 5, "sex": [""] * 5, "baseline": [None] * 5, "endline": [None] * 5})
        df = st.data_editor(start, num_rows="dynamic", use_container_width=True, key="score_editor",
                            column_config={"sex": st.column_config.SelectboxColumn("sex", options=["F", "M", ""]),
                                           "baseline": st.column_config.NumberColumn(min_value=0, max_value=float(max_score)),
                                           "endline": st.column_config.NumberColumn(min_value=0, max_value=float(max_score))})
    else:
        up = st.file_uploader("Upload CSV with columns: student_id, sex (optional), baseline, endline", type="csv")
        df = pd.read_csv(up) if up is not None else pd.DataFrame(columns=["student_id", "sex", "baseline", "endline"])

    if {"baseline", "endline"} <= set(df.columns):
        scored = df.copy()
        scored[["baseline", "endline"]] = scored[["baseline", "endline"]].apply(pd.to_numeric, errors="coerce")
        scored = scored.dropna(subset=["baseline", "endline"])
        bad = scored[(scored["baseline"] < 0) | (scored["endline"] < 0) | (scored["baseline"] > max_score) | (scored["endline"] > max_score)]
        if len(bad):
            st.error(f"{len(bad)} row(s) have scores outside 0 to {max_score}. Fix them before analysing.")
        elif len(scored) < 2:
            st.info("Enter or upload at least two students with both scores.")
        else:
            r = logic.analyze_gain(scored, max_score)
            st.session_state["gain_result"] = r
            m = st.columns(4)
            m[0].metric("Students", r["n"])
            m[1].metric("Baseline mean", f"{r['baseline_mean']:.1f}")
            m[2].metric("Endline mean", f"{r['endline_mean']:.1f}", delta=f"{r['mean_gain']:+.1f}")
            m[3].metric("Improved", f"{r['pct_improved']:.0f}%")
            st.markdown(
                f"- Mean gain: **{r['mean_gain']:.2f} points** ({r['gain_pct_points']:.1f} percentage points of the quiz), "
                f"95% CI {r['ci_low']:.2f} to {r['ci_high']:.2f}\n"
                f"- Paired t-test: t = {r['t']:.2f}, p = {r['p']:.4f}; Wilcoxon p = {r['wilcoxon_p']:.4f}\n"
                f"- Effect size (Cohen's dz): **{r['cohens_dz']:.2f}** ({r['effect_label']} by conventional benchmarks)")
            diff = (scored["endline"] - scored["baseline"]).astype(int)
            st.bar_chart(diff.value_counts().sort_index(), x_label="Gain (points)", y_label="Students")
            if "sex" in scored.columns and scored["sex"].astype(str).str.strip().ne("").any():
                g = scored.assign(gain=scored["endline"] - scored["baseline"]).groupby("sex")["gain"].agg(["count", "mean"]).round(2)
                g.columns = ["Students", "Mean gain"]
                st.markdown("**Gain by sex**")
                st.dataframe(g, use_container_width=True)
            st.warning("Without a comparison group, report gains as *associated with* the programme, not caused by it.")
            out = scored.assign(gain=scored["endline"] - scored["baseline"])
            st.download_button("Download scored data (CSV)", ui.csv_bytes(out), file_name="aiss_scored.csv", mime="text/csv")
    else:
        st.info("Add baseline and endline scores to begin.")

with tab2:
    st.write("Club composition should look like your school. Large gaps mean some learners are being left out.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Club members**")
        cf = st.number_input("Female (club)", 0, value=18, key="cf")
        cm = st.number_input("Male (club)", 0, value=22, key="cm")
    with c2:
        st.markdown("**Whole school roll**")
        sf = st.number_input("Female (school)", 0, value=240, key="sf")
        sm = st.number_input("Male (school)", 0, value=210, key="sm")
    thr = st.slider("Flag a gap larger than (percentage points)", 1, 30, 10)
    if cf + cm == 0 or sf + sm == 0:
        st.info("Enter counts for both the club and the school.")
    else:
        gap = logic.participation_gap({"Female": cf, "Male": cm}, {"Female": sf, "Male": sm}, thr)
        st.dataframe(gap, use_container_width=True, hide_index=True)
        if (gap["Status"] == "Review").any():
            st.warning("The club does not match the school. Try school-hours sessions and direct invitations (see Curriculum Planner, equity section).")
        else:
            st.success("Club composition is within your chosen tolerance.")
