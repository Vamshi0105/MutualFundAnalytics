import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PROCESSED = BASE / 'data' / 'processed'
OUTPUTS = BASE / 'outputs'
OUTPUTS.mkdir(exist_ok=True)

# Load cleaned NAV data
nav = pd.read_csv(PROCESSED / 'nav_history_clean.csv')
nav['date'] = pd.to_datetime(nav['date'])

# Sort and calculate returns
nav = nav.sort_values(['amfi_code', 'date'])
nav['daily_return'] = nav.groupby('amfi_code')['nav'].pct_change()

# Metrics
scorecard = (
    nav.groupby('amfi_code')['daily_return']
       .agg(avg_return='mean', volatility='std')
       .reset_index()
)

scorecard['cagr'] = scorecard['avg_return'] * 252
scorecard['volatility'] = scorecard['volatility'] * (252 ** 0.5)
scorecard['sharpe_ratio'] = scorecard['cagr'] / scorecard['volatility']
scorecard['max_drawdown'] = -0.15  # placeholder

# Save
scorecard.to_csv(OUTPUTS / 'fund_scorecard.csv', index=False)

print('Created:', OUTPUTS / 'fund_scorecard.csv')
print(scorecard.head())