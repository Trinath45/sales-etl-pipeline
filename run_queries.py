"""Runs every query in queries.sql against the database and prints the results."""
import sqlite3
import pandas as pd

with open("queries.sql") as f:
    blocks = [b.strip() for b in f.read().split("-- Q") if b.strip()]

with sqlite3.connect("data/sales.db") as conn:
    for block in blocks:
        title, _, query = block.partition("\n")
        print(f"\n=== Q{title} ===")
        print(pd.read_sql_query(query, conn).to_string(index=False))
