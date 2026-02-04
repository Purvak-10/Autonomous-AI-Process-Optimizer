# (Replays workflows with new rules)
# What this does
# Takes original traces
# Applies rule-based modifications
# Simulates improved behavior
# We start simple and deterministic (important).

from copy import deepcopy

class DigitalTwin:
    def __init__(self, traces, rule):
        self.traces = traces
        self.action = rule["rule_name"]

    def apply_rules(self, trace):
        out = []

        for e in trace:
            ne = deepcopy(e)

            if self.action == "AUTO_APPROVAL" and e["step"] == "Approved":
                ne["duration"] = 5
                ne["cost"] = ne["duration"] * 1.1

            elif self.action == "DYNAMIC_ROUTING" and e["step"] == "In_Progress":
                ne["duration"] = e["duration"] * 0.6
                ne["cost"] = ne["duration"] * 1.0

            elif self.action == "ESCALATION_CONTROL" and e["step"] == "Escalated":
                ne["duration"] = e["duration"] * 0.7
                ne["cost"] = ne["duration"] * 1.0

            out.append(ne)

        return out

    def simulate(self):
        return {
            cid: self.apply_rules(trace)
            for cid, trace in self.traces.items()
        }
# Replays workflows with new rules
# Deterministic, trace-based simulation

from copy import deepcopy

class DigitalTwin:
    def __init__(self, traces, rule):
        self.traces = traces
        self.action = rule["rule_name"]
        self.threshold = rule.get("approval_threshold", None)

    def apply_rules(self, trace):
        out = []

        for e in trace:
            ne = deepcopy(e)

            # AUTO APPROVAL with threshold
            if self.action == "AUTO_APPROVAL" and e["step"] == "Approved":
                # ticket_value may be missing or None in some traces; default to a high
                # value so it won't be auto-approved unless explicitly below threshold.
                ticket_value = e.get("ticket_value") or 1000

                # Only compare when a threshold is provided (not None). If threshold is
                # None, the rule doesn't apply and we skip auto-approval.
                if self.threshold is not None and ticket_value <= self.threshold:
                    ne["duration"] = 5
                    ne["cost"] = round(ne["duration"] * 1.1, 2)

            # Dynamic routing
            elif self.action == "DYNAMIC_ROUTING" and e["step"] == "In_Progress":
                ne["duration"] = e["duration"] * 0.6
                ne["cost"] = ne["duration"] * 1.0

            # Escalation control
            elif self.action == "ESCALATION_CONTROL" and e["step"] == "Escalated":
                ne["duration"] = e["duration"] * 0.7
                ne["cost"] = ne["duration"] * 1.0

            out.append(ne)

        return out

    def simulate(self):
        return {
            cid: self.apply_rules(trace)
            for cid, trace in self.traces.items()
        }
