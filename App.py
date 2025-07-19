import streamlit as st
from graphviz import Digraph
from sympy import symbols, Eq, solve
from CoolProp.CoolProp import PropsSI
import matplotlib.pyplot as plt
import numpy as np
import json

st.set_page_config(layout="wide", page_title="EmeraldThermoSim V2 + SAF", page_icon="🔥")

# Custom CSS for modern professional styling
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #1f2937;
        }
        .stButton>button {
            color: white;
            background-color: #10b981;
            border-radius: 0.5rem;
            padding: 0.6rem 1.2rem;
            font-weight: bold;
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #059669;
        }
        .stTextArea textarea {
            background-color: #f9fafb;
            border-radius: 0.5rem;
        }
        .stExpanderHeader {
            font-weight: bold;
            color: #2563eb;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------
# SAF Core Utilities
# ----------------------------------

class SAFCore:
    def __init__(self):
        self.original_model = {}
        self.modified_model = {}

    def load_model(self, data):
        self.original_model = data
        self.modified_model = json.loads(json.dumps(data))  # deep copy

    def edit_component(self, comp_id, param, new_value):
        if comp_id in self.modified_model['components']:
            self.modified_model['components'][comp_id]['params'][param] = new_value

    def compare_models(self):
        diffs = {}
        for cid in self.original_model['components']:
            orig = self.original_model['components'][cid]['params']
            mod = self.modified_model['components'][cid]['params']
            diffs[cid] = {k: (orig[k], mod[k]) for k in orig if orig[k] != mod[k]}
        return diffs

    def save_model(self):
        return json.dumps(self.modified_model, indent=2)

    def load_saved_model(self, data):
        self.modified_model = json.loads(data)

saf = SAFCore()

# ----------------------------------
# Example Rankine + R134a Model
# ----------------------------------

def get_rankine_r134a_model():
    return {
        "fluid": "R134a",
        "components": {
            "pump": {"type": "pump", "params": {"inlet_pressure": 20000, "outlet_pressure": 800000, "efficiency": 0.85}},
            "boiler": {"type": "boiler", "params": {"inlet_temp": 300, "outlet_temp": 450}},
            "turbine": {"type": "turbine", "params": {"inlet_pressure": 800000, "outlet_pressure": 20000, "efficiency": 0.85}},
            "condenser": {"type": "condenser", "params": {"inlet_temp": 310, "outlet_temp": 290}},
        },
        "connections": [
            ("pump", "boiler"),
            ("boiler", "turbine"),
            ("turbine", "condenser"),
            ("condenser", "pump")
        ]
    }

# ----------------------------------
# Diagram Render
# ----------------------------------

def render_block_diagram(model):
    dot = Digraph()
    for cid, comp in model['components'].items():
        label = f"{cid}\n({comp['type']})"
        dot.node(cid, label, style="filled", fillcolor="#c7d2fe", shape="box", fontname="Segoe UI")
    for src, dst in model['connections']:
        dot.edge(src, dst)
    st.graphviz_chart(dot)

# ----------------------------------
# Interactive Editor
# ----------------------------------

def component_editor():
    for cid, comp in saf.modified_model['components'].items():
        with st.expander(f"Edit {cid} ({comp['type']})"):
            for param, val in comp['params'].items():
                try:
                    new_val = st.number_input(f"{param} ({cid})", value=float(val), key=f"{cid}_{param}")
                    saf.edit_component(cid, param, new_val)
                except Exception as e:
                    st.warning(f"Could not edit {param}: {e}")

# ----------------------------------
# T-s and P-v Plotting (with error handling)
# ----------------------------------

def plot_diagrams(fluid):
    try:
        T = np.linspace(250, 500, 300)
        s, p, v = [], [], []
        for Ti in T:
            try:
                s_val = PropsSI('S','T',Ti,'Q',0.5,fluid)
                p_val = PropsSI('P','T',Ti,'Q',0.5,fluid)
                v_val = 1 / PropsSI('D','T',Ti,'Q',0.5,fluid)
                s.append(s_val)
                p.append(p_val)
                v.append(v_val)
            except:
                continue

        col1, col2 = st.columns(2)
        with col1:
            fig1, ax1 = plt.subplots()
            ax1.plot(s, T, color="#3b82f6")
            ax1.set_title('T-s Diagram')
            ax1.set_xlabel('Entropy [J/kg-K]')
            ax1.set_ylabel('Temperature [K]')
            st.pyplot(fig1)

        with col2:
            fig2, ax2 = plt.subplots()
            ax2.plot(v, p, color="#6366f1")
            ax2.set_title('P-v Diagram')
            ax2.set_xlabel('Volume [m^3/kg]')
            ax2.set_ylabel('Pressure [Pa]')
            st.pyplot(fig2)
    except Exception as e:
        st.error(f"Diagram generation failed: {e}")

# ----------------------------------
# Streamlit UI
# ----------------------------------

st.title("💎 EmeraldThermoSim V2 + SAF")

if "initialized" not in st.session_state:
    model = get_rankine_r134a_model()
    saf.load_model(model)
    st.session_state.initialized = True

st.subheader("📌 1. System Diagram")
render_block_diagram(saf.modified_model)

st.subheader("⚙️ 2. Component Parameters")
component_editor()

st.subheader("📊 3. Comparison Report")
if st.button("Compare Changes"):
    diffs = saf.compare_models()
    st.json(diffs)

st.subheader("🧊 4. Diagrams")
plot_diagrams(saf.modified_model['fluid'])

st.subheader("💾 5. Save / Load Model")
saved = st.text_area("📦 Saved JSON", value=saf.save_model())
if st.button("Load This JSON"):
    try:
        saf.load_saved_model(saved)
        st.success("Model reloaded.")
    except Exception as e:
        st.error(f"Failed to load model: {e}")





