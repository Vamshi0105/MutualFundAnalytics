import pandas as pd
import numpy as np
from scipy.stats import linregress
from pathlib import Path

# ==========================
# Paths
# ==========================
BASE = Path("./data/Processed")  # same folder as the CSV files
OUTPUT = BASE / "outputs"
OUTPUT.mkdir(exist_ok=True)

# ==========================
# Load data
# ==========================
fund_master = pd.read_csv(BASE / "01_fund_master.csv")
nav = pd.read_csv(BASE / "02_nav_history.csv")
benchmark = pd.read_csv(BASE / "10_benchmark_indices.csv")

# Date formatting
nav["date"] = pd.to_datetime(nav["date"])
benchmark["date"] = pd.to_datetime(benchmark["date"])

# Sort
nav = nav.sort_values(["amfi_code", "date"])

# Merge scheme names
nav = nav.merge(
    fund_master[["amfi_code", "scheme_name"]],
    on="amfi_code",
    how="left"
)

# ==========================
# Daily returns
# ==========================
nav["daily_return"] = nav.groupby("amfi_code")["nav"].pct_change()

# ==========================
# Distribution summary
# ==========================
distribution = (
    nav.groupby(["amfi_code", "scheme_name"])["daily_return"]
    .agg(
        mean_daily_return="mean",
        std_daily_return="std",
        min_return="min",
        max_return="max"
    )
    .reset_index()
)

distribution.to_csv(
    OUTPUT / "distribution_summary.csv",
    index=False
)

# ==========================
# CAGR
# ==========================
def calculate_cagr(df, years):
    end_date = df["date"].max()
    start_date = end_date - pd.DateOffset(years=years)

    temp = df[df["date"] >= start_date]

    if len(temp) < 2:
        return np.nan

    start_nav = temp["nav"].iloc[0]
    end_nav = temp["nav"].iloc[-1]

    return (end_nav / start_nav) ** (1 / years) - 1


cagr_results = []

for (code, name), df in nav.groupby(["amfi_code", "scheme_name"]):
    cagr_results.append({
        "amfi_code": code,
        "scheme_name": name,
        "CAGR_1Y": calculate_cagr(df, 1),
        "CAGR_3Y": calculate_cagr(df, 3),
        "CAGR_5Y": calculate_cagr(df, 5)
    })

cagr_df = pd.DataFrame(cagr_results)
cagr_df.to_csv(
    OUTPUT / "cagr_comparison.csv",
    index=False
)

# ==========================
# Sharpe Ratio
# ==========================
RF = 0.065
RF_DAILY = RF / 252

sharpe_results = []

for (code, name), df in nav.groupby(["amfi_code", "scheme_name"]):
    r = df["daily_return"].dropna()

    if len(r) < 2 or r.std() == 0:
        sharpe = np.nan
    else:
        sharpe = ((r.mean() - RF_DAILY) / r.std()) * np.sqrt(252)

    sharpe_results.append({
        "amfi_code": code,
        "scheme_name": name,
        "Sharpe": sharpe
    })

sharpe_df = (
    pd.DataFrame(sharpe_results)
    .sort_values("Sharpe", ascending=False)
)

sharpe_df.to_csv(
    OUTPUT / "sharpe_ratio.csv",
    index=False
)

# ==========================
# Alpha & Beta vs NIFTY100
# ==========================
nifty100 = benchmark[
    benchmark["index_name"] == "NIFTY100"
].copy()

nifty100.rename(
    columns={"close_value": "market_nav"},
    inplace=True
)

nifty100["market_return"] = nifty100["market_nav"].pct_change()

alpha_beta = []

for (code, name), df in nav.groupby(["amfi_code", "scheme_name"]):
    merged = df.merge(
        nifty100[["date", "market_return"]],
        on="date",
        how="inner"
    )

    merged = merged.dropna()

    if len(merged) < 2:
        alpha = beta = r2 = np.nan
    else:
        slope, intercept, r, p, se = linregress(
            merged["market_return"],
            merged["daily_return"]
        )

        alpha = intercept * 252
        beta = slope
        r2 = r ** 2

    alpha_beta.append({
        "amfi_code": code,
        "scheme_name": name,
        "Alpha": alpha,
        "Beta": beta,
        "R_squared": r2
    })

alpha_beta_df = pd.DataFrame(alpha_beta)

alpha_beta_df.to_csv(
    OUTPUT / "alpha_beta.csv",
    index=False
)

# ==========================
# Maximum Drawdown
# ==========================
drawdowns = []

for (code, name), df in nav.groupby(["amfi_code", "scheme_name"]):
    running_max = df["nav"].cummax()
    dd = df["nav"] / running_max - 1

    end_idx = dd.idxmin()
    end_date = df.loc[end_idx, "date"]

    peak_idx = df.loc[:end_idx, "nav"].idxmax()
    start_date = df.loc[peak_idx, "date"]

    drawdowns.append({
        "amfi_code": code,
        "scheme_name": name,
        "Max_Drawdown": dd.min(),
        "Drawdown_Start": start_date,
        "Drawdown_End": end_date
    })

drawdown_df = pd.DataFrame(drawdowns)

drawdown_df.to_csv(
    OUTPUT / "drawdown.csv",
    index=False
)

# ==========================
# Summary
# ==========================
print("Analytics completed successfully!")
print(f"Funds processed: {nav['amfi_code'].nunique()}")
print(f"Outputs saved in: {OUTPUT}")

print("Top 10 Sharpe Ratios:")
print(sharpe_df.head(10))

print("Top 10 CAGR (5Y):")
print(
    cagr_df.sort_values(
        "CAGR_5Y",
        ascending=False
    ).head(10)
)
from pathlib import Path

# Get the folder where this Python script is located
BASE = Path(__file__).resolve().parent

OUTPUT = BASE / "outputs"
OUTPUT.mkdir(parents=True, exist_ok=True)

print("Script location:", BASE)
print("Output location:", OUTPUT)
distribution.to_csv(OUTPUT / "distribution_summary.csv", index=False)
print("Saved:", OUTPUT / "distribution_summary.csv")

cagr_df.to_csv(OUTPUT / "cagr_comparison.csv", index=False)
print("Saved:", OUTPUT / "cagr_comparison.csv")

sharpe_df.to_csv(OUTPUT / "sharpe_ratio.csv", index=False)
print("Saved:", OUTPUT / "sharpe_ratio.csv")

alpha_beta_df.to_csv(OUTPUT / "alpha_beta.csv", index=False)
print("Saved:", OUTPUT / "alpha_beta.csv")

drawdown_df.to_csv(OUTPUT / "drawdown.csv", index=False)
print("Saved:", OUTPUT / "drawdown.csv")
distribution.to_csv(OUTPUT / "distribution_summary.csv", index=False)
print("Saved:", OUTPUT / "distribution_summary.csv")

cagr_df.to_csv(OUTPUT / "cagr_comparison.csv", index=False)
print("Saved:", OUTPUT / "cagr_comparison.csv")

sharpe_df.to_csv(OUTPUT / "sharpe_ratio.csv", index=False)
print("Saved:", OUTPUT / "sharpe_ratio.csv")

alpha_beta_df.to_csv(OUTPUT / "alpha_beta.csv", index=False)
print("Saved:", OUTPUT / "alpha_beta.csv")

drawdown_df.to_csv(OUTPUT / "drawdown.csv", index=False)
print("Saved:", OUTPUT / "drawdown.csv")
print("Distribution rows:", len(distribution))
print("CAGR rows:", len(cagr_df))
print("Sharpe rows:", len(sharpe_df))
print("Alpha/Beta rows:", len(alpha_beta_df))
print("Drawdown rows:", len(drawdown_df))