# Directory Structure
# emeraldthermosim-v3/
# ├── app.py
# ├── thermosim.py
# ├── saf_logic.py
# ├── diagram_renderer.py
# ├── utils.py
# └── presets/
#     ├── default_rankine.json
#     └── edited_rankine.json

# -------------------------- app.py --------------------------
import streamlit as st
from thermosim import simulate_rankine
from saf_logic import SAFSystem
from diagram_renderer import render_diagram
from utils import load_preset

st.set_page_config(page_title="EmeraldThermoSim v3", layout="wide")

mode = st.sidebar.radio("Select Mode", ["🧪 Classic Simulator", "⚙️ SAF Mode", "📊 Compare Models"])

if mode == "🧪 Classic Simulator":
    st.title("Classic Rankine Cycle Simulator")
    with st.form("input_form"):
        P_high = st.number_input("High Pressure [Pa]", value=8e6, format="%.0f")
        P_low = st.number_input("Low Pressure [Pa]", value=1e5, format="%.0f")
        T_high = st.number_input("High Temperature [K]", value=773.15, format="%.2f")
        fluid = st.selectbox("Working Fluid", ["Water", "R134a"])
        submitted = st.form_submit_button("Run Simulation")

    if submitted:
        results = simulate_rankine(P_high, P_low, T_high, fluid)
        st.success("Simulation complete!")
        st.json({k: v for k, v in results.items() if not k.endswith("_plot")})
        st.pyplot(results["ts_plot"])
        st.pyplot(results["pv_plot"])

elif mode == "⚙️ SAF Mode":
    st.title("SAF Intelligent Editing")
    st.markdown("Visual model builder with live updates.")

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
    st.json({k: v for k, v in output.items() if not k.endswith("_plot")})
    st.pyplot(output["ts_plot"])
    st.pyplot(output["pv_plot"])

elif mode == "📊 Compare Models":
    st.title("Compare Saved Designs")
    m1 = load_preset("presets/default_rankine.json")
    m2 = load_preset("presets/edited_rankine.json")
    diff = SAFSystem.compare_models(m1, m2)
    st.json(diff)


# ----------------------- thermosim.py -----------------------
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
    ax1.set_title("T-s Diagram Placeholder")
    ax1.plot([s1, s3], [h1, h3])

    fig2, ax2 = plt.subplots()
    ax2.set_title("P-v Diagram Placeholder")
    ax2.plot([P_low, P_high], [h1, h3])

    return {
        "work_pump": work_pump,
        "heat_added": heat_added,
        "work_turbine": work_turbine,
        "net_work": net_work,
        "efficiency": efficiency,
        "ts_plot": fig1,
        "pv_plot": fig2
    }


# ---------------------- saf_logic.py ----------------------
import json
from thermosim import simulate_rankine

class SAFSystem:
    def __init__(self, components):
        self.components = components

    def list_components(self):
        return list(self.components.keys())

    def get_component_params(self, name):
        return self.components.get(name, {})

    def update_component(self, name, new_values):
        self.components[name].update(new_values)

    def run_simulation(self):
        return simulate_rankine(
            self.components['pump']['P_high'],
            self.components['pump']['P_low'],
            self.components['boiler']['T_high'],
            self.components['fluid']['type']
        )

    @staticmethod
    def load_preset(path):
        with open(path, 'r') as f:
            data = json.load(f)
        return SAFSystem(data)

    @staticmethod
    def compare_models(model1, model2):
        diffs = {}
        for k in model1.components:
            diffs[k] = {}
            for p in model1.components[k]:
                v1 = model1.components[k][p]
                v2 = model2.components[k][p]
                if v1 != v2:
                    diffs[k][p] = {"old": v1, "new": v2}
        return diffs


# ------------------ diagram_renderer.py ------------------
def render_diagram(model):
    dot = "digraph G {\n"
    for name, params in model.components.items():
        label = f"{name}\n" + "\\n".join([f"{k}: {v}" for k, v in params.items()])
        dot += f'  {name} [label="{label}"]\n'
    dot += "  pump -> boiler -> turbine -> condenser -> pump\n"
    dot += "}"
    return dot


# ------------------------ utils.py ------------------------
import json
from saf_logic import SAFSystem

def load_preset(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return SAFSystem(data)


# -------------------- presets/default_rankine.json --------------------
{
  "pump": {
    "P_low": 100000,
    "P_high": 8000000
  },
  "boiler": {
    "T_high": 773.15
  },
  "turbine": {},
  "condenser": {},
  "fluid": {
    "type": "Water"
  }
}


# -------------------- presets/edited_rankine.json --------------------
{
  "pump": {
    "P_low": 120000,
    "P_high": 8500000
  },
  "boiler": {
    "T_high": 823.15
  },
  "turbine": {},
  "condenser": {},
  "fluid": {
    "type": "Water"
  }
}


