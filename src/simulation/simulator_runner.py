# (Runs one hypothesis)

from src.simulation.digital_twin import DigitalTwin
from src.simulation.impact_analyzer import ImpactAnalyzer

class SimulatorRunner:
    def __init__(self, traces, sla_limit=480):
        self.traces = traces
        self.sla_limit = sla_limit

    def run(self, rule):
        twin = DigitalTwin(self.traces, rule)
        experimental = twin.simulate()

        analyzer = ImpactAnalyzer(
            baseline=self.traces,
            experimental=experimental,
            sla_limit=self.sla_limit
        )

        return analyzer.analyze()
from src.simulation.digital_twin import DigitalTwin
from src.mining.metrics_engine import MetricsEngine
from src.config_loader import load_sla_rules

class SimulatorRunner:
    def __init__(self, traces):
        self.traces = traces
        self.sla_rules = load_sla_rules()

    def compute_metrics(self, traces):
        metrics = MetricsEngine(traces, self.sla_rules).compute()
        return metrics

    def run(self, rule):
        # Baseline
        baseline_metrics = self.compute_metrics(self.traces)

        # Experimental
        twin = DigitalTwin(self.traces, rule)
        simulated_traces = twin.simulate()
        experimental_metrics = self.compute_metrics(simulated_traces)

        # Delta
        delta = {
            k: experimental_metrics[k] - baseline_metrics[k]
            for k in baseline_metrics
        }

        return baseline_metrics, experimental_metrics, delta
