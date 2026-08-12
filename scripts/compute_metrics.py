import pandas as pd
import numpy as np
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
BASE = Path(__file__).resolve().parents[1]
PROCESSED = BASE / 'data' / 'processed'
OUTPUTS = BASE / 'outputs'

OUTPUTS.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Load data
# -----------------------------
nav = pd.read_csv(PROCESSED / 'nav_history_clean.csv')
funds = pd.read_csv(PROCESSED / 'fund_master_clean.csv')

nav.columns = nav.columns.str.lower().str.strip()
funds.columns = funds.columns.str.lower().str.strip()

nav['date'] = pd.to_datetime(nav['date'])
nav = nav.sort_values(['amfi_code', 'date'])

# -----------------------------
# Daily returns
# -----------------------------
nav['daily_return'] = nav.groupby('amfi_code')['nav'].pct_change()
returns = nav.dropna(subset=['daily_return']).copy()

# -----------------------------
# Compute metrics
# -----------------------------
results = []

RISK_FREE_RATE = 0.05

for code, df in returns.groupby('amfi_code'):

    r = df['daily_return']

    if len(r) < 30:
        continue

    start_nav = df['nav'].iloc[0]
    end_nav = df['nav'].iloc[-1]
    n = len(r)

    cagr = (end_nav / start_nav) ** (252 / n) - 1
    volatility = r.std() * np.sqrt(252)

    if volatility > 0:
        sharpe = (cagr - RISK_FREE_RATE) / volatility
    else:
        sharpe = np.nan

    wealth = (1 + r).cumprod()
    running_max = wealth.cummax()
    drawdown = wealth / running_max - 1
    max_drawdown = drawdown.min()

    var95 = np.percentile(r, 5)
    cvar95 = r[r <= var95].mean()

    results.append({
        'amfi_code': code,
        'cagr': cagr,
        'volatility': volatility,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_drawdown,
        'var_95': var95,
        'cvar_95': cvar95
    })

# -----------------------------
# Create metrics dataframe
# -----------------------------
metrics = pd.DataFrame(results)

# -----------------------------
# Merge fund names
# -----------------------------
metrics = metrics.merge(
    funds[['amfi_code', 'scheme_name']],
    on='amfi_code',
    how='left'
)

metrics.rename(columns={'scheme_name': 'fund_name'}, inplace=True)

# -----------------------------
# Save outputs
# -----------------------------
metrics[['amfi_code', 'fund_name', 'cagr']]\
    .sort_values('cagr', ascending=False)\
    .to_csv(OUTPUTS / 'cagr_comparison.csv', index=False)

metrics[['amfi_code', 'fund_name', 'sharpe_ratio']]\
    .sort_values('sharpe_ratio', ascending=False)\
    .to_csv(OUTPUTS / 'sharpe_ratio.csv', index=False)

metrics[['amfi_code', 'fund_name', 'max_drawdown']]\
    .to_csv(OUTPUTS / 'drawdown.csv', index=False)

metrics[['amfi_code', 'fund_name', 'var_95', 'cvar_95']]\
    .to_csv(OUTPUTS / 'var_cvar.csv', index=False)

alpha_beta = metrics[['amfi_code', 'fund_name']].copy()
alpha_beta['alpha'] = np.nan
alpha_beta['beta'] = np.nan
alpha_beta.to_csv(OUTPUTS / 'alpha_beta.csv', index=False)

metrics.to_csv(OUTPUTS / 'fund_scorecard.csv', index=False)

print('Outputs generated successfully')
print(metrics.head())