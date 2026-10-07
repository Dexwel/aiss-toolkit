import pandas as pd
import streamlit as st
from aiss import ui
from aiss.data import TIERS, REFERENCES

ui.setup("About", "ℹ️")
st.title("ℹ️ About the AISS Framework")
st.markdown("""
**AISS** stands for **AI Implementation Framework for Nigerian Secondary Schools**. It is a learner-centred,
resource-differentiated model that holds learning outcomes constant while varying how lessons are delivered.

**Four competency domains:** Understand AI, Use AI, Evaluate AI, Construct with AI.
**Five learner stages:** Curious, Careful, Critical, Creative, Connected (JSS 1 to SS 3).
**Four tiers:** paper, shared screen, offline computers, online lab.
**Six enabling conditions:** teacher training, infrastructure, curriculum, safeguarding, financing, evidence.
""")
st.dataframe(pd.DataFrame([{"Tier": v["name"], "Students see": v["sees"], "Students do": v["does"], "Students can prove": v["proves"]} for v in TIERS.values()]),
             use_container_width=True, hide_index=True)

st.markdown("### Limitations")
st.markdown("""
- The framework is built from literature and national data; it has **not yet been piloted** or validated in a controlled trial.
- Cost figures are planning estimates and are sensitive to inflation and local prices.
- Unplugged activities teach the logic of labelling, rules and error testing; they complement, not replace, digital practice where available.
- This toolkit is a planning aid. It is not legal, financial or medical advice.
""")
st.markdown("### Privacy")
st.write("The app does not collect or store personal data. Entries live only in your browser session and are lost when you close the tab. Download your results to keep them.")
st.markdown("### Key references")
for r in REFERENCES:
    st.markdown(f"- {r}")
st.markdown("### Cite this tool")
st.code("[Author]. (2026). AISS Toolkit: AI Implementation Framework for Nigerian Secondary Schools [Web application]. https://github.com/<your-username>/aiss-toolkit", language=None)
st.caption("Please verify all references against the original sources before formal citation.")
