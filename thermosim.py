# thermosim.py

import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP
import numpy as np

def simulate_rankine(P_high, P_low, T_high, fluid):
    # 1 -> Pump (isentropic compression)
    h1 = CP.PropsSI('H', 'P', P_low, 'Q', 0, fluid)
    s1 = CP.PropsSI('S', 'P', P_low, 'Q', 0, fluid)

    h2s = CP.PropsSI('H', 'P', P_high, 'S', s1, fluid)
    work_pump = h2s - h1

    # 2 -> Boiler (isobaric heating)
    h3 = CP.PropsSI('H', 'P', P_high, 'T', T_high, fluid)
    heat_added = h3 - h2s

    # 3 -> Turbine (isentropic expansion)
    s3 = CP.PropsSI('S', 'P', P_high, 'T', T_high, fluid)
    h4s = CP.PropsSI('H', 'P', P_low, 'S', s3, fluid)
    work_turbine = h3 - h4s

    net_work = work_turbine - work_pump
    efficiency = net_work / heat_added

    # Generate T-s Diagram
    T_vals = np.linspace(300, T_high, 100)
    s_vals = [CP.PropsSI('S', 'P', P_high, 'T', T, fluid) for T in T_vals]
    fig_ts, ax1 = plt.subplots()
    ax1.plot(s_vals, T_vals, label="Boiler Curve")
    ax1.set_xlabel("Entropy (J/kg·K)")
    ax1.set_ylabel("Temperature (K)")
    ax1.set_title("T-s Diagram")
    ax1.grid(True)

    # Generate P-v Diagram
    v_vals = [1 / CP.PropsSI('D', 'P', P_high, 'T', T, fluid) for T in T_vals]
    fig_pv, ax2 = plt.subplots()
    ax2.plot(v_vals, [P_high] * len(v_vals), label="Boiler Pressure Line")
    ax2.set_xlabel("Specific Volume (m³/kg)")
    ax2.set_ylabel("Pressure (Pa)")
    ax2.set_title("P-v Diagram")
    ax2.grid(True)

    return {
        "work_pump": work_pump,
        "work_turbine": work_turbine,
        "heat_added": heat_added,
        "net_work": net_work,
        "efficiency": efficiency,
        "ts_plot": fig_ts,
        "pv_plot": fig_pv
    }
