# (Convert ideas → executable rules)
# What this does
# Turns human-readable ideas into:
# Config overrides
# Simulation rules

class RuleCompiler:
    def compile(self, hypothesis):
        name = hypothesis["change"].lower()

        if "auto" in name or "rush" in name:
            action = "AUTO_APPROVAL"
        elif "route" in name or "resource" in name:
            action = "DYNAMIC_ROUTING"
        elif "escalat" in name:
            action = "ESCALATION_CONTROL"
        else:
            action = "NO_OP"

        return {
            "rule_name": action,
            "description": hypothesis["description"],
            "apply_if": hypothesis["condition"]
        }
