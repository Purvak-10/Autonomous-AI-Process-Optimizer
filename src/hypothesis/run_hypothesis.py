from src.llm_engine.reasoning_agent import ReasoningAgent
from src.llm_engine.context_builder import ContextBuilder
from src.mining.bottleneck_detector import BottleneckDetector
from src.mining.metrics_engine import MetricsEngine
from src.storage.db_connector import DBConnector
from src.storage.trace_builder import TraceBuilder
from src.config_loader import load_sla_rules
from src.hypothesis.generator import HypothesisGenerator
from src.hypothesis.validity_checker import ValidityChecker
from src.hypothesis.rule_compiler import RuleCompiler

def generate_compiled_rules(verbose=True):
    # Load traces
    db = DBConnector()
    conn = db.get_connection()
    traces = TraceBuilder(conn).build_traces()

    # Metrics
    bottlenecks, avg_durations = BottleneckDetector(traces).detect()
    sla_rules = load_sla_rules()
    metrics = MetricsEngine(traces, sla_rules).compute()

    context = ContextBuilder().build(
        graph_edges={},
        avg_durations=avg_durations,
        bottlenecks=bottlenecks,
        metrics=metrics
    )

    # Phase 4
    root_cause_output = ReasoningAgent().analyze(context)

    # Normalize root cause (LLMs are not strict)
    root_cause = (
        root_cause_output.get("root_cause")
        or root_cause_output.get("category")
        or "Process Design Bottleneck"
    )

    # Phase 5
    generator = HypothesisGenerator()
    hypotheses = generator.generate(
    root_cause=root_cause,
    explanation=root_cause_output.get("explanation", "")
    )


    checker = ValidityChecker()
    safe_hypotheses = checker.filter(hypotheses)

    compiler = RuleCompiler()
    compiled_rules = [compiler.compile(h) for h in safe_hypotheses]

    if verbose:
        print("\nCompiled Rules:")
        for r in compiled_rules:
            print(r)

    return compiled_rules


if __name__ == "__main__":
    generate_compiled_rules(verbose=True)
