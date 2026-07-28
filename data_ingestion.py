import os
import pandas as pd

# -------------------------------
# Folder Paths
# -------------------------------
RAW_FOLDER = "data/raw"
REPORT_FOLDER = "reports"

os.makedirs(REPORT_FOLDER, exist_ok=True)

# -------------------------------
# Dataset List
# -------------------------------
datasets = [
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

summary = []

print("=" * 80)
print("BLUESTOCK CAPSTONE - DAY 1 DATA INGESTION")
print("=" * 80)

# -------------------------------
# Read Every CSV
# -------------------------------
for file in datasets:

    path = os.path.join(RAW_FOLDER, file)

    print("\n")
    print("=" * 80)
    print(file)
    print("=" * 80)

    df = pd.read_csv(path)

    print("\nShape")
    print(df.shape)

    print("\nColumns")
    print(df.columns.tolist())

    print("\nData Types")
    print(df.dtypes)

    print("\nHead")
    print(df.head())

    print("\nMissing Values")
    print(df.isnull().sum())

    print("\nDuplicate Rows")
    print(df.duplicated().sum())

    summary.append({
        "Dataset": file,
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum())
    })

# -------------------------------
# Dataset Summary
# -------------------------------
summary_df = pd.DataFrame(summary)

summary_df.to_csv(
    os.path.join(REPORT_FOLDER, "dataset_summary.csv"),
    index=False
)

print("\n")
print("=" * 80)
print("DATASET SUMMARY")
print("=" * 80)

print(summary_df)

# -------------------------------
# Fund Master Exploration
# -------------------------------
print("\n")
print("=" * 80)
print("FUND MASTER ANALYSIS")
print("=" * 80)

fund_master = pd.read_csv(
    os.path.join(RAW_FOLDER, "01_fund_master.csv")
)

print("\nUnique Fund Houses")

if "fund_house" in fund_master.columns:
    print(sorted(fund_master["fund_house"].unique()))

print("\nUnique Categories")

if "category" in fund_master.columns:
    print(sorted(fund_master["category"].unique()))

print("\nUnique Sub Categories")

for col in fund_master.columns:

    if "sub" in col.lower():

        print(sorted(fund_master[col].dropna().unique()))

print("\nRisk Grades")

for col in fund_master.columns:

    if "risk" in col.lower():

        print(sorted(fund_master[col].dropna().unique()))

# -------------------------------
# Validate AMFI Codes
# -------------------------------
print("\n")
print("=" * 80)
print("AMFI CODE VALIDATION")
print("=" * 80)

nav = pd.read_csv(
    os.path.join(RAW_FOLDER, "02_nav_history.csv")
)

amfi_master = None
amfi_nav = None

for col in fund_master.columns:

    if "amfi" in col.lower():

        amfi_master = col
        break

for col in nav.columns:

    if "amfi" in col.lower():

        amfi_nav = col
        break

if amfi_master and amfi_nav:

    missing = set(
        fund_master[amfi_master]
    ) - set(
        nav[amfi_nav]
    )

    print("Missing Codes:", len(missing))

    if len(missing):

        print(missing)

    with open(
        os.path.join(REPORT_FOLDER, "amfi_validation_report.txt"),
        "w"
    ) as f:

        f.write("AMFI Validation Report\n\n")

        f.write(f"Missing Codes : {len(missing)}\n")

        for code in missing:
            f.write(str(code) + "\n")

else:

    print("AMFI code column not found automatically.")

# -------------------------------
# Data Quality Report
# -------------------------------
with open(
    os.path.join(REPORT_FOLDER, "data_quality_summary.txt"),
    "w"
) as f:

    f.write("Bluestock Capstone\n")
    f.write("\nData Quality Summary\n\n")

    for row in summary:

        f.write(
            f"{row['Dataset']} -> "
            f"Rows={row['Rows']}, "
            f"Columns={row['Columns']}, "
            f"Missing={row['Missing Values']}, "
            f"Duplicates={row['Duplicate Rows']}\n"
        )

print("\n")
print("=" * 80)
print("ALL REPORTS GENERATED SUCCESSFULLY")
print("=" * 80)