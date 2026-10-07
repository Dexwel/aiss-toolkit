import pandas as pd
import streamlit as st
from aiss import ui, logic
from aiss.data import TIERS

ui.setup("Cost Calculator", "💰")
st.title("💰 Cost Calculator")
st.write("Planning estimates in Nigerian Naira. **Edit any value** to match local prices; defaults come from the AISS paper.")

base = pd.DataFrame({
    "Tier": [TIERS[t]["name"] for t in TIERS],
    "Setup": [TIERS[t]["setup"] for t in TIERS],
    "Running": [TIERS[t]["running"] for t in TIERS],
    "Students": [TIERS[t]["students"] for t in TIERS],
})
edited = st.data_editor(base, use_container_width=True, hide_index=True, disabled=["Tier"],
                        column_config={"Setup": st.column_config.NumberColumn("Setup cost (₦)", min_value=0, step=1000),
                                       "Running": st.column_config.NumberColumn("Yearly running cost (₦)", min_value=0, step=1000),
                                       "Students": st.column_config.NumberColumn("Students per year", min_value=1, step=1)})
c1, c2 = st.columns(2)
years = c1.slider("Planning horizon (years)", 1, 5, 3)
infl = c2.slider("Annual cost inflation (%)", 0, 40, 0) / 100
res = logic.cost_table(edited, years, infl)

view = pd.DataFrame({
    "Tier": res["Tier"],
    "Cost per student per year": res["Cost per student per year"].map(ui.naira),
    f"Total over {years} yr": res["Total over horizon"].map(ui.naira),
    f"Cost per student over {years} yr": res["Cost per student over horizon"].map(ui.naira),
})
st.dataframe(view, use_container_width=True, hide_index=True)
st.caption("Horizon total = setup + yearly running cost for each year (with inflation applied to running costs). "
           "Cost per student per year = yearly running cost / students served.")
st.bar_chart(res.set_index("Tier")["Cost per student per year"])

st.markdown("#### What can my budget start today?")
budget = st.number_input("Available setup budget (₦)", min_value=0, value=300_000, step=50_000)
afford = [r["Tier"] for _, r in res.iterrows() if r["Setup"] <= budget]
if afford:
    st.success("Affordable to start: " + ", ".join(afford))
    st.caption("Infrastructure follows a fixed order: power, devices, a securable room, then connectivity. "
               "Do not start without agreed funding for Years 2 and 3.")
else:
    st.warning("Your budget does not cover setup for any tier. Seek SUBEB/UBEC grants, PTA or alumni support.")
st.download_button("Download cost table (CSV)", ui.csv_bytes(res), file_name="aiss_costs.csv", mime="text/csv")
