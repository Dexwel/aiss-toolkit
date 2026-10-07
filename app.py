import streamlit as st
from aiss import ui
from aiss.data import STAGES

ui.setup("Home", "🎓")

st.title("🎓 AISS Toolkit")
st.subheader("AI Implementation Framework for Nigerian Secondary Schools")
st.write(
    "A practical toolkit for teachers, principals and education officials to plan, teach, assess and cost "
    "**AI education in any school**, whether it has a computer lab or only a chalkboard. "
    "The core idea: **every student learns the same AI skills; only the way lessons are delivered changes.**"
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Competency domains", 4, help="Understand, Use, Evaluate, Construct")
c2.metric("Learner stages", 5, help="JSS 1 to SS 3")
c3.metric("Delivery tiers", 4, help="Tier 0 (paper) to Tier 3 (online lab)")
c4.metric("Enabling conditions", 6)

st.divider()
st.markdown("### Start here")
a, b, c = st.columns(3)
with a:
    st.markdown("**1. Find your tier**")
    st.caption("Audit your school's power, devices, internet and staffing in about 30 minutes.")
    st.page_link("pages/1_School_Audit.py", label="Open School Audit", icon="🏫")
with b:
    st.markdown("**2. Plan and teach**")
    st.caption("Get the 12-week sequence matched to your tier, with unplugged lesson ideas.")
    st.page_link("pages/2_Curriculum_Planner.py", label="Open Curriculum Planner", icon="📅")
with c:
    st.markdown("**3. Budget**")
    st.caption("Compare costs across tiers and see what your budget can start today.")
    st.page_link("pages/3_Cost_Calculator.py", label="Open Cost Calculator", icon="💰")
d, e, f = st.columns(3)
with d:
    st.markdown("**4. Measure learning**")
    st.caption("Analyse baseline and endline scores and check who is joining the club.")
    st.page_link("pages/4_Assessment_Analyzer.py", label="Open Assessment Analyzer", icon="📝")
with e:
    st.markdown("**5. Mark projects and portfolios**")
    st.caption("Score projects with the rubric, track portfolios and print a consent letter.")
    st.page_link("pages/5_Project_Rubric.py", label="Open Project Rubric", icon="🎯")
with f:
    st.markdown("**6. Monitor the programme**")
    st.caption("Check five indicators to see whether the programme is working.")
    st.page_link("pages/7_ME_Dashboard.py", label="Open M&E Dashboard", icon="📈")

st.divider()
st.markdown("### The framework at a glance")
tabs = st.tabs(["Overview", "Learner progression", "Competency map", "Tiers", "Tier decision", "Assessment cycle", "Pathways", "Governance"])
with tabs[0]:
    ui.show_image("fig1_framework_overview.jpg", "Four domains define outcomes; six conditions are system inputs; four tiers are for delivery, not outcomes.")
with tabs[1]:
    ui.show_image("fig2_progression.jpg", "Five-stage progression from JSS 1 to SS 3.")
    for name, level, text in STAGES:
        st.markdown(f"**{name}** ({level}): {text}")
with tabs[2]:
    ui.show_image("fig3_competency_map.jpg", "Can-do statements by domain and level. 'Question AI' is the same domain as Evaluate AI.")
with tabs[3]:
    ui.show_image("fig4_tiers.jpg", "What students see, do and can prove at each tier.")
with tabs[4]:
    ui.show_image("fig5_tier_decision.jpg", "Power, then computers, then internet decide the tier. Re-check every term.")
with tabs[5]:
    ui.show_image("fig6_assessment_cycle.jpg", "Baseline quiz, 12-week club, project, portfolio folder, endline quiz.")
with tabs[6]:
    ui.show_image("fig7_pathways.jpg", "Post-school pathways and the civic case for universal AI literacy.")
with tabs[7]:
    ui.show_image("fig8_governance.jpg", "National, state, school and home roles; name a real person for each role.")

st.divider()
st.caption(ui.DISCLAIMER)
