# (Measure improvements)
# What this does
# Compares:
# Cycle time
# Cost
# SLA violations
# Before vs After.


class ImpactAnalyzer:
    def __init__(self, baseline, experimental, sla_limit=480):
        self.baseline = baseline
        self.experimental = experimental
        self.sla_limit = sla_limit

    def analyze(self):
        def metrics(traces):
            total_time = []
            total_cost = []
            sla_violations = 0

            for trace in traces.values():
                cycle_time = sum(e["duration"] for e in trace)
                cost = sum(e["cost"] for e in trace)

                total_time.append(cycle_time)
                total_cost.append(cost)

                if cycle_time > self.sla_limit:
                    sla_violations += 1

            return {
                "avg_cycle_time": sum(total_time) / len(total_time),
                "avg_cost": sum(total_cost) / len(total_cost),
                "sla_violation_rate": sla_violations / len(traces)
            }

        baseline_metrics = metrics(self.baseline)
        experimental_metrics = metrics(self.experimental)

        delta = {
            k: experimental_metrics[k] - baseline_metrics[k]
            for k in baseline_metrics
        }

        return baseline_metrics, experimental_metrics, delta
