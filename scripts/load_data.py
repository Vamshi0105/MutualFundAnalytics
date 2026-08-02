import os
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///bluestock_mf.db"
)

processed = "data/processed"

files = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv"
]

for file in files:

    df = pd.read_csv(
        os.path.join(processed, file)
    )

    table_name = (
    file.replace(".csv", "")
        .split("_", 1)[1]   # Removes)
    )

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    db_rows = pd.read_sql(
        f"SELECT COUNT(*) AS cnt FROM {table_name}",
        engine
    )

    print(f"{table_name}")
    print(f"CSV Rows : {len(df)}")
    print(f"DB Rows  : {db_rows['cnt'][0]}")
    print("-" * 40)

print("All datasets loaded successfully.")