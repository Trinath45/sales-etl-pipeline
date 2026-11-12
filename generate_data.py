"""Creates a messy sample sales CSV (data/raw_sales.csv) so the pipeline has something to clean.
Tip: you can replace this with any real Kaggle sales dataset and adjust the column names in pipeline.py."""
import random
from datetime import date, timedelta
import pandas as pd

random.seed(42)
products = {"Laptop": ("Electronics", 55000), "Phone": ("Electronics", 22000), "Headphones": ("Electronics", 2500),
            "Desk Chair": ("Furniture", 7500), "Bookshelf": ("Furniture", 5200), "Notebook": ("Stationery", 80),
            "Pen Set": ("Stationery", 250)}
regions = ["North", "South", "East", "West"]
customers = ["Asha Rao", "Ravi Kumar", "Meena Iyer", "Kiran Reddy", "Sneha Patel", "Arjun Singh", "Divya Nair", "Rahul Verma"]

rows = []
for i in range(1, 1001):
    prod = random.choice(list(products))
    d = date(2025, 1, 1) + timedelta(days=random.randint(0, 364))
    date_str = d.strftime("%Y-%m-%d") if random.random() < 0.6 else d.strftime("%d-%b-%Y")   # mixed date formats
    cust = random.choice(customers)
    cust = random.choice([cust, cust.upper(), cust.lower(), "  " + cust + " "])                  # messy names
    rows.append({"order_id": 1000 + i, "order_date": date_str, "customer_name": cust,
                 "region": random.choice(regions + [r.lower() for r in regions]),               # inconsistent case
                 "product": prod, "category": products[prod][0],
                 "quantity": random.randint(1, 5) if random.random() > 0.03 else None,           # missing values
                 "unit_price": products[prod][1] if random.random() > 0.02 else None})

df = pd.DataFrame(rows)
df = pd.concat([df, df.sample(30, random_state=1)], ignore_index=True)                           # duplicate rows
df = df.sample(frac=1, random_state=7).reset_index(drop=True)
import os; os.makedirs("data", exist_ok=True)
df.to_csv("data/raw_sales.csv", index=False)
print(f"Created data/raw_sales.csv with {len(df)} rows")
