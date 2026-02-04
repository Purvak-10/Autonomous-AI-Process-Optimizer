from src.simulation.run_simulation import run_simulation

def simulate_threshold(threshold):
    return run_simulation(
        rule_name="AUTO_APPROVAL",
        approval_threshold=threshold
    )
