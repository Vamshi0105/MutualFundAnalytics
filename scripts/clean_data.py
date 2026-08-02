import os
import pandas as pd

RAW = "data/raw"
PROCESSED = "data/processed"

os.makedirs(PROCESSED, exist_ok=True)

# --------------------------
# 1. Fund Master
# --------------------------
fund = pd.read_csv(f"{RAW}/01_fund_master.csv")

fund["launch_date"] = pd.to_datetime(
    fund["launch_date"],
    errors="coerce"
)

fund = fund.drop_duplicates()

fund.to_csv(
    f"{PROCESSED}/01_fund_master.csv",
    index=False
)

# --------------------------
# 2. NAV History
# --------------------------
nav = pd.read_csv(f"{RAW}/02_nav_history.csv")

nav["date"] = pd.to_datetime(
    nav["date"],
    errors="coerce"
)

nav = nav.sort_values(
    ["amfi_code", "date"]
)

nav = nav.drop_duplicates(
    subset=["amfi_code", "date"]
)

nav["nav"] = (
    nav.groupby("amfi_code")["nav"]
       .ffill()
)

nav = nav[nav["nav"] > 0]

nav.to_csv(
    f"{PROCESSED}/02_nav_history.csv",
    index=False
)

# --------------------------
# 3. AUM
# --------------------------
aum = pd.read_csv(f"{RAW}/03_aum_by_fund_house.csv")

aum["date"] = pd.to_datetime(
    aum["date"]
)

aum = aum.drop_duplicates()

aum.to_csv(
    f"{PROCESSED}/03_aum_by_fund_house.csv",
    index=False
)

# --------------------------
# 4. SIP Inflows
# --------------------------
sip = pd.read_csv(f"{RAW}/04_monthly_sip_inflows.csv")

sip["month"] = pd.to_datetime(
    sip["month"]
)

sip.to_csv(
    f"{PROCESSED}/04_monthly_sip_inflows.csv",
    index=False
)

# --------------------------
# 5. Category Inflows
# --------------------------
cat = pd.read_csv(f"{RAW}/05_category_inflows.csv")

cat["month"] = pd.to_datetime(
    cat["month"]
)

cat.to_csv(
    f"{PROCESSED}/05_category_inflows.csv",
    index=False
)

# --------------------------
# 6. Industry Folios
# --------------------------
folio = pd.read_csv(f"{RAW}/06_industry_folio_count.csv")

folio["month"] = pd.to_datetime(
    folio["month"]
)

folio.to_csv(
    f"{PROCESSED}/06_industry_folio_count.csv",
    index=False
)

# --------------------------
# 7. Scheme Performance
# --------------------------
perf = pd.read_csv(f"{RAW}/07_scheme_performance.csv")

returns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct"
]

for col in returns:
    perf[col] = pd.to_numeric(
        perf[col],
        errors="coerce"
    )

perf["expense_flag"] = ~perf[
    "expense_ratio_pct"
].between(0.1, 2.5)

perf.to_csv(
    f"{PROCESSED}/07_scheme_performance.csv",
    index=False
)

# --------------------------
# 8. Transactions
# --------------------------
tx = pd.read_csv(
    f"{RAW}/08_investor_transactions.csv"
)

tx["transaction_date"] = pd.to_datetime(
    tx["transaction_date"]
)

tx["transaction_type"] = (
    tx["transaction_type"]
    .str.strip()
    .str.title()
)

tx["transaction_type"] = (
    tx["transaction_type"]
    .replace({
        "Sip": "SIP",
        "Lumpsum": "Lumpsum",
        "Redemption": "Redemption"
    })
)

tx = tx[
    tx["amount_inr"] > 0
]

valid = [
    "Verified",
    "Pending",
    "Rejected"
]

tx["kyc_status"] = tx["kyc_status"].where(
    tx["kyc_status"].isin(valid),
    "Pending"
)

tx.to_csv(
    f"{PROCESSED}/08_investor_transactions.csv",
    index=False
)

# --------------------------
# 9. Portfolio
# --------------------------
portfolio = pd.read_csv(
    f"{RAW}/09_portfolio_holdings.csv"
)

portfolio["portfolio_date"] = pd.to_datetime(
    portfolio["portfolio_date"]
)

portfolio.to_csv(
    f"{PROCESSED}/09_portfolio_holdings.csv",
    index=False
)

# --------------------------
# 10. Benchmark
# --------------------------
benchmark = pd.read_csv(
    f"{RAW}/10_benchmark_indices.csv"
)

benchmark["date"] = pd.to_datetime(
    benchmark["date"]
)

benchmark.to_csv(
    f"{PROCESSED}/10_benchmark_indices.csv",
    index=False
)

print("All 10 datasets cleaned successfully.")