import streamlit as st
from aiss import ui, logic
from aiss.data import AUDIT_ITEMS, MAX_AUDIT_SCORE, TIERS, TIER_ACTIONS

ui.setup("School Audit", "🏫")
st.title("🏫 School Audit and Tier Assignment")
st.write("Answer from physical inspection, not from reports. Takes about 30 minutes. "
         "The result gives your **planning tier** and the first actions to take.")

with st.form("audit"):
    school = st.text_input("School name (optional)")
    st.markdown("#### Quick triage (Figure 5)")
    t1, t2, t3 = st.columns(3)
    power = t1.toggle("Reliable power", value=False)
    computers = t2.toggle("Working computers for students", value=False)
    internet = t3.toggle("Internet access", value=False)
    st.markdown("#### Detailed audit (Appendix A, 10 items)")
    choices = {}
    for iid, question, options in AUDIT_ITEMS:
        labels = [o[0] for o in options]
        choices[iid] = st.radio(f"{iid}. {question}", labels, horizontal=True, index=len(labels) - 1, key=f"q{iid}")
    submitted = st.form_submit_button("Calculate my tier", type="primary")

if submitted:
    answers, answers_text = {}, []
    for iid, question, options in AUDIT_ITEMS:
        pts = dict(options)[choices[iid]]
        answers[iid] = pts
        answers_text.append((question, choices[iid], pts))
    score = logic.audit_score(answers)
    score_tier = logic.tier_from_score(score)
    triage = logic.triage_tier(power, computers, internet)
    plan = logic.planning_tier(score_tier, triage)
    flags = logic.audit_flags(answers, plan)
    st.session_state["plan_tier"] = plan
    st.session_state["audit_school"] = school

    st.success(f"Recommended planning tier: **{TIERS[plan]['name']}**")
    m1, m2, m3 = st.columns(3)
    m1.metric("Audit score", f"{score} / {MAX_AUDIT_SCORE}")
    m2.metric("Score-based tier", score_tier)
    m3.metric("Quick triage tier", triage)
    st.caption("The planning tier is the lower of the two methods, so you start with what your school can sustain.")

    if flags:
        st.markdown("#### Readiness flags")
        for f in flags:
            st.warning(f)
    st.markdown("#### Recommended next actions")
    for a in TIER_ACTIONS[plan]:
        st.markdown(f"- {a}")
    if plan == 0:
        st.info("Learning on paper is not less. Tier 0 students build the same core AI skills with different tools.")
    report = logic.audit_report_md(school, score, score_tier, triage, plan, answers_text, flags, TIER_ACTIONS[plan])
    st.download_button("Download report (Markdown)", report, file_name="aiss_audit_report.md", mime="text/markdown")
    st.page_link("pages/2_Curriculum_Planner.py", label="Next: open the Curriculum Planner", icon="📅")
