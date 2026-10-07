import pandas as pd
import streamlit as st
from aiss import ui

ui.setup("M&E Dashboard", "📈")
st.title("📈 Monitoring and Evaluation Dashboard")
st.write("Five indicators focus on measured learning and persistence, not on devices installed.")

gr = st.session_state.get("gain_result")
ps = st.session_state.get("portfolio_stats")
if gr:
    st.info("Learning-gain values were prefilled from the Assessment Analyzer.")

st.markdown("#### 1. Learner competency gain")
c1, c2 = st.columns(2)
dz = c1.number_input("Effect size (Cohen's dz)", value=float(round(gr["cohens_dz"], 2)) if gr and gr["cohens_dz"] != float("inf") else 0.0, step=0.05)
p = c2.number_input("p-value (paired test)", min_value=0.0, max_value=1.0, value=float(round(gr["p"], 4)) if gr else 1.0, step=0.01, format="%.4f")

st.markdown("#### 2. Portfolio completion")
c1, c2 = st.columns(2)
enrolled = c1.number_input("Enrolled learners", min_value=0, value=ps[1] if ps else 0)
complete = c2.number_input("Learners with all six items", min_value=0, value=ps[0] if ps else 0)

st.markdown("#### 3. Instructional delivery")
sessions = st.number_input("Sessions delivered this term", min_value=0, value=0)

st.markdown("#### 4. Participation equity (female share)")
c1, c2 = st.columns(2)
club_f = c1.number_input("Female share of club (%)", 0.0, 100.0, 50.0)
school_f = c2.number_input("Female share of school (%)", 0.0, 100.0, 50.0)
tol = st.slider("Tolerance (percentage points)", 1, 30, 10)

st.markdown("#### 5. Programme persistence")
c1, c2, c3 = st.columns(3)
champ = c1.checkbox("Champion teacher still teaching at 12 months")
dev_total = c2.number_input("Devices installed", min_value=0, value=0)
dev_ok = c3.number_input("Devices operational", min_value=0, value=0)

dev_pct = (dev_ok / dev_total * 100) if dev_total else None
rows = [
    ("Learner competency gain", f"dz = {dz:.2f}, p = {p:.3f}", "Met" if (p < 0.05 and dz >= 0.2) else "Not met", "p < 0.05 and dz >= 0.2"),
    ("Portfolio completion", f"{complete}/{enrolled}" if enrolled else "n/a", "Met" if enrolled and complete / enrolled > 0.5 else "Not met", "Majority of learners complete all six items"),
    ("Instructional delivery", f"{sessions} sessions", "Met" if sessions >= 12 else "Not met", "At least 12 sessions in the first term"),
    ("Participation equity", f"gap {club_f - school_f:+.1f} pp", "Met" if abs(club_f - school_f) <= tol else "Not met", f"Club within {tol} pp of school"),
    ("Programme persistence", f"champion {'yes' if champ else 'no'}; devices {dev_pct:.0f}%" if dev_pct is not None else f"champion {'yes' if champ else 'no'}; no devices recorded",
     "Met" if champ and (dev_pct is None or dev_pct >= 70) else "Not met", "Champion retained; at least 70% of devices operational (if any)"),
]
df = pd.DataFrame(rows, columns=["Indicator", "Value", "Status", "Threshold"])
st.markdown("#### Results")
met = int((df["Status"] == "Met").sum())
st.metric("Indicators met", f"{met} of 5")
st.dataframe(df, use_container_width=True, hide_index=True)
st.caption("Thresholds follow the AISS paper where it gives one; the 10-point equity tolerance and the dz >= 0.2 rule are adjustable planning conventions.")
st.download_button("Download dashboard (CSV)", ui.csv_bytes(df), file_name="aiss_me_dashboard.csv", mime="text/csv")
