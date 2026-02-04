# (Main runner for PHASE 1)
# Purpose:
# Ties everything together
# Generates thousands of tickets
# Produces real-looking logs

import random
from datetime import datetime, timedelta
from src.config_loader import load_company_config
from src.generator.workflow_engine import WorkflowEngine
from src.generator.actor_simulator import ActorSimulator
from src.generator.anomaly_injector import AnomalyInjector
from src.generator.log_writer import LogWriter


def run(num_cases=1000):
    config = load_company_config()
    workflow = WorkflowEngine(config)
    actor_sim = ActorSimulator(config)
    anomaly = AnomalyInjector()
    writer = LogWriter()

    for i in range(num_cases):
        case_id = f"TICKET_{i}"

        # ✅ STEP 1: Ticket-level business value
        ticket_value = random.randint(100, 5000)

        current_step = "Created"
        current_time = datetime.now()

        while current_step:
            actor, delay, cost = actor_sim.simulate_step(current_step)
            delay = anomaly.apply(current_step, actor, delay)

            current_time += timedelta(minutes=delay)

            # ✅ STEP 2: Attach ticket_value to every event
            writer.write({
                "case_id": case_id,
                "step": current_step,
                "timestamp": current_time.isoformat(),
                "actor": actor,
                "duration_minutes": delay,
                "cost": cost,
                "ticket_value": ticket_value
            })

            if current_step == "Closed":
                break

            current_step = workflow.get_next_step(current_step)


if __name__ == "__main__":
    run(num_cases=2000)
