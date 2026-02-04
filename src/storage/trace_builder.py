# (Reconstruct full workflows)
# What this does
# Groups events by case_id
# Sorts them by timestamp
# Builds a trace = ordered list of steps

from collections import defaultdict

class TraceBuilder:
    def __init__(self, conn):
        self.conn = conn

    def build_traces(self):
        rows = self.conn.execute("""
            SELECT case_id, step, timestamp, actor, duration_minutes, cost
            FROM events
            ORDER BY case_id, timestamp
        """).fetchall()

        traces = defaultdict(list)

        for row in rows:
            case_id = row[0]
            traces[case_id].append({
                "step": row[1],
                "timestamp": row[2],
                "actor": row[3],
                "duration": row[4],
                "cost": row[5]
            })

        return traces
