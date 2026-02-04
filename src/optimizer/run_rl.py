# (Train the optimizer)
# This script:
# Uses Digital Twin as environment
# Trains over multiple episodes
# Learns which policy works best

from src.storage.db_connector import DBConnector
from src.storage.trace_builder import TraceBuilder
from src.hypothesis.run_hypothesis import generate_compiled_rules
from src.simulation.simulator_runner import SimulatorRunner
from src.optimizer.scoring_engine import ScoringEngine
from src.optimizer.rl_agent import QLearningAgent

def run(episodes=20):
    # Load traces
    db = DBConnector()
    conn = db.get_connection()
    traces = TraceBuilder(conn).build_traces()

    # Policies
    rules = generate_compiled_rules(verbose=False)
    actions = [r["rule_name"] for r in rules]
    rule_map = {r["rule_name"]: r for r in rules}

    simulator = SimulatorRunner(traces)
    scorer = ScoringEngine()

    agent = QLearningAgent(actions)

    print("\n=== RL TRAINING STARTED ===\n")

    # Initial state (baseline)
    baseline, _, _ = simulator.run(rules[0])
    state = (
        baseline["avg_cycle_time"],
        baseline["avg_cost"],
        baseline["sla_violation_rate"]
    )

    for ep in range(episodes):
        action = agent.choose_action(state)
        rule = rule_map[action]

        baseline, experimental, delta = simulator.run(rule)
        reward = scorer.score(delta)

        next_state = (
            experimental["avg_cycle_time"],
            experimental["avg_cost"],
            experimental["sla_violation_rate"]
        )

        agent.update(state, action, reward, next_state)
        state = next_state

        print(
            f"Episode {ep+1:02d} | "
            f"Action: {action:20s} | "
            f"Reward: {reward:8.2f}"
        )

    print("\n=== LEARNED POLICY VALUES ===\n")
    for (state_key, action), value in agent.q_table.items():
        print(f"{action:20s} → Q-value: {value:.2f}")

if __name__ == "__main__":
    run()
