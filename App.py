# thermosim.py

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

    # Placeholder plots for T-s and P-v
    ax1.set_title("T-s Diagram")
    ax1.set_xlabel("Entropy (s)")
    ax1.set_ylabel("Temperature (T)")
    ax1.plot(
        [s1, s1, s3, s3],
        [
            CP.PropsSI('T','P',P_low,'Q',0,fluid),
            CP.PropsSI('T','P',P_high,'S',s1,fluid),
            T_high,
            CP.PropsSI('T','P',P_low,'S',s3,fluid)
        ],
        marker='o'
    )

    ax2.set_title("P-v Diagram")
    ax2.set_xlabel("Specific Volume (v)")
    ax2.set_ylabel("Pressure (P)")
    v1 = CP.PropsSI('D', 'P', P_low, 'Q', 0, fluid)
    v2 = CP.PropsSI('D', 'P', P_high, 'S', s1, fluid)
    v3 = CP.PropsSI('D', 'P', P_high, 'T', T_high, fluid)
    v4 = CP.PropsSI('D', 'P', P_low, 'S', s3, fluid)
    ax2.plot([1/v1, 1/v2, 1/v3, 1/v4], [P_low, P_high, P_high, P_low], marker='o')

    return {
        "work_pump": work_pump,
        "heat_added": heat_added,
        "work_turbine": work_turbine,
        "net_work": net_work,
        "efficiency": efficiency,
        "ts_plot": fig1,
        "pv_plot": fig2
    }


# saf_logic.py

class SAFSystem:
    def __init__(self, model):
        self.original_model = model
        self.components = self._decompose(model)

    def _decompose(self, model):
        # Simulate breakdown into subcomponents (simplified)
        return {
            "Pump Efficiency": 0.85,
            "Turbine Efficiency": 0.9,
            "Heat Exchanger Effectiveness": 0.95
        }

    def modify_component(self, component, new_value):
        if component in self.components:
            self.components[component] = new_value

    def reconstruct_model(self):
        # Simulate reconstruction (simplified summary)
        return f"Model updated with: {self.components}"

    def compare_to_original(self):
        changes = []
        for key in self.components:
            if self.components[key] != self._decompose(self.original_model)[key]:
                changes.append(f"{key} changed to {self.components[key]}")
        return changes



