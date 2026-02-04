print(">>> run_reasoning.py STARTED <<<")

from src.storage.db_connector import DBConnector
from src.storage.trace_builder import TraceBuilder
from src.mining.graph_builder import ProcessGraphBuilder
from src.mining.bottleneck_detector import BottleneckDetector
from src.mining.metrics_engine import MetricsEngine
from src.config_loader import load_sla_rules
from src.llm_engine.context_builder import ContextBuilder
from src.llm_engine.reasoning_agent import ReasoningAgent

def run():
    print(">>> run() FUNCTION ENTERED <<<")

    db = DBConnector()
    conn = db.get_connection()
    traces = TraceBuilder(conn).build_traces()

    print(f">>> Loaded {len(traces)} traces <<<")

    graph = ProcessGraphBuilder(traces).build()
    bottlenecks, avg_durations = BottleneckDetector(traces).detect()

    graph_edges = {
        f"{u}->{v}": data["count"]
        for u, v, data in graph.edges(data=True)
    }

    sla_rules = load_sla_rules()
    metrics = MetricsEngine(traces, sla_rules).compute()

    context = ContextBuilder().build(
        graph_edges=graph_edges,
        avg_durations=avg_durations,
        bottlenecks=bottlenecks,
        metrics=metrics
    )

    agent = ReasoningAgent()
    result = agent.analyze(context)

    print(">>> FINAL RESULT <<<")
    print(result)

if __name__ == "__main__":
    print(">>> __main__ BLOCK <<<")
    run()
