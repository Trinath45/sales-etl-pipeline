"""ETL pipeline: raw sales CSV -> cleaned data -> SQLite database."""
import logging
import sqlite3
import pandas as pd

RAW_PATH = "data/raw_sales.csv"
DB_PATH = "data/sales.db"
DATE_FORMATS = ["%Y-%m-%d", "%d-%b-%Y"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("etl")


def extract(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    log.info("Extracted %d rows from %s", len(df), path)
    return df


def parse_date(value):
    for fmt in DATE_FORMATS:
        try:
            return pd.to_datetime(value, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT


def transform(df: pd.DataFrame) -> pd.DataFrame:
    start = len(df)

    df = df.drop_duplicates(subset="order_id")                      # 1. remove duplicates
    log.info("Removed %d duplicate rows", start - len(df))

    before = len(df)
    df = df.dropna(subset=["quantity", "unit_price"])               # 2. drop rows with missing numbers
    log.info("Dropped %d rows with missing quantity/price", before - len(df))

    df["customer_name"] = df["customer_name"].str.strip().str.title()   # 3. standardize text
    df["region"] = df["region"].str.strip().str.title()

    df["order_date"] = df["order_date"].apply(parse_date)           # 4. fix data types
    df = df.dropna(subset=["order_date"])
    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)

    df["total_amount"] = df["quantity"] * df["unit_price"]          # 5. derived columns
    df["order_month"] = df["order_date"].dt.strftime("%Y-%m")
    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")

    log.info("Transform complete: %d clean rows", len(df))
    return df.reset_index(drop=True)


def load(df: pd.DataFrame, db_path: str) -> None:
    with sqlite3.connect(db_path) as conn:
        df.to_sql("sales", conn, if_exists="replace", index=False)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_region ON sales(region)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_month ON sales(order_month)")
    log.info("Loaded %d rows into %s (table: sales)", len(df), db_path)


def run() -> None:
    load(transform(extract(RAW_PATH)), DB_PATH)
    log.info("Pipeline finished successfully")


if __name__ == "__main__":
    run()
