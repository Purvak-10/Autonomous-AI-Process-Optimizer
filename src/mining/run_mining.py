# (Main runner for PHASE 3)

from src.storage.db_connector import DBConnector
from src.storage.trace_builder import TraceBuilder
from src.mining.graph_builder import ProcessGraphBuilder
from src.mining.bottleneck_detector import BottleneckDetector
from src.mining.metrics_engine import MetricsEngine
from src.config_loader import load_sla_rules

def run():
    # Load traces
    db = DBConnector()
    conn = db.get_connection()
    traces = TraceBuilder(conn).build_traces()

    # Build process graph
    graph = ProcessGraphBuilder(traces).build()

    print("Process Graph Edges (with frequency):")
    for u, v, data in graph.edges(data=True):
        print(f"{u} → {v} : {data['count']}")

    # Detect bottlenecks
    bottlenecks, avg_durations = BottleneckDetector(traces).detect()

    print("\nAverage Duration per Step:")
    for step, avg in avg_durations.items():
        print(f"{step}: {round(avg, 2)} mins")

    print("\nDetected Bottlenecks:")
    for step, avg in bottlenecks.items():
        print(f"{step}: {round(avg, 2)} mins")

    # Metrics
    sla_rules = load_sla_rules()
    metrics = MetricsEngine(traces, sla_rules).compute()

    print("\nBaseline Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {round(v, 2)}")

if __name__ == "__main__":
    run()
