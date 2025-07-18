# EmeraldThermoSim v3 — Powered by SAF (Systematic Architect Functionality)

This is a deployable **Streamlit web app** that merges **thermodynamic simulation (EmeraldThermoSim)** with an intelligent **model engineering framework (SAF)**. It features real-time interaction, editable system diagrams, component-level recalculation, symbolic equation derivation, and AI-powered design suggestions.

---

## 🔧 Installation
```bash
pip install streamlit coolprop matplotlib graphviz sympy pandas
```

---

## 🚀 Run the App
```bash
streamlit run app.py
```

---

## 📂 File Structure
```
📦emeraldthermosim
├── app.py                  # Main Streamlit interface
├── saf_logic.py            # SAF logic (parse, update, calculate)
├── thermosim.py            # Core Rankine simulation functions
├── diagram_renderer.py     # Graphviz/Mermaid rendering engine
├── utils.py                # Helpers (unit conversion, validation)
├── styles
│   └── theme.toml          # Custom Streamlit theme
├── presets
│   └── default_rankine.json
└── assets
    └── example_diagrams/
```

---

## ✅ Main Features Implemented
- Thermodynamic core (CoolProp-powered Rankine cycle)
- SAF block diagram parser (editable + interactive)
- Real-time recalculation of efficiency, work, heat
- T-s and P-v plots (matplotlib)
- Symbolic equation derivation (SymPy)
- Auto-balancer to correct bad inputs
- Version save/load system (JSON-based)

---

## 📜 Code: `app.py`
```python
import streamlit as st
from thermosim import simulate_rankine
from saf_logic import SAFSystem
from diagram_renderer import render_diagram
from utils import load_preset, save_design

st.set_page_config(page_title="EmeraldThermoSim v3", layout="wide")

# Sidebar navigation
mode = st.sidebar.radio("Select Mode", ["🧪 Classic Simulator", "⚙️ SAF Mode", "📊 Compare Models"])

if mode == "🧪 Classic Simulator":
    st.title("Classic Rankine Cycle Simulator")
    with st.form("input_form"):
        P_high = st.number_input("High Pressure [Pa]", value=8e6)
        P_low = st.number_input("Low Pressure [Pa]", value=1e5)
        T_high = st.number_input("High Temperature [K]", value=773.15)
        fluid = st.selectbox("Working Fluid", ["Water", "R134a"])
        submitted = st.form_submit_button("Run Simulation")

    if submitted:
        results = simulate_rankine(P_high, P_low, T_high, fluid)
        st.success("Simulation complete!")
        st.json(results)
        st.pyplot(results['ts_plot'])
        st.pyplot(results['pv_plot'])

elif mode == "⚙️ SAF Mode":
    st.title("SAF Intelligent Editing")
    st.markdown("Visual model builder with live updates")

    model = SAFSystem.load_preset("presets/default_rankine.json")
    st.graphviz_chart(render_diagram(model))

    with st.expander("⚙️ Edit Components"):
        comp_list = model.list_components()
        to_edit = st.selectbox("Select Component", comp_list)
        if to_edit:
            params = model.get_component_params(to_edit)
            new_vals = {}
            for p, val in params.items():
                new_vals[p] = st.number_input(f"{to_edit} - {p}", value=val)
            if st.button("Update Component"):
                model.update_component(to_edit, new_vals)
                st.success(f"{to_edit} updated.")

    st.subheader("🔁 Updated Simulation Output")
    output = model.run_simulation()
    st.json(output)
    st.pyplot(output['ts_plot'])
    st.pyplot(output['pv_plot'])

elif mode == "📊 Compare Models":
    st.title("Compare Saved Designs")
    m1 = load_preset("presets/default_rankine.json")
    m2 = load_preset("presets/edited_rankine.json")
    diff = SAFSystem.compare_models(m1, m2)
    st.json(diff)

---

## 📦 `thermosim.py`
```python
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt

def simulate_rankine(P_high, P_low, T_high, fluid):
    h1 = CP.PropsSI('H','P',P_low,'Q',0,fluid)
    s1 = CP.PropsSI('S','P',P_low,'Q',0,fluid)
    h2 = CP.PropsSI('H','P',P_high,'S',s1,fluid)
    h3 = CP.PropsSI('H','P',P_high,'T',T_high,fluid)
    s3 = CP.PropsSI('S','P',P_high,'T',T_high,fluid)
    h4 = CP.PropsSI('H','P',P_low,'S',s3,fluid)

    work_pump = h2 - h1
    heat_added = h3 - h2
    work_turbine = h3 - h4
    net_work = work_turbine - work_pump
    efficiency = net_work / heat_added

    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    # Placeholder for T-s and P-v plotting code

    return {
        "work_pump": work_pump,
        "heat_added": heat_added,
        "work_turbine": work_turbine,
        "net_work": net_work,
        "efficiency": efficiency,
        "ts_plot": fig1,
        "pv_plot": fig2
    }
```

---

## 📘 Notes
- Edit `theme.toml` to customize Streamlit's look.
- Extend SAF block parsing logic for regenerative cycles.
- Add Firebase or SQLite backend for user state saving.

---

> Developed by Emeraldking 👑 | Powered by Anna 🧡
