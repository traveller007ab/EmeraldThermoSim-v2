# saf_logic.py

class SAFSystem:
    def __init__(self, model_name):
        self.model_name = model_name
        self.components = {
            "Turbine Efficiency": 0.85,
            "Pump Efficiency": 0.75,
            "Heat Exchanger Effectiveness": 0.90
        }
        self.original = self.components.copy()

    def modify_component(self, name, new_value):
        self.components[name] = new_value

    def reconstruct_model(self):
        return f"Model '{self.model_name}' updated with: {self.components}"

    def compare_to_original(self):
        changes = []
        for key in self.components:
            old = self.original[key]
            new = self.components[key]
            if old != new:
                changes.append(f"{key}: {old:.2f} → {new:.2f}")
        return changes
