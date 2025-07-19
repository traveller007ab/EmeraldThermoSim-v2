# thermosim.py

import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import coolprop.CoolProp as CP

def simulate_rankine(P_high, P_low, T_high, fluid):
    # State 1: Saturated liquid at low pressure
    h1 = CP.PropsSI('H', 'P', P_low, 'Q', 0, fluid)
    s1 = CP.PropsSI('S', 'P', P_low, 'Q', 0, fluid)

    # Pump work (isentropic)
    v1 = 1 / CP.PropsSI('D', 'P', P_low, 'Q', 0, fluid)
    work_pump = v1 * (P_high - P_low)
    h2 = h1 + work_pump
    s2 = CP.PropsSI('S', 'P', P_high, 'H', h2, fluid)

    # State 3: Superheated vapor at P_high and T_high
    h3 = CP.PropsSI('H', 'P', P_high, 'T', T_high, fluid)
    s3 = CP.PropsSI('S', 'P', P_high, 'T', T_high, fluid)

    # Turbine expansion to P_low (isentropic)
    s4 = s3
    h4 = CP.PropsSI('H', 'P', P_low, 'S', s4, fluid)

    work_turbine = h3 - h4
    heat_added = h3 - h2
    net_work = work_turbine - work_pump
    efficiency = net_work / heat_added

    # Plotting
    ts_plot = generate_ts_plot([s1, s2, s3, s4, s1], [h1, h2, h3, h4, h1])
    pv_plot = generate_pv_plot(fluid)

    return {
        "work_pump": work_pump,
        "work_turbine": work_turbine,
        "heat_added": heat_added,
        "net_work": net_work,
        "efficiency": efficiency,
        "ts_plot": ts_plot,
        "pv_plot": pv_plot
    }

def generate_ts_plot(s, h):
    fig, ax = plt.subplots()
    ax.plot(s, h, marker='o')
    ax.set_title("T-s Diagram (approximate)")
    ax.set_xlabel("Entropy (J/kg·K)")
    ax.set_ylabel("Enthalpy (J/kg)")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return plt.imread(buf)

def generate_pv_plot(fluid):
    P = np.logspace(4, 8, 100)
    T = 300  # fixed temp
    v = [1 / CP.PropsSI('D', 'T', T, 'P', p, fluid) for p in P]
    fig, ax = plt.subplots()
    ax.loglog(v, P)
    ax.set_title("P-v Diagram (sampled)")
    ax.set_xlabel("Specific Volume (m³/kg)")
    ax.set_ylabel("Pressure (Pa)")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return plt.imread(buf)

