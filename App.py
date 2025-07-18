# App.py

import streamlit as st
from thermosim import simulate_rankine
from saf_logic import SAFSystem

st.set_page_config(page_title="EmeraldThermoSim V3", layout="wide")
st.title("💠 EmeraldThermoSim v3")
st.markdown("""
A powerful thermodynamic simulator + SAF editor for Rankine Cycle.
""")

# Sidebar inputs
st.sidebar.header("Rankine Cycle Inputs")
P_high = st.sidebar.number_input("Boiler Pressure (Pa)", value=8e6)
P_low = st.sidebar.number_input("Condenser Pressure (Pa)", value=1e5)
T_high = st.sidebar.number_input("Turbine Inlet Temperature (K)", value=773.15)
fluid = st.sidebar.selectbox("Working Fluid", ["Water", "R134a", "Ammonia"], index=0)

# Run Simulation
if st.sidebar.button("Run Simulation"):
    results = simulate_rankine(P_high, P_low, T_high, fluid)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Performance Metrics")
        st.write(f"Pump Work: {results['work_pump']:.2f} J/kg")
        st.write(f"Turbine Work: {results['work_turbine']:.2f} J/kg")
        st.write(f"Heat Added: {results['heat_added']:.2f} J/kg")
        st.write(f"Net Work: {results['net_work']:.2f} J/kg")
        st.write(f"Thermal Efficiency: {results['efficiency']*100:.2f}%")

    with col2:
        st.subheader("T-s Diagram")
        st.pyplot(results['ts_plot'])
        st.subheader("P-v Diagram")
        st.pyplot(results['pv_plot'])

# SAF Environment
st.markdown("---")
st.header("🔧 Systematic Architect Functionality (SAF)")
user_model = st.text_input("Enter model name or version (for simulation reference):", "Basic Rankine Model")

saf = SAFSystem(user_model)

st.subheader("Core Components")
new_values = {}
for component, value in saf.components.items():
    new_val = st.slider(f"{component}", min_value=0.0, max_value=1.0, value=float(value), step=0.01)
    saf.modify_component(component, new_val)
    new_values[component] = new_val

if st.button("Update Model"):
    updated_model = saf.reconstruct_model()
    comparison = saf.compare_to_original()
    st.success(updated_model)
    if comparison:
        st.info("\n".join(comparison))
    else:
        st.info("No changes detected.")

st.markdown("""
---
**Developed by EmeraldKing 🧪🔬**  
Built using Python, Streamlit, and CoolProp
""")




