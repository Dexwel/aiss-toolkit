import pandas as pd
import streamlit as st
from aiss import ui, logic
from aiss.data import PORTFOLIO_ITEMS

ui.setup("Portfolio & Consent", "📁")
st.title("📁 Portfolio Tracker and Parental Consent")
tab1, tab2 = st.tabs(["Portfolio tracker", "Consent letter generator"])

with tab1:
    st.write("Each student keeps six items. Tick them off as they are completed.")
    start = pd.DataFrame({"Student": ["", "", ""], **{i: [False] * 3 for i in PORTFOLIO_ITEMS}})
    df = st.data_editor(start, num_rows="dynamic", use_container_width=True, hide_index=True, key="portfolio_editor")
    df = df[df["Student"].astype(str).str.strip() != ""]
    if len(df):
        for col in PORTFOLIO_ITEMS:
            df[col] = df[col].fillna(False).astype(bool)
        done, pct = logic.portfolio_completion(df, PORTFOLIO_ITEMS)
        st.session_state["portfolio_stats"] = (done, len(df))
        c1, c2 = st.columns(2)
        c1.metric("Complete portfolios", f"{done} of {len(df)}")
        c2.metric("Completion rate", f"{pct:.0f}%")
        st.progress(min(pct / 100, 1.0))
        st.download_button("Download tracker (CSV)", ui.csv_bytes(df), file_name="aiss_portfolios.csv", mime="text/csv")
    else:
        st.info("Add student names to see completion.")

with tab2:
    st.write("Obtain documented parental or guardian consent before any learner uses an online AI tool "
             "(Nigeria Data Protection Act, 2023). Edit the letter to suit your school and have it checked locally.")
    school = st.text_input("School name", value=st.session_state.get("audit_school", ""))
    principal = st.text_input("Principal name")
    contact = st.text_input("Contact (phone or email)")
    online = st.checkbox("This term includes free online AI tools", value=False)
    letter = logic.consent_letter(school, principal, contact, online)
    st.text_area("Preview (editable)", letter, height=380)
    st.download_button("Download letter (.txt)", letter, file_name="aiss_consent_letter.txt", mime="text/plain")
    st.caption("Template only; not legal advice. Tools that run locally in the browser are preferable to ones that send a minor's data to external servers.")
