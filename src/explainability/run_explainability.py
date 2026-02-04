# (Main runner for PHASE 9)

from src.optimizer.run_optimizer import run as run_optimizer
from src.explainability.narrative_generator import NarrativeGenerator
from src.explainability.trust_report import TrustReport

def run():
    # Run optimizer to get best policy
    result = run_optimizer()

    selected = result["selected"]
    all_results = result["all_results"]
    root_cause = result["root_cause"]
    hypotheses = list(all_results.keys())

    # Narrative
    narrator = NarrativeGenerator()
    narrative = narrator.generate(
        policy=selected["rule"],
        impact=selected["delta"]
    )

    print("\n=== EXECUTIVE SUMMARY ===\n")
    print(narrative)

    # Trust Report
    report = TrustReport().build(
        root_cause=root_cause,
        hypotheses=hypotheses,
        simulation_results=all_results,
        selected_policy=selected
    )

    print("\n=== TRUST REPORT ===\n")
    for k, v in report.items():
        print(f"{k.upper()}:\n{v}\n")

if __name__ == "__main__":
    run()
