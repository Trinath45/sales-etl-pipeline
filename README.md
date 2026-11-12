# Sales ETL Pipeline

An automated ETL (Extract, Transform, Load) pipeline built with Python, pandas and SQL (SQLite). It takes a messy raw sales CSV, cleans it, loads it into a SQL database, and answers business questions with SQL queries.

## Pipeline flow
`raw_sales.csv` -> **Extract** (pandas) -> **Transform** (clean) -> **Load** (SQLite) -> **Analyze** (SQL)

## What the Transform step fixes
- Removes duplicate orders
- Drops rows with missing quantity/price
- Standardizes customer names and regions (case, extra spaces)
- Parses mixed date formats into one format
- Adds `total_amount` and `order_month` columns

## SQL analysis (queries.sql)
Revenue by region, top products, month-over-month growth (`LAG`), top customers per region (`RANK`), revenue share by category.

## How to run
```bash
pip install -r requirements.txt
python generate_data.py   # creates sample raw data (or use your own CSV)
python pipeline.py        # runs the ETL pipeline
python run_queries.py     # runs the SQL analysis
```

## Tech stack
Python, pandas, SQL, SQLite, Git

## Possible improvements
Schedule with Airflow, move to PostgreSQL/BigQuery, add data quality checks, add unit tests.
