# (Main runner for PHASE 6)
from src.storage.db_connector import DBConnector
from src.storage.trace_builder import TraceBuilder
from src.simulation.simulator_runner import SimulatorRunner

def run_simulation(rule_name, approval_threshold=None):
    # Load baseline traces
    db = DBConnector()
    conn = db.get_connection()
    traces = TraceBuilder(conn).build_traces()

    simulator = SimulatorRunner(traces)

    rule = {
        "rule_name": rule_name,
        "approval_threshold": approval_threshold
    }

    baseline, experimental, delta = simulator.run(rule)

    return {
        "baseline": baseline,
        "experimental": experimental,
        "delta": delta
    }


if __name__ == "__main__":
    # Example standalone run
    result = run_simulation("AUTO_APPROVAL", approval_threshold=1000)
    print(result)
