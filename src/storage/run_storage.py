# (Main runner for PHASE 2)

from src.storage.db_connector import DBConnector
from src.storage.trace_builder import TraceBuilder
from src.storage.indexer import Indexer

def run():
    db = DBConnector()
    db.load_csv()

    conn = db.get_connection()

    indexer = Indexer(conn)
    indexer.create_indexes()

    trace_builder = TraceBuilder(conn)
    traces = trace_builder.build_traces()

    print("Total cases reconstructed:", len(traces))

    # Print one sample trace
    sample_case = list(traces.keys())[0]
    print(f"\nSample trace for {sample_case}:")
    for event in traces[sample_case]:
        print(event)

if __name__ == "__main__":
    run()
