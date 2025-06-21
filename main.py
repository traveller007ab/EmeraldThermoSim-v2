
import streamlit as st
from CoolProp.CoolProp import PropsSI

st.set_page_config(page_title="EmeraldThermoSim v2", layout="centered")
st.title("🌿 EmeraldThermoSim v2.0")
st.markdown("Simulate a basic **Rankine Cycle** powered by CoolProp. Built for mechanical engineering students.")

st.header("🔧 Input Parameters")
col1, col2 = st.columns(2)

with col1:
    P_high = st.number_input("Boiler Pressure (bar)", min_value=1.0, value=80.0)
    T_boiler = st.number_input("Boiler Temperature (°C)", min_value=100.0, value=480.0)
    eta_turbine = st.slider("Turbine Efficiency (%)", min_value=10, max_value=100, value=85)

with col2:
    P_low = st.number_input("Condenser Pressure (bar)", min_value=0.01, value=0.1)
    T_condenser = st.number_input("Condenser Temperature (°C)", min_value=20.0, value=40.0)
    eta_pump = st.slider("Pump Efficiency (%)", min_value=10, max_value=100, value=90)

P1 = P_high * 1e5
P2 = P_low * 1e5

h1 = PropsSI("H", "P", P2, "Q", 0, "Water") / 1000
s1 = PropsSI("S", "P", P2, "Q", 0, "Water")
h2s = PropsSI("H", "P", P1, "S", s1, "Water") / 1000
h2 = h1 + (h2s - h1) / (eta_pump / 100)

T3_K = T_boiler + 273.15
h3 = PropsSI("H", "P", P1, "T", T3_K, "Water") / 1000
s3 = PropsSI("S", "P", P1, "T", T3_K, "Water")
h4s = PropsSI("H", "P", P2, "S", s3, "Water") / 1000
h4 = h3 - (h3 - h4s) * (eta_turbine / 100)

Wt = h3 - h4
Wp = h2 - h1
Wnet = Wt - Wp
Qin = h3 - h2
efficiency = (Wnet / Qin) * 100

st.header("📊 Simulation Results")
col3, col4 = st.columns(2)

with col3:
    st.metric("Turbine Work Output", f"{Wt:.2f} kJ/kg")
    st.metric("Pump Work Input", f"{Wp:.2f} kJ/kg")
    st.metric("Net Work Output", f"{Wnet:.2f} kJ/kg")

with col4:
    st.metric("Heat Supplied (Qin)", f"{Qin:.2f} kJ/kg")
    st.metric("Thermal Efficiency", f"{efficiency:.2f} %")

st.markdown("---")
st.caption("Built with ❤️ by Emeraldking | Powered by CoolProp & Streamlit")
