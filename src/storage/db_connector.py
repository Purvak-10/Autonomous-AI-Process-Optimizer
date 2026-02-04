# (Load raw logs into a database)
# Why DuckDB?
# Zero setup
# File-based
# SQL support
# Perfect for analytics
# Used in real data platforms


import duckdb
from pathlib import Path

DB_PATH = Path("data/processed/events.duckdb")
CSV_PATH = Path("data/raw_logs/event_logs.csv")

class DBConnector:
    def __init__(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(DB_PATH)

    def load_csv(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS events AS
            SELECT * FROM read_csv_auto(?)
        """, [str(CSV_PATH)])

    def get_connection(self):
        return self.conn
