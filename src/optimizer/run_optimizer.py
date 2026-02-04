# (Runs Phase 6 + Phase 7 together)

from src.storage.db_connector import DBConnector
from src.storage.trace_builder import TraceBuilder
from src.hypothesis.run_hypothesis import generate_compiled_rules
from src.simulation.simulator_runner import SimulatorRunner
from src.optimizer.scoring_engine import ScoringEngine

def run():
    # Load baseline traces
    db = DBConnector()
    conn = db.get_connection()
    traces = TraceBuilder(conn).build_traces()

    # Fetch hypotheses
    rules = generate_compiled_rules(verbose=False)

    simulator = SimulatorRunner(traces)
    results = {}

    print("\nRunning simulations...\n")

    for rule in rules:
        baseline, experimental, delta = simulator.run(rule)

        results[rule["rule_name"]] = {
            "baseline": baseline,
            "experimental": experimental,
            "delta": delta
        }

    # Score & rank
    scorer = ScoringEngine(
        w_cycle_time=0.5,
        w_cost=0.3,
        w_sla=0.2
    )

    ranking = scorer.rank(results)

    print("\n=== POLICY RANKING ===\n")
    for r in ranking:
        print(f"Rule: {r['rule']}")
        print(f"Score: {r['score']}")
        print(f"Delta: {r['delta']}")
        print("-" * 40)

    print("\n🏆 SELECTED POLICY:")
    print(ranking[0])
    return {
    "selected": ranking[0],
    "all_results": results,
    "root_cause": "Approval delay due to system design"
}


if __name__ == "__main__":
    run()
