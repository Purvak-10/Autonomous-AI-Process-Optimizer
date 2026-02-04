# (Make it fast)
# Why indexing matters
# When logs grow to millions of rows:
# Queries slow down
# Dashboards lag
# AI pipelines stall
# Indexes fix this.

class Indexer:
    def __init__(self, conn):
        self.conn = conn

    def create_indexes(self):
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_case ON events(case_id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_step ON events(step)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_time ON events(timestamp)")
