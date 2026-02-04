# (Baseline KPIs)
# Metrics we compute
# Cycle time per ticket
# Cost per ticket
# SLA violations
# These metrics define “current performance”.


class MetricsEngine:
    def __init__(self, traces, sla_rules):
        self.traces = traces
        self.sla_rules = sla_rules

    def compute(self):
        total_cycle_time = []
        total_cost = []
        sla_violations = 0

        for events in self.traces.values():
            cycle_time = sum(e["duration"] for e in events)
            cost = sum(e["cost"] for e in events)

            total_cycle_time.append(cycle_time)
            total_cost.append(cost)

            if cycle_time > self.sla_rules["priority_levels"]["medium"]["max_resolution_minutes"]:
                sla_violations += 1

        return {
            "avg_cycle_time": sum(total_cycle_time) / len(total_cycle_time),
            "avg_cost": sum(total_cost) / len(total_cost),
            "sla_violation_rate": sla_violations / len(self.traces)
        }

