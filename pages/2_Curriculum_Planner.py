import pandas as pd
import streamlit as st
from aiss import ui
from aiss.data import CURRICULUM, TIERS, STAGES, EQUITY

ui.setup("Curriculum Planner", "📅")
st.title("📅 12-Week Curriculum Planner")
st.write("One hour per week over one term. Learning outcomes are identical at every tier; only the activity format differs.")

default = st.session_state.get("plan_tier", 0)
tier = st.selectbox("Your tier", list(TIERS), index=default, format_func=lambda t: TIERS[t]["name"])
st.caption(f"Students see: {TIERS[tier]['sees']}. Students do: {TIERS[tier]['does']}. Students can prove: {TIERS[tier]['proves']}.")

col = "Paper activity (Tier 0-1)" if tier <= 1 else "Digital activity (Tier 2-3)"
rows = [{"Weeks": r["Weeks"], "Core topic": r["Core topic"], "Your activity": r[col]} for r in CURRICULUM]
df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True, hide_index=True)
st.download_button("Download plan (CSV)", ui.csv_bytes(df), file_name=f"aiss_plan_tier{tier}.csv", mime="text/csv")
if tier >= 2:
    st.info("Keep a paper portfolio alongside saved models so evidence stays portable if equipment fails.")
with st.expander("See both paper and digital versions side by side"):
    st.dataframe(pd.DataFrame(CURRICULUM), use_container_width=True, hide_index=True)

with st.expander("Worked example: card-sorting lesson (Weeks 3 to 7, no electricity)"):
    st.markdown("""
1. **Label.** Students sort picture cards of market produce into *fresh* and *spoiled*, noting the features they used (colour, firmness, marks).
2. **Build a rule.** Groups write a rule table from their labelled examples.
3. **Test.** They test the rule on cards they have not seen and count the errors.
4. **Reflect.** Why did it fail? Which cards were unfair to the rule? What data would improve it?

Labelling, rule-building and error-counting are the training, testing and evaluation steps of supervised learning.
""")
with st.expander("Learner progression (JSS 1 to SS 3)"):
    st.dataframe(pd.DataFrame(STAGES, columns=["Stage", "Class", "Learning focus"]), use_container_width=True, hide_index=True)
with st.expander("Equity: who might be left out, and what to do"):
    st.dataframe(pd.DataFrame(EQUITY, columns=["Student group", "Common barrier", "Teacher action"]), use_container_width=True, hide_index=True)
